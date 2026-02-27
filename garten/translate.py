"""Translation generation module.

Generates and regenerates translation files for articles and pages
using the OpenAI-powered translation service. Uses SHA-256 hashing
to detect stale translations and skip up-to-date ones.
"""

from __future__ import annotations

import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path

from .utils import get_logger, parse_frontmatter, strip_frontmatter

logger = get_logger("translate")


def _compute_source_hash(path: Path) -> str:
    """Compute SHA-256 hash of a source file's contents."""
    content = path.read_bytes()
    return hashlib.sha256(content).hexdigest()


def _get_stored_hash(translation_path: Path) -> str:
    """Extract source_hash from a translation file's frontmatter."""
    if not translation_path.exists():
        return ""
    text = translation_path.read_text(encoding="utf-8")
    meta = parse_frontmatter(text)
    return meta.get("source_hash", "")


def _needs_translation(
    source_path: Path, translation_path: Path, force: bool
) -> bool:
    """Check whether a translation file needs to be (re)generated."""
    if force:
        return True
    if not translation_path.exists():
        return True
    current_hash = _compute_source_hash(source_path)
    stored_hash = _get_stored_hash(translation_path)
    return current_hash != stored_hash


def _write_translation_file(
    path: Path,
    source_meta: dict,
    translated_text: str,
    source_hash: str,
    target_lang: str,
    source_lang: str,
    model: str,
) -> None:
    """Write a translation file with proper frontmatter."""
    # Parse frontmatter from the translated text (the API returns full markdown
    # including frontmatter with translated title, excerpt, tags, etc.)
    trans_meta = parse_frontmatter(translated_text)
    trans_body = strip_frontmatter(translated_text)

    # Build frontmatter from translated metadata, falling back to source
    title = trans_meta.get("title", source_meta.get("title", ""))
    image = source_meta.get("image", "")
    excerpt = trans_meta.get("excerpt") or trans_meta.get("summary") or ""
    tags = trans_meta.get("tags", source_meta.get("tags", ""))
    date = source_meta.get("date", "")

    lines = ["---"]
    if date:
        lines.append(f"date: {date}")
    if image:
        lines.append(f"image: {image}")
    if excerpt:
        lines.append(f"excerpt: {excerpt}")
    if title:
        lines.append(f"title: {title}")
    if tags:
        lines.append(f"tags: {tags}")
    lines.append(f"translation: {target_lang}")
    lines.append(f"source_language: {source_lang}")
    lines.append(f"source_hash: {source_hash}")
    lines.append(f"translator: {model}")
    lines.append(f"translate_date: {datetime.now(timezone.utc).isoformat()}")
    lines.append("generated_by: simplified-translation-system")
    lines.append("---")
    lines.append("")

    # If the API returned text without frontmatter, use the whole translated
    # text as the body.
    body = trans_body if trans_body.strip() else translated_text
    lines.append(body)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _find_content_files(content_path: Path, cfg: dict) -> list[Path]:
    """Find all translatable content files (articles and pages)."""
    translation_cfg = cfg.get("translation", {})
    exclude_categories = translation_cfg.get("exclude_categories", ["recipes"])
    exclude_paths = translation_cfg.get("exclude_paths", ["/pages/impressum/"])

    article_paths = cfg.get("article_paths", ["articles"])
    page_paths = cfg.get("page_paths", ["pages"])

    files: list[Path] = []
    for sub in article_paths + page_paths:
        base_dir = content_path / sub
        if not base_dir.is_dir():
            continue
        for md in sorted(base_dir.rglob("*.md")):
            # Skip files inside extensions/ or attachments/
            rel_parts = md.relative_to(base_dir).parts
            if "extensions" in rel_parts or "attachments" in rel_parts:
                continue
            # Check category exclusion (first dir component is the category
            # for articles, but pages don't have categories — they use paths)
            skip = False
            for exc_cat in exclude_categories:
                if f"/{exc_cat}/" in str(md) or str(md).endswith(f"/{exc_cat}"):
                    skip = True
                    break
            for exc_path in exclude_paths:
                # e.g. /pages/impressum/ should match content/pages/impressum/
                clean = exc_path.strip("/")
                if clean in str(md.relative_to(content_path)):
                    skip = True
                    break
            if not skip:
                files.append(md)

    return files


def translate_content(
    cfg: dict, dry_run: bool = False, force: bool = False
) -> dict:
    """Translate all content files that need translation.

    Args:
        cfg: Site configuration dict (from load_config).
        dry_run: If True, report what would be translated without calling API.
        force: If True, regenerate all translations regardless of hash match.

    Returns:
        Stats dict with counts: translated, skipped, failed, total.
    """
    from extensions.translation_service import TranslationConfig, TranslationService

    content_path: Path = cfg["content_path"]
    translation_cfg = cfg.get("translation", {})
    target_languages = translation_cfg.get("target_languages", ["de", "fr"])
    default_lang = cfg.get("default_lang", "en")

    # Find all content files to process
    source_files = _find_content_files(content_path, cfg)
    logger.info(f"Found {len(source_files)} content files to check")

    stats = {"translated": 0, "skipped": 0, "failed": 0, "total": 0}

    if dry_run:
        # Just report what would be translated
        for source_path in source_files:
            stem = source_path.stem
            ext_dir = source_path.parent / "extensions"
            for lang in target_languages:
                # Skip if target language matches source language
                if lang == default_lang:
                    continue
                trans_path = ext_dir / f"{stem}-{lang.upper()}.md"
                stats["total"] += 1
                if _needs_translation(source_path, trans_path, force):
                    status = "STALE" if trans_path.exists() else "MISSING"
                    logger.info(
                        f"[{status}] {source_path.name} -> {lang.upper()}"
                    )
                    stats["translated"] += 1
                else:
                    stats["skipped"] += 1
        logger.info(
            f"Dry run: {stats['translated']} need translation, "
            f"{stats['skipped']} up-to-date"
        )
        return stats

    # Initialize translation service
    svc_config = TranslationConfig.from_dotenv()
    svc_config.target_languages = target_languages
    service = TranslationService(svc_config)

    for source_path in source_files:
        source_text = source_path.read_text(encoding="utf-8")
        source_meta = parse_frontmatter(source_text)
        source_hash = _compute_source_hash(source_path)
        stem = source_path.stem
        ext_dir = source_path.parent / "extensions"

        # Detect source language
        body = strip_frontmatter(source_text)
        source_lang = service.detect_language(body)

        # Determine which languages to translate into
        langs_for_file = []
        for lang in target_languages:
            if lang == source_lang:
                continue
            langs_for_file.append(lang)
        # If source is not default lang, also translate to default lang
        if source_lang != default_lang and default_lang not in langs_for_file:
            langs_for_file.append(default_lang)

        for lang in langs_for_file:
            trans_path = ext_dir / f"{stem}-{lang.upper()}.md"
            stats["total"] += 1

            if not _needs_translation(source_path, trans_path, force):
                stats["skipped"] += 1
                continue

            action = "Regenerating" if trans_path.exists() else "Translating"
            logger.info(
                f"{action} {source_path.name} -> {lang.upper()}"
            )

            try:
                result = service.translate_content(
                    source_text, source_lang, lang
                )
                _write_translation_file(
                    path=trans_path,
                    source_meta=source_meta,
                    translated_text=result.translation,
                    source_hash=source_hash,
                    target_lang=lang,
                    source_lang=source_lang,
                    model=result.model or svc_config.model,
                )
                stats["translated"] += 1
                # Rate limiting between API calls
                time.sleep(svc_config.rate_limit_delay)

            except Exception as e:
                logger.error(
                    f"Failed to translate {source_path.name} -> "
                    f"{lang.upper()}: {e}"
                )
                stats["failed"] += 1

    logger.info(
        f"Translation complete: {stats['translated']} translated, "
        f"{stats['skipped']} skipped, {stats['failed']} failed"
    )
    return stats

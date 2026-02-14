"""Phase 1: Content discovery.

Sub-phases:
    1.1  Scan content directories
    1.2  Parse frontmatter
    1.3  Auto-title from directory names
    1.4  Assign categories from directory structure
    1.5  Find translation files in extensions/
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from .models import Article, Page, Recipe
from .utils import get_logger, normalize_slug, slugify

logger = get_logger("discover")


# ---------------------------------------------------------------------------
# 1.2  Frontmatter parsing
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str]:
    """Parse YAML-style frontmatter between ``---`` markers.

    Returns a dict with **lowercase** keys.  Values are raw strings;
    type coercion happens in the caller.
    """
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}

    meta: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip().lower()
        value = value.strip()
        # Strip surrounding quotes
        if len(value) >= 2 and value[0] in ('"', "'") and value[-1] == value[0]:
            value = value[1:-1]
        meta[key] = value
    return meta


# ---------------------------------------------------------------------------
# 1.3  Auto-title from directory names
# ---------------------------------------------------------------------------

_DATE_PREFIX_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-")
_YEAR_MONTH_PREFIX_RE = re.compile(r"^(\d{4})-(\d{2})-")


def title_from_dirname(dirname: str) -> str:
    """Derive a human title from a content directory name.

    Strips leading date prefixes like ``2025-04-18-`` and converts
    hyphens/underscores to spaces with title-casing.
    """
    name = dirname
    # Try YYYY-MM-DD- first (most common)
    if _DATE_PREFIX_RE.match(name):
        parts = name.split("-", 3)
        name = parts[3] if len(parts) > 3 else name
    # Fall back to YYYY-MM- prefix
    elif _YEAR_MONTH_PREFIX_RE.match(name):
        parts = name.split("-", 2)
        name = parts[2] if len(parts) > 2 else name

    return name.replace("-", " ").replace("_", " ").title()


def _date_from_dirname(dirname: str) -> datetime | None:
    """Try to extract a date from a date-prefixed directory name."""
    m = _DATE_PREFIX_RE.match(dirname)
    if m:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = _YEAR_MONTH_PREFIX_RE.match(dirname)
    if m:
        return datetime(int(m.group(1)), int(m.group(2)), 1)
    return None


# ---------------------------------------------------------------------------
# Tag parsing
# ---------------------------------------------------------------------------


def _parse_tags(raw: str) -> list[str]:
    """Parse a comma-separated tag string into a list of lowercased, trimmed tags."""
    if not raw:
        return []
    return [t.strip().lower() for t in raw.split(",") if t.strip()]


# ---------------------------------------------------------------------------
# Date parsing
# ---------------------------------------------------------------------------


def _parse_date(raw: str | None) -> datetime | None:
    """Parse various date formats found in content frontmatter."""
    if not raw:
        return None
    raw = raw.strip()
    # ISO 8601 with timezone: 2009-12-13T00:00:00.000Z
    for fmt in (
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    logger.warning(f"Unparseable date: {raw!r}")
    return None


# ---------------------------------------------------------------------------
# 1.1  Scan content directories
# ---------------------------------------------------------------------------


def _find_md_files(base_dir: Path) -> list[Path]:
    """Find all .md files under *base_dir*, excluding extensions/ and attachments/."""
    results: list[Path] = []
    for md in sorted(base_dir.rglob("*.md")):
        # Exclude files inside extensions/ or attachments/ subdirectories
        rel_parts = md.relative_to(base_dir).parts
        if "extensions" in rel_parts or "attachments" in rel_parts:
            continue
        results.append(md)
    return results


# ---------------------------------------------------------------------------
# Build Article / Page / Recipe from a parsed file
# ---------------------------------------------------------------------------


def _build_article(md_path: Path, content_root: Path) -> Article:
    text = md_path.read_text(encoding="utf-8")
    meta = parse_frontmatter(text)
    content_dir = md_path.parent

    # 1.3 Auto-title
    title = meta.get("title", "")
    if not title:
        title = title_from_dirname(content_dir.name)
    # Strip surrounding quotes (Pelican compat)
    if title.startswith('"') and title.endswith('"'):
        title = title[1:-1]

    # 1.4 Category from directory structure
    rel = md_path.relative_to(content_root)
    category = rel.parts[0] if len(rel.parts) > 1 else ""

    # Slug: derived from title (matching Pelican's SLUGIFY_SOURCE = "title")
    slug = slugify(title)

    # "summary" and "excerpt" map to the same field
    excerpt = meta.get("excerpt") or meta.get("summary") or None

    # Date: frontmatter > directory name > file mtime
    date = _parse_date(meta.get("date"))
    if date is None:
        date = _date_from_dirname(content_dir.name)
    if date is None:
        date = datetime.fromtimestamp(md_path.stat().st_mtime)

    return Article(
        title=title,
        date=date,
        tags=_parse_tags(meta.get("tags", "")),
        excerpt=excerpt,
        image=meta.get("image") or None,
        updates=meta.get("updates") or None,
        status=meta.get("status", "published"),
        slug=slug,
        category=category,
        source_path=md_path,
        content_dir=content_dir,
    )


def _build_page(md_path: Path, content_root: Path) -> Page:
    text = md_path.read_text(encoding="utf-8")
    meta = parse_frontmatter(text)
    content_dir = md_path.parent

    title = meta.get("title", "")
    if not title:
        title = title_from_dirname(content_dir.name)
    if title.startswith('"') and title.endswith('"'):
        title = title[1:-1]

    # Slug: explicit metadata wins, else derive from title
    raw_slug = meta.get("slug", "")
    slug = normalize_slug(raw_slug) if raw_slug else slugify(title)

    return Page(
        title=title,
        date=_parse_date(meta.get("date")),
        slug=slug,
        status=meta.get("status", "published"),
        image=meta.get("image") or None,
        source_path=md_path,
        content_dir=content_dir,
    )


def _build_recipe(md_path: Path, content_root: Path) -> Recipe:
    text = md_path.read_text(encoding="utf-8")
    meta = parse_frontmatter(text)
    content_dir = md_path.parent

    title = meta.get("title", "")
    if not title:
        # Derive from filename
        title = md_path.stem.replace("-", " ").replace("_", " ").title()

    # Slug: explicit metadata wins, else derive from filename
    raw_slug = meta.get("slug", "") or md_path.stem
    slug = normalize_slug(raw_slug)

    # "summary" and "excerpt" map to the same field
    excerpt = meta.get("excerpt") or meta.get("summary") or None

    return Recipe(
        title=title,
        layout=meta.get("layout", "recipe"),
        slug=slug,
        date_published=_parse_date(meta.get("date_published")),
        date_updated=_parse_date(meta.get("date_updated")),
        date=_parse_date(meta.get("date")),
        image=meta.get("image") or None,
        excerpt=excerpt,
        tags=_parse_tags(meta.get("tags", "")),
        source_path=md_path,
        content_dir=content_dir,
    )


# ---------------------------------------------------------------------------
# 1.5  Find translation files
# ---------------------------------------------------------------------------


def _find_translation_files(
    content_item: Article | Page | Recipe,
    languages: list[str],
    default_lang: str,
) -> dict[str, Path]:
    """Discover translation files in the extensions/ subdirectory."""
    ext_dir = content_item.content_dir / "extensions"
    if not ext_dir.is_dir():
        return {}

    base_name = content_item.source_path.stem
    found: dict[str, Path] = {}
    for lang in languages:
        if lang == default_lang:
            continue
        candidate = ext_dir / f"{base_name}-{lang.upper()}.md"
        if candidate.exists():
            found[lang] = candidate
    return found


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def discover(cfg: dict) -> dict:
    """Run the full Discover phase and return a manifest dict.

    The manifest has keys ``articles``, ``pages``, ``recipes`` — each a
    list of dicts ready for JSON serialisation.
    """
    content_root: Path = cfg["content_path"]

    article_paths = cfg.get("article_paths", ["articles"])
    page_paths = cfg.get("page_paths", ["pages"])
    recipe_paths = cfg.get("recipe_paths", ["recipes"])

    multilingual = cfg.get("multilingual", {})
    languages = multilingual.get("languages", [cfg.get("default_lang", "en")])
    default_lang = multilingual.get("default_lang", cfg.get("default_lang", "en"))

    # --- 1.1 Scan ---
    articles: list[Article] = []
    for sub in article_paths:
        for md in _find_md_files(content_root / sub):
            articles.append(_build_article(md, content_root))

    pages: list[Page] = []
    for sub in page_paths:
        for md in _find_md_files(content_root / sub):
            pages.append(_build_page(md, content_root))

    recipes: list[Recipe] = []
    for sub in recipe_paths:
        for md in _find_md_files(content_root / sub):
            recipes.append(_build_recipe(md, content_root))

    # --- 1.5 Find translation files ---
    for item in articles:
        item.translation_files = _find_translation_files(
            item, languages, default_lang
        )
    for item in pages:
        item.translation_files = _find_translation_files(
            item, languages, default_lang
        )
    # Recipes don't have translations per spec (excluded category)

    logger.info(
        f"Discovered {len(articles)} articles, "
        f"{len(pages)} pages, {len(recipes)} recipes"
    )

    return _to_manifest(articles, pages, recipes)


# ---------------------------------------------------------------------------
# Serialisation helpers
# ---------------------------------------------------------------------------


def _path_str(p: Path | None) -> str:
    return str(p) if p else ""


def _dt_str(dt: datetime | None) -> str:
    return dt.isoformat() if dt else ""


def _article_to_dict(a: Article) -> dict:
    return {
        "content_type": a.content_type,
        "title": a.title,
        "date": _dt_str(a.date),
        "tags": a.tags,
        "excerpt": a.excerpt,
        "image": a.image,
        "updates": a.updates,
        "status": a.status,
        "slug": a.slug,
        "category": a.category,
        "source_path": _path_str(a.source_path),
        "content_dir": _path_str(a.content_dir),
        "translation_files": {
            lang: _path_str(p) for lang, p in a.translation_files.items()
        },
    }


def _page_to_dict(p: Page) -> dict:
    return {
        "content_type": p.content_type,
        "title": p.title,
        "date": _dt_str(p.date),
        "slug": p.slug,
        "status": p.status,
        "image": p.image,
        "source_path": _path_str(p.source_path),
        "content_dir": _path_str(p.content_dir),
        "translation_files": {
            lang: _path_str(path) for lang, path in p.translation_files.items()
        },
    }


def _recipe_to_dict(r: Recipe) -> dict:
    return {
        "content_type": r.content_type,
        "title": r.title,
        "layout": r.layout,
        "slug": r.slug,
        "date_published": _dt_str(r.date_published),
        "date_updated": _dt_str(r.date_updated),
        "date": _dt_str(r.date),
        "image": r.image,
        "excerpt": r.excerpt,
        "tags": r.tags,
        "source_path": _path_str(r.source_path),
        "content_dir": _path_str(r.content_dir),
    }


def _to_manifest(
    articles: list[Article],
    pages: list[Page],
    recipes: list[Recipe],
) -> dict:
    return {
        "articles": [_article_to_dict(a) for a in articles],
        "pages": [_page_to_dict(p) for p in pages],
        "recipes": [_recipe_to_dict(r) for r in recipes],
    }


# ---------------------------------------------------------------------------
# Write artefact
# ---------------------------------------------------------------------------


def write_manifest(manifest: dict, build_path: Path) -> Path:
    """Write the discover manifest to ``.build/discover/manifest.json``."""
    out_dir = build_path / "discover"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "manifest.json"
    with open(out_file, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    logger.info(f"Wrote manifest to {out_file}")
    return out_file

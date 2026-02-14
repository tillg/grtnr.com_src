"""Phase 3: Content processing.

Sub-phases:
    3.1  Markdown -> HTML (includes WikiLinks extension)
    3.2  Fix image URLs (adjacent images)
    3.3  Generate summaries from excerpts
    3.4  External link post-processing (add target=_blank)
    3.5  Process translation files
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import markdown
from bs4 import BeautifulSoup
from typogrify.filters import typogrify

from .markdown_wikilinks import WikiLinksExtension
from .utils import get_logger

logger = get_logger("process")

# Reuse the frontmatter regex from discover
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".svg", ".pdf"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def strip_frontmatter(text: str) -> str:
    """Remove the YAML frontmatter block and return just the body."""
    m = _FRONTMATTER_RE.match(text)
    return text[m.end() :] if m else text


# ---------------------------------------------------------------------------
# 3.1  Markdown -> HTML
# ---------------------------------------------------------------------------


def _create_markdown_processor() -> markdown.Markdown:
    """Create a Python-Markdown instance with the same extensions as Pelican.

    A new instance is created per document because Python-Markdown
    maintains internal state between calls.
    """
    return markdown.Markdown(
        extensions=[
            "markdown.extensions.toc",
            "markdown.extensions.codehilite",
            "markdown.extensions.extra",
            "markdown.extensions.meta",
            WikiLinksExtension(),
        ],
        extension_configs={
            "markdown.extensions.toc": {
                "permalink": False,
                "anchorlink": False,
                "toc_depth": 3,
                "marker": "[TOC]",
            },
            "markdown.extensions.codehilite": {"css_class": "highlight"},
        },
        output_format="html5",
    )


def render_markdown(body: str) -> str:
    """Render a markdown body string to HTML."""
    md = _create_markdown_processor()
    return md.convert(body)


# ---------------------------------------------------------------------------
# 3.2  Fix image URLs (adjacent images)
# ---------------------------------------------------------------------------


def find_adjacent_files(content_dir: Path) -> list[str]:
    """Find image and attachment files adjacent to content.

    Returns filenames (not paths) of image files in the content directory
    and any files in an attachments/ subdirectory.
    """
    files: list[str] = []
    if not content_dir.is_dir():
        return files

    for f in content_dir.iterdir():
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS:
            files.append(f.name)

    attachments_dir = content_dir / "attachments"
    if attachments_dir.is_dir():
        for f in attachments_dir.iterdir():
            if f.is_file():
                files.append(f.name)

    return sorted(files)


def fix_image_urls(html: str, slug: str, image_names: list[str]) -> str:
    """Fix relative image/file URLs to absolute slug-based paths.

    Matches the Pelican copy_adjacent_images plugin behaviour: URLs are
    rewritten to ``/{slug}/{filename}``.
    """
    for img_name in image_names:
        escaped = re.escape(img_name)

        # HTML img tags with relative src
        html = re.sub(
            r'<img([^>]*) src=["\'](?!https?://|/)([^"\']*'
            + escaped
            + ")[\"']",
            r'<img\1 src="/' + slug + r'/\2"',
            html,
        )

        # Markdown images (should be converted by now, but just in case)
        html = re.sub(
            r"!\[(.*?)\]\((?!https?://|/)([^)]*" + escaped + r")\)",
            r"![\1](/" + slug + r"/\2)",
            html,
        )

        # HTML anchor tags with relative href (PDFs, attachments)
        html = re.sub(
            r'<a([^>]*) href=["\'](?!https?://|/|#)([^"\']*'
            + escaped
            + ")[\"']",
            r'<a\1 href="/' + slug + r'/\2"',
            html,
        )

    return html


# ---------------------------------------------------------------------------
# 3.3  Generate summaries from excerpts
# ---------------------------------------------------------------------------


def generate_summary(excerpt: str | None) -> str:
    """Generate a summary string from an excerpt.

    Strips surrounding quotes (Pelican compat).
    """
    if not excerpt:
        return ""
    excerpt = excerpt.strip()
    if len(excerpt) >= 2 and excerpt[0] == '"' and excerpt[-1] == '"':
        excerpt = excerpt[1:-1]
    return excerpt


# ---------------------------------------------------------------------------
# 3.4  External link post-processing
# ---------------------------------------------------------------------------


def process_external_links(html: str) -> str:
    """Add target=_blank and rel=noopener noreferrer to external links."""
    if not html:
        return html

    soup = BeautifulSoup(html, "html.parser")
    modified = False
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("http://") or href.startswith("https://"):
            link["target"] = "_blank"
            link["rel"] = "noopener noreferrer"
            modified = True

    return str(soup) if modified else html


# ---------------------------------------------------------------------------
# Per-item processing
# ---------------------------------------------------------------------------


def _process_item(item: dict) -> None:
    """Process a single content item through all sub-phases."""
    source_path = Path(item["source_path"])
    content_dir = Path(item["content_dir"])

    # Read source and strip frontmatter
    text = source_path.read_text(encoding="utf-8")
    body = strip_frontmatter(text)

    # 3.1 Markdown -> HTML
    html = render_markdown(body)

    # 3.2 Fix image URLs
    adjacent_files = find_adjacent_files(content_dir)
    if adjacent_files:
        slug = item["slug"]
        # Recipes use recipes/{slug}/ URL structure
        if item["content_type"] == "recipe":
            url_prefix = f"recipes/{slug}"
        else:
            url_prefix = slug
        html = fix_image_urls(html, url_prefix, adjacent_files)
        item["adjacent_files"] = adjacent_files

    # 3.3 Summary (articles only)
    if item["content_type"] == "article":
        item["summary"] = generate_summary(item.get("excerpt"))

    # 3.4 External links
    html = process_external_links(html)

    # Typogrify (matches Pelican's TYPOGRIFY = True)
    html = typogrify(html)

    item["content"] = html


# ---------------------------------------------------------------------------
# 3.5  Process translation files
# ---------------------------------------------------------------------------


def _parse_translation_frontmatter(text: str) -> dict[str, str]:
    """Parse frontmatter from a translation file.

    Returns a dict with lowercase keys and raw string values.
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
        if len(value) >= 2 and value[0] in ('"', "'") and value[-1] == value[0]:
            value = value[1:-1]
        meta[key] = value
    return meta


def _process_translation(
    item: dict, lang: str, translation_path: str
) -> dict | None:
    """Process a single translation file.

    Returns a dict with translated content and metadata, or None on error.
    """
    path = Path(translation_path)
    if not path.exists():
        logger.warning(f"Translation file not found: {path}")
        return None

    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        logger.warning(f"Failed to read translation file {path}: {e}")
        return None

    meta = _parse_translation_frontmatter(text)
    body = strip_frontmatter(text)

    # 3.1 Render markdown
    html = render_markdown(body)

    # 3.2 Fix image URLs (same images as original)
    adjacent_files = item.get("adjacent_files", [])
    if adjacent_files:
        slug = item["slug"]
        if item["content_type"] == "recipe":
            url_prefix = f"recipes/{slug}"
        else:
            url_prefix = slug
        html = fix_image_urls(html, url_prefix, adjacent_files)

    # 3.4 External links
    html = process_external_links(html)

    # Typogrify
    html = typogrify(html)

    # Extract translated metadata
    title = meta.get("title", item.get("title", ""))
    excerpt = meta.get("excerpt") or meta.get("summary") or None
    summary = generate_summary(excerpt) if item["content_type"] == "article" else ""

    return {
        "lang": lang,
        "title": title,
        "content": html,
        "excerpt": excerpt,
        "summary": summary,
        "source_hash": meta.get("source_hash", ""),
        "translator": meta.get("translator", ""),
        "translate_date": meta.get("translate_date", ""),
        "translation": meta.get("translation", lang),
    }


def _process_translations(item: dict) -> None:
    """Process all translation files for a content item.

    Adds an ``item["translations"]`` dict keyed by language code.
    """
    translation_files = item.get("translation_files", {})
    if not translation_files:
        item["translations"] = {}
        return

    translations = {}
    for lang, path in translation_files.items():
        result = _process_translation(item, lang, path)
        if result:
            translations[lang] = result

    item["translations"] = translations
    if translations:
        logger.info(
            f"Processed {len(translations)} translations for '{item['slug']}': "
            f"{list(translations.keys())}"
        )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def process(manifest: dict, cfg: dict) -> dict:
    """Run the full Process phase on a discover manifest.

    Enriches each content item with ``content`` (rendered HTML),
    ``summary`` (for articles), and ``translations`` (processed
    translation files).  Returns the same manifest dict, mutated.
    """
    all_items = (
        manifest["articles"] + manifest["pages"] + manifest["recipes"]
    )
    for item in all_items:
        _process_item(item)

    # 3.5 Process translations
    translatable = manifest["articles"] + manifest["pages"]
    trans_count = 0
    for item in translatable:
        _process_translations(item)
        trans_count += len(item.get("translations", {}))

    logger.info(
        f"Processed {len(manifest['articles'])} articles, "
        f"{len(manifest['pages'])} pages, "
        f"{len(manifest['recipes'])} recipes, "
        f"{trans_count} translations"
    )
    return manifest


# ---------------------------------------------------------------------------
# Write artifacts
# ---------------------------------------------------------------------------


def write_artifacts(manifest: dict, build_path: Path) -> Path:
    """Write process artifacts to ``.build/process/``.

    Writes:
      - ``manifest.json`` — full manifest with content references
      - ``html/{content_type}/{slug}.html`` — individual HTML fragments
    """
    out_dir = build_path / "process"
    out_dir.mkdir(parents=True, exist_ok=True)

    html_dir = out_dir / "html"

    # Write individual HTML files (including translations)
    for content_type in ("articles", "pages", "recipes"):
        type_dir = html_dir / content_type
        type_dir.mkdir(parents=True, exist_ok=True)
        for item in manifest[content_type]:
            html_file = type_dir / f"{item['slug']}.html"
            html_file.write_text(item.get("content", ""), encoding="utf-8")
            # Write translation HTML files
            for lang, trans in item.get("translations", {}).items():
                trans_file = type_dir / f"{item['slug']}-{lang}.html"
                trans_file.write_text(
                    trans.get("content", ""), encoding="utf-8"
                )

    # Write manifest (without inline content to keep it readable)
    manifest_slim = _slim_manifest(manifest)
    manifest_file = out_dir / "manifest.json"
    with open(manifest_file, "w") as f:
        json.dump(manifest_slim, f, indent=2, ensure_ascii=False)

    logger.info(f"Wrote process artifacts to {out_dir}")
    return manifest_file


def _slim_manifest(manifest: dict) -> dict:
    """Create a manifest copy with content replaced by file references."""
    result = {}
    for content_type in ("articles", "pages", "recipes"):
        items = []
        for item in manifest[content_type]:
            slim = {k: v for k, v in item.items() if k not in ("content",)}
            slim["content_file"] = f"html/{content_type}/{item['slug']}.html"
            # Slim down translations too
            if "translations" in slim:
                slim_trans = {}
                for lang, trans in slim["translations"].items():
                    slim_trans[lang] = {
                        k: v for k, v in trans.items() if k != "content"
                    }
                    slim_trans[lang]["content_file"] = (
                        f"html/{content_type}/{item['slug']}-{lang}.html"
                    )
                slim["translations"] = slim_trans
            items.append(slim)
        result[content_type] = items
    return result

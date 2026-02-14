"""Phase 3: Content processing.

Sub-phases:
    3.1  Markdown -> HTML (includes WikiLinks extension)
    3.2  Fix image URLs (adjacent images)
    3.3  Generate summaries from excerpts
    3.4  External link post-processing (add target=_blank)
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
# Public API
# ---------------------------------------------------------------------------


def process(manifest: dict, cfg: dict) -> dict:
    """Run the full Process phase on a discover manifest.

    Enriches each content item with ``content`` (rendered HTML) and
    ``summary`` (for articles).  Returns the same manifest dict, mutated.
    """
    all_items = (
        manifest["articles"] + manifest["pages"] + manifest["recipes"]
    )
    for item in all_items:
        _process_item(item)

    logger.info(
        f"Processed {len(manifest['articles'])} articles, "
        f"{len(manifest['pages'])} pages, "
        f"{len(manifest['recipes'])} recipes"
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

    # Write individual HTML files
    for content_type in ("articles", "pages", "recipes"):
        type_dir = html_dir / content_type
        type_dir.mkdir(parents=True, exist_ok=True)
        for item in manifest[content_type]:
            html_file = type_dir / f"{item['slug']}.html"
            html_file.write_text(item.get("content", ""), encoding="utf-8")

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
            slim = {k: v for k, v in item.items() if k != "content"}
            slim["content_file"] = f"html/{content_type}/{item['slug']}.html"
            items.append(slim)
        result[content_type] = items
    return result

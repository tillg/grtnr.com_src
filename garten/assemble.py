"""Phase 4: Site assembly.

Sub-phases:
    4.1  Generate URLs for all content
    4.4  Build tag + category groupings
    4.5  Build pagination
    4.8  Filter articles for index

Multilingual sub-phases (4.2, 4.3, 4.6, 4.7) are deferred to Increment 4.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

from .utils import get_logger, normalize_slug, slugify

logger = get_logger("assemble")


# ---------------------------------------------------------------------------
# Tag / Category helper classes (template-compatible)
# ---------------------------------------------------------------------------


class Tag:
    """A tag with display name and slug, compatible with Jinja2 templates.

    Templates use ``{{ tag }}`` for display and ``tag.slug`` for URLs.
    """

    def __init__(self, name: str, slug: str = ""):
        self.name = name
        self.slug = slug or slugify(name)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Tag({self.name!r})"

    def __hash__(self) -> int:
        return hash(self.slug)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Tag):
            return self.slug == other.slug
        return NotImplemented


class Category:
    """A category with display name, slug, and URL."""

    def __init__(self, name: str, slug: str = ""):
        self.name = name
        self.slug = slug or slugify(name)
        self.url = f"category/{self.slug}/"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Category({self.name!r})"

    def __hash__(self) -> int:
        return hash(self.slug)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Category):
            return self.slug == other.slug
        return NotImplemented


class Author:
    """An author with display name, slug, and URL."""

    def __init__(self, name: str, slug: str = ""):
        self.name = name
        self.slug = slug or slugify(name)
        self.url = f"author/{self.slug}.html"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Author({self.name!r})"


# ---------------------------------------------------------------------------
# 4.1  Generate URLs
# ---------------------------------------------------------------------------


def generate_urls(manifest: dict) -> None:
    """Set ``url`` and ``save_as`` on every content item."""
    for item in manifest["articles"]:
        slug = item["slug"]
        item["url"] = f"{slug}/"
        item["save_as"] = f"{slug}/index.html"

    for item in manifest["pages"]:
        slug = item["slug"]
        item["url"] = f"{slug}/"
        item["save_as"] = f"{slug}/index.html"

    for item in manifest["recipes"]:
        slug = item["slug"]
        item["url"] = f"recipes/{slug}/"
        item["save_as"] = f"recipes/{slug}/index.html"


# ---------------------------------------------------------------------------
# Locale dates
# ---------------------------------------------------------------------------

# Platform-portable date formatting. %-d (no zero-pad) is POSIX but
# not available on Windows. We use it since dev/CI is macOS/Linux.
_DATE_FORMAT_EN = "%B %-d, %Y"  # "February 14, 2026"


def _format_locale_date(date_str: str, lang: str = "en") -> str:
    """Format an ISO date string into a locale-appropriate display string."""
    if not date_str:
        return ""
    from datetime import datetime

    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(date_str.replace("Z", ""), fmt)
            return dt.strftime(_DATE_FORMAT_EN)
        except ValueError:
            continue
    return date_str


def set_locale_dates(manifest: dict) -> None:
    """Set ``locale_date`` on all content items."""
    for item in manifest["articles"]:
        item["locale_date"] = _format_locale_date(item.get("date", ""))

    for item in manifest["pages"]:
        item["locale_date"] = _format_locale_date(item.get("date", ""))

    for item in manifest["recipes"]:
        # Recipes use date_published or date
        date = item.get("date_published") or item.get("date") or ""
        item["locale_date"] = _format_locale_date(date)


# ---------------------------------------------------------------------------
# 4.4  Build tag + category groupings
# ---------------------------------------------------------------------------


def build_tag_map(articles: list[dict]) -> dict[Tag, list[dict]]:
    """Build a mapping of Tag objects to their articles.

    Only includes published articles. Returns tags sorted by article count
    (descending).
    """
    tag_articles: dict[str, list[dict]] = defaultdict(list)
    tag_objects: dict[str, Tag] = {}

    for article in articles:
        if article.get("status") == "hidden":
            continue
        for tag_name in article.get("tags", []):
            tag_slug = slugify(tag_name)
            if tag_name not in tag_objects:
                tag_objects[tag_name] = Tag(tag_name, tag_slug)
            tag_articles[tag_name].append(article)

    return {tag_objects[name]: arts for name, arts in tag_articles.items()}


def build_category_map(articles: list[dict]) -> dict[Category, list[dict]]:
    """Build a mapping of Category objects to their articles."""
    cat_articles: dict[str, list[dict]] = defaultdict(list)
    cat_objects: dict[str, Category] = {}

    for article in articles:
        if article.get("status") == "hidden":
            continue
        cat_name = article.get("category", "")
        if not cat_name:
            continue
        if cat_name not in cat_objects:
            cat_objects[cat_name] = Category(cat_name)
        cat_articles[cat_name].append(article)

    return {cat_objects[name]: arts for name, arts in cat_articles.items()}


# ---------------------------------------------------------------------------
# 4.5  Build pagination
# ---------------------------------------------------------------------------


def build_pagination(
    articles: list[dict], per_page: int = 10
) -> list[dict]:
    """Build pagination data for the index pages.

    Returns a list of page dicts, each with:
      - page_num: 1-based page number
      - articles: list of article dicts for this page
      - url: output URL (index.html, index2.html, ...)
      - save_as: output file path
      - has_previous: bool
      - has_next: bool
      - previous_url: str or None
      - next_url: str or None
    """
    if not articles:
        return []

    total_pages = math.ceil(len(articles) / per_page)
    pages = []

    for i in range(total_pages):
        page_num = i + 1
        start = i * per_page
        end = start + per_page
        page_articles = articles[start:end]

        url = "index.html" if page_num == 1 else f"index{page_num}.html"
        save_as = url

        prev_url = None
        if page_num > 1:
            prev_url = (
                "index.html" if page_num == 2 else f"index{page_num - 1}.html"
            )

        next_url = None
        if page_num < total_pages:
            next_url = f"index{page_num + 1}.html"

        pages.append(
            {
                "page_num": page_num,
                "articles": page_articles,
                "url": url,
                "save_as": save_as,
                "has_previous": page_num > 1,
                "has_next": page_num < total_pages,
                "previous_url": prev_url,
                "next_url": next_url,
            }
        )

    return pages


# ---------------------------------------------------------------------------
# 4.8  Filter articles for index
# ---------------------------------------------------------------------------


def filter_articles_for_index(
    articles: list[dict], categories_in_index: list[str] | None = None
) -> list[dict]:
    """Filter articles for the homepage index.

    If *categories_in_index* is empty or None, all published articles
    are included (matching Pelican's ``CATEGORIES_IN_INDEX = []``).
    """
    result = [a for a in articles if a.get("status") != "hidden"]
    if categories_in_index:
        result = [
            a for a in result if a.get("category") in categories_in_index
        ]
    return result


# ---------------------------------------------------------------------------
# Sort helpers
# ---------------------------------------------------------------------------


def sort_articles_by_date(articles: list[dict], reverse: bool = True) -> list[dict]:
    """Sort articles by date (newest first by default)."""
    return sorted(articles, key=lambda a: a.get("date", ""), reverse=reverse)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def assemble(manifest: dict, cfg: dict) -> dict:
    """Run the full Assemble phase.

    Enriches the manifest with URLs, locale dates, and builds the site
    structure (tags, categories, pagination). Returns a site context dict.
    """
    # 4.1 Generate URLs
    generate_urls(manifest)

    # Set locale dates
    set_locale_dates(manifest)

    # Sort articles by date (newest first)
    manifest["articles"] = sort_articles_by_date(manifest["articles"])

    # 4.8 Filter articles for index
    categories_in_index = cfg.get("categories_in_index", [])
    index_articles = filter_articles_for_index(
        manifest["articles"], categories_in_index
    )

    # 4.4 Build tag and category groupings
    tag_map = build_tag_map(manifest["articles"])
    category_map = build_category_map(manifest["articles"])

    # 4.5 Build pagination
    per_page = cfg.get("default_pagination", 10)
    pagination = build_pagination(index_articles, per_page)

    site = {
        "articles": manifest["articles"],
        "pages": manifest["pages"],
        "recipes": manifest["recipes"],
        "tag_map": tag_map,
        "category_map": category_map,
        "pagination": pagination,
        "index_articles": index_articles,
    }

    logger.info(
        f"Assembled site: {len(site['articles'])} articles, "
        f"{len(site['pages'])} pages, {len(site['recipes'])} recipes, "
        f"{len(tag_map)} tags, {len(category_map)} categories, "
        f"{len(pagination)} index pages"
    )

    return site


# ---------------------------------------------------------------------------
# Write artifacts
# ---------------------------------------------------------------------------


def write_artifacts(site: dict, build_path: Path) -> Path:
    """Write assemble artifacts to ``.build/assemble/``."""
    out_dir = build_path / "assemble"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Build a JSON-serializable summary
    summary = {
        "article_count": len(site["articles"]),
        "page_count": len(site["pages"]),
        "recipe_count": len(site["recipes"]),
        "tags": {
            str(tag): [a["slug"] for a in arts]
            for tag, arts in site["tag_map"].items()
        },
        "categories": {
            str(cat): [a["slug"] for a in arts]
            for cat, arts in site["category_map"].items()
        },
        "pagination_pages": len(site["pagination"]),
        "index_article_count": len(site["index_articles"]),
    }

    out_file = out_dir / "site.json"
    with open(out_file, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    logger.info(f"Wrote assemble artifacts to {out_dir}")
    return out_file

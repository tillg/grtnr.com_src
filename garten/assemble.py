"""Phase 4: Site assembly.

Sub-phases:
    4.1  Generate URLs for all content
    4.2  Generate language-prefixed URLs
    4.3  Prefix internal links with language codes
    4.4  Build tag + category groupings
    4.5  Build pagination
    4.6  Build menu with translations
    4.7  Build language switcher data
    4.8  Filter articles for index
"""

from __future__ import annotations

import copy
import json
import math
import re
from collections import defaultdict
from pathlib import Path

from .utils import get_logger, localize_date, normalize_slug, slugify

logger = get_logger("assemble")

LANG_NAMES = {
    "en": "English",
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
    "it": "Italiano",
}


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
# 4.2  Generate language-prefixed URLs
# ---------------------------------------------------------------------------


def generate_multilingual_urls(
    items: list[dict], languages: list[str], default_lang: str
) -> None:
    """Set ``multilingual_urls`` on every content item.

    Creates a dict mapping language code to the URL for that language
    version, used for hreflang tags in templates.
    """
    for item in items:
        slug = item["slug"]
        urls = {}
        for lang in languages:
            if lang == default_lang:
                urls[lang] = f"/{slug}/"
            else:
                urls[lang] = f"/{lang}/{slug}/"
        item["multilingual_urls"] = urls


# ---------------------------------------------------------------------------
# 4.3  Prefix internal links with language codes
# ---------------------------------------------------------------------------


def prefix_internal_links(
    html: str, lang: str, languages: list[str]
) -> str:
    """Prefix internal content links with language code.

    Rewrites ``href="/slug/"`` to ``href="/de/slug/"`` for translated pages,
    while leaving theme assets, static files, and already-prefixed
    links untouched.
    """
    if not html or lang == "en":
        # English content at root level doesn't need prefixing
        # (language-prefixed copies are handled separately)
        return html

    lang_prefixes = "|".join(languages)
    skip_prefixes = ("/theme/", "/static/", "/favicon", "/recipes")

    def replace_href(match):
        prefix = match.group(1)
        path = match.group(2)
        suffix = match.group(3)

        # Already has a language prefix
        if re.match(rf"^/({lang_prefixes})/", path):
            return match.group(0)

        # Static / theme assets
        if any(path.startswith(s) for s in skip_prefixes):
            return match.group(0)

        return f"{prefix}/{lang}{path}{suffix}"

    return re.sub(r'(href=["\'])(/[^"\']*?)(["\'])', replace_href, html)


# ---------------------------------------------------------------------------
# 4.7  Build language switcher data
# ---------------------------------------------------------------------------


def build_language_links(
    item: dict, languages: list[str], default_lang: str
) -> list[dict]:
    """Generate language switching links for a content item.

    Returns a list of dicts with ``code``, ``name``, ``url`` for each
    non-default language.
    """
    slug = item["slug"]
    item_url = item.get("url", f"{slug}/")
    links = []
    for lang in languages:
        if lang == default_lang:
            continue
        if item_url.startswith("/"):
            lang_url = f"/{lang}{item_url}"
        else:
            lang_url = f"/{lang}/{item_url}"
        links.append({
            "code": lang,
            "name": LANG_NAMES.get(lang, lang.upper()),
            "url": lang_url,
        })
    return links


# ---------------------------------------------------------------------------
# Locale dates
# ---------------------------------------------------------------------------


def set_locale_dates(manifest: dict, lang: str = "en") -> None:
    """Set ``locale_date`` on all content items."""
    for item in manifest["articles"]:
        item["locale_date"] = localize_date(item.get("date", ""), lang)

    for item in manifest["pages"]:
        item["locale_date"] = localize_date(item.get("date", ""), lang)

    for item in manifest["recipes"]:
        date = item.get("date_published") or item.get("date") or ""
        item["locale_date"] = localize_date(date, lang)


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
    articles: list[dict], per_page: int = 10, url_prefix: str = ""
) -> list[dict]:
    """Build pagination data for the index pages.

    *url_prefix* is prepended to page URLs (e.g. ``"de/"`` for German).
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

        # Page 1: index.html  (URL: / or /de/)
        # Page N: page/N/index.html  (URL: /page/N/ or /de/page/N/)
        if page_num == 1:
            url = f"{url_prefix}index.html"
            save_as = url
        else:
            url = f"{url_prefix}page/{page_num}/index.html"
            save_as = url

        prev_url = None
        if page_num > 1:
            prev_url = (
                f"{url_prefix}index.html"
                if page_num == 2
                else f"{url_prefix}page/{page_num - 1}/index.html"
            )

        next_url = None
        if page_num < total_pages:
            next_url = f"{url_prefix}page/{page_num + 1}/index.html"

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
# Build per-language article/page lists
# ---------------------------------------------------------------------------


def _build_lang_article(
    original: dict, lang: str, languages: list[str]
) -> dict:
    """Build a language-specific article dict from original + translation.

    If a translation exists for *lang*, uses translated content/title/summary.
    Otherwise uses the original content as fallback.
    """
    trans = original.get("translations", {}).get(lang, {})
    slug = original["slug"]

    art = copy.copy(original)
    art["lang"] = lang
    art["url"] = f"{lang}/{slug}/"
    art["save_as"] = f"{lang}/{slug}/index.html"
    art["locale_date"] = localize_date(original.get("date", ""), lang)

    if trans:
        art["content"] = prefix_internal_links(
            trans.get("content", original.get("content", "")),
            lang, languages,
        )
        art["title"] = trans.get("title") or original.get("title", "")
        art["summary"] = trans.get("summary") or original.get("summary", "")
        art["excerpt"] = trans.get("excerpt") or original.get("excerpt")
        art["translation"] = trans.get("translation", lang)
        art["translator"] = trans.get("translator", "")
        art["original_url"] = f"/{original['slug']}/"
    else:
        art["content"] = prefix_internal_links(
            original.get("content", ""), lang, languages
        )
        art["translation"] = False
        art["translator"] = ""
        art["original_url"] = ""

    # Don't carry translations dict into per-language copies
    art.pop("translations", None)
    art.pop("translation_files", None)
    return art


def _build_lang_page(
    original: dict, lang: str, languages: list[str]
) -> dict:
    """Build a language-specific page dict from original + translation."""
    trans = original.get("translations", {}).get(lang, {})
    slug = original["slug"]

    pg = copy.copy(original)
    pg["lang"] = lang
    pg["url"] = f"{lang}/{slug}/"
    pg["save_as"] = f"{lang}/{slug}/index.html"
    pg["locale_date"] = localize_date(original.get("date", ""), lang)

    if trans:
        pg["content"] = prefix_internal_links(
            trans.get("content", original.get("content", "")),
            lang, languages,
        )
        pg["title"] = trans.get("title") or original.get("title", "")
    else:
        pg["content"] = prefix_internal_links(
            original.get("content", ""), lang, languages
        )

    pg.pop("translations", None)
    pg.pop("translation_files", None)
    return pg


def build_per_language_content(
    manifest: dict, languages: list[str], default_lang: str, cfg: dict
) -> dict:
    """Build per-language article and page lists.

    For each non-default language, creates language-specific copies of
    articles and pages with translated content (or fallback to original).
    For the default language, creates copies at /{lang}/{slug}/ path.

    Returns a dict keyed by language code, each containing:
    ``articles``, ``pages``, ``tag_map``, ``pagination``, ``index_articles``.
    """
    categories_in_index = cfg.get("categories_in_index", [])
    per_page = cfg.get("default_pagination", 10)

    per_lang = {}
    for lang in languages:
        # Build language-specific articles
        lang_articles = []
        for art in manifest["articles"]:
            lang_art = _build_lang_article(art, lang, languages)
            lang_articles.append(lang_art)

        lang_articles = sort_articles_by_date(lang_articles)

        # Build language-specific pages
        lang_pages = []
        for pg in manifest["pages"]:
            lang_pg = _build_lang_page(pg, lang, languages)
            lang_pages.append(lang_pg)

        # Build tag map and pagination for this language
        lang_index = filter_articles_for_index(
            lang_articles, categories_in_index
        )
        lang_tag_map = build_tag_map(lang_articles)
        lang_pagination = build_pagination(
            lang_index, per_page, url_prefix=f"{lang}/"
        )

        per_lang[lang] = {
            "articles": lang_articles,
            "pages": lang_pages,
            "tag_map": lang_tag_map,
            "pagination": lang_pagination,
            "index_articles": lang_index,
        }

        logger.info(
            f"Language '{lang}': {len(lang_articles)} articles, "
            f"{len(lang_pages)} pages, {len(lang_pagination)} index pages"
        )

    return per_lang


# ---------------------------------------------------------------------------
# 4.6  Build menu with translations
# ---------------------------------------------------------------------------


def load_menu_translations(base_path: Path) -> dict:
    """Load menu translations from ``menu_translations.json``."""
    path = base_path / "menu_translations.json"
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


# Paths that exist only at root level, never under language prefixes.
_NO_LANG_PREFIX_PATHS = {"/recipes"}


def build_translated_links(
    links: list, lang: str, menu_translations: dict
) -> list:
    """Build language-specific menu links.

    Translates menu titles and adds language prefix to hrefs for
    non-English languages, except for paths that only exist at root
    (e.g. ``/recipes``).
    """
    lang_trans = menu_translations.get(lang, {})
    result = []
    for link in links:
        title = link[0] if isinstance(link, (list, tuple)) else link
        href = link[1] if isinstance(link, (list, tuple)) else "#"

        translated_title = lang_trans.get(title, title)
        if lang != "en" and href not in _NO_LANG_PREFIX_PATHS:
            translated_href = f"/{lang}{href}"
        else:
            translated_href = href

        result.append([translated_title, translated_href])
    return result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def assemble(manifest: dict, cfg: dict) -> dict:
    """Run the full Assemble phase.

    Enriches the manifest with URLs, locale dates, and builds the site
    structure (tags, categories, pagination). Returns a site context dict.
    """
    multilingual = cfg.get("multilingual", {})
    ml_enabled = multilingual.get("enabled", False)
    languages = multilingual.get("languages", [cfg.get("default_lang", "en")])
    default_lang = multilingual.get(
        "default_lang", cfg.get("default_lang", "en")
    )

    # 4.1 Generate URLs (root-level English)
    generate_urls(manifest)

    # Set locale dates (English)
    set_locale_dates(manifest, default_lang)

    # Sort articles by date (newest first)
    manifest["articles"] = sort_articles_by_date(manifest["articles"])

    # 4.2 Generate multilingual URLs (for hreflang tags)
    if ml_enabled:
        generate_multilingual_urls(
            manifest["articles"] + manifest["pages"],
            languages, default_lang,
        )

    # 4.7 Build language links (sidebar language switcher)
    if ml_enabled:
        for item in manifest["articles"]:
            item["language_links"] = build_language_links(
                item, languages, default_lang
            )
        for item in manifest["pages"]:
            item["language_links"] = build_language_links(
                item, languages, default_lang
            )

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
        "languages": languages,
        "default_lang": default_lang,
        "multilingual_enabled": ml_enabled,
    }

    # Build per-language content
    if ml_enabled:
        # 4.6 Load menu translations
        menu_translations = load_menu_translations(cfg.get("base_path", Path(".")))
        site["menu_translations"] = menu_translations

        site["per_lang"] = build_per_language_content(
            manifest, languages, default_lang, cfg
        )

    logger.info(
        f"Assembled site: {len(site['articles'])} articles, "
        f"{len(site['pages'])} pages, {len(site['recipes'])} recipes, "
        f"{len(tag_map)} tags, {len(category_map)} categories, "
        f"{len(pagination)} index pages"
    )
    if ml_enabled:
        logger.info(
            f"Multilingual: {len(languages)} languages ({', '.join(languages)})"
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
        "multilingual_enabled": site.get("multilingual_enabled", False),
        "languages": site.get("languages", []),
    }

    if "per_lang" in site:
        summary["per_lang"] = {
            lang: {
                "article_count": len(data["articles"]),
                "page_count": len(data["pages"]),
                "pagination_pages": len(data["pagination"]),
            }
            for lang, data in site["per_lang"].items()
        }

    out_file = out_dir / "site.json"
    with open(out_file, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    logger.info(f"Wrote assemble artifacts to {out_dir}")
    return out_file

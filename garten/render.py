"""Phase 5: Template rendering and file output.

Sub-phases:
    5.1  Render articles, pages, recipes
    5.2  Render index pages (paginated)
    5.3  Render tag + category pages
    5.5  Render sitemap, robots.txt, humans.txt
    5.6  Render root redirect page
    5.7  Copy static assets + images to language dirs
"""

from __future__ import annotations

import shutil
from pathlib import Path
from types import SimpleNamespace

from jinja2 import Environment, FileSystemLoader

from .assemble import Author, Category, Tag, build_translated_links
from .utils import get_logger

logger = get_logger("render")


# ---------------------------------------------------------------------------
# Template-compatible wrapper objects
# ---------------------------------------------------------------------------


class ArticleWrapper:
    """Wraps an article dict to provide attribute access for templates.

    Templates use ``article.title``, ``article.url``, ``article.tags``, etc.
    Tags are converted to Tag objects with ``.slug`` for URL generation.
    """

    def __init__(self, data: dict, tag_objects: dict[str, Tag] | None = None):
        self._data = data
        self.title = data.get("title", "")
        self.slug = data.get("slug", "")
        self.url = data.get("url", "")
        self.save_as = data.get("save_as", "")
        self.content = data.get("content", "")
        self.summary = data.get("summary", "")
        self.locale_date = data.get("locale_date", "")
        self.date = data.get("date", "")
        self.image = data.get("image")
        self.excerpt = data.get("excerpt")
        self.category = data.get("category", "")
        self.status = data.get("status", "published")

        # Convert tag strings to Tag objects
        tag_objects = tag_objects or {}
        self.tags = []
        for tag_name in data.get("tags", []):
            if tag_name in tag_objects:
                self.tags.append(tag_objects[tag_name])
            else:
                from .utils import slugify

                self.tags.append(Tag(tag_name, slugify(tag_name)))

        # Multilingual
        self.multilingual_urls = data.get("multilingual_urls", {})
        self.language_links = data.get("language_links", [])
        self.translations = []
        self.translation = data.get("translation", False)
        self.translator = data.get("translator", "")
        self.original_url = data.get("original_url", "")

        # Meta tags
        self.keywords = []
        self.description = data.get("excerpt", "") or data.get("summary", "")

    def __repr__(self) -> str:
        return f"ArticleWrapper({self.slug!r})"


class PageWrapper:
    """Wraps a page dict for template access."""

    def __init__(self, data: dict):
        self._data = data
        self.title = data.get("title", "")
        self.slug = data.get("slug", "")
        self.url = data.get("url", "")
        self.save_as = data.get("save_as", "")
        self.content = data.get("content", "")
        self.locale_date = data.get("locale_date", "")
        self.image = data.get("image")
        self.status = data.get("status", "published")

        # Multilingual
        self.multilingual_urls = data.get("multilingual_urls", {})
        self.language_links = data.get("language_links", [])
        self.translations = []
        self.modified = False
        self.locale_modified = ""

    def __repr__(self) -> str:
        return f"PageWrapper({self.slug!r})"


class RecipeWrapper:
    """Wraps a recipe dict for template access.

    Provides both direct attributes (for recipe.html) and a .metadata
    namespace (for recipe_preview.html).
    """

    def __init__(self, data: dict, tag_objects: dict[str, Tag] | None = None):
        self._data = data
        self.title = data.get("title", "")
        self.slug = data.get("slug", "")
        self.url = data.get("url", "")
        self.save_as = data.get("save_as", "")
        self.content = data.get("content", "")
        self.locale_date = data.get("locale_date", "")
        self.image = data.get("image")
        self.excerpt = data.get("excerpt")
        self.category = "recipes"

        # Recipe-specific fields (not in frontmatter per spec,
        # but templates check for them via {% if %})
        self.description = data.get("excerpt", "")
        self.prep_time = None
        self.cook_time = None
        self.servings = None
        self.ingredients = []
        self.notes = None

        # Convert tag strings to Tag objects
        tag_objects = tag_objects or {}
        self.tags = []
        for tag_name in data.get("tags", []):
            if tag_name in tag_objects:
                self.tags.append(tag_objects[tag_name])
            else:
                from .utils import slugify

                self.tags.append(Tag(tag_name, slugify(tag_name)))

        # Multilingual
        self.multilingual_urls = data.get("multilingual_urls", {})

        # Metadata namespace for recipe_preview.html
        self.metadata = SimpleNamespace(
            prep_time=self.prep_time,
            cook_time=self.cook_time,
            servings=self.servings,
            tags=self.tags,
            image=self.image,
            summary=self.excerpt or "",
            description=self.description,
        )

    def __repr__(self) -> str:
        return f"RecipeWrapper({self.slug!r})"


# ---------------------------------------------------------------------------
# Pagination namespace (template-compatible)
# ---------------------------------------------------------------------------


def _make_pagination_context(page_data: dict) -> dict:
    """Build pagination template variables from a page data dict.

    Returns dict with ``articles_page``, ``articles_previous_page``,
    ``articles_next_page`` used by the index template.
    """
    has_prev = page_data["has_previous"]
    has_next = page_data["has_next"]

    articles_page = SimpleNamespace(
        object_list=page_data["articles"],
        has_previous=lambda: has_prev,
        has_next=lambda: has_next,
    )

    articles_previous_page = None
    if has_prev:
        articles_previous_page = SimpleNamespace(url=page_data["previous_url"])

    articles_next_page = None
    if has_next:
        articles_next_page = SimpleNamespace(url=page_data["next_url"])

    return {
        "articles_page": articles_page,
        "articles_previous_page": articles_previous_page,
        "articles_next_page": articles_next_page,
    }


# ---------------------------------------------------------------------------
# Jinja2 environment setup
# ---------------------------------------------------------------------------


def create_jinja_env(theme_path: Path) -> Environment:
    """Create a Jinja2 environment from the theme's template directory."""
    template_dir = theme_path / "templates"
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return env


# ---------------------------------------------------------------------------
# Global template context
# ---------------------------------------------------------------------------


def build_global_context(cfg: dict) -> dict:
    """Build the global template context shared by all templates.

    Provides variables like SITENAME, SITEURL, LINKS used by templates.
    """
    absolute_siteurl = cfg.get("siteurl", "").rstrip("/")
    siteurl = absolute_siteurl
    # For local dev, SITEURL should be empty (relative URLs)
    if cfg.get("relative_urls", True):
        siteurl = ""

    return {
        "SITENAME": cfg.get("sitename", ""),
        "SITEURL": siteurl,
        "ABSOLUTE_SITEURL": absolute_siteurl,
        "AUTHOR": cfg.get("author", ""),
        "DESCRIPTION": cfg.get("description", ""),
        "SITEDESCRIPTION": "",
        "DEFAULT_LANG": cfg.get("default_lang", "en"),
        "LANG": cfg.get("default_lang", "en"),
        "current_language": cfg.get("default_lang", "en"),
        "BUILD_TIME": cfg.get("build_time", ""),
        "GOOGLE_ANALYTICS": cfg.get("google_analytics", ""),
        "GA_ACCOUNT": "",
        "MULTILINGUAL_ENABLED": cfg.get("multilingual", {}).get(
            "enabled", False
        ),
        "DEFAULT_PAGINATION": cfg.get("default_pagination", 10),
        "LINKS": cfg.get("links", []),
        "RELATIVE_URLS": cfg.get("relative_urls", True),
        # Feeds (None for dev, set in production)
        "FEED_ALL_ATOM": cfg.get("feed_all_atom"),
        "FEED_ALL_RSS": cfg.get("feed_all_rss"),
        "FEED_ATOM": cfg.get("feed_atom"),
        "FEED_RSS": cfg.get("feed_rss"),
        "FEED_DOMAIN": siteurl,
        "CATEGORY_FEED_ATOM": cfg.get("category_feed_atom"),
        "CATEGORY_FEED_RSS": cfg.get("category_feed_rss"),
        "TAG_FEED_ATOM": cfg.get("tag_feed_atom"),
        "TAG_FEED_RSS": cfg.get("tag_feed_rss"),
    }


# ---------------------------------------------------------------------------
# Build wrapper objects
# ---------------------------------------------------------------------------


def _build_tag_object_map(tag_map: dict[Tag, list]) -> dict[str, Tag]:
    """Build a name -> Tag lookup from the tag map."""
    return {str(tag): tag for tag in tag_map}


def wrap_articles(
    articles: list[dict], tag_objects: dict[str, Tag]
) -> list[ArticleWrapper]:
    """Convert article dicts to template-compatible wrapper objects."""
    return [ArticleWrapper(a, tag_objects) for a in articles]


def wrap_pages(pages: list[dict]) -> list[PageWrapper]:
    """Convert page dicts to template-compatible wrapper objects."""
    return [PageWrapper(p) for p in pages]


def wrap_recipes(
    recipes: list[dict], tag_objects: dict[str, Tag]
) -> list[RecipeWrapper]:
    """Convert recipe dicts to template-compatible wrapper objects."""
    return [RecipeWrapper(r, tag_objects) for r in recipes]


# ---------------------------------------------------------------------------
# 5.1  Render individual content pages
# ---------------------------------------------------------------------------


def render_articles(
    env: Environment,
    articles: list[ArticleWrapper],
    global_ctx: dict,
    output_path: Path,
) -> int:
    """Render each article to its own page."""
    template = env.get_template("article.html")
    count = 0
    for article in articles:
        if article.status == "hidden":
            continue
        ctx = {**global_ctx, "article": article}
        html = template.render(ctx)
        out_file = output_path / article.save_as
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(html, encoding="utf-8")
        count += 1
    return count


def render_pages(
    env: Environment,
    pages: list[PageWrapper],
    global_ctx: dict,
    output_path: Path,
) -> int:
    """Render each page to its own file."""
    template = env.get_template("page.html")
    count = 0
    for page in pages:
        if page.status == "hidden":
            continue
        ctx = {**global_ctx, "page": page}
        html = template.render(ctx)
        out_file = output_path / page.save_as
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(html, encoding="utf-8")
        count += 1
    return count


def render_recipes(
    env: Environment,
    recipes: list[RecipeWrapper],
    global_ctx: dict,
    output_path: Path,
    url_prefix: str = "",
) -> int:
    """Render each recipe to its own page."""
    template = env.get_template("recipe.html")
    count = 0
    for recipe in recipes:
        ctx = {**global_ctx, "recipe": recipe}
        html = template.render(ctx)
        out_file = output_path / f"{url_prefix}{recipe.save_as}"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(html, encoding="utf-8")
        count += 1
    return count


# ---------------------------------------------------------------------------
# 5.2  Render index pages (paginated)
# ---------------------------------------------------------------------------


def render_index_pages(
    env: Environment,
    pagination: list[dict],
    tag_objects: dict[str, Tag],
    global_ctx: dict,
    output_path: Path,
) -> int:
    """Render paginated index pages."""
    template = env.get_template("index.html")
    count = 0
    for page_data in pagination:
        # Wrap articles for this page
        page_articles = wrap_articles(page_data["articles"], tag_objects)

        # Build pagination context with wrapped articles
        pag_data_wrapped = {**page_data, "articles": page_articles}
        pag_ctx = _make_pagination_context(pag_data_wrapped)

        ctx = {**global_ctx, **pag_ctx}
        html = template.render(ctx)
        out_file = output_path / page_data["save_as"]
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(html, encoding="utf-8")
        count += 1
    return count


# ---------------------------------------------------------------------------
# 5.3  Render tag + category pages
# ---------------------------------------------------------------------------


def render_tag_pages(
    env: Environment,
    tag_map: dict[Tag, list[dict]],
    tag_objects: dict[str, Tag],
    global_ctx: dict,
    output_path: Path,
    url_prefix: str = "",
) -> int:
    """Render individual tag pages (one per tag)."""
    template = env.get_template("tag.html")
    count = 0
    for tag, articles in tag_map.items():
        wrapped = wrap_articles(articles, tag_objects)
        ctx = {**global_ctx, "tag": tag, "articles": wrapped}
        html = template.render(ctx)
        out_file = output_path / f"{url_prefix}tag/{tag.slug}/index.html"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(html, encoding="utf-8")
        count += 1
    return count


def render_tags_page(
    env: Environment,
    tag_map: dict[Tag, list[dict]],
    global_ctx: dict,
    output_path: Path,
    url_prefix: str = "",
) -> None:
    """Render the tags overview page (all tags with counts)."""
    template = env.get_template("tags.html")
    tags_list = [(tag, articles) for tag, articles in tag_map.items()]
    ctx = {**global_ctx, "tags": tags_list}
    html = template.render(ctx)
    out_file = output_path / f"{url_prefix}tags/index.html"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")


def render_category_pages(
    env: Environment,
    category_map: dict[Category, list[dict]],
    tag_objects: dict[str, Tag],
    global_ctx: dict,
    output_path: Path,
) -> int:
    """Render individual category pages."""
    template = env.get_template("index.html")
    count = 0
    for cat, articles in category_map.items():
        wrapped = wrap_articles(articles, tag_objects)
        # Category page uses index template with category context
        pag_data = {
            "articles": wrapped,
            "has_previous": False,
            "has_next": False,
            "previous_url": None,
            "next_url": None,
        }
        pag_ctx = _make_pagination_context(pag_data)
        ctx = {**global_ctx, **pag_ctx, "category": cat}
        html = template.render(ctx)
        out_file = output_path / f"category/{cat.slug}/index.html"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(html, encoding="utf-8")
        count += 1
    return count


def render_categories_page(
    env: Environment,
    category_map: dict[Category, list[dict]],
    global_ctx: dict,
    output_path: Path,
) -> None:
    """Render the categories overview page."""
    template = env.get_template("categories.html")
    categories_list = [
        (cat, articles) for cat, articles in category_map.items()
    ]
    ctx = {**global_ctx, "categories": categories_list}
    html = template.render(ctx)
    out_file = output_path / "categories.html"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# 5.5  Render direct templates (sitemap, robots, humans, archives, etc.)
# ---------------------------------------------------------------------------


def render_archives(
    env: Environment,
    articles: list[ArticleWrapper],
    global_ctx: dict,
    output_path: Path,
) -> None:
    """Render the archives page (all articles by date)."""
    template = env.get_template("archives.html")
    ctx = {**global_ctx, "dates": articles}
    html = template.render(ctx)
    out_file = output_path / "archives.html"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")


def render_authors_page(
    env: Environment,
    author: str,
    articles: list[ArticleWrapper],
    global_ctx: dict,
    output_path: Path,
) -> None:
    """Render the authors overview page and individual author page."""
    author_obj = Author(author)

    # Authors overview page
    template = env.get_template("authors.html")
    ctx = {**global_ctx, "authors": [(author_obj, articles)]}
    html = template.render(ctx)
    out_file = output_path / "authors.html"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")

    # Individual author page (uses index template)
    idx_template = env.get_template("index.html")
    pag_data = {
        "articles": articles,
        "has_previous": False,
        "has_next": False,
        "previous_url": None,
        "next_url": None,
    }
    pag_ctx = _make_pagination_context(pag_data)
    ctx = {**global_ctx, **pag_ctx, "author": author_obj}
    html = idx_template.render(ctx)
    out_file = output_path / author_obj.url
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")


def render_sitemap(
    env: Environment,
    articles: list[ArticleWrapper],
    pages: list[PageWrapper],
    global_ctx: dict,
    output_path: Path,
) -> None:
    """Render the XML sitemap."""
    template = env.get_template("sitemap.html")
    ctx = {**global_ctx, "articles": articles, "pages": pages}
    xml = template.render(ctx)
    out_file = output_path / "sitemap.xml"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(xml, encoding="utf-8")


def render_robots(
    env: Environment, global_ctx: dict, output_path: Path
) -> None:
    """Render robots.txt."""
    template = env.get_template("robots.html")
    txt = template.render(global_ctx)
    out_file = output_path / "robots.txt"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(txt, encoding="utf-8")


def render_humans(
    env: Environment, global_ctx: dict, output_path: Path
) -> None:
    """Render humans.txt."""
    template = env.get_template("humans.html")
    txt = template.render(global_ctx)
    out_file = output_path / "humans.txt"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(txt, encoding="utf-8")


def render_recipes_index(
    env: Environment,
    recipes: list[RecipeWrapper],
    global_ctx: dict,
    output_path: Path,
) -> None:
    """Render the recipes index page."""
    template = env.get_template("recipes_index.html")
    ctx = {**global_ctx, "recipes": recipes}
    html = template.render(ctx)
    out_file = output_path / "recipes/index.html"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# 5.5b Render search page
# ---------------------------------------------------------------------------


def render_search_page(
    env: Environment,
    global_ctx: dict,
    output_path: Path,
    url_prefix: str = "",
) -> None:
    """Render the dedicated search page."""
    template = env.get_template("search.html")
    html = template.render(global_ctx)
    out_file = output_path / f"{url_prefix}search/index.html"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# 5.6  Render root redirect page
# ---------------------------------------------------------------------------


def render_root_redirect(
    env: Environment,
    global_ctx: dict,
    output_path: Path,
) -> None:
    """Render the root index.html with auto-redirect to detected language."""
    template = env.get_template("auto_redirect.html")
    html = template.render(global_ctx)
    out_file = output_path / "index.html"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# 5.7  Copy static assets + images
# ---------------------------------------------------------------------------


def copy_theme_static(theme_path: Path, output_path: Path) -> int:
    """Copy theme static files to output/theme/."""
    src = theme_path / "static"
    dst = output_path / "theme"
    if not src.is_dir():
        return 0

    count = 0
    for item in src.rglob("*"):
        if item.is_file():
            rel = item.relative_to(src)
            out_file = dst / rel
            out_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, out_file)
            count += 1
    return count


def copy_content_static(content_path: Path, output_path: Path) -> int:
    """Copy content/static files to output root with EXTRA_PATH_METADATA mappings."""
    static_dir = content_path / "static"
    if not static_dir.is_dir():
        return 0

    # Mapping of source files to their output locations
    extra_path_metadata = {
        "favicon.ico": "favicon.ico",
        "apple-touch-icon.png": "apple-touch-icon.png",
    }

    count = 0
    for item in static_dir.rglob("*"):
        if item.is_file():
            rel = item.relative_to(static_dir)
            rel_str = str(rel)

            # Check for special mappings
            if rel_str in extra_path_metadata:
                out_file = output_path / extra_path_metadata[rel_str]
            else:
                # Default: copy to output/static/
                out_file = output_path / "static" / rel

            out_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, out_file)
            count += 1
    return count


def copy_adjacent_images(
    manifest_items: list[dict], output_path: Path
) -> int:
    """Copy adjacent images from content directories to output.

    Each content item's adjacent files are copied to the output directory
    matching its save_as path.
    """
    count = 0
    for item in manifest_items:
        adjacent = item.get("adjacent_files", [])
        if not adjacent:
            continue

        content_dir = Path(item["content_dir"])
        save_as = item.get("save_as", "")
        if not save_as:
            continue

        # Output directory is the parent of save_as
        out_dir = output_path / Path(save_as).parent

        for filename in adjacent:
            src = content_dir / filename
            if not src.exists():
                # Check attachments subdirectory
                src = content_dir / "attachments" / filename
            if src.exists():
                out_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, out_dir / filename)
                count += 1

    return count


def copy_images_for_language(
    original_items: list[dict], lang_items: list[dict], output_path: Path
) -> int:
    """Copy images from original content dirs to language-specific output dirs.

    For each language-specific item, copies the images from the original
    content directory to the language output directory (e.g. output/de/slug/).
    """
    count = 0
    # Build a slug -> original item lookup
    orig_by_slug = {item["slug"]: item for item in original_items}

    for lang_item in lang_items:
        slug = lang_item["slug"]
        orig = orig_by_slug.get(slug)
        if not orig:
            continue

        adjacent = orig.get("adjacent_files", [])
        if not adjacent:
            continue

        content_dir = Path(orig["content_dir"])
        save_as = lang_item.get("save_as", "")
        if not save_as:
            continue

        out_dir = output_path / Path(save_as).parent

        for filename in adjacent:
            src = content_dir / filename
            if not src.exists():
                src = content_dir / "attachments" / filename
            if src.exists():
                out_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, out_dir / filename)
                count += 1

    return count


# ---------------------------------------------------------------------------
# Multilingual rendering
# ---------------------------------------------------------------------------


def _render_language(
    env: Environment,
    lang: str,
    lang_data: dict,
    tag_objects: dict[str, Tag],
    lang_ctx: dict,
    output_path: Path,
    recipes: list | None = None,
) -> dict:
    """Render all content for a single language.

    Returns a dict of counts.
    """
    articles = wrap_articles(lang_data["articles"], tag_objects)
    pages = wrap_pages(lang_data["pages"])

    # 5.1 Per-language articles
    art_count = render_articles(env, articles, lang_ctx, output_path)

    # 5.1 Per-language pages
    page_count = render_pages(env, pages, lang_ctx, output_path)

    # 5.1 Per-language recipes (shared across languages)
    recipe_count = 0
    if recipes is not None:
        recipe_count = render_recipes(
            env, recipes, lang_ctx, output_path, url_prefix=f"{lang}/"
        )

    # 5.2 Per-language paginated index
    idx_count = render_index_pages(
        env, lang_data["pagination"], tag_objects, lang_ctx, output_path
    )

    # 5.3 Per-language tag pages
    lang_tag_map = lang_data.get("tag_map", {})
    lang_tag_objects = _build_tag_object_map(lang_tag_map)
    tag_count = render_tag_pages(
        env, lang_tag_map, lang_tag_objects, lang_ctx, output_path,
        url_prefix=f"{lang}/",
    )
    render_tags_page(
        env, lang_tag_map, lang_ctx, output_path,
        url_prefix=f"{lang}/",
    )

    # Search page for this language
    render_search_page(env, lang_ctx, output_path, url_prefix=f"{lang}/")

    return {
        "articles": art_count,
        "pages": page_count,
        "recipes": recipe_count,
        "index_pages": idx_count,
        "tag_pages": tag_count,
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def render(site: dict, cfg: dict) -> None:
    """Run the full Render phase.

    Takes the assembled site context and writes all output files.
    """
    output_path: Path = cfg["output_path"]
    theme_path: Path = cfg["theme_path"]
    content_path: Path = cfg["content_path"]

    ml_enabled = site.get("multilingual_enabled", False)
    languages = site.get("languages", [cfg.get("default_lang", "en")])
    default_lang = site.get("default_lang", cfg.get("default_lang", "en"))
    menu_translations = site.get("menu_translations", {})

    # Clean output directory
    if output_path.exists():
        shutil.rmtree(output_path, ignore_errors=True)
    output_path.mkdir(parents=True, exist_ok=True)

    # Create Jinja2 environment
    env = create_jinja_env(theme_path)

    # Build global context
    global_ctx = build_global_context(cfg)

    # Build tag object lookup
    tag_objects = _build_tag_object_map(site["tag_map"])

    # Wrap content items
    articles = wrap_articles(site["articles"], tag_objects)
    pages = wrap_pages(site["pages"])
    recipes = wrap_recipes(site["recipes"], tag_objects)

    # Filter to published articles only
    published_articles = [a for a in articles if a.status != "hidden"]
    published_pages = [p for p in pages if p.status != "hidden"]

    # 5.1 Render individual content (root-level English)
    art_count = render_articles(env, articles, global_ctx, output_path)
    page_count = render_pages(env, pages, global_ctx, output_path)
    recipe_count = render_recipes(env, recipes, global_ctx, output_path)
    logger.info(
        f"Rendered {art_count} articles, {page_count} pages, "
        f"{recipe_count} recipes"
    )

    if ml_enabled:
        # 5.6 Root redirect page replaces the root index
        render_root_redirect(env, global_ctx, output_path)
        logger.info("Rendered root redirect page")
    else:
        # 5.2 Render paginated index pages (root-level, English only)
        idx_count = render_index_pages(
            env, site["pagination"], tag_objects, global_ctx, output_path
        )
        logger.info(f"Rendered {idx_count} index pages")

    # 5.3 Render tag + category pages (root-level)
    tag_count = render_tag_pages(
        env, site["tag_map"], tag_objects, global_ctx, output_path
    )
    render_tags_page(env, site["tag_map"], global_ctx, output_path)
    cat_count = render_category_pages(
        env, site["category_map"], tag_objects, global_ctx, output_path
    )
    render_categories_page(
        env, site["category_map"], global_ctx, output_path
    )
    logger.info(f"Rendered {tag_count} tag pages, {cat_count} category pages")

    # 5.5 Render direct templates
    render_archives(env, published_articles, global_ctx, output_path)
    render_authors_page(
        env,
        cfg.get("author", ""),
        published_articles,
        global_ctx,
        output_path,
    )
    render_sitemap(
        env, published_articles, published_pages, global_ctx, output_path
    )
    render_robots(env, global_ctx, output_path)
    render_humans(env, global_ctx, output_path)
    render_recipes_index(env, recipes, global_ctx, output_path)
    render_search_page(env, global_ctx, output_path)
    logger.info("Rendered direct templates (archives, sitemap, robots, etc.)")

    # 5.7 Copy static assets
    theme_count = copy_theme_static(theme_path, output_path)
    static_count = copy_content_static(content_path, output_path)
    logger.info(
        f"Copied {theme_count} theme files, {static_count} content static files"
    )

    # Copy adjacent images for all root-level content types
    all_items = site["articles"] + site["pages"] + site["recipes"]
    img_count = copy_adjacent_images(all_items, output_path)
    logger.info(f"Copied {img_count} adjacent images/files")

    # --- Multilingual rendering ---
    if ml_enabled and "per_lang" in site:
        links = cfg.get("links", [])

        for lang, lang_data in site["per_lang"].items():
            # Build language-specific template context
            lang_tag_objects = _build_tag_object_map(
                lang_data.get("tag_map", {})
            )

            # Translate menu links
            translated_links = build_translated_links(
                links, lang, menu_translations, default_lang
            )

            lang_ctx = {
                **global_ctx,
                "LANG": lang,
                "current_language": lang,
                "LINKS": translated_links,
                "PAGEFIND_INDEX": True,
            }

            counts = _render_language(
                env, lang, lang_data, lang_tag_objects, lang_ctx, output_path,
                recipes=recipes,
            )

            # Copy images for this language
            lang_img_count = copy_images_for_language(
                site["articles"], lang_data["articles"], output_path
            )
            lang_img_count += copy_images_for_language(
                site["pages"], lang_data["pages"], output_path
            )

            logger.info(
                f"Language '{lang}': {counts['articles']} articles, "
                f"{counts['pages']} pages, {counts['index_pages']} index, "
                f"{counts['tag_pages']} tag pages, "
                f"{lang_img_count} images copied"
            )

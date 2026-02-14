"""Tests for garten Phase 5: Render."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from garten.assemble import Tag
from garten.config import load_config
from garten.render import (
    ArticleWrapper,
    PageWrapper,
    RecipeWrapper,
    build_global_context,
    copy_adjacent_images,
    copy_content_static,
    copy_theme_static,
    create_jinja_env,
    wrap_articles,
    wrap_pages,
    wrap_recipes,
)

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def cfg():
    return load_config(ROOT / "site.json")


def _make_article(slug="test", tags=None, **overrides):
    data = {
        "content_type": "article",
        "slug": slug,
        "title": slug.replace("-", " ").title(),
        "tags": tags or [],
        "category": "articles",
        "status": "published",
        "date": "2025-06-15T00:00:00",
        "locale_date": "June 15, 2025",
        "url": f"{slug}/",
        "save_as": f"{slug}/index.html",
        "content": f"<p>Content for {slug}</p>",
        "summary": "A summary",
        "excerpt": "A summary",
        "image": None,
    }
    data.update(overrides)
    return data


def _make_page(slug="about", **overrides):
    data = {
        "content_type": "page",
        "slug": slug,
        "title": slug.replace("-", " ").title(),
        "status": "published",
        "date": "2025-01-01T00:00:00",
        "locale_date": "January 1, 2025",
        "url": f"{slug}/",
        "save_as": f"{slug}/index.html",
        "content": f"<p>Content for {slug}</p>",
        "image": None,
    }
    data.update(overrides)
    return data


def _make_recipe(slug="hummus", **overrides):
    data = {
        "content_type": "recipe",
        "slug": slug,
        "title": slug.replace("-", " ").title(),
        "url": f"recipes/{slug}/",
        "save_as": f"recipes/{slug}/index.html",
        "content": f"<p>Recipe content for {slug}</p>",
        "locale_date": "",
        "image": "hummus.jpg",
        "excerpt": "A delicious recipe",
        "tags": [],
    }
    data.update(overrides)
    return data


# ---------------------------------------------------------------------------
# ArticleWrapper
# ---------------------------------------------------------------------------


class TestArticleWrapper:
    def test_basic_attributes(self):
        data = _make_article(slug="my-post", tags=["tech", "ai"])
        tag_objects = {"tech": Tag("tech"), "ai": Tag("ai")}
        wrapper = ArticleWrapper(data, tag_objects)

        assert wrapper.title == "My Post"
        assert wrapper.slug == "my-post"
        assert wrapper.url == "my-post/"
        assert wrapper.content == "<p>Content for my-post</p>"
        assert wrapper.locale_date == "June 15, 2025"

    def test_tags_are_tag_objects(self):
        data = _make_article(tags=["tech", "ai"])
        tag_objects = {"tech": Tag("tech"), "ai": Tag("ai")}
        wrapper = ArticleWrapper(data, tag_objects)

        assert len(wrapper.tags) == 2
        assert all(isinstance(t, Tag) for t in wrapper.tags)
        assert wrapper.tags[0].slug == "tech"

    def test_multilingual_defaults_empty(self):
        wrapper = ArticleWrapper(_make_article())
        assert wrapper.multilingual_urls == {}
        assert wrapper.language_links == []
        assert wrapper.translations == []
        assert wrapper.translation is False

    def test_hidden_status_preserved(self):
        wrapper = ArticleWrapper(_make_article(status="hidden"))
        assert wrapper.status == "hidden"


# ---------------------------------------------------------------------------
# PageWrapper
# ---------------------------------------------------------------------------


class TestPageWrapper:
    def test_basic_attributes(self):
        wrapper = PageWrapper(_make_page(slug="about"))
        assert wrapper.title == "About"
        assert wrapper.url == "about/"
        assert wrapper.content == "<p>Content for about</p>"

    def test_multilingual_defaults(self):
        wrapper = PageWrapper(_make_page())
        assert wrapper.multilingual_urls == {}
        assert wrapper.translations == []
        assert wrapper.modified is False


# ---------------------------------------------------------------------------
# RecipeWrapper
# ---------------------------------------------------------------------------


class TestRecipeWrapper:
    def test_basic_attributes(self):
        wrapper = RecipeWrapper(_make_recipe(slug="hummus"))
        assert wrapper.title == "Hummus"
        assert wrapper.url == "recipes/hummus/"
        assert wrapper.image == "hummus.jpg"

    def test_metadata_namespace(self):
        wrapper = RecipeWrapper(_make_recipe())
        assert wrapper.metadata.image == "hummus.jpg"
        assert wrapper.metadata.description == "A delicious recipe"
        assert wrapper.metadata.prep_time is None

    def test_recipe_tags_converted(self):
        data = _make_recipe(tags=["vegetarian"])
        tag_objects = {"vegetarian": Tag("vegetarian")}
        wrapper = RecipeWrapper(data, tag_objects)
        assert len(wrapper.tags) == 1
        assert wrapper.tags[0].slug == "vegetarian"
        # Also in metadata
        assert len(wrapper.metadata.tags) == 1


# ---------------------------------------------------------------------------
# Global context
# ---------------------------------------------------------------------------


class TestBuildGlobalContext:
    def test_sitename(self, cfg):
        ctx = build_global_context(cfg)
        assert ctx["SITENAME"] == "grtnr.com"

    def test_siteurl_empty_for_relative(self, cfg):
        ctx = build_global_context(cfg)
        # relative_urls is True in site.json
        assert ctx["SITEURL"] == ""

    def test_google_analytics(self, cfg):
        ctx = build_global_context(cfg)
        assert ctx["GOOGLE_ANALYTICS"] == "G-H8M7YDCSD4"

    def test_links_present(self, cfg):
        ctx = build_global_context(cfg)
        assert len(ctx["LINKS"]) == 4
        assert ctx["LINKS"][0] == ["Topics", "/tags"]

    def test_feeds_none_for_dev(self, cfg):
        ctx = build_global_context(cfg)
        assert ctx["FEED_ALL_ATOM"] is None


# ---------------------------------------------------------------------------
# Jinja2 environment
# ---------------------------------------------------------------------------


class TestJinjaEnv:
    def test_templates_load(self, cfg):
        env = create_jinja_env(cfg["theme_path"])
        template = env.get_template("base.html")
        assert template is not None

    def test_all_required_templates_exist(self, cfg):
        env = create_jinja_env(cfg["theme_path"])
        required = [
            "base.html",
            "index.html",
            "article.html",
            "page.html",
            "recipe.html",
            "tags.html",
            "tag.html",
            "sitemap.html",
            "robots.html",
            "archives.html",
            "recipes_index.html",
        ]
        for name in required:
            assert env.get_template(name), f"Missing template: {name}"


# ---------------------------------------------------------------------------
# Static file copying
# ---------------------------------------------------------------------------


class TestCopyThemeStatic:
    def test_copies_css_files(self, cfg, tmp_path):
        count = copy_theme_static(cfg["theme_path"], tmp_path)
        assert count > 0
        assert (tmp_path / "theme" / "css" / "poole.css").exists()
        assert (tmp_path / "theme" / "css" / "syntax.css").exists()

    def test_copies_js_files(self, cfg, tmp_path):
        copy_theme_static(cfg["theme_path"], tmp_path)
        assert (tmp_path / "theme" / "js" / "giscus-comments.js").exists()


class TestCopyContentStatic:
    def test_copies_favicon(self, cfg, tmp_path):
        count = copy_content_static(cfg["content_path"], tmp_path)
        assert count > 0
        assert (tmp_path / "favicon.ico").exists()


class TestCopyAdjacentImages:
    def test_copies_images_to_article_dir(self, tmp_path):
        # Create a fake content directory with an image
        content_dir = tmp_path / "content" / "my-article"
        content_dir.mkdir(parents=True)
        (content_dir / "photo.jpg").write_bytes(b"fake-jpg")

        items = [
            {
                "slug": "my-article",
                "save_as": "my-article/index.html",
                "content_dir": str(content_dir),
                "adjacent_files": ["photo.jpg"],
            }
        ]

        output = tmp_path / "output"
        output.mkdir()
        count = copy_adjacent_images(items, output)
        assert count == 1
        assert (output / "my-article" / "photo.jpg").exists()


# ---------------------------------------------------------------------------
# Integration: full render pipeline
# ---------------------------------------------------------------------------


class TestRenderIntegration:
    """Integration tests that render the full site from real content."""

    @pytest.fixture
    def rendered_output(self, cfg, tmp_path):
        from garten.assemble import assemble
        from garten.discover import discover
        from garten.process import process
        from garten.render import render

        cfg = dict(cfg)
        cfg["output_path"] = tmp_path / "output"

        manifest = discover(cfg)
        process(manifest, cfg)
        site = assemble(manifest, cfg)
        render(site, cfg)
        return cfg["output_path"]

    def test_index_pages_created(self, rendered_output):
        assert (rendered_output / "index.html").exists()
        assert (rendered_output / "index2.html").exists()

    def test_article_pages_created(self, rendered_output):
        assert (
            rendered_output / "how-i-code-with-claude" / "index.html"
        ).exists()

    def test_page_pages_created(self, rendered_output):
        assert (rendered_output / "about" / "index.html").exists()

    def test_recipe_pages_created(self, rendered_output):
        assert (
            rendered_output / "recipes" / "hummus-from-mr-jim" / "index.html"
        ).exists()

    def test_tags_page_created(self, rendered_output):
        assert (rendered_output / "tags" / "index.html").exists()

    def test_tag_pages_created(self, rendered_output):
        assert (rendered_output / "tag" / "tech" / "index.html").exists()

    def test_sitemap_created(self, rendered_output):
        assert (rendered_output / "sitemap.xml").exists()

    def test_robots_created(self, rendered_output):
        assert (rendered_output / "robots.txt").exists()

    def test_archives_created(self, rendered_output):
        assert (rendered_output / "archives.html").exists()

    def test_recipes_index_created(self, rendered_output):
        assert (rendered_output / "recipes" / "index.html").exists()

    def test_theme_css_copied(self, rendered_output):
        assert (rendered_output / "theme" / "css" / "poole.css").exists()

    def test_favicon_copied(self, rendered_output):
        assert (rendered_output / "favicon.ico").exists()

    def test_images_copied_to_article_dirs(self, rendered_output):
        # Check a known article with an image
        assert (
            rendered_output / "how-i-code-with-claude" / "claude.png"
        ).exists()

    def test_index_contains_article_titles(self, rendered_output):
        html = (rendered_output / "index.html").read_text()
        assert "post-title" in html

    def test_index_has_pagination(self, rendered_output):
        html = (rendered_output / "index.html").read_text()
        assert "pagination" in html

    def test_tag_page_lists_articles(self, rendered_output):
        html = (rendered_output / "tag" / "tech" / "index.html").read_text()
        assert "<li>" in html

    def test_sitemap_has_urls(self, rendered_output):
        xml = (rendered_output / "sitemap.xml").read_text()
        assert "<loc>" in xml

    def test_category_page_created(self, rendered_output):
        assert (
            rendered_output / "category" / "articles" / "index.html"
        ).exists()

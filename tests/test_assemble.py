"""Tests for garten Phase 4: Assemble."""

from __future__ import annotations

import math
from pathlib import Path

import pytest

from garten.assemble import (
    Author,
    Category,
    Tag,
    build_category_map,
    build_pagination,
    build_tag_map,
    filter_articles_for_index,
    generate_urls,
    set_locale_dates,
    sort_articles_by_date,
)
from garten.config import load_config

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def cfg():
    return load_config(ROOT / "site.json")


def _make_article(
    slug="test", tags=None, category="articles", status="published", date=""
):
    return {
        "content_type": "article",
        "slug": slug,
        "title": slug.replace("-", " ").title(),
        "tags": tags or [],
        "category": category,
        "status": status,
        "date": date,
        "excerpt": None,
        "image": None,
    }


def _make_page(slug="about", status="published"):
    return {
        "content_type": "page",
        "slug": slug,
        "title": slug.replace("-", " ").title(),
        "status": status,
        "date": "2025-01-01T00:00:00",
    }


def _make_recipe(slug="hummus"):
    return {
        "content_type": "recipe",
        "slug": slug,
        "title": slug.replace("-", " ").title(),
        "date": "",
        "date_published": "",
    }


def _make_manifest(articles=None, pages=None, recipes=None):
    return {
        "articles": articles or [],
        "pages": pages or [],
        "recipes": recipes or [],
    }


# ---------------------------------------------------------------------------
# Tag class
# ---------------------------------------------------------------------------


class TestTag:
    def test_str_returns_name(self):
        tag = Tag("Machine Learning", "machine-learning")
        assert str(tag) == "Machine Learning"

    def test_slug_derived_from_name(self):
        tag = Tag("Machine Learning")
        assert tag.slug == "machine-learning"

    def test_equality_by_slug(self):
        assert Tag("tech", "tech") == Tag("Tech", "tech")

    def test_hash_by_slug(self):
        s = {Tag("tech", "tech"), Tag("Tech", "tech")}
        assert len(s) == 1

    def test_repr(self):
        assert "Tag(" in repr(Tag("code"))


# ---------------------------------------------------------------------------
# Category class
# ---------------------------------------------------------------------------


class TestCategory:
    def test_url(self):
        cat = Category("articles")
        assert cat.url == "category/articles/"

    def test_str(self):
        cat = Category("articles")
        assert str(cat) == "articles"


# ---------------------------------------------------------------------------
# Author class
# ---------------------------------------------------------------------------


class TestAuthor:
    def test_url(self):
        auth = Author("Till Gartner")
        assert auth.url == "author/till-gartner.html"


# ---------------------------------------------------------------------------
# 4.1 URL generation
# ---------------------------------------------------------------------------


class TestGenerateUrls:
    def test_article_urls(self):
        manifest = _make_manifest(
            articles=[_make_article(slug="my-post")]
        )
        generate_urls(manifest)
        art = manifest["articles"][0]
        assert art["url"] == "my-post/"
        assert art["save_as"] == "my-post/index.html"

    def test_page_urls(self):
        manifest = _make_manifest(pages=[_make_page(slug="about")])
        generate_urls(manifest)
        page = manifest["pages"][0]
        assert page["url"] == "about/"
        assert page["save_as"] == "about/index.html"

    def test_recipe_urls(self):
        manifest = _make_manifest(recipes=[_make_recipe(slug="hummus")])
        generate_urls(manifest)
        recipe = manifest["recipes"][0]
        assert recipe["url"] == "recipes/hummus/"
        assert recipe["save_as"] == "recipes/hummus/index.html"


# ---------------------------------------------------------------------------
# Locale dates
# ---------------------------------------------------------------------------


class TestLocaleDates:
    def test_article_date_formatted(self):
        manifest = _make_manifest(
            articles=[_make_article(date="2025-06-15T00:00:00")]
        )
        set_locale_dates(manifest)
        assert manifest["articles"][0]["locale_date"] == "June 15, 2025"

    def test_missing_date_returns_empty(self):
        manifest = _make_manifest(articles=[_make_article(date="")])
        set_locale_dates(manifest)
        assert manifest["articles"][0]["locale_date"] == ""


# ---------------------------------------------------------------------------
# 4.4 Tag / category groupings
# ---------------------------------------------------------------------------


class TestBuildTagMap:
    def test_basic_tag_mapping(self):
        articles = [
            _make_article(slug="a1", tags=["tech", "ai"]),
            _make_article(slug="a2", tags=["tech"]),
        ]
        tag_map = build_tag_map(articles)
        tag_names = {str(t) for t in tag_map}
        assert "tech" in tag_names
        assert "ai" in tag_names
        # tech should have 2 articles
        tech_tag = [t for t in tag_map if str(t) == "tech"][0]
        assert len(tag_map[tech_tag]) == 2

    def test_hidden_articles_excluded(self):
        articles = [
            _make_article(slug="a1", tags=["tech"]),
            _make_article(slug="a2", tags=["tech"], status="hidden"),
        ]
        tag_map = build_tag_map(articles)
        tech_tag = [t for t in tag_map if str(t) == "tech"][0]
        assert len(tag_map[tech_tag]) == 1

    def test_empty_tags(self):
        articles = [_make_article(slug="a1", tags=[])]
        tag_map = build_tag_map(articles)
        assert len(tag_map) == 0


class TestBuildCategoryMap:
    def test_basic_category_mapping(self):
        articles = [
            _make_article(slug="a1", category="articles"),
            _make_article(slug="a2", category="articles"),
        ]
        cat_map = build_category_map(articles)
        assert len(cat_map) == 1
        cat = list(cat_map.keys())[0]
        assert str(cat) == "articles"
        assert len(cat_map[cat]) == 2


# ---------------------------------------------------------------------------
# 4.5 Pagination
# ---------------------------------------------------------------------------


class TestBuildPagination:
    def test_single_page(self):
        articles = [_make_article(slug=f"a{i}") for i in range(5)]
        pages = build_pagination(articles, per_page=10)
        assert len(pages) == 1
        assert pages[0]["page_num"] == 1
        assert pages[0]["url"] == "index.html"
        assert pages[0]["has_previous"] is False
        assert pages[0]["has_next"] is False

    def test_multiple_pages(self):
        articles = [_make_article(slug=f"a{i}") for i in range(25)]
        pages = build_pagination(articles, per_page=10)
        assert len(pages) == 3

        # First page
        assert pages[0]["has_previous"] is False
        assert pages[0]["has_next"] is True
        assert pages[0]["url"] == "index.html"
        assert pages[0]["next_url"] == "index2.html"
        assert len(pages[0]["articles"]) == 10

        # Middle page
        assert pages[1]["has_previous"] is True
        assert pages[1]["has_next"] is True
        assert pages[1]["url"] == "index2.html"
        assert pages[1]["previous_url"] == "index.html"
        assert pages[1]["next_url"] == "index3.html"

        # Last page
        assert pages[2]["has_previous"] is True
        assert pages[2]["has_next"] is False
        assert pages[2]["url"] == "index3.html"
        assert len(pages[2]["articles"]) == 5

    def test_empty_articles(self):
        pages = build_pagination([], per_page=10)
        assert pages == []

    def test_exact_page_boundary(self):
        articles = [_make_article(slug=f"a{i}") for i in range(20)]
        pages = build_pagination(articles, per_page=10)
        assert len(pages) == 2
        assert len(pages[0]["articles"]) == 10
        assert len(pages[1]["articles"]) == 10


# ---------------------------------------------------------------------------
# 4.8 Filter articles for index
# ---------------------------------------------------------------------------


class TestFilterArticlesForIndex:
    def test_hidden_excluded(self):
        articles = [
            _make_article(slug="a1"),
            _make_article(slug="a2", status="hidden"),
        ]
        result = filter_articles_for_index(articles)
        assert len(result) == 1
        assert result[0]["slug"] == "a1"

    def test_empty_categories_keeps_all(self):
        articles = [
            _make_article(slug="a1", category="articles"),
            _make_article(slug="a2", category="other"),
        ]
        result = filter_articles_for_index(articles, categories_in_index=[])
        assert len(result) == 2

    def test_category_filter(self):
        articles = [
            _make_article(slug="a1", category="articles"),
            _make_article(slug="a2", category="other"),
        ]
        result = filter_articles_for_index(
            articles, categories_in_index=["articles"]
        )
        assert len(result) == 1
        assert result[0]["slug"] == "a1"


# ---------------------------------------------------------------------------
# Sort
# ---------------------------------------------------------------------------


class TestSortArticles:
    def test_sort_by_date_descending(self):
        articles = [
            _make_article(slug="old", date="2020-01-01T00:00:00"),
            _make_article(slug="new", date="2025-01-01T00:00:00"),
            _make_article(slug="mid", date="2023-06-15T00:00:00"),
        ]
        result = sort_articles_by_date(articles)
        assert [a["slug"] for a in result] == ["new", "mid", "old"]


# ---------------------------------------------------------------------------
# Integration: real content
# ---------------------------------------------------------------------------


class TestAssembleIntegration:
    """Integration tests that run assemble on real content."""

    @pytest.fixture
    def site(self, cfg):
        from garten.assemble import assemble
        from garten.discover import discover
        from garten.process import process

        manifest = discover(cfg)
        process(manifest, cfg)
        return assemble(manifest, cfg)

    def test_all_articles_have_urls(self, site):
        for art in site["articles"]:
            assert art["url"], f"Article {art['slug']} has no URL"
            assert art["save_as"], f"Article {art['slug']} has no save_as"

    def test_all_pages_have_urls(self, site):
        for page in site["pages"]:
            assert page["url"], f"Page {page['slug']} has no URL"

    def test_all_recipes_have_urls(self, site):
        for recipe in site["recipes"]:
            assert recipe["url"], f"Recipe {recipe['slug']} has no URL"
            assert recipe["url"].startswith("recipes/")

    def test_tag_map_has_entries(self, site):
        assert len(site["tag_map"]) > 0

    def test_pagination_matches_article_count(self, site):
        total = sum(
            len(p["articles"]) for p in site["pagination"]
        )
        index_count = len(site["index_articles"])
        assert total == index_count

    def test_articles_sorted_newest_first(self, site):
        dates = [a["date"] for a in site["articles"] if a["date"]]
        for i in range(len(dates) - 1):
            assert dates[i] >= dates[i + 1]

    def test_locale_dates_set(self, site):
        for art in site["articles"]:
            if art["date"]:
                assert art["locale_date"], (
                    f"Article {art['slug']} missing locale_date"
                )

    def test_expected_pagination_pages(self, site, cfg):
        per_page = cfg.get("default_pagination", 10)
        expected = math.ceil(
            len(site["index_articles"]) / per_page
        )
        assert len(site["pagination"]) == expected

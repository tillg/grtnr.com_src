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
    build_language_links,
    build_pagination,
    build_per_language_content,
    build_tag_map,
    build_translated_links,
    filter_articles_for_index,
    generate_multilingual_urls,
    generate_urls,
    load_menu_translations,
    prefix_internal_links,
    set_locale_dates,
    sort_articles_by_date,
)
from garten.config import load_config
from garten.utils import localize_date

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
        assert pages[0]["url"] == ""
        assert pages[0]["save_as"] == "index.html"
        assert pages[0]["has_previous"] is False
        assert pages[0]["has_next"] is False

    def test_multiple_pages(self):
        articles = [_make_article(slug=f"a{i}") for i in range(25)]
        pages = build_pagination(articles, per_page=10)
        assert len(pages) == 3

        # First page — clean directory URL, file save_as
        assert pages[0]["has_previous"] is False
        assert pages[0]["has_next"] is True
        assert pages[0]["url"] == ""
        assert pages[0]["save_as"] == "index.html"
        assert pages[0]["next_url"] == "page/2/"
        assert len(pages[0]["articles"]) == 10

        # Middle page
        assert pages[1]["has_previous"] is True
        assert pages[1]["has_next"] is True
        assert pages[1]["url"] == "page/2/"
        assert pages[1]["save_as"] == "page/2/index.html"
        assert pages[1]["previous_url"] == ""
        assert pages[1]["next_url"] == "page/3/"

        # Last page
        assert pages[2]["has_previous"] is True
        assert pages[2]["has_next"] is False
        assert pages[2]["url"] == "page/3/"
        assert pages[2]["save_as"] == "page/3/index.html"
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


# ---------------------------------------------------------------------------
# Date localization (utils.localize_date)
# ---------------------------------------------------------------------------


class TestLocalizeDateEnglish:
    def test_english_format(self):
        assert localize_date("2025-06-15T00:00:00", "en") == "June 15, 2025"

    def test_english_january(self):
        assert localize_date("2026-01-01T00:00:00", "en") == "January 1, 2026"

    def test_english_december(self):
        assert localize_date("2025-12-25T00:00:00", "en") == "December 25, 2025"


class TestLocalizeDateGerman:
    def test_german_format(self):
        # 2025-06-15 is a Sunday
        result = localize_date("2025-06-15T00:00:00", "de")
        assert result == "So 15. Jun 2025"

    def test_german_weekday(self):
        # 2026-02-14 is a Saturday
        result = localize_date("2026-02-14T00:00:00", "de")
        assert result == "Sa 14. Feb 2026"


class TestLocalizeDateFrench:
    def test_french_format(self):
        # 2025-06-15 is a Sunday (dimanche)
        result = localize_date("2025-06-15T00:00:00", "fr")
        assert result == "dimanche 15 juin 2025"

    def test_french_weekday(self):
        # 2026-02-14 is a Saturday (samedi)
        result = localize_date("2026-02-14T00:00:00", "fr")
        assert result == "samedi 14 février 2026"


class TestLocalizeDateEdgeCases:
    def test_none_returns_empty(self):
        assert localize_date(None) == ""

    def test_empty_string_returns_empty(self):
        assert localize_date("") == ""

    def test_iso_date_only(self):
        assert localize_date("2025-06-15") == "June 15, 2025"

    def test_unknown_lang_falls_back_to_english(self):
        result = localize_date("2025-06-15T00:00:00", "xx")
        assert result == "June 15, 2025"

    def test_datetime_object(self):
        from datetime import datetime

        dt = datetime(2025, 3, 15)
        assert localize_date(dt, "en") == "March 15, 2025"

    def test_unparseable_string_returned_as_is(self):
        assert localize_date("not-a-date", "en") == "not-a-date"


# ---------------------------------------------------------------------------
# 4.2 Multilingual URLs
# ---------------------------------------------------------------------------


class TestGenerateMultilingualUrls:
    def test_sets_multilingual_urls(self):
        items = [{"slug": "my-post", "url": "my-post/"}]
        generate_multilingual_urls(items, ["en", "de", "fr"], "en")
        urls = items[0]["multilingual_urls"]
        assert urls["en"] == "/my-post/"
        assert urls["de"] == "/de/my-post/"
        assert urls["fr"] == "/fr/my-post/"

    def test_single_language(self):
        items = [{"slug": "test", "url": "test/"}]
        generate_multilingual_urls(items, ["en"], "en")
        assert items[0]["multilingual_urls"] == {"en": "/test/"}

    def test_non_english_default(self):
        items = [{"slug": "test", "url": "test/"}]
        generate_multilingual_urls(items, ["de", "en"], "de")
        urls = items[0]["multilingual_urls"]
        assert urls["de"] == "/test/"
        assert urls["en"] == "/en/test/"


# ---------------------------------------------------------------------------
# 4.3 Prefix internal links
# ---------------------------------------------------------------------------


class TestPrefixInternalLinks:
    def test_prefixes_internal_links(self):
        html = '<a href="/about/">About</a>'
        result = prefix_internal_links(html, "de", ["en", "de", "fr"])
        assert 'href="/de/about/"' in result

    def test_english_not_prefixed(self):
        html = '<a href="/about/">About</a>'
        result = prefix_internal_links(html, "en", ["en", "de", "fr"])
        assert 'href="/about/"' in result

    def test_theme_links_not_prefixed(self):
        html = '<a href="/theme/css/style.css">CSS</a>'
        result = prefix_internal_links(html, "de", ["en", "de", "fr"])
        assert 'href="/theme/css/style.css"' in result

    def test_static_links_not_prefixed(self):
        html = '<a href="/static/file.txt">File</a>'
        result = prefix_internal_links(html, "de", ["en", "de", "fr"])
        assert 'href="/static/file.txt"' in result

    def test_favicon_not_prefixed(self):
        html = '<link href="/favicon.ico">'
        result = prefix_internal_links(html, "de", ["en", "de", "fr"])
        assert 'href="/favicon.ico"' in result

    def test_already_prefixed_not_doubled(self):
        html = '<a href="/de/about/">About</a>'
        result = prefix_internal_links(html, "de", ["en", "de", "fr"])
        assert 'href="/de/about/"' in result
        assert "/de/de/" not in result

    def test_external_links_unchanged(self):
        # External links don't match the /path pattern
        html = '<a href="https://example.com">External</a>'
        result = prefix_internal_links(html, "de", ["en", "de", "fr"])
        assert 'href="https://example.com"' in result

    def test_empty_html(self):
        assert prefix_internal_links("", "de", ["en", "de"]) == ""

    def test_multiple_links(self):
        html = '<a href="/about/">A</a> <a href="/tags/">B</a>'
        result = prefix_internal_links(html, "fr", ["en", "fr"])
        assert 'href="/fr/about/"' in result
        assert 'href="/fr/tags/"' in result

    def test_default_lang_not_prefixed_with_custom_default(self):
        """When default_lang is 'de', German links should not be prefixed."""
        html = '<a href="/about/">About</a>'
        result = prefix_internal_links(html, "de", ["de", "en"], default_lang="de")
        assert 'href="/about/"' in result

    def test_non_default_prefixed_with_custom_default(self):
        """When default_lang is 'de', English links should be prefixed."""
        html = '<a href="/about/">About</a>'
        result = prefix_internal_links(html, "en", ["de", "en"], default_lang="de")
        assert 'href="/en/about/"' in result


# ---------------------------------------------------------------------------
# 4.7 Language switcher links
# ---------------------------------------------------------------------------


class TestBuildLanguageLinks:
    def test_returns_non_default_languages(self):
        item = {"slug": "test", "url": "test/"}
        links = build_language_links(item, ["en", "de", "fr"], "en")
        assert len(links) == 2
        codes = [l["code"] for l in links]
        assert "de" in codes
        assert "fr" in codes

    def test_urls_have_language_prefix(self):
        item = {"slug": "my-post", "url": "my-post/"}
        links = build_language_links(item, ["en", "de"], "en")
        assert links[0]["url"] == "/de/my-post/"

    def test_includes_language_names(self):
        item = {"slug": "test", "url": "test/"}
        links = build_language_links(item, ["en", "de", "fr"], "en")
        de = [l for l in links if l["code"] == "de"][0]
        fr = [l for l in links if l["code"] == "fr"][0]
        assert de["name"] == "Deutsch"
        assert fr["name"] == "Français"


# ---------------------------------------------------------------------------
# 4.5 Pagination with url_prefix
# ---------------------------------------------------------------------------


class TestBuildPaginationWithPrefix:
    def test_url_prefix(self):
        articles = [_make_article(slug=f"a{i}") for i in range(15)]
        pages = build_pagination(articles, per_page=10, url_prefix="de/")
        assert pages[0]["url"] == "de/"
        assert pages[0]["save_as"] == "de/index.html"
        assert pages[1]["url"] == "de/page/2/"
        assert pages[1]["save_as"] == "de/page/2/index.html"
        assert pages[0]["next_url"] == "de/page/2/"
        assert pages[1]["previous_url"] == "de/"

    def test_single_page_with_prefix(self):
        articles = [_make_article(slug=f"a{i}") for i in range(5)]
        pages = build_pagination(articles, per_page=10, url_prefix="fr/")
        assert pages[0]["url"] == "fr/"
        assert pages[0]["save_as"] == "fr/index.html"


# ---------------------------------------------------------------------------
# Locale dates with language
# ---------------------------------------------------------------------------


class TestSetLocaleDatesMultilingual:
    def test_german_dates(self):
        manifest = _make_manifest(
            articles=[_make_article(date="2025-06-15T00:00:00")]
        )
        set_locale_dates(manifest, lang="de")
        assert manifest["articles"][0]["locale_date"] == "So 15. Jun 2025"

    def test_french_dates(self):
        manifest = _make_manifest(
            articles=[_make_article(date="2025-06-15T00:00:00")]
        )
        set_locale_dates(manifest, lang="fr")
        assert manifest["articles"][0]["locale_date"] == "dimanche 15 juin 2025"


# ---------------------------------------------------------------------------
# 4.6 Menu translations
# ---------------------------------------------------------------------------


class TestLoadMenuTranslations:
    def test_loads_from_file(self):
        menu = load_menu_translations(ROOT)
        assert "en" in menu
        assert "de" in menu
        assert menu["de"]["Topics"] == "Themen"

    def test_missing_file_returns_empty(self, tmp_path):
        menu = load_menu_translations(tmp_path)
        assert menu == {}


class TestBuildTranslatedLinks:
    def test_translates_titles(self):
        links = [["Topics", "/tags"], ["About", "/about"]]
        menu_trans = {
            "de": {"Topics": "Themen", "About": "Über"},
        }
        result = build_translated_links(links, "de", menu_trans)
        assert result[0][0] == "Themen"
        assert result[1][0] == "Über"

    def test_prefixes_hrefs_for_non_english(self):
        links = [["Topics", "/tags"]]
        menu_trans = {"de": {"Topics": "Themen"}}
        result = build_translated_links(links, "de", menu_trans)
        assert result[0][1] == "/de/tags"

    def test_english_hrefs_unchanged(self):
        links = [["Topics", "/tags"]]
        menu_trans = {"en": {"Topics": "Topics"}}
        result = build_translated_links(links, "en", menu_trans)
        assert result[0][1] == "/tags"

    def test_missing_translation_falls_back(self):
        links = [["Custom", "/custom"]]
        menu_trans = {"de": {}}
        result = build_translated_links(links, "de", menu_trans)
        assert result[0][0] == "Custom"

    def test_default_lang_hrefs_unchanged_with_custom_default(self):
        """When default_lang is 'de', German hrefs should not be prefixed."""
        links = [["Themen", "/tags"]]
        menu_trans = {"de": {"Themen": "Themen"}}
        result = build_translated_links(links, "de", menu_trans, default_lang="de")
        assert result[0][1] == "/tags"

    def test_non_default_hrefs_prefixed_with_custom_default(self):
        """When default_lang is 'de', English hrefs should be prefixed."""
        links = [["Topics", "/tags"]]
        menu_trans = {"en": {"Topics": "Topics"}}
        result = build_translated_links(links, "en", menu_trans, default_lang="de")
        assert result[0][1] == "/en/tags"


# ---------------------------------------------------------------------------
# Build per-language content
# ---------------------------------------------------------------------------


class TestBuildPerLanguageContent:
    def test_builds_all_languages(self):
        articles = [
            _make_article(
                slug="test",
                date="2025-01-01T00:00:00",
                tags=["tech"],
            )
        ]
        articles[0]["translations"] = {}
        articles[0]["translation_files"] = {}
        articles[0]["content"] = "<p>Hello</p>"

        pages = [_make_page(slug="about")]
        pages[0]["translations"] = {}
        pages[0]["translation_files"] = {}
        pages[0]["content"] = "<p>About</p>"

        manifest = _make_manifest(articles=articles, pages=pages)
        generate_urls(manifest)

        cfg = {"categories_in_index": [], "default_pagination": 10}

        per_lang = build_per_language_content(
            manifest, ["en", "de"], "en", cfg
        )
        assert "en" in per_lang
        assert "de" in per_lang
        assert len(per_lang["en"]["articles"]) == 1
        assert len(per_lang["de"]["articles"]) == 1

    def test_lang_articles_have_prefixed_urls(self):
        articles = [_make_article(slug="test", date="2025-01-01T00:00:00")]
        articles[0]["translations"] = {}
        articles[0]["translation_files"] = {}
        articles[0]["content"] = "<p>Hello</p>"

        manifest = _make_manifest(articles=articles)
        generate_urls(manifest)

        cfg = {"categories_in_index": [], "default_pagination": 10}
        per_lang = build_per_language_content(
            manifest, ["en", "de"], "en", cfg
        )
        assert per_lang["de"]["articles"][0]["url"] == "de/test/"
        assert per_lang["de"]["articles"][0]["save_as"] == "de/test/index.html"
        assert per_lang["en"]["articles"][0]["url"] == "en/test/"

    def test_translations_used_when_available(self):
        articles = [_make_article(slug="test", date="2025-01-01T00:00:00")]
        articles[0]["translations"] = {
            "de": {
                "content": "<p>Hallo Welt</p>",
                "title": "Deutscher Titel",
                "summary": "Deutsche Zusammenfassung",
                "translation": "de",
                "translator": "Claude",
            }
        }
        articles[0]["translation_files"] = {}
        articles[0]["content"] = "<p>Hello World</p>"

        manifest = _make_manifest(articles=articles)
        generate_urls(manifest)

        cfg = {"categories_in_index": [], "default_pagination": 10}
        per_lang = build_per_language_content(
            manifest, ["en", "de"], "en", cfg
        )
        de_art = per_lang["de"]["articles"][0]
        assert de_art["title"] == "Deutscher Titel"
        assert "Hallo Welt" in de_art["content"]
        assert de_art["translator"] == "Claude"

    def test_pagination_per_language(self):
        articles = [
            _make_article(slug=f"a{i}", date=f"2025-01-{i+1:02d}T00:00:00")
            for i in range(15)
        ]
        for a in articles:
            a["translations"] = {}
            a["translation_files"] = {}
            a["content"] = f"<p>{a['slug']}</p>"

        manifest = _make_manifest(articles=articles)
        generate_urls(manifest)

        cfg = {"categories_in_index": [], "default_pagination": 10}
        per_lang = build_per_language_content(
            manifest, ["en", "de"], "en", cfg
        )
        assert len(per_lang["de"]["pagination"]) == 2
        assert per_lang["de"]["pagination"][0]["url"] == "de/"


# ---------------------------------------------------------------------------
# Integration: full assemble with multilingual
# ---------------------------------------------------------------------------


class TestAssembleMultilingualIntegration:
    """Integration tests for assemble with multilingual enabled."""

    @pytest.fixture
    def site(self, cfg):
        from garten.assemble import assemble
        from garten.discover import discover
        from garten.process import process

        manifest = discover(cfg)
        process(manifest, cfg)
        return assemble(manifest, cfg)

    def test_multilingual_enabled(self, site):
        assert site["multilingual_enabled"] is True

    def test_has_languages(self, site):
        assert site["languages"] == ["en", "de", "fr"]

    def test_has_per_lang(self, site):
        assert "per_lang" in site
        assert "en" in site["per_lang"]
        assert "de" in site["per_lang"]
        assert "fr" in site["per_lang"]

    def test_per_lang_has_articles(self, site):
        for lang in site["languages"]:
            lang_data = site["per_lang"][lang]
            assert len(lang_data["articles"]) > 0

    def test_per_lang_has_pagination(self, site):
        for lang in site["languages"]:
            lang_data = site["per_lang"][lang]
            assert len(lang_data["pagination"]) > 0

    def test_per_lang_has_tag_map(self, site):
        for lang in site["languages"]:
            lang_data = site["per_lang"][lang]
            assert len(lang_data["tag_map"]) > 0

    def test_articles_have_multilingual_urls(self, site):
        for art in site["articles"]:
            assert "multilingual_urls" in art
            assert len(art["multilingual_urls"]) == 3

    def test_articles_have_language_links(self, site):
        for art in site["articles"]:
            assert "language_links" in art
            # Should have links for non-default languages
            assert len(art["language_links"]) == 2

    def test_has_menu_translations(self, site):
        assert "menu_translations" in site
        assert "de" in site["menu_translations"]

    def test_german_original_has_en_translation_in_per_lang(self, site):
        """German-original articles should have English content in per_lang['en']."""
        en_articles = site["per_lang"]["en"]["articles"]
        crowdsourcing = [
            a for a in en_articles if "crowdsourcing" in a["slug"]
        ]
        assert len(crowdsourcing) == 1
        art = crowdsourcing[0]
        # Should use the English translation, not German original
        assert art["translation"] == "en"
        # Title should be the English translation
        assert "Coat of Arms" in art["title"]

    def test_german_original_root_level_has_english_content(self, site):
        """Root-level content for German originals should show English (Option A)."""
        crowdsourcing = [
            a for a in site["articles"] if "crowdsourcing" in a["slug"]
        ]
        assert len(crowdsourcing) == 1
        art = crowdsourcing[0]
        # The English translation title should be used at root level
        assert "Coat of Arms" in art["title"]

    def test_german_original_de_version_has_german_content(self, site):
        """The /de/ version of a German original should show German content."""
        de_articles = site["per_lang"]["de"]["articles"]
        crowdsourcing = [
            a for a in de_articles if "crowdsourcing" in a["slug"]
        ]
        assert len(crowdsourcing) == 1
        # Should use the original German content (no DE translation exists)
        assert crowdsourcing[0]["translation"] is False

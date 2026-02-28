"""Tests for garten.discover — Phase 1.

Two kinds of tests:

1. **Unit tests** for individual helpers (frontmatter parsing, title
   generation, slug normalisation, date parsing).
2. **Comparison test** that runs garten's Discover phase on the real
   content directory and asserts the results are correct.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

import pytest

# Ensure project root is on sys.path so imports work when running with
# ``python -m pytest`` from the repo root.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from garten.config import load_config
from garten.discover import (
    _build_article,
    _build_page,
    _build_recipe,
    _find_translation_files,
    _parse_date,
    _parse_tags,
    discover,
    parse_frontmatter,
    title_from_dirname,
    write_manifest,
)
from garten.utils import normalize_slug, slugify

# ===================================================================
# Unit tests — frontmatter
# ===================================================================


class TestParseFrontmatter:
    def test_basic(self):
        text = "---\ntitle: Hello World\ndate: 2025-04-18\n---\nBody here"
        meta = parse_frontmatter(text)
        assert meta["title"] == "Hello World"
        assert meta["date"] == "2025-04-18"

    def test_case_insensitive_keys(self):
        text = "---\nTitle: My Title\nTags: code, AI\n---\n"
        meta = parse_frontmatter(text)
        assert meta["title"] == "My Title"
        assert meta["tags"] == "code, AI"

    def test_quoted_values_stripped(self):
        text = '---\nexcerpt: "A nice summary"\n---\n'
        meta = parse_frontmatter(text)
        assert meta["excerpt"] == "A nice summary"

    def test_no_frontmatter(self):
        text = "Just some text"
        assert parse_frontmatter(text) == {}

    def test_colon_in_value(self):
        text = "---\ntitle: Hello: World\n---\n"
        meta = parse_frontmatter(text)
        assert meta["title"] == "Hello: World"

    def test_empty_tags(self):
        text = "---\ntags:\n---\n"
        meta = parse_frontmatter(text)
        assert meta["tags"] == ""


# ===================================================================
# Unit tests — title generation
# ===================================================================


class TestTitleFromDirname:
    def test_date_prefix_stripped(self):
        assert title_from_dirname("2025-04-18-digital-garden") == "Digital Garden"

    def test_underscores_converted(self):
        assert title_from_dirname("2012-04-10-indien_tag_1") == "Indien Tag 1"

    def test_no_date_prefix(self):
        assert title_from_dirname("about") == "About"

    def test_year_month_prefix(self):
        assert title_from_dirname("2025-07-swiftui-cheatsheet") == "Swiftui Cheatsheet"


# ===================================================================
# Unit tests — slug normalisation
# ===================================================================


class TestNormalizeSlug:
    def test_german_chars(self):
        assert normalize_slug("Käsekuchen") == "kaesekuchen"

    def test_spaces_removed(self):
        assert normalize_slug("linzer torte") == "linzertorte"

    def test_hyphens_preserved(self):
        assert normalize_slug("digital-garden") == "digital-garden"

    def test_special_chars_removed(self):
        assert normalize_slug("hello!world?") == "helloworld"

    def test_empty_string(self):
        assert normalize_slug("") == ""

    def test_eszett(self):
        assert normalize_slug("straße") == "strasse"


# ===================================================================
# Unit tests — tag parsing
# ===================================================================


class TestParseTags:
    def test_comma_separated(self):
        assert _parse_tags("code, AI") == ["code", "ai"]

    def test_single(self):
        assert _parse_tags("tech") == ["tech"]

    def test_empty(self):
        assert _parse_tags("") == []

    def test_whitespace(self):
        assert _parse_tags("  a , b , c  ") == ["a", "b", "c"]

    def test_lowercased(self):
        assert _parse_tags("Tech, AI") == ["tech", "ai"]


# ===================================================================
# Unit tests — date parsing
# ===================================================================


class TestParseDate:
    def test_simple_date(self):
        assert _parse_date("2025-04-18") == datetime(2025, 4, 18)

    def test_iso_with_tz(self):
        dt = _parse_date("2009-12-13T00:00:00.000Z")
        assert dt == datetime(2009, 12, 13, 0, 0, 0)

    def test_iso_no_tz(self):
        dt = _parse_date("2021-12-06T11:20:09.000Z")
        assert dt is not None
        assert dt.year == 2021

    def test_none(self):
        assert _parse_date(None) is None

    def test_empty(self):
        assert _parse_date("") is None


# ===================================================================
# Integration — full discover on real content
# ===================================================================


@pytest.fixture
def cfg():
    os.chdir(ROOT)
    return load_config(ROOT / "site.json")


class TestDiscoverIntegration:
    """Run Discover against the actual content directory."""

    def test_discover_returns_all_content_types(self, cfg):
        manifest = discover(cfg)
        assert "articles" in manifest
        assert "pages" in manifest
        assert "recipes" in manifest

    def test_article_count(self, cfg):
        manifest = discover(cfg)
        assert len(manifest["articles"]) >= 50

    def test_page_count(self, cfg):
        manifest = discover(cfg)
        assert len(manifest["pages"]) >= 3

    def test_recipe_count(self, cfg):
        manifest = discover(cfg)
        assert len(manifest["recipes"]) >= 30

    def test_articles_have_required_fields(self, cfg):
        manifest = discover(cfg)
        for art in manifest["articles"]:
            assert art["title"], f"Missing title for {art['source_path']}"
            assert art["slug"], f"Missing slug for {art['source_path']}"
            assert art["category"] == "articles"
            assert art["content_type"] == "article"

    def test_pages_have_required_fields(self, cfg):
        manifest = discover(cfg)
        for page in manifest["pages"]:
            assert page["title"], f"Missing title for {page['source_path']}"
            assert page["slug"], f"Missing slug for {page['source_path']}"
            assert page["content_type"] == "page"

    def test_recipes_have_required_fields(self, cfg):
        manifest = discover(cfg)
        for recipe in manifest["recipes"]:
            assert recipe["title"], f"Missing title for {recipe['source_path']}"
            assert recipe["slug"], f"Missing slug for {recipe['source_path']}"
            assert recipe["content_type"] == "recipe"

    def test_hidden_page_detected(self, cfg):
        manifest = discover(cfg)
        todo = [p for p in manifest["pages"] if p["slug"] == "todo"]
        assert len(todo) == 1
        assert todo[0]["status"] == "hidden"

    def test_translation_files_found(self, cfg):
        manifest = discover(cfg)
        # Most articles should have DE and FR translation files
        with_translations = [a for a in manifest["articles"] if a["translation_files"]]
        # At least some should have translations
        assert len(with_translations) > 0
        # Check a specific one we know has translations
        claude = [
            a for a in manifest["articles"] if "how-i-code-with-claude" in a["slug"]
        ]
        if claude:
            assert "de" in claude[0]["translation_files"]
            assert "fr" in claude[0]["translation_files"]

    def test_en_translation_found_for_german_originals(self, cfg):
        """German-original articles should have EN translation files discovered."""
        manifest = discover(cfg)
        crowdsourcing = [
            a for a in manifest["articles"] if "crowdsourcing" in a["slug"]
        ]
        assert len(crowdsourcing) == 1
        assert "en" in crowdsourcing[0]["translation_files"]

    def test_auto_title_works(self, cfg):
        """Articles without explicit title get one from directory name."""
        manifest = discover(cfg)
        # digital-garden has no title in frontmatter
        garden = [a for a in manifest["articles"] if "digital-garden" in a["slug"]]
        assert len(garden) == 1
        assert garden[0]["title"] == "Digital Garden"

    def test_explicit_title_preserved(self, cfg):
        manifest = discover(cfg)
        # indien-tag1 has explicit title: "Indien Tag 1"
        indien = [
            a
            for a in manifest["articles"]
            if a["source_path"].endswith("indien_tag_1.md")
        ]
        assert len(indien) == 1
        assert indien[0]["title"] == "Indien Tag 1"

    def test_recipe_slug_normalized(self, cfg):
        manifest = discover(cfg)
        # "Böhmischer Gulasch" has slug "bohmischer-gulasch"
        gulasch = [r for r in manifest["recipes"] if "bohmischer-gulasch" in r["slug"]]
        assert len(gulasch) == 1

    def test_summary_and_excerpt_both_work(self, cfg):
        """The SwiftUI cheatsheet uses 'summary' instead of 'excerpt'."""
        manifest = discover(cfg)
        swift = [a for a in manifest["articles"] if "swiftui" in a["slug"]]
        assert len(swift) == 1
        assert swift[0]["excerpt"] is not None

    def test_tags_parsed(self, cfg):
        manifest = discover(cfg)
        claude = [
            a for a in manifest["articles"] if "how-i-code-with-claude" in a["slug"]
        ]
        if claude:
            assert "code" in claude[0]["tags"]

    def test_write_manifest(self, cfg, tmp_path):
        manifest = discover(cfg)
        path = write_manifest(manifest, tmp_path)
        assert path.exists()
        import json

        data = json.loads(path.read_text())
        assert len(data["articles"]) >= 50

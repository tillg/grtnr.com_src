"""Tests for garten.process -- Phase 3.

Two kinds of tests:

1. **Unit tests** for individual sub-phases (markdown rendering, image URL
   fixing, summary generation, external link processing, typogrify).
2. **Integration tests** that run the full Process phase on real content
   and verify key properties of the output.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from garten.config import load_config
from garten.discover import discover
from garten.process import (
    find_adjacent_files,
    fix_image_urls,
    generate_summary,
    process,
    process_external_links,
    render_markdown,
    strip_frontmatter,
    write_artifacts,
)


# ===================================================================
# Unit tests -- strip_frontmatter
# ===================================================================


class TestStripFrontmatter:
    def test_strips_frontmatter(self):
        text = "---\ntitle: Hello\ndate: 2025-01-01\n---\nBody text here"
        assert strip_frontmatter(text) == "Body text here"

    def test_no_frontmatter(self):
        text = "Just body text"
        assert strip_frontmatter(text) == "Just body text"

    def test_preserves_body_formatting(self):
        text = "---\ntitle: Test\n---\n# Heading\n\nParagraph **bold**\n"
        body = strip_frontmatter(text)
        assert body.startswith("# Heading")
        assert "**bold**" in body

    def test_frontmatter_with_colons_in_values(self):
        text = '---\ntitle: Hello: World\nexcerpt: "A nice: summary"\n---\nBody'
        assert strip_frontmatter(text) == "Body"


# ===================================================================
# Unit tests -- 3.1 Markdown rendering
# ===================================================================


class TestRenderMarkdown:
    def test_basic_paragraph(self):
        html = render_markdown("Hello world")
        assert "<p>" in html
        assert "Hello world" in html

    def test_heading(self):
        html = render_markdown("# Title\n\nParagraph")
        assert "<h1" in html  # TOC extension adds id attribute
        assert "Title" in html

    def test_bold_italic(self):
        html = render_markdown("**bold** and *italic*")
        assert "<strong>bold</strong>" in html
        assert "<em>italic</em>" in html

    def test_code_block(self):
        html = render_markdown("```python\nprint('hello')\n```")
        assert "highlight" in html  # codehilite css class
        assert "print" in html

    def test_fenced_code_without_lang(self):
        html = render_markdown("```\nsome code\n```")
        assert "some code" in html

    def test_link(self):
        html = render_markdown("[text](https://example.com)")
        assert 'href="https://example.com"' in html

    def test_image(self):
        html = render_markdown("![alt text](image.png)")
        assert "<img" in html
        assert 'src="image.png"' in html
        assert "alt" in html

    def test_toc_marker(self):
        md = "[TOC]\n\n# One\n\n## Two\n\n### Three"
        html = render_markdown(md)
        assert '<div class="toc">' in html

    def test_wikilinks_simple(self):
        html = render_markdown("See [[Digital Garden]] for more.")
        assert 'href="/digital-garden/"' in html
        assert "Digital Garden" in html

    def test_wikilinks_with_display_text(self):
        html = render_markdown("Read [[My Page|this page]].")
        assert 'href="/my-page/"' in html
        assert "this page" in html

    def test_wikilinks_german_chars(self):
        html = render_markdown("See [[Käsekuchen]]")
        assert 'href="/kaesekuchen/"' in html

    def test_table(self):
        md = "| A | B |\n|---|---|\n| 1 | 2 |"
        html = render_markdown(md)
        assert "<table>" in html

    def test_footnotes(self):
        md = "Text[^1]\n\n[^1]: Footnote content"
        html = render_markdown(md)
        assert "Footnote" in html


# ===================================================================
# Unit tests -- 3.2 Image URL fixing
# ===================================================================


class TestFixImageUrls:
    def test_html_img_tag(self):
        html = '<img src="photo.jpg" alt="Photo">'
        result = fix_image_urls(html, "my-article", ["photo.jpg"])
        assert 'src="/my-article/photo.jpg"' in result

    def test_already_absolute_unchanged(self):
        html = '<img src="/absolute/photo.jpg" alt="Photo">'
        result = fix_image_urls(html, "my-article", ["photo.jpg"])
        assert 'src="/absolute/photo.jpg"' in result

    def test_external_url_unchanged(self):
        html = '<img src="https://example.com/photo.jpg">'
        result = fix_image_urls(html, "my-article", ["photo.jpg"])
        assert 'src="https://example.com/photo.jpg"' in result

    def test_markdown_image(self):
        html = "![Alt](photo.jpg)"
        result = fix_image_urls(html, "my-article", ["photo.jpg"])
        assert "(/my-article/photo.jpg)" in result

    def test_anchor_tag_pdf(self):
        html = '<a href="document.pdf">Download</a>'
        result = fix_image_urls(html, "my-article", ["document.pdf"])
        assert 'href="/my-article/document.pdf"' in result

    def test_anchor_with_hash_unchanged(self):
        html = '<a href="#section">Jump</a>'
        result = fix_image_urls(html, "slug", ["section"])
        # hash links should not be modified
        assert 'href="#section"' in result

    def test_multiple_images(self):
        html = '<img src="a.jpg"><img src="b.png">'
        result = fix_image_urls(html, "slug", ["a.jpg", "b.png"])
        assert 'src="/slug/a.jpg"' in result
        assert 'src="/slug/b.png"' in result

    def test_no_matching_images_unchanged(self):
        html = '<img src="other.jpg">'
        result = fix_image_urls(html, "slug", ["photo.jpg"])
        assert 'src="other.jpg"' in result


# ===================================================================
# Unit tests -- 3.2 Find adjacent files
# ===================================================================


class TestFindAdjacentFiles:
    def test_finds_images(self, tmp_path):
        (tmp_path / "photo.jpg").touch()
        (tmp_path / "diagram.png").touch()
        (tmp_path / "content.md").touch()
        files = find_adjacent_files(tmp_path)
        assert "photo.jpg" in files
        assert "diagram.png" in files
        assert "content.md" not in files

    def test_finds_attachments(self, tmp_path):
        att_dir = tmp_path / "attachments"
        att_dir.mkdir()
        (att_dir / "document.pdf").touch()
        (att_dir / "data.csv").touch()
        files = find_adjacent_files(tmp_path)
        assert "document.pdf" in files
        assert "data.csv" in files

    def test_empty_directory(self, tmp_path):
        assert find_adjacent_files(tmp_path) == []

    def test_nonexistent_directory(self):
        assert find_adjacent_files(Path("/nonexistent")) == []

    def test_svg_and_gif(self, tmp_path):
        (tmp_path / "icon.svg").touch()
        (tmp_path / "animation.gif").touch()
        files = find_adjacent_files(tmp_path)
        assert "icon.svg" in files
        assert "animation.gif" in files


# ===================================================================
# Unit tests -- 3.3 Summary generation
# ===================================================================


class TestGenerateSummary:
    def test_basic(self):
        assert generate_summary("A nice summary") == "A nice summary"

    def test_strips_quotes(self):
        assert generate_summary('"Quoted summary"') == "Quoted summary"

    def test_none(self):
        assert generate_summary(None) == ""

    def test_empty(self):
        assert generate_summary("") == ""

    def test_whitespace_stripped(self):
        assert generate_summary("  spaced  ") == "spaced"

    def test_single_quotes_not_stripped(self):
        assert generate_summary("It's a test") == "It's a test"


# ===================================================================
# Unit tests -- 3.4 External links
# ===================================================================


class TestProcessExternalLinks:
    def test_adds_target_blank(self):
        html = '<a href="https://example.com">Link</a>'
        result = process_external_links(html)
        assert 'target="_blank"' in result
        assert 'rel="noopener noreferrer"' in result

    def test_http_link(self):
        html = '<a href="http://example.com">Link</a>'
        result = process_external_links(html)
        assert 'target="_blank"' in result

    def test_internal_link_unchanged(self):
        html = '<a href="/about/">About</a>'
        result = process_external_links(html)
        assert "target" not in result

    def test_relative_link_unchanged(self):
        html = '<a href="page.html">Page</a>'
        result = process_external_links(html)
        assert "target" not in result

    def test_hash_link_unchanged(self):
        html = '<a href="#section">Jump</a>'
        result = process_external_links(html)
        assert "target" not in result

    def test_empty_html(self):
        assert process_external_links("") == ""

    def test_multiple_links(self):
        html = (
            '<a href="https://a.com">A</a> '
            '<a href="/local/">L</a> '
            '<a href="https://b.com">B</a>'
        )
        result = process_external_links(html)
        assert result.count('target="_blank"') == 2


# ===================================================================
# Unit tests -- Typogrify
# ===================================================================


class TestTypogrify:
    def test_smart_quotes(self):
        html = render_markdown('"Hello" said the bot.')
        # After typogrify: straight quotes become curly
        from typogrify.filters import typogrify

        result = typogrify(html)
        assert "\u201c" in result or "&ldquo;" in result or "&#8220;" in result

    def test_ampersand(self):
        from typogrify.filters import typogrify

        result = typogrify("<p>Bread &amp; Butter</p>")
        assert "amp" in result.lower() or "&" in result


# ===================================================================
# Integration -- full process on real content
# ===================================================================


@pytest.fixture
def cfg():
    os.chdir(ROOT)
    return load_config(ROOT / "site.json")


@pytest.fixture
def manifest(cfg):
    return discover(cfg)


class TestProcessIntegration:
    """Run Process on the real content directory."""

    def test_process_returns_manifest(self, manifest, cfg):
        result = process(manifest, cfg)
        assert "articles" in result
        assert "pages" in result
        assert "recipes" in result

    def test_all_articles_have_content(self, manifest, cfg):
        process(manifest, cfg)
        for art in manifest["articles"]:
            assert art["content"], (
                f"Article {art['slug']} has empty content"
            )

    def test_all_pages_have_content(self, manifest, cfg):
        process(manifest, cfg)
        for page in manifest["pages"]:
            assert page["content"], (
                f"Page {page['slug']} has empty content"
            )

    def test_all_recipes_have_content(self, manifest, cfg):
        process(manifest, cfg)
        for recipe in manifest["recipes"]:
            assert recipe["content"], (
                f"Recipe {recipe['slug']} has empty content"
            )

    def test_articles_with_excerpt_have_summary(self, manifest, cfg):
        process(manifest, cfg)
        articles_with_excerpt = [
            a for a in manifest["articles"] if a.get("excerpt")
        ]
        for art in articles_with_excerpt:
            assert art["summary"], (
                f"Article {art['slug']} has excerpt but no summary"
            )

    def test_external_links_have_target_blank(self, manifest, cfg):
        process(manifest, cfg)
        # Pick an article that has external links
        for art in manifest["articles"]:
            if "https://" in art["content"]:
                assert 'target="_blank"' in art["content"], (
                    f"Article {art['slug']} has external links "
                    f"without target=_blank"
                )
                break

    def test_wikilinks_resolved(self, manifest, cfg):
        process(manifest, cfg)
        garden = [
            a for a in manifest["articles"] if "digital-garden" in a["slug"]
        ]
        assert len(garden) == 1
        content = garden[0]["content"]
        # WikiLinks should be resolved to proper href links
        assert "[[" not in content, (
            "Unresolved WikiLinks found in digital-garden article"
        )

    def test_image_urls_fixed(self, manifest, cfg):
        process(manifest, cfg)
        # Find an article with adjacent images
        for art in manifest["articles"]:
            if art.get("adjacent_files"):
                # Image URLs in content should be absolute
                for img_name in art["adjacent_files"]:
                    if img_name in art["content"]:
                        assert (
                            f'/{art["slug"]}/{img_name}' in art["content"]
                        ), (
                            f"Image {img_name} not properly prefixed "
                            f"in article {art['slug']}"
                        )
                break

    def test_content_is_html(self, manifest, cfg):
        process(manifest, cfg)
        # All content should contain HTML tags
        for art in manifest["articles"][:5]:
            assert "<" in art["content"], (
                f"Article {art['slug']} content doesn't look like HTML"
            )

    def test_write_artifacts(self, manifest, cfg, tmp_path):
        process(manifest, cfg)
        path = write_artifacts(manifest, tmp_path)
        assert path.exists()

        # Check HTML files were written
        html_dir = tmp_path / "process" / "html"
        assert (html_dir / "articles").is_dir()
        assert (html_dir / "pages").is_dir()
        assert (html_dir / "recipes").is_dir()

        # Check files exist: original + translations
        article_htmls = list((html_dir / "articles").glob("*.html"))
        total_translations = sum(
            len(a.get("translations", {})) for a in manifest["articles"]
        )
        expected = len(manifest["articles"]) + total_translations
        assert len(article_htmls) == expected

    def test_recipe_content_has_html(self, manifest, cfg):
        """Recipes have no separate structured data -- all structure
        is in the markdown body rendered as HTML."""
        process(manifest, cfg)
        for recipe in manifest["recipes"]:
            assert "<p>" in recipe["content"] or "<h" in recipe["content"], (
                f"Recipe {recipe['slug']} content missing HTML structure"
            )


# ===================================================================
# Spot-check: specific content items
# ===================================================================


class TestSpotChecks:
    """Verify specific articles render expected features correctly."""

    def test_code_highlighting(self, manifest, cfg):
        """Articles with code blocks should have syntax highlighting."""
        process(manifest, cfg)
        js = [
            a
            for a in manifest["articles"]
            if "playing-with-javascript" in a["slug"]
        ]
        if js:
            assert "highlight" in js[0]["content"]

    def test_toc_generation(self, manifest, cfg):
        """Articles using [TOC] should have a table of contents."""
        process(manifest, cfg)
        garden = [
            a for a in manifest["articles"] if "digital-garden" in a["slug"]
        ]
        if garden:
            assert '<div class="toc">' in garden[0]["content"]

    def test_recipe_with_image(self, manifest, cfg):
        """Recipe with inline image should have fixed URL."""
        process(manifest, cfg)
        banh = [
            r for r in manifest["recipes"] if r["slug"] == "banh-xeo"
        ]
        if banh:
            content = banh[0]["content"]
            # The inline image should have a fixed URL
            assert "Vietnamesisches-Banh-xeo-Rezept.jpg" in content


# ===================================================================
# Unit tests -- 3.5 Translation processing
# ===================================================================


class TestParseTranslationFrontmatter:
    def test_basic_frontmatter(self):
        from garten.process import _parse_translation_frontmatter

        text = '---\ntitle: "Hallo Welt"\nlang: de\n---\nBody'
        meta = _parse_translation_frontmatter(text)
        assert meta["title"] == "Hallo Welt"
        assert meta["lang"] == "de"

    def test_no_frontmatter(self):
        from garten.process import _parse_translation_frontmatter

        meta = _parse_translation_frontmatter("Just body text")
        assert meta == {}

    def test_strips_quotes(self):
        from garten.process import _parse_translation_frontmatter

        text = "---\ntitle: 'Quoted'\nexcerpt: \"Double\"\n---\nBody"
        meta = _parse_translation_frontmatter(text)
        assert meta["title"] == "Quoted"
        assert meta["excerpt"] == "Double"

    def test_keys_lowercased(self):
        from garten.process import _parse_translation_frontmatter

        text = "---\nTitle: Hello\nSource_Hash: abc123\n---\nBody"
        meta = _parse_translation_frontmatter(text)
        assert "title" in meta
        assert "source_hash" in meta


class TestProcessTranslation:
    def test_processes_translation_file(self, tmp_path):
        from garten.process import _process_translation

        # Create a translation file
        trans_file = tmp_path / "test-de.md"
        trans_file.write_text(
            '---\ntitle: "Deutscher Titel"\n'
            "translator: Claude\n---\n\n"
            "Dies ist der **übersetzte** Inhalt.\n",
            encoding="utf-8",
        )

        item = {
            "slug": "test",
            "content_type": "article",
            "adjacent_files": [],
        }

        result = _process_translation(item, "de", str(trans_file))
        assert result is not None
        assert result["lang"] == "de"
        assert result["title"] == "Deutscher Titel"
        assert result["translator"] == "Claude"
        assert "<strong>" in result["content"]

    def test_missing_file_returns_none(self):
        from garten.process import _process_translation

        item = {"slug": "test", "content_type": "article", "adjacent_files": []}
        result = _process_translation(item, "de", "/nonexistent/file.md")
        assert result is None

    def test_falls_back_to_original_title(self, tmp_path):
        from garten.process import _process_translation

        trans_file = tmp_path / "test-de.md"
        trans_file.write_text("---\nlang: de\n---\nTranslated body\n")

        item = {
            "slug": "test",
            "title": "Original Title",
            "content_type": "article",
            "adjacent_files": [],
        }

        result = _process_translation(item, "de", str(trans_file))
        assert result["title"] == "Original Title"


class TestProcessTranslations:
    def test_adds_translations_dict(self, tmp_path):
        from garten.process import _process_translations

        # Create translation files
        de_file = tmp_path / "test-de.md"
        de_file.write_text('---\ntitle: "DE Title"\n---\nDeutsch\n')

        item = {
            "slug": "test",
            "content_type": "article",
            "adjacent_files": [],
            "translation_files": {"de": str(de_file)},
        }

        _process_translations(item)
        assert "translations" in item
        assert "de" in item["translations"]
        assert item["translations"]["de"]["title"] == "DE Title"

    def test_empty_translation_files(self):
        from garten.process import _process_translations

        item = {
            "slug": "test",
            "content_type": "article",
            "translation_files": {},
        }
        _process_translations(item)
        assert item["translations"] == {}

    def test_no_translation_files_key(self):
        from garten.process import _process_translations

        item = {"slug": "test", "content_type": "article"}
        _process_translations(item)
        assert item["translations"] == {}


class TestProcessIntegrationTranslations:
    """Integration tests for translation processing on real content."""

    def test_articles_have_translations_dict(self, manifest, cfg):
        process(manifest, cfg)
        for art in manifest["articles"]:
            assert "translations" in art

    def test_pages_have_translations_dict(self, manifest, cfg):
        process(manifest, cfg)
        for page in manifest["pages"]:
            assert "translations" in page

    def test_translated_articles_have_html(self, manifest, cfg):
        process(manifest, cfg)
        for art in manifest["articles"]:
            for lang, trans in art.get("translations", {}).items():
                assert trans.get("content"), (
                    f"Translation {lang} for {art['slug']} has empty content"
                )
                assert "<" in trans["content"], (
                    f"Translation {lang} for {art['slug']} is not HTML"
                )

    def test_write_artifacts_includes_translations(self, manifest, cfg, tmp_path):
        process(manifest, cfg)
        write_artifacts(manifest, tmp_path)
        html_dir = tmp_path / "process" / "html" / "articles"
        # Check for translation HTML files
        for art in manifest["articles"]:
            for lang in art.get("translations", {}):
                trans_file = html_dir / f"{art['slug']}-{lang}.html"
                assert trans_file.exists(), (
                    f"Missing translation HTML: {trans_file.name}"
                )

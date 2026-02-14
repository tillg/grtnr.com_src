"""
Multilingual Site Plugin for Pelican

This plugin creates a multilingual website structure by:
1. Generating language-specific versions of all content
2. Creating proper URL structures for each language
3. Providing language switching functionality
4. Adding SEO-friendly hreflang tags
"""

import locale
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from pelican import signals
from pelican.contents import Article, Page
from pelican.generators import Generator
from pelican.writers import Writer

# Import centralized logging
try:
    from logger_config import get_logger

    logger = get_logger("multilingual_site")
except ImportError:
    import logging

    logger = logging.getLogger("multilingual_site")

# Import normalize_slug function
from normalize_slugs import normalize_slug


class DateLocalizer:
    """Handles date localization for different languages"""

    def __init__(self):
        # Language-specific date formats and month/day names
        self.lang_configs = {
            "en": {
                "locale": "en_US.UTF-8",
                "months": [
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December",
                ],
                "months_short": [
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dec",
                ],
                "weekdays": [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ],
                "weekdays_short": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                "format": "%a %d %b %Y",  # Wed 21 May 2025
            },
            "de": {
                "locale": "de_DE.UTF-8",
                "months": [
                    "Januar",
                    "Februar",
                    "März",
                    "April",
                    "Mai",
                    "Juni",
                    "Juli",
                    "August",
                    "September",
                    "Oktober",
                    "November",
                    "Dezember",
                ],
                "months_short": [
                    "Jan",
                    "Feb",
                    "Mär",
                    "Apr",
                    "Mai",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Okt",
                    "Nov",
                    "Dez",
                ],
                "weekdays": [
                    "Montag",
                    "Dienstag",
                    "Mittwoch",
                    "Donnerstag",
                    "Freitag",
                    "Samstag",
                    "Sonntag",
                ],
                "weekdays_short": ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"],
                "format": "%a %d. %b %Y",  # Mi 21. Mai 2025
            },
            "fr": {
                "locale": "fr_FR.UTF-8",
                "months": [
                    "janvier",
                    "février",
                    "mars",
                    "avril",
                    "mai",
                    "juin",
                    "juillet",
                    "août",
                    "septembre",
                    "octobre",
                    "novembre",
                    "décembre",
                ],
                "months_short": [
                    "jan",
                    "fév",
                    "mar",
                    "avr",
                    "mai",
                    "jun",
                    "jul",
                    "aoû",
                    "sep",
                    "oct",
                    "nov",
                    "déc",
                ],
                "weekdays": [
                    "lundi",
                    "mardi",
                    "mercredi",
                    "jeudi",
                    "vendredi",
                    "samedi",
                    "dimanche",
                ],
                "weekdays_short": ["lun", "mar", "mer", "jeu", "ven", "sam", "dim"],
                "format": "%a %d %b %Y",  # mer 21 mai 2025
            },
        }

    def localize_date(self, date_obj, target_lang: str) -> str:
        """Convert a date object to localized string"""
        if target_lang not in self.lang_configs:
            target_lang = "en"  # fallback to English

        config = self.lang_configs[target_lang]

        try:
            # Get date components
            weekday_idx = date_obj.weekday()  # 0=Monday, 6=Sunday
            month_idx = date_obj.month - 1  # 0-based index for months

            # Build localized date string
            weekday_short = config["weekdays_short"][weekday_idx]
            month_short = config["months_short"][month_idx]

            if target_lang == "de":
                # German format: "Mi 21. Mai 2025"
                return f"{weekday_short} {date_obj.day}. {month_short} {date_obj.year}"
            elif target_lang == "fr":
                # French format: "Mercredi 21 mai 2025"
                weekday_full = config["weekdays"][weekday_idx]
                month_full = config["months"][month_idx]
                return f"{weekday_full} {date_obj.day} {month_full} {date_obj.year}"
            else:
                # English format: "Wed 21 May 2025"
                return f"{weekday_short} {date_obj.day} {month_short} {date_obj.year}"

        except Exception as e:
            logger.warning(f"Failed to localize date for language {target_lang}: {e}")
            # Fallback to English format
            return date_obj.strftime("%a %d %b %Y")


class StaticURLGenerator:
    """Generates static URLs for all languages during build"""

    def __init__(self, default_lang="en", supported_langs=None):
        if supported_langs is None:
            supported_langs = ["en", "de", "fr"]
        self.default_lang = default_lang
        self.supported_langs = supported_langs

    def generate_language_urls(
        self, content_slug: str, translations: Dict[str, str]
    ) -> Dict[str, str]:
        """Generate URLs for all language versions of content"""
        urls = {}
        for lang in self.supported_langs:
            if lang in translations:
                translated_slug = translations[lang]
                urls[lang] = f"/{lang}/{translated_slug}/"
            else:
                # Fallback to default language slug
                urls[lang] = f"/{lang}/{content_slug}/"
        return urls

    def get_canonical_url(self, content_slug: str, lang: str) -> str:
        """Get canonical URL for SEO purposes"""
        return f"/{lang}/{content_slug}/"


class MultilingualContentProcessor:
    """Transforms content for multilingual output"""

    def __init__(self, settings):
        self.settings = settings
        self.default_lang = settings.get("DEFAULT_LANG", "en")
        self.supported_langs = settings.get(
            "MULTILINGUAL_LANGUAGES", ["en", "de", "fr"]
        )
        self.url_generator = StaticURLGenerator(self.default_lang, self.supported_langs)
        self.date_localizer = DateLocalizer()

    def process_articles(self, articles: List[Article]) -> Dict[str, List[Article]]:
        """Process articles for each language"""
        processed_articles = {lang: [] for lang in self.supported_langs}

        logger.debug(f"Processing {len(articles)} articles for multilingual content")
        for article in articles:
            # Skip translation files themselves
            if self._is_translation_file(article):
                logger.debug(
                    f"Skipping translation file: {getattr(article, 'source_path', 'unknown')}"
                )
                continue

            # Process original content (assume English)
            original_lang = self._detect_content_language(article)
            logger.debug(
                f"Processing article '{getattr(article, 'title', 'unknown')}' in language '{original_lang}'"
            )

            # For now, put original English content in English list
            if original_lang == "en":
                # Add localized date for English articles too
                if hasattr(article, "date") and article.date:
                    article.locale_date = self.date_localizer.localize_date(
                        article.date, "en"
                    )
                processed_articles["en"].append(article)

            # Add language-specific metadata
            article.lang = original_lang
            article.multilingual_urls = self._get_multilingual_urls(article)

            # Process translations and add translated articles
            translations = self._find_translations(article)
            logger.debug(
                f"Found {len(translations)} translations for article '{article.title}': {list(translations.keys())}"
            )

            # For each supported language, add either the translation or the original as fallback
            for lang in self.supported_langs:
                if lang == original_lang:
                    continue  # Already added above

                if lang in translations:
                    # Add translation if available
                    try:
                        logger.debug(
                            f"Processing translation for '{article.title}' in language '{lang}'"
                        )
                        translated_article = (
                            self._create_translated_article_from_content(
                                article, translations[lang], lang
                            )
                        )
                        processed_articles[lang].append(translated_article)
                        logger.debug(
                            f"Added translated article '{translated_article.title}' for language '{lang}'"
                        )
                    except Exception as e:
                        logger.warning(
                            f"Failed to process translation for {article.title} in {lang}: {e}"
                        )
                        logger.exception("Full exception details:")
                        # Fall back to original if translation fails
                        processed_articles[lang].append(article)
                else:
                    # Add original article as fallback if no translation available
                    logger.debug(
                        f"No translation for '{article.title}' in '{lang}', using original"
                    )
                    processed_articles[lang].append(article)

        return processed_articles

    def process_pages(self, pages: List[Page]) -> Dict[str, List[Page]]:
        """Process pages for each language"""
        processed_pages = {lang: [] for lang in self.supported_langs}

        for page in pages:
            # Skip translation files themselves
            if self._is_translation_file(page):
                continue

            # Process original content
            original_lang = self._detect_content_language(page)
            processed_pages[original_lang].append(page)

            # Add language-specific metadata
            page.lang = original_lang
            page.multilingual_urls = self._get_multilingual_urls(page)

            # Process translations
            translations = self._find_translations(page)
            for lang, translated_content in translations.items():
                if lang != original_lang:
                    translated_page = self._create_translated_page(
                        page, translated_content, lang
                    )
                    processed_pages[lang].append(translated_page)

        return processed_pages

    def _is_translation_file(self, content) -> bool:
        """Check if content is a translation file"""
        source_path = getattr(content, "source_path", "")
        return "/extensions/" in source_path

    def _detect_content_language(self, content) -> str:
        """Detect the language of content"""
        # For now, assume all original content is in default language
        # This could be enhanced with actual language detection
        return self.default_lang

    def _find_translations(self, content) -> Dict[str, str]:
        """Find translation files for given content"""
        translations = {}

        source_path = Path(getattr(content, "source_path", ""))
        logger.debug(f"Looking for translations for: {source_path}")
        if not source_path.exists():
            logger.debug(f"Source path does not exist: {source_path}")
            return translations

        # Look for translations in extensions directory
        extensions_dir = source_path.parent / "extensions"
        logger.debug(f"Looking for extensions directory: {extensions_dir}")
        if not extensions_dir.exists():
            logger.debug(f"Extensions directory does not exist: {extensions_dir}")
            return translations

        base_name = source_path.stem
        logger.debug(f"Looking for translations with base name: {base_name}")

        # Find translation files
        for lang in self.supported_langs:
            if lang == self.default_lang:
                continue

            translation_file = extensions_dir / f"{base_name}-{lang.upper()}.md"
            logger.debug(f"Checking for translation file: {translation_file}")
            if translation_file.exists():
                logger.debug(f"Found translation file for {lang}: {translation_file}")
                try:
                    with open(translation_file, "r", encoding="utf-8") as f:
                        translations[lang] = f.read()
                except Exception as e:
                    logger.error(
                        f"Failed to read translation file {translation_file}: {e}"
                    )
            else:
                logger.debug(
                    f"No translation file found for {lang}: {translation_file}"
                )

        logger.debug(
            f"Found {len(translations)} translations: {list(translations.keys())}"
        )
        return translations

    def _get_multilingual_urls(self, content) -> Dict[str, str]:
        """Get multilingual URLs for content"""
        content_slug = getattr(content, "slug", "")
        translations = self._find_translations(content)

        # Create a mapping of language to translated slugs
        translated_slugs = {}
        for lang in self.supported_langs:
            if lang in translations:
                # Extract slug from translation metadata if available
                translated_slugs[lang] = self._extract_translated_slug(
                    translations[lang], content_slug
                )
            else:
                translated_slugs[lang] = content_slug

        return self.url_generator.generate_language_urls(content_slug, translated_slugs)

    def _extract_translated_slug(
        self, translation_content: str, fallback_slug: str
    ) -> str:
        """Extract or generate translated slug from content"""
        # For now, use the original slug
        # This could be enhanced to translate slugs as well
        return fallback_slug

    def _create_translated_article(
        self, original_article: Article, translation_content: str, lang: str
    ) -> Article:
        """Create a translated article object"""
        # For now, create a copy of the original article with language-specific properties
        # This avoids the complex Article constructor issues
        translated_article = type(original_article)(
            original_article._content,
            metadata=original_article.metadata.copy(),
            source_path=original_article.source_path,
            context=original_article._context,
        )

        # Copy essential attributes from original (skip read-only properties)
        skipped_attrs = {"save_as", "url", "filename", "source_path", "_content"}
        for attr in dir(original_article):
            if (
                not attr.startswith("_")
                and hasattr(original_article, attr)
                and attr not in skipped_attrs
            ):
                try:
                    value = getattr(original_article, attr)
                    if not callable(value):  # Skip methods
                        setattr(translated_article, attr, value)
                except (AttributeError, TypeError):
                    pass  # Skip problematic attributes

        # Set language-specific attributes
        translated_article.lang = lang
        translated_article.original_article = original_article
        translated_article.multilingual_urls = original_article.multilingual_urls

        # Override metadata to include language-specific URLs
        translated_article.metadata = translated_article.metadata.copy()
        translated_article.metadata["lang"] = lang

        # Set language-specific save path and URL through metadata
        original_slug = getattr(translated_article, "slug", "unknown")
        translated_article.metadata["save_as"] = f"{lang}/{original_slug}/index.html"
        translated_article.metadata["url"] = f"/{lang}/{original_slug}/"

        return translated_article

    def _create_translated_article_from_content(
        self, original_article: Article, translation_content: str, lang: str
    ) -> Article:
        """Create a translated article with actual translated content"""
        # Parse the translation content to extract the inner markdown
        metadata, content = self._parse_translation_content(translation_content)
        logger.debug(f"Parsed translation metadata: {metadata}")
        logger.debug(f"Translated content length: {len(content)} chars")

        # Extract a clean summary from the markdown content before processing
        clean_summary = self._extract_clean_summary(content)

        # Process the markdown content to HTML using Pelican's markdown processor
        processed_content = self._process_markdown_content(content)
        logger.debug(f"Processed content length: {len(processed_content)} chars")

        # Create a new metadata dict with language-specific URL settings
        new_metadata = original_article.metadata.copy()
        original_slug = getattr(original_article, "slug", "unknown")
        new_metadata["save_as"] = f"{lang}/{original_slug}/index.html"
        new_metadata["url"] = (
            f"{lang}/{original_slug}"  # Remove both leading and trailing slash to prevent double slash
        )
        new_metadata["lang"] = lang

        # Override with translated metadata if available
        if "excerpt" in metadata:
            clean_excerpt = self._process_markdown_content(metadata["excerpt"])
            # Remove wrapping <p> tags if it's a single paragraph for inline display
            if (
                clean_excerpt.startswith("<p>")
                and clean_excerpt.endswith("</p>")
                and clean_excerpt.count("<p>") == 1
            ):
                clean_excerpt = clean_excerpt[3:-4]
            new_metadata["excerpt"] = clean_excerpt
            new_metadata["summary"] = (
                clean_excerpt  # Also set summary for template display
            )
            logger.debug(
                f"Set translated excerpt and summary for {lang}: {clean_excerpt}"
            )

        # Handle summary field directly (some articles use summary instead of excerpt)
        if "summary" in metadata:
            clean_summary_from_meta = self._process_markdown_content(
                metadata["summary"]
            )
            # Remove wrapping <p> tags if it's a single paragraph for inline display
            if (
                clean_summary_from_meta.startswith("<p>")
                and clean_summary_from_meta.endswith("</p>")
                and clean_summary_from_meta.count("<p>") == 1
            ):
                clean_summary_from_meta = clean_summary_from_meta[3:-4]
            new_metadata["summary"] = clean_summary_from_meta
            logger.debug(
                f"Set translated summary for {lang}: {clean_summary_from_meta}"
            )

        # If no explicit summary/excerpt in metadata, use the clean summary we extracted
        if (
            "summary" not in new_metadata
            and "excerpt" not in new_metadata
            and clean_summary
        ):
            new_metadata["summary"] = clean_summary
            logger.debug(
                f"Set auto-generated clean summary for {lang}: {clean_summary[:100]}..."
            )

        # Override title if provided in translated metadata
        if "title" in metadata:
            new_metadata["title"] = metadata["title"]
            logger.debug(f"Set translated title: {metadata['title']}")

        # Create a new article with the processed content and updated metadata
        # Pass the processed HTML content instead of raw markdown
        translated_article = type(original_article)(
            processed_content,  # Use the processed HTML content
            metadata=new_metadata,
            source_path=original_article.source_path,
            context=original_article._context,
        )

        # Copy attributes but override with language-specific ones
        for attr in ["slug", "date", "category", "tags", "author"]:
            if hasattr(original_article, attr):
                try:
                    setattr(translated_article, attr, getattr(original_article, attr))
                except AttributeError:
                    # Some attributes might be read-only
                    pass

        # Set language-specific attributes
        translated_article.lang = lang

        # Add localized date if the article has a date
        if hasattr(translated_article, "date") and translated_article.date:
            localized_date = self.date_localizer.localize_date(
                translated_article.date, lang
            )
            translated_article.locale_date = localized_date
            logger.debug(f"Set localized date for {lang}: {localized_date}")

        # Set summary and excerpt attributes for template display
        if "summary" in new_metadata:
            translated_article.summary = new_metadata["summary"]
            logger.debug(f"Set summary attribute for {lang}: {new_metadata['summary']}")

        if "excerpt" in new_metadata:
            translated_article.excerpt = new_metadata["excerpt"]
            # Force summary to be set from excerpt to override any original summary
            translated_article.summary = new_metadata["excerpt"]
            logger.debug(
                f"Set summary from excerpt for {lang}: {new_metadata['excerpt']}"
            )

        # Add original article URL for template display
        translated_article.original_url = f"/{original_article.slug}/"
        logger.debug(
            f"Set original article URL for {lang}: {translated_article.original_url}"
        )

        # Add translation metadata fields as attributes for template display
        if "translation" in metadata:
            translated_article.translation = metadata["translation"]
            logger.debug(
                f"Set translation attribute for {lang}: {metadata['translation']}"
            )

        if "translator" in metadata:
            translated_article.translator = metadata["translator"]
            logger.debug(
                f"Set translator attribute for {lang}: {metadata['translator']}"
            )

        if "source_file" in metadata:
            translated_article.source_file = metadata["source_file"]
            logger.debug(
                f"Set source_file attribute for {lang}: {metadata['source_file']}"
            )

        logger.debug(
            f"Created translated article '{translated_article.title}' for language '{lang}' with URL {translated_article.metadata['url']}"
        )
        return translated_article

    def _create_translated_page(
        self, original_page: Page, translation_content: str, lang: str
    ) -> Page:
        """Create a translated page object"""
        # For now, create a copy of the original page with language-specific properties
        # This avoids the complex Page constructor issues
        translated_page = type(original_page)(
            original_page._content,
            metadata=original_page.metadata.copy(),
            source_path=original_page.source_path,
            context=original_page._context,
        )

        # Copy essential attributes from original (skip read-only properties)
        skipped_attrs = {"save_as", "url", "filename", "source_path", "_content"}
        for attr in dir(original_page):
            if (
                not attr.startswith("_")
                and hasattr(original_page, attr)
                and attr not in skipped_attrs
            ):
                try:
                    value = getattr(original_page, attr)
                    if not callable(value):  # Skip methods
                        setattr(translated_page, attr, value)
                except (AttributeError, TypeError):
                    pass  # Skip problematic attributes

        # Set language-specific attributes
        translated_page.lang = lang
        translated_page.original_page = original_page
        translated_page.multilingual_urls = original_page.multilingual_urls

        # Override metadata to include language-specific URLs
        translated_page.metadata = translated_page.metadata.copy()
        translated_page.metadata["lang"] = lang

        # Set language-specific save path and URL through metadata
        original_slug = getattr(translated_page, "slug", "unknown")
        translated_page.metadata["save_as"] = f"{lang}/{original_slug}/index.html"
        translated_page.metadata["url"] = f"/{lang}/{original_slug}/"

        return translated_page

    def _parse_translation_content(self, content: str) -> Tuple[Dict, str]:
        """Parse translation content into metadata and body"""
        lines = content.split("\n")
        metadata = {}
        body_start = 0

        # Check for frontmatter
        if lines and lines[0].strip() == "---":
            body_start = 1
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == "---":
                    body_start = i + 1
                    break

                # Parse metadata
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip()

        body = "\n".join(lines[body_start:])

        # Extract nested markdown content if present
        if body.strip().startswith("```markdown"):
            # Find the closing ```
            body_lines = body.split("\n")
            if body_lines[0].strip() == "```markdown":
                # Find the closing ```
                for i, line in enumerate(body_lines[1:], 1):
                    if line.strip() == "```":
                        # Extract content between markdown code blocks
                        nested_content = "\n".join(body_lines[1:i])
                        # Parse the nested content for its own metadata
                        nested_metadata, nested_body = self._parse_nested_markdown(
                            nested_content
                        )
                        # Merge metadata, with nested taking precedence
                        metadata.update(nested_metadata)
                        body = nested_body
                        break

        return metadata, body

    def _parse_nested_markdown(self, content: str) -> Tuple[Dict, str]:
        """Parse nested markdown content with its own frontmatter"""
        lines = content.split("\n")
        metadata = {}
        body_start = 0

        # Check for frontmatter in nested content
        if lines and lines[0].strip() == "---":
            body_start = 1
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == "---":
                    body_start = i + 1
                    break

                # Parse metadata
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip().strip("\"'")

        body = "\n".join(lines[body_start:])
        return metadata, body

    def _extract_clean_summary(self, content: str) -> str:
        """Extract a clean text summary from markdown content, excluding TOC and other markup"""
        import re

        # Remove TOC markers
        content = re.sub(r"\[TOC\]", "", content)

        # Split into lines and process
        lines = content.split("\n")
        summary_lines = []

        for line in lines:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Skip headers
            if line.startswith("#"):
                continue

            # Skip image references
            if line.startswith("<img") or line.startswith("!["):
                continue

            # Skip code blocks
            if line.startswith("```"):
                continue

            # Skip lists (we want paragraph text for summary)
            if (
                line.startswith("- ")
                or line.startswith("* ")
                or re.match(r"^\d+\.", line)
            ):
                continue

            # Skip links that are on their own line
            if line.startswith("http") or line.startswith("[") and line.endswith("]"):
                continue

            # Add the line if it looks like paragraph text
            if len(line) > 20:  # Only include substantial text
                summary_lines.append(line)

                # Stop after we have enough content for a summary
                if len(" ".join(summary_lines)) > 150:
                    break

        # Join the lines and clean up markdown formatting
        summary = " ".join(summary_lines)

        # Remove markdown formatting
        summary = re.sub(r"\*\*(.+?)\*\*", r"\1", summary)  # Bold
        summary = re.sub(r"_(.+?)_", r"\1", summary)  # Italic
        summary = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", summary)  # Links
        summary = re.sub(r"`(.+?)`", r"\1", summary)  # Code

        # Clean up extra whitespace
        summary = re.sub(r"\s+", " ", summary).strip()

        # Truncate if too long
        if len(summary) > 200:
            summary = summary[:200].rsplit(" ", 1)[0] + "..."

        logger.debug(f"Extracted clean summary: {summary}")
        return summary

    def _process_markdown_content(self, content: str) -> str:
        """Process markdown content to HTML using Pelican's markdown processor"""
        try:
            # Import markdown and create processor with same settings as Pelican
            from markdown import Markdown

            # Get markdown settings from Pelican configuration
            markdown_settings = self.settings.get("MARKDOWN", {})

            # Ensure we have the required extensions
            if "extensions" not in markdown_settings:
                markdown_settings["extensions"] = []

            # Add meta extension if not already present
            if "markdown.extensions.meta" not in markdown_settings["extensions"]:
                markdown_settings["extensions"].append("markdown.extensions.meta")

            # Create markdown processor with the same configuration as Pelican
            md = Markdown(**markdown_settings)

            # Convert markdown to HTML
            processed_content = md.convert(content)

            logger.debug(
                f"Markdown processing successful, converted {len(content)} chars to {len(processed_content)} chars"
            )
            return processed_content

        except Exception as e:
            logger.error(f"Failed to process markdown content: {e}")
            # Fall back to returning the original content if processing fails
            return content


class LanguageSwitcher:
    """Language switching UI component"""

    def __init__(self, supported_langs=None):
        if supported_langs is None:
            supported_langs = ["en", "de", "fr"]
        self.supported_langs = supported_langs
        self.lang_names = {
            "en": "English",
            "de": "Deutsch",
            "fr": "Français",
            "es": "Español",
            "it": "Italiano",
        }

    def generate_language_links(
        self, current_url: str, current_lang: str
    ) -> List[Dict]:
        """Generate language switching links"""
        links = []

        for lang in self.supported_langs:
            if lang == current_lang:
                continue

            # Generate equivalent URL in target language
            equivalent_url = self.get_equivalent_url(current_url, lang)

            links.append(
                {
                    "code": lang,
                    "name": self.lang_names.get(lang, lang.upper()),
                    "url": equivalent_url,
                }
            )

        return links

    def get_equivalent_url(self, url: str, target_lang: str) -> str:
        """Find equivalent URL in target language"""
        # Simple implementation - replace language code in URL
        # This could be enhanced with actual URL mapping

        # Remove leading/trailing slashes
        url = url.strip("/")

        # Split URL parts
        parts = url.split("/")

        # If URL starts with language code, replace it
        if parts and parts[0] in self.supported_langs:
            parts[0] = target_lang
        else:
            # Add language code at the beginning
            parts = [target_lang] + parts

        return "/" + "/".join(parts) + "/"


class MultilingualOutputGenerator:
    """Handles generation of multilingual content files"""

    def __init__(self, output_path, settings):
        self.output_path = output_path
        self.settings = settings

    def generate_language_article(
        self, writer, article: Article, context: Dict, template_getter
    ):
        """Generate individual article page for a specific language"""
        save_as = article.metadata.get("save_as")
        if not save_as:
            logger.warning(
                f"No save_as metadata for article '{article.title}', skipping"
            )
            return

        # Copy images for this language-specific article
        self._copy_images_for_translated_article(article)

        article_context = context.copy()
        article_context["article"] = article

        try:
            writer.write_file(
                save_as,
                template_getter("article"),
                article_context,
                override_output=self.output_path,
            )
            logger.debug(f"Generated article page: {save_as}")
        except Exception as e:
            logger.error(f"Failed to generate article '{article.title}': {e}")

    def generate_language_page(
        self, writer, page: Page, context: Dict, template_getter
    ):
        """Generate individual page for a specific language"""
        save_as = page.metadata.get("save_as")
        if not save_as:
            logger.warning(f"No save_as metadata for page '{page.title}', skipping")
            return

        page_context = context.copy()
        page_context["page"] = page

        try:
            writer.write_file(
                save_as,
                template_getter("page"),
                page_context,
                override_output=self.output_path,
            )
            logger.debug(f"Generated page: {save_as}")
        except Exception as e:
            logger.error(f"Failed to generate page '{page.title}': {e}")

    def generate_language_index(
        self, writer, lang: str, articles: List[Article], context: Dict, template_getter
    ):
        """Generate index page for a specific language with proper pagination"""
        from types import SimpleNamespace

        # Get pagination settings
        pagination_size = self.settings.get("DEFAULT_PAGINATION", 10)

        if not pagination_size or len(articles) <= pagination_size:
            # No pagination needed - generate single index page
            self._generate_single_language_index(
                writer, lang, articles, context, template_getter
            )
            return

        # Generate paginated index pages
        total_pages = (len(articles) + pagination_size - 1) // pagination_size

        for page_num in range(1, total_pages + 1):
            start_idx = (page_num - 1) * pagination_size
            end_idx = start_idx + pagination_size
            page_articles = articles[start_idx:end_idx]

            # Create pagination object
            articles_page = SimpleNamespace()
            articles_page.object_list = page_articles
            articles_page.has_previous = lambda p=page_num: p > 1
            articles_page.has_next = lambda p=page_num, t=total_pages: p < t
            articles_page.previous_page_number = page_num - 1 if page_num > 1 else None
            articles_page.next_page_number = (
                page_num + 1 if page_num < total_pages else None
            )
            articles_page.number = page_num

            # Create previous/next page objects for template
            if page_num > 1:
                articles_previous_page = SimpleNamespace()
                articles_previous_page.url = (
                    f"{lang}/index.html"
                    if page_num == 2
                    else f"{lang}/index{page_num-1}.html"
                )
            else:
                articles_previous_page = None

            if page_num < total_pages:
                articles_next_page = SimpleNamespace()
                articles_next_page.url = f"{lang}/index{page_num+1}.html"
            else:
                articles_next_page = None

            # Determine save path
            if page_num == 1:
                index_save_as = f"{lang}/index.html"
            else:
                index_save_as = f"{lang}/index{page_num}.html"

            # Prepare context
            index_context = context.copy()
            index_context["articles"] = page_articles
            index_context["articles_page"] = articles_page
            index_context["articles_previous_page"] = articles_previous_page
            index_context["articles_next_page"] = articles_next_page

            writer.write_file(
                index_save_as,
                template_getter("index"),
                index_context,
                override_output=self.output_path,
            )

    def _generate_single_language_index(
        self, writer, lang: str, articles: List[Article], context: Dict, template_getter
    ):
        """Generate single index page without pagination"""
        from types import SimpleNamespace

        index_save_as = f"{lang}/index.html"

        # Create a mock pagination object that the template expects
        articles_page = SimpleNamespace()
        articles_page.object_list = articles
        articles_page.has_previous = lambda: False
        articles_page.has_next = lambda: False
        articles_page.previous_page_number = None
        articles_page.next_page_number = None
        articles_page.number = 1

        index_context = context.copy()
        index_context["articles"] = articles
        index_context["articles_page"] = articles_page
        index_context["articles_previous_page"] = None
        index_context["articles_next_page"] = None

        writer.write_file(
            index_save_as,
            template_getter("index"),
            index_context,
            override_output=self.output_path,
        )

    def generate_root_page_with_default_language(
        self, writer, context: Dict, articles: List[Article], template_getter
    ):
        """Generate root index page with auto-redirect functionality"""
        root_context = context.copy()

        writer.write_file(
            "index.html",
            template_getter("auto_redirect"),
            root_context,
            override_output=self.output_path,
        )

    def _copy_images_for_translated_article(self, article: Article):
        """Copy images from the original article source to the translated article directory"""
        try:
            import shutil

            # Get the original source path and the target output directory
            source_path = getattr(article, "source_path", "")
            save_as = article.metadata.get("save_as", "")

            if not source_path or not save_as:
                return

            # Get source directory (where the original article and images are)
            source_dir = os.path.dirname(source_path)

            # Get target directory (where the translated article should be)
            output_dir = os.path.join(self.output_path, os.path.dirname(save_as))

            # Ensure the target directory exists
            os.makedirs(output_dir, exist_ok=True)

            # Copy all image files from source to target
            copied_images = []
            if os.path.exists(source_dir):
                for filename in os.listdir(source_dir):
                    if filename.lower().endswith(
                        (".jpg", ".jpeg", ".png", ".gif", ".svg", ".pdf")
                    ):
                        src_file = os.path.join(source_dir, filename)
                        dst_file = os.path.join(output_dir, filename)

                        # Only copy if the file doesn't already exist or if source is newer
                        if not os.path.exists(dst_file) or os.path.getmtime(
                            src_file
                        ) > os.path.getmtime(dst_file):
                            shutil.copy2(src_file, dst_file)
                            copied_images.append(filename)
                            logger.debug(f"Copied image {filename} to {output_dir}")

            # Copy all files from attachments/ subdirectory
            attachments_dir = os.path.join(source_dir, "attachments")
            if os.path.isdir(attachments_dir):
                for filename in os.listdir(attachments_dir):
                    src_file = os.path.join(attachments_dir, filename)
                    if os.path.isfile(src_file):
                        dst_file = os.path.join(output_dir, filename)
                        if not os.path.exists(dst_file) or os.path.getmtime(
                            src_file
                        ) > os.path.getmtime(dst_file):
                            shutil.copy2(src_file, dst_file)
                            copied_images.append(filename)

            if copied_images:
                logger.debug(
                    f"Copied {len(copied_images)} images for translated article {article.title}"
                )

        except Exception as e:
            logger.warning(
                f"Failed to copy images for translated article {article.title}: {e}"
            )


class MultilingualContextManager:
    """Manages multilingual context and language-specific data"""

    def __init__(self, content_processor, language_switcher):
        self.content_processor = content_processor
        self.language_switcher = language_switcher

    def generate_context(self, context: Dict):
        """Generate context for multilingual site"""
        # Add language switcher to context
        context["language_switcher"] = self.language_switcher
        context["multilingual_languages"] = self.content_processor.supported_langs
        context["default_language"] = self.content_processor.default_lang
        context["MULTILINGUAL_ENABLED"] = True

    def create_language_context(
        self, base_context: Dict, lang: str, articles: List[Article], pages: List[Page]
    ) -> Dict:
        """Create language-specific context"""
        lang_context = base_context.copy()
        lang_context["articles"] = articles
        lang_context["pages"] = pages
        lang_context["LANG"] = lang
        lang_context["current_language"] = lang
        return lang_context


class MultilingualSiteGenerator(Generator):
    """Generator for multilingual site functionality"""

    def __init__(self, context, settings, path, theme, output_path):
        super().__init__(context, settings, path, theme, output_path)

        # Check if multilingual is enabled
        multilingual_enabled = settings.get("MULTILINGUAL_ENABLED", False)
        logger.info(
            f"Multilingual initialization: MULTILINGUAL_ENABLED = {multilingual_enabled}"
        )
        if not multilingual_enabled:
            logger.info("Multilingual site is disabled")
            return

        self.content_processor = MultilingualContentProcessor(settings)
        self.language_switcher = LanguageSwitcher(
            settings.get("MULTILINGUAL_LANGUAGES", ["en", "de", "fr"])
        )
        self.output_generator = MultilingualOutputGenerator(output_path, settings)
        self.context_manager = MultilingualContextManager(
            self.content_processor, self.language_switcher
        )

        logger.info(
            f"Multilingual site generator initialized for languages: {self.content_processor.supported_langs}"
        )

    def generate_context(self):
        """Generate context for multilingual site"""
        if not self.settings.get("MULTILINGUAL_ENABLED", False):
            return

        self.context_manager.generate_context(self.context)

    def generate_output(self, writer):
        """Generate multilingual site output"""
        if not self.settings.get("MULTILINGUAL_ENABLED", False):
            return

        logger.info("Starting multilingual site generation")

        # Process articles and pages
        articles = self.context.get("articles", [])
        pages = self.context.get("pages", [])

        logger.info(
            f"Starting to process {len(articles)} articles for multilingual generation"
        )
        processed_articles = self.content_processor.process_articles(articles)
        processed_pages = self.content_processor.process_pages(pages)

        # Log results
        for lang, lang_articles in processed_articles.items():
            logger.info(f"Language '{lang}': {len(lang_articles)} articles")

        # Generate language-specific versions
        for lang in self.content_processor.supported_langs:
            self._generate_language_version(
                writer, lang, processed_articles[lang], processed_pages[lang]
            )

        # Generate root page with English content (default language)
        self.output_generator.generate_root_page_with_default_language(
            writer, self.context, processed_articles["en"], self.get_template
        )

        logger.info("Multilingual site generation completed")

    def _generate_language_version(
        self, writer, lang: str, articles: List[Article], pages: List[Page]
    ):
        """Generate content for a specific language"""
        logger.info(f"Generating content for language: {lang}")

        # Create language-specific context
        lang_context = self.context_manager.create_language_context(
            self.context, lang, articles, pages
        )

        # Generate individual articles for this language
        logger.info(
            f"Generating {len(articles)} individual articles for language '{lang}'"
        )
        for article in articles:
            self.output_generator.generate_language_article(
                writer, article, lang_context, self.get_template
            )

        # Generate individual pages for this language
        logger.info(f"Generating {len(pages)} individual pages for language '{lang}'")
        for page in pages:
            self.output_generator.generate_language_page(
                writer, page, lang_context, self.get_template
            )

        # Generate language-specific index
        self.output_generator.generate_language_index(
            writer, lang, articles, lang_context, self.get_template
        )


def get_generators(pelican_object):
    """Register the multilingual site generator"""
    if pelican_object.settings.get("MULTILINGUAL_ENABLED", False):
        return MultilingualSiteGenerator
    return None


def enhance_content_with_multilingual_data(content_generator):
    """Enhance content objects with multilingual data"""
    settings = content_generator.settings

    if not settings.get("MULTILINGUAL_ENABLED", False):
        return

    supported_langs = settings.get("MULTILINGUAL_LANGUAGES", ["en", "de", "fr"])
    default_lang = settings.get("MULTILINGUAL_DEFAULT_LANG", "en")
    date_localizer = DateLocalizer()

    logger.info(
        f"Enhancing content with multilingual data for languages: {supported_langs}"
    )

    # Simple language switcher that generates basic links
    def generate_simple_language_links(content_url, current_lang):
        links = []
        for lang in supported_langs:
            if lang != current_lang:
                # Simple URL replacement - this is a basic implementation
                if content_url.startswith("/"):
                    lang_url = f"/{lang}{content_url}"
                else:
                    lang_url = f"/{lang}/{content_url}"
                links.append(
                    {
                        "code": lang,
                        "name": {
                            "en": "English",
                            "de": "Deutsch",
                            "fr": "Français",
                            "es": "Español",
                            "it": "Italiano",
                        }.get(lang, lang.upper()),
                        "url": lang_url,
                    }
                )
        return links

    # Process articles
    if hasattr(content_generator, "articles"):
        for article in content_generator.articles:
            try:
                article.multilingual_urls = {}
                article.language_links = generate_simple_language_links(
                    getattr(article, "url", ""), default_lang
                )
                # Add localized date if not already set
                if (
                    hasattr(article, "date")
                    and article.date
                    and not hasattr(article, "locale_date")
                ):
                    article.locale_date = date_localizer.localize_date(
                        article.date, default_lang
                    )
                logger.debug(f"Enhanced article: {article.title}")
            except Exception as e:
                logger.warning(
                    f"Failed to enhance article {getattr(article, 'title', 'unknown')} with multilingual data: {e}"
                )
                article.multilingual_urls = {}
                article.language_links = []

    # Process pages
    if hasattr(content_generator, "pages"):
        for page in content_generator.pages:
            try:
                page.multilingual_urls = {}
                page.language_links = generate_simple_language_links(
                    getattr(page, "url", ""), default_lang
                )
                logger.debug(f"Enhanced page: {page.title}")
            except Exception as e:
                logger.warning(
                    f"Failed to enhance page {getattr(page, 'title', 'unknown')} with multilingual data: {e}"
                )
                page.multilingual_urls = {}
                page.language_links = []


def register():
    """Register plugin with Pelican"""
    signals.get_generators.connect(get_generators)
    signals.article_generator_finalized.connect(enhance_content_with_multilingual_data)
    signals.page_generator_finalized.connect(enhance_content_with_multilingual_data)

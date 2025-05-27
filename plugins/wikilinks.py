"""
Custom WikiLinks plugin for Pelican that uses the normalize_slug function
to ensure consistent URL generation for [[page]] links.
"""

import re

import markdown
from markdown.preprocessors import Preprocessor
from pelican import signals

# Import the central normalize_slug function
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from normalize_slugs import normalize_slug


class WikiLinksPreprocessor(Preprocessor):
    """Markdown preprocessor to handle [[WikiLinks]] before markdown processing."""

    def run(self, lines):
        """Process wikilinks in the markdown text."""
        text = "\n".join(lines)

        def replace_wikilink(match):
            link_text = match.group(1)
            if not link_text:
                return match.group(0)

            # Handle [[Page|Display Text]] syntax
            if "|" in link_text:
                page_name, display_text = link_text.split("|", 1)
                page_name = page_name.strip()
                display_text = display_text.strip()
            else:
                page_name = link_text.strip()
                display_text = page_name

            # Convert page name to slug: replace spaces with hyphens, then normalize
            if not page_name.strip():
                return match.group(0)  # Return original if empty

            slug = page_name.lower().replace(" ", "-")
            slug = normalize_slug(slug)

            # Create the link markdown
            return f"[{display_text}](/{slug}/)"

        # Find and replace all [[...]] patterns
        wikilink_pattern = r"\[\[([^\]]+)\]\]"
        text = re.sub(wikilink_pattern, replace_wikilink, text)

        return text.split("\n")


def add_wikilinks_preprocessor(pelican):
    """Add the wikilinks preprocessor to markdown."""
    if hasattr(pelican.settings, "MARKDOWN"):
        md_config = pelican.settings["MARKDOWN"]

        # Create a custom markdown instance to get the preprocessor
        md = markdown.Markdown()
        md.preprocessors.register(WikiLinksPreprocessor(md), "wikilinks", 25)

        # Add our preprocessor to the markdown configuration
        if "extension_configs" not in md_config:
            md_config["extension_configs"] = {}

        # Store the markdown instance so Pelican can use it
        pelican.settings["MARKDOWN"]["preprocessors"] = [WikiLinksPreprocessor]


def process_wikilinks(content):
    """
    Process [[WikiLink]] syntax and convert to proper URLs using normalize_slug.
    """
    print(f"DEBUG: Processing content object: {type(content)}")
    print(f"DEBUG: Has source: {hasattr(content, 'source')}")
    print(f"DEBUG: Has _content: {hasattr(content, '_content')}")

    # Check both _content and source attributes
    source_content = None
    if hasattr(content, "source") and content.source:
        source_content = content.source
        print(f"DEBUG: Using source content, has [[: {'[[' in source_content}")
    elif hasattr(content, "_content") and content._content:
        source_content = content._content
        print(f"DEBUG: Using _content, has [[: {'[[' in source_content}")
    else:
        print("DEBUG: No content found")
        return

    if not source_content:
        print("DEBUG: Source content is empty")
        return

    def replace_wikilink(match):
        link_text = match.group(1)
        if not link_text:
            return match.group(0)

        # Handle [[Page|Display Text]] syntax
        if "|" in link_text:
            page_name, display_text = link_text.split("|", 1)
            page_name = page_name.strip()
            display_text = display_text.strip()
        else:
            page_name = link_text.strip()
            display_text = page_name

        # Convert page name to slug: first replace spaces with hyphens, then normalize
        if not page_name.strip():
            return match.group(0)  # Return original if empty

        slug = page_name.lower().replace(" ", "-")
        slug = normalize_slug(slug)

        # Create the link HTML
        return f'<a href="/{slug}/" class="wikilink">{display_text}</a>'

    # Find and replace all [[...]] patterns
    wikilink_pattern = r"\[\[([^\]]+)\]\]"
    try:
        processed_content = re.sub(wikilink_pattern, replace_wikilink, source_content)

        # Update the appropriate attribute
        if hasattr(content, "source") and content.source:
            content.source = processed_content
        elif hasattr(content, "_content") and content._content:
            content._content = processed_content
    except TypeError:
        # Skip if content is None or not a string
        pass


def process_content_wikilinks(content_generator):
    """Process wikilinks for all articles and pages."""
    # Process articles
    if hasattr(content_generator, "articles"):
        for article in content_generator.articles:
            process_wikilinks(article)

    if hasattr(content_generator, "hidden_articles"):
        for article in content_generator.hidden_articles:
            process_wikilinks(article)

    # Process pages
    if hasattr(content_generator, "pages"):
        for page in content_generator.pages:
            process_wikilinks(page)

    if hasattr(content_generator, "hidden_pages"):
        for page in content_generator.hidden_pages:
            process_wikilinks(page)


def register():
    """Register the plugin."""
    signals.initialized.connect(add_wikilinks_preprocessor)

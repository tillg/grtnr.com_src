"""
Custom markdown extension for WikiLinks that uses proper slug normalization.
"""

import os
import re
import sys

from markdown import Extension
from markdown.preprocessors import Preprocessor


class CustomWikiLinksPreprocessor(Preprocessor):
    """Preprocessor to handle [[WikiLinks]] with custom slug normalization."""

    def run(self, lines):
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

            if not page_name.strip():
                return match.group(0)

            # Convert to slug with hyphens
            slug = page_name.lower().replace(" ", "-")
            # Import normalize_slug locally to avoid E402
            sys.path.insert(0, os.path.dirname(__file__))
            from normalize_slugs import normalize_slug

            slug = normalize_slug(slug)

            # Return markdown link format
            return f"[{display_text}](/{slug}/)"

        wikilink_pattern = r"\[\[([^\]]+)\]\]"
        text = re.sub(wikilink_pattern, replace_wikilink, text)

        return text.split("\n")


class CustomWikiLinksExtension(Extension):
    """Markdown extension for custom WikiLinks."""

    def extendMarkdown(self, md):
        md.preprocessors.register(
            CustomWikiLinksPreprocessor(md),
            "custom_wikilinks",
            175,  # High priority to run before other preprocessors
        )


def makeExtension(**kwargs):
    return CustomWikiLinksExtension(**kwargs)

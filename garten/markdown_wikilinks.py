"""Custom markdown extension for WikiLinks with slug normalization.

Ported from plugins/markdown_wikilinks.py to use garten.utils.normalize_slug
instead of the Pelican plugin's version.

Registered as a Python-Markdown preprocessor at priority 175 (high priority,
runs before other preprocessors).
"""

import re

from markdown import Extension
from markdown.preprocessors import Preprocessor

from .utils import normalize_slug


class WikiLinksPreprocessor(Preprocessor):
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

            # Convert to slug with hyphens, then normalize
            slug = page_name.lower().replace(" ", "-")
            slug = normalize_slug(slug)

            return f"[{display_text}](/{slug}/)"

        text = re.sub(r"\[\[([^\]]+)\]\]", replace_wikilink, text)
        return text.split("\n")


class WikiLinksExtension(Extension):
    """Markdown extension for custom WikiLinks."""

    def extendMarkdown(self, md):
        md.preprocessors.register(
            WikiLinksPreprocessor(md),
            "custom_wikilinks",
            175,
        )


def makeExtension(**kwargs):
    return WikiLinksExtension(**kwargs)

"""
Link validation plugin for Pelican.

Validates internal links after content generation to catch broken links.
"""

import logging
import re
from pathlib import Path
from urllib.parse import urlparse

from pelican import signals

logger = logging.getLogger(__name__)


class LinkValidator:
    """Validates internal links in generated content."""

    def __init__(self, pelican_obj):
        self.pelican = pelican_obj
        self.settings = pelican_obj.settings
        self.output_path = Path(pelican_obj.output_path)
        self.errors = []
        self.internal_links = {}
        self.valid_paths = set()

    def collect_valid_paths(self):
        """Collect all valid paths from generated HTML files."""
        if not self.output_path.exists():
            return

        # Find all generated HTML files
        for html_file in self.output_path.rglob("*.html"):
            # Get relative path from output directory
            rel_path = html_file.relative_to(self.output_path)

            # Convert to URL format
            if rel_path.name == "index.html":
                # For index.html files, use the directory path
                url_path = str(rel_path.parent) + "/"
            else:
                url_path = str(rel_path)

            # Normalize path
            if url_path.startswith("./"):
                url_path = url_path[2:]
            if url_path == ".":
                url_path = ""

            self.valid_paths.add(url_path)

            # Also add without trailing slash for directories
            if url_path.endswith("/") and url_path != "":
                self.valid_paths.add(url_path.rstrip("/"))

        logger.debug(f"Collected {len(self.valid_paths)} valid paths")

    def extract_internal_links(self, content):
        """Extract internal links from HTML content."""
        # Match href attributes with internal links
        href_pattern = r'href=["\']([^"\']*)["\']'
        links = re.findall(href_pattern, content)

        internal_links = []
        for link in links:
            parsed = urlparse(link)

            # Skip external links, anchors, and javascript
            if parsed.netloc or link.startswith(
                ("http:", "https:", "mailto:", "#", "javascript:")
            ):
                continue

            # Skip theme assets and static files
            if (
                link.startswith("./theme/")
                or link.startswith("../theme/")
                or link.startswith("/theme/")
                or link.endswith(".css")
                or link.endswith(".js")
                or link.endswith(".ico")
                or link.endswith(".png")
                or link.endswith(".jpg")
                or link.endswith(".svg")
            ):
                continue

            # Only check content links (HTML pages)
            if (
                link.startswith("/")
                or link.endswith("/")
                or link.endswith(".html")
                or "." not in link.split("/")[-1]
            ):  # Probably a page without extension
                internal_links.append(link)

        return internal_links

    def normalize_link(self, link, current_path=""):
        """Normalize link for comparison, resolving relative paths."""
        # Remove anchors
        if "#" in link:
            link = link.split("#")[0]

        # Remove query parameters
        if "?" in link:
            link = link.split("?")[0]

        # Handle absolute paths
        if link.startswith("/"):
            return link[1:]

        # Handle relative paths
        if link.startswith("./"):
            link = link[2:]  # Remove './'

        # Resolve relative paths from current directory
        if current_path:
            current_dir = str(Path(current_path).parent)
            if current_dir == ".":
                current_dir = ""

            # Handle parent directory references
            while link.startswith("../"):
                link = link[3:]  # Remove '../'
                if current_dir:
                    current_dir = str(Path(current_dir).parent)
                    if current_dir == ".":
                        current_dir = ""

            # Combine current directory with relative link
            if current_dir:
                normalized = str(Path(current_dir) / link)
            else:
                normalized = link
        else:
            normalized = link

        # Handle empty case (refers to root)
        if not normalized or normalized == ".":
            return ""

        return normalized

    def validate_html_file(self, html_file):
        """Validate links in a single HTML file."""
        try:
            content = html_file.read_text(encoding="utf-8")
            links = self.extract_internal_links(content)

            rel_path = html_file.relative_to(self.output_path)
            source_file = str(rel_path)

            for link in links:
                normalized_link = self.normalize_link(link, source_file)

                # Skip empty links and anchors
                if not normalized_link or link.startswith("#"):
                    continue

                # Track all internal links for verbose output
                if source_file not in self.internal_links:
                    self.internal_links[source_file] = []
                self.internal_links[source_file].append(link)

                # Check if link exists in valid paths
                if (
                    normalized_link not in self.valid_paths
                    and normalized_link + "/" not in self.valid_paths
                    and normalized_link.rstrip("/") not in self.valid_paths
                ):

                    error_msg = (
                        f"Broken internal link in {source_file}: "
                        f"'{link}' -> '{normalized_link}'"
                    )
                    self.errors.append(error_msg)
                    logger.warning(error_msg)

        except Exception as e:
            logger.warning(f"Error processing {html_file}: {e}")

    def validate_all_links(self):
        """Validate all internal links in generated content."""
        # First collect all valid paths
        self.collect_valid_paths()

        # Then validate links in all HTML files
        for html_file in self.output_path.rglob("*.html"):
            self.validate_html_file(html_file)

    def report_results(self):
        """Report validation results."""
        # Show verbose output if requested
        if self.settings.get("VALIDATE_LINKS_VERBOSE", False):
            logger.info("Internal links found:")
            for source_file, links in self.internal_links.items():
                if links:
                    logger.info(f"  {source_file}:")
                    for link in links:
                        logger.info(f"    {link}")

        if self.errors:
            logger.error(f"Found {len(self.errors)} broken internal links:")
            for error in self.errors:
                logger.error(f"  {error}")

            # Fail build if setting is enabled
            if self.settings.get("VALIDATE_LINKS_FAIL_ON_ERROR", True):
                raise Exception(
                    f"Build failed due to {len(self.errors)} broken internal links"
                )
        else:
            total_links = sum(len(links) for links in self.internal_links.values())
            logger.info(f"All {total_links} internal links validated successfully")


def validate_links_after_generation(pelican_obj):
    """Signal handler called after content generation."""
    validator = LinkValidator(pelican_obj)
    validator.validate_all_links()
    validator.report_results()


def register():
    """Register the plugin with Pelican."""
    signals.finalized.connect(validate_links_after_generation)

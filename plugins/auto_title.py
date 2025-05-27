import os
import sys

from pelican import signals
from pelican.readers import MarkdownReader

# Import centralized logging
sys.path.insert(0, os.path.dirname(__file__))
from logger_config import get_logger

# Setup logger for this plugin
logger = get_logger('auto_title')


class AutoTitleReader(MarkdownReader):
    def read(self, source_path):
        """Read content and derive title from directory name if not present."""
        content, metadata = super().read(source_path)

        # Only process if no title is present
        if "title" not in metadata:
            # Get directory name
            dir_name = os.path.basename(os.path.dirname(source_path))

            # Try to remove a date prefix if it exists
            # (e.g., 2025-04-18-digital-garden)
            parts = dir_name.split("-")
            if len(parts) >= 4 and all(p.isdigit() for p in parts[:3]):
                logger.debug(f"Detected date prefix in {dir_name}, removing it.")
                title_parts = parts[3:]
            else:
                title_parts = parts

            # Convert to title case
            title = " ".join(title_parts).replace("_", " ").title()
            metadata["title"] = title
            logger.debug(f"Generated title '{title}' from directory '{dir_name}'")

        # Remove surrounding quotes
        title = metadata["title"]
        if title.startswith('"') and title.endswith('"'):
            title = title[1:-1]
            metadata["title"] = title

        return content, metadata


def add_reader(readers):
    readers.reader_classes["md"] = AutoTitleReader


def register():
    signals.readers_init.connect(add_reader)

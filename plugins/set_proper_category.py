# plugins/fix_categories.py
import os
import sys

from pelican import signals

# Import centralized logging
sys.path.insert(0, os.path.dirname(__file__))
from logger_config import get_logger

# Setup logger for this plugin
logger = get_logger("set_proper_category")


def set_proper_category(generator):
    """Set the category of articles based on their directory structure.

    We can't use the Pelican standard way switched on by
    USE_FOLDER_AS_CATEGORY because of our nested directory structure.
    """

    for article in generator.articles:
        # Get the relative path from content directory
        rel_path = os.path.relpath(article.source_path, generator.path)
        # Split path to get components
        path_parts = rel_path.split(os.sep)

        # The first directory is the main category
        if len(path_parts) > 1:
            main_category = path_parts[0]
            # Set the category
            article.category.name = main_category

    logger.info(f"Fixed categories for {len(generator.articles)} articles")


def register():
    signals.article_generator_finalized.connect(set_proper_category)

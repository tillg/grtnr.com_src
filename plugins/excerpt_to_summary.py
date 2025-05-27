import os
import sys

from pelican import signals

# Import centralized logging
sys.path.insert(0, os.path.dirname(__file__))
from logger_config import get_logger

# Setup logger for this plugin
logger = get_logger('excerpt_to_summary')


def convert_excerpt_to_summary(generator):
    logger.info("Plugin excerpt_to_summary loaded!")
    for article in generator.articles:
        if hasattr(article, "excerpt"):
            # Remove quotes if present
            excerpt = article.excerpt
            if excerpt.startswith('"') and excerpt.endswith('"'):
                excerpt = excerpt[1:-1]

            logger.debug(f"Converting excerpt to summary for article: {article.title}")
            article.metadata["summary"] = excerpt
            article.summary = excerpt


def register():
    signals.article_generator_pretaxonomy.connect(convert_excerpt_to_summary)


# Register the plugin on import
register()

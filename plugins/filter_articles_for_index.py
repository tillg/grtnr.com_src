# plugins/filter_index_articles.py
from pelican import signals


def filter_articles_for_index(generators):
    """Filter articles for the index page before pagination."""
    # Find the ArticlesGenerator
    article_generator = None
    for generator in generators:
        if generator.__class__.__name__ == 'ArticlesGenerator':
            article_generator = generator
            break
    
    if not article_generator:
        return
    
    # Get the categories to include from settings
    categories_in_index = article_generator.settings.get("CATEGORIES_IN_INDEX", [])

    # If no categories specified, keep all articles (don't filter)
    if not categories_in_index:
        return

    # Filter the articles
    filtered_articles = [
        article
        for article in article_generator.articles
        if article.category and article.category.name in categories_in_index
    ]

    # Replace the articles list with the filtered list
    # This must happen before pagination
    article_generator.articles = filtered_articles


def register():
    # Connect to all_generators_finalized to filter after articles are loaded but before pagination
    signals.all_generators_finalized.connect(filter_articles_for_index)
    # signals.article_generator_context.connect(filter_articles_for_index)
    # signals.article_generator_init.connect(filter_articles_for_index)
    # signals.article_generator_finalized.connect(filter_articles_for_index)

# plugins/filter_index_articles.py
from pelican import signals


def filter_articles_for_index(generator):
    """Filter articles for the index page before pagination."""
    # Get the categories to include from settings
    categories_in_index = generator.settings.get('CATEGORIES_IN_INDEX', [])
    # print(
    #     f"filter_articles_for_index: Categories in index: {categories_in_index}")

    # If no categories specified, keep all articles (don't filter)
    if not categories_in_index:
        return

    # Filter the articles
    filtered_articles = [
        article for article in generator.articles
        if article.category and article.category.name in categories_in_index
    ]

    # Replace the articles list with the filtered list
    # This must happen before pagination
    generator.articles = filtered_articles

    # print(
    #     f"filter_articles_for_index: {len(filtered_articles)} articles kept")


def register():
    # Connect to generator_init to filter before pagination
    # signals.article_generator_init.connect(filter_articles_for_index)
    signals.article_generator_finalized.connect(filter_articles_for_index)
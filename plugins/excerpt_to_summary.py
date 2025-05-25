from pelican import signals


def convert_excerpt_to_summary(generator):
    print("convert_excerpt_to_summary: Plugin excerpt_to_summary loaded!")
    for article in generator.articles:
        if hasattr(article, 'excerpt'):
            # Remove quotes if present
            excerpt = article.excerpt
            if excerpt.startswith('"') and excerpt.endswith('"'):
                excerpt = excerpt[1:-1]

            # print(f"convert_excerpt_to_summary: Converting excerpt to
            # summary for article: {article.title}")
            article.metadata['summary'] = excerpt
            article.summary = excerpt


def register():
    signals.article_generator_pretaxonomy.connect(convert_excerpt_to_summary)


# Register the plugin on import
register()

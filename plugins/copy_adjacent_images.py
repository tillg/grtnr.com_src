import os
import shutil
import re
from pelican import signals


def copy_adjacent_images(generator):
    # Process regular articles
    process_articles(generator, generator.articles)

    # Also process hidden articles
    if hasattr(generator, 'hidden_articles'):
        process_articles(generator, generator.hidden_articles)


def process_articles(generator, article_list):
    for article in article_list:
        source_path = article.source_path
        slug = article.slug
        # print(f"copy_adjacent_images: Copying images of article: {slug}")
        output_path = os.path.join(generator.output_path, slug)

        # Ensure the target output directory exists
        os.makedirs(output_path, exist_ok=True)

        # Copy all image files from the article's source directory to the output directory
        source_dir = os.path.dirname(source_path)
        copied_images = []
        for fname in os.listdir(source_dir):
            if fname.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg')):
                src = os.path.join(source_dir, fname)
                dst = os.path.join(output_path, fname)
                shutil.copy2(src, dst)
                copied_images.append(fname)

        # Fix image URLs in the content if the article is hidden
        if hasattr(generator, 'hidden_articles') and article in generator.hidden_articles:
            fix_image_urls(article, slug, copied_images)


def fix_image_urls(article, slug, image_names):
    # Find image references and fix them
    for img_name in image_names:
        # Look for HTML img tags with relative paths
        article._content = re.sub(
            r'<img([^>]*) src=["\'](?!https?://|/)([^"\']*' +
            re.escape(img_name) + ')["\']',
            r'<img\1 src="/' + slug + r'/\2"',
            article._content
        )

        # Look for Markdown image syntax
        article._content = re.sub(
            r'!\[(.*?)\]\((?!https?://|/)([^)]*' +
            re.escape(img_name) + r')\)',
            r'![\1](/' + slug + r'/\2)',
            article._content
        )


def register():
    signals.article_generator_finalized.connect(copy_adjacent_images)

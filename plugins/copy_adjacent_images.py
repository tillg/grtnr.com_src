import os
import shutil
import re
from pelican import signals


def copy_images_for_articles(generator):
    """Handle only articles in this handler"""
    # Process regular articles
    process_content_items(generator, generator.articles)

    # Process hidden articles
    if hasattr(generator, 'hidden_articles'):
        process_content_items(generator, generator.hidden_articles)
        
    # Process recipes if available
    if hasattr(generator, 'recipes'):
        process_content_items(generator, generator.recipes)


def copy_images_for_pages(generator):
    """Handle only pages in this handler"""
    # Process pages
    if hasattr(generator, 'pages'):
        process_content_items(generator, generator.pages)

    # Process hidden pages
    if hasattr(generator, 'hidden_pages'):
        process_content_items(generator, generator.hidden_pages)


def process_content_items(generator, item_list):
    for item in item_list:
        source_path = item.source_path
        slug = item.slug
        output_path = os.path.join(generator.output_path, slug)

        # Ensure the target output directory exists
        os.makedirs(output_path, exist_ok=True)

        # Copy all image files from the source directory to the output directory
        source_dir = os.path.dirname(source_path)
        copied_images = []
        for fname in os.listdir(source_dir):
            if fname.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg')):
                src = os.path.join(source_dir, fname)
                dst = os.path.join(output_path, fname)
                shutil.copy2(src, dst)
                copied_images.append(fname)

        # Fix image URLs for all content items (not just hidden ones)
        fix_image_urls(item, slug, copied_images)


def fix_image_urls(item, slug, image_names):
    # Find image references and fix them
    for img_name in image_names:
        # Look for HTML img tags with relative paths
        item._content = re.sub(
            r'<img([^>]*) src=["\'](?!https?://|/)([^"\']*' +
            re.escape(img_name) + ')["\']',
            r'<img\1 src="/' + slug + r'/\2"',
            item._content
        )

        # Look for Markdown image syntax
        item._content = re.sub(
            r'!\[(.*?)\]\((?!https?://|/)([^)]*' +
            re.escape(img_name) + r')\)',
            r'![\1](/' + slug + r'/\2)',
            item._content
        )


def register():
    # Connect different handlers for articles and pages
    signals.article_generator_finalized.connect(copy_images_for_articles)
    signals.page_generator_finalized.connect(copy_images_for_pages)
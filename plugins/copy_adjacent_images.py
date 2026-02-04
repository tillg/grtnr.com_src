import os
import re
import shutil

from pelican import signals


def copy_images_for_articles(generator):
    """Handle only articles in this handler"""
    # Process regular articles
    process_content_items(generator, generator.articles)

    # Process hidden articles
    if hasattr(generator, "hidden_articles"):
        process_content_items(generator, generator.hidden_articles)


def copy_images_for_pages(generator):
    """Handle only pages in this handler"""
    # Process pages
    if hasattr(generator, "pages"):
        process_content_items(generator, generator.pages)

    # Process hidden pages
    if hasattr(generator, "hidden_pages"):
        process_content_items(generator, generator.hidden_pages)


def copy_images_for_recipes(generator, writer):
    """Handle recipes after they are processed"""
    # Process recipes if available
    if hasattr(generator, "context") and "recipes" in generator.context:
        process_content_items(generator, generator.context["recipes"])
        
        # Also copy images for localized recipe pages
        copy_images_for_localized_recipes(generator, generator.context["recipes"])


def copy_images_for_localized_recipes(generator, recipes):
    """Copy images for programmatically generated localized recipe pages."""
    # Check if multilingual is enabled
    multilingual_enabled = generator.settings.get("MULTILINGUAL_ENABLED", False)
    if not multilingual_enabled:
        return
    
    languages = generator.settings.get("MULTILINGUAL_LANGUAGES", ["en"])
    default_lang = generator.settings.get("MULTILINGUAL_DEFAULT_LANG", "en")
    
    for lang in languages:
        if lang != default_lang:  # Skip default language as it's already processed
            for recipe in recipes:
                copy_images_for_localized_recipe(generator, recipe, lang)


def copy_images_for_localized_recipe(generator, recipe, language):
    """Copy images for a single localized recipe."""
    # Get source directory from original recipe
    source_dir = os.path.dirname(recipe.source_path)
    
    # Create target directory for localized recipe (e.g., output/de/recipes/hummus-from-mr-jim/)
    localized_save_as = f"{language}/{recipe.save_as}"
    output_path = os.path.join(generator.output_path, os.path.dirname(localized_save_as))
    
    # Ensure the target directory exists
    os.makedirs(output_path, exist_ok=True)
    
    # Copy all image files from source to localized output directory
    try:
        for fname in os.listdir(source_dir):
            if fname.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".svg", ".pdf")):
                src = os.path.join(source_dir, fname)
                dst = os.path.join(output_path, fname)
                shutil.copy2(src, dst)
    except OSError:
        # Handle cases where source directory doesn't exist or isn't readable
        pass


def process_content_items(generator, item_list):
    """Orchestrates image copying and URL fixing for content items."""
    for item in item_list:
        copied_images = copy_adjacent_images(generator, item)
        update_image_urls_in_content(item, copied_images)


def copy_adjacent_images(generator, item):
    """Copy adjacent image files from source to output directory."""
    source_path = item.source_path
    slug = item.slug
    
    # For recipes, use the save_as path if available, otherwise use slug
    if hasattr(item, "save_as"):
        # Extract directory from save_as (e.g., "recipes/hummus-from-mr-jim/index.html" -> "recipes/hummus-from-mr-jim")
        output_path = os.path.join(
            generator.output_path, os.path.dirname(item.save_as)
        )
    else:
        output_path = os.path.join(generator.output_path, slug)

    # Ensure the target output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Copy all image files from the source directory to the output directory
    source_dir = os.path.dirname(source_path)
    copied_images = []
    for fname in os.listdir(source_dir):
        if fname.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".svg", ".pdf")):
            src = os.path.join(source_dir, fname)
            dst = os.path.join(output_path, fname)
            shutil.copy2(src, dst)
            copied_images.append(fname)
    
    return copied_images


def update_image_urls_in_content(item, copied_images):
    """Update image URLs in content to use absolute paths."""
    # Only fix URLs for items that have _content attribute (articles/pages)
    if hasattr(item, "_content") and copied_images:
        convert_relative_image_paths(item, item.slug, copied_images)


def convert_relative_image_paths(item, slug, image_names):
    # Find image references and fix them
    for img_name in image_names:
        # Look for HTML img tags with relative paths
        item._content = re.sub(
            r'<img([^>]*) src=["\'](?!https?://|/)([^"\']*'
            + re.escape(img_name)
            + ")[\"']",
            r'<img\1 src="/' + slug + r'/\2"',
            item._content,
        )

        # Look for Markdown image syntax
        item._content = re.sub(
            r"!\[(.*?)\]\((?!https?://|/)([^)]*" + re.escape(img_name) + r")\)",
            r"![\1](/" + slug + r"/\2)",
            item._content,
        )

        # Look for HTML anchor tags with relative paths (for PDFs and other files)
        item._content = re.sub(
            r'<a([^>]*) href=["\'](?!https?://|/|#)([^"\']*'
            + re.escape(img_name)
            + ")[\"']",
            r'<a\1 href="/' + slug + r'/\2"',
            item._content,
        )


def register():
    # Connect different handlers for articles and pages
    signals.article_generator_finalized.connect(copy_images_for_articles)
    signals.page_generator_finalized.connect(copy_images_for_pages)
    # Connect to article writer finalized to handle recipes after they're processed
    signals.article_writer_finalized.connect(copy_images_for_recipes)

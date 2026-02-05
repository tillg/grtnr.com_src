# plugins/recipes/__init__.py
import datetime
import os
import sys

from pelican import signals

# Import the central normalize_slug function
sys.path.insert(0, os.path.dirname(__file__))
# Import centralized logging
from logger_config import get_logger
from normalize_slugs import normalize_slug

# Setup logger for this plugin
logger = get_logger("recipes")


class RecipeAdapter:
    """Adapter class for recipes to store in the context."""

    def __init__(self, title, content, metadata, slug, url, save_as, source_path):
        self.title = title
        self.content = content
        self._metadata = metadata
        self.slug = slug
        self._url = url
        self.save_as = save_as
        self.source_path = source_path
        self.template = "recipe"
        self.category = "recipes"

    @property
    def url(self):
        return self._url

    @property
    def metadata(self):
        return self._metadata

    # Add any other properties needed by your templates


def add_recipes_to_context(generator):
    # Only process recipes for ArticleGenerator to avoid duplicate processing
    if not hasattr(generator, "articles"):
        return

    # Skip if recipes already added to avoid duplicates
    if "recipes" in generator.context:
        return

    import os

    from pelican.readers import MarkdownReader

    recipe_dir = generator.settings.get("RECIPE_DIR", "recipes")
    recipe_url_pattern = generator.settings.get("RECIPE_URL", "recipes/{slug}/")
    recipe_save_as_pattern = generator.settings.get(
        "RECIPE_SAVE_AS", "recipes/{slug}/index.html"
    )
    recipe_path = os.path.join(generator.path, recipe_dir)

    if not os.path.exists(recipe_path):
        logger.warning(f"Recipe folder {recipe_path} does not exist.")
        return

    md_reader = MarkdownReader(generator.settings)
    recipes = []

    # Process recipe files
    for root, _, files in os.walk(recipe_path):
        for filename in files:
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(root, filename)

            try:
                content, metadata = md_reader.read(filepath)

                # Set defaults
                if "title" not in metadata:
                    metadata["title"] = (
                        os.path.splitext(filename)[0].replace("-", " ").title()
                    )

                if "date" not in metadata:
                    file_stat = os.stat(filepath)
                    metadata["date"] = datetime.datetime.fromtimestamp(
                        file_stat.st_mtime
                    )

                # Get slug from metadata or derive from filename, then normalize
                raw_slug = metadata.get("slug", os.path.splitext(filename)[0])
                slug = normalize_slug(raw_slug)

                # Update metadata with normalized slug so all URL generation is
                # consistent
                metadata["slug"] = slug

                # Format URL and save_as
                url = recipe_url_pattern.format(slug=slug)
                save_as = recipe_save_as_pattern.format(slug=slug)

                # Create recipe adapter
                recipe = RecipeAdapter(
                    title=metadata["title"],
                    content=content,
                    metadata=metadata,
                    slug=slug,
                    url=url,
                    save_as=save_as,
                    source_path=filepath,
                )

                recipes.append(recipe)
                logger.debug(f"Processed recipe: {recipe.title}")

            except Exception as e:
                logger.error(f"Error processing {filepath}: {e}", exc_info=True)

    # Add recipes to context
    generator.context["recipes"] = recipes
    logger.info(f"Added {len(recipes)} recipes to context")


def generate_recipes(generator, writer):
    """Generate the recipe pages."""
    if "recipes" not in generator.context:
        return

    recipes = generator.context["recipes"]
    logger.info(f"Generating {len(recipes)} recipe pages")

    # Generate main recipe pages
    for recipe in recipes:
        try:
            writer.write_file(
                recipe.save_as,
                generator.get_template(recipe.template),
                generator.context,
                recipe=recipe,
                relative_urls=generator.settings.get("RELATIVE_URLS", False),
            )
            logger.debug(f"Generated recipe page: {recipe.title}")
        except Exception as e:
            logger.error(f"Error writing recipe {recipe.title}: {e}", exc_info=True)

    # Generate localized recipe pages
    _generate_localized_recipe_pages(generator, writer, recipes)

    # Generate recipe indices (main + localized)
    _generate_recipe_indices(generator, writer, recipes)


def _generate_localized_recipe_pages(generator, writer, recipes):
    """Generate localized recipe pages for all languages."""

    # Check if multilingual is enabled
    multilingual_enabled = generator.settings.get("MULTILINGUAL_ENABLED", False)
    if not multilingual_enabled:
        return

    languages = generator.settings.get("MULTILINGUAL_LANGUAGES", ["en"])
    default_lang = generator.settings.get("MULTILINGUAL_DEFAULT_LANG", "en")

    for lang in languages:
        if lang != default_lang:  # Skip default language as it's already generated
            for recipe in recipes:
                try:
                    # Create localized recipe
                    localized_recipe = _create_localized_recipe(recipe, lang)

                    # Create localized context
                    localized_context = generator.context.copy()
                    localized_context["LANGUAGE"] = lang

                    writer.write_file(
                        localized_recipe.save_as,
                        generator.get_template(recipe.template),
                        localized_context,
                        recipe=localized_recipe,
                        relative_urls=generator.settings.get("RELATIVE_URLS", False),
                    )
                    logger.debug(
                        f"Generated localized recipe page for {lang}: {recipe.title}"
                    )
                except Exception as e:
                    logger.error(
                        f"Error writing localized recipe {recipe.title} for {lang}: {e}",
                        exc_info=True,
                    )


def _generate_recipe_indices(generator, writer, recipes):
    """Generate recipe index pages for all languages."""

    # Generate main recipe index
    try:
        writer.write_file(
            "recipes/index.html",
            generator.get_template("recipes_index"),
            generator.context,
            recipes=recipes,
            relative_urls=generator.settings.get("RELATIVE_URLS", False),
        )
        logger.info("Generated main recipe index")
    except Exception as e:
        logger.error(f"Error writing main recipe index: {e}", exc_info=True)

    # Check if multilingual is enabled and generate localized indices
    multilingual_enabled = generator.settings.get("MULTILINGUAL_ENABLED", False)
    if multilingual_enabled:
        languages = generator.settings.get("MULTILINGUAL_LANGUAGES", ["en"])
        default_lang = generator.settings.get("MULTILINGUAL_DEFAULT_LANG", "en")

        for lang in languages:
            if lang != default_lang:  # Skip default language as it's already generated
                try:
                    # Create localized context
                    localized_context = generator.context.copy()
                    localized_context["LANGUAGE"] = lang

                    # Create localized recipes with adjusted URLs
                    localized_recipes = []
                    for recipe in recipes:
                        localized_recipe = _create_localized_recipe(recipe, lang)
                        localized_recipes.append(localized_recipe)

                    writer.write_file(
                        f"{lang}/recipes/index.html",
                        generator.get_template("recipes_index"),
                        localized_context,
                        recipes=localized_recipes,
                        relative_urls=generator.settings.get("RELATIVE_URLS", False),
                    )
                    logger.info(f"Generated localized recipe index for {lang}")
                except Exception as e:
                    logger.error(
                        f"Error writing localized recipe index for {lang}: {e}",
                        exc_info=True,
                    )


def _create_localized_recipe(recipe, lang):
    """Create a localized version of a recipe with adjusted URLs."""

    class LocalizedRecipeAdapter:
        def __init__(self, original_recipe, language):
            # Copy all attributes from the original recipe, excluding properties
            for attr in dir(original_recipe):
                if not attr.startswith("_") and not isinstance(
                    getattr(type(original_recipe), attr, None), property
                ):
                    try:
                        setattr(self, attr, getattr(original_recipe, attr))
                    except AttributeError:
                        # Skip attributes that can't be set
                        pass

            # Store original metadata separately
            self._metadata = original_recipe.metadata

            # Adjust URLs to include language prefix - ensure proper slash handling
            original_url = original_recipe.url
            # For localized recipes, we need to prepend the language code
            # but keep the same relative/absolute nature as the original
            if original_url.startswith("/"):
                self._url = f"/{language}{original_url}"
            else:
                self._url = f"{language}/{original_url}"
            self.save_as = f"{language}/{original_recipe.save_as}"

        @property
        def url(self):
            return self._url

        @property
        def metadata(self):
            return self._metadata

    return LocalizedRecipeAdapter(recipe, lang)


def register():
    """Register the plugin."""
    logger.info("Registering recipes plugin with signals")
    signals.generator_init.connect(add_recipes_to_context)
    signals.article_writer_finalized.connect(generate_recipes)

# plugins/recipes/__init__.py
from pelican import signals
import datetime
import unicodedata
import re


def normalize_slug(text):
    """
    Normalize text for use in URLs and file paths.
    This function provides centralized character transliteration 
    for consistent URL/path generation across the entire site.
    """
    if not text:
        return text
    
    # Common German character mappings
    char_map = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
        'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue'
    }
    
    # Apply character mappings
    for char, replacement in char_map.items():
        text = text.replace(char, replacement)
    
    # Remove or replace other non-ASCII characters
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Convert to lowercase and replace spaces/special chars with hyphens
    text = re.sub(r'[^a-zA-Z0-9\-_]', '-', text.lower())
    text = re.sub(r'-+', '-', text)  # Remove multiple consecutive hyphens
    text = text.strip('-')  # Remove leading/trailing hyphens
    
    return text


class RecipeAdapter:
    """Adapter class for recipes to store in the context."""

    def __init__(self, title, content, metadata, slug, url, save_as,
                 source_path):
        self.title = title
        self.content = content
        self._metadata = metadata
        self.slug = slug
        self._url = url
        self.save_as = save_as
        self.source_path = source_path
        self.template = 'recipe'
        self.category = 'recipes'

    @property
    def url(self):
        return self._url

    @property
    def metadata(self):
        return self._metadata

    # Add any other properties needed by your templates


def add_recipes_to_context(generator):
    # Only process recipes for ArticleGenerator to avoid duplicate processing
    if not hasattr(generator, 'articles'):
        return
        
    # Skip if recipes already added to avoid duplicates
    if 'recipes' in generator.context:
        return
        
    import os
    from pelican.readers import MarkdownReader

    recipe_dir = generator.settings.get('RECIPE_DIR', 'recipes')
    recipe_url_pattern = generator.settings.get(
        'RECIPE_URL', 'recipes/{slug}/')
    recipe_save_as_pattern = generator.settings.get(
        'RECIPE_SAVE_AS', 'recipes/{slug}/index.html')
    recipe_path = os.path.join(generator.path, recipe_dir)

    if not os.path.exists(recipe_path):
        print(f"Recipe folder {recipe_path} does not exist.")
        return

    md_reader = MarkdownReader(generator.settings)
    recipes = []

    # Process recipe files
    for root, _, files in os.walk(recipe_path):
        for filename in files:
            if not filename.endswith('.md'):
                continue

            filepath = os.path.join(root, filename)

            try:
                content, metadata = md_reader.read(filepath)

                # Set defaults
                if 'title' not in metadata:
                    metadata['title'] = os.path.splitext(
                        filename)[0].replace('-', ' ').title()

                if 'date' not in metadata:
                    file_stat = os.stat(filepath)
                    metadata['date'] = datetime.datetime.fromtimestamp(
                        file_stat.st_mtime)

                # Get slug from metadata or derive from filename, then normalize
                raw_slug = metadata.get('slug', os.path.splitext(filename)[0])
                slug = normalize_slug(raw_slug)

                # Format URL and save_as
                url = recipe_url_pattern.format(slug=slug)
                save_as = recipe_save_as_pattern.format(slug=slug)

                # Create recipe adapter
                recipe = RecipeAdapter(
                    title=metadata['title'],
                    content=content,
                    metadata=metadata,
                    slug=slug,
                    url=url,
                    save_as=save_as,
                    source_path=filepath
                )

                recipes.append(recipe)
                # print(f"Processed recipe: {recipe.title}")

            except Exception as e:
                print(f"Error processing {filepath}: {e}")
                import traceback
                traceback.print_exc()

    # Add recipes to context
    generator.context['recipes'] = recipes
    print(f"Added {len(recipes)} recipes to context")


def generate_recipes(generator, writer):
    """Generate the recipe pages."""
    if 'recipes' not in generator.context:
        return

    recipes = generator.context['recipes']
    print(f"Generating {len(recipes)} recipe pages")

    for recipe in recipes:
        try:
            writer.write_file(
                recipe.save_as, generator.get_template(recipe.template),
                generator.context, recipe=recipe,
                relative_urls=generator.settings.get('RELATIVE_URLS', False)
            )
            # print(f"Generated recipe page: {recipe.title}")
        except Exception as e:
            print(f"Error writing recipe {recipe.title}: {e}")
            import traceback
            traceback.print_exc()

    # Generate recipe index
    try:
        writer.write_file(
            'recipes/index.html', generator.get_template('recipes_index'),
            generator.context, recipes=recipes,
            relative_urls=generator.settings.get('RELATIVE_URLS', False)
        )
        print("Generated recipe index")
    except Exception as e:
        print(f"Error writing recipe index: {e}")
        import traceback
        traceback.print_exc()


def register():
    """Register the plugin."""
    print("Registering recipes plugin with signals")
    signals.generator_init.connect(add_recipes_to_context)
    signals.article_writer_finalized.connect(generate_recipes)

import os
import shutil
from pelican import signals

def copy_adjacent_images(generator):
    for article in generator.articles:
        source_path = article.source_path
        slug = article.slug
        #print(f"copy_adjacent_images: Copying images of article: {slug}")
        output_path = os.path.join(generator.output_path, slug)

        # Ensure the target output directory exists
        os.makedirs(output_path, exist_ok=True)

        # Copy all image files from the article's source directory to the output directory
        source_dir = os.path.dirname(source_path)
        for fname in os.listdir(source_dir):
            if fname.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg')):
                src = os.path.join(source_dir, fname)
                dst = os.path.join(output_path, fname)
                shutil.copy2(src, dst)

def register():
    signals.article_generator_finalized.connect(copy_adjacent_images)
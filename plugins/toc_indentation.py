# plugins/toc_indentation.py
from pelican import signals
from bs4 import BeautifulSoup


def process_content(content):
    if (hasattr(content, '_content') and
            not hasattr(content, '_toc_processed')):
        soup = BeautifulSoup(content._content, 'html.parser')
        modified = False

        # Find all ul elements within the content
        for ul in soup.find_all('ul'):
            # Check if this might be a TOC (contains links to anchors)
            links = ul.find_all(
                'a', href=lambda href: href and href.startswith('#')
            )
            if links and len(links) > 0:
                # Add the toc class to this ul
                ul['class'] = ul.get('class', []) + ['toc']
                # Also fix nested ul elements to ensure proper
                # indentation
                for nested_ul in ul.find_all('ul'):
                    nested_ul['class'] = (
                        nested_ul.get('class', []) + ['toc']
                    )
                modified = True

        # Only update content if modifications were made
        if modified:
            content._content = str(soup)

        # Mark as processed to prevent recursive processing
        setattr(content, '_toc_processed', True)


def register():
    signals.content_object_init.connect(process_content)

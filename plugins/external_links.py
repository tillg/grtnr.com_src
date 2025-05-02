from pelican import signals
from bs4 import BeautifulSoup
import re

def is_external_link(href):
    return href and (href.startswith('http://') or href.startswith('https://'))

def process_external_links(content):
    if not content._content:
        return

    soup = BeautifulSoup(content._content, 'html.parser')
    for link in soup.find_all('a', href=True):
        if is_external_link(link['href']):
            link['target'] = '_blank'
            link['rel'] = 'noopener noreferrer'
    
    content._content = str(soup)

def register():
    signals.content_object_init.connect(process_external_links)
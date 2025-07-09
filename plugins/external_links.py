from bs4 import BeautifulSoup
from pelican import signals


def is_external_link(href):
    return href and (href.startswith("http://") or href.startswith("https://"))


def add_external_link_attributes(content):
    if not content._content:
        return

    soup = BeautifulSoup(content._content, "html.parser")
    for link in soup.find_all("a", href=True):
        if is_external_link(link["href"]):
            link["target"] = "_blank"
            link["rel"] = "noopener noreferrer"

    content._content = str(soup)


def register():
    signals.content_object_init.connect(add_external_link_attributes)

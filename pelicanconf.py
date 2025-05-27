import datetime
import os

import pytz

# Our sitename might vary depending on the environment
SITENAME = "grtnr.com"
# Override SITENAME from environment variable if available
if "PELICAN_SITENAME" in os.environ:
    SITENAME = os.environ["PELICAN_SITENAME"]

AUTHOR = "Till Gartner"
SITEURL = ""
DESCRIPTION = (
    "Stuff that keeps me busy, like family, coding, math, " "mountains and more."
)
THEME = "pelicanyan"

PATH = "content"
ARTICLE_PATHS = ["articles"]
PAGE_PATHS = ["pages"]
STATIC_PATHS = ["static"]
ARTICLE_EXCLUDES = ["recipes"]

# Add static files mapping
EXTRA_PATH_METADATA = {
    "static/favicon.ico": {"save_as": "favicon.ico"},
    "static/apple-touch-icon.png": {"save_as": "apple-touch-icon.png"},
    "static/apple-touch-icon-precomposed.png": {
        "save_as": "apple-touch-icon-precomposed.png"
    },
    "static/robots.txt": {"save_as": "robots.txt"},
    "static/humans.txt": {"save_as": "humans.txt"},
}

ARTICLE_SAVE_AS = "{slug}/index.html"
ARTICLE_URL = "{slug}/"

PAGE_SAVE_AS = "{slug}/index.html"
PAGE_URL = "{slug}/"

# Create the slug based on the title if not given in the article.
SLUGIFY_SOURCE = "title"

# Ensure static files are copied to article directories
STATIC_CREATE_LINKS = True

TIMEZONE = "Europe/Rome"

# Set defaults
DEFAULT_LANG = "en"
DEFAULT_DATE = "fs"  # Use file system's modification date

DATE_FORMATS = {
    "en": "%B %-d, %Y",
    "de": "%-d %b %Y",
}

# Add the plugins directory to the path
PLUGIN_PATHS = ["plugins"]
PLUGINS = [
    "auto_title",
    "normalize_slugs",
    "recipes",
    "set_proper_category",
    "filter_articles_for_index",
    "copy_adjacent_images",
    "excerpt_to_summary",
    "external_links",
]

# Categories
USE_FOLDER_AS_CATEGORY = False  # Don't categorize by folder name
CATEGORY_URL = "category/{slug}/"
CATEGORY_SAVE_AS = "category/{slug}/index.html"
CATEGORIES_IN_INDEX = []

DEBUG = True
DELETE_OUTPUT_DIRECTORY = True
CACHE_CONTENT = False

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Topics", "/tags"),
    ("Recipes", "/recipes"),
    ("About", "/about"),
    ("Impressum", "/impressum"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = 10

# Tag cloud settings
TAG_CLOUD_STEPS = 4  # Count of different font sizes in the tag cloud
TAG_CLOUD_MAX_ITEMS = 100  # Maximum number of tags in the cloud
TAG_CLOUD_SORTING = "size"  # 'size' (default) or 'alphabetically'

# URL settings for tags
TAG_URL = "tag/{slug}/"
TAG_SAVE_AS = "tag/{slug}/index.html"
TAGS_URL = "tags/"
TAGS_SAVE_AS = "tags/index.html"

# Generate tag pages
GENERATE_TAGS = True

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# GA_ACCOUNT = 'UA-12344321-1'
TWITTER_ACCOUNT = "tillg"
DIRECT_TEMPLATES = (
    "index",
    "categories",
    "authors",
    "archives",
    "sitemap",
    "robots",
    "humans",
    "tags",
)
ROBOTS_SAVE_AS = "robots.txt"
HUMANS_SAVE_AS = "humans.txt"
SITEMAP_SAVE_AS = "sitemap.xml"
TYPOGRIFY = True


# Add recipes as a content type
RECIPE_DIR = "recipes"
RECIPE_URL = "recipes/{slug}/"
RECIPE_SAVE_AS = "recipes/{slug}/index.html"

RECIPE_PATHS = ["recipes"]  # New setting for recipes

# Register the recipes path
DIRECT_TEMPLATES += ("recipes_index",)  # Add recipes index to direct templates

# Recipes are processed by the recipes plugin, not as static content

GOOGLE_ANALYTICS = "G-H8M7YDCSD4"

# Add built time
# Get current time in UTC
utc_now = datetime.datetime.now(pytz.UTC)

# Convert to your local timezone
local_now = utc_now.astimezone(pytz.timezone(TIMEZONE))

# Format the time
BUILD_TIME = local_now.strftime("%d.%m.%Y %H:%M:%S")

# Markdown config so TOC works
MARKDOWN = {
    "extensions": [
        "markdown.extensions.toc",
        "markdown.extensions.codehilite",
        "markdown.extensions.extra",
        "markdown.extensions.meta",
        "plugins.markdown_wikilinks",
    ],
    "extension_configs": {
        "markdown.extensions.toc": {
            "permalink": False,
            "anchorlink": False,
            "toc_depth": 3,
            "marker": "[TOC]",
        },
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "plugins.markdown_wikilinks": {},
    },
    "output_format": "html5",
}

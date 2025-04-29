AUTHOR = 'Till Gartner'
SITENAME = 'grtnr.com'
SITEURL = ""

PATH = "content"
ARTICLE_PATHS = ['.']
STATIC_PATHS = ['static']
ARTICLE_EXCLUDES = []

# Add static files mapping
EXTRA_PATH_METADATA = {
    'static/favicon.ico': {'save_as': 'favicon.ico'},
    'static/apple-touch-icon.png': {'save_as': 'apple-touch-icon.png'},
    'static/apple-touch-icon-precomposed.png': {'save_as': 'apple-touch-icon-precomposed.png'},
    'static/robots.txt': {'save_as': 'robots.txt'},
    'static/humans.txt': {'save_as': 'humans.txt'}
}

ARTICLE_SAVE_AS = '{slug}/index.html'
ARTICLE_URL = '{slug}/'

# Create the slug based on the title if not given in the article.
SLUGIFY_SOURCE = 'title'

# Ensure static files are copied to article directories
STATIC_CREATE_LINKS = True

TIMEZONE = 'Europe/Rome'

DEFAULT_LANG = 'en'
DATE_FORMATS = {
    'en': '%B %-d, %Y',
    'de': '%-d %b %Y',
}

# Add the plugins directory to the path
PLUGIN_PATHS = ['plugins']
PLUGINS = ['auto_title', 'copy_adjacent_images',
           'excerpt_to_summary', 'external_links']

USE_FOLDER_AS_CATEGORY = False  # Don't categorize by folder name

DEBUG = True
DELETE_OUTPUT_DIRECTORY = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
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
TAG_CLOUD_SORTING = 'size'  # 'size' (default) or 'alphabetically'

# URL settings for tags
TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'
TAGS_URL = 'tags/'
TAGS_SAVE_AS = 'tags/index.html'

# Generate tag pages
GENERATE_TAGS = True

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = 'pelicanyan'
# GA_ACCOUNT = 'UA-12344321-1'
TWITTER_ACCOUNT = 'tillg'
DIRECT_TEMPLATES = ('index', 'categories', 'authors',
                    'archives', 'sitemap', 'robots', 'humans', 'tags')
ROBOTS_SAVE_AS = 'robots.txt'
HUMANS_SAVE_AS = 'humans.txt'
SITEMAP_SAVE_AS = 'sitemap.xml'
TYPOGRIFY = True

MENUITEMS = [
    ('Tags', '/tags/'),
]

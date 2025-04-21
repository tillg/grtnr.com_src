AUTHOR = 'Till Gartner'
SITENAME = 'grtnr.com'
SITEURL = ""

PATH = "content"
ARTICLE_PATHS = ['.']
STATIC_PATHS = ['.'] 
ARTICLE_EXCLUDES = []

ARTICLE_SAVE_AS = '{slug}/index.html'
ARTICLE_URL = '{slug}/'

# Create the slug based on the title if not given in the article.
SLUGIFY_SOURCE = 'title'

# Ensure static files are copied to article directories
STATIC_CREATE_LINKS = True
EXTRA_PATH_METADATA = {}

DELETE_OUTPUT_DIRECTORY = True

TIMEZONE = 'Europe/Rome'

DEFAULT_LANG = 'en'

# Add the plugins directory to the path
PLUGIN_PATHS = ['plugins']
PLUGINS = ['auto_title']

USE_FOLDER_AS_CATEGORY = False  # Don't categorize by folder name

#Set the default metadata to help guide article output
# DEFAULT_METADATA = {
#     'slug': '',  # Use the slug in the article file itself
# }

DEBUG = True

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

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# playground_pelican

Playing around with [Pelican](https://blog.getpelican.com/) static site generator, as announced in my [article](https://grtnr.com/2025-04-18-digital-garden.html).

## Get things up & running

In order to get things running

- Make sure you have Python installed. I work with Python 3.12
- Install the requireed packages: `pip install -r requirements.txt`
- Build it: `pelican`
- In the dev process, you probably want to run it, keep it watching file changes and serve the website: `pelican -r -l`

To work in a Github Codespace, start a Codespace and build it with `pelican`.

## Log

### 2025-05-19: First steps

- Installed Pelican using `pip install pelican`.
- Created a new Pelican project using `pelican-quickstart`.
- Played around with settings in order to have the article markdown file next to the images. In order to get this I need to
  - Change the directory names of the articles to not have the date in it.
- I also added a plugin that generates the title based on the filename: `auto_title.py`.

### 2025-04-21: get the theme

- Starting to install the theme [Pelicanyan](https://github.com/thomaswilley/pelicanyan?tab=readme-ov-file#pelicanyan)
- Imported the content from the old grtnr.com blog and fixed the little problems.

### 2025-04-23: Adapt details

Details like

- Added giscus
- clean titles
- Copy favicon and other static images to output/

### 2025-04-27 & 28: Move to remote Codespace

- Setup Codespace with devcontainer
- Use Dockerfile

## TODO

- Google tracking
- Fix the article "2016-02-13 Playing around with D3.js"
- On sidebar add the last creation / build date.
- Search capability
- Show google tracking data to the visitors
- Show git history to the visitors on the site
- Design home page
- Multilingual
- Linting
- Smart resizing of images
- Add a sitemap
- Check links in build pipeline
- Add a search
- Page cloud
- Tag cloud

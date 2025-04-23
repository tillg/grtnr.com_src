# playground_pelican

Playing around with [Pelican](https://blog.getpelican.com/) static site generator, as announced in my [article](https://grtnr.com/2025-04-18-digital-garden.html).

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

## TODO

- Google tracking
- Tags
- Tage pages
- Design home page
- Multilingual
- Linting
- Smart resizing of images
- Going live to test.grtnr.com
- Add a sitemap
- Check links in build pipeline
- Add a search
- Page cloud
- Tag cloud
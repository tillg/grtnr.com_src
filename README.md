# grtnr.com_src

This is the source of the Website [grtnr.com](https://grtnr.com) and it's test site [test.grtnr.com](https://test.grtnr.com).

[TOC]

## Get things up & running

In order to get things running

- Make sure you have Python installed. I work with Python 3.12
- Install the requireed packages: `pip install -r requirements.txt`
- Build it: `pelican`
- In the dev process, you probably want to run it, keep it watching file changes and serve the website: `pelican -r -l`

To work in a Github Codespace, start a Codespace and build it with `pelican`.

## TODO

- Fix deployment: Deploy to grtnr.com when committing to main, deploy to test.grtnr.com when committing to another branch.
- Fix the article "2016-02-13 Playing around with D3.js"
- Search capability
- Show google tracking data to the visitors
- Show git history to the visitors on the site
- Design home page
- Multilingual
- Linting
- Smart resizing of images
- Add a sitemap
- Check links in build pipeline
- Page cloud
- Tag cloud

## Archive

For historical reasons I kept old versions of my site in this repo:

- [grtnr_2022](grtnr_2022) contains the Jekyll based version of 2022
- [grtnr_2024](grtnr_2024) contains the Jekyll based version of 2024
- [Migration to Pelican](MIGRATION_TO_PELICAN.md) explains my path of migrating from the 2024-Version on Jekyll to Pelican.

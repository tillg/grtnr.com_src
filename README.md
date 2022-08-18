# grtnr.com_jekyll_2022

The content of my website. Can be reached under...

* https://tillg.github.io/grtnr.com_jekyll_2022/

## Installing & running locally

To install & run the site locally, you need to install the bundles from the `gemfile`:

```bash
bundle install
```

and then tun the site locally with `bundle exec jekyll serve`.

## Todo

* ~~Fix: Images are not visible~~
* Find a more pleasant layout
* Have actions that test before publishing:
  * Can all the content be properly translated to HTML?
  * Are all the links valid?
  * Are all the images available?
* Have Google tracking
* Have sitemap
* Navigation with categories, i.e. recipes, tech, family, travel...
* Integrate search
* Integrate comments
* Differentiate posts and pages (i.e. about, impressum...)

## Problems 

A list of problems I met and how I delt with them.

### Image location
Typically Jekyll wants it's images to be in `assets/images/...`. When referring images in posts or pages, usually one references `/assets/images/image.jpg`. In my case the site might be rendered not in the root directory, so for example to `https://tillg.github.io/jekyll_test/`. Thus, referencing `/assets` points to `https://tillg.github.io/assets` rather than to `https://tillg.github.io/jekyll_test/assets`.

Other criteria that I have:

* Editing in VS Code should be smooth: When writing posts in VS Code I use the Markdown preview side by side. I would like to see the pictures in this preview, so the reference to pictures should also be valid in the source code.
* Running jekyll locally with `bundle exec jekyll serve` should also properly reference the pictures.
* In production, i.e. on `https://grtnr.com` it shopuld obviouzsly also work.

Therefore I decided keep the images close to the posts: For every post I create a subdirectory with the name of the post, i.e. `2021-12-05-till-plaetzchen/`. Inside this dir I put the markdown file with the post and the images, i.e. `2021-12-05-till-plaetzchen.md` and `plaetzchen.jpg`.

In order for Jekyll to copy the image files to the apropriate location, I have to use [jekyll-postfiles](https://nhoizey.github.io/jekyll-postfiles/).,
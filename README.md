# grtnr.com_jekyll_2022

The content of my website. Can be reached under...

* https://tillg.github.io/grtnr.com_jekyll_2022/
* https://new.grtnr.de

## Installing & running locally

To install & run the site locally, you need to install the bundles from the `gemfile`:

```bash
bundle install
```

and then tun the site locally with `bundle exec jekyll serve`.

## Todo & done

* ~~Fix: Images are not visible~~ 2022-08
* ~~2022-08-20 Link it to grtnr.com (with CNAME) --> Using https://new.grtnr.de instead.~~
* Build process should check if all links work: external, pictures, etc.
* Find a more pleasant layout
* Have recipes as extra collection & extra layout
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

### Domain grtnr.com

Somehow I couldn't get the domain grtnr.com to work: When setting the DNS A Records at    this is the result of a dig (even after waiting some days):
```bash
dig grtnr.com +nostats +nocomments +nocmd

; <<>> DiG 9.10.6 <<>> grtnr.com +nostats +nocomments +nocmd
;; global options: +cmd
;grtnr.com.			IN	A
grtnr.com.		600	IN	A	15.197.142.173
grtnr.com.		600	IN	A	3.33.152.147
```

That's the way it should look:
```bash
 dig new.grtnr.de +nostats +nocomments +nocmd

; <<>> DiG 9.10.6 <<>> new.grtnr.de +nostats +nocomments +nocmd
;; global options: +cmd
;new.grtnr.de.			IN	A
new.grtnr.de.		3600	IN	CNAME	tillg.github.io.
tillg.github.io.	3600	IN	A	185.199.108.153
tillg.github.io.	3600	IN	A	185.199.109.153
tillg.github.io.	3600	IN	A	185.199.110.153
tillg.github.io.	3600	IN	A	185.199.111.153
```

For the time being I switched over to the domain https://new.grtnr.de .
### Check links

[How to Check for Broken Links in Jekyll](https://www.supertechcrew.com/jekyll-check-for-broken-links/)
### Image location

Typically Jekyll wants it's images to be in `assets/images/...`. When referring images in posts or pages, usually one references `/assets/images/image.jpg`. In my case the site might be rendered not in the root directory, so for example to `https://tillg.github.io/jekyll_test/`. Thus, referencing `/assets` points to `https://tillg.github.io/assets` rather than to `https://tillg.github.io/jekyll_test/assets`.

Other criteria that I have:

* Editing in VS Code should be smooth: When writing posts in VS Code I use the Markdown preview side by side. I would like to see the pictures in this preview, so the reference to pictures should also be valid in the source code.
* Running jekyll locally with `bundle exec jekyll serve` should also properly reference the pictures.
* In production, i.e. on `https://grtnr.com` it shopuld obviouzsly also work.

Therefore I decided keep the images close to the posts: For every post I create a subdirectory with the name of the post, i.e. `2021-12-05-till-plaetzchen/`. Inside this dir I put the markdown file with the post and the images, i.e. `2021-12-05-till-plaetzchen.md` and `plaetzchen.jpg`.

In order for Jekyll to copy the image files to the apropriate location, I have to use [jekyll-postfiles](https://nhoizey.github.io/jekyll-postfiles/).
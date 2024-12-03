# grtnr.com_2024

The content of my website. Can be reached under...

* https://tillg.github.io/grtnr.com_2024/
* https://grtnr.com

## Installing & running locally

To install & run the site locally, you need to install the bundles from the `gemfile`. Make sure you have an up-to-date ruby version on your system (see below for tips for Mac users).

```bash
gem install bundler 
bundle install
```

and then tun the site locally with `bundle exec jekyll serve`.

Once all dependies are installed, it is best to use the standard scripts that are also used by the github actions:

* **`./build.sh`** - guess what this does... ;)
* **`./post_build_check_soft.sh`**: Runs checks on the built `_site` directory. If errors are found they are reported but don't break the build.
* **`./post_build_check_hard.sh`**: Runs checks on the built `_site`directory that have to succeed, otherwise the build is considered to be broken.

## Todo 

* Check that every enntry has a date
* DNS Setup: Forwart tillgartner.com --> grtnr.com
* Test: If I remove the accent image (wooden_desk.jpg), my link tests should fail - why didn't they?
* Build pipeline: Check that posts have the right structure: Have a layout, a date etc.
* Build pipeline: Make sure that posts have the proper file names: YYYY-MM-DD-xyz.md
* Build pipeline: Test that the no of posts corresponds to the number of entries in the posts directory
* Build pipeline: Create a warning if a blog entry has no excerpt
* Sort out tags in theme hydejack
* Make sure images are minimized during build process
* Navigation with categories, i.e. recipes, tech, family, travel...
* Lint & format Markdown before commit (commit hooks)
* Have sitemap
* Integrate search
* Integrate comments
* Make Google analytics visible within the website - so visitors can see how many visitors there are

##  Findings, Readings, Problems

A list of topics I worked on, details I found out, problems I solved.

### Changing theme

In Nov/Dec 2024 I changed from the [Hydejack theme](https://hydejack.com) to [Lanyon](https://github.com/poole/lanyon). The Hydejack theme was pretty much packaged as gem, wjereas Lanyon come along as preset Jekyll installation. These were the things I had to take care of:

* Set up a new site from scratch
* Copy over the posts
* Home page with a list of posts
* Generate the site with pictures from within sub-dirs per post. See [jekyll-postfiles](https://github.com/nhoizey/jekyll-postfiles) plugin
* Fix the posts so that they render well.
* Recipes: Make a `recipes.html` page (similar to my `index.html`). Set the link to the image as `src="/{{ post.image }}"` so it picks the images in the root.

These are the things I still need to deal with ion order to be on par with the old site:

* Go thru all the old commit messages and check we have not lost any functionality...
* Deploy via github actions

### Ruby versions

**Update 27.11.2024**: New Mac, new problems. After (re-)reading lots of ruby installationb guides, I decided that I only need ONE ruby version on my Mac, thus there is no need to use a ruby version manager 😉
Therefore I use `brew install ruby`. The problem is, that ruby is installed _keg only_, i.e. it is not symlinked: brew does not override the system ruby, as this could break some usages. 
In order to find how to use the new, brew-installed ruby, run `brew info ruby` and follow the guide.


**Old explanation**: Getting the right ruby version running locally can be a mess! Everything worked fine on my Mac, then I tried to add content 6 months later, and nothing worked anymore: The updated ruby version that I got via my usual `brew upgrade` didn't support some features that jekyll needed.

So I went for `chruby`: A tool to _change ruby_ versions. Installing ruby versions so that chruby can switch between them needs `ruby-install`. And installing versions failed, because... [This stackoverflow article](https://stackoverflow.com/questions/74353384/installing-ruby-but-getting-error-linker-command-failed-with-exit-code-1) fixed it.

Cheatsheet:
```bash
# See what ruby versions are installed
> chruby

# Install another versions
> ruby-install 3.1.2 -- --enable-shared # See the article mentioned above why...
```

### Linting

Requirements:

* Linting in my VScode
* Automatic repair where possible
* Linting as commit-gate. I.e. commits fail if linting failed.
* Same rules are used when linting in VScode and when linting when committing - sourced from the same configuration! So that config changes are just to be made in one place and become effective everywhere automatically.

Reading:

* [How to use ESLint in VSCode](https://www.robinwieruch.de/vscode-eslint/)
* [Automatically format and lint code with pre-commit](https://interrupt.memfault.com/blog/pre-commit)
* [A Guide to Order: Setting up Prettier and Eslint with Husky, Lint-staged and Commitizen](https://folafunmi.hashnode.dev/a-guide-to-order-setting-up-prettier-and-eslint-with-husky-lint-staged-and-commitizen)

### Resizing images

* A Jekyll plugin that seems to do exactly that: [Jekyll Resize 🖼 🤏 🔬](https://github.com/MichaelCurrin/jekyll-resize)

### Going live

**Target**: Publish under https://grtnr.de

* Redirect DNS to point to Github - **DONE**
* Fix CNAME file in repo & re-built & deploy **DONE**
* Fix settings of github repo **DONE**
* --> New site should be visible, maybe wait a bit... **DONE**
* Adjust google tracking **DONE**
* Decommission the old blog on AWS **DONE**

```bash
# Checking if the DNS settings are visible
 dig grtnr.de +nostats +nocomments +nocmd

; <<>> DiG 9.10.6 <<>> grtnr.de +nostats +nocomments +nocmd
;; global options: +cmd
;grtnr.de.			IN	A
grtnr.de.		600	IN	A	185.199.108.153
grtnr.de.		600	IN	A	185.199.109.153
grtnr.de.		600	IN	A	185.199.110.153
grtnr.de.		600	IN	A	185.199.111.153

# Looks good...
```

### Overriding theme

I wanted to override certain aspects of my theme (Hydejack): Maybe the footer, create a new layout for recipes that is based on blog layouts etc.

A very good description on [how to override certain aspects of themes](https://jekyllrb.com/docs/themes/) - including a way on how to do it while still using the gem based theme, which allows future updates.

```bash
# Find where the theme gem is located 
bundle info --path jekyll-theme-hydejack
/usr/local/lib/ruby/gems/3.1.0/gems/jekyll-theme-hydejack-9.1.6
```

### Google Analytics

Go check for analytics data [here](https://analytics.google.com).

As no data became visible even after a couple of days, I started looking into the [Google Analytics Debugger](https://chrome.google.com/webstore/detail/google-analytics-debugger/jnkmfdileelhofjcijamephohjechhna?hl=en).

It seems that Google changed the way they track traffic. They used to have _Universal Analytics IDs_ (of the shape `UA-...`) and switched to _Analytics 4 IDs_ of the shape `G-...`. Since hydejack currently only supports UA-type IDs, I created one like [explained here](https://support.google.com/analytics/answer/10269537). 

Note: **Universal Analytics properties will stop collecting data starting 1 July 2023. It’s recommended that you create a Google Analytics 4 property instead.**

### Using Theme Hydejack

I used the theme [Hydejack](https://hydejack.com) (as of 2022-08). It looks nice, hase some images that don't get in your way, is responsive - so I give it a try. Configuration was straight forward.

But it seems to have a bug: When building the site and running my `htmlproofer` check, the check raised an error in every HTML file: ` 'a' tag is missing a reference`.

Tracking down the source I ended up in the the following file in the theme's gem: `_includes/templates/error.html`:

```liquid
<template id="_error-template">
  <div class="page">
    <h1 class="page-title">{{ strings.error.title | default:"Error" }}</h1>
    {% capture link %}<a class="this-link" href=""></a>{% endcapture %}
    {% assign text = strings.error.message | default:"Sorry, an error occurred while loading: <!--link-->." %}
    <p class="lead">
      {{ text | replace:"<!--link-->",link }}
    </p>
  </div>
</template>
```

When looking at it, it is obvious that the `href=""` will always stay empty... So I replaced it with an overridden `error.html` file in my repo. 

### Jekyll Themes

Jekyll themes I looked at:

**[Hydejack](https://hydejack.com)**: For nerds & academics (so that could fit ;) ), a bit more colorful.

![Hydejack](/images/hydejack-9.jpg)

**[al-folio](https://github.com/alshedivat/al-folio)**: **Too dry, REALLY for academics...** For academics, maybe a bit black-anbd-white-ish, but coiuld fit every content.

![Theme preview](/images/al-folio-preview.png)

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

[How to Check for Broken Links in Jekyll](https://www.supertechcrew.com/jekyll-check-for-broken-links/).

This works somehow locally: 

```bash
bundle exec jekyll build
bundle exec htmlproofer ./_site
```

Problems so far:

* http links are considered a _bug_ or are reported as such. But some pages don't offer https and I still want to link them --> how to switch off this test?


### Image location

Typically Jekyll wants it's images to be in `assets/images/...`. When referring images in posts or pages, usually one references `/assets/images/image.jpg`. In my case the site might be rendered not in the root directory, so for example to `https://tillg.github.io/jekyll_test/`. Thus, referencing `/assets` points to `https://tillg.github.io/assets` rather than to `https://tillg.github.io/jekyll_test/assets`.

Other criteria that I have:

* Editing in VS Code should be smooth: When writing posts in VS Code I use the Markdown preview side by side. I would like to see the pictures in this preview, so the reference to pictures should also be valid in the source code.
* Running jekyll locally with `bundle exec jekyll serve` should also properly reference the pictures.
* In production, i.e. on `https://grtnr.com` it shopuld obviouzsly also work.

Therefore I decided keep the images close to the posts: For every post I create a subdirectory with the name of the post, i.e. `2021-12-05-till-plaetzchen/`. Inside this dir I put the markdown file with the post and the images, i.e. `2021-12-05-till-plaetzchen.md` and `plaetzchen.jpg`.

In order for Jekyll to copy the image files to the apropriate location, I have to use [jekyll-postfiles](https://nhoizey.github.io/jekyll-postfiles/).

**Update** (2022-08-28): When separating the recipes from the blog posts I had another problem:

* Recipes are Jekyll collection, so trheir respective md files are located in `/_recipes`.
* If I put the images next to the recipe, the path in the source is as follows: `/_recipes/sandwiches/<here are the MD file and images>`.
* When referring images from the MD file as `sandwich.jpg` it works fine when being called from the recipe page itself, but fails when being called from the list of recipes...

Solution:

* I defined the output path for recipe documents like so:

```yaml
collections:
  recipes:
    output: true
    permalink: /:name
```

This way the recipes are rendered in the root directory, alongside with their images. So the pic references within the recipes work well.

Furthermore I created a recipe list: `/recipes.md`. This is rendered to `/recipes.html`. In this overview the header images are shown if there are any (i.e. imges referenced in the front matter). And they are referenced as `sandwich.jpg` - and are located within the same directory ;)
---
title: How I moved to GitHub & JBake
tags: tech, webSite
image: github.png
date: 2015-11-30
---

**\*** This page is ~~under construction~~ unfinished... **\***

First: It's not my invention! Many did it before, there are lots of description out there. It still took me some time ;)

[This](http://alexcican.com/post/guide-hosting-website-dropbox-github/) and [this](http://alexcican.com/post/blog-dropbox-scriptogram) was the most inspiring source and easiest explanation (that gives confidence ;) ).

# Setup

So this is the overall setup I have:

- A directory on my Mac that holds the content. I use the basic structure that [Jbake](http://jbake.org) uses.
- A git-cloned directory on my Mac with the output of the jBake-process
- A little script that I run every time I modified something. The script does the baking and the git-publishing
- And of course the settings in the DNS to point my Domain name to the Github IPs

## JBake

Why do I use JBake? I like the principle and I feel more comfortable in Java than in other programming languages. I haven't touched the JBake internal code, but I feel confident that I could.
The principle way that JBake operates is similar to the famous [Jekyll](https://jekyllrb.com/): It parses content files and creates (static) HTML files out of it. The content files can contain Markdown or some other formats; I just use Markdown.

My directory structure looks like this:

```
.
|-- assets
|   |-- favicon.gif
|   |-- robots.txt
|   |-- img
|   |   |-- logo.png
|   |-- js
|   |   |-- custom.js
|   |-- css
|       |-- style.css
|
|-- content
|   |-- about.html
|   |-- 2013
|       |-- 01
|       |   |-- hello-world.html
|       |-- 02
|           |-- weekly-links-1.ad
|           |-- weekly-links-2.md
|
|-- templates
|   |-- index.ftl
|   |-- page.ftl
|   |-- post.ftl
|   |-- feed.ftl
|
|-- jbake.properties
```

By default JBake produces the output directory into this tree. In my case I bake my stuff into a directory that is git-synced.

## The GitHub setup

## The DNS settings

# Next up

There are a couple of things I plan to change.

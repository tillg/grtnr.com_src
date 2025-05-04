---
title: Autocompleting my Blog
tags: blog, tech, softwareweneed
summary: I now have a Pelican based blog and want to automagically add or fix content: Picture tags, article summaries, translations... Finally a wa to use AI 🤖
---

- [Tools I would like to have](#tools-i-would-like-to-have)
  - [Picture tag completion (AI)](#picture-tag-completion-ai)
  - [Link checker](#link-checker)
  - [Extract Generator (AI)](#extract-generator-ai)
  - [Translator (AI'ish)](#translator-aiish)
  - [Article illustration (AI)](#article-illustration-ai)
- [We need a build pipeline](#we-need-a-build-pipeline)
  - [Interims data](#interims-data)
  - [Integrity of authored content](#integrity-of-authored-content)
  - [Where to keep data](#where-to-keep-data)
  - [Processing order](#processing-order)

Since last week my blog is based on [Pelican](https://getpelican.com), the Python based static blog generator. Now that the blog is built in a language that I master more or less, I can think of improving the process of writing and building things myself. And of course there are lots of tools that I can think of in order to make my life as well as the life of my readers easier. So here are some examples of these helpers.

## Tools I would like to have

### Picture tag completion (AI)

Whenever I add a picture without an alt text, it's bad for blind people. But I am lazy, so why not let an AI describe the picture and add it as ALT text?

### Link checker

I have many links pointing to external locations. And sometimes webpages disappear, so my links might point into Nirwana. It would be nice if

- my user wouldn't have to click on broken links 
- I would get a tip that I need to fix one or the other link
- I could maybe prevent the situation by keeping a copy of the page I link to in my own blog. Or is that evil scraping and content stealing?

### Extract Generator (AI)

I often write articles without specifying the summary / excerpt that is shown in the article list. By default Pelican (and other static generators) take the first paragraph or the first 30 words and use it as excerpt. 

Wouldn't it be much nicer to ask an LLM to generate a reasonable 3 lines summary?

### Translator (AI'ish)

In my blog I sometimes write English, sometimes German articles. Maybe there is even a French article here and there. Wouldn't it be nice to have every article in every language? It feels as if nowadays that should be a standard, given the good quality of today's translation tools. 

So I write my articles in whatever language just comes out of my little brain, and the system should generate the missing languages.

### Article illustration (AI)

I try to have pictures for most of my articles, as it's just a nicer reading experiance and pleasant for the eye. I often find something in the internet, but not always - also because I sometimes don't even bother searching an image. But the AI could search, or even generate a nice picture for my _naked_ articles.

## We need a build pipeline

In order to get those things built, I feel I need something like a _Build Pipeline_:

![Build Pipeline](https://insights.mgm-tp.com/wp-content/uploads/2023/08/mgm-CI-CD-Pipeline.png)
_A modern CI/CD build pipeline, taken from [mgm technology partners](https://mgm-tp.com)_

Some thoughts about the structure, the processing and how to organize data.

### Interims data

What Pelican does, is to take the source of the articles, together with the configuration and generate the web pages. It does so by it's standard processing and by potential plugins. Plugins can be third-party or delf-developed. In my case I have both.

Many of the tools I envisage create additional data, and often times the creation is expensive and time consuming. Think of creating an excerpt of an article: The entire text needs top be sent to an AI and processed. This takes multiple seconds and costs real money. Therefore it's certainly not something we wnt to run on every build. So we will have to keep the data between the different build runs.

### Integrity of authored content

One way we could think of solving this, is to simply add the AI generated excerpt to the original markdown (in this case it would go in the front matter as `summary` field). 

But I don't like this at all: I don't want the AI to mess around in the text and content I have been crafting personally. Therefore I want to define the following rule for my system:

**My authored Markdown files should never be modified by automated tools.**

### Where to keep data

That leaves me with the question where to keep the data like AI generated summaries. The natural place is to keep it next to the markdown files, but in it's own file. As I have separate directories for each of my article, I end up with this shape of directories and files:

```file
content
    articles
    ...
    2025-04-18-digital-garden
        2025-04-18-ditigal-garden.md
        2025-04-18-digital-garden.picture-tags.json
        2025-04-18-digital-garden.summary.json
        digital-garden.jpg
```

Some thoughts and arguments for this structure:

- Every tool has it's own file to keep things separate.
- I use JSON files: Easy to process and easy to read.
- The files are next to the original article, so everything that relates is close by and _encapsulated_.
- The JSON files are also version controlled and stored in Git, so wether I run the build process on my local dev machine or inside Github Actions or another CI/CD processor, it re-uses the previously generated data.

### Processing order

This data layout requires a multi-step build-process:

1. **Create additional data:** generate the summaries, the picture descriptions, the pictures, check the links (and store the result of those checks)... This process part is potentially time consuming, generates lots of additional data and requires intelligent caching and cache-validation mechanisms. I.e. "How do I check if I need to re-create the summary of an article or I can use the one in the JSON file alongside the markdown article?".
2. **Build the site:** This is the basic Pelican creation process as we know it, except that it also needs to _integrate_ the additional data that is now in the JSON files. I will do this one or more Pelican plugins that I will develop.

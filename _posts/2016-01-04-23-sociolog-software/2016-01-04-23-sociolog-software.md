---
title: sociolog - Your trail across social media
tags: [softwareWeNeed]
layout: post
date: 2016-01-04
image: sociolog.png
---

I write or blog in different media:

- Twitter
- Facebook
- A private blog with restricted access (because it contains family pictures)
- This [blog](http://tillgartner.com)

From time to time I find it nice to scroll through my past. I do this most often on our family blog, because it contains the most interesting content and because it is easy to scroll through. I would like to be able to scroll through all my past across all media. 

So this is what my software should do:

- Collect all entries I wrote in the social media:
	- Twitter
	- Facebook
	- Wordpress
- Create one document per entry in a Github Repo
- Handle properly duplicate content: Since some years my Twitter account is _linked_ to my Facebook account in that Twitter entries are replicated to Facebook. That's because I have people that I consider _audience_ in both media. 
- Collect also the feedback to my posts
- Nicely display them in a static way, including overview pages

Some technical thoughts:

- I would write it in java because that's what I know best
- Would be a headless program i.e. no UI
- Input should be the date of the last recorded social media entry
- It collects all the entries (including the comments to it) on the different social media channels since that date
- It dedupes them (i.e. merges the ones that are the same or replicates of one another on different channels)
- It creates one document / file per social media entry and writes them in an output directory
- This directory is then replicated / added to a github account
- Social media entry documents would be named like `2015-12-03-The_title_of_what_ I_wrote-TWITTER.json`
- There would be a _header file_ with a fixed name, i.e. `sociologs.json`. This file would hold the first 20 logs and point to a file with the next logs.
- The domain `sociolog.io` would be [available](https://www.godaddy.com/domains/searchresults.aspx?&checkAvail=1&domainToCheck=sociolog.io) - as of today, Jan 4 2016.
- The generated `index.html` would load the data via JS/AJAX requests and continue loading while the user scrolls down

If anyone is interested, or has comment, please get in touch at till`dot`gartner`at`gmail`dot`com.


---
title: A Proxy for offline surfing
tags: softwareweneed
---

This is a piece of software I would love to have: A proxy that runs on my notebook and that intelligently caches certain websites so I can surf them when being offline.

More specifically:

- A proxy that runs on my notebook
- The proxy knows what pages/sites I want to have available when being offline
- When the browser requests one of those pages, the proxy checks wether the website is reachable. If so, it downloads the page and sends it to the browser. If the proxy can’t reach the website, it tries to serve the page from its local cache.

This way, I could surf normally when being online. When being offline, I could only access a little part of the internet – but I could still read some pages.

Once this is achieved, the proxy could be improved:

- While being idle and having an internet connection, it could refresh pages in it’s cache
- By counting what pages I access often, it could decide what pages make sense to be cached
- It could learn what pages change how often and adapt the refresh intervals accordingly
- …

And here are the questions I have:

- Does anyone out there know a tool that provides this functionality?
- Would anyone see a killer-problem I missed?
- Any good ideas how this could be built?

For completeness of information: I use a MacBook, OS X 10.6. Comments are welcome….

Have a nice evening,

– Till.
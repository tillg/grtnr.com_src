---
date: 2025-04-18
image: digital-garden.jpg
excerpt: "I read a bout digital gardens and liked the idea. So I started thinking on how I would setup such a garden - and of course used AI help..."
---

![Digital garden](digital-garden.jpg)

- [Requirements](#requirements)
- [Technology and Architecture](#technology-and-architecture)
- [ChatGPT: Building a Python-Powered Digital Garden: Stack \& Architecture](#chatgpt-building-a-python-powered-digital-garden-stack--architecture)
  - [Static Site Generator \& Content Organization](#static-site-generator--content-organization)
  - [Markdown Editing \& Local Preview](#markdown-editing--local-preview)
  - [Wiki-Style Internal Linking \& Backlinks](#wiki-style-internal-linking--backlinks)
  - [Custom Content Types \& Templates](#custom-content-types--templates)
  - [Beautiful Theming (Ghost-Inspired Design)](#beautiful-theming-ghost-inspired-design)
  - [Multi-Language Support \& AI Translations](#multi-language-support--ai-translations)
  - [Content Access Control (Roles \& Authentication)](#content-access-control-roles--authentication)
  - [Tags, Indexes, and Navigation Pages](#tags-indexes-and-navigation-pages)
  - [Build Pipeline \& Link Validation](#build-pipeline--link-validation)
  - [Summary of the Recommended Stack](#summary-of-the-recommended-stack)
- [Follow up questions](#follow-up-questions)
  - [Changing the structure](#changing-the-structure)
  - [Articles or Pages?](#articles-or-pages)
- [Playing around](#playing-around)


I read about Digital Gardens on [heise (in German)](https://www.heise.de/hintergrund/Nerd-Trend-Digitaler-Garten-Die-eigene-Website-als-persoenliches-Wissensarchiv-10344169.html) and really liked the idea. The key differences to my current blog that I thought of are

* The idea of writing down ideas and starting articles right away - and having them in the garden immediatly. That's a big digfference to the attidude of "I need to finish the article before I publish it".
* The idea of linking to other articles and creating a network of articles. That's something I can already do in my blog, but the process is delicate: If I rename or move an article around, the links to it are broken. Also the idea of backlinks is striking.
* Putting the topics more to the front rather than the date: My blog is primarely structured and presented by date. Having the topic(s) more as navigation structure seems compelling. Of course I would still löeave the date of creation, as well as the date of the last modification.

# Requirements

As usual I tend to start by looking at the technical side 😀. So I jotted down my requirements and asked ChatGPT for help.

My requirements for a digital garden system:

* Articles are based on markdown files.
* Built as static generated website.
* One article in one directory together with its resources: pictures, PDFs, other files. This way local rendering per article makes sense, very helpful while editing. I would edit the articles with VScode or another editor that has markdown support.
* Articles (i.e. their directories) can be in a directory tree structure. Their directory structure describes the category. For example/tech/dev/data_science
* Written in Python, so I can tinker around.
* Build pipeline can be completed: a stage to check internal links.
* Internal links as *[ [links] ]*. And show backlinks in linked articles.
* I want to easily create specific article types with special structure, fields, rendering. Examples are RECIPE, PLACE or LOCATION, TRIP ADVENTURE, …
* Beautiful site! Not like a messy nerdy garden! Take inspiration from beautiful blogs like ghost.
* Multilingual, with languages filled up by AI if not provided by author.
* Different access rights: some content is public, other for family & friends or other user groups.
* Access roles, for example: articles that are unpublished can only be seen by users with role EDITOR.
* Allow multiple index pages: tags, historical index (maybe also per tag), most read, most starred… Index pages can be generated but also hand crafted. Specifically the home page.

# Technology and Architecture

[This is what ChatGPT produced](https://chatgpt.com/share/68026bb5-d040-8009-9f79-ec0fd35880f4) (I thionk it's really good, so I paste it all here):

Great. I’ll explore the best Python-based static site generators and architecture for building a beautifully styled, markdown-driven digital garden with support for access control, internal link checking, multilingual support, and article-type customization. I’ll also ensure the system supports your preferred local editing flow, generates plain HTML, and works well with GitHub Pages.

I’ll get back to you with a recommended stack, architecture diagram, and suggestions on how to implement your requirements smoothly.

_Researched for 11m 16s * 23 sources_

# ChatGPT: Building a Python-Powered Digital Garden: Stack & Architecture

## Static Site Generator & Content Organization  
For a **Python-based static site generator**, **Pelican** is an excellent choice. Pelican is actively maintained and well-documented, supporting Markdown content and multi-language publishing out-of-the-box ([GitHub - getpelican/pelican: Static site generator that supports Markdown and reST syntax. Powered by Python.](https://github.com/getpelican/pelican#:~:text=,rich%20plugin%20ecosystem%3A%20Pelican%20Plugins)). It generates a plain HTML site (no need for React/Vue) and has a rich plugin ecosystem for extending functionality ([GitHub - getpelican/pelican: Static site generator that supports Markdown and reST syntax. Powered by Python.](https://github.com/getpelican/pelican#:~:text=,rich%20plugin%20ecosystem%3A%20Pelican%20Plugins)). 

**Content Structure:** Organize the digital garden’s content in a logical directory hierarchy under Pelican’s `content/` folder. Each article lives in its own subdirectory alongside its assets. For example: 

```
content/
├── tech/
│   └── dev/
│        └── data_science/
│             └── my-article/ 
│                  ├── index.md        # Article in Markdown
│                  ├── figure1.png     # Images/PDFs related to article
│                  └── data.pdf
└── travel/
    └── trip-to-paris/
         ├── index.md
         └── eiffel.jpg
``` 

In this layout, every article (`index.md`) is grouped with its media. Pelican can handle “page bundles” like this by treating those subfolders as both content and static paths. We configure Pelican’s settings to include each folder in `ARTICLE_PATHS` and `STATIC_PATHS` so that markdown files are processed and assets are copied through to output ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Starting%20with%20Pelican%203,directory%20reserved%20for%20static%20files)) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=generated%20site,in%20earlier%20versions%20of%20Pelican)). Pelican’s **attach syntax** allows linking to local files easily: in Markdown, use `{attach}` to reference files in the same folder. For example: `![Figure]({attach}figure1.png)` in `my-article/index.md` will copy *figure1.png* into the article’s output directory and link to it ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Starting%20with%20Pelican%203,sibling%20of%20the%20linking%20document)) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Title%3A%20Test%20Post%20Category%3A%20test,31)). This keeps images/PDFs co-located with their article and ensures links aren’t broken after the static build ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=output%20%E2%94%94%E2%94%80%E2%94%80%202014%20%E2%94%9C%E2%94%80%E2%94%80%20archive,post.html)). 

Pelican also supports using folder names as categories automatically. By default, the immediate parent folder becomes the category (e.g. “data_science” in the path above) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Note%20that%2C%20aside%20from%20the,W3C%E2%80%99s%20suggested%20subset%20ISO%208601)). We can preserve deeper nesting in URLs by customizing the save path. For instance, setting `ARTICLE_SAVE_AS = '{category}/{slug}/index.html'` and similar `ARTICLE_URL` will output each post as an `index.html` inside a folder matching its category/slug. This yields clean URLs like `/tech/dev/data_science/my-article/` reflecting the directory structure. (Pelican’s `USE_FOLDER_AS_CATEGORY=True` by default uses the lowest folder as category; for multi-level taxonomy, one can either combine the path into one category or treat top folders as sections and use tags for sub-classification.) 

## Markdown Editing & Local Preview  
All articles are written in plain **Markdown** (with YAML/TOML front matter for metadata) so you can comfortably author content in VS Code or any editor. Each Markdown file begins with metadata like title, date, tags, etc. Pelican only requires a title (it can derive others if needed) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Note%20that%2C%20aside%20from%20the,W3C%E2%80%99s%20suggested%20subset%20ISO%208601)), but we’ll use metadata extensively for custom behavior (more on this later). A sample front matter for an article might be: 

```markdown
Title: My Data Science Journey  
Date: 2025-04-10  
Category: data_science  
Tags: python, analytics  
Slug: my-data-science-journey  
Status: published  
```

**Local Preview:** To enable per-article preview while editing, use Pelican’s built-in development server. Pelican’s CLI/Makefile supports an auto-reload server (e.g. `make devserver` or `pelican --autoreload --listen`) that watches for file changes and rebuilds as you write. This way, you can navigate to `http://localhost:8000/tech/dev/data_science/my-article/` and see the rendered HTML update on each save. Because Pelican does selective output writing and caching, rebuilds are fast even for large sites ([GitHub - getpelican/pelican: Static site generator that supports Markdown and reST syntax. Powered by Python.](https://github.com/getpelican/pelican#:~:text=,rich%20plugin%20ecosystem%3A%20Pelican%20Plugins)). This gives a near real-time preview of the article in the context of the actual theme/template. For quick iteration on a single page, Pelican’s incremental build will detect only *my-article* has changed and regenerate just that page, making the feedback loop quick. VS Code can also preview Markdown, but using Pelican’s server ensures the content is seen with the final site’s styling and layout. 

## Wiki-Style Internal Linking & Backlinks  
To interconnect notes in wiki fashion, we enable **[[Wiki-Style]] linking** in Markdown. Pelican has a community plugin called **Wikilinks** that automatically converts `[[Page Name]]` syntax into proper hyperlinks between pages ([GitHub - minchinweb/minchin.pelican.plugins.wikilinks: Support Wikilinks when generating Pelican sites](https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks/#:~:text=Usage%20Notes)). For example, writing `We build on ideas from [[My Data Science Journey]]` in another article will link to the “My Data Science Journey” page (resolving to its slug or filename). The Wikilinks plugin supports optional display text (e.g. `[[Page Name|custom text]]`) ([GitHub - minchinweb/minchin.pelican.plugins.wikilinks: Support Wikilinks when generating Pelican sites](https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks/#:~:text=Usage%20Notes)). Under the hood, it scans for `[[...]]` patterns after markdown processing and replaces them with `<a>` links to the target page’s URL ([GitHub - minchinweb/minchin.pelican.plugins.wikilinks: Support Wikilinks when generating Pelican sites](https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks/#:~:text=In%20basic%20usage%2C%20this%20allow,is%20finished)). This makes cross-referencing content as easy as in tools like Obsidian or Roam. (We will enforce unique filenames for notes to avoid ambiguous links ([GitHub - minchinweb/minchin.pelican.plugins.wikilinks: Support Wikilinks when generating Pelican sites](https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks/#:~:text=Known%20Issues)).) 

**Backlinks:** To achieve bi-directional linking (seeing what links back to a page), we can create a custom Pelican plugin or utilize the site’s metadata. During the build, we can collect all the wiki link references: e.g. maintain a dictionary mapping each target page to a list of pages that mentioned it. Then extend Pelican’s article context to include a “backlinks” list for each article. Finally, in the article template, if backlinks exist, render a section “**Linked from:** …” listing those referring pages. This requires a custom plugin that hooks into Pelican’s generation phase (using signals like `article_generator_finalized`) to gather links and inject the data. The effort is manageable given Pelican’s plugin API (Python hooks), and ensures every page ends with a list of other notes that link to it, reinforcing the wiki-like navigation. If writing a plugin from scratch, we’d parse each article’s HTML (or use the internal link map from the Wikilinks plugin) to identify outgoing `href`s pointing inside the site, then invert that mapping. 

Pelican’s standard linking syntax (`{filename}target.md`) could also be used for internal links ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=the%20other%20content%20will%20be,placed%20after%20site%20generation)) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=,filename%7D%2Farticle2.md)), but the wiki-style is more intuitive for a digital garden workflow. With the Wikilinks plugin and a backlinks plugin, the site will have **fully connected pages** with automatic references. 

## Custom Content Types & Templates  
One strength of Pelican is its flexible metadata and templating, which we leverage to define **custom article types** like `RECIPE` or `TRIP`. All Markdown files can include arbitrary front-matter fields (as long as they don’t conflict with reserved keywords) ([Writing content — Pelican 4.7.2 documentation](https://docs.getpelican.com/en/4.7.2/content.html#file-metadata#:~:text=This%20is%20the%20content%20of,my%20super%20blog%20post)) ([Writing content — Pelican 4.7.2 documentation](https://docs.getpelican.com/en/4.7.2/content.html#file-metadata#:~:text=,false)). We define a metadata field `Type` (or use a tag/category) to denote the content type, and add any custom fields needed. For example, a recipe might have: 

```markdown
Title: Chocolate Chip Cookies  
Date: 2025-03-01  
Type: recipe  
Servings: 4  
Prep_Time: 15 min  
Cook_Time: 10 min  
Ingredients: 
  - Flour 
  - Sugar 
  - Chocolate chips 
Steps: 
  1. Preheat oven…  
  2. Mix ingredients…  
Template: recipe  <!-- use a custom Jinja template -->
```

In this case, we set `Template: recipe` which tells Pelican to render this page with `recipe.html` instead of the default template ([Writing content — Pelican 4.7.2 documentation](https://docs.getpelican.com/en/4.7.2/content.html#file-metadata#:~:text=match%20at%20L131%20,to%20use%20for%20this%20article%2Fpage)). We will create separate Jinja2 templates (e.g., `recipe.html`, `trip.html`) in the theme. These templates extend the base layout but present the content in a specialized way. For instance, **`recipe.html`** can format the Ingredients list as a checklist, show Prep/Cook time in a sidebar, etc., whereas **`trip.html`** might display location info, dates, and an image gallery differently. Pelican will pass all front-matter fields into the template context, so fields like `Ingredients` or `Location` become accessible variables. We can thus iterate over `recipe.ingredients` in Jinja to output an HTML list, for example. This approach gives us **structured content** without needing a database – essentially a lightweight CMS defined via markdown metadata. 

Pelican’s flexibility here means we can support any number of content types. If needed, we could also write a Pelican plugin to validate that required fields are present for each type (ensuring, say, every `Type: recipe` file has an Ingredients list) or even generate additional pages (e.g., an index of all recipes). But even without extra plugins, using Jinja templates keyed on a metadata flag is sufficient and keeps things simple. 

## Beautiful Theming (Ghost-Inspired Design)  
We want the site to look modern and polished – more like a blog or magazine than a raw wiki. Pelican supports theming with Jinja2 templates and static CSS, allowing full control over design ([GitHub - getpelican/pelican: Static site generator that supports Markdown and reST syntax. Powered by Python.](https://github.com/getpelican/pelican#:~:text=,rich%20plugin%20ecosystem%3A%20Pelican%20Plugins)). We can start from an existing **Ghost-inspired theme** for Pelican to save time. For example, the *Casper* theme (Ghost’s default) has been ported to Pelican as **Casper2Pelican** ([GitHub - abr4xas/Casper2Pelican: The default personal blogging theme for pelican](https://github.com/abr4xas/Casper2Pelican#:~:text=Casper2Pelican)), and others like *Nicholas* or *Ghastly* offer clean Ghost-like aesthetics. These themes feature modern typography, responsive layout, and support for cover images and author profiles. The Casper2Pelican README notes it’s based on Ghost’s default and even supports author bios, social sharing, and header images via metadata ([GitHub - abr4xas/Casper2Pelican: The default personal blogging theme for pelican](https://github.com/abr4xas/Casper2Pelican#:~:text=,and%20share%20buttons%20on%20article)). Using such a theme (or a similar Pelican theme) gives us a head start with a **beautiful design** consistent with popular blogs. 

We can customize the theme further to match our vision. This might include: 
- **Header images** for articles: e.g. using a metadata field `Image: path/to/cover.jpg` which the template uses as a banner at the top of a post (Casper2Pelican already checks an `image` field for header image ([GitHub - abr4xas/Casper2Pelican: The default personal blogging theme for pelican](https://github.com/abr4xas/Casper2Pelican#:~:text=,and%20share%20buttons%20on%20article))). 
- **Navigation and Home Page:** We’ll create a custom home page instead of a simple blog index. For instance, design a welcome page (`content/pages/home.md`) with an overview and featured posts. Using Pelican’s pages feature, we set `SAVE_AS = 'index.html'` for that page so it becomes the landing page. The normal blog index (listing latest notes) can be generated at `/archive/` or a different URL. 
- **CSS Framework:** Optionally, incorporate a modern CSS framework or utility library (e.g. Tailwind or Bootstrap) to easily achieve a clean look for elements like tables, code blocks, callouts, etc., if the chosen theme doesn’t already handle it. Many Pelican themes use Bootstrap 4/5 or pure CSS. We should ensure the styling for wiki link references and backlinks section is cohesive (e.g., backlinks as a small italicized list at bottom). 
- **Mobile-friendly design:** The theme should be responsive; Ghost-based themes typically are. We’ll verify that navigation (category lists, tag pages) collapses nicely on mobile. 

By leveraging an existing theme and tweaking it, we meet the requirement of a **“beautiful design inspired by modern blogs”**. Pelican’s theme system separates content from presentation, so we can iterate on the look independently. The end result won’t feel like a bare-bones dev wiki – instead, it will have polished typography, spacing, and visuals similar to a Ghost blog (as evidenced by the Casper2Pelican screenshot and demo blogs ([GitHub - abr4xas/Casper2Pelican: The default personal blogging theme for pelican](https://github.com/abr4xas/Casper2Pelican#:~:text=Demo))). 

## Multi-Language Support & AI Translations  
The digital garden will be **multilingual**, serving content in (for example) English and Spanish. Pelican, with the **`i18n_subsites`** plugin, can generate a multi-language site where each language is a sub-site. We organize content by language – e.g. `content/en/...` and `content/es/...` – or include a `Lang` metadata on each file. Pelican’s multi-language support allows each article to have translated counterparts identified by the same slug and a `lang` code ([Writing content — Pelican 4.7.2 documentation](https://docs.getpelican.com/en/4.7.2/content.html#file-metadata#:~:text=,without%20extension)). At build time, the i18n plugin produces separate output folders for each language (or language-specific paths) and can generate a language switcher. The Pelican docs highlight *“publication of articles in multiple languages”* as a core feature ([GitHub - getpelican/pelican: Static site generator that supports Markdown and reST syntax. Powered by Python.](https://github.com/getpelican/pelican#:~:text=,rich%20plugin%20ecosystem%3A%20Pelican%20Plugins)). In practice, you might have `my-article.en.md` and `my-article.es.md`. If a translation is missing, Pelican can default to the original or we can configure fallback behavior.

**Auto-fill with AI:** To meet the requirement of filling untranslated content using AI, we introduce a **translation pipeline step**. This would run *before* or *during* the build. For any article that lacks a manual translation, a script can automatically generate one via an AI translation service. For example, we could use a translation API (like DeepL or Google Cloud Translate) or an AI model (like GPT-4) through their Python SDKs to translate English Markdown to Spanish Markdown. The build workflow could be:
1. Detect articles that exist in English but not in Spanish (perhaps by scanning the `content/en` vs `content/es` directories).
2. For each missing translation, call the AI API to produce a translated Markdown text. Preserve the front matter (with `lang: es` and a note that it’s auto-generated) and have the body translated. 
3. Save these generated files in `content/es/...` so that Pelican includes them in the site generation. Optionally mark them with a flag (e.g. `Translation: machine`) that the template can use to display a disclaimer banner like “🤖 This is an AI-translated version; it may contain errors.” 

Because this process can be time-consuming or cost API usage, we’d integrate it as an optional step (only generate if the file isn’t already there, and possibly commit the result to the repo so it’s reused). This way, untranslated content is automatically populated, ensuring the Spanish site is never missing a page – it will either have a human-written translation or an AI-provided one. 

Pelican’s i18n plugin will link between language versions of each page (it adds link rel="alternate" and allows template language switchers). We can thus have a language toggle on each page. Users will see a fully bilingual site, largely maintained by writing primarily in one language and letting AI assist with the other. 

All tools here are Python-friendly: Pelican’s plugin is Python, and calling an AI translation (via requests or an SDK) is straightforward to script. This setup future-proofs the site – content creators can focus on one language, and AI can help keep other languages up-to-date. 

## Content Access Control (Roles & Authentication)  
Even though the site is static, we need **access roles** for certain content (public vs friends/family vs private drafts). We can handle this by a combination of build-time filtering and client-side authentication using Auth0. 

**Drafts & Unlisted Posts:** Pelican supports a `Status` metadata. If we mark an article `Status: draft`, Pelican will not publish it (by default ([Writing content — Pelican 4.7.2 documentation](https://docs.getpelican.com/en/4.7.2/content.html#file-metadata#:~:text=,without%20extension)) ([Writing content — Pelican 4.7.2 documentation](https://docs.getpelican.com/en/4.7.2/content.html#file-metadata#:~:text=If%20your%20articles%20should%20be,include%20the%20status%20in%20the))】, so drafts remain excluded from the generated site. For “friends/family” posts that are finished but should not be public, we can use Pelican’s `hidden` status (or simply exclude them from indexes). A `Status: hidden` post *is* generated as an HTML page but is omitted from feeds and listing ([Writing content — Pelican 4.7.2 documentation](https://docs.getpelican.com/en/4.7.2/content.html#file-metadata#:~:text=on%20the%20index%20page%20nor,any%20category%20or%20tag%20page))】. This creates an **unlisted page** – only accessible if you know the URL. We can distribute those URLs privately. This provides basic obscurity but not true security. 

For stronger protection, we integrate **Auth0 authentication** into the static site. At build time, we decide which pages require login. For example, we might add a metadata flag `Visibility: friends` or `auth_required: true` for pages that should only be seen by certain users. The build process can then inject an Auth0 login gate into those pages. Concretely, we can create a Jinja template snippet that includes the Auth0 JavaScript SDK and a script to enforce login. Each protected page, when rendered, would contain something like: 

```html
<div id="protected-content"> ... full content ... </div>
<script src="https://cdn.auth0.com/js/auth0-spa-js/1.XX/auth0-spa.min.js"></script>
<script>
  // Initialize Auth0 client
  const auth0 = await createAuth0Client({ domain: "YOUR_DOMAIN", client_id: "YOUR_CLIENTID", cacheLocation: 'localstorage' });
  const isAuthenticated = await auth0.isAuthenticated();
  if(!isAuthenticated) {
    document.getElementById('protected-content').style.display = 'none';
    // Show a login button or auto-login:
    await auth0.loginWithRedirect();
  } else {
    document.getElementById('protected-content').style.display = 'block';
  }
</script>
```

This is a sketch, but the idea is the page will require an Auth0 login before showing content. Auth0 will handle the login redirect and token management (the Auth0 SPA SDK is used as shown in Auth0’s Gatsby exampl ([How to Secure GatsbyJS Sites with Auth0 for Authentication](https://auth0.com/blog/securing-gatsby-with-auth0/#:~:text=How%20to%20Secure%20GatsbyJS%20Sites,management%20on%20a%20GatsbyJS)) ([How to Secure GatsbyJS Sites with Auth0 for Authentication](https://auth0.com/blog/securing-gatsby-with-auth0/#:~:text=How%20to%20Secure%20GatsbyJS%20Sites,management%20on%20a%20GatsbyJS))】). At build-time we embed the Auth0 credentials (domain, client ID) which are not sensitive. We do **not** include any secret keys in the static code. After login, the content div becomes visible. 

**Role-Based Access:** Auth0 supports role claims in token ([Manage Role-Based Access Control Roles - Auth0](https://auth0.com/docs/manage-users/access-control/configure-core-rbac/roles#:~:text=We%20provide%20various%20functions%20to,or%20the%20Auth0%20Management%20API))】. If we want to distinguish “friends and family” vs “editors”, we can assign roles in Auth0 (e.g., a user role “family” or an allowed email list). The front-end script can then query the user’s profile/claims after login and decide whether to show the page. For example, a page for “family” could check `if(user.roles.includes('family')) { show content } else { hide and show "Access Denied" }`. This check is done client-side with the data from Auth0. While not foolproof (since the HTML is technically delivered), we could also choose not to even deploy certain files publicly. Another approach is to generate two versions of the site: one public (excluding private pages entirely) and one for authenticated use. However, since the requirement is static hosting on GitHub Pages (which doesn’t support server-side auth), using Auth0’s client-side gating is a practical solutio ([Protecting Static Website using Auth0 but using existing users - Auth0 Community](https://community.auth0.com/t/protecting-static-website-using-auth0-but-using-existing-users/76359#:~:text=Hello,Auth0%20JavaScript%20SDK%20Quickstarts%3A%20Login))】. 

In summary, public content will be generated normally and listed on the site. Private content will either be hidden from listings or not present at all in the public build. If hidden but present, they will have Auth0 code embedded to ensure only authorized users can easily view them. This setup turns the static site into a pseudo-protected site. It’s important to note that truly secure content shouldn’t be published to public servers at all – for highly sensitive info, one might maintain it in a private repo or use a hosting service with access control. But for “friends/family” level privacy, this approach (unlisted pages + Auth0 login on the front-end) is sufficient and commonly used. Auth0’s documentation and quickstarts will guide the integration of their SPA SDK into our static pages, making the process straightforward. 

## Tags, Indexes, and Navigation Pages  
We will support **multiple index pages** to help discover content: by tag, by category, by popularity, etc. Pelican automatically creates index pages for **tags and categories**. Each tag will get a page listing all articles with that tag (Pelican’s templates and generators handle this if enabled). Same for categories (and with our nested scheme, categories like “data_science” under “tech/dev” will show all related posts). We’ll ensure the theme includes pages for tags/categories in the navigation or as part of a sitemap. 

For a **“Most Read”** page, since the site is static, we need to gather view statistics from an external source. One option is to use an analytics service (like Google Analytics or Plausible) on the site, then periodically retrieve pageview counts. We can incorporate a JSON of page view stats (keyed by URL or slug) and have a build step to sort articles by views and generate a page of “Top 10 most read articles.” This would be a custom script that runs before site generation to update a data file (or we use Pelican’s [`READERS` or data files plugin] to ingest a CSV/JSON). Alternatively, if we don’t have analytics integration, we might define "most read" manually or by other metrics (like an editorial choice or proxy like time since posted). But assuming we have GA, we could use Google Analytics Reporting API via Python to get the most viewed URLs and then produce a static page listing those (with links and maybe view counts). 

We also plan a **handcrafted home page** as mentioned earlier. This will likely be a static page (written in Markdown for convenience) that is set as the landing page. We can curate content here – e.g., a welcome message, featured posts in different categories, etc. Because Pelican allows creating arbitrary pages (any file under `content/pages/` by default) and does not force the blog index to be the root, we can completely customize the homepage. For example, the homepage could even be written as a Jinja template itself if we want dynamic content (Pelican allows creating templates for pages). But simpler, we can hardcode or use shortcodes for pulling in snippets (Pelican plugins exist for including content or defining shortcodes). 

**Navigation:** The site will have a menu (likely in the header) linking to key index pages: e.g. *Blog*, *Categories*, *Tags*, *About*, *Languages*. We will enable Pelican’s `DISPLAY_PAGES_ON_MENU` and `DISPLAY_CATEGORIES_ON_MENU` settings as needed, or manually define a menu in config for finer control. The Ghost-based theme we use might already support a configurable menu. We’ll include a link to the “All Tags” page and maybe a link to “All Posts” archive. If the site becomes large, we could add a search functionality; Pelican has a plugin for search that works by building a JSON index used by a JS script (for example, **Tipue Search** plugin or `pelican-search` which provides Lunr.js searc ([Adding Search to my Pelican Blog Site | Stanley Solutions Blog](https://blog.stanleysolutionsnw.com/adding-search-to-my-pelican-blog-site.html#:~:text=Adding%20Search%20to%20my%20Pelican,based%20system))】). That would add a small JS (still lightweight) to enable full-text search on the client side, which is a nice enhancement for a digital garden. (This is optional but worth noting since gardens benefit from search.) 

## Build Pipeline & Link Validation  
To tie everything together, we’ll set up a robust **build pipeline** (e.g., using GitHub Actions or similar CI) to automate site generation, validation, and deployment to GitHub Pages. The stages would include: 

1. **Generate Site:** Use Pelican to build the site. This involves installing the Python dependencies (Pelican and required plugins like `pelican-i18n_subsites`, `pelican-wikilinks`, etc., all available via pip), then running `pelican content -o output -s pelicanconf.py` (and possibly once per language if using i18n plugin in a certain way). The Pelican config will include all our settings (paths, plugins, theme, etc.). 

2. **Validate Internal Links:** After generation, we perform a link check focusing on internal links. We want to catch any broken references (especially from the wiki links or manual links). We can use an automated link checker – for example, a tool like **LinkChecker** (Python) or `html-proofer`. A Python approach could be writing a small script that parses all output HTML files and verifies that every `<a href>` pointing to the same domain has a corresponding file. Since we have the list of output files, we can map URLs to files easily. Another approach is to use Pelican’s own link mapping: the Wikilinks plugin might warn if a target is missing. If not, our custom backlink plugin could also log missing targets. In any case, the CI can run a script to ensure no 404s for internal hyperlinks. If a broken link is found, the build should fail, alerting us to fix the reference or add the missing page. This step addresses the requirement of a **build stage validating internal links** – essential in a wiki-like garden where content moves and many cross-links exist. 

3. **Deploy to GitHub Pages:** Once the site passes checks, the pipeline can deploy it. For GitHub Pages, that typically means pushing the `output/` (static files) to the `gh-pages` branch or the `docs/` folder of the repository. We can use a GH Action for this, or even GitHub Pages’ native static publishing if we keep the output in `docs/`. The deployment must include all language versions (possibly in subfolders like `en/` and `es/` if configured) and all static assets. Since everything is static, deployment is as simple as uploading the files – no server-side logic needed. 

4. **(Optional) Post-deploy Tasks:** If using analytics for “most read” or if we want to purge a CDN cache, etc., those could be additional steps. But not strictly necessary for core functionality. 

**Actively Maintained Tools:** All components in this stack are widely used and maintained. Pelican is a mature project (10k+ stars on GitHub, active as of 2025 ([pelican for professional website : r/django - Reddit](https://www.reddit.com/r/django/comments/oxuxg1/pelican_for_professional_website/#:~:text=pelican%20for%20professional%20website%20%3A,is%2C%20what%20is%20your))】, and its plugins (like Wikilinks and i18n) are actively kept up-to-date with Pelican release ([GitHub - minchinweb/minchin.pelican.plugins.wikilinks: Support Wikilinks when generating Pelican sites](https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks/#:~:text=Further%20configuration%20will%20depend%20on,file))】. Auth0 is a reliable commercial platform with extensive documentation and support for SPA integration. Any AI translation step can utilize stable APIs (Google Translate, DeepL) or libraries. By using established tools, we ensure longevity and community support. 

## Summary of the Recommended Stack  
- **Pelican (Python Static Site Generator)** – Core engine for markdown-to-HTML, multi-language output, theming, and plugin ([GitHub - getpelican/pelican: Static site generator that supports Markdown and reST syntax. Powered by Python.](https://github.com/getpelican/pelican#:~:text=,rich%20plugin%20ecosystem%3A%20Pelican%20Plugins))】.  
- **Content Structure:** Markdown files in a nested directory hierarchy, one article per folder with associated images/docs, using Pelican’s attach mechanism for bundling asset ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=Starting%20with%20Pelican%203,sibling%20of%20the%20linking%20document)) ([Writing content - PELICAN 4.11.0](https://docs.getpelican.com/en/latest/content.html#:~:text=%21%5BIcon%5D%28))】.  
- **Pelican Plugins:** 
  - *Wikilinks* for `[[wiki-style]]` link syntax between page ([GitHub - minchinweb/minchin.pelican.plugins.wikilinks: Support Wikilinks when generating Pelican sites](https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks/#:~:text=Usage%20Notes))】. 
  - *i18n_subsites* for multi-language site generation (creating language-specific versions of the site ([[Pelican] Translate String According to Default Language in Theme](https://siongui.github.io/2017/01/07/pelican-translate-string-according-to-default-language-in-theme/#:~:text=Pelican%20static%20site%20generator%20and,macro%20to%20achieve%20this%20goal))】. 
  - *Neighbors* (if using a theme that requires it) to get next/previous article links easil ([GitHub - abr4xas/Casper2Pelican: The default personal blogging theme for pelican](https://github.com/abr4xas/Casper2Pelican#:~:text=Abr4xas%2C%20amendments%20by%20Colin%20Wren))】. 
  - *Tipue Search or similar* (optional) for client-side search functionalit ([Adding Search to my Pelican Blog Site | Stanley Solutions Blog](https://blog.stanleysolutionsnw.com/adding-search-to-my-pelican-blog-site.html#:~:text=Adding%20Search%20to%20my%20Pelican,based%20system))】. 
  - Custom plugins for backlink aggregation and any additional validation or content processing (AI translation insertion could also be done here or in CI). 
- **Templates/Theming:** A responsive theme inspired by Ghost’s **Casper** (e.g. Casper2Pelica ([GitHub - abr4xas/Casper2Pelican: The default personal blogging theme for pelican](https://github.com/abr4xas/Casper2Pelican#:~:text=Casper2Pelican))】 or another port) to provide a clean, modern UI. We will customize templates for special content types (recipes, trips) using Pelican’s template override featur ([Writing content — Pelican 4.7.2 documentation](https://docs.getpelican.com/en/4.7.2/content.html#file-metadata#:~:text=match%20at%20L131%20,to%20use%20for%20this%20article%2Fpage))】 and front-matter metadata, and include visual enhancements (cover images, syntax highlighting for code, etc.). The design will emphasize readability and aesthetics, avoiding a technical look. 
- **Authentication:** Auth0 SPA integration for protected sections. We do this by embedding Auth0’s JS and gating logic in pages marked as non-public. Auth0 manages the user accounts and login dialogs (e.g., via Google OAuth or email/password as configured), and the static site just includes the necessary scripts. This adds a slight JS dependency on those pages, but only for the sake of auth – the overall site remains static and content-focused. 
- **Build/Deployment Pipeline:** Use GitHub Actions (or similar CI) to run the build. The pipeline will run Pelican, run a **link checker** to validate all internal references (preventing broken links in the graph), and then deploy to GitHub Pages. Content translations via AI can be automated in this pipeline as well, ensuring the latest content is available in all languages. 

By combining these technologies, we get a **robust, customizable, and beautiful digital garden system** that meets all the listed requirements. All major components are Python-based (Pelican, plugins, build scripts), aligning with the preference for Python tooling. The architecture leverages static site best practices (pre-render everything for speed and simplicit ([GitHub - getpelican/pelican: Static site generator that supports Markdown and reST syntax. Powered by Python.](https://github.com/getpelican/pelican#:~:text=With%20Pelican%2C%20you%20can%20create,web%20server%20or%20hosting%20service)) ([GitHub - getpelican/pelican: Static site generator that supports Markdown and reST syntax. Powered by Python.](https://github.com/getpelican/pelican#:~:text=,is%20simple%20to%20host%20anywhere))】) while layering on advanced features like backlinks, full-text search, and role-based access that are often missing from simpler static blogs. The result is a personal knowledge garden that is easy to write in (just Markdown in VSCode), easy to maintain (thanks to automation and plugin support), and delightful for readers in terms of appearance and navigation. 

**References:** The selection of Pelican is supported by its official docs and community plugins, which confirm it can handle multi-language content, Markdown, and is extensibl ([GitHub - getpelican/pelican: Static site generator that supports Markdown and reST syntax. Powered by Python.](https://github.com/getpelican/pelican#:~:text=,rich%20plugin%20ecosystem%3A%20Pelican%20Plugins)) ([GitHub - minchinweb/minchin.pelican.plugins.wikilinks: Support Wikilinks when generating Pelican sites](https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks/#:~:text=Usage%20Notes))】. The Ghost-inspired design is facilitated by existing Pelican themes (e.g., Casper2Pelican) which explicitly aims to bring Ghost’s default look to Pelica ([GitHub - abr4xas/Casper2Pelican: The default personal blogging theme for pelican](https://github.com/abr4xas/Casper2Pelican#:~:text=Casper2Pelican))】. Auth0 integration for static sites is a known approach (Auth0 provides SPA SDKs and guides for static site authentication flow ([Protecting Static Website using Auth0 but using existing users - Auth0 Community](https://community.auth0.com/t/protecting-static-website-using-auth0-but-using-existing-users/76359#:~:text=Hello,Auth0%20JavaScript%20SDK%20Quickstarts%3A%20Login))】). All these pieces together form a cohesive stack to realize the envisioned digital garden.

# Follow up questions

While ponderimg (and soon testing) the suggested solution, some more questions came up to me.

## Changing the structure

- How does the system behave when I move an article feom one location of the tree to another?
- How does the system behave when I rename an article?
- How does the system behave when I delete an article?
- How does the system behave when I rename a folder?
- How does the system behave when I delete a folder?

## Articles or Pages?

From the [Pelican documentation](https://docs.getpelican.com/en/latest/content.html):

>Pelican considers “articles” to be chronological content, such as posts on a blog, and thus associated with a date.
The idea behind “pages” is that they are usually not temporal in nature and are used for content that does not change very often (e.g., “About” or “Contact” pages).

So what should **my** articles be? In my article concept the date is not too important. But maybe the workflow to edit Pelican articles is easier than the one to edit pages?

# Playing around

So I create a [github repo](https://github.com/tillg/playground_pelican) and start playimng around.
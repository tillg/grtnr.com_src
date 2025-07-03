# TODO

This file collects planned features and improvements for the grtnr.com website.

[TOC]

## Automatically translate articled

- Articles should be translated automatically by an AI service
- The original language of the article is identified by an AI service too
-

### Architecture

We will build a service `translate` that gets a markdown text, a `original-language` code and a `target-language` code. It returns the translation as markdown.

We will keep translations once created and only re-translate (or translate for the first time), if the original markdown has been modified. To this end we keep track of the hash of the to-be-translated markdown file.

The translation service is completely encapsulated. It can be tested on it's own, we can have different implementations that use different backend services.

### File organization

The interim artefacts are always to be seen in context of an article or a page, a recipe or similar. They should be stored in git, but still be easily identied as automatically created artefacts.

Therefore we will use the following directory structure:

```text
content/
	articles/
		2025-07-03-something-interesting/
			2025-07-03-something-interesting.md
			extensions/
				2025-07-03-something-interesting-DE.md
				2025-07-03-something-interesting-FR.md
				2025-07-03-something-interesting-SUMMARY.md
				2025-07-03-something-interesting-IMAGE-TAGS.csv
```

Every `md` file in the `extensions` will have a frontmatter that contains data used to decide on wether the text is still valid or needs to be re-generated:

```text
---
last-created: 2025-07-03-16:25:10
hash-on-last-created: xyz
---
```

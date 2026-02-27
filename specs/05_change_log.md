# Change Log

## Goal

Add a change log page to the site that gives visitors a human-readable timeline of what
changed and when. The log is a regular content page (auto-translated like any other page),
maintained in English, ordered oldest-first.

## How It Works

1. A page at `content/pages/changelog/changelog.md` holds the full change log
2. Each entry is a date heading followed by a short, plain-language summary
3. For the initial version, entries are derived from the git commit history — many
   technical commits are collapsed into single meaningful lines
4. Going forward, every commit updates the change log if the changes are user-visible

---

## Decisions

### Format

Simple markdown list grouped by date. Multiple changes on the same day share one date
heading. Entries read like release notes for a human visitor, not a developer.

```markdown
### 2026-02-14

- Replace Pelican with garten, a custom static site generator
- Improve link checking with lychee
```

### Ordering

Oldest entries at the top, newest at the bottom. Visitors scroll down to see what's new.

### Language

The source file is English. The automatic translation system translates it to German and
French like any other page.

### Maintenance

CLAUDE.md includes guidance that the change log should be reviewed and potentially
extended with every commit. Only user-visible changes need an entry — internal refactors,
CI tweaks, and translation regeneration commits do not.

### Content Scope

The change log covers site features and notable content additions. It does not list every
individual article — visitors can see those on the index page. Entries like "Add search"
or "Add multilingual support" belong here. "Published article about X" only belongs here
if it's a notable milestone (e.g. the first article, or a batch import).

---

## Scope of Changes

### 1. `content/pages/changelog/changelog.md` — New page

Create the change log page with entries derived from the full git history. The initial
content covers 2022-08-08 through today.

**Frontmatter:**

```yaml
---
date: 2022-08-08
layout: page
title: Change Log
status: published
---
```

**Initial entries (derived from git history):**

```markdown
### 2022-08-08

- Launch site on GitHub Pages with Jekyll

### 2022-08-25

- Switch to Hydejack theme
- Add link checking to the build process

### 2022-08-27

- Add recipes section with dedicated layout
- Set up Google Analytics

### 2022-08-28

- Organize images next to their content files instead of a shared assets folder

### 2023-03-11

- Import content from tillgartner.de

### 2023-05-07

- Add AI Chat web app

### 2024-03-12

- Import older articles (JavaScript, D3, static site generators, and more)

### 2024-04-08

- Add JupyterLab installation guide

### 2024-11-27

- Upgrade build system to Ruby 3.3
- Write about Jekyll theme evaluation

### 2025-07-04

- Add AI-powered automatic translation (English, German, French)

### 2025-07-09

- Launch multilingual site with language switcher

### 2025-08-03

- Start SwiftUI cheatsheet series

### 2026-02-04

- Add Claude Code to the development workflow

### 2026-02-14

- Replace Pelican with garten, a custom Python static site generator
- Improve link checking with lychee
- Add daily production link checks

### 2026-02-26

- Add article about Peoplez

### 2026-02-27

- Add SEO meta tags (Open Graph, Twitter Cards, JSON-LD)
- Add hero images and excerpts to all articles
- Improve automatic translations (parallel processing, Du-form for German)
- Add client-side search with Pagefind
```

### 2. `CLAUDE.md` — Add change log maintenance guidance

Add a section to CLAUDE.md explaining when and how to update the change log during
commits.

### 3. `menu_translations.json` — Add "Change Log" entry

Add translations for the menu item if the changelog is linked from navigation. Otherwise
skip — visitors find it via the existing page listing.

---

## Implementation Plan

1. Create `content/pages/changelog/changelog.md` with frontmatter and initial entries
2. Add change log maintenance guidance to CLAUDE.md
3. Run `inv render` to verify it builds without errors
4. Verify the page appears in the site output

---

## Verification

```bash
inv render
# Check the page exists in output
cat output/changelog/index.html | head -20
# Verify translations are generated
ls output/en/changelog/ output/de/changelog/ output/fr/changelog/
```

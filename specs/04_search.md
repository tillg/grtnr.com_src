# Client-Side Search

## Goal

Add full-text search to the site so visitors can find articles, pages, and recipes by
typing keywords. Everything runs in the browser — no server or API required.

## How It Works

1. At build time, generate a search index from the rendered HTML output
2. Include a small search library and UI on a dedicated search page
3. When the user types a query, JavaScript searches the index and shows results instantly

---

## Decisions

### Tool: Pagefind

Use [Pagefind](https://pagefind.app/). It scans the rendered HTML in `output/`, generates
a compact binary index split into chunks, and writes everything to `output/pagefind/`.
The browser lazy-loads only the index chunks needed for each query.

```bash
npx pagefind --site output
```

### Pipeline Integration

Add a `search_index` invoke task. Wire it into `build()` and `preview()` between the
pipeline and link checking. Does not run during `livereload` — search is a production
feature, not needed during content editing. To test search locally, use
`inv build && inv serve`.

```
build() / preview():  _run_garten_pipeline() → search_index() → check_links()
livereload():         _run_garten_pipeline()  (no search index, keeps rebuilds fast)
```

CI gets search indexing for free since `publish.yml` runs `inv build`.

### UI Approach: Dedicated Search Page with Pagefind UI

Use Pagefind's built-in search UI component on a dedicated search page. The search page
loads Pagefind's CSS and JS — they are **not** loaded on every page. Override Pagefind's
CSS to match the site's Lanyon theme (colors, fonts, spacing).

The entry point is a magnifying glass (loupe) icon in the masthead, next to the language
globe. It is a simple `<a>` link — no JavaScript widget or modal.

### Placement: Loupe Icon in Masthead + Dedicated Search Page

Add a magnifying glass icon to the masthead, positioned left of the language globe. Clicking
it navigates to a per-language search page (`/{lang}/search/`). This keeps the entry point
visible on all pages while giving search results a full-page layout.

The loupe icon follows the same visual pattern as the `.language-globe-btn`: a circular
button with an SVG icon, hover effects, and responsive sizing. Both icons are wrapped in a
shared `.masthead-icons` container for consistent layout.

### Multilingual Behavior

Pagefind supports multilingual indexing via the `lang` attribute on the `<html>` tag.
Each language version of the site is already rendered with the correct `lang` attribute.
Pagefind will automatically scope search results to the current language.

The base template currently has `<html lang="{{ LANG or DEFAULT_LANG }}">` with
`current_language` only in a `data-lang` attribute. Pagefind reads `lang`, not `data-lang`,
so the `lang` attribute must be changed to use `current_language` for per-page scoping.

### Content Scoping

By default Pagefind indexes everything inside `<body>`. Use `data-pagefind-body` on the
main content area to limit indexing to article/page content. The sidebar, nav, footer,
language switcher, and comments (client-side rendered via giscus) are all outside this
container and automatically excluded.

---

## Scope of Changes

### 1. `tasks.py` — Add `search_index` task and wire into build

Add a new invoke task that runs Pagefind via `npx` (no `package.json` needed — the
project already uses `npx` for prettier and markdownlint):

```python
@task
def search_index(c):
    """Generate search index with Pagefind."""
    c.run("npx pagefind --site output")
```

Wire into `build()` and `preview()` between pipeline and link checking:

```python
@task
def build(c):
    _run_garten_pipeline()
    search_index(c)
    check_links(c)
```

### 2. `theme/pelicanyan/templates/base.html` — Fix `lang` attribute

Change the existing `<html>` tag's `lang` attribute from `{{ LANG or DEFAULT_LANG }}` to
`{{ current_language or DEFAULT_LANG }}` so it reflects the per-page language:

```html
<html lang="{{ current_language or DEFAULT_LANG }}"{% if current_language %} data-lang="{{ current_language }}"{% endif %}>
```

This enables Pagefind's multilingual filtering.

### 3. `theme/pelicanyan/templates/base.html` — Content scoping

Add `data-pagefind-body` to the main content container so only article/page content is
indexed (not the sidebar, nav, or footer):

```html
<div class="container content" data-pagefind-body>
  {% block content %}{% endblock %}
</div>
```

### 4. `theme/pelicanyan/templates/base.html` — Add loupe icon to masthead

Add a magnifying glass icon in the masthead area, left of the language globe. Wrap both
icons in a `.masthead-icons` container:

```html
<div class="masthead-icons">
  <a href="{{ SITEURL }}/{{ current_language or 'en' }}/search/" class="search-icon-btn"
     aria-label="Search">
    <svg class="search-icon" viewBox="0 0 24 24" width="20" height="20"
         fill="none" stroke="currentColor" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
      <circle cx="11" cy="11" r="8"/>
      <line x1="21" y1="21" x2="16.65" y2="16.65"/>
    </svg>
  </a>
  {% if MULTILINGUAL_ENABLED %}
  <div class="language-switcher-top">
    <!-- existing globe button and language menu -->
  </div>
  {% endif %}
</div>
```

The `.masthead-icons` container replaces the current standalone
`.language-switcher-top` positioning. Both icons share the same absolute top-right
placement, laid out horizontally with flexbox.

### 5. `theme/pelicanyan/templates/search.html` — Dedicated search page

Create a new template extending `base.html`. It loads Pagefind assets and renders the
search UI container:

```html
{% extends "base.html" %}

{% block head %}
{{ super() }}
<link href="{{ SITEURL }}/pagefind/pagefind-ui.css" rel="stylesheet" />
{% endblock %}

{% block content %}
<h1>Search</h1>
<div id="search"></div>
{% endblock %}

{% block scripts %}
{{ super() }}
<script src="{{ SITEURL }}/pagefind/pagefind-ui.js"></script>
<script>
  new PagefindUI({ element: "#search", showSubResults: true });
</script>
{% endblock %}
```

Pagefind CSS and JS are only loaded on this page, not site-wide.

Note: `base.html` needs `{% block head %}` and `{% block scripts %}` extension points
if they don't already exist. Add them during implementation.

### 6. `garten/render.py` — Add `render_search_page()` function

Add a new function following the same pattern as `render_archives()`:

```python
def render_search_page(env, context, output_path):
    """Render the search page."""
    template = env.get_template("search.html")
    html = template.render(**context)
    search_dir = os.path.join(output_path, "search")
    os.makedirs(search_dir, exist_ok=True)
    write_file(os.path.join(search_dir, "index.html"), html)
```

Call it in two places:

- In the main render path (for `output/search/index.html`)
- In `_render_language()` for each language (for `output/{lang}/search/index.html`)

### 7. `theme/pelicanyan/static/css/styles.css` — Search styling

**Loupe icon styles** (matching the globe button pattern):

```css
/* Masthead icons container */
.masthead-icons {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 1000;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

/* Search icon button (matches .language-globe-btn) */
.search-icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  border-radius: 50%;
  transition: background-color 0.2s ease;
  color: #333;
  text-decoration: none;
}

.search-icon-btn:hover {
  background-color: rgba(0, 0, 0, 0.1);
  color: #268bd2;
  text-decoration: none;
}
```

**Search page styles:**

- Pagefind UI font overrides → PT Sans / PT Serif
- Input field styling → match site form elements
- Result link colors → match site link colors
- Responsive layout adjustments

**Update `.language-switcher-top`:**

Change from absolute positioning to `position: relative` since the parent
`.masthead-icons` container now handles the absolute positioning.

### 8. `lychee.toml` — Exclude Pagefind assets

Add Pagefind's generated files to lychee's exclude patterns so link checking doesn't
flag them:

```toml
exclude_path = ["output/pagefind"]
```

### 9. `.gitignore` — Ignore generated index

The Pagefind output (`output/pagefind/`) is already covered by ignoring `output/`, and
`node_modules/` is already in `.gitignore`. No changes needed.

### 10. CI workflow (`publish.yml`) — Add Node.js setup

Since `search_index` is wired into `build()`, CI gets Pagefind for free via `inv build` —
no separate step needed. However, `npx` requires Node.js. Add `actions/setup-node@v4`
before the build step:

```yaml
- name: Set up Node.js
  uses: actions/setup-node@v4
  with:
    node-version: "20"
```

---

## Implementation Plan

1. Change `<html lang>` attribute in base.html from `{{ LANG or DEFAULT_LANG }}` to
   `{{ current_language or DEFAULT_LANG }}`
2. Add `data-pagefind-body` to the content container in base.html
3. Add loupe icon to masthead in base.html (wrap with globe in `.masthead-icons`)
4. Create `search.html` template with Pagefind UI
5. Add `render_search_page()` to `render.py`, wire into main render + `_render_language`
6. Add CSS for loupe icon and search page styling in styles.css
7. Add `search_index` invoke task to tasks.py
8. Wire `search_index` into `build` and `preview` task chains
9. Add `setup-node` step to `publish.yml`
10. Update lychee.toml if needed
11. Test locally: `inv build && inv serve`
12. Verify multilingual search works (search in English → English results only)

---

## Verification

```bash
# Build (includes pipeline + search index + link check) and serve
inv build
inv serve

# Open localhost:8000, click the magnifying glass icon in the top-right
# Verify:
# - Loupe icon appears left of the language globe on all pages
# - Clicking the loupe navigates to /{lang}/search/
# - Search finds articles by title and content
# - Results link to the correct pages
# - Switching to /de/ and searching returns German results
# - Switching to /fr/ and searching returns French results
# - Search page matches the site's visual style
# - Pagefind assets are NOT loaded on non-search pages (check network tab)
```

## Future Enhancements (Out of Scope)

- **Search analytics** — Track what users search for
- **Keyboard shortcut** — `/` or `Ctrl+K` to focus search from any page
- **Filters** — Filter by tag, category, or date

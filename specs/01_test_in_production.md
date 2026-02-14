# Test in Production

## Goal

Verify the **live deployed site** (grtnr.com) actually works — pages load, links resolve, all languages are served.

## What We Already Have

The build pipeline runs `linkchecker` against the local `./output` directory, catching broken links **before** deployment (pre-commit hook, `inv build`, CI). This spec adds a **complementary** check that tests the real deployed site, and replaces `linkchecker` with `lychee` across the board.

## What We Verify

1. **Page availability** — All pages return HTTP 200 (not 404/500)
2. **Language coverage** — Language variant links in the generated pages resolve correctly (covered implicitly by lychee checking all links)
3. **Internal links** — Links within grtnr.com resolve correctly
4. **External links** — Links to external resources still work
5. **Response time** — Pages that take > 30 seconds fail via lychee's `timeout = 30` setting (binary pass/fail — no separate "slow page" reporting)

---

## Decisions

- **Tool:** Replace `linkchecker` with [`lychee`](https://github.com/lycheeverse/lychee) everywhere — both for the existing build-time check (local `./output`) and the new production check (live site). One tool, two modes.
- **Installation:** Each developer installs lychee locally (e.g., `brew install lychee` on macOS — documented in README.md). In CI, use the [`lycheeverse/lychee-action`](https://github.com/lycheeverse/lychee-action) GitHub Action.
- **Output:** Use lychee's native markdown output (`--format markdown`). Remove `check-links.sh` and `linkcheck-errors.txt`.
- **Schedule:** Daily scheduled GitHub Action (cron).
- **Target:** Only `grtnr.com` (production).
- **Failure handling:** If any link is broken (internal or external), the GitHub Action fails and GitHub sends a failure notification. Exclude known crawler-hostile domains (LinkedIn, Twitter/X, etc.) in `lychee.toml` to reduce noise.
- **Reporting:** Markdown output saved as GitHub Actions artifact. No HTML report — iterate later if needed.
- **Configuration:** One `lychee.toml` for local builds. The production workflow uses CLI overrides where needed (e.g., longer timeout, different excludes). Keeps config simple — one file in the repo, production differences visible in the workflow YAML.
- **Multilingual:** No custom verification script. lychee checks all links present in the generated pages — if language variant links exist in the HTML, lychee verifies they resolve.
- **Production page discovery:** Build the site in CI, extract all page URLs from `./output` HTML files, then check them live against `https://grtnr.com` (Option D). This gives a true production test without requiring a sitemap plugin.

---

## Scope of Changes

### 1. Replace `linkchecker` with `lychee` in build pipeline

- Delete `check-links.sh` and remove `linkcheck-errors.txt` output
- Update `tasks.py` `check_links` task to call `lychee ./output` directly with native markdown output
- Update CI workflow (`publish.yml`) to use `lycheeverse/lychee-action` instead of `apt-get install linkchecker`
- Update pre-commit hook messages (remove references to `linkcheck-errors.txt`)
- Add `lychee.toml` config file with defaults (timeout=30, excluded domains for crawler-hostile sites)
- Remove `linkcheck-errors.txt` from `.gitignore`
- Document lychee installation in README.md (`brew install lychee`)

### 2. New GitHub Action: daily production check

A new workflow file `.github/workflows/test-production.yml` that runs on a daily cron schedule:

- Checks out the repo and builds the site to get the full list of pages
- Extracts all page URLs from `./output` HTML files, remaps paths to `https://grtnr.com/...`
- Runs lychee against these live URLs to verify they resolve
- Uses `--format markdown` for the report, saved as a GitHub Actions artifact
- Fails the action if any issues are found (triggering GitHub notification)

### 3. Update documentation

- Update CLAUDE.md references to `linkchecker`, `check-links.sh`, and `linkcheck-errors.txt`
- Update README.md with lychee installation instructions

---

## Implementation Plan

1. Add `lychee.toml` configuration with defaults
2. Delete `check-links.sh` and update `tasks.py` to call `lychee` directly
3. Update `publish.yml` to use `lycheeverse/lychee-action`
4. Update pre-commit hook messages and `.gitignore`
5. Update CLAUDE.md and README.md references
6. Create `test-production.yml` workflow with daily cron (build + extract URLs + check live)
7. Test locally with `lychee ./output`, then verify CI works

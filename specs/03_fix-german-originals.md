# Fix: German-original articles missing English translations

## Problem

Articles originally written in German (8 currently) have their `-EN.md` translation
files on disk but the pipeline never loads them. The English and root-level versions
of these articles display German text instead of the English translation.

## Root Cause

`garten/discover.py:_find_translation_files()` skips looking for translation files
in the default language (`"en"`), assuming originals are always in the default language.
This assumption is wrong for German-original content.

## Files to Change

### 1. `garten/discover.py` — `_find_translation_files()`

**Current (buggy):**
```python
for lang in languages:
    if lang == default_lang:
        continue
    candidate = ext_dir / f"{base_name}-{lang.upper()}.md"
    if candidate.exists():
        found[lang] = candidate
```

**Fix:** Remove the `if lang == default_lang: continue` guard. Look for translation
files in ALL configured languages. English originals won't have `-EN.md` files so
nothing changes for them; German originals will now find their `-EN.md` files.

```python
for lang in languages:
    candidate = ext_dir / f"{base_name}-{lang.upper()}.md"
    if candidate.exists():
        found[lang] = candidate
```

### 2. `garten/assemble.py` — `_build_lang_article()` and `_build_lang_page()`

These functions build per-language content. When an English translation exists for a
German original, it should be used for the `en` language version. Verify that the
existing fallback logic works correctly now that `translations["en"]` will be populated.

The current logic (approximately):
```python
trans = original.get("translations", {}).get(lang, {})
if trans:
    art["content"] = trans["content"]
    art["title"] = trans.get("title", original["title"])
    ...
```

This should already work once translations["en"] is populated. **Verify, don't change
unless needed.**

### 3. `garten/assemble.py` — `prefix_internal_links()` (line ~165)

**Current:**
```python
def prefix_internal_links(html: str, lang: str, languages: list[str]) -> str:
    if not html or lang == "en":
        return html
```

**Fix:** Accept `default_lang` as a parameter and compare against it:
```python
def prefix_internal_links(
    html: str, lang: str, languages: list[str], default_lang: str = "en"
) -> str:
    if not html or lang == default_lang:
        return html
```

Update all callers to pass `default_lang` from config.

### 4. `garten/assemble.py` — `build_translated_links()` (line ~543)

**Current:**
```python
if lang != "en" and href not in _NO_LANG_PREFIX_PATHS:
```

**Fix:** Accept `default_lang` as a parameter:
```python
def build_translated_links(
    links: list, lang: str, menu_translations: dict, default_lang: str = "en"
) -> list:
    ...
    if lang != default_lang and href not in _NO_LANG_PREFIX_PATHS:
```

Update all callers to pass `default_lang` from config.

### 5. `garten/assemble.py` — `build_language_links()`

Check whether this function also skips generating a language link for `"en"` when the
original is German. If it does, users on the German root-level page can't switch to
the English translation. Fix similarly by comparing against `default_lang` rather than
hardcoded `"en"`.

### 6. Root-level content for German originals

Currently root-level URLs (`/slug/`) always show the original content. For German
originals, this means root shows German. Two options:

**Option A (recommended):** Root-level content for German originals should use the
English translation (since root = default language = English). In `generate_urls()`
or the render phase, when an article has a translation in the default language, swap
the root-level content with the default-language translation.

**Option B (simpler):** Accept that root-level shows the original language and rely
on the language switcher to let users navigate to `/en/slug/`. This is simpler but
means root-level English readers see German text.

## Tests to Add/Update

1. **Unit test for `_find_translation_files`** — Assert that `-EN.md` files are found
   for German originals.
2. **Unit test for `prefix_internal_links`** — Test with `default_lang="de"` to verify
   it no longer hardcodes English.
3. **Integration test** — Pick a known German-original article (e.g. `crowdsourcing-angebot`)
   and verify:
   - `manifest["articles"]` entry has `"en"` in `translation_files`
   - After process phase, `translations["en"]` contains the English content
   - After assemble, the `/en/` version has English title/content
   - After render, the output HTML at `en/crowdsourcing-.../index.html` contains
     English text (e.g. "Crowdsourcing! Pay 100")
4. **Update hardcoded content counts** if the fix changes how articles are counted.

## Verification

After the fix, run:
```bash
source .venv/bin/activate
inv build    # full build with link checking
python -m pytest tests/ -q
```

Then manually check a German-original article in the output:
```bash
# Should contain English text, not German
grep -l "Crowdsourcing" output/en/crowdsourcing-*/index.html
```

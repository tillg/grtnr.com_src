## Rework the translation cache

Currently the translation has a kind of a dual cache system that is problematic:

- Translations are cached in a cache in /cache/translations
- Translated documents are stored in the `extension` folder of every article, page, recipe.

Those 2 caches interact in a strange way.

This is the analysis made by Claude:

```text
Now I have a complete understanding of the issue! The problem is in the automatic translation system's architecture:

  Root Cause Analysis

  The translation system has a disconnect between caching and file writing:

  1. Cache works correctly - It prevents unnecessary API calls when content hasn't changed
  2. File writing always happens - Even when using cached translations, the system always writes new files with fresh timestamps

  The Problematic Flow

  1. You run inv build
  2. Translation system processes all articles
  3. For each article, it checks the cache (✅ works correctly)
  4. If cache hit: retrieves cached translation content
  5. But then it ALWAYS writes a new file with a fresh Translate-Date timestamp
  6. This causes the git diff to show "changes" even though only the timestamp changed

  Why This Happens

  The system treats file writing as a generation step rather than a persistence step. The code always:
  - Creates fresh metadata with current timestamp
  - Writes the complete file to disk
  - Overwrites any existing translation file

  The Fix

  To solve this, the translation system would need to:

  1. Check if translation file already exists
  2. Compare source content hash with existing translation file hash
  3. Only write new file if source has actually changed
  4. Preserve original timestamp for unchanged translations

  Immediate Workaround

  For now, you can avoid this issue by:

  1. Don't commit translation files that only have timestamp changes
  2. Use .gitignore patterns to exclude translation files from commits
  3. Only commit translation files when you've actually changed source content

  This is a design flaw in the automatic translation system - it should respect the cache at the file level, not just the API level.
```

## Simple cache structure

We want to change this to a simpler cache:

- Only translated documents are stored in the `extension` subfolder of articles, pages, recipes
- The other translation cache is removed, both in code and it's data at `/cache/translations`
- The translated documents get a front matter variable that holds the hash value of the original document in order to quickly decide wether translation is required or not
- There is a function translate_document(path_to_source_doc, language, path_to_target_doc) that does it all. It also checks if the target doc already exists and wether it needs to translate or if the existing target doc is still up to date (by checking the hash value).
- This function uses the existing translation functions to translate the document title, the summary as well as the content.

## Cleanup code

Look thru the code base and try to identify legacy structures:

- Unused code. Make sure we only have functions and code that is really used
- Wrong names: Look for functions that do something else than the name suggests. In this case explain me what the function does and come up with a suggestion for a name.
- Duplicate functionality: Functionality that has been developed twice, or twiuse very similar. Explain me those functions or functional blocks.

Are there other type of bad code smell that we should look for?

All the findings should be reported in THIS MD file, including suggestions on how to fix them.

---

# Code Cleanup Analysis Report

## 1. Unused Code (High Priority - Safe to Remove)

### Unused Plugin Files

- **`plugins/toc_indentation.py`** - TOC indentation plugin (34 lines) - not listed in `pelicanconf.py`
- **`plugins/validate_links.py`** - Link validation plugin (229 lines) - not listed in `pelicanconf.py`

### Backup Files

- **`plugins/translation_service.py.backup`** - Old backup of translation service (300 lines)

### Empty Directories

- **`plugins/custom_tag_pages/`** - Empty directory

## 2. Functions with Misleading Names

### Functions That Do More Than Their Name Suggests

1. **`pelican_run()` in `tasks.py`**

   - **What it does**: Processes command-line arguments and calls `pelican_main()`
   - **Better name**: `prepare_and_run_pelican()`

2. **`reserve()` in `tasks.py`**

   - **What it does**: Builds the site then serves it
   - **Better name**: `build_and_serve()`

3. **`process_external_links()` in `plugins/external_links.py`**

   - **What it does**: Adds `target="_blank"` attributes to external links
   - **Better name**: `add_external_link_attributes()`

4. **`fix_image_urls()` in `plugins/copy_adjacent_images.py`**

   - **What it does**: Converts relative image paths to absolute paths
   - **Better name**: `convert_relative_image_paths()`

5. **`set_proper_category()` in `plugins/set_proper_category.py`**

   - **What it does**: Assigns categories based on directory structure
   - **Better name**: `assign_categories_from_directory()`

6. **`convert_excerpt_to_summary()` in `plugins/excerpt_to_summary.py`**

   - **What it does**: Copies excerpt metadata to summary field
   - **Better name**: `copy_excerpt_to_summary()`

7. **`process_wikilinks()` in `plugins/wikilinks.py`**
   - **What it does**: Converts `[[WikiLink]]` syntax to HTML anchor tags
   - **Better name**: `convert_wikilinks_to_html()`

### Functions with Generic Names

- **`clean()` in `tasks.py`** → `clean_output_directory()`
- **`register()` functions** → Should be more specific like `register_auto_title_plugin()`

### Functions Violating Single Responsibility

- **`process_content_items()` in `plugins/copy_adjacent_images.py`** - Does copying AND URL fixing.
  - **Fix**: Split into two functions:
    - `copy_adjacent_images()` - Handle file copying and directory creation
    - `update_image_urls_in_content()` - Handle URL fixing in content
    - Keep `process_content_items()` as orchestrator that calls both
- **`generate_output()` in `plugins/automatic_translation.py`** - Filters, processes, and tracks statistics
  - **Fix**: Split into focused functions:
    - `filter_translatable_content()` - Handle content filtering logic
    - `process_translations_batch()` - Handle parallel translation processing
    - `track_translation_statistics()` - Handle statistics collection
    - Keep `generate_output()` as coordinator that calls these in sequence

## 3. Duplicate Functionality

### Major Duplications

1. **Duplicate Automatic Translation Plugins**

   - **Main**: `plugins/automatic_translation.py` (429 lines)
   - **Duplicate**: `extensions/plugins/automatic_translation.py` (290 lines)
   - **Recommendation**: Keep the main version (has parallel processing), remove the duplicate

2. **Duplicate WikiLinks Processing**

   - **Plugin**: `plugins/wikilinks.py` (165 lines)
   - **Markdown Extension**: `plugins/markdown_wikilinks.py` (67 lines)
   - **Note**: This appears intentional for robust processing, but common logic could be extracted
   - **Fix**: Extract shared logic into utility module:
     - Create `plugins/utils/wikilinks_parser.py` with shared functions:
       - `parse_wikilink(text)` - Parse `[[Page Name|Display]]` syntax
       - `normalize_wikilink_slug(page_name)` - Consistent slug normalization
       - `build_wikilink_url(slug, display_text)` - URL construction
     - Both plugins import and use these utilities, reducing duplication by ~40 lines

3. **Duplicate Translation Service Tests**
   - **Main**: `tests/test_translation_service.py`
   - **Duplicate**: `extensions/tests/test_translation_service.py`
   - **Recommendation**: Consolidate into single test suite

## 4. Other Code Smells

### Large Classes with Too Many Responsibilities

- **`MultilingualSiteGenerator`** - Handles URL generation, content processing, file parsing, and article creation
  - **Fix**: Apply Single Responsibility Principle by splitting into focused classes:
    - `MultilingualURLBuilder` - Handle URL generation and language-specific paths
    - `TranslationFileParser` - Handle parsing of translation files and metadata
    - `MultilingualContentProcessor` - Handle content processing and article creation
    - `MultilingualSiteGenerator` becomes orchestrator that delegates to these services
- **`TranslationService`** - Handles API calls, caching, language detection, and batch processing
  - **Fix**: Break down into specialized services using composition:
    - `TranslationAPIClient` - Handle OpenAI API calls and retry logic
    - `LanguageDetector` - Handle language detection and validation
    - `TranslationCacheManager` - Handle caching operations
    - `BatchTranslationProcessor` - Handle batch processing and parallel execution
    - `TranslationService` becomes facade that coordinates these services

### Magic Numbers and Hardcoded Values

- Translation limits: `max_tokens=4096`, `temperature=0.3`
  - Fix: Extract values to config file.
- File extensions: `".jpg", ".jpeg", ".png", ".gif", ".svg"`
  - Fix: Extract values to config file.

### Primitive Obsession

- File paths as strings instead of Path objects
  - Fix: Make paths as path objects
- URLs as string concatenation
  - **Fix**: Create URL value objects and builder pattern:
    - `ContentURL` class with validation and proper path handling
    - `URLBuilder` class with methods like `add_language()`, `add_path()`, `build()`
    - Use `urllib.parse.urljoin()` for proper URL construction
    - Example: `URLBuilder().language("de").path("articles").slug("my-post").build()`

## 5. Recommendations

### High Priority

1. **Remove duplicate automatic translation plugin** in `extensions/plugins/`
2. **Remove backup file** `translation_service.py.backup`
3. **Break down large functions** (especially `_create_translated_article_from_content`)
4. **Extract configuration constants** from hardcoded values

### Medium Priority

1. **Rename misleading functions** listed above
2. **Consolidate test files** into single comprehensive suite
3. **Create utility functions** for common content processing patterns
4. **Implement proper exception handling** with specific exception types
5. **Create domain objects** for language codes and paths

### Low Priority

1. **Standardize coding style** and import organization
2. **Extract common WikiLinks logic** into shared utility
3. **Create logger utility** to reduce repeated import patterns

## 6. Additional Code Smells to Watch For

Based on analysis, these are other important code smells in software projects:

- **Shotgun Surgery**: Changes requiring modifications in many places
- **Divergent Change**: One class changed for many different reasons
- **Refused Bequest**: Subclasses that don't use inherited methods
- **Lazy Class**: Classes that don't do enough to pay for themselves
- **Speculative Generality**: Unused abstract classes or methods
- **Message Chains**: Long chains of method calls
- **Middle Man**: Classes that delegate most of their work
- **Parallel Inheritance Hierarchies**: When subclassing requires subclassing another class
- **Large Class**: Classes trying to do too much
- **Dead Code**: Unused code that can be removed

## 7. Cleanup Action Plan

1. **Phase 1**: Remove unused files and duplicates (immediate impact) ✅ **COMPLETED**
2. **Phase 2**: Rename misleading functions (improves readability) ✅ **COMPLETED**
3. **Phase 3**: Refactor large functions and classes (improves maintainability) ✅ **COMPLETED**
4. **Phase 4**: Implement proper error handling and domain objects (improves robustness)
5. **Phase 5**: Standardize coding style (improves consistency)

## 8. Phase 3 Implementation Results

✅ **Successfully completed phase 3 refactoring with the following improvements:**

### 8.1 Refactored `copy_adjacent_images.py`
- **Split `process_content_items()`** into focused functions:
  - `copy_adjacent_images()` - Handles file copying and directory creation
  - `update_image_urls_in_content()` - Handles URL fixing in content
  - `process_content_items()` - Acts as orchestrator calling both functions

### 8.2 Refactored `automatic_translation.py`
- **Split `generate_output()`** into specialized functions:
  - `_filter_translatable_content()` - Handles content filtering logic
  - `_process_translations_batch()` - Handles parallel translation processing
  - `_log_translation_statistics()` - Handles statistics collection
  - `generate_output()` - Acts as coordinator calling these in sequence

### 8.3 Refactored `multilingual_site.py`
- **Split `MultilingualSiteGenerator`** into focused classes:
  - `MultilingualOutputGenerator` - Handles generation of multilingual content files
  - `MultilingualContextManager` - Manages multilingual context and language-specific data
  - `MultilingualSiteGenerator` - Simplified orchestrator using the specialized classes

### 8.4 Refactored `translation_service/service.py`
- **Split `TranslationService`** into specialized classes:
  - `TranslationAPIClient` - Handles OpenAI API calls with retry logic
  - `BatchTranslationProcessor` - Handles batch processing of multiple translations
  - `TranslationService` - Simplified facade coordinating the specialized services

### 8.5 Build Verification
- ✅ All refactored code builds successfully
- ✅ All plugins load correctly
- ✅ No breaking changes introduced
- ✅ System maintains all existing functionality

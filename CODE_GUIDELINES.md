# Code Guidelines

This document outlines the code quality standards, tools, and workflows for the grtnr.com project.

[TOC]

## Overview

This project uses automated formatting and linting to ensure consistent code quality across Python, Markdown, and JSON files. The approach prioritizes automation over manual fixes, with most issues being auto-corrected by formatting tools.

## Quick Start Commands

### Python

```bash
# Format and lint Python files
inv check-py

# Format only
inv format-py

# Lint only
inv lint-py
```

### Markdown

```bash
# Format and lint Markdown files
inv check-md

# Format only
inv format-md

# Lint only
inv lint-md

# Work with single files
inv format-md --file="path/to/file.md"
inv lint-md --file="path/to/file.md"
inv check-md --file="path/to/file.md"
```

### JSON

```bash
# Format and lint JSON files
inv check-json

# Format only
inv format-json

# Lint only
inv lint-json

# Work with single files
inv format-json --file="path/to/file.json"
inv lint-json --file="path/to/file.json"
inv check-json --file="path/to/file.json"
```

### Installation

```bash
# Install Python dependencies
pip install -r .devcontainer/requirements.txt

# Install Node.js dependencies
npm install
```

## Python Code Quality

### Tools Used

- **Black**: Code formatter with 88-character line length
- **isort**: Import organization tool (configured to work with Black)
- **flake8**: Linting tool for style and error checking

### Configuration

**Black Configuration** (in `pyproject.toml`):

```toml
[tool.black]
line-length = 88
exclude = '''
/(
    \.venv
  | venv
  | __pycache__
  | \.git
  | output
)/
'''
```

**isort Configuration** (in `pyproject.toml`):

```toml
[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
skip = [".venv", "venv", "__pycache__", "output"]
```

**flake8 Configuration** (in `.flake8`):

```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude =
    .git,
    __pycache__,
    .venv,
    venv,
    output,
    node_modules,
    *.egg-info
```

### File Exclusions

The following directories are excluded from formatting and linting:

- `.venv/`, `venv/`: Virtual environment files
- `__pycache__/`: Python bytecode cache
- `output/`: Generated Pelican output
- `node_modules/`: Node.js dependencies
- `.git/`: Git repository files

### Manual Commands

```bash
# Format with Black
.venv/bin/black .

# Organize imports with isort
.venv/bin/isort .

# Lint with flake8
.venv/bin/flake8
```

### Required Python Packages

```txt
# Formatting and Linting
black==24.10.0
isort==5.13.2
flake8==7.2.0
```

## Markdown Code Quality

### Tools Used

- **Prettier**: Markdown formatter with 88-character line length
- **markdownlint**: Linting tool for Markdown style and structure checking

### Configuration

**Prettier Configuration** (in `.prettierrc.json`):

```json
{
  "printWidth": 88,
  "tabWidth": 2,
  "useTabs": false,
  "semi": false,
  "singleQuote": false,
  "quoteProps": "as-needed",
  "trailingComma": "none",
  "bracketSpacing": true,
  "proseWrap": "preserve",
  "overrides": [
    {
      "files": "*.md",
      "options": {
        "proseWrap": "preserve",
        "printWidth": 88
      }
    }
  ]
}
```

**markdownlint Configuration** (in `.markdownlint.json`):

```json
{
  "default": true,
  "MD013": false,
  "MD024": {
    "siblings_only": true
  },
  "MD033": false,
  "MD036": false,
  "MD041": false,
  "MD046": {
    "style": "fenced"
  }
}
```

**markdownlint Ignore File** (in `.markdownlintignore`):

```text
node_modules/
output/
.venv/
venv/
__pycache__/
*.egg-info/
```

### Manual Commands

```bash
# Format with Prettier
npx prettier --write --log-level warn '**/*.md'

# Lint with markdownlint
npx markdownlint '**/*.md'
```

### Required Node.js Packages

```json
{
  "devDependencies": {
    "markdownlint-cli": "^0.44.0",
    "prettier": "^3.5.3"
  }
}
```

## JSON Code Quality

### Tools Used

- **Prettier**: JSON formatter with 2-space indentation
- **jsonlint**: JSON syntax validation and linting tool

### Configuration

**Prettier Configuration** (in `.prettierrc.json`):

JSON files use the same Prettier configuration as other files, with specific settings:

```json
{
  "printWidth": 88,
  "tabWidth": 2,
  "useTabs": false,
  "trailingComma": "none",
  "bracketSpacing": true
}
```

**File Exclusions** (in `.prettierignore`):

```text
node_modules/
output/
.venv/
venv/
__pycache__/
*.egg-info/
```

### Manual Commands

```bash
# Format with Prettier
npx prettier --write --log-level warn '**/*.json'

# Lint with jsonlint (quiet mode)
npx jsonlint filename.json -q

# Bulk lint all JSON files (quiet mode)
find . -name '*.json' -not -path './node_modules/*' -not -path './output/*' -not -path './.venv/*' -not -path './venv/*' -exec npx jsonlint {} -q \;
```

### Required Node.js Packages

```json
{
  "devDependencies": {
    "jsonlint": "^1.6.3",
    "prettier": "^3.5.3"
  }
}
```

## VS Code Integration

### Settings Configuration

The workspace includes automatic formatting and linting for Python, Markdown, and JSON files:

**VS Code Settings** (in `.vscode/settings.json`):

```json
{
  "files.associations": {
    "*.html": "jinja-html"
  },
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": "explicit"
  },
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "ms-python.black-formatter"
  },
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "flake8.args": ["--max-line-length=88", "--extend-ignore=E203,W503"],
  "flake8.interpreter": ["./.venv/bin/python"],
  "python.analysis.typeCheckingMode": "basic",
  "[markdown]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.wordWrap": "wordWrapColumn",
    "editor.wordWrapColumn": 88
  },
  "markdownlint.config": {
    "extends": ".markdownlint.json"
  },
  "[json]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.detectIndentation": false,
    "editor.tabSize": 2,
    "editor.insertSpaces": true
  },
  "[jsonc]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.detectIndentation": false,
    "editor.tabSize": 2,
    "editor.insertSpaces": true
  }
}
```

### Required Extensions

**VS Code Extensions** (in `.vscode/extensions.json`):

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.isort",
    "ms-python.flake8",
    "esbenp.prettier-vscode",
    "DavidAnson.vscode-markdownlint"
  ]
}
```

### Features

- **Auto-format on save**: Enabled for Python, Markdown, and JSON files
- **Import organization**: Automatic import sorting on save for Python
- **Linting integration**: Real-time error display for all languages
- **Word wrap**: Set to 88 characters for consistency (Markdown only)
- **JSON formatting**: 2-space indentation with consistent formatting
- **Extension recommendations**: Automatically suggests required extensions

## Installation Guide

### Python Setup

```bash
# Install all dependencies
pip install -r .devcontainer/requirements.txt

# Or install individually
pip install black==24.10.0 isort==5.13.2 flake8==7.2.0
```

### Node.js Setup

```bash
# Install Node.js dependencies
npm install

# Or install individually
npm install --save-dev markdownlint-cli prettier jsonlint
```

## Troubleshooting

### Python Issues

**"Black and flake8 disagree on line length"**

This is configured correctly - both use 88 characters. If you see conflicts, ensure you're using the project's configuration files.

**"VS Code not showing linting errors"**

1. Ensure the flake8 extension is installed
2. Check that the correct Python interpreter is selected (`.venv/bin/python`)
3. Reload VS Code window if needed

**"Import organization not working"**

1. Ensure the isort extension is installed
2. Check that `"source.organizeImports": "explicit"` is set in VS Code settings
3. Verify the virtual environment is active

### Markdown Issues

**"Prettier not formatting Markdown files"**

1. Ensure the Prettier VS Code extension is installed
2. Check that Prettier is set as the default formatter for Markdown
3. Verify `.prettierrc.json` configuration exists
4. Try running `npx prettier --write filename.md` manually

**"markdownlint not showing errors in VS Code"**

1. Install the markdownlint VS Code extension
2. Check that `.markdownlint.json` configuration exists
3. Reload VS Code window if needed
4. Try running `npx markdownlint filename.md` manually

**"Line length violations in Markdown"**

markdownlint is configured to allow long lines in code blocks, tables, and headings. If you see line length violations:

1. Check if it's in prose text (should be wrapped)
2. Long URLs and code blocks are exempt from line length rules
3. Consider using reference-style links for long URLs

### JSON Issues

**"Prettier not formatting JSON files"**

1. Ensure the Prettier VS Code extension is installed
2. Check that Prettier is set as the default formatter for JSON files
3. Verify `.prettierrc.json` configuration exists
4. Try running `npx prettier --write filename.json` manually

**"jsonlint not catching errors"**

1. Check that jsonlint is installed: `npm list jsonlint`
2. Try running `npx jsonlint filename.json` manually
3. Ensure the JSON file doesn't have comments (use JSONC for commented JSON)
4. Check file path excludes in the find command

**"JSON formatting inconsistent"**

1. Ensure all JSON files use 2-space indentation
2. Check that VS Code is using Prettier as the default formatter
3. Verify no conflicting JSON formatters are installed
4. Run `inv format-json` to standardize all files

### Configuration Conflicts

If you encounter issues with configuration:

1. **Check pyproject.toml** - Primary configuration file for Black and isort
2. **Check .flake8** - Configuration file for flake8
3. **Check .prettierrc.json** - Configuration file for Prettier and JSON formatting
4. **Check .markdownlint.json** - Configuration file for markdownlint
5. **Check .vscode/settings.json** - VS Code workspace settings
6. **Check .prettierignore** - File exclusions for Prettier

### Common Fixes

1. **Clear caches**: Delete `.cache/`, `__pycache__/`, `node_modules/.cache/`
2. **Reinstall dependencies**: `pip install -r requirements.txt && npm install`
3. **Restart VS Code**: Reload window or restart application
4. **Check virtual environment**: Ensure `.venv/bin/python` is active

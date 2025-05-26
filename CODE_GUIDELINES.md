# Code Guidelines

This document outlines the code quality standards, tools, and workflows for the grtnr.com project.

[TOC]

## Overview

This project uses automated formatting and linting to ensure consistent code quality across Python files. The approach prioritizes automation over manual fixes, with most issues being auto-corrected by formatting tools.

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
    *.egg-info
```

### File Exclusions

The following directories are excluded from formatting and linting:

- `.venv/`, `venv/`: Virtual environment files
- `__pycache__/`: Python bytecode cache
- `output/`: Generated Pelican output
- `.git/`: Git repository files

## VS Code Integration

### Auto-formatting on Save

**VS Code Settings** (in `.vscode/settings.json`):

```json
{
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": "explicit"
    },
    "[python]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "ms-python.black-formatter"
    },
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "flake8.args": [
        "--max-line-length=88",
        "--extend-ignore=E203,W503"
    ]
}
```

**Required Extensions:**

- Python
- Black Formatter
- isort
- flake8

## Available Commands

### Formatting Commands

- `inv format-py` - Format Python files only (Black + isort)

### Linting Commands

- `inv lint-py` - Lint Python files only (flake8)

### Combined Commands

- `inv check-py` - Format and lint Python files (complete workflow)

## Development Workflow

### Recommended Pre-commit Process

1. **Format code**: `inv format-py`
1. **Check for linting issues**: `inv lint-py`
1. **Fix any remaining issues** (usually minimal after formatting)
1. **Commit changes**

### Alternative Workflow

1. **Format and check in one command**: `inv check-py`
1. **Fix any remaining issues** (if any)
1. **Commit changes**

### VS Code Workflow

1. **Edit files** - Auto-formatting on save handles most issues
1. **Run `inv lint-py`** before committing to catch any remaining issues
1. **Commit changes**

## Dependencies

### Required Python Packages

```txt
# Formatting and Linting
black==24.10.0
isort==5.13.2
flake8==7.2.0
```

### Installation

```bash
# Install all dependencies
pip install -r .devcontainer/requirements.txt

# Or install individually
pip install black==24.10.0 isort==5.13.2 flake8==7.2.0
```

## Troubleshooting

### Common Issues

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

### Configuration Conflicts

If you encounter issues with configuration:

1. **Check pyproject.toml** - Primary configuration file for Black and isort
2. **Check .flake8** - flake8-specific configuration
3. **Check .vscode/settings.json** - VS Code integration settings
4. **Ensure virtual environment** - All tools should use `.venv/bin/python`

The tools are configured to work together harmoniously with the 88-character line length standard.
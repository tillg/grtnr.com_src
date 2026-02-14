"""Content dataclasses for garten."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class Article:
    # --- From frontmatter ---
    title: str = ""
    date: datetime | None = None
    tags: list[str] = field(default_factory=list)
    excerpt: str | None = None
    image: str | None = None
    updates: str | None = None
    status: str = "published"

    # --- Derived during Discover ---
    slug: str = ""
    category: str = ""
    source_path: Path = field(default_factory=Path)
    content_dir: Path = field(default_factory=Path)
    content_type: str = "article"

    # --- Set during Process ---
    content: str = ""
    summary: str = ""

    # --- Set during Assemble ---
    url: str = ""
    save_as: str = ""
    multilingual_urls: dict[str, str] = field(default_factory=dict)
    locale_date: str = ""
    translation_files: dict[str, Path] = field(default_factory=dict)


@dataclass
class Page:
    # --- From frontmatter ---
    title: str = ""
    date: datetime | None = None
    slug: str = ""
    status: str = "published"
    image: str | None = None

    # --- Derived during Discover ---
    source_path: Path = field(default_factory=Path)
    content_dir: Path = field(default_factory=Path)
    content_type: str = "page"

    # --- Set during Process ---
    content: str = ""

    # --- Set during Assemble ---
    url: str = ""
    save_as: str = ""
    multilingual_urls: dict[str, str] = field(default_factory=dict)
    locale_date: str = ""
    translation_files: dict[str, Path] = field(default_factory=dict)


@dataclass
class Recipe:
    # --- From frontmatter ---
    title: str = ""
    layout: str = "recipe"
    slug: str = ""
    date_published: datetime | None = None
    date_updated: datetime | None = None
    date: datetime | None = None
    image: str | None = None
    excerpt: str | None = None
    tags: list[str] = field(default_factory=list)

    # --- Derived during Discover ---
    source_path: Path = field(default_factory=Path)
    content_dir: Path = field(default_factory=Path)
    content_type: str = "recipe"
    category: str = "recipes"

    # --- Set during Process ---
    content: str = ""

    # --- Set during Assemble ---
    url: str = ""
    save_as: str = ""
    multilingual_urls: dict[str, str] = field(default_factory=dict)
    locale_date: str = ""


@dataclass
class TranslatedContent:
    """A translated variant of any content type."""

    original: Article | Page | Recipe = field(default_factory=Article)
    lang: str = ""
    title: str = ""
    content: str = ""
    excerpt: str | None = None
    url: str = ""
    save_as: str = ""
    source_hash: str = ""
    translator: str = ""
    translate_date: datetime | None = None
    locale_date: str = ""

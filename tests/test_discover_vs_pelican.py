"""Compare garten's Discover phase against Pelican's content discovery.

Runs both systems on the same content directory and diffs the results.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "plugins"))

os.chdir(ROOT)


# ---------------------------------------------------------------------------
# Pelican discovery
# ---------------------------------------------------------------------------


def _run_pelican() -> dict:
    """Run Pelican and capture discovered content via signal hook."""
    from pelican import Pelican
    from pelican.generators import ArticlesGenerator, PagesGenerator
    from pelican.settings import DEFAULT_CONFIG, get_settings_from_file

    settings = DEFAULT_CONFIG.copy()
    settings.update(get_settings_from_file("pelicanconf.py"))

    captured: dict = {"articles": [], "pages": [], "recipes": []}

    from pelican import signals

    def on_generators_finalized(generators):
        for gen in generators:
            if isinstance(gen, ArticlesGenerator):
                for art in gen.articles:
                    # Skip translation files
                    if hasattr(art, "source_path") and "/extensions/" in str(
                        art.source_path
                    ):
                        continue
                    captured["articles"].append(
                        {
                            "title": str(getattr(art, "title", "")),
                            "slug": str(getattr(art, "slug", "")),
                            "date": (
                                art.date.strftime("%Y-%m-%d")
                                if hasattr(art, "date") and art.date
                                else ""
                            ),
                            "category": str(getattr(art.category, "name", "")),
                            "status": str(getattr(art, "status", "published")),
                            "tags": sorted(
                                str(t).lower()
                                for t in getattr(art, "tags", [])
                            ),
                            "source_path": str(getattr(art, "source_path", "")),
                        }
                    )
                # Recipes from context
                for recipe in gen.context.get("recipes", []):
                    captured["recipes"].append(
                        {
                            "title": str(getattr(recipe, "title", "")),
                            "slug": str(getattr(recipe, "slug", "")),
                            "source_path": str(
                                getattr(recipe, "source_path", "")
                            ),
                        }
                    )
            elif isinstance(gen, PagesGenerator):
                for page in gen.pages + getattr(gen, "hidden_pages", []):
                    if hasattr(page, "source_path") and "/extensions/" in str(
                        page.source_path
                    ):
                        continue
                    captured["pages"].append(
                        {
                            "title": str(getattr(page, "title", "")),
                            "slug": str(getattr(page, "slug", "")),
                            "status": str(getattr(page, "status", "published")),
                            "source_path": str(
                                getattr(page, "source_path", "")
                            ),
                        }
                    )

    signals.all_generators_finalized.connect(on_generators_finalized)

    try:
        pelican = Pelican(settings)
        pelican.run()
    except Exception:
        pass  # We only care about content discovery, not output generation

    signals.all_generators_finalized.disconnect(on_generators_finalized)

    return captured


# ---------------------------------------------------------------------------
# Garten discovery
# ---------------------------------------------------------------------------


def _run_garten() -> dict:
    """Run garten's discover phase and return normalised results."""
    from garten.config import load_config
    from garten.discover import discover

    cfg = load_config(ROOT / "site.json")
    manifest = discover(cfg)

    articles = []
    for a in manifest["articles"]:
        articles.append(
            {
                "title": a["title"],
                "slug": a["slug"],
                "date": a["date"][:10] if a["date"] else "",
                "category": a["category"],
                "status": a["status"],
                "tags": sorted(a["tags"]),
                "source_path": a["source_path"],
            }
        )

    pages = []
    for p in manifest["pages"]:
        pages.append(
            {
                "title": p["title"],
                "slug": p["slug"],
                "status": p["status"],
                "source_path": p["source_path"],
            }
        )

    recipes = []
    for r in manifest["recipes"]:
        recipes.append(
            {
                "title": r["title"],
                "slug": r["slug"],
                "source_path": r["source_path"],
            }
        )

    return {"articles": articles, "pages": pages, "recipes": recipes}


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------


def _normalize_path(p: str) -> str:
    """Normalise to relative path from project root for comparison."""
    root_str = str(ROOT) + "/"
    if p.startswith(root_str):
        return p[len(root_str):]
    return p


def _by_source(items: list[dict]) -> dict[str, dict]:
    """Index a list of content dicts by normalised source_path."""
    return {_normalize_path(item["source_path"]): item for item in items}


def _strip_typogrify(text: str) -> str:
    """Remove Typogrify formatting for comparison.

    Typogrify adds &nbsp;, <span class="caps">, <span class="amp">, etc.
    This is a Process-phase concern; Discover should compare plain text.
    """
    import re

    text = text.replace("&nbsp;", " ")
    text = re.sub(r'<span class="[^"]*">', "", text)
    text = text.replace("</span>", "")
    text = text.replace("&amp;", "&")
    return text


def _compare(label: str, pelican_items: list[dict], garten_items: list[dict]):
    """Compare two lists of content items and print differences."""
    p_by_src = _by_source(pelican_items)
    g_by_src = _by_source(garten_items)

    p_paths = set(p_by_src.keys())
    g_paths = set(g_by_src.keys())

    diffs = []

    # Items only in one side
    only_pelican = p_paths - g_paths
    only_garten = g_paths - p_paths

    if only_pelican:
        diffs.append(f"  Only in Pelican ({len(only_pelican)}):")
        for p in sorted(only_pelican):
            diffs.append(f"    - {p}")

    if only_garten:
        diffs.append(f"  Only in garten ({len(only_garten)}):")
        for p in sorted(only_garten):
            diffs.append(f"    + {p}")

    # Items in both — compare fields
    common = p_paths & g_paths
    field_diffs = 0
    typogrify_only = 0
    for path in sorted(common):
        p_item = p_by_src[path]
        g_item = g_by_src[path]
        for key in p_item:
            if key == "source_path":
                continue
            pv = p_item.get(key)
            gv = g_item.get(key)
            if pv != gv:
                # Check if difference is only Typogrify formatting
                if (
                    key == "title"
                    and isinstance(pv, str)
                    and isinstance(gv, str)
                    and _strip_typogrify(pv) == gv
                ):
                    typogrify_only += 1
                    continue
                field_diffs += 1
                diffs.append(
                    f"  {Path(path).name}  {key}: "
                    f"pelican={pv!r}  garten={gv!r}"
                )

    print(f"\n{'='*60}")
    print(f" {label}")
    print(f"{'='*60}")
    print(f"  Pelican: {len(pelican_items)}  |  garten: {len(garten_items)}")
    print(f"  Common: {len(common)}  |  Field diffs: {field_diffs}")
    if typogrify_only:
        print(f"  (Typogrify-only title diffs: {typogrify_only} — expected)")
    if diffs:
        print()
        for line in diffs:
            print(line)
    else:
        print("  MATCH")
    print()

    return len(diffs) == 0


def main():
    print("Running Pelican discovery...")
    pelican = _run_pelican()
    print("Running garten discovery...")
    garten = _run_garten()

    all_match = True
    all_match &= _compare("ARTICLES", pelican["articles"], garten["articles"])
    all_match &= _compare("PAGES", pelican["pages"], garten["pages"])
    all_match &= _compare("RECIPES", pelican["recipes"], garten["recipes"])

    if all_match:
        print("ALL MATCH")
    else:
        print("DIFFERENCES FOUND — see above")

    return 0 if all_match else 1


if __name__ == "__main__":
    sys.exit(main())

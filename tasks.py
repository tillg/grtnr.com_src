import os
import shutil
import sys

from dotenv import load_dotenv
from invoke import task

from garten.config import load_config
from garten.utils import get_logger

# Setup logger for tasks
logger = get_logger("tasks")

# Load environment variables from .env file
load_dotenv()

OPEN_BROWSER_ON_SERVE = True

_CFG = load_config("site.json")

CONFIG = {
    "deploy_path": str(_CFG["output_path"]),
    "host": "localhost",
    "port": 8000,
}


def _run_garten_pipeline():
    """Run the full garten pipeline (discover → process → assemble → render)."""
    from garten.assemble import assemble as run_assemble
    from garten.assemble import write_artifacts as write_assemble_artifacts
    from garten.discover import discover as run_discover
    from garten.discover import write_manifest
    from garten.process import process as run_process
    from garten.process import write_artifacts

    cfg = load_config("site.json")
    manifest = run_discover(cfg)
    write_manifest(manifest, cfg["build_path"])
    run_process(manifest, cfg)
    write_artifacts(manifest, cfg["build_path"])
    site = run_assemble(manifest, cfg)
    write_assemble_artifacts(site, cfg["build_path"])

    from garten.render import render as run_render

    run_render(site, cfg)


@task
def clean_output_directory(c):
    """Remove generated files"""
    if os.path.isdir(CONFIG["deploy_path"]):
        shutil.rmtree(CONFIG["deploy_path"])
        os.makedirs(CONFIG["deploy_path"])


# Backward compatibility alias
@task
def clean(c):
    """Remove generated files (alias for clean_output_directory)"""
    clean_output_directory(c)


@task
def search_index(c):
    """Build Pagefind search index from the generated site"""
    logger.info("Building Pagefind search index...")
    c.run("python -m pagefind --site output")


@task
def build(c):
    """Build local version of site"""
    _run_garten_pipeline()
    search_index(c)
    check_links(c)


@task
def serve(c):
    """Serve site at http://$HOST:$PORT/ (default is localhost:8000)"""
    from functools import partial
    from http.server import HTTPServer, SimpleHTTPRequestHandler

    handler = partial(SimpleHTTPRequestHandler, directory=CONFIG["deploy_path"])

    server = HTTPServer((CONFIG["host"], CONFIG["port"]), handler)

    if OPEN_BROWSER_ON_SERVE:
        import webbrowser

        webbrowser.open("http://{host}:{port}".format(**CONFIG))

    sys.stderr.write("Serving at {host}:{port} ...\n".format(**CONFIG))
    server.serve_forever()


@task
def build_and_serve(c):
    """`build`, then `serve`"""
    build(c)
    serve(c)


# Backward compatibility alias
@task
def reserve(c):
    """Build then serve (alias for build_and_serve)"""
    build_and_serve(c)


@task
def preview(c):
    """Build production version of site"""
    _run_garten_pipeline()
    search_index(c)
    check_links(c)


@task
def check_links(c):
    """Check links in the generated site using lychee"""
    logger.info("Running lychee on output directory...")
    output_dir = os.path.abspath(CONFIG["deploy_path"])
    result = c.run(
        f"lychee --config lychee.toml --offline"
        f" --root-dir '{output_dir}' --index-files index.html"
        f" ./output",
        warn=True,
    )
    if result.return_code == 0:
        logger.info("Link check completed successfully - no broken links found")
    else:
        logger.error("Link check failed - broken links found!")
        sys.exit(1)


@task
def format_py(c):
    """Format Python code with Black and organize imports with isort"""
    logger.info("Running Black formatter...")
    c.run(".venv/bin/black .")
    logger.info("Running isort to organize imports...")
    c.run(".venv/bin/isort .")
    logger.info("Python formatting complete!")


@task
def lint_py(c):
    """Run flake8 linting on Python files"""
    logger.info("Running flake8 linter...")
    c.run(".venv/bin/flake8")


@task
def check_py(c):
    """Format and lint Python files"""
    format_py(c)
    lint_py(c)


@task
def format_md(c, file=None):
    """Format Markdown files with Prettier"""
    if file:
        logger.info(f"Running Prettier formatter on {file}...")
        c.run(f"npx prettier --write --log-level warn '{file}'")
    else:
        logger.info("Running Prettier formatter on all Markdown files...")
        c.run("npx prettier --write --log-level warn '**/*.md'")
    logger.info("Markdown formatting complete!")


@task
def lint_md(c, file=None):
    """Run markdownlint on Markdown files"""
    if file:
        logger.info(f"Running markdownlint on {file}...")
        result = c.run(f"npx markdownlint '{file}'", warn=True)
    else:
        logger.info("Running markdownlint on all files...")
        result = c.run("npx markdownlint '**/*.md'", warn=True)

    # Count violations and provide summary
    if result.stderr:
        violations = result.stderr.strip().split("\n")
        violation_count = len([line for line in violations if line.strip()])
        logger.info(f"{violation_count} linting violations found")
    else:
        logger.info("0 linting violations found")


@task
def check_md(c, file=None):
    """Format and lint Markdown files"""
    format_md(c, file=file)
    lint_md(c, file=file)


@task
def format_json(c, file=None):
    """Format JSON files with Prettier"""
    if file:
        logger.info(f"Running Prettier formatter on {file}...")
        c.run(f"npx prettier --write --log-level warn '{file}'")
    else:
        logger.info("Running Prettier formatter on all JSON files...")
        c.run("npx prettier --write --log-level warn '**/*.json'")
    logger.info("JSON formatting complete!")


@task
def lint_json(c, file=None):
    """Run jsonlint on JSON files"""
    if file:
        c.run(f"npx jsonlint '{file}' -q")
    else:
        c.run(
            "find . -name '*.json'"
            " -not -path './node_modules/*'"
            " -not -path './output/*'"
            " -not -path './.venv/*'"
            " -not -path './venv/*'"
            " -not -path './.devcontainer/*'"
            " -exec npx jsonlint {} -q \\;"
        )


@task
def check_json(c, file=None):
    """Format and lint JSON files"""
    format_json(c, file=file)
    lint_json(c, file=file)


@task
def livereload(c):
    """Automatically reload browser tab upon file modification."""
    from livereload import Server

    def cached_build():
        _run_garten_pipeline()

    cached_build()
    server = Server()

    theme_path = str(_CFG["theme_path"])
    content_path = str(_CFG["content_path"])

    watched_globs = [
        "site.json",
        f"{theme_path}/templates/**/*.html",
    ]

    content_file_extensions = [".md"]
    for extension in content_file_extensions:
        content_glob = f"{content_path}/**/*{extension}"
        watched_globs.append(content_glob)

    static_file_extensions = [".css", ".js"]
    for extension in static_file_extensions:
        static_file_glob = f"{theme_path}/static/**/*{extension}"
        watched_globs.append(static_file_glob)

    # Watch garten source files for changes
    garten_file_extensions = [".py"]
    for extension in garten_file_extensions:
        garten_glob = f"garten/**/*{extension}"
        watched_globs.append(garten_glob)

    for glob in watched_globs:
        server.watch(glob, cached_build)

    if OPEN_BROWSER_ON_SERVE:
        import webbrowser

        webbrowser.open("http://{host}:{port}".format(**CONFIG))

    server.serve(host=CONFIG["host"], port=CONFIG["port"], root=CONFIG["deploy_path"])


@task
def translate(c, dry_run=False, force=False):
    """Generate or regenerate translations for all content."""
    from garten.translate import translate_content

    cfg = load_config("site.json")
    stats = translate_content(cfg, dry_run=dry_run, force=force)

    print(f"\nTranslation summary:")
    print(f"  Translated: {stats['translated']}")
    print(f"  Skipped:    {stats['skipped']}")
    print(f"  Failed:     {stats['failed']}")
    print(f"  Total:      {stats['total']}")

    if stats["failed"] > 0:
        sys.exit(1)


@task
def clean_translations(c):
    """Remove all translation files from extensions directories"""
    from garten.utils import remove_all_translations

    content_path = str(_CFG["content_path"])

    print("Cleaning up all translation files...")

    try:
        removed_files, removed_dirs = remove_all_translations(content_path)

        if removed_files > 0:
            print("Successfully removed:")
            print(f"   {removed_files} translation files")
            print(f"   {removed_dirs} empty extension directories")
        else:
            print("No translation files found to remove")

    except Exception as e:
        print(f"Error during cleanup: {e}")
        sys.exit(1)



@task
def discover(c):
    """Run garten Phase 1: content discovery"""
    from garten.discover import discover as run_discover
    from garten.discover import write_manifest

    cfg = load_config("site.json")
    manifest = run_discover(cfg)
    write_manifest(manifest, cfg["build_path"])


@task
def process(c):
    """Run garten Phases 1-3: discover + process"""
    from garten.discover import discover as run_discover
    from garten.discover import write_manifest
    from garten.process import process as run_process
    from garten.process import write_artifacts

    cfg = load_config("site.json")
    manifest = run_discover(cfg)
    write_manifest(manifest, cfg["build_path"])
    run_process(manifest, cfg)
    write_artifacts(manifest, cfg["build_path"])


@task
def assemble(c):
    """Run garten Phases 1-4: discover + process + assemble"""
    from garten.assemble import assemble as run_assemble
    from garten.assemble import write_artifacts as write_assemble_artifacts
    from garten.discover import discover as run_discover
    from garten.discover import write_manifest
    from garten.process import process as run_process
    from garten.process import write_artifacts

    cfg = load_config("site.json")
    manifest = run_discover(cfg)
    write_manifest(manifest, cfg["build_path"])
    run_process(manifest, cfg)
    write_artifacts(manifest, cfg["build_path"])
    site = run_assemble(manifest, cfg)
    write_assemble_artifacts(site, cfg["build_path"])


@task
def render(c):
    """Run garten Phases 1-5: discover + process + assemble + render"""
    from garten.assemble import assemble as run_assemble
    from garten.assemble import write_artifacts as write_assemble_artifacts
    from garten.discover import discover as run_discover
    from garten.discover import write_manifest
    from garten.process import process as run_process
    from garten.process import write_artifacts
    from garten.render import render as run_render

    cfg = load_config("site.json")
    manifest = run_discover(cfg)
    write_manifest(manifest, cfg["build_path"])
    run_process(manifest, cfg)
    write_artifacts(manifest, cfg["build_path"])
    site = run_assemble(manifest, cfg)
    write_assemble_artifacts(site, cfg["build_path"])
    run_render(site, cfg)


@task
def preview_process(c, slug=None):
    """Preview processed HTML in browser. Use --slug to pick one, or omit to list."""
    import tempfile
    import webbrowser

    build_dir = os.path.join(os.path.dirname(__file__), ".build", "process")
    html_dir = os.path.join(build_dir, "html")

    if not os.path.isdir(html_dir):
        print("No process artifacts found. Run `inv process` first.")
        sys.exit(1)

    # Collect all available slugs
    all_files = {}
    for content_type in ("articles", "pages", "recipes"):
        type_dir = os.path.join(html_dir, content_type)
        if os.path.isdir(type_dir):
            for f in sorted(os.listdir(type_dir)):
                if f.endswith(".html"):
                    name = f[:-5]
                    all_files[name] = os.path.join(type_dir, f)

    if not slug:
        print("Available content (pass --slug to preview):\n")
        for name in sorted(all_files):
            print(f"  {name}")
        print(f"\nTotal: {len(all_files)} items")
        return

    if slug not in all_files:
        # Try partial match
        matches = [k for k in all_files if slug in k]
        if len(matches) == 1:
            slug = matches[0]
        elif len(matches) > 1:
            print(f"Multiple matches for '{slug}':")
            for m in matches:
                print(f"  {m}")
            return
        else:
            print(f"No match for '{slug}'")
            return

    content = open(all_files[slug]).read()
    wrapper = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{slug}</title>
<style>
  body {{ max-width: 48rem; margin: 2rem auto; padding: 0 1rem;
         font-family: -apple-system, system-ui, sans-serif;
         line-height: 1.6; color: #333; }}
  img {{ max-width: 100%; height: auto; }}
  pre {{ background: #f5f5f5; padding: 1rem; overflow-x: auto;
         border-radius: 4px; }}
  code {{ background: #f5f5f5; padding: 0.15em 0.3em; border-radius: 3px; }}
  pre code {{ background: none; padding: 0; }}
  blockquote {{ border-left: 3px solid #ccc; margin-left: 0;
                padding-left: 1rem; color: #666; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #ddd; padding: 0.5rem; text-align: left; }}
  .toc {{ background: #f9f9f9; padding: 1rem; border-radius: 4px;
          margin-bottom: 1.5rem; }}
  .highlight pre {{ margin: 0; }}
  a {{ color: #0066cc; }}
</style>
</head>
<body>
<h1>{slug.replace('-', ' ').title()}</h1>
<hr>
{content}
</body>
</html>"""

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(wrapper)
        tmp_path = f.name

    webbrowser.open(f"file://{tmp_path}")
    print(f"Opened preview for '{slug}'")

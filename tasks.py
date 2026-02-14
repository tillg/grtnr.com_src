import os
import shlex
import shutil
import sys
from dotenv import load_dotenv
from invoke import task
from invoke.main import program
from pelican import main as pelican_main
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer
from pelican.settings import DEFAULT_CONFIG, get_settings_from_file

# Import centralized logging
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "plugins"))
from logger_config import get_logger

# Setup logger for tasks
logger = get_logger("tasks")

# Load environment variables from .env file
load_dotenv()

OPEN_BROWSER_ON_SERVE = True
SETTINGS_FILE_BASE = "pelicanconf.py"
SETTINGS = {}
SETTINGS.update(DEFAULT_CONFIG)
LOCAL_SETTINGS = get_settings_from_file(SETTINGS_FILE_BASE)
SETTINGS.update(LOCAL_SETTINGS)

CONFIG = {
    "settings_base": SETTINGS_FILE_BASE,
    "settings_publish": "publishconf.py",
    # Output path. Can be absolute or relative to tasks.py. Default: 'output'
    "deploy_path": SETTINGS["OUTPUT_PATH"],
    # Host and port for `serve`
    "host": "localhost",
    "port": 8000,
}


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
def build(c):
    """Build local version of site"""
    prepare_and_run_pelican("-s {settings_base}".format(**CONFIG))
    check_links(c)


@task
def rebuild(c):
    """`build` with the delete switch"""
    prepare_and_run_pelican("-d -s {settings_base}".format(**CONFIG))


@task
def regenerate(c):
    """Automatically regenerate site upon file modification"""
    prepare_and_run_pelican("-r -s {settings_base}".format(**CONFIG))


@task
def serve(c):
    """Serve site at http://$HOST:$PORT/ (default is localhost:8000)"""

    class AddressReuseTCPServer(RootedHTTPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(
        CONFIG["deploy_path"],
        (CONFIG["host"], CONFIG["port"]),
        ComplexHTTPRequestHandler,
    )

    if OPEN_BROWSER_ON_SERVE:
        # Open site in default browser
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
    # Use pelicanconf.py directly instead of publishconf.py to avoid import issues
    prepare_and_run_pelican("-s " + CONFIG["settings_base"])
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
            "find . -name '*.json' -not -path './node_modules/*' -not -path './output/*' -not -path './.venv/*' -not -path './venv/*' -not -path './.devcontainer/*' -exec npx jsonlint {} -q \\;"
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
        cmd = "-s {settings_base} -e CACHE_CONTENT=true " "LOAD_CONTENT_CACHE=true"
        prepare_and_run_pelican(cmd.format(**CONFIG))

    cached_build()
    server = Server()
    theme_path = SETTINGS["THEME"]
    watched_globs = [
        CONFIG["settings_base"],
        f"{theme_path}/templates/**/*.html",
    ]

    content_file_extensions = [".md", ".rst"]
    for extension in content_file_extensions:
        content_glob = "{}/**/*{}".format(SETTINGS["PATH"], extension)
        watched_globs.append(content_glob)

    static_file_extensions = [".css", ".js"]
    for extension in static_file_extensions:
        static_file_glob = f"{theme_path}/static/**/*{extension}"
        watched_globs.append(static_file_glob)

    # Watch plugin files for changes
    plugin_file_extensions = [".py"]
    for extension in plugin_file_extensions:
        plugin_glob = f"plugins/**/*{extension}"
        watched_globs.append(plugin_glob)

    for glob in watched_globs:
        server.watch(glob, cached_build)

    if OPEN_BROWSER_ON_SERVE:
        # Open site in default browser
        import webbrowser

        webbrowser.open("http://{host}:{port}".format(**CONFIG))

    server.serve(host=CONFIG["host"], port=CONFIG["port"], root=CONFIG["deploy_path"])


@task
def clean_translations(c):
    """Remove all translation files from extensions directories"""
    # Import file manager
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "plugins"))
    from file_organization import ExtensionFileManager

    # Initialize file manager
    content_path = SETTINGS.get("PATH", "content")
    file_manager = ExtensionFileManager(content_root=content_path)

    print("🗑️  Cleaning up all translation files...")

    try:
        removed_files, removed_dirs = file_manager.remove_all_translations_global()

        if removed_files > 0:
            print(f"✅ Successfully removed:")
            print(f"   📄 {removed_files} translation files")
            print(f"   📁 {removed_dirs} empty extension directories")
        else:
            print("ℹ️  No translation files found to remove")

    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        sys.exit(1)


def prepare_and_run_pelican(cmd):
    # allows to pass-through args to pelican
    remainder = getattr(program.core, "remainder", None) or ""
    if remainder:
        cmd += " " + remainder
    pelican_main(shlex.split(cmd))

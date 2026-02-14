"""Shared utilities: slug normalization, logging, date helpers, frontmatter."""

import logging
import os
import re
import sys
import unicodedata
from datetime import datetime
from typing import Union

from unidecode import unidecode


# ---------------------------------------------------------------------------
# Logging (ported from plugins/logger_config.py)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str]:
    """Parse YAML-style frontmatter between ``---`` markers.

    Returns a dict with **lowercase** keys.  Values are raw strings;
    type coercion happens in the caller.
    """
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}

    meta: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip().lower()
        value = value.strip()
        # Strip surrounding quotes
        if len(value) >= 2 and value[0] in ('"', "'") and value[-1] == value[0]:
            value = value[1:-1]
        meta[key] = value
    return meta


def strip_frontmatter(text: str) -> str:
    """Remove the YAML frontmatter block and return just the body."""
    m = _FRONTMATTER_RE.match(text)
    return text[m.end() :] if m else text


# ---------------------------------------------------------------------------
# Logging (ported from plugins/logger_config.py)
# ---------------------------------------------------------------------------


class _ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[35m",
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        ts = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M")
        msg = f"{color}{ts} {record.levelname:<8}{self.RESET} {record.getMessage()}"
        if record.exc_info:
            msg += "\n" + self.formatException(record.exc_info)
        return msg


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(f"garten.{name}")
    if logger.handlers:
        return logger
    numeric = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(numeric)
    handler.setFormatter(_ColoredFormatter())
    logger.addHandler(handler)
    logger.propagate = False
    return logger


# ---------------------------------------------------------------------------
# Slug normalization (ported from plugins/normalize_slugs.py)
# ---------------------------------------------------------------------------

_GERMAN_CHAR_MAP = {
    "ä": "ae",
    "ö": "oe",
    "ü": "ue",
    "ß": "ss",
    "Ä": "Ae",
    "Ö": "Oe",
    "Ü": "Ue",
}


def normalize_slug(text: str) -> str:
    """Normalize *text* into a URL-safe slug.

    Applies German character transliteration, NFKD decomposition, and
    strips everything that isn't alphanumeric or a hyphen.

    Used for recipe slugs (which have explicit slug metadata).
    """
    if not text:
        return text

    for char, repl in _GERMAN_CHAR_MAP.items():
        text = text.replace(char, repl)

    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = text.replace(" ", "")
    text = re.sub(r"[^a-zA-Z0-9\-_]", "", text)
    text = re.sub(r"-+", "-", text)
    text = text.strip("-")
    return text


# Pelican's default SLUG_REGEX_SUBSTITUTIONS
_SLUG_REGEX_SUBS = [
    (r"[^\w\s-]", ""),
    (r"(?u)\A\s*", ""),
    (r"(?u)\s*\Z", ""),
    (r"[-\s]+", "-"),
]


def slugify(text: str) -> str:
    """Generate a URL slug from a title string.

    Replicates Pelican's ``slugify(value, regex_subs=...)`` behaviour:
    Unidecode → regex substitutions → lowercase.

    Used for articles and pages where ``SLUGIFY_SOURCE = "title"``.
    """
    if not text:
        return text
    text = unidecode(text)
    for pattern, repl in _SLUG_REGEX_SUBS:
        text = re.sub(pattern, repl, text)
    return text.lower()


# ---------------------------------------------------------------------------
# Date localization (ported from plugins/multilingual_site.py)
# ---------------------------------------------------------------------------

_LANG_DATE_CONFIG = {
    "en": {
        "months_short": [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
        ],
        "weekdays_short": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "weekdays": [
            "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday",
        ],
        "months": [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December",
        ],
    },
    "de": {
        "months_short": [
            "Jan", "Feb", "Mär", "Apr", "Mai", "Jun",
            "Jul", "Aug", "Sep", "Okt", "Nov", "Dez",
        ],
        "weekdays_short": ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"],
        "weekdays": [
            "Montag", "Dienstag", "Mittwoch", "Donnerstag",
            "Freitag", "Samstag", "Sonntag",
        ],
        "months": [
            "Januar", "Februar", "März", "April", "Mai", "Juni",
            "Juli", "August", "September", "Oktober", "November", "Dezember",
        ],
    },
    "fr": {
        "months_short": [
            "jan", "fév", "mar", "avr", "mai", "jun",
            "jul", "aoû", "sep", "oct", "nov", "déc",
        ],
        "weekdays_short": ["lun", "mar", "mer", "jeu", "ven", "sam", "dim"],
        "weekdays": [
            "lundi", "mardi", "mercredi", "jeudi",
            "vendredi", "samedi", "dimanche",
        ],
        "months": [
            "janvier", "février", "mars", "avril", "mai", "juin",
            "juillet", "août", "septembre", "octobre", "novembre", "décembre",
        ],
    },
}


def localize_date(dt: Union[datetime, str, None], lang: str = "en") -> str:
    """Format a date for display in the given language.

    Accepts a ``datetime`` object or an ISO date string.  Returns a
    locale-appropriate display string matching the Pelican multilingual
    plugin format:

    - English: ``February 14, 2026``  (used for articles)
    - German:  ``Mi 14. Feb 2026``
    - French:  ``vendredi 14 février 2026``
    """
    if dt is None:
        return ""

    if isinstance(dt, str):
        if not dt:
            return ""
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%d"):
            try:
                dt = datetime.strptime(dt.replace("Z", ""), fmt)
                break
            except ValueError:
                continue
        else:
            return dt  # unparseable, return as-is

    cfg = _LANG_DATE_CONFIG.get(lang, _LANG_DATE_CONFIG["en"])
    month_idx = dt.month - 1
    weekday_idx = dt.weekday()

    if lang == "de":
        wd = cfg["weekdays_short"][weekday_idx]
        mon = cfg["months_short"][month_idx]
        return f"{wd} {dt.day}. {mon} {dt.year}"
    elif lang == "fr":
        wd = cfg["weekdays"][weekday_idx]
        mon = cfg["months"][month_idx]
        return f"{wd} {dt.day} {mon} {dt.year}"
    else:
        # English: "February 14, 2026"
        mon = cfg["months"][month_idx]
        return f"{mon} {dt.day}, {dt.year}"


# ---------------------------------------------------------------------------
# Translation file cleanup
# ---------------------------------------------------------------------------

_cleanup_logger = get_logger("cleanup")


def remove_all_translations(content_root: str) -> tuple[int, int]:
    """Remove all translation files from extensions/ directories.

    Walks *content_root*, finds ``extensions/`` subdirectories, deletes
    every ``.md`` file inside them, and removes the directory if empty.

    Returns ``(removed_files, removed_dirs)``.
    """
    removed_files = 0
    removed_dirs = 0

    for root, dirs, _files in os.walk(content_root):
        if "extensions" not in dirs:
            continue

        ext_path = os.path.join(root, "extensions")
        try:
            for fname in os.listdir(ext_path):
                if fname.endswith(".md"):
                    os.remove(os.path.join(ext_path, fname))
                    removed_files += 1

            if not os.listdir(ext_path):
                os.rmdir(ext_path)
                removed_dirs += 1
        except Exception as e:
            _cleanup_logger.warning(
                f"Failed to process extensions directory {ext_path}: {e}"
            )

    _cleanup_logger.info(
        f"Cleanup complete: removed {removed_files} translation files "
        f"and {removed_dirs} empty directories"
    )
    return removed_files, removed_dirs

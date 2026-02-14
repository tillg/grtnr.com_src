"""Shared utilities: slug normalization, logging, date helpers."""

import logging
import re
import sys
import unicodedata
from datetime import datetime

from unidecode import unidecode


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

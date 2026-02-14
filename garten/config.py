"""Configuration loader: reads site.json with GARTEN_ env overrides."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

import pytz

from .utils import get_logger

logger = get_logger("config")


def _set_nested(d: dict, keys: list[str], value: str) -> None:
    """Set a nested dict value from a list of keys."""
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value


def _coerce(value: str) -> str | bool | int | list[str]:
    """Best-effort coercion of env-var strings to Python types."""
    low = value.lower()
    if low in ("true", "1", "yes"):
        return True
    if low in ("false", "0", "no"):
        return False
    if "," in value:
        return [v.strip() for v in value.split(",") if v.strip()]
    try:
        return int(value)
    except ValueError:
        return value


def load_config(site_json: Path | str = "site.json") -> dict:
    """Load site configuration from JSON file + GARTEN_ env overrides.

    Returns a plain dict (not a frozen object) so phases can read whatever
    keys they need.
    """
    site_json = Path(site_json)
    if not site_json.exists():
        raise FileNotFoundError(f"Config file not found: {site_json}")

    with open(site_json) as f:
        cfg = json.load(f)

    # --- Apply GARTEN_ env overrides ---
    for key, value in os.environ.items():
        if not key.startswith("GARTEN_"):
            continue
        # GARTEN_SITEURL -> ["siteurl"]
        # GARTEN_TRANSLATION__ENABLED -> ["translation", "enabled"]
        parts = key[len("GARTEN_"):].lower().split("__")
        _set_nested(cfg, parts, _coerce(value))

    # --- Compute runtime values ---
    tz = pytz.timezone(cfg.get("timezone", "UTC"))
    cfg["build_time"] = datetime.now(pytz.UTC).astimezone(tz).strftime(
        "%d.%m.%Y %H:%M:%S"
    )

    # Resolve paths relative to site.json location
    base = site_json.parent.resolve()
    cfg["base_path"] = base
    cfg["content_path"] = base / cfg.get("content_path", "content")
    cfg["output_path"] = base / cfg.get("output_path", "output")
    cfg["theme_path"] = base / cfg.get("theme_path", "pelicanyan")
    cfg["build_path"] = base / ".build"

    logger.info(f"Loaded config from {site_json}")
    return cfg

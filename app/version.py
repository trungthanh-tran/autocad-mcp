"""Package version resolved from installed metadata or the source pyproject."""

from __future__ import annotations

import tomllib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


def package_version() -> str:
    """Return the source version, or installed metadata outside a checkout."""
    pyproject = Path(__file__).with_name("pyproject.toml")
    if pyproject.is_file():
        with pyproject.open("rb") as stream:
            return str(tomllib.load(stream)["project"]["version"])
    for distribution in ("cadtroly", "autocad-mcp-pro"):
        try:
            return version(distribution)
        except PackageNotFoundError:
            continue
    return "0.0.0"


__version__ = package_version()

"""Runtime dependency bootstrap for the stdio MCP launcher.

The source checkout is commonly launched directly from ``.mcp.json``.  This
keeps that path usable on a fresh machine while avoiding a pip invocation when
all dependencies are already installed.  Diagnostics go to stderr because
stdout is reserved for MCP JSON-RPC.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path


REQUIRED_MODULES = {
    "fastmcp": "fastmcp",
    "ezdxf": "ezdxf",
    "pydantic": "pydantic",
    "openpyxl": "openpyxl",
    "matplotlib": "matplotlib",
    "PIL": "Pillow",
    "pymupdf": "PyMuPDF",
    "yaml": "PyYAML",
    "fastapi": "fastapi",
    "uvicorn": "uvicorn",
    "multipart": "python-multipart",
}


def ensure_runtime_dependencies() -> dict:
    """Install project dependencies only when a required import is missing."""
    if os.environ.get("CADTROLY_AUTO_INSTALL", "true").strip().lower() in {"0", "false", "no", "off"}:
        return {"installed": False, "skipped": True, "missing": []}

    missing = [package for module, package in REQUIRED_MODULES.items() if importlib.util.find_spec(module) is None]
    if not missing:
        return {"installed": False, "skipped": False, "missing": []}

    project_dir = Path(__file__).resolve().parents[2]
    print(
        "[cadtroly] Missing runtime packages: " + ", ".join(missing) + "; installing project dependencies...",
        file=sys.stderr,
        flush=True,
    )
    lock_file = project_dir / "requirements-mcp.lock"
    command = [sys.executable, "-m", "pip", "install"]
    if lock_file.is_file():
        command.extend(["-r", str(lock_file)])
    command.extend(["-e", str(project_dir)])
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "Could not install MCP dependencies. "
            f"Run manually: {' '.join(command)}"
        ) from exc
    return {"installed": True, "skipped": False, "missing": missing}


__all__ = ["ensure_runtime_dependencies"]

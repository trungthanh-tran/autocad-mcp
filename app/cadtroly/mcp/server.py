"""Điểm vào MCP của cadtroly = server.py của fork (U-C4N) đã đăng ký thêm tool cadtroly.

Chạy:  python -m cadtroly.mcp     hoặc   python server.py
Biến môi trường: CADTROLY_KHO, AUTOCAD_MCP_BACKEND=auto|com|ezdxf, TOOL_PROFILE=lean|full, TOOL_PACKS=core,arch
"""
from __future__ import annotations

import logging
import os

os.environ.setdefault("TOOL_PROFILE", "full")
os.environ.setdefault("TOOL_PACKS", "all")
os.environ.setdefault("AUTOCAD_MCP_BACKEND", "auto")

from server import mcp  # noqa: E402  (server.py ở gốc app: fork U-C4N + register cadtroly)


def build_server():
    return mcp


def main() -> None:
    logging.basicConfig(level=os.environ.get("CADTROLY_LOG", "WARNING"))
    mcp.run()


if __name__ == "__main__":
    main()

"""Trạng thái phiên của cadtroly, gắn vào lifespan của server.py (fork U-C4N)."""
from __future__ import annotations

from pathlib import Path

from .config import Config
from .kho.store import Kho
from .reader import read_dxf
from .reader.model import Drawing


class SessionState:
    """Bản vẽ đã đọc và nhóm ánh xạ, theo đường dẫn tuyệt đối."""

    def __init__(self):
        self.drawings: dict[str, Drawing] = {}
        self.groups: dict[str, list] = {}

    def key(self, path: str) -> str:
        return str(Path(path).resolve())

    def drawing(self, path: str, *, reload: bool = False) -> Drawing:
        k = self.key(path)
        if reload or k not in self.drawings:
            self.drawings[k] = read_dxf(k)
        return self.drawings[k]


def make_state() -> dict:
    cfg = Config.load()
    kho = Kho(cfg)
    kho.log("mcp", "start")
    return {"cfg": cfg, "kho": kho, "state": SessionState()}

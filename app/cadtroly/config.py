"""Cấu hình: đường dẫn kho, tuỳ chọn AutoCAD.

Kho là một thư mục trên máy người dùng. Bản cập nhật chương trình không đụng kho.
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path

KHO_SUBDIRS = ("tieu-chuan", "quy-tac", "chi-tiet", "du-an-cu", "skill", "log", "out")


def default_kho() -> Path:
    env = os.environ.get("CADTROLY_KHO")
    if env:
        return Path(env)
    return Path.home() / "CAD-kho"


@dataclass
class AcadConfig:
    backend: str = "auto"               # auto | com | ezdxf
    preview_before_run: bool = True
    undo_group_per_run: bool = True
    screenshot_after_run: bool = True
    never_autosave: bool = True
    mark_layer: str = "_AI_MARK"


@dataclass
class Config:
    kho: Path = field(default_factory=default_kho)
    acad: AcadConfig = field(default_factory=AcadConfig)
    version: str = "0.2.0"

    @property
    def path(self) -> Path:
        return self.kho / "config.json"

    def ensure_dirs(self) -> None:
        for d in KHO_SUBDIRS:
            (self.kho / d).mkdir(parents=True, exist_ok=True)

    def save(self) -> None:
        self.ensure_dirs()
        data = asdict(self)
        data["kho"] = str(self.kho)
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, kho: Path | None = None) -> "Config":
        cfg = cls(kho=kho or default_kho())
        if cfg.path.exists():
            data = json.loads(cfg.path.read_text(encoding="utf-8"))
            cfg.acad = AcadConfig(**data.get("acad", {}))
        return cfg

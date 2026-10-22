"""Cấu hình: đường dẫn kho, nguồn AI, tuỳ chọn AutoCAD.

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
class LLMConfig:
    provider: str = "claude"            # claude | gemini | openai | none
    model_fast: str = "claude-haiku-5-5"
    model_main: str = "claude-sonnet-5-5"
    model_hard: str = "claude-opus-5-5"
    fallback_provider: str | None = None
    mask_project_names: bool = True
    send_render: bool = True            # chỉ ảnh render vùng đang xem, không bao giờ gửi DWG


@dataclass
class AcadConfig:
    backend: str = "auto"               # auto | com | ezdxf
    preview_before_run: bool = True
    undo_group_per_run: bool = True
    screenshot_after_run: bool = True
    never_autosave: bool = True
    mark_layer: str = "_AI_MARK"


@dataclass
class ReportConfig:
    url: str = ""                                                 # endpoint nhận báo lỗi của dev, ví dụ https://<server>/cadtroly/report (xem tools/report_server.py)
    token: str = ""                                               # Bearer token nếu máy chủ yêu cầu
    auto_on_crash: bool = True                                    # lần mở sau khi crash: tự gửi, không hỏi
    don_vi: str = ""                                              # tên đơn vị/đối tác để dev biết ai gửi


@dataclass
class Config:
    kho: Path = field(default_factory=default_kho)
    llm: LLMConfig = field(default_factory=LLMConfig)
    acad: AcadConfig = field(default_factory=AcadConfig)
    report: ReportConfig = field(default_factory=ReportConfig)
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
            cfg.llm = LLMConfig(**data.get("llm", {}))
            cfg.acad = AcadConfig(**data.get("acad", {}))
            cfg.report = ReportConfig(**data.get("report", {}))
        return cfg

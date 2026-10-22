"""Kho tri thức: thư mục trên máy người dùng.

kho/
  tieu-chuan/   PDF tiêu chuẩn + <ten>.rules.json (bảng quy tắc đã bóc, có trạng thái duyệt)
  quy-tac/      anh-xa.json (ánh xạ layer/block), cach-tinh.json
  chi-tiet/     chi tiết tham số (LISP + mô tả JSON)
  du-an-cu/     mỗi dự án một thư mục có ho-so.json
  skill/        mỗi skill một thư mục có SKILL.md
  log/          nhật ký theo ngày
  out/          Excel, báo cáo xuất ra
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from ..config import Config
from .rules import RuleStore


class Kho:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.root = cfg.kho
        self.bundled_root = Path(__file__).resolve().parents[2] / "kho-mac-dinh"
        cfg.ensure_dirs()
        self.rules = RuleStore(self.root / "quy-tac", self.bundled_root / "quy-tac")

    def _files(self, folder: str, pattern: str) -> list[Path]:
        """User files override bundled files with the same filename."""
        out: dict[str, Path] = {}
        for base in (self.bundled_root / folder, self.root / folder):
            if base.exists():
                for f in base.glob(pattern):
                    out[f.name] = f
        return [out[name] for name in sorted(out)]

    def ruleset_path(self, ruleset: str) -> Path | None:
        name = Path(ruleset).name
        suffix = name if name.endswith(".rules.json") else f"{name}.rules.json"
        candidates = [
            self.root / "tieu-chuan" / suffix, self.root / "quy-tac" / suffix,
            self.bundled_root / "tieu-chuan" / suffix, self.bundled_root / "quy-tac" / suffix,
        ]
        return next((p for p in candidates if p.exists()), None)

    # ---- tiêu chuẩn ----
    def standards(self) -> list[dict]:
        out = []
        for f in self._files("tieu-chuan", "*.rules.json"):
            d = json.loads(f.read_text(encoding="utf-8"))
            rules = d.get("rules", [])
            out.append({
                "id": d.get("id", f.stem.replace(".rules", "")),
                "ten": d.get("ten", f.stem),
                "hieu_luc": d.get("hieu_luc", "unknown"),
                "thay_boi": d.get("thay_boi"),
                "so_quy_tac": len(rules),
                "cho_duyet": sum(1 for r in rules if not r.get("duyet")),
                "file": str(f),
            })
        return out

    def rulesets(self) -> list[dict]:
        """All bundled and user rule files, including company rules."""
        out = []
        for f in self._files("tieu-chuan", "*.rules.json") + self._files("quy-tac", "*.rules.json"):
            data = json.loads(f.read_text(encoding="utf-8"))
            rules = data.get("rules", [])
            out.append({
                "id": data.get("id", f.stem.replace(".rules", "")),
                "ten": data.get("ten", f.stem),
                "hieu_luc": data.get("hieu_luc", "unknown"),
                "so_quy_tac": len(rules),
                "cho_duyet": sum(1 for r in rules if not r.get("duyet")),
                "file": str(f),
            })
        return out

    def load_standard(self, std_id: str) -> dict:
        f = self.ruleset_path(std_id)
        if f is None:
            raise FileNotFoundError(std_id)
        return json.loads(f.read_text(encoding="utf-8"))

    def save_standard(self, data: dict) -> Path:
        f = self.root / "tieu-chuan" / f"{data['id']}.rules.json"
        f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return f

    # ---- chi tiết ----
    def details(self) -> list[dict]:
        out = []
        for f in sorted((self.root / "chi-tiet").glob("*.json")):
            d = json.loads(f.read_text(encoding="utf-8"))
            d["file"] = str(f)
            out.append(d)
        return out

    # ---- dự án cũ ----
    def projects(self) -> list[dict]:
        out = []
        for d in sorted((self.root / "du-an-cu").iterdir()):
            f = d / "ho-so.json"
            if d.is_dir() and f.exists():
                p = json.loads(f.read_text(encoding="utf-8"))
                p["dir"] = str(d)
                out.append(p)
        return out

    # ---- skill ----
    def skills(self) -> list[dict]:
        out = []
        dirs: dict[str, Path] = {}
        for base in (self.bundled_root / "skill", self.root / "skill"):
            if base.exists():
                for d in base.iterdir():
                    if d.is_dir():
                        dirs[d.name] = d
        for d in (dirs[name] for name in sorted(dirs)):
            md = d / "SKILL.md"
            if d.is_dir() and md.exists():
                meta = _frontmatter(md.read_text(encoding="utf-8"))
                meta.setdefault("name", d.name)
                meta["dir"] = str(d)
                meta["enabled"] = (d / ".disabled").exists() is False
                out.append(meta)
        return out

    def set_skill(self, name: str, enabled: bool) -> None:
        flag = self.root / "skill" / name / ".disabled"
        if enabled and flag.exists():
            flag.unlink()
        elif not enabled:
            flag.parent.mkdir(parents=True, exist_ok=True)
            flag.write_text("")

    def skill_path(self, name: str) -> Path | None:
        for base in (self.root / "skill", self.bundled_root / "skill"):
            path = base / name / "SKILL.md"
            if path.exists():
                return path
        return None

    # ---- nhật ký ----
    def log(self, _kind: str, _msg: str, **data) -> None:
        f = self.root / "log" / f"{datetime.now():%Y-%m-%d}.log"
        line = {"t": datetime.now().isoformat(timespec="seconds"), "kind": _kind, "msg": _msg, **data}
        with f.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(line, ensure_ascii=False) + "\n")

    def status(self) -> dict:
        return {
            "kho": str(self.root),
            "tieu_chuan": len(self.standards()),
            "quy_tac": len(self.rules.rules),
            "chi_tiet": len(self.details()),
            "du_an_cu": len(self.projects()),
            "skill": [s["name"] for s in self.skills() if s["enabled"]],
        }


def _frontmatter(text: str) -> dict:
    meta: dict = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end > 0:
            for line in text[3:end].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
    return meta

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
import re
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
                "nganh": data.get("nganh", data.get("industry", "unknown")),
                "phien_ban": data.get("phien_ban", data.get("version", "unknown")),
                "nguon": data.get("nguon", data.get("source", "unknown")),
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
        standard_id = str(data.get("id", "")).strip().lower()
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,63}", standard_id):
            raise ValueError("standard id must be ASCII kebab-case, 2-64 characters")
        if not isinstance(data.get("rules"), list):
            raise ValueError("standard rules must be a list")
        data = dict(data)
        data["id"] = standard_id
        data.setdefault("nganh", "unknown")
        data.setdefault("phien_ban", data.get("version", "unknown"))
        data.setdefault("nguon", "user")
        f = self.root / "tieu-chuan" / f"{standard_id}.rules.json"
        f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return f

    def standard_list(self, industry: str | None = None) -> list[dict]:
        """List standards/rules with an optional industry filter."""
        wanted = industry.strip().lower() if industry else None
        rows = self.rulesets()
        if wanted:
            rows = [r for r in rows if str(r.get("nganh", r.get("industry", "unknown"))).lower() == wanted]
        return rows

    def standard_add(self, data: dict, *, overwrite: bool = False) -> Path:
        standard_id = str(data.get("id", "")).strip().lower()
        existing = self.ruleset_path(standard_id) if standard_id else None
        target = self.root / "tieu-chuan" / f"{standard_id}.rules.json"
        if existing is not None and not (overwrite and target.exists()):
            raise FileExistsError(f"standard already exists: {standard_id}")
        return self.save_standard(data)

    def standard_delete(self, standard_id: str) -> Path:
        clean = str(standard_id).strip().lower()
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,63}", clean):
            raise ValueError("standard id must be ASCII kebab-case, 2-64 characters")
        for folder in (self.root / "tieu-chuan", self.root / "quy-tac"):
            target = folder / f"{clean}.rules.json"
            if target.exists():
                target.unlink()
                return target
        if self.ruleset_path(clean) is not None:
            raise PermissionError("bundled standards cannot be deleted")
        raise FileNotFoundError(clean)

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

    def add_skill(self, name: str, content: str, *, overwrite: bool = False) -> Path:
        """Add a user-authored SKILL.md without allowing path traversal or code files."""
        clean = str(name).strip().lower()
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,63}", clean):
            raise ValueError("skill name must be ASCII kebab-case, 2-64 characters")
        if not isinstance(content, str) or not content.strip():
            raise ValueError("skill content must not be empty")
        if len(content.encode("utf-8")) > 128_000:
            raise ValueError("skill content is limited to 128 KB")
        if not content.lstrip().startswith("---"):
            raise ValueError("skill content must start with YAML frontmatter (---)")
        target = self.root / "skill" / clean / "SKILL.md"
        existing = self.skill_path(clean)
        if existing is not None and not (overwrite and target.exists()):
            raise FileExistsError(f"skill already exists: {clean}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
        return target

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

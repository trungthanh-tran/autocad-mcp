"""Lớp dịch vụ dùng chung cho MCP tool, web UI và chat: không phụ thuộc FastMCP hay FastAPI."""
from __future__ import annotations

import json
from pathlib import Path

from .check.engine import check_drawing, load_ruleset, summarize
from .config import Config
from .kho.store import Kho
from .state import SessionState
from .takeoff.calc import compute, stats
from .takeoff.excel import export_excel
from .takeoff.mapper import apply_decision, propose_mapping


class Service:
    def __init__(self, cfg: Config | None = None):
        self.cfg = cfg or Config.load()
        self.kho = Kho(self.cfg)
        self.state = SessionState()

    # ---- bản vẽ ----
    def read(self, path: str, reload: bool = False) -> dict:
        d = self.state.drawing(path, reload=reload)
        return d.summary() | {"layers_list": d.layers, "blocks_list": d.block_defs}

    # ---- luồng A ----
    def propose(self, path: str) -> dict:
        d = self.state.drawing(path)
        groups = propose_mapping(d, self.kho.rules)
        self.state.groups[self.state.key(path)] = groups
        self.kho.log("takeoff", "propose", path=path, stats=stats(groups))
        return {"stats": stats(groups), "groups": [g.to_dict() for g in groups]}

    def _groups(self, path: str):
        return self.state.groups.get(self.state.key(path)) or propose_mapping(self.state.drawing(path), self.kho.rules)

    def decide(self, path: str, kind: str, name: str, cong_tac: str, don_vi: str, cach_tinh: str,
               tham_so: dict | None = None, save_rule: bool = True) -> dict:
        groups = self._groups(path)
        for g in groups:
            if g.kind == kind and g.name == name:
                apply_decision(g, self.kho.rules, cong_tac=cong_tac, don_vi=don_vi, cach_tinh=cach_tinh,
                               tham_so=tham_so, save=save_rule)
                self.state.groups[self.state.key(path)] = groups
                self.kho.log("takeoff", "decide", kind=kind, name=name, cong_tac=cong_tac, saved=save_rule)
                return {"ok": True, "group": g.to_dict(), "stats": stats(groups), "rules_total": len(self.kho.rules.rules)}
        raise KeyError(f"Không có nhóm {kind} '{name}'")

    def accept_all_b(self, path: str, save_rule: bool = True) -> dict:
        """Duyệt nhanh mọi nhóm B có công tác đề xuất (người dùng bấm 'Duyệt tất cả B')."""
        n = 0
        for g in self._groups(path):
            if g.tin_cay == "B" and g.cong_tac and not g.skip:
                apply_decision(g, self.kho.rules, cong_tac=g.cong_tac, don_vi=g.don_vi, cach_tinh=g.cach_tinh,
                               tham_so=g.tham_so, save=save_rule)
                n += 1
        return {"ok": True, "accepted": n, "stats": stats(self._groups(path))}

    def compute(self, path: str, height_m: float | None = None, tru_lo_cua: float = 0.0) -> dict:
        d = self.state.drawing(path)
        rows = compute(d, self._groups(path), height_m=height_m, overrides={"tru_lo_cua": tru_lo_cua})
        return {"rows": [{"cong_tac": r.cong_tac, "don_vi": r.don_vi, "khoi_luong": r.khoi_luong,
                          "cach_tinh": r.cach_tinh, "nguon": r.nguon, "tin_cay": r.tin_cay,
                          "ghi_chu": r.ghi_chu, "so_handle": len(r.handles),
                          "zoom": next((c.get("vi_tri") for c in r.chi_tiet if c.get("vi_tri")), None)} for r in rows]}

    def export(self, path: str, out: str | None = None, height_m: float | None = None) -> dict:
        d = self.state.drawing(path)
        groups = self._groups(path)
        rows = compute(d, groups, height_m=height_m)
        out_p = Path(out) if out else self.cfg.kho / "out" / (Path(path).stem + ".xlsx")
        export_excel(d, groups, rows, out_p, meta={"stats": stats(groups)})
        for g in groups:
            if g.rule:
                self.kho.rules.bump(g.rule)
        self.kho.log("takeoff", "export", path=path, out=str(out_p))
        return {"ok": True, "excel": str(out_p), "stats": stats(groups), "rows": len(rows)}

    def run_folder(self, folder: str, height_m: float | None = None) -> dict:
        p = Path(folder)
        files = sorted(p.glob("*.dxf")) if p.is_dir() else [p]
        res = []
        for f in files:
            try:
                self.propose(str(f))
                res.append({"file": str(f)} | self.export(str(f), height_m=height_m))
            except Exception as exc:
                res.append({"file": str(f), "error": str(exc)})
        return {"count": len(res), "results": res}

    # ---- luồng D ----
    def rulesets(self) -> list[dict]:
        extra = [{"id": f.stem.replace(".rules", ""), "ten": json.loads(f.read_text(encoding="utf-8")).get("ten", f.stem),
                  "file": str(f), "hieu_luc": "co"} for f in (self.kho.root / "quy-tac").glob("*.rules.json")]
        return self.kho.standards() + extra

    def check(self, path: str, ruleset: str, include_unapproved: bool = False) -> dict:
        rp = Path(ruleset)
        if not rp.exists():
            for c in (self.kho.root / "tieu-chuan" / f"{ruleset}.rules.json", self.kho.root / "quy-tac" / f"{ruleset}.rules.json"):
                if c.exists():
                    rp = c
                    break
            else:
                raise KeyError(f"Không thấy bộ quy tắc '{ruleset}'")
        rs = load_ruleset(rp)
        fs = check_drawing(self.state.drawing(path), rs, only_approved=not include_unapproved)
        self.kho.log("check", "run", path=path, ruleset=rs.id, **summarize(fs))
        return {"ruleset": rs.id, "ten": rs.ten, "summary": summarize(fs), "findings": [f.to_dict() for f in fs]}

    # ---- kho ----
    def status(self) -> dict:
        return self.kho.status() | {"llm": self.cfg.llm.provider, "model": self.cfg.llm.model_main,
                                    "version": self.cfg.version, "config": str(self.cfg.path)}

    def recent(self, n: int = 10) -> list[dict]:
        logs = sorted((self.kho.root / "log").glob("*.log"), reverse=True)
        out = []
        for f in logs:
            for line in reversed(f.read_text(encoding="utf-8").splitlines()):
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if d.get("kind") in ("takeoff", "check") and d.get("msg") in ("export", "run"):
                    out.append(d)
                if len(out) >= n:
                    return out
        return out

"""Tool riêng của cadtroly, đăng ký lên server.py (fork U-C4N) qua register(mcp).

  drawing_read / drawing_entities      đọc bản vẽ thành số liệu (reader riêng, ezdxf)
  takeoff_propose/decide/compute/export/run   luồng A bóc khối lượng ra Excel có truy vết
  check_rulesets / check_run           luồng D kiểm tra theo bộ quy tắc
  kho_*                                kho tri thức, skill
Các tool AutoCAD (drawing_open, entity_*, layer_*, system_run_lisp, view_screenshot, transaction_*…)
là của upstream trong server.py, dùng chung lifespan: ctx.lifespan_context có backend + cfg + kho + state.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Annotated

from fastmcp import Context, FastMCP
from fastmcp.exceptions import ToolError

from ..check.engine import check_drawing, load_ruleset, summarize
from ..takeoff.calc import compute, stats
from ..takeoff.excel import export_excel
from ..takeoff.mapper import apply_decision, propose_mapping

log = logging.getLogger("cadtroly")

CADTROLY_TOOL_NAMES = frozenset({
    "drawing_read", "drawing_entities",
    "takeoff_propose", "takeoff_decide", "takeoff_compute", "takeoff_export", "takeoff_run",
    "check_rulesets", "check_run",
    "kho_status", "kho_rules_export", "kho_rules_import", "kho_skills", "kho_skill_toggle",
})


def _ctx(ctx: Context) -> dict:
    lc = ctx.lifespan_context if ctx is not None else None
    if not lc or "kho" not in lc:
        raise ToolError("Server chưa sẵn sàng (lifespan).")
    return lc


def register(mcp: FastMCP) -> None:
    """Đăng ký tool cadtroly lên server (server.py của fork gọi hàm này)."""
    # ------------------------------------------------------------------ đọc
    @mcp.tool(tags={"read"}, annotations={"readOnlyHint": True})
    async def drawing_read(path: Annotated[str, "Đường dẫn DXF (DWG cần ODA converter)"],
                           ctx: Context = None) -> dict:
        """Đọc bản vẽ thành số liệu: layer, block, số đối tượng, đơn vị. Không gửi gì đi."""
        st = _ctx(ctx)["state"]
        d = st.drawing(path)
        return d.summary() | {"layers_list": d.layers, "blocks_list": d.block_defs}

    @mcp.tool(tags={"read"}, annotations={"readOnlyHint": True})
    async def drawing_entities(path: str, layer: str | None = None, block: str | None = None,
                               kind: str | None = None, limit: int = 100, ctx: Context = None) -> dict:
        """Liệt kê đối tượng theo layer/block/loại kèm handle, toạ độ, chiều dài, diện tích, text."""
        d = _ctx(ctx)["state"].drawing(path)
        out = []
        for e in d.entities:
            if layer and e.layer != layer:
                continue
            if block and e.block_name != block:
                continue
            if kind and e.dxftype != kind:
                continue
            out.append({"handle": e.handle, "type": e.dxftype, "layer": e.layer, "block": e.block_name,
                        "point": e.point, "length": e.length, "area": e.area, "text": e.text,
                        "attribs": e.attribs or None, "accuracy": e.accuracy})
            if len(out) >= limit:
                break
        return {"count": len(out), "entities": out}

    # --------------------------------------------------------------- takeoff
    @mcp.tool(tags={"takeoff"})
    async def takeoff_propose(path: str, ctx: Context = None) -> dict:
        """Bước 2 luồng A: gom theo layer/block, đề xuất công tác với tin cậy A/B/C. B/C cần kỹ sư quyết."""
        lc = _ctx(ctx)
        st, kho = lc["state"], lc["kho"]
        d = st.drawing(path)
        groups = propose_mapping(d, kho.rules)
        st.groups[st.key(path)] = groups
        kho.log("takeoff", "propose", path=path, stats=stats(groups))
        return {"stats": stats(groups), "groups": [g.to_dict() for g in groups],
                "huong_dan": "Gọi takeoff_decide cho từng nhóm B/C với cong_tac/don_vi/cach_tinh. "
                             "cach_tinh: count|length|area|volume_by_height|area_by_height|skip"}

    @mcp.tool(tags={"takeoff"})
    async def takeoff_decide(path: str, kind: Annotated[str, "layer | block"], name: str, cong_tac: str,
                             don_vi: str, cach_tinh: str, tham_so: dict | None = None,
                             save_rule: Annotated[bool, "Lưu thành quy tắc đơn vị để lần sau tự áp"] = True,
                             ctx: Context = None) -> dict:
        """Kỹ sư xác nhận ánh xạ một nhóm. Mặc định lưu thành quy tắc đơn vị (không train, chỉ ghi file)."""
        lc = _ctx(ctx)
        st, kho = lc["state"], lc["kho"]
        groups = st.groups.get(st.key(path)) or propose_mapping(st.drawing(path), kho.rules)
        for g in groups:
            if g.kind == kind and g.name == name:
                apply_decision(g, kho.rules, cong_tac=cong_tac, don_vi=don_vi, cach_tinh=cach_tinh,
                               tham_so=tham_so, save=save_rule)
                st.groups[st.key(path)] = groups
                kho.log("takeoff", "decide", kind=kind, name=name, cong_tac=cong_tac, saved=save_rule)
                return {"ok": True, "group": g.to_dict(), "rules_total": len(kho.rules.rules)}
        raise ToolError(f"Không có nhóm {kind} '{name}' trong bản vẽ này.")

    @mcp.tool(tags={"takeoff"})
    async def takeoff_compute(path: str, height_m: Annotated[float | None, "Chiều cao tầng (m); bỏ trống = tìm text H="] = None,
                              tru_lo_cua_m3: float = 0.0, ctx: Context = None) -> dict:
        """Bước 3 luồng A: tính khối lượng. Mỗi dòng có nguồn truy vết và tin cậy; thiếu dữ liệu thì để trống."""
        lc = _ctx(ctx)
        st, kho = lc["state"], lc["kho"]
        d = st.drawing(path)
        groups = st.groups.get(st.key(path)) or propose_mapping(d, kho.rules)
        rows = compute(d, groups, height_m=height_m, overrides={"tru_lo_cua": tru_lo_cua_m3})
        return {"rows": [{"cong_tac": r.cong_tac, "don_vi": r.don_vi, "khoi_luong": r.khoi_luong,
                          "cach_tinh": r.cach_tinh, "nguon": r.nguon, "tin_cay": r.tin_cay,
                          "ghi_chu": r.ghi_chu, "so_handle": len(r.handles)} for r in rows]}

    @mcp.tool(tags={"takeoff"})
    async def takeoff_export(path: str, out: Annotated[str | None, "File .xlsx; bỏ trống = kho/out/<ten>.xlsx"] = None,
                             height_m: float | None = None, ctx: Context = None) -> dict:
        """Bước 4 luồng A: xuất Excel 4 sheet (Khối lượng, Chi tiết từng handle + lệnh zoom, Ánh xạ, Kiểm soát)."""
        lc = _ctx(ctx)
        st, kho, cfg = lc["state"], lc["kho"], lc["cfg"]
        d = st.drawing(path)
        groups = st.groups.get(st.key(path)) or propose_mapping(d, kho.rules)
        rows = compute(d, groups, height_m=height_m)
        out_p = Path(out) if out else cfg.kho / "out" / (Path(path).stem + ".xlsx")
        export_excel(d, groups, rows, out_p, meta={"stats": stats(groups)})
        for g in groups:
            if g.rule:
                kho.rules.bump(g.rule)
        kho.log("takeoff", "export", path=path, out=str(out_p))
        return {"ok": True, "excel": str(out_p), "stats": stats(groups), "rows": len(rows)}

    @mcp.tool(tags={"takeoff"})
    async def takeoff_run(path: Annotated[str, "File DXF hoặc thư mục"], height_m: float | None = None,
                          ctx: Context = None) -> dict:
        """Chạy trọn luồng A không hỏi (dùng quy tắc đã có). Thư mục → mỗi file một Excel. Nhóm B/C vẫn ghi rõ trong Excel."""
        lc = _ctx(ctx)
        st, kho, cfg = lc["state"], lc["kho"], lc["cfg"]
        p = Path(path)
        files = sorted(p.glob("*.dxf")) if p.is_dir() else [p]
        results = []
        for f in files:
            try:
                d = st.drawing(str(f))
                groups = propose_mapping(d, kho.rules)
                rows = compute(d, groups, height_m=height_m)
                out_p = cfg.kho / "out" / (f.stem + ".xlsx")
                export_excel(d, groups, rows, out_p, meta={"stats": stats(groups)})
                results.append({"file": str(f), "excel": str(out_p), "stats": stats(groups)})
            except Exception as exc:
                results.append({"file": str(f), "error": str(exc)})
        return {"count": len(results), "results": results}

    # ----------------------------------------------------------------- check
    @mcp.tool(tags={"check"}, annotations={"readOnlyHint": True})
    async def check_rulesets(ctx: Context = None) -> dict:
        """Liệt kê bộ quy tắc trong kho (tiêu chuẩn đã bóc + chuẩn công ty), kèm hiệu lực và số dòng chờ duyệt."""
        kho = _ctx(ctx)["kho"]
        return {"rulesets": kho.rulesets()}

    @mcp.tool(tags={"check"}, annotations={"readOnlyHint": True})
    async def check_run(path: str, ruleset: Annotated[str, "id bộ quy tắc hoặc đường dẫn .rules.json"],
                        include_unapproved: bool = False, ctx: Context = None) -> dict:
        """Luồng D: rà bản vẽ theo bộ quy tắc. Trả về từng vấn đề kèm điều khoản, handle, vị trí, có tự sửa được không."""
        lc = _ctx(ctx)
        st, kho = lc["state"], lc["kho"]
        rp = Path(ruleset)
        if not rp.exists():
            rp = kho.ruleset_path(ruleset)
            if rp is None:
                raise ToolError(f"Không thấy bộ quy tắc '{ruleset}'. Gọi check_rulesets để xem danh sách.")
        rs = load_ruleset(rp)
        d = st.drawing(path)
        findings = check_drawing(d, rs, only_approved=not include_unapproved)
        kho.log("check", "run", path=path, ruleset=rs.id, **summarize(findings))
        return {"ruleset": rs.id, "summary": summarize(findings), "findings": [f.to_dict() for f in findings]}

    # ------------------------------------------------------------------- kho
    @mcp.tool(tags={"kho"}, annotations={"readOnlyHint": True})
    async def kho_status(ctx: Context = None) -> dict:
        """Tình trạng kho tri thức, backend AutoCAD, nguồn AI."""
        lc = _ctx(ctx)
        b = lc["backend"]
        return lc["kho"].status() | {"backend": getattr(b, "name", None), "backend_error": lc.get("init_error"),
                                     "llm": lc["cfg"].llm.provider, "version": lc["cfg"].version}

    @mcp.tool(tags={"kho"}, annotations={"readOnlyHint": True})
    async def kho_rules_export(ctx: Context = None) -> dict:
        """Xuất quy tắc ánh xạ của đơn vị (chỉ quy tắc, không bản vẽ) để chia sẻ."""
        return {"rules": _ctx(ctx)["kho"].rules.export()}

    @mcp.tool(tags={"kho"})
    async def kho_rules_import(rules: list[dict], ctx: Context = None) -> dict:
        """Nhập quy tắc ánh xạ từ nơi khác (ghi đè theo pattern)."""
        n = _ctx(ctx)["kho"].rules.import_rules(rules)
        return {"imported": n}

    @mcp.tool(tags={"kho"}, annotations={"readOnlyHint": True})
    async def kho_skills(ctx: Context = None) -> dict:
        """Skill chuyên ngành trong kho/skill (mỗi thư mục một SKILL.md), bật/tắt."""
        return {"skills": _ctx(ctx)["kho"].skills()}

    @mcp.tool(tags={"kho"})
    async def kho_skill_toggle(name: str, enabled: bool, ctx: Context = None) -> dict:
        """Bật/tắt một skill."""
        _ctx(ctx)["kho"].set_skill(name, enabled)
        return {"ok": True, "skills": _ctx(ctx)["kho"].skills()}

    @mcp.resource("cadtroly://skill/{name}")
    async def skill_text(name: str, ctx: Context = None) -> str:
        """Nội dung SKILL.md của một skill (hướng dẫn cho AI theo ngành)."""
        p = _ctx(ctx)["kho"].skill_path(name)
        return p.read_text(encoding="utf-8") if p else f"Không có skill {name}"


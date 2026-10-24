"""Tool riêng của cadtroly, đăng ký lên server.py (fork U-C4N) qua register(mcp).

  drawing_read / drawing_entities      đọc bản vẽ thành số liệu (reader riêng, ezdxf)
  takeoff_propose/decide/compute/export/run   luồng A bóc khối lượng ra Excel có truy vết
  takeoff_earthwork / takeoff_rebar    cầu đường: đào đắp từ trắc ngang, thống kê thép từ ghi chú
  approval_execute                     chạy thao tác phá huỷ đã được người dùng đồng ý (approval.py)
  check_rulesets / check_run           luồng D kiểm tra theo bộ quy tắc
  knowledge_*                          kho tri thức, skill
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
from ..takeoff.calc import compute, stats, takeoff_questions
from ..takeoff.civil import earthwork, rebar, rebar_by_diameter, rebar_questions
from ..takeoff.excel import export_earthwork, export_excel, export_rebar
from ..takeoff.mapper import apply_decision, propose_mapping

log = logging.getLogger("cadtroly")

# Gửi kèm mọi kết quả có câu hỏi: tool không tự quyết chỗ không rõ, LLM cũng không được tự trả lời thay người dùng.
_ASK = ("Còn câu hỏi trong can_hoi. Hỏi người dùng đúng nội dung từng câu, chờ trả lời, rồi gọi lại tool với tham số "
        "tương ứng. Không tự chọn đáp án, không suy từ bản vẽ khác hay kinh nghiệm.")

CADTROLY_TOOL_NAMES = frozenset({
    "drawing_read", "drawing_entities",
    "takeoff_propose", "takeoff_decide", "takeoff_compute", "takeoff_export", "takeoff_run",
    "takeoff_earthwork", "takeoff_rebar",
    "check_rulesets", "check_run",
    "knowledge_industries", "knowledge_standards", "knowledge_standard_add", "knowledge_standard_delete",
    "knowledge_status", "knowledge_rules_export", "knowledge_rules_import", "knowledge_skills", "knowledge_skill_toggle", "knowledge_skill_add",
    "kho_industries", "kho_standards", "kho_standard_add", "kho_standard_delete",
    "kho_status", "kho_rules_export", "kho_rules_import", "kho_skills", "kho_skill_toggle", "kho_skill_add",
    "approval_execute",
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
                             ma_dinh_muc: Annotated[str, "Mã hiệu định mức TT 38/2026/TT-BXD, ví dụ do kỹ sư "
                                                         "đọc từ bảng định mức; không tự bịa"] = "",
                             ctx: Context = None) -> dict:
        """Kỹ sư xác nhận ánh xạ một nhóm. Mặc định lưu thành quy tắc đơn vị (không train, chỉ ghi file)."""
        lc = _ctx(ctx)
        st, kho = lc["state"], lc["kho"]
        groups = st.groups.get(st.key(path)) or propose_mapping(st.drawing(path), kho.rules)
        for g in groups:
            if g.kind == kind and g.name == name:
                apply_decision(g, kho.rules, cong_tac=cong_tac, don_vi=don_vi, cach_tinh=cach_tinh,
                               tham_so=tham_so, ma_dinh_muc=ma_dinh_muc, save=save_rule)
                st.groups[st.key(path)] = groups
                kho.log("takeoff", "decide", kind=kind, name=name, cong_tac=cong_tac, saved=save_rule)
                return {"ok": True, "group": g.to_dict(), "rules_total": len(kho.rules.rules)}
        raise ToolError(f"Không có nhóm {kind} '{name}' trong bản vẽ này.")

    @mcp.tool(tags={"takeoff"})
    async def takeoff_compute(path: str, height_m: Annotated[float | None, "Chiều cao tầng (m); bỏ trống = tìm text H="] = None,
                              tru_lo_cua_m3: float = 0.0,
                              chap_nhan_B: Annotated[bool, "Chỉ khi người dùng nói rõ chấp nhận mọi đề xuất B"] = False,
                              ctx: Context = None) -> dict:
        """Bước 3 luồng A: tính khối lượng. Mỗi dòng có nguồn truy vết và tin cậy; thiếu dữ liệu thì để trống."""
        lc = _ctx(ctx)
        st, kho = lc["state"], lc["kho"]
        d = st.drawing(path)
        groups = st.groups.get(st.key(path)) or propose_mapping(d, kho.rules)
        rows = compute(d, groups, height_m=height_m, overrides={"tru_lo_cua": tru_lo_cua_m3}, chap_nhan_B=chap_nhan_B)
        hoi = takeoff_questions(rows)
        return {"can_hoi": hoi, "huong_dan": _ASK if hoi else "", "rows": [{"ma_dinh_muc": r.ma_dinh_muc, "cong_tac": r.cong_tac, "don_vi": r.don_vi,
                          "khoi_luong": r.khoi_luong,
                          "cach_tinh": r.cach_tinh, "nguon": r.nguon, "tin_cay": r.tin_cay,
                          "ghi_chu": r.ghi_chu, "so_handle": len(r.handles)} for r in rows]}

    @mcp.tool(tags={"takeoff"})
    async def takeoff_export(path: str, out: Annotated[str | None, "File .xlsx; bỏ trống = kho/out/<ten>.xlsx"] = None,
                             height_m: float | None = None,
                             chap_nhan_B: Annotated[bool, "Chỉ khi người dùng nói rõ chấp nhận mọi đề xuất B"] = False,
                             xuat_khi_con_hoi: Annotated[bool, "Xuất nháp dù còn câu hỏi (dòng chờ để trống)"] = False,
                             ctx: Context = None) -> dict:
        """Bước 4 luồng A: xuất Excel 4 sheet (Khối lượng, Chi tiết từng handle + lệnh zoom, Ánh xạ, Kiểm soát)."""
        lc = _ctx(ctx)
        st, kho, cfg = lc["state"], lc["kho"], lc["cfg"]
        d = st.drawing(path)
        groups = st.groups.get(st.key(path)) or propose_mapping(d, kho.rules)
        rows = compute(d, groups, height_m=height_m, chap_nhan_B=chap_nhan_B)
        hoi = takeoff_questions(rows)
        if hoi and not xuat_khi_con_hoi:
            return {"ok": False, "excel": None, "can_hoi": hoi, "huong_dan": _ASK, "stats": stats(groups)}
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
        """Chạy trọn luồng A theo quy tắc đã có. Thư mục → mỗi file một Excel nháp: nhóm B (đề xuất) và C để trống,
        ghi lý do chờ xác nhận; câu hỏi từng file trả về trong can_hoi."""
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
                results.append({"file": str(f), "excel": str(out_p), "stats": stats(groups),
                                "can_hoi": takeoff_questions(rows)})
            except Exception as exc:
                results.append({"file": str(f), "error": str(exc)})
        return {"count": len(results), "results": results}

    # ------------------------------------------------------------ cầu đường
    @mcp.tool(tags={"takeoff"})
    async def takeoff_earthwork(
        path: Annotated[str, "Bản vẽ trắc ngang DXF/DWG (Nova-TDN, bản vẽ tay…)"],
        out: Annotated[str | None, "File .xlsx; bỏ trống = không xuất, chỉ trả số liệu"] = None,
        ma_dinh_muc: Annotated[dict | None, "Mã định mức theo loại: {'dao': '...', 'dap_k95': '...'}"] = None,
        thieu_dien_tich: Annotated[str | None, "Trả lời câu hỏi: 'bang_0' | 'bo_doan'. Chỉ điền theo người dùng"] = None,
        cong_trung: Annotated[bool | None, "Trả lời câu hỏi: cộng hai giá trị cùng loại ở một trắc ngang"] = None,
        gan: Annotated[dict | None, "Trả lời câu hỏi: {handle diện tích: 'Km0+020'}"] = None,
        gan_o_so: Annotated[dict | None, "Trả lời câu hỏi: {handle ô nhãn: handle ô số}"] = None,
        xuat_khi_con_hoi: Annotated[bool, "Xuất Excel nháp dù còn câu hỏi (ô chờ trả lời để trống)"] = False,
        ctx: Context = None,
    ) -> dict:
        """Đào đắp từ trắc ngang: đọc text lý trình (Km0+100) và diện tích (F đào = …, ô 'Diện tích đắp'),
        tính V = (F1+F2)/2 × L giữa hai trắc ngang liền kề. Mỗi số có handle nguồn và tin cậy A/B/C.
        Không suy diễn: chỗ không rõ trả về can_hoi — hỏi người dùng nguyên văn, gọi lại với câu trả lời."""
        lc = _ctx(ctx)
        st, kho = lc["state"], lc["kho"]
        d = st.drawing(path)
        res = earthwork(d, thieu_dien_tich=thieu_dien_tich, cong_trung=cong_trung, gan=gan, gan_o_so=gan_o_so)
        hoi = res["can_hoi"]
        xl = None
        if out and (not hoi or xuat_khi_con_hoi):
            xl = str(export_earthwork(d, res, out, ma_dinh_muc=ma_dinh_muc))
        kho.log("takeoff", "earthwork", path=path, sections=len(res["sections"]), totals=res["totals"], out=xl,
                can_hoi=len(hoi))
        return {
            "can_hoi": hoi,
            "huong_dan": _ASK if hoi else "",
            "totals_m3": {res["names"].get(k, k): v for k, v in res["totals"].items()},
            "chua_du": [res["names"].get(k, k) for k in res.get("incomplete", [])],
            "sections": [{"ly_trinh": s.label, "m": s.station_m, "handle": s.handle, "F_m2": s.areas,
                          "tin_cay": s.tin_cay, "ghi_chu": s.ghi_chu} for s in res["sections"]],
            "segments": res["segments"], "warnings": res["warnings"], "excel": xl,
        }

    @mcp.tool(tags={"takeoff"})
    async def takeoff_rebar(
        path: Annotated[str, "Bản vẽ cốt thép DXF/DWG"],
        out: Annotated[str | None, "File .xlsx; bỏ trống = không xuất"] = None,
        ma_dinh_muc: Annotated[dict | None, "Mã định mức theo đường kính: {'16': '...'}"] = None,
        don_vi_L: Annotated[str | None, "Trả lời câu hỏi: 'mm' | 'm' cho L= không ghi đơn vị"] = None,
        trung_lap: Annotated[str | None, "Trả lời câu hỏi: 'mot_lan' | 'tung_cho' cho ghi chú lặp"] = None,
        xuat_khi_con_hoi: Annotated[bool, "Xuất Excel nháp dù còn câu hỏi (dòng chờ trả lời để trống)"] = False,
        ctx: Context = None,
    ) -> dict:
        """Thống kê thép từ ghi chú 'N1 12Ø16 L=5200' / '6%%c22 L=12.5m' / 'F1-D25-125': số thanh × dài ×
        khối lượng 1 m dài theo Bảng 2 TCVN 1651-2:2018 (thép trơn: TCVN 1651-1:2018, cùng giá trị).
        Không suy diễn: L= không ghi đơn vị, ghi chú lặp ở nhiều chỗ → can_hoi, khối lượng để trống tới khi trả lời."""
        lc = _ctx(ctx)
        st, kho = lc["state"], lc["kho"]
        d = st.drawing(path)
        items = rebar(d, trung_lap=trung_lap, don_vi_L=don_vi_L)
        hoi = rebar_questions(items)
        by_d = rebar_by_diameter(items)
        xl = None
        if out and (not hoi or xuat_khi_con_hoi):
            xl = str(export_rebar(d, items, by_d, out, ma_dinh_muc=ma_dinh_muc))
        kho.log("takeoff", "rebar", path=path, items=len(items), out=xl, can_hoi=len(hoi))
        return {
            "can_hoi": hoi,
            "huong_dan": _ASK if hoi else "",
            "tong_kg": round(sum(g["tong_kg"] for g in by_d.values()), 2),
            "tong_chua_du": any(g["thieu"] for g in by_d.values()),
            "theo_duong_kinh": {f"Ø{k}": v for k, v in by_d.items()},
            "items": [{"so_hieu": i.so_hieu, "d_mm": i.d_mm, "so_thanh": i.so_thanh, "dai_m": i.dai_m,
                       "tong_kg": i.tong_kg, "tin_cay": i.tin_cay, "ghi_chu": i.ghi_chu, "text": i.text,
                       "handles": i.handles} for i in items],
            "excel": xl,
        }

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

    @mcp.tool(name="knowledge_industries", tags={"kho", "check"}, annotations={"readOnlyHint": True})
    async def knowledge_industries(ctx: Context = None) -> dict:
        """Liệt kê danh mục ngành với mã máy và tên tiếng Việt để chọn tiêu chuẩn."""
        return {"industries": _ctx(ctx)["kho"].industries()}

    @mcp.tool(name="knowledge_standards", tags={"kho", "check"}, annotations={"readOnlyHint": True})
    async def knowledge_standards(
        industry: Annotated[str | None, "building, structural, fire, mechanical, pid, architecture, civil hoặc bỏ trống"] = None,
        ctx: Context = None,
    ) -> dict:
        """Liệt kê tiêu chuẩn/rule theo ngành, phiên bản, nguồn và trạng thái duyệt."""
        return {"standards": _ctx(ctx)["kho"].standard_list(industry)}

    @mcp.tool(name="knowledge_standard_add", tags={"kho", "check"})
    async def knowledge_standard_add(
        standard: Annotated[dict, "id, nganh, ten, phien_ban, nguon, hieu_luc và rules"],
        overwrite: Annotated[bool, "Cho phép cập nhật tiêu chuẩn do người dùng đã thêm"] = False,
        ctx: Context = None,
    ) -> dict:
        """Thêm tiêu chuẩn/rule JSON vào kho người dùng; không ghi vào bộ mặc định."""
        kho = _ctx(ctx)["kho"]
        try:
            path = kho.standard_add(standard, overwrite=overwrite)
        except (FileExistsError, ValueError) as exc:
            raise ToolError(str(exc)) from exc
        kho.log("standard", "add", id=standard.get("id"), path=str(path), overwrite=overwrite)
        return {"ok": True, "path": str(path), "standards": kho.standard_list()}

    @mcp.tool(name="knowledge_standard_delete", tags={"kho"})
    async def knowledge_standard_delete(
        standard_id: str,
        confirm: Annotated[bool, "Bắt buộc True để xóa tiêu chuẩn người dùng"] = False,
        ctx: Context = None,
    ) -> dict:
        """Xóa tiêu chuẩn do người dùng thêm; tiêu chuẩn mặc định không thể xóa."""
        if not confirm:
            raise ToolError("Cần confirm=true để xóa tiêu chuẩn.")
        kho = _ctx(ctx)["kho"]
        try:
            path = kho.standard_delete(standard_id)
        except (FileNotFoundError, PermissionError, ValueError) as exc:
            raise ToolError(str(exc)) from exc
        kho.log("standard", "delete", id=standard_id, path=str(path))
        return {"ok": True, "deleted": str(path), "standards": kho.standard_list()}

    # ------------------------------------------------------------------- kho
    @mcp.tool(name="knowledge_status", tags={"kho"}, annotations={"readOnlyHint": True})
    async def knowledge_status(ctx: Context = None) -> dict:
        """Tình trạng kho tri thức và backend AutoCAD."""
        lc = _ctx(ctx)
        b = lc["backend"]
        return lc["kho"].status() | {"backend": getattr(b, "name", None), "backend_error": lc.get("init_error"),
                                     "version": lc["cfg"].version}

    @mcp.tool(name="knowledge_rules_export", tags={"kho"}, annotations={"readOnlyHint": True})
    async def knowledge_rules_export(ctx: Context = None) -> dict:
        """Xuất quy tắc ánh xạ của đơn vị (chỉ quy tắc, không bản vẽ) để chia sẻ."""
        return {"rules": _ctx(ctx)["kho"].rules.export()}

    @mcp.tool(name="knowledge_rules_import", tags={"kho"})
    async def knowledge_rules_import(rules: list[dict], ctx: Context = None) -> dict:
        """Nhập quy tắc ánh xạ từ nơi khác (ghi đè theo pattern)."""
        n = _ctx(ctx)["kho"].rules.import_rules(rules)
        return {"imported": n}

    @mcp.tool(name="knowledge_skills", tags={"kho"}, annotations={"readOnlyHint": True})
    async def knowledge_skills(ctx: Context = None) -> dict:
        """Skill chuyên ngành trong kho/skill (mỗi thư mục một SKILL.md), bật/tắt."""
        return {"skills": _ctx(ctx)["kho"].skills()}

    @mcp.tool(name="knowledge_skill_toggle", tags={"kho"})
    async def knowledge_skill_toggle(name: str, enabled: bool, ctx: Context = None) -> dict:
        """Bật/tắt một skill."""
        _ctx(ctx)["kho"].set_skill(name, enabled)
        return {"ok": True, "skills": _ctx(ctx)["kho"].skills()}

    @mcp.tool(name="knowledge_skill_add", tags={"kho"})
    async def knowledge_skill_add(
        name: Annotated[str, "Tên ASCII kebab-case, ví dụ qa-mep"],
        content: Annotated[str, "Nội dung SKILL.md có YAML frontmatter"],
        overwrite: Annotated[bool, "Cho phép cập nhật skill do người dùng đã tạo"] = False,
        ctx: Context = None,
    ) -> dict:
        """Thêm skill do LLM soạn vào kho người dùng; chỉ ghi SKILL.md, không chạy mã."""
        kho = _ctx(ctx)["kho"]
        try:
            path = kho.add_skill(name, content, overwrite=overwrite)
        except (FileExistsError, ValueError) as exc:
            raise ToolError(str(exc)) from exc
        kho.log("skill", "add", name=name, path=str(path), overwrite=overwrite)
        return {"ok": True, "name": name, "path": str(path), "skills": kho.skills()}

    # Backward-compatible aliases for clients that used the original kho_* names.
    # The knowledge_* names remain canonical and are advertised in new documentation.
    legacy_aliases = {
        "kho_industries": knowledge_industries,
        "kho_standards": knowledge_standards,
        "kho_standard_add": knowledge_standard_add,
        "kho_standard_delete": knowledge_standard_delete,
        "kho_status": knowledge_status,
        "kho_rules_export": knowledge_rules_export,
        "kho_rules_import": knowledge_rules_import,
        "kho_skills": knowledge_skills,
        "kho_skill_toggle": knowledge_skill_toggle,
        "kho_skill_add": knowledge_skill_add,
    }
    for legacy_name, canonical_tool in legacy_aliases.items():
        canonical_name = legacy_name.replace("kho_", "knowledge_", 1)
        mcp.tool(name=legacy_name, description=f"Tương thích cũ; dùng {canonical_name} cho kết nối mới.")(canonical_tool)

    # -------------------------------------------------------------- duyệt
    @mcp.tool(name="approval_execute", tags={"approval"})
    async def approval_execute(
        token: Annotated[str, "Token từ kết quả approval_required, chỉ dùng sau khi người dùng đồng ý"],
        ctx: Context = None,
    ) -> dict:
        """Chạy thao tác phá huỷ đã được người dùng đồng ý, đúng tham số đã xem trước. Token dùng một lần."""
        # ApprovalMiddleware chặn lời gọi này và chạy tool gốc; tới được đây nghĩa là middleware chưa cài.
        raise ToolError("Bước duyệt chưa được cài trên server (ApprovalMiddleware).")

    @mcp.resource("cadtroly://skill/{name}")
    async def skill_text(name: str, ctx: Context = None) -> str:
        """Nội dung SKILL.md của một skill (hướng dẫn cho AI theo ngành)."""
        p = _ctx(ctx)["kho"].skill_path(name)
        return p.read_text(encoding="utf-8") if p else f"Không có skill {name}"


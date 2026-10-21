"""Xuất Excel có truy vết: sheet Khối lượng, Chi tiết (từng handle), Ánh xạ, Kiểm soát."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from ..reader.model import Drawing
from .calc import TakeoffRow
from .mapper import Group

FILL = {"A": "C6EFCE", "B": "FFEB9C", "C": "FFC7CE"}


def _autosize(ws, maxw=60):
    for col in ws.columns:
        w = max((len(str(c.value)) if c.value is not None else 0) for c in col)
        ws.column_dimensions[get_column_letter(col[0].column)].width = min(max(10, w + 2), maxw)


def export_excel(dwg: Drawing, groups: list[Group], rows: list[TakeoffRow], out: str | Path,
                 *, meta: dict | None = None) -> Path:
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    bold = Font(bold=True)

    # --- Khối lượng ---
    ws = wb.active
    ws.title = "Khoi luong"
    ws.append(["BẢNG KHỐI LƯỢNG", "", "", "", "", "", ""])
    ws["A1"].font = Font(bold=True, size=13)
    ws.append(["Bản vẽ", dwg.path])
    ws.append(["Đơn vị bản vẽ", dwg.units, "Xuất lúc", datetime.now().strftime("%d/%m/%Y %H:%M")])
    ws.append([])
    hdr = ["STT", "Công tác", "ĐV", "Khối lượng", "Cách tính", "Nguồn (truy vết)", "Tin cậy", "Nhóm", "Ghi chú"]
    ws.append(hdr)
    for c in ws[ws.max_row]:
        c.font = bold
    for i, r in enumerate(rows, 1):
        ws.append([i, r.cong_tac, r.don_vi, r.khoi_luong, r.cach_tinh, r.nguon, r.tin_cay, r.nhom, r.ghi_chu])
        cell = ws.cell(row=ws.max_row, column=7)
        cell.fill = PatternFill("solid", fgColor=FILL.get(r.tin_cay, "FFFFFF"))
        cell.alignment = Alignment(horizontal="center")
    ws.append([])
    ws.append(["A = đếm/đo trực tiếp theo quy tắc", "B = suy từ tên hoặc text, cần xác nhận", "C = không xác định, để trống"])
    _autosize(ws)

    # --- Chi tiết ---
    wd = wb.create_sheet("Chi tiet")
    wd.append(["Công tác", "Handle", "Layer/Block", "Giá trị", "Đơn vị", "X", "Y", "Độ chính xác", "Lệnh zoom"])
    for c in wd[1]:
        c.font = bold
    for r in rows:
        for d in r.chi_tiet:
            p = d.get("vi_tri") or (None, None)
            zoom = f"_.ZOOM _C {p[0]:.0f},{p[1]:.0f} 5000" if p and p[0] is not None else ""
            wd.append([r.cong_tac, d["handle"], r.nhom, d.get("gia_tri"), r.don_vi,
                       round(p[0], 1) if p[0] is not None else None,
                       round(p[1], 1) if p[1] is not None else None,
                       d.get("do_chinh_xac", "exact"), zoom])
    _autosize(wd)

    # --- Ánh xạ ---
    wm = wb.create_sheet("Anh xa")
    wm.append(["Loại", "Tên trong bản vẽ", "Số lượng", "Mô tả", "Công tác", "ĐV", "Cách tính", "Tham số", "Tin cậy", "Lý do"])
    for c in wm[1]:
        c.font = bold
    for g in groups:
        wm.append([g.kind, g.name, g.count, g.describe(), "(bỏ qua)" if g.skip else g.cong_tac, g.don_vi,
                   g.cach_tinh, str(g.tham_so) if g.tham_so else "", g.tin_cay, g.ly_do])
        wm.cell(row=wm.max_row, column=9).fill = PatternFill("solid", fgColor=FILL.get(g.tin_cay, "FFFFFF"))
    _autosize(wm)

    # --- Kiểm soát ---
    wk = wb.create_sheet("Kiem soat")
    wk.append(["Mục", "Giá trị"])
    for c in wk[1]:
        c.font = bold
    s = dwg.summary()
    for k, v in [("Đối tượng", s["entities"]), ("Layer", s["layers"]), ("Block", s["blocks"]),
                 ("INSERT", s["inserts"]), ("Loại", str(s["kinds"]))]:
        wk.append([k, v])
    for k, v in (meta or {}).items():
        wk.append([k, str(v)])
    wk.append(["Phương pháp", "Đếm block theo tên; đo polyline/hatch flatten dung sai 0.01; cao từ text H= hoặc người nhập; không bịa số thiếu."])
    _autosize(wk)

    wb.save(out)
    return out

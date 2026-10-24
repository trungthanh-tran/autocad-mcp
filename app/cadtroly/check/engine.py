"""Luồng D: kiểm tra bản vẽ theo bộ quy tắc JSON.

Bộ quy tắc (kho/tieu-chuan/<id>.rules.json hoặc kho/quy-tac/chuan-cong-ty.rules.json):
{
  "id": "chuan-cong-ty", "ten": "Chuẩn vẽ công ty", "hieu_luc": "co",
  "rules": [
    {"id": "L-01", "loai": "layer_name", "pattern": "^[A-Z]{1,2}-[A-Z0-9]+$", "muc": "loi",
     "mo_ta": "Tên layer phải dạng X-XXX", "dieu": "Quy định vẽ 2024 §3.1", "duyet": true},
    {"id": "L-02", "loai": "text_height_min", "gia_tri": 2.5, "muc": "loi", ...},
    {"id": "L-03", "loai": "no_entity_on_layer", "layer": "0", "muc": "loi", ...},
    {"id": "L-04", "loai": "dim_no_override", "muc": "canh_bao", ...},
    {"id": "S-01", "loai": "min_value_by_block_attr", "block": "LANCAN", "attr": "CAO", "gia_tri": 1000,
     "muc": "loi", "dieu": "QCVN 18:2021/BXD §2.1.x", ...},
    {"id": "S-02", "loai": "required_text", "pattern": "lưới an toàn", "muc": "xac_nhan", ...}
  ]
}
Loại "xac_nhan" = tiêu chuẩn ghi "theo điều kiện thực tế", tool không tự kết luận.

Cốt thép (đọc ghi chú thép trên bản vẽ bằng takeoff.civil.rebar: "N1 12Ø16 L=5200", "F1-D25-125", "Ø12 a200"):
    {"loai": "rebar_diameter_in", "gia_tri": [6, 8, 10, …]}      đường kính phải thuộc dãy cho phép
    {"loai": "rebar_note_complete"}                              ghi chú phải có số thanh (kèm L=) hoặc bước
    {"loai": "rebar_clear_spacing_min", "gia_tri": 25}            bước − d ≥ max(d, gia_tri) mm
    {"loai": "rebar_spacing_max", "gia_tri": 400}                 bước ≤ gia_tri mm
    {"loai": "rebar_grade_in", "gia_tri": ["CB300-V", …]}        mác ghi trong ghi chú phải thuộc danh sách
    {"loai": "rebar_grade_flag", "gia_tri": ["CB600-V"]}          có dùng mác trong danh sách → báo (thường xac_nhan)
    {"loai": "cover_note_min", "gia_tri": 10, "theo_duong_kinh": true}
                                  chiều dày lớp bảo vệ GHI trên bản vẽ (lớp bê tông bảo vệ 25, abv=25) ≥ gia_tri,
                                  và ≥ đường kính thanh lớn nhất trong ghi chú thép khi theo_duong_kinh
Giá trị số (khoảng cách, bước…) không có mặc định trong code: chỉ lấy từ bộ quy tắc do kỹ sư nhập theo văn bản gốc.
"""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

from ..reader.model import Drawing, Entity
from ..takeoff.civil import RebarItem, rebar


@dataclass
class Finding:
    rule_id: str
    muc: str                      # loi | canh_bao | xac_nhan
    mo_ta: str
    dieu: str
    handles: list[str] = field(default_factory=list)
    vi_tri: tuple[float, float] | None = None
    gia_tri: str = ""
    tu_sua_duoc: bool = False
    goi_y: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RuleSet:
    id: str
    ten: str
    rules: list[dict]
    hieu_luc: str = "co"
    thay_boi: str | None = None


def load_ruleset(path: str | Path) -> RuleSet:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    return RuleSet(id=d["id"], ten=d.get("ten", d["id"]), rules=d.get("rules", []),
                   hieu_luc=d.get("hieu_luc", "co"), thay_boi=d.get("thay_boi"))


def _first_pt(ents: list[Entity]):
    for e in ents:
        if e.point:
            return e.point
    return None


def check_drawing(dwg: Drawing, rs: RuleSet, *, only_approved: bool = True) -> list[Finding]:
    out: list[Finding] = []
    if rs.hieu_luc == "khong":
        out.append(Finding(rs.id, "canh_bao", f"Bộ quy tắc {rs.ten} đã hết hiệu lực"
                           + (f", thay bởi {rs.thay_boi}" if rs.thay_boi else ""), ""))
    bars: list[RebarItem] | None = None
    for r in rs.rules:
        if only_approved and not r.get("duyet", False):
            continue
        if r["loai"] == "cover_note_min":
            if bars is None:
                bars = rebar(dwg)
            f = _cover_rule(r, dwg, bars)
            if f:
                out.append(f)
            continue
        if r["loai"].startswith("rebar_"):
            if bars is None:
                bars = rebar(dwg)
            f = _rebar_rule(r, bars)
            if f:
                out.append(f)
            continue
        loai, muc, dieu, rid = r["loai"], r.get("muc", "loi"), r.get("dieu", ""), r["id"]
        mo_ta = r.get("mo_ta", loai)
        if loai == "layer_name":
            rx = re.compile(r["pattern"])
            bad = [l for l in dwg.layers if l not in ("0", "Defpoints") and not rx.match(l)]
            if bad:
                hs = [e.handle for e in dwg.entities if e.layer in bad][:200]
                out.append(Finding(rid, muc, f"{mo_ta}: {len(bad)} layer sai tên ({', '.join(bad[:6])}{'…' if len(bad) > 6 else ''})",
                                   dieu, hs, tu_sua_duoc=True, goi_y="đổi tên layer theo mẫu"))
        elif loai == "text_height_min":
            v = float(r["gia_tri"])
            bad = [e for e in dwg.entities if e.text and e.dxftype in ("TEXT", "MTEXT")
                   and (e.extra.get("height") or 0) < v]
            if bad:
                out.append(Finding(rid, muc, f"{mo_ta}: {len(bad)} text cao < {v}", dieu,
                                   [e.handle for e in bad], _first_pt(bad), tu_sua_duoc=True,
                                   goi_y=f"đặt cao chữ {v}"))
        elif loai == "no_entity_on_layer":
            bad = [e for e in dwg.entities if e.layer == r["layer"]]
            if bad:
                out.append(Finding(rid, muc, f"{mo_ta}: {len(bad)} đối tượng trên layer {r['layer']}", dieu,
                                   [e.handle for e in bad], _first_pt(bad), tu_sua_duoc=True,
                                   goi_y="chuyển sang layer đúng"))
        elif loai == "dim_no_override":
            bad = [e for e in dwg.entities if e.dxftype == "DIMENSION" and e.extra.get("override")]
            if bad:
                out.append(Finding(rid, muc, f"{mo_ta}: {len(bad)} dimension bị ghi đè", dieu,
                                   [e.handle for e in bad], _first_pt(bad), goi_y="xoá text override"))
        elif loai == "min_value_by_block_attr":
            bad, vals = [], []
            for e in dwg.entities:
                if e.block_name and re.search(r["block"], e.block_name, re.I):
                    raw = e.attribs.get(r["attr"], "")
                    m = re.search(r"\d+(?:\.\d+)?", raw.replace(",", "."))
                    if m and float(m.group()) < float(r["gia_tri"]):
                        bad.append(e)
                        vals.append(raw)
            if bad:
                out.append(Finding(rid, muc, f"{mo_ta}: {len(bad)} block {r['block']} có {r['attr']} < {r['gia_tri']}",
                                   dieu, [e.handle for e in bad], _first_pt(bad), gia_tri=", ".join(vals[:5])))
        elif loai == "required_text":
            rx = re.compile(r["pattern"], re.I)
            found = [e for e in dwg.texts() if rx.search(e.text or "")]
            if not found:
                out.append(Finding(rid, muc, f"{mo_ta}: không thấy ghi chú '{r['pattern']}'", dieu))
            elif muc == "xac_nhan":
                out.append(Finding(rid, "xac_nhan", f"{mo_ta}: có ghi chú, cần kỹ sư xác nhận thực tế", dieu,
                                   [e.handle for e in found], _first_pt(found)))
        elif loai == "required_layer":
            if r["layer"] not in dwg.layers:
                out.append(Finding(rid, muc, f"{mo_ta}: thiếu layer {r['layer']}", dieu))
        elif loai == "max_count_per_layer":
            n = sum(1 for e in dwg.entities if e.layer == r["layer"])
            if n > int(r["gia_tri"]):
                out.append(Finding(rid, muc, f"{mo_ta}: {n} > {r['gia_tri']} trên {r['layer']}", dieu))
    return out


_COVER = re.compile(r"(?:lop\s*(?:(?:be\s*tong|bt)\s*)?bao\s*ve|\ba\s*bv\b|\babv\b)[^0-9]{0,40}?(\d{1,3}(?:[.,]\d+)?)\s*(mm|cm)?")


def _ascii(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.replace("đ", "d").replace("Đ", "D").lower()


def _cover_rule(r: dict, dwg: Drawing, bars: list[RebarItem]) -> Finding | None:
    """So chiều dày lớp bảo vệ ghi trong text với gia_tri (và đường kính thanh lớn nhất). Không ghi → không kết luận."""
    v_min = float(r["gia_tri"])
    d_max = max((b.d_mm for b in bars), default=0) if r.get("theo_duong_kinh") else 0
    need = max(v_min, d_max)
    bad, vals = [], []
    for e in dwg.texts():
        m = _COVER.search(_ascii(e.text or ""))
        if not m:
            continue
        v = float(m.group(1).replace(",", "."))
        v = v * 10 if (m.group(2) or "") == "cm" else v
        vals.append(v)
        if v < need:
            bad.append((e, v))
    if not bad:
        return None
    lim = f"{need:g} mm" + (f" (= đường kính thanh lớn nhất Ø{d_max})" if d_max > v_min else "")
    return Finding(r["id"], r.get("muc", "loi"), f"{r.get('mo_ta', 'lớp bảo vệ')}: ghi {', '.join(f'{v:g}' for _, v in bad)} mm < {lim}",
                   r.get("dieu", ""), [e.handle for e, _ in bad], bad[0][0].point,
                   gia_tri=", ".join(f"{v:g}" for _, v in bad), goi_y=r.get("trich", "")[:300])


def _bar_pt(items: list[RebarItem]):
    return next((it.point for it in items if it.point), None)


def _bar_list(items: list[RebarItem], n: int = 5) -> str:
    return ", ".join(f"{it.so_hieu or '?'} '{it.text.strip()}'" for it in items[:n]) + ("…" if len(items) > n else "")


def _rebar_rule(r: dict, bars: list[RebarItem]) -> Finding | None:
    loai, muc, dieu, rid = r["loai"], r.get("muc", "loi"), r.get("dieu", ""), r["id"]
    mo_ta = r.get("mo_ta", loai)
    bad: list[RebarItem] = []
    goi_y = ""
    if loai == "rebar_diameter_in":
        allowed = {int(v) for v in r["gia_tri"]}
        bad = [b for b in bars if b.d_mm not in allowed]
        goi_y = "đổi sang đường kính trong dãy: " + ", ".join(str(v) for v in sorted(allowed))
    elif loai == "rebar_note_complete":
        bad = [b for b in bars if (b.so_thanh is None and b.buoc_mm is None)
               or (b.so_thanh and b.dai_m is None and b.L_raw is None)]
        goi_y = "ghi đủ số thanh + L=, hoặc bước a…"
    elif loai == "rebar_clear_spacing_min":
        v = float(r["gia_tri"])
        bad = [b for b in bars if b.buoc_mm and b.buoc_mm - b.d_mm < max(b.d_mm, v)]
        goi_y = f"khoảng hở thông thủy (bước − d) ≥ max(d, {v:g}) mm"
    elif loai == "rebar_spacing_max":
        v = float(r["gia_tri"])
        bad = [b for b in bars if b.buoc_mm and b.buoc_mm > v]
        goi_y = f"bước ≤ {v:g} mm"
    elif loai == "rebar_grade_flag":
        flagged = {str(v).upper() for v in r["gia_tri"]}
        bad = [b for b in bars if b.mac and b.mac.upper() in flagged]
    elif loai == "rebar_grade_in":
        allowed = {str(v).upper() for v in r["gia_tri"]}
        bad = [b for b in bars if b.mac and b.mac.upper() not in allowed]
        goi_y = "mác trong bộ quy tắc: " + ", ".join(sorted(allowed))
    else:
        return None
    if not bad:
        return None
    hs = [h for b in bad for h in b.handles]
    return Finding(rid, muc, f"{mo_ta}: {len(bad)} ghi chú thép ({_bar_list(bad)})", dieu, hs, _bar_pt(bad),
                   gia_tri="; ".join(f"Ø{b.d_mm}" + (f" a{b.buoc_mm:g}" if b.buoc_mm else "") for b in bad[:5]),
                   goi_y=goi_y)


def summarize(findings: list[Finding]) -> dict:
    return {
        "loi": sum(1 for f in findings if f.muc == "loi"),
        "canh_bao": sum(1 for f in findings if f.muc == "canh_bao"),
        "xac_nhan": sum(1 for f in findings if f.muc == "xac_nhan"),
        "tu_sua_duoc": sum(1 for f in findings if f.tu_sua_duoc),
    }

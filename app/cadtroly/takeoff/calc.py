"""Bước 3 luồng A: tính khối lượng từ nhóm đã ánh xạ. Mỗi dòng có truy vết.

Cách tính:
  count              đếm đối tượng
  length             Σ chiều dài (m)
  area               Σ diện tích vùng kín / hatch (m2)
  volume_by_height   Σ dài × dày × cao (m3)   — tường
  area_by_height     Σ dài × cao (m2)         — trát, ván khuôn
Chiều cao "H": lấy từ text dạng H=3300 / H 3.3 trong bản vẽ, hoặc do người nhập.
Thiếu dữ liệu thì để trống và hạ tin cậy, không bịa.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from ..reader.model import Drawing, Entity
from .mapper import Group


@dataclass
class TakeoffRow:
    cong_tac: str
    don_vi: str
    khoi_luong: float | None
    cach_tinh: str
    nguon: str                      # "142 handle · layer TUONG220 · cao từ text H=3300"
    tin_cay: str
    nhom: str
    handles: list[str] = field(default_factory=list)
    chi_tiet: list[dict] = field(default_factory=list)   # từng đối tượng: handle, giá trị
    ghi_chu: str = ""


def find_height(dwg: Drawing) -> tuple[float | None, str]:
    """Tìm chiều cao tầng trong text: H=3300, H= 3.3m, CAO 3300."""
    for e in dwg.texts():
        t = (e.text or "").replace(",", ".")
        m = re.search(r"\b(?:H|CAO|h)\s*[=:]?\s*(\d+(?:\.\d+)?)\s*(mm|m)?", t)
        if m:
            v = float(m.group(1))
            unit = m.group(2)
            if unit == "m" or (unit is None and v < 20):
                return v, f'text "{e.text}" tại {e.as_trace()}'
            return v * dwg.to_m, f'text "{e.text}" tại {e.as_trace()}'
    return None, ""


def _area_m2(e: Entity, k: float) -> float | None:
    return e.area * k * k if e.area is not None else None


def _len_m(e: Entity, k: float) -> float | None:
    return e.length * k if e.length is not None else None


def compute(dwg: Drawing, groups: list[Group], *, height_m: float | None = None,
            overrides: dict | None = None) -> list[TakeoffRow]:
    k = dwg.to_m
    overrides = overrides or {}
    auto_h, h_src = find_height(dwg)
    H = height_m if height_m is not None else auto_h
    h_note = "người nhập" if height_m is not None else h_src
    rows: list[TakeoffRow] = []
    for g in groups:
        if g.skip or g.tin_cay == "C" or not g.cong_tac:
            if not g.skip:
                rows.append(TakeoffRow(g.cong_tac or f"[chưa xác định] {g.name}", g.don_vi or "", None,
                                       g.cach_tinh, f"{g.count} đối tượng · {g.kind} {g.name}", "C",
                                       g.name, [e.handle for e in g.entities],
                                       ghi_chu="khoanh trên bản vẽ để người đếm"))
            continue
        det, total, note, tc = [], 0.0, "", g.tin_cay
        ct = g.cach_tinh
        if ct == "count":
            total = float(g.count)
            det = [{"handle": e.handle, "gia_tri": 1, "vi_tri": e.point} for e in g.entities]
        elif ct == "length":
            for e in g.entities:
                v = _len_m(e, k)
                if v is not None:
                    total += v
                    det.append({"handle": e.handle, "gia_tri": round(v, 3), "vi_tri": e.point})
        elif ct == "area":
            miss = 0
            for e in g.entities:
                v = _area_m2(e, k)
                if v is None or v == 0:
                    miss += 1
                    continue
                total += v
                det.append({"handle": e.handle, "gia_tri": round(v, 3), "vi_tri": e.point,
                            "do_chinh_xac": e.accuracy})
            if miss:
                note = f"{miss} đối tượng không kín, bỏ qua"
                tc = "B" if tc == "A" else tc
        elif ct in ("volume_by_height", "area_by_height"):
            day = g.tham_so.get("day")
            if H is None:
                rows.append(TakeoffRow(g.cong_tac, g.don_vi, None, ct,
                                       f"{g.count} handle · {g.kind} {g.name} · THIẾU chiều cao",
                                       "C", g.name, [e.handle for e in g.entities],
                                       ghi_chu="cần chiều cao tầng (không tìm thấy text H=)"))
                continue
            if ct == "volume_by_height" and not day:
                rows.append(TakeoffRow(g.cong_tac, g.don_vi, None, ct,
                                       f"{g.count} handle · {g.kind} {g.name} · THIẾU độ dày",
                                       "C", g.name, [e.handle for e in g.entities],
                                       ghi_chu="cần độ dày (tham số 'day')"))
                continue
            for e in g.entities:
                L = _len_m(e, k)
                if L is None:
                    continue
                v = L * H * (day if ct == "volume_by_height" else 1.0)
                total += v
                det.append({"handle": e.handle, "gia_tri": round(v, 3), "dai_m": round(L, 3), "vi_tri": e.point})
            tru = overrides.get("tru_lo_cua", 0.0)
            if tru:
                total -= tru
                note = f"trừ lỗ cửa {tru} {g.don_vi}"
            note = (note + " · " if note else "") + f"cao {round(H, 3)} m từ {h_note}"
            if h_src and height_m is None:
                tc = "B" if tc == "A" else tc   # cao suy từ text → B
        nguon = f"{len(det)} handle · {g.kind} {g.name}" + (f" · {note}" if note else "")
        rows.append(TakeoffRow(g.cong_tac, g.don_vi, round(total, 3), ct, nguon, tc, g.name,
                               [d["handle"] for d in det], det, ghi_chu=g.ly_do))
    return rows


def stats(groups: list[Group]) -> dict:
    tot = sum(g.count for g in groups if not g.skip) or 1
    out = {"A": 0, "B": 0, "C": 0}
    for g in groups:
        if not g.skip:
            out[g.tin_cay] += g.count
    return {k: round(100 * v / tot) for k, v in out.items()} | {"tong": tot}

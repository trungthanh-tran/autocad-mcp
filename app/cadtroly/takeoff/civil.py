"""Bóc khối lượng cầu đường từ bản vẽ AutoCAD thường (bản vẽ tay, Nova-TDN, xuất từ phần mềm khác).

Không cần đối tượng Civil 3D: chỉ đọc TEXT/MTEXT đã có trên bản vẽ.

  earthwork  đào đắp từ trắc ngang. Mỗi trắc ngang có text lý trình (Km0+100) và text diện tích
             (F đào = 12.35, hoặc ô "Diện tích đào" cạnh ô số). Khối lượng giữa hai trắc ngang liền
             kề = (F1 + F2) / 2 × khoảng cách (phương pháp mặt cắt trung bình).
  rebar      thống kê thép từ ghi chú: "N1 12Ø16 L=5200", "6%%c22 L=12.5". KL = số thanh × dài ×
             0.0061654·d² kg/m.

Tin cậy như luồng A: A đọc thẳng từ một text; B phải ghép (nhãn với ô số, diện tích với lý trình gần
nhất khi có lý trình khác gần tương đương); C thiếu dữ liệu, để trống chứ không đoán.
"""
from __future__ import annotations

import math
import re
import unicodedata
from dataclasses import dataclass, field

from ..reader.model import Drawing, Entity

STEEL_KG_PER_M_PER_MM2 = math.pi / 4 * 7850 / 1e6     # 0.0061654 kg/m cho d = 1 mm


def ascii_lower(s: str) -> str:
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.replace("đ", "d").replace("Đ", "D").lower()


def _num(s: str) -> float:
    return float(s.replace(",", "."))


def _dist(a, b) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _h(e: Entity) -> float:
    return float((e.extra or {}).get("height") or 0) or 2.5


# ----------------------------------------------------------------- lý trình
_KM = re.compile(r"km\s*(\d+)\s*\+\s*(\d+(?:[.,]\d+)?)")
_LT = re.compile(r"^\s*(?:ly trinh|lt)\s*[:=]?\s*(\d+)\s*\+\s*(\d+(?:[.,]\d+)?)")


def parse_station(text: str) -> float | None:
    """'Km0+100.50' → 100.5 m; 'Lý trình: 1+250' → 1250 m. Không khớp → None."""
    t = ascii_lower(text)
    m = _KM.search(t) or _LT.search(t)
    if not m:
        return None
    return int(m.group(1)) * 1000 + _num(m.group(2))


def fmt_station(m: float) -> str:
    km = int(m // 1000)
    return f"Km{km}+{m - km * 1000:06.2f}"


# --------------------------------------------------------------- diện tích
# nhãn (đã bỏ dấu) → mã loại; thứ tự quan trọng: "vet huu co" trước "dao"
CATEGORIES: list[tuple[str, str, str]] = [
    (r"(?:vet|boc)\s*huu\s*co|\bvhc\b|\bbhc\b", "vet_huu_co", "Vét/bóc hữu cơ"),
    (r"danh\s*cap", "danh_cap", "Đánh cấp"),
    (r"\bdao\b", "dao", "Đào nền"),
    (r"\bdap\b", "dap", "Đắp nền"),
]
_K = re.compile(r"\bk\s*(9[058])\b")
_VALUE = r"[=:]\s*(\d+(?:[.,]\d+)?)\s*(?:m2|m²)?\s*$"
_ONLY_NUM = re.compile(r"^\s*(\d+(?:[.,]\d+)?)\s*(?:m2|m²)?\s*$")


def _category(t: str) -> tuple[str, str] | None:
    t = re.sub(r"\b(f|s|dt)(dao|dap)\b", r"\1 \2", t)          # "FĐào" → "f dao"
    for rx, code, label in CATEGORIES:
        if re.search(rx, t):
            k = _K.search(t)
            if k and code == "dap":
                return f"dap_k{k.group(1)}", f"Đắp nền K{k.group(1)}"
            return code, label
    return None


@dataclass
class AreaItem:
    loai: str
    ten: str
    f_m2: float
    handles: list[str]
    point: tuple[float, float]
    text: str
    tin_cay: str = "A"
    ghi_chu: str = ""


def find_areas(dwg: Drawing) -> list[AreaItem]:
    """Diện tích ghi trên trắc ngang: 'F đào = 12.35' (A) hoặc ô nhãn 'Diện tích đào' + ô số bên phải (B)."""
    texts = [e for e in dwg.texts() if e.point]
    nums = [(e, _ONLY_NUM.match(e.text or "")) for e in texts]
    nums = [(e, _num(m.group(1))) for e, m in nums if m]
    used: set[str] = set()
    out: list[AreaItem] = []
    for e in texts:
        t = ascii_lower(e.text or "").strip()
        cat = _category(t)
        if not cat:
            continue
        m = re.search(_VALUE, t)
        if m:
            out.append(AreaItem(cat[0], cat[1], _num(m.group(1)), [e.handle], e.point, e.text or ""))
            continue
        if re.search(r"\d", _K.sub("", t).replace("m2", "").replace("m²", "")):
            continue                       # có số mà không đúng dạng "nhãn = số": không đoán
        h = _h(e)
        best = None
        for ne, v in nums:
            if ne.handle in used:
                continue
            dx, dy = ne.point[0] - e.point[0], ne.point[1] - e.point[1]
            if 0 < dx <= 40 * h and abs(dy) <= 0.8 * h and (best is None or dx < best[0]):
                best = (dx, ne, v)
        if best:
            used.add(best[1].handle)
            out.append(AreaItem(cat[0], cat[1], best[2], [e.handle, best[1].handle], e.point,
                                f"{e.text} | {best[1].text}", "B", "ghép nhãn với ô số cùng hàng"))
    return out


@dataclass
class Section:
    station_m: float
    label: str
    handle: str
    point: tuple[float, float]
    areas: dict[str, float] = field(default_factory=dict)
    sources: dict[str, list[str]] = field(default_factory=dict)
    tin_cay: dict[str, str] = field(default_factory=dict)
    ghi_chu: list[str] = field(default_factory=list)


def earthwork(dwg: Drawing) -> dict:
    """Ghép diện tích về lý trình gần nhất rồi tính khối lượng giữa các trắc ngang liền kề."""
    stations: list[Section] = []
    seen: set[float] = set()
    for e in dwg.texts():
        s = parse_station(e.text or "") if e.point else None
        if s is None:
            continue
        if s in seen:                          # cùng lý trình ghi hai lần (tiêu đề + bảng)
            continue
        seen.add(s)
        stations.append(Section(s, e.text or "", e.handle, e.point))
    areas = find_areas(dwg)
    if not stations:
        return {"sections": [], "segments": [], "totals": {}, "names": {}, "unassigned": areas,
                "warnings": ["Không thấy text lý trình dạng Km0+100 hoặc 'Lý trình: 0+100'."]}
    names: dict[str, str] = {}
    for a in areas:
        ranked = sorted(stations, key=lambda s: _dist(s.point, a.point))
        sec = ranked[0]
        d0 = _dist(sec.point, a.point)
        tc, note = a.tin_cay, a.ghi_chu
        if len(ranked) > 1 and _dist(ranked[1].point, a.point) < 1.25 * d0:
            tc, note = ("B" if tc == "A" else tc), (note + "; " if note else "") + \
                f"gần cả {ranked[1].label}, đã gán {sec.label}"
        names[a.loai] = a.ten
        if a.loai in sec.areas:
            sec.ghi_chu.append(f"{a.ten}: cộng 2 giá trị")
            tc = "B" if tc == "A" else tc
        sec.areas[a.loai] = round(sec.areas.get(a.loai, 0.0) + a.f_m2, 4)
        sec.sources.setdefault(a.loai, []).extend(a.handles)
        prev = sec.tin_cay.get(a.loai, "A")
        sec.tin_cay[a.loai] = max(prev, tc)          # "A" < "B" < "C"
        if note:
            sec.ghi_chu.append(note)
    stations.sort(key=lambda s: s.station_m)
    segments, totals = [], {}
    for s1, s2 in zip(stations, stations[1:]):
        L = round(s2.station_m - s1.station_m, 3)
        seg = {"tu": s1.label, "den": s2.label, "tu_m": s1.station_m, "den_m": s2.station_m, "L_m": L,
               "khoi_luong": {}, "tin_cay": {}}
        for loai in sorted(set(s1.areas) | set(s2.areas)):
            f1, f2 = s1.areas.get(loai), s2.areas.get(loai)
            if f1 is None or f2 is None:
                # một đầu không ghi = 0 là quy ước phổ biến nhưng không chắc → B
                tc = "B"
                f1, f2 = f1 or 0.0, f2 or 0.0
            else:
                tc = max(s1.tin_cay.get(loai, "A"), s2.tin_cay.get(loai, "A"))
            v = round((f1 + f2) / 2 * L, 3)
            seg["khoi_luong"][loai] = v
            seg["tin_cay"][loai] = tc
            totals[loai] = round(totals.get(loai, 0.0) + v, 3)
        segments.append(seg)
    warnings = []
    empty = [s.label for s in stations if not s.areas]
    if empty:
        warnings.append(f"{len(empty)} trắc ngang không thấy diện tích: {', '.join(empty[:10])}")
    if len(stations) == 1:
        warnings.append("Chỉ có một trắc ngang, chưa tính được khối lượng.")
    return {"sections": stations, "segments": segments, "totals": totals, "names": names,
            "unassigned": [], "warnings": warnings}


# ---------------------------------------------------------------------- thép
_DIA = r"(?:%%c|[øØΦφ∅⌀]|\\U\+2205|\\U\+00D8)"
# số thanh không được dính chữ phía trước (N4 Ø10 là số hiệu N4, không phải 4 thanh); 'x' là phép nhân
_BAR = re.compile(r"(?:(?<![A-Za-z\d])(\d+)\s*[x×*]\s*)?(?:(?<![A-WYZa-wyz\d])(\d+))?\s*" + _DIA + r"\s*(\d{1,2})\b", re.I)
_LEN = re.compile(r"\bL\s*=\s*(\d+(?:[.,]\d+)?)\s*(mm|m)?", re.I)
_SPACING = re.compile(r"\b[aA@]\s*=?\s*(\d{2,3})\b")
_MARK = re.compile(r"\b(N\s?\d{1,3}[a-z]?)\b|\((\d{1,3}[a-z]?)\)|^\s*(\d{1,3}[a-z]?)\s*[-:.]", re.I)


@dataclass
class RebarItem:
    so_hieu: str
    d_mm: int
    so_thanh: int | None
    dai_m: float | None
    handles: list[str]
    text: str
    point: tuple[float, float] | None
    tin_cay: str = "A"
    ghi_chu: str = ""

    @property
    def tong_dai_m(self) -> float | None:
        return round(self.so_thanh * self.dai_m, 3) if self.so_thanh and self.dai_m else None

    @property
    def kg_per_m(self) -> float:
        return round(STEEL_KG_PER_M_PER_MM2 * self.d_mm ** 2, 4)

    @property
    def tong_kg(self) -> float | None:
        return round(self.tong_dai_m * self.kg_per_m, 2) if self.tong_dai_m else None


def rebar(dwg: Drawing) -> list[RebarItem]:
    """Mỗi ghi chú thép một dòng. Cùng số hiệu/Ø/số thanh/dài ghi ở nhiều hình chiếu chỉ tính một lần (B)."""
    out: list[RebarItem] = []
    seen: dict[tuple, RebarItem] = {}
    for e in dwg.texts():
        raw = e.text or ""
        m = _BAR.search(raw)
        if not m:
            continue
        mult = int(m.group(1)) if m.group(1) else 1
        n = int(m.group(2)) * mult if m.group(2) else None
        d = int(m.group(3))
        if not 6 <= d <= 50:
            continue
        L = None
        lm = _LEN.search(raw)
        if lm:
            v = _num(lm.group(1))
            unit = (lm.group(2) or "").lower()
            L = v if unit == "m" or (not unit and v < 50) else v / 1000
        mk = _MARK.search(raw[: m.start()])
        so_hieu = next((g for g in mk.groups() if g), "").replace(" ", "").upper() if mk else ""
        key = (so_hieu or ascii_lower(raw).strip(), d, n, L)
        if key in seen:
            dup = seen[key]
            dup.handles.append(e.handle)
            dup.tin_cay = "B" if dup.tin_cay == "A" else dup.tin_cay
            dup.ghi_chu = f"ghi ở {len(dup.handles)} chỗ, chỉ tính 1 lần — kiểm tra có phải thanh khác nhau không"
            continue
        tc, note = "A", ""
        if n is None:
            tc = "C"
            note = ("bước " + _SPACING.search(raw).group(1) + " mm, cần chiều dài phân bố để ra số thanh"
                    if _SPACING.search(raw) else "không ghi số thanh")
        elif L is None:
            tc, note = "C", "không ghi chiều dài L="
        if mult > 1:
            note = (note + "; " if note else "") + f"nhân {mult} theo ghi chú"
        it = RebarItem(so_hieu, d, n, L, [e.handle], raw, e.point, tc, note)
        seen[key] = it
        out.append(it)
    return out


def rebar_by_diameter(items: list[RebarItem]) -> dict[int, dict]:
    out: dict[int, dict] = {}
    for it in items:
        g = out.setdefault(it.d_mm, {"so_dong": 0, "tong_dai_m": 0.0, "tong_kg": 0.0, "thieu": 0})
        g["so_dong"] += 1
        if it.tong_kg is None:
            g["thieu"] += 1
        else:
            g["tong_dai_m"] = round(g["tong_dai_m"] + it.tong_dai_m, 3)
            g["tong_kg"] = round(g["tong_kg"] + it.tong_kg, 2)
    return dict(sorted(out.items()))

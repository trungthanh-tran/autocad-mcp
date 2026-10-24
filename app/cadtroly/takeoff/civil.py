"""Bóc khối lượng cầu đường từ bản vẽ AutoCAD thường (bản vẽ tay, Nova-TDN, xuất từ phần mềm khác).

Không cần đối tượng Civil 3D: chỉ đọc TEXT/MTEXT đã có trên bản vẽ.

  earthwork  đào đắp từ trắc ngang. Mỗi trắc ngang có text lý trình (Km0+100) và text diện tích
             (F đào = 12.35, hoặc ô "Diện tích đào" cạnh ô số). Khối lượng giữa hai trắc ngang liền
             kề = (F1 + F2) / 2 × khoảng cách (phương pháp mặt cắt trung bình).
  rebar      thống kê thép từ ghi chú: "N1 12Ø16 L=5200", "6%%c22 L=12.5", "F1-D25-125". KL = số thanh × dài ×
             khối lượng 1 m dài theo Bảng 2 TCVN 1651-2:2018 / TCVN 1651-1:2018 (cỡ ngoài bảng: công thức của Bảng 2).

Không suy diễn: chỗ không rõ (diện tích nằm giữa hai lý trình, một đầu đoạn không ghi diện tích, hai giá trị cùng
loại, L= không ghi đơn vị, ghi chú thép lặp ở nhiều chỗ) không tự chọn — để trống (C) và trả câu hỏi can_hoi;
chỉ tính khi người dùng trả lời qua tham số. Tin cậy: A đọc thẳng một text hoặc theo chỉ định của người dùng;
B ghép nhãn với ô số cùng hàng (chỉ khi duy nhất một ô ứng viên); C thiếu dữ liệu / chờ trả lời.
"""
from __future__ import annotations

import math
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field

from ..reader.model import Drawing, Entity



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


def find_areas(dwg: Drawing, *, gan_o_so: dict[str, str] | None = None) -> tuple[list[AreaItem], list[dict]]:
    """Diện tích ghi trên trắc ngang: 'F đào = 12.35' (A) hoặc ô nhãn 'Diện tích đào' + ô số cùng hàng bên phải (B).

    Ô nhãn có từ hai ô số ứng viên gần tương đương → không ghép, trả câu hỏi (gan_o_so={handle nhãn: handle ô số}).
    """
    gan_o_so = gan_o_so or {}
    texts = [e for e in dwg.texts() if e.point]
    by_handle = {e.handle: e for e in texts}
    nums = [(e, _ONLY_NUM.match(e.text or "")) for e in texts]
    nums = [(e, _num(m.group(1))) for e, m in nums if m]
    used: set[str] = set()
    out: list[AreaItem] = []
    hoi: list[dict] = []
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
            continue                       # có số mà không đúng dạng "nhãn = số": không đọc
        if e.handle in gan_o_so:
            ne = by_handle.get(gan_o_so[e.handle])
            mm = _ONLY_NUM.match(ne.text or "") if ne else None
            if mm:
                used.add(ne.handle)
                out.append(AreaItem(cat[0], cat[1], _num(mm.group(1)), [e.handle, ne.handle], e.point,
                                    f"{e.text} | {ne.text}", "A", "người dùng chỉ định ô số"))
            continue
        h = _h(e)
        cands = []
        for ne, v in nums:
            if ne.handle in used:
                continue
            dx, dy = ne.point[0] - e.point[0], ne.point[1] - e.point[1]
            if 0 < dx <= 40 * h and abs(dy) <= 0.8 * h:
                cands.append((dx, ne, v))
        cands.sort(key=lambda c: c[0])
        if not cands:
            continue
        if len(cands) > 1 and cands[1][0] < 1.5 * cands[0][0]:
            hoi.append({"ma": "o_so", "cau_hoi": f"Ô nhãn '{e.text}' (handle {e.handle}) có nhiều ô số cùng hàng: "
                                                 + ", ".join(f"{c[1].text} ({c[1].handle})" for c in cands[:4])
                                                 + ". Ô nào là giá trị của nhãn này?",
                        "tham_so": "gan_o_so", "vi_du": {e.handle: cands[0][1].handle}})
            continue
        used.add(cands[0][1].handle)
        out.append(AreaItem(cat[0], cat[1], cands[0][2], [e.handle, cands[0][1].handle], e.point,
                            f"{e.text} | {cands[0][1].text}", "B", "ghép nhãn với ô số cùng hàng"))
    return out, hoi


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
    points: list[tuple[float, float]] = field(default_factory=list)     # mọi chỗ ghi lý trình này
    conflict: set[str] = field(default_factory=set)                     # loại có 2 giá trị, chưa được trả lời

    def dist(self, p) -> float:
        return min(_dist(q, p) for q in (self.points or [self.point]))


def earthwork(dwg: Drawing, *, thieu_dien_tich: str | None = None, cong_trung: bool | None = None,
              gan: dict[str, str] | None = None, gan_o_so: dict[str, str] | None = None) -> dict:
    """Ghép diện tích về trắc ngang rồi tính khối lượng giữa các trắc ngang liền kề.

    Không tự quyết những chỗ không rõ — trả về can_hoi, chỉ tính khi người dùng trả lời qua tham số:
      thieu_dien_tich  "bang_0" (một đầu đoạn không ghi = 0) | "bo_doan" (không tính đoạn đó)
      cong_trung       True: cộng hai giá trị cùng loại ở một trắc ngang; False: không cộng (để trống, báo)
      gan              {handle text diện tích: "Km0+020"} khi diện tích nằm giữa hai lý trình
      gan_o_so         {handle ô nhãn: handle ô số} khi một nhãn có nhiều ô số ứng viên
    """
    gan = gan or {}
    hoi: list[dict] = []
    stations: dict[float, Section] = {}
    for e in dwg.texts():
        s = parse_station(e.text or "") if e.point else None
        if s is None:
            continue
        if s in stations:
            stations[s].points.append(e.point)        # cùng lý trình ghi nhiều chỗ: cùng một trắc ngang
            continue
        stations[s] = Section(s, e.text or "", e.handle, e.point, points=[e.point])
    areas, hoi_o = find_areas(dwg, gan_o_so=gan_o_so)
    hoi.extend(hoi_o)
    secs = list(stations.values())
    if not secs:
        return {"sections": [], "segments": [], "totals": {}, "names": {}, "unassigned": areas, "can_hoi": hoi,
                "warnings": ["Không thấy text lý trình dạng Km0+100 hoặc 'Lý trình: 0+100'."]}
    names: dict[str, str] = {}
    unassigned: list[AreaItem] = []
    pending: dict[tuple[float, str], list[AreaItem]] = defaultdict(list)
    for a in areas:
        names[a.loai] = a.ten
        key = next((h for h in a.handles if h in gan), None)
        if key is not None:
            st = parse_station(gan[key])
            sec = stations.get(st) if st is not None else None
            if sec is None:
                unassigned.append(a)
                hoi.append({"ma": "gan", "cau_hoi": f"Lý trình '{gan[key]}' chỉ định cho '{a.text}' không có trên bản vẽ.",
                            "tham_so": "gan"})
                continue
            pending[(sec.station_m, a.loai)].append(a)
            continue
        ranked = sorted(secs, key=lambda s: s.dist(a.point))
        if len(ranked) > 1 and ranked[1].dist(a.point) < 1.25 * ranked[0].dist(a.point):
            unassigned.append(a)
            hoi.append({"ma": "gan", "cau_hoi": f"Diện tích '{a.text}' (handle {a.handles[0]}) nằm giữa "
                                               f"{ranked[0].label} và {ranked[1].label}: thuộc trắc ngang nào?",
                        "tham_so": "gan", "vi_du": {a.handles[0]: ranked[0].label}})
            continue
        pending[(ranked[0].station_m, a.loai)].append(a)

    for (st, loai), items in pending.items():
        sec = stations[st]
        if len(items) > 1 and cong_trung is not True:
            sec.conflict.add(loai)
            sec.sources.setdefault(loai, []).extend(h for a in items for h in a.handles)
            sec.ghi_chu.append(f"{names[loai]}: {len(items)} giá trị ({', '.join(f'{a.f_m2:g}' for a in items)})"
                               + (" — không cộng theo chỉ định" if cong_trung is False else " — chờ trả lời"))
            if cong_trung is None:
                hoi.append({"ma": "cong_trung", "cau_hoi": f"{sec.label} có {len(items)} giá trị {names[loai]}: "
                                                           + ", ".join(f"{a.f_m2:g} ({a.handles[0]})" for a in items)
                                                           + ". Cộng lại, hay chỉ định lại trắc ngang cho từng giá trị?",
                            "tham_so": "cong_trung | gan"})
            continue
        sec.areas[loai] = round(sum(a.f_m2 for a in items), 4)
        sec.sources.setdefault(loai, []).extend(h for a in items for h in a.handles)
        sec.tin_cay[loai] = max(a.tin_cay for a in items)
        for a in items:
            if a.ghi_chu:
                sec.ghi_chu.append(a.ghi_chu)
        if len(items) > 1:
            sec.ghi_chu.append(f"{names[loai]}: cộng {len(items)} giá trị theo chỉ định")

    secs.sort(key=lambda s: s.station_m)
    segments, totals, missing = [], {}, []
    incomplete: set[str] = set()
    for s1, s2 in zip(secs, secs[1:]):
        L = round(s2.station_m - s1.station_m, 3)
        seg = {"tu": s1.label, "den": s2.label, "tu_m": s1.station_m, "den_m": s2.station_m, "L_m": L,
               "khoi_luong": {}, "tin_cay": {}}
        for loai in sorted(set(s1.areas) | set(s2.areas) | s1.conflict | s2.conflict):
            if loai in s1.conflict or loai in s2.conflict:
                seg["khoi_luong"][loai], seg["tin_cay"][loai] = None, "C"
                incomplete.add(loai)
                continue
            f1, f2 = s1.areas.get(loai), s2.areas.get(loai)
            if f1 is None or f2 is None:
                if thieu_dien_tich == "bang_0":
                    f1, f2, tc = f1 or 0.0, f2 or 0.0, "A"
                else:
                    seg["khoi_luong"][loai], seg["tin_cay"][loai] = None, "C"
                    if thieu_dien_tich is None:
                        missing.append(f"{s1.label}–{s2.label} ({names.get(loai, loai)})")
                    incomplete.add(loai)
                    continue
            else:
                tc = max(s1.tin_cay.get(loai, "A"), s2.tin_cay.get(loai, "A"))
            v = round((f1 + f2) / 2 * L, 3)
            seg["khoi_luong"][loai] = v
            seg["tin_cay"][loai] = tc
            totals[loai] = round(totals.get(loai, 0.0) + v, 3)
        segments.append(seg)
    if missing:
        hoi.append({"ma": "thieu_dien_tich", "cau_hoi": "Các đoạn có một đầu không ghi diện tích: " + "; ".join(missing[:12])
                    + ("…" if len(missing) > 12 else "") + ". Coi đầu không ghi bằng 0, hay không tính các đoạn này?",
                    "tham_so": "thieu_dien_tich", "lua_chon": ["bang_0", "bo_doan"]})
    warnings = []
    empty = [s.label for s in secs if not s.areas and not s.conflict]
    if empty:
        warnings.append(f"{len(empty)} trắc ngang không thấy diện tích: {', '.join(empty[:10])}")
    if len(secs) == 1:
        warnings.append("Chỉ có một trắc ngang, chưa tính được khối lượng.")
    if incomplete:
        warnings.append("Tổng chưa đủ (có đoạn chưa tính): " + ", ".join(names.get(k, k) for k in sorted(incomplete)))
    return {"sections": secs, "segments": segments, "totals": totals, "names": names, "unassigned": unassigned,
            "incomplete": sorted(incomplete), "can_hoi": hoi, "warnings": warnings}


# ---------------------------------------------------------------------- thép
_DIA = r"(?:%%c|[øØΦφ∅⌀]|\\U\+2205|\\U\+00D8)"
# số thanh không được dính chữ phía trước (N4 Ø10 là số hiệu N4, không phải 4 thanh); 'x' là phép nhân
_BAR = re.compile(r"(?:(?<![A-Za-z\d])(\d+)\s*[x×*]\s*)?(?:(?<![A-WYZa-wyz\d])(\d+))?\s*" + _DIA + r"\s*(\d{1,2})\b", re.I)
_LEN = re.compile(r"\bL\s*=\s*(\d+(?:[.,]\d+)?)\s*(mm|m)?", re.I)
_SPACING = re.compile(r"\b[aA@]\s*=?\s*(\d{2,3})\b")
# Kiểu ghi bản vẽ cầu/hầm: số hiệu-D đường kính[-bước], ví dụ S4-D14, F1-D25-125, H2-D14-250
_MARK_D = re.compile(r"(?<![A-Za-z\d])([A-Z]{1,2}\d{1,2}[a-z]?)\s*-\s*D(\d{1,2})(?:\s*-\s*(\d{2,3}))?\b")
# Khối lượng 1 m dài "yêu cầu" và sai lệch cho phép — chép từ Bảng 2 TCVN 1651-2:2018 (thép vằn, d 6…50) và
# Bảng 2 TCVN 1651-1:2018 (thép trơn, d 6…40, cùng giá trị); đã đọc trực tiếp văn bản ngày 2026-10-24, xem
# kho-mac-dinh/tieu-chuan/tcvn-cot-thep.rules.json "doi_chieu". Cỡ ngoài bảng → công thức của chính Bảng 2:
# 7,85·10⁻³ × 0,7854·d² (ghi rõ trong Excel là ngoài bảng).
NOMINAL_KG_PER_M = {6: 0.222, 8: 0.395, 10: 0.617, 12: 0.888, 14: 1.21, 16: 1.58, 18: 2.00, 20: 2.47,
                    22: 2.98, 25: 3.85, 28: 4.83, 32: 6.31, 36: 7.99, 40: 9.86, 50: 15.42}
MASS_TOLERANCE_PCT = {6: 8, 8: 8, 10: 6, 12: 6, 14: 5, 16: 5, 18: 5, 20: 5, 22: 5,
                      25: 4, 28: 4, 32: 4, 36: 4, 40: 4, 50: 4}
_GRADE = re.compile(r"\bCB\s*(\d{3})\s*-?\s*([TV])\b", re.I)   # đọc mọi mác dạng CBxxx-T/V; hợp lệ hay không do quy tắc
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
    buoc_mm: float | None = None              # bước thép (a200, -250)
    mac: str = ""                             # mác thép ghi cùng ghi chú (CB400-V)
    L_raw: float | None = None                # số sau L= như ghi, chưa đổi đơn vị
    L_unit_missing: bool = False              # L= không ghi đơn vị và chưa được trả lời
    trung: int = 1                            # số chỗ ghi cùng ghi chú
    cho_tra_loi: bool = False                 # còn câu hỏi chưa trả lời → không tính khối lượng

    @property
    def tong_dai_m(self) -> float | None:
        if self.cho_tra_loi or not (self.so_thanh and self.dai_m):
            return None
        return round(self.so_thanh * self.dai_m, 3)

    @property
    def kg_per_m(self) -> float:
        return NOMINAL_KG_PER_M.get(self.d_mm, round(7.85e-3 * 0.7854 * self.d_mm ** 2, 4))

    @property
    def trong_bang(self) -> bool:
        return self.d_mm in NOMINAL_KG_PER_M

    @property
    def tong_kg(self) -> float | None:
        return round(self.tong_dai_m * self.kg_per_m, 2) if self.tong_dai_m else None


def rebar(dwg: Drawing, *, trung_lap: str | None = None, don_vi_L: str | None = None) -> list[RebarItem]:
    """Mỗi ghi chú thép một dòng. Không tự quyết chỗ không rõ (xem rebar_questions):
      don_vi_L   "mm" | "m" cho L= không ghi đơn vị; chưa trả lời → dài để trống (C)
      trung_lap  "mot_lan" (ghi chú giống nhau ở nhiều chỗ là cùng một thanh) | "tung_cho" (mỗi chỗ là thanh riêng);
                 chưa trả lời → khối lượng các dòng trùng để trống (C)
    """
    out: list[RebarItem] = []
    seen: dict[tuple, RebarItem] = {}
    for e in dwg.texts():
        raw = e.text or ""
        m = _BAR.search(raw)
        md = None if m else _MARK_D.search(raw)
        if not m and not md:
            continue
        if m:
            mult = int(m.group(1)) if m.group(1) else 1
            n = int(m.group(2)) * mult if m.group(2) else None
            d = int(m.group(3))
        else:
            mult, n, d = 1, None, int(md.group(2))
        if not 6 <= d <= 50:
            continue
        L, L_raw, L_unit_missing = None, None, False
        lm = _LEN.search(raw)
        if lm:
            L_raw = _num(lm.group(1))
            unit = (lm.group(2) or "").lower() or (don_vi_L or "").lower()
            if unit == "m":
                L = L_raw
            elif unit == "mm":
                L = L_raw / 1000
            else:
                L_unit_missing = True
        if m:
            mk = _MARK.search(raw[: m.start()])
            so_hieu = next((g for g in mk.groups() if g), "").replace(" ", "").upper() if mk else ""
            sp = _SPACING.search(raw)
            buoc = float(sp.group(1)) if sp else None
        else:
            so_hieu, buoc = md.group(1).upper(), (float(md.group(3)) if md.group(3) else None)
        g = _GRADE.search(raw)
        mac = f"CB{g.group(1)}-{g.group(2).upper()}" if g else ""
        key = (so_hieu or ascii_lower(raw).strip(), d, n, L_raw)
        if key in seen and trung_lap != "tung_cho":
            dup = seen[key]
            dup.handles.append(e.handle)
            dup.trung = len(dup.handles)
            continue
        tc, note = "A", ""
        if n is None:
            tc = "C"
            note = (f"bước {buoc:g} mm, cần chiều dài phân bố để ra số thanh" if buoc else "không ghi số thanh")
        elif L_unit_missing:
            tc, note = "C", f"L={L_raw:g} không ghi đơn vị — chờ xác nhận mm hay m"
        elif L is None:
            tc, note = "C", "không ghi chiều dài L="
        if mult > 1:
            note = (note + "; " if note else "") + f"nhân {mult} theo ghi chú"
        it = RebarItem(so_hieu, d, n, L, [e.handle], raw, e.point, tc, note, buoc, mac)
        it.L_raw, it.L_unit_missing = L_raw, L_unit_missing
        seen[key] = it
        out.append(it)
    for it in out:
        if it.trung > 1:
            if trung_lap == "mot_lan":
                it.ghi_chu = (it.ghi_chu + "; " if it.ghi_chu else "") + \
                    f"ghi ở {it.trung} chỗ, tính 1 lần theo chỉ định"
            else:
                it.tin_cay = "C"
                it.cho_tra_loi = True
                it.ghi_chu = (it.ghi_chu + "; " if it.ghi_chu else "") + \
                    f"ghi ở {it.trung} chỗ — chờ trả lời cùng một thanh hay thanh riêng"
    return out


def rebar_questions(items: list[RebarItem]) -> list[dict]:
    hoi = []
    nounit = [it for it in items if it.L_unit_missing]
    if nounit:
        hoi.append({"ma": "don_vi_L", "cau_hoi": f"{len(nounit)} ghi chú có L= không ghi đơn vị (ví dụ "
                                                 + ", ".join(f"'{it.text.strip()}'" for it in nounit[:4])
                                                 + "). Chiều dài L là mm hay m?",
                    "tham_so": "don_vi_L", "lua_chon": ["mm", "m"]})
    dups = [it for it in items if it.cho_tra_loi]
    if dups:
        hoi.append({"ma": "trung_lap", "cau_hoi": f"{len(dups)} ghi chú thép xuất hiện ở nhiều chỗ (ví dụ "
                                                  + ", ".join(f"'{it.text.strip()}' × {it.trung}" for it in dups[:4])
                                                  + "). Đó là cùng một thanh ghi ở nhiều hình chiếu (tính 1 lần), "
                                                    "hay mỗi chỗ là thanh riêng (tính từng chỗ)?",
                    "tham_so": "trung_lap", "lua_chon": ["mot_lan", "tung_cho"]})
    return hoi


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

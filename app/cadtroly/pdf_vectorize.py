"""PDF-to-DXF conversion used directly by the MCP ``pdf_vectorize`` tool.

Giữ bản vẽ liền như bản gốc, không vỡ vụn:
- Mỗi nét PDF (một path) thành một polyline liền: các đoạn nối tiếp được nối lại, path đóng thì polyline đóng;
  hình chữ nhật ``re`` không bị bỏ. Độ dày nét → lineweight, nét đứt → linetype đúng mẫu gạch của PDF,
  màu nét giữ nguyên, hình đặc nhỏ (mũi tên) → HATCH đặc.
- Chữ đặt theo đường chân chữ (origin) và đúng góc xoay; các mảnh (span) cùng một dòng gộp thành một TEXT.
- Kích thước dựng lại thành DIMENSION thật: con số + đường dim song song cạnh nó + vạch chặn/mũi tên hoặc đường
  gióng ở hai đầu. DIMLFAC suy từ chính số ghi / chiều dài đo, nên DIMENSION hiển thị đúng số trên PDF; số không
  khớp (hoặc dạng 25x250=6250) giữ nguyên chữ gốc làm text override. Các mảnh đã gộp vào DIMENSION không ghi lại.
- Toạ độ trên khổ A1 (841 × 594 mm), cùng một hệ số co cho hai trục, trang xoay xử lý đúng.
"""

from __future__ import annotations

import math
import re
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import ezdxf
import pymupdf
from ezdxf import colors as ezcolors

PAPER_W = 841.0
PAPER_H = 594.0
CAP_HEIGHT = 0.72            # chiều cao chữ hoa / cỡ chữ PDF (em) — DXF TEXT height là chiều cao chữ hoa
JOIN_TOL = 0.05              # mm trên giấy: hai đầu đoạn gần hơn → coi là nối liền
VIEW_GAP = 4.0               # mm trên giấy: nét cách nhau ít hơn → cùng một hình (các hình trên tờ cách xa hơn)
LINEWEIGHTS = (0, 5, 9, 13, 15, 18, 20, 25, 30, 35, 40, 50, 53, 60, 70, 80, 90, 100, 106, 120, 140, 158, 200, 211)


# ------------------------------------------------------------------ toạ độ
class _Transform:
    """PDF (y xuống, có thể xoay) → giấy A1 mm (y lên), cùng hệ số cho hai trục."""

    def __init__(self, pw: float, ph: float, rotation: int):
        self.pw, self.ph, self.rot = pw, ph, rotation
        self.dw, self.dh = (ph, pw) if rotation in (90, 270) else (pw, ph)
        self.s = min(PAPER_W / self.dw, PAPER_H / self.dh)

    def display(self, x: float, y: float) -> tuple[float, float]:
        r = self.rot
        if r == 90:
            return self.ph - y, x
        if r == 180:
            return self.pw - x, self.ph - y
        if r == 270:
            return y, self.pw - x
        return x, y

    def __call__(self, p) -> tuple[float, float]:
        dx, dy = self.display(float(p[0]), float(p[1]))
        return dx * self.s, (self.dh - dy) * self.s

    def norm(self, x: float, y: float) -> tuple[float, float]:
        """Vị trí tương đối trên trang hiển thị (0..1, y xuống) — cho phân loại layer."""
        dx, dy = self.display(x, y)
        return dx / self.dw, dy / self.dh


# ------------------------------------------------------------- phân layer
_DIM_RE = re.compile(r"(?:\d+[.,]?\d*|±\s*\d|\+\s*\d).*?(?:mm|m|°)?$", re.I)
_TITLE_WORDS = ("ground floor", "rest room", "elevation", "section", "plan", "drawing no", "scale")
_NOTE_WORDS = ("note", "all dimensions", "hvac", "downspout", "see ", "typ.", "level", "finish")

# The PDF exporter preserved the original DWG layer names in each vector
# drawing.  Use those names first; geometric heuristics are only the fallback
# for the many unnamed/ambiguous paths in a plotted sheet.
_SOURCE_LAYER_GROUPS = {
    "PDF_COLUMNS": {"COL", "CTL"},
    "PDF_WALLS": {"WALL-C", "TUONG XAY", "TUONG XAY"},
    "PDF_DOORS": {"DO", "DOOR", "A_DOOR", "4DOOR"},
    "PDF_WINDOWS": {"WINDOW", "WID", "A_WID", "PANEL W"},
    "PDF_FURNITURE": {"FUR", "NHA", "BLOCK-H"},
    "PDF_SANITARY": {"AA-FFXM-SANI", "BM_화장실 세면기", "TOI"},
    "PDF_DIMENSIONS": {"DIM", "KICHTHUOC", "DMCAI", "4DP"},
    "PDF_HATCH": {"HATCH", "HAT", "5HAT", "CON HATCH", "INSUL"},
    "PDF_STRUCTURE": {"CONC", "2CONC"},
    "PDF_FINISHES": {"FIN", "FINISH", "6FIN"},
    "PDF_CEILING": {"CEILING"},
    "PDF_LIGHTING": {"LED"},
    "PDF_SECTIONS_ELEVATIONS": {"2SEC", "3SEC", "4ELE", "3ELE", "ELE3", "BM_ELEV", "7ELE"},
    "PDF_SITE": {
        "_ROAD", "_WALKWAY", "TALUY", "TALUYN", "TALUYD", "DUONG NHUA",
        "DUONG DAT", "THUY HE", "V_CONTOUR_00-04", "V_CONTOUR_05-09",
        "V_CONTOUR_10-14", "V_DONGMUC", "FA_SD", "CAOTHE", "DIA VAT",
        "DIAVAT", "HO GA", "BO KENH", "CAU CONG",
    },
    "PDF_REFERENCE": {"KE", "CEN", "CENTER", "AXIS BOX", "KATA_GRID", "TIM"},
    "PDF_DETAIL_LINES": {"3BLOCK", "4CAGE", "5CAGE", "LEAN", "DTL", "HATHE"},
    "PDF_SYMBOLS": {"SYM", "SYMBOL", "BUBBLE", "CMARK", "E_SYM-EMR", "E_SYM-NOR", "ORIENTATE", "MARK"},
    "PDF_NOTES": {"NOTE TEXT-M(T)", "KEY TEXT(T)", "TK"},
    "PDF_TITLE": {"TITLE", "TAN-TIT", "REV.1", "REV.B", "REV.C", "REV.D"},
    "PDF_TEXT": {"TEXT", "M TEXT", "M TEXT(T)", "TEXT_3", "TXT", "BUBB-TEXT", "VNTIME", "TVL"},
}

_SOURCE_TO_GROUP = {
    source: group
    for group, sources in _SOURCE_LAYER_GROUPS.items()
    for source in sources
}

LAYER_COLORS = {
    "PDF_FRAME": 8, "PDF_GEOMETRY": 7, "PDF_HATCH": 9, "PDF_COLUMNS": 30, "PDF_WALLS": 31, "PDF_DOORS": 32,
    "PDF_WINDOWS": 33, "PDF_FURNITURE": 34, "PDF_SANITARY": 35, "PDF_STRUCTURE": 36, "PDF_FINISHES": 37,
    "PDF_CEILING": 38, "PDF_LIGHTING": 39, "PDF_SECTIONS_ELEVATIONS": 40, "PDF_SITE": 41, "PDF_REFERENCE": 42,
    "PDF_DETAIL_LINES": 43, "PDF_SYMBOLS": 4, "PDF_DIMENSIONS": 3, "PDF_TEXT": 2, "PDF_NOTES": 6, "PDF_TITLE": 1,
}


def _text_layer(text, center_norm, size):
    nx, ny = center_norm
    folded = text.casefold()
    if any(word in folded for word in _TITLE_WORDS) or size >= 14:
        return "PDF_TITLE"
    if any(word in folded for word in _NOTE_WORDS) or len(text) > 42:
        return "PDF_NOTES"
    if _DIM_RE.search(text) or re.fullmatch(r"[A-Z]?\s*\d+(?:[.,]\d+)?", text):
        return "PDF_DIMENSIONS"
    if nx < 0.06 or nx > 0.94 or ny < 0.06 or ny > 0.94:
        return "PDF_FRAME"
    return "PDF_TEXT"


def _drawing_layer(drawing, tf: _Transform):
    source_layer = (drawing.get("layer") or "").strip().upper()
    if source_layer in _SOURCE_TO_GROUP:
        return _SOURCE_TO_GROUP[source_layer]
    r = drawing["rect"]
    (ax, ay), (bx, by) = tf.display(r.x0, r.y0), tf.display(r.x1, r.y1)
    width, height = abs(bx - ax), abs(by - ay)
    area = width * height
    nx, ny = (ax + bx) / (2 * tf.dw), (ay + by) / (2 * tf.dh)
    if drawing.get("fill") is not None:
        return "PDF_HATCH"
    if nx < 0.025 or nx > 0.975 or ny < 0.025 or ny > 0.975:
        return "PDF_FRAME"
    if area < 180 or max(width, height) < 22:
        return "PDF_SYMBOLS"
    if len(drawing.get("items", ())) >= 20 and max(width, height) < 80:
        return "PDF_SYMBOLS"
    return "PDF_GEOMETRY"


# --------------------------------------------------------------- nét PDF
@dataclass
class _Prim:
    pts: list[tuple[float, float]]
    closed: bool
    layer: str
    style: dict
    fill: tuple | None = None
    stroke: bool = True
    used: bool = False

    @property
    def is_segment(self) -> bool:
        return len(self.pts) == 2 and not self.closed

    def bbox(self):
        xs, ys = [p[0] for p in self.pts], [p[1] for p in self.pts]
        return min(xs), min(ys), max(xs), max(ys)


def _bezier(p0, p1, p2, p3, tf: _Transform) -> list[tuple[float, float]]:
    pts = [tf(p) for p in (p0, p1, p2, p3)]
    approx = sum(math.dist(pts[i], pts[i + 1]) for i in range(3))
    n = max(4, min(48, int(approx / 0.4)))          # ~0.4 mm mỗi đoạn trên giấy
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1.0 - t
        out.append(tuple(u ** 3 * a + 3 * u * u * t * b + 3 * u * t * t * c + t ** 3 * d
                         for a, b, c, d in zip(*pts)))
    return out


def _dash_pattern(dashes: str | None, scale: float) -> list[float] | None:
    """'[3 2] 0' (pt) → [tổng, gạch, -hở, …] (mm giấy) theo quy ước linetype DXF; nét liền → None."""
    if not dashes:
        return None
    m = re.search(r"\[([^\]]*)\]", dashes)
    nums = [float(v) * scale for v in (m.group(1).split() if m else [])]
    nums = [v for v in nums if v > 1e-6]
    if not nums:
        return None
    if len(nums) % 2:
        nums = nums * 2
    pat = [v if i % 2 == 0 else -v for i, v in enumerate(nums)]
    return [round(sum(nums), 4)] + [round(v, 4) for v in pat]


def _lineweight(width_mm: float) -> int:
    hundredths = width_mm * 100
    return min(LINEWEIGHTS, key=lambda w: abs(w - hundredths))


def _true_color(rgb) -> int | None:
    if not rgb:
        return None
    r, g, b = (int(round(max(0.0, min(1.0, float(c))) * 255)) for c in rgb[:3])
    if abs(r - g) < 8 and abs(g - b) < 8:          # đen/xám/trắng: để màu theo layer
        return None
    return ezcolors.rgb2int((r, g, b))


def _primitives(drawing, tf: _Transform, layer: str, linetypes: dict, doc) -> list[_Prim]:
    # lineweight theo bề rộng in thật của nét trên PDF (1 pt = 0.3528 mm), không nhân hệ số phóng khổ giấy
    width = float(drawing.get("width") or 0.0) * 25.4 / 72
    style = {"lineweight": _lineweight(width)} if drawing.get("width") is not None else {}
    pat = _dash_pattern(drawing.get("dashes"), tf.s)
    if pat:
        key = tuple(pat)
        if key not in linetypes:
            name = f"PDF_DASH_{len(linetypes) + 1}"
            doc.linetypes.add(name, pattern=list(pat), description="Nét đứt theo PDF")
            linetypes[key] = name
        style["linetype"] = linetypes[key]
    color = _true_color(drawing.get("color"))
    if color is not None:
        style["true_color"] = color
    fill = drawing.get("fill")
    kind = drawing.get("type", "s")
    stroke = kind in ("s", "fs") or fill is None

    out: list[_Prim] = []
    chain: list[tuple[float, float]] = []

    def flush():
        nonlocal chain
        if len(chain) >= 2:
            closed = len(chain) > 3 and math.dist(chain[0], chain[-1]) < JOIN_TOL
            pts = chain[:-1] if closed else chain
            out.append(_Prim(pts, closed, layer, dict(style), fill, stroke))
        chain = []

    def extend(pts):
        nonlocal chain
        if chain and math.dist(chain[-1], pts[0]) < JOIN_TOL:
            chain.extend(pts[1:])
        else:
            flush()
            chain = list(pts)

    for item in drawing["items"]:
        k = item[0]
        if k == "l":
            a, b = tf(item[1]), tf(item[2])
            if math.dist(a, b) > 1e-5:
                extend([a, b])
        elif k == "c":
            extend(_bezier(item[1], item[2], item[3], item[4], tf))
        elif k == "re":
            flush()
            r = item[1]
            out.append(_Prim([tf((r.x0, r.y0)), tf((r.x1, r.y0)), tf((r.x1, r.y1)), tf((r.x0, r.y1))],
                             True, layer, dict(style), fill, stroke))
        elif k == "qu":
            flush()
            q = item[1]
            out.append(_Prim([tf(p) for p in (q.ul, q.ur, q.lr, q.ll)], True, layer, dict(style), fill, stroke))
    if drawing.get("closePath") and chain and len(chain) > 2 and math.dist(chain[0], chain[-1]) >= JOIN_TOL:
        chain.append(chain[0])
    flush()
    if fill is not None:
        for p in out:
            if not p.closed and len(p.pts) > 2:       # PDF tô kín cả path hở
                p.closed = True
    return out


# ------------------------------------------------------------------- chữ
@dataclass
class _Text:
    text: str
    insert: tuple[float, float]
    angle: float                     # độ, trên giấy
    height: float                    # chiều cao chữ hoa, mm giấy
    width: float                     # bề rộng dòng chữ, mm giấy
    layer: str
    used: bool = False

    @property
    def dir(self) -> tuple[float, float]:
        a = math.radians(self.angle)
        return math.cos(a), math.sin(a)

    @property
    def center(self) -> tuple[float, float]:
        ux, uy = self.dir
        vx, vy = -uy, ux
        return (self.insert[0] + ux * self.width / 2 + vx * self.height / 2,
                self.insert[1] + uy * self.width / 2 + vy * self.height / 2)


def _texts(page, tf: _Transform) -> list[_Text]:
    out = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            spans = [s for s in line.get("spans", []) if s.get("text", "").strip()]
            if not spans:
                continue
            dx, dy = line.get("dir", (1.0, 0.0))
            parts, prev = [], None
            for s in spans:
                if prev is not None:
                    gap = (s["bbox"][0] - prev["bbox"][2]) if abs(dy) < 0.5 else abs(s["bbox"][1] - prev["bbox"][3])
                    if gap > 0.25 * float(s.get("size", 8.0)) and not parts[-1].endswith(" "):
                        parts.append(" ")
                parts.append(s["text"])
                prev = s
            text = "".join(parts).strip()
            ox, oy = spans[0]["origin"]
            size = max(float(s.get("size", 8.0)) for s in spans)
            p0 = tf((ox, oy))
            p1 = tf((ox + dx * 10.0, oy + dy * 10.0))
            angle = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
            x0, y0, x1, y1 = line["bbox"]
            along = math.hypot((x1 - x0) * dx, (y1 - y0) * dy) if abs(dx) > 1e-6 and abs(dy) > 1e-6 else \
                (x1 - x0 if abs(dx) >= abs(dy) else y1 - y0)
            cx, cy = tf.norm((x0 + x1) / 2, (y0 + y1) / 2)
            out.append(_Text(text, p0, round(angle, 4) % 360, max(0.5, size * CAP_HEIGHT * tf.s),
                             abs(along) * tf.s, _text_layer(text, (cx, cy), size)))
    return out


# -------------------------------------------------------------- kích thước
_DIM_VALUE = re.compile(r"^(?:\d+(?:[.,]\d+)?\s*[x×]\s*\d+(?:[.,]\d+)?\s*=\s*)?(\d+(?:[.,]\d+)?)$")


class _Grid:
    def __init__(self, cell: float):
        self.cell = cell
        self.cells: dict[tuple[int, int], list[int]] = defaultdict(list)

    def add(self, i: int, bbox):
        c = self.cell
        for gx in range(int(bbox[0] // c), int(bbox[2] // c) + 1):
            for gy in range(int(bbox[1] // c), int(bbox[3] // c) + 1):
                self.cells[(gx, gy)].append(i)

    def near(self, x: float, y: float, r: float) -> set[int]:
        c = self.cell
        out: set[int] = set()
        for gx in range(int((x - r) // c), int((x + r) // c) + 1):
            for gy in range(int((y - r) // c), int((y + r) // c) + 1):
                out.update(self.cells.get((gx, gy), ()))
        return out


def _angle_diff(a: float, b: float) -> float:
    """Độ lệch hướng của hai đường (không phân biệt chiều), 0..90."""
    d = abs((a - b) % 180)
    return min(d, 180 - d)


def _seg_angle(p) -> float:
    (x1, y1), (x2, y2) = p.pts
    return math.degrees(math.atan2(y2 - y1, x2 - x1)) % 180


def _point_seg_dist(pt, a, b) -> float:
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((pt[0] - ax) * dx + (pt[1] - ay) * dy) / L2))
    return math.dist(pt, (ax + t * dx, ay + t * dy))


@dataclass
class _Dim:
    p1: tuple[float, float]          # điểm gốc (chân đường gióng hoặc đầu đường dim)
    p2: tuple[float, float]
    line_a: tuple[float, float]      # hai đầu đường dim
    line_b: tuple[float, float]
    text: _Text
    value: float
    plain: bool                      # chữ chỉ là con số
    ticks: bool                      # vạch chặn (True) hay mũi tên
    parts: list[_Prim] = field(default_factory=list)

    @property
    def length(self) -> float:
        return math.dist(self.line_a, self.line_b)


def _find_dims(prims: list[_Prim], texts: list[_Text]) -> list[_Dim]:
    segs = [i for i, p in enumerate(prims) if p.is_segment and p.stroke]
    small = [i for i, p in enumerate(prims) if p.fill is not None and p.closed and len(p.pts) <= 8]
    grid = _Grid(10.0)
    for i in segs + small:
        grid.add(i, prims[i].bbox())

    dims: list[_Dim] = []
    for t in texts:
        m = _DIM_VALUE.match(t.text.replace(" ", ""))
        if not m:
            continue
        value = float(m.group(1).replace(",", "."))
        if value <= 0:
            continue
        h = t.height
        ux, uy = t.dir
        vx, vy = -uy, ux
        cx, cy = t.center
        band = 2.6 * h
        cand: dict[float, list[tuple[int, float, float]]] = defaultdict(list)
        for i in grid.near(cx, cy, max(band, t.width) + 30):
            p = prims[i]
            if not p.is_segment or _angle_diff(_seg_angle(p), t.angle) > 1.5:
                continue
            (x1, y1), (x2, y2) = p.pts
            off = ((x1 - cx) * vx + (y1 - cy) * vy)
            if abs(off) >= band:
                continue
            s1, s2 = sorted(((x1 - cx) * ux + (y1 - cy) * uy, (x2 - cx) * ux + (y2 - cy) * uy))
            if abs(off) < 0.15 * h and s1 < -0.3 * t.width and s2 > 0.3 * t.width:
                continue                         # đoạn chạy xuyên thân chữ: không phải đường dim của chữ này
            cand[round(off / (0.2 * h))].append((i, s1, s2))
        best = None
        for _, members in cand.items():
            members.sort(key=lambda m_: m_[1])
            spans, cur = [], None
            for i, s1, s2 in members:            # nối các đoạn thẳng hàng, khe nhỏ (đường dim bị cắt quanh chữ)
                if cur and s1 <= cur[1] + 1.5 * t.width + 2 * h:
                    cur[1] = max(cur[1], s2)
                    cur[2].append(i)
                else:
                    cur = [s1, s2, [i]]
                    spans.append(cur)
            for s1, s2, ids in spans:
                if s1 <= 0.0 <= s2 and s2 - s1 >= 0.6 * t.width:
                    off = abs((prims[ids[0]].pts[0][0] - cx) * vx + (prims[ids[0]].pts[0][1] - cy) * vy)
                    if best is None or off < best[0]:
                        best = (off, s1, s2, ids)
        if best is None:
            continue
        _, s1, s2, ids = best
        p0 = prims[ids[0]].pts[0]
        off = (p0[0] - cx) * vx + (p0[1] - cy) * vy
        a = (cx + ux * s1 + vx * off, cy + uy * s1 + vy * off)
        b = (cx + ux * s2 + vx * off, cy + uy * s2 + vy * off)
        line_angle = t.angle % 180
        ends, parts, ticks = [], [prims[i] for i in ids], 0
        for e in (a, b):
            origin, end_ok = e, False
            for j in grid.near(e[0], e[1], 4 * h):
                q = prims[j]
                if q in parts:
                    continue
                if q.fill is not None and q.closed:          # mũi tên đặc chạm đầu đường dim
                    qb = q.bbox()
                    if max(qb[2] - qb[0], qb[3] - qb[1]) < 3 * h and \
                            min(math.dist(e, v) for v in q.pts) < 0.3 * h:
                        parts.append(q)
                        end_ok = True
                    continue
                if not q.is_segment:
                    continue
                L = math.dist(*q.pts)
                ad = _angle_diff(_seg_angle(q), line_angle)
                d = _point_seg_dist(e, *q.pts)
                if d > 0.15 * h:
                    continue
                if 85 <= ad and L > 1.2 * h:                   # đường gióng: gốc là đầu xa đường dim
                    far = max(q.pts, key=lambda v: abs((v[0] - e[0]) * vx + (v[1] - e[1]) * vy))
                    if abs((far[0] - e[0]) * vx + (far[1] - e[1]) * vy) > 0.5 * h:
                        origin = far
                    parts.append(q)
                    end_ok = True
                elif 25 <= ad <= 70 and 0.3 * h <= L <= 4 * h and \
                        math.dist(e, ((q.pts[0][0] + q.pts[1][0]) / 2, (q.pts[0][1] + q.pts[1][1]) / 2)) < 0.4 * L:
                    parts.append(q)                            # vạch chặn xiên qua đầu đường dim
                    ticks += 1
                    end_ok = True
            ends.append((origin, end_ok))
        if not (ends[0][1] and ends[1][1]):
            continue
        plain = bool(re.fullmatch(r"\d+(?:[.,]\d+)?", t.text.strip()))
        dims.append(_Dim(ends[0][0], ends[1][0], a, b, t, value, plain, ticks >= 2, parts))
    return dims


def _scale_clusters(dims: list[_Dim]) -> dict[int, float]:
    """id(dim) → DIMLFAC: trung vị của nhóm có tỉ lệ số ghi / chiều dài giống nhau (±1%)."""
    ratios = sorted((d.value / d.length, id(d)) for d in dims if d.length > 0)
    out, group = {}, []

    def close():
        if group:
            med = statistics.median(r for r, _ in group)
            for _, k in group:
                out[k] = med

    for r, k in ratios:
        if group and r > group[0][0] * 1.01:
            close()
            group = []
        group.append((r, k))
    close()
    return out


def _nice(f: float) -> float:
    """Làm tròn hệ số (60.0003 → 60) chỉ khi sai số đủ nhỏ để số hiển thị trên dim 5 chữ số không lệch."""
    for digits in range(0, 7):
        v = round(f, digits)
        if v and abs(v - f) / f < 2e-5:
            return v
    return round(f, 7)


# ---------------------------------------------------------- nhãn + đường dẫn
@dataclass
class _Leader:
    text: _Text
    vertices: list[tuple[float, float]]       # từ đầu mũi tên tới điểm gần chữ
    arrow: str                                # "" | "_DOT" | "_OBLIQUE" (tên khối mũi tên AutoCAD), "" = mặc định
    parts: list[_Prim] = field(default_factory=list)


def _text_box(t: _Text) -> list[tuple[float, float]]:
    ux, uy = t.dir
    vx, vy = -uy, ux
    x, y = t.insert
    d = -0.3 * t.height                         # phần chân chữ (g, p, y)
    return [(x + vx * d, y + vy * d), (x + ux * t.width + vx * d, y + uy * t.width + vy * d),
            (x + ux * t.width + vx * t.height * 1.1, y + uy * t.width + vy * t.height * 1.1),
            (x + vx * t.height * 1.1, y + vy * t.height * 1.1)]


def _dist_to_box(pt, box) -> float:
    if _inside(pt, box):
        return 0.0
    return min(_point_seg_dist(pt, box[i], box[(i + 1) % 4]) for i in range(4))


def _inside(pt, poly) -> bool:
    x, y = pt
    inside = False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / ((y2 - y1) or 1e-12) + x1:
            inside = not inside
    return inside


def _find_leaders(prims: list[_Prim], texts: list[_Text]) -> list[_Leader]:
    """Nhãn (S2-D25-250, LƯỚI L1…) có một đường dẫn chạm chữ, đầu kia chỉ vào hình — gộp thành MLEADER."""
    cand = [i for i, p in enumerate(prims) if not p.used and p.stroke and p.fill is None and not p.closed
            and 2 <= len(p.pts) <= 4]
    marks = [i for i, p in enumerate(prims) if not p.used and p.closed and len(p.pts) <= 48
             and max(p.bbox()[2] - p.bbox()[0], p.bbox()[3] - p.bbox()[1]) < 4.0]
    cand_ids, mark_ids = set(cand), set(marks)
    grid = _Grid(10.0)
    for i in cand + marks:
        grid.add(i, prims[i].bbox())
    taken: set[int] = set()
    out: list[_Leader] = []
    for t in texts:
        if t.used or t.layer in ("PDF_TITLE", "PDF_FRAME") or len(t.text) < 2 or _DIM_VALUE.match(t.text):
            continue
        h, box = t.height, _text_box(t)
        best = None
        cx, cy = t.center
        for i in grid.near(cx, cy, t.width + 6 * h):
            if i in taken or i not in cand_ids:
                continue
            p = prims[i]
            length = sum(math.dist(p.pts[k], p.pts[k + 1]) for k in range(len(p.pts) - 1))
            if not (2 * h <= length <= 25 * h):
                continue
            da, db = _dist_to_box(p.pts[0], box), _dist_to_box(p.pts[-1], box)
            near, far = (p.pts[0], p.pts[-1]) if da <= db else (p.pts[-1], p.pts[0])
            dn, df = min(da, db), max(da, db)
            if dn > 0.8 * h or df < 2 * h:
                continue
            if len(p.pts) == 2 and _angle_diff(_seg_angle(p), t.angle) < 8 and _point_seg_dist(far, *box[:2]) < h:
                continue                              # gạch chân chữ, không chỉ vào đâu
            if best is None or dn < best[0]:
                verts = list(p.pts) if p.pts[-1] == near else list(reversed(p.pts))
                best = (dn, i, verts, far)
        if best is None:
            continue
        _, i, verts, far = best
        taken.add(i)
        parts, arrow = [prims[i]], "_NONE"
        for j in grid.near(far[0], far[1], 3.0):
            q = prims[j]
            if j in taken or j not in mark_ids:
                continue
            qb = q.bbox()
            qc = ((qb[0] + qb[2]) / 2, (qb[1] + qb[3]) / 2)
            if math.dist(qc, far) < max(qb[2] - qb[0], qb[3] - qb[1]) + 0.2:
                arrow = "_DOT" if len(q.pts) > 8 else ""
                parts.append(q)
                taken.add(j)
                break
        out.append(_Leader(t, verts, arrow, parts))
        t.used = True
        for q in parts:
            q.used = True
    return out


# --------------------------------------------------------------- ảnh, dấu
@dataclass
class _Image:
    path: Path
    pixels: tuple[int, int]
    insert: tuple[float, float]
    size: tuple[float, float]


def _images(pdf, page, tf: _Transform, assets_dir: Path) -> list[_Image]:
    out = []
    seen: dict[int, Path] = {}
    for n, info in enumerate(page.get_image_info(xrefs=True), 1):
        xref = info.get("xref") or 0
        if xref <= 0:
            continue
        r = info["bbox"]
        corners = [tf((r[0], r[1])), tf((r[2], r[1])), tf((r[2], r[3])), tf((r[0], r[3]))]
        xs, ys = [c[0] for c in corners], [c[1] for c in corners]
        if max(xs) - min(xs) < 0.5 or max(ys) - min(ys) < 0.5:
            continue
        if xref not in seen:
            pix = pymupdf.Pixmap(pdf, xref)
            smask = pdf.extract_image(xref).get("smask") or 0
            if smask:
                pix = pymupdf.Pixmap(pix, pymupdf.Pixmap(pdf, smask))
            elif pix.n - pix.alpha >= 4:
                pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
            assets_dir.mkdir(parents=True, exist_ok=True)
            p = assets_dir / f"anh-{len(seen) + 1:02d}.png"
            pix.save(str(p))
            seen[xref] = p
        p = seen[xref]
        w, h = info.get("width") or 1, info.get("height") or 1
        out.append(_Image(p, (int(w), int(h)), (min(xs), min(ys)), (max(xs) - min(xs), max(ys) - min(ys))))
    return out


# ------------------------------------------------------- hình và tỷ lệ 1:1
_SCALE_RE = re.compile(r"^\(?\s*(?:TL|TỶ LỆ|TY LE|SCALE)?\s*[:.]?\s*1\s*[:/]\s*(\d+(?:[.,]\d+)?)\s*\)?$", re.I)


@dataclass
class _View:
    bbox: list[float]
    members: list = field(default_factory=list)       # _Prim | _Text | _Dim | _Leader
    factor: float | None = None                       # giấy → thực (mm thực / mm giấy)
    source: str = ""


def _bbox_of(item) -> tuple[float, float, float, float]:
    if isinstance(item, _Prim):
        return item.bbox()
    if isinstance(item, _Text):
        xs, ys = zip(*_text_box(item))
        return min(xs), min(ys), max(xs), max(ys)
    if isinstance(item, _Dim):
        pts = [item.p1, item.p2, item.line_a, item.line_b] + _text_box(item.text)
        xs, ys = zip(*pts)
        g = 2 * item.text.height                     # khe đường gióng – hình (dimexo) không được tách dim khỏi hình
        return min(xs) - g, min(ys) - g, max(xs) + g, max(ys) + g
    pts = list(item.vertices) + _text_box(item.text)
    xs, ys = zip(*pts)
    return min(xs), min(ys), max(xs), max(ys)


def _views(items: list, gap: float) -> list[_View]:
    """Gom các đối tượng chạm/gần nhau (khe ≤ gap mm giấy) thành từng hình (union-find trên bbox)."""
    boxes = [_bbox_of(it) for it in items]
    parent = list(range(len(items)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    grid = _Grid(20.0)
    for i, b in enumerate(boxes):
        grid.add(i, (b[0] - gap, b[1] - gap, b[2] + gap, b[3] + gap))
    for i, b in enumerate(boxes):
        cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        r = max(b[2] - b[0], b[3] - b[1]) / 2 + gap
        for j in grid.near(cx, cy, r):
            if j <= i:
                continue
            c = boxes[j]
            if b[0] - gap <= c[2] and c[0] - gap <= b[2] and b[1] - gap <= c[3] and c[1] - gap <= b[3]:
                parent[find(i)] = find(j)
    groups: dict[int, _View] = {}
    for i, it in enumerate(items):
        v = groups.setdefault(find(i), _View(list(boxes[i])))
        v.members.append(it)
        b = boxes[i]
        v.bbox = [min(v.bbox[0], b[0]), min(v.bbox[1], b[1]), max(v.bbox[2], b[2]), max(v.bbox[3], b[3])]
    return list(groups.values())


def _assign_scales(views: list[_View], labels: list[tuple[_Text, float]], lfac: dict[int, float],
                   label_factor) -> None:
    for v in views:
        fs = [lfac[id(m)] for m in v.members if isinstance(m, _Dim) and id(m) in lfac]
        if fs:
            v.factor, v.source = statistics.median(fs), f"{len(fs)} kích thước"
    # nhãn "(1:60)" dưới tên hình: gán cho hình có nét gần nhất nằm ngay dưới nhãn (hoặc chứa nhãn)
    for t, n in labels:
        cx, cy = t.center
        best = None
        for v in views:
            if v.factor is not None or not any(isinstance(m, _Prim) for m in v.members):
                continue
            x0, y0, x1, y1 = v.bbox
            if not (x0 - 5 <= cx <= x1 + 5):
                continue
            dy = 0.0 if y0 <= cy <= y1 else (cy - y1 if cy > y1 else None)
            if dy is not None and dy < 25 and (best is None or dy < best[0]):
                best = (dy, v)
        if best:
            best[1].factor, best[1].source = label_factor(n), f"nhãn 1:{n:g}"


# ------------------------------------------------------------------ ghi ra
def _fmt(x: float) -> str:
    return f"{x:g}"


class _Writer:
    def __init__(self, doc, keep_color: bool):
        self.doc, self.keep_color = doc, keep_color
        self.by_layer: Counter = Counter()
        self.n = Counter()

    def prim(self, ctr, p: _Prim, T, f: float):
        pts = [T(q) for q in p.pts]
        attrs = {"layer": p.layer, **{k: v for k, v in p.style.items() if self.keep_color or k != "true_color"}}
        if f != 1.0 and "linetype" in attrs:
            attrs["ltscale"] = f
        if p.fill is not None and p.closed and len(pts) >= 3:
            hatch = ctr.add_hatch(dxfattribs={"layer": p.layer})
            fc = _true_color(p.fill) if self.keep_color else None
            if fc is not None:
                hatch.dxf.true_color = fc
            hatch.paths.add_polyline_path(pts, is_closed=True)
            self.n["hatches"] += 1
            self.by_layer[p.layer] += 1
            if not p.stroke:
                return
        if p.is_segment:
            ctr.add_line(pts[0], pts[1], dxfattribs=attrs)
            self.n["lines"] += 1
        else:
            ctr.add_lwpolyline(pts, close=p.closed, dxfattribs=attrs)
            self.n["polylines"] += 1
        self.by_layer[p.layer] += 1

    def text(self, ctr, t: _Text, T, f: float):
        ctr.add_text(t.text, dxfattribs={"layer": t.layer, "height": t.height * f, "insert": T(t.insert),
                                         "rotation": t.angle})
        self.n["text"] += 1
        self.by_layer[t.layer] += 1

    def dim(self, ctr, d: _Dim, T, f: float, lfac: float):
        """lfac: hệ số giấy → thực. Ở model 1:1 (f = lfac) DIMLFAC ≈ 1, kích thước hiện đúng số đo thật."""
        p1, p2, a, b = T(d.p1), T(d.p2), T(d.line_a), T(d.line_b)
        k = _nice(lfac / f)
        L = math.dist(a, b)
        dec = len(d.text.text.split(".")[-1]) if "." in d.text.text else 0
        override = {"dimlfac": k, "dimscale": f, "dimtxt": d.text.height, "dimdec": dec,
                    "dimtsz": d.text.height * 0.5 if d.ticks else 0.0}
        if not d.plain or abs(round(L * k, dec) - d.value) > 0.5 * 10 ** -dec:
            text = d.text.text
            self.n["dimension_text_override"] += 1
        else:
            text = "<>"
        ux, uy = b[0] - a[0], b[1] - a[1]
        Ln = math.hypot(ux, uy) or 1.0
        nx, ny = -uy / Ln, ux / Ln
        dist = (a[0] - p1[0]) * nx + (a[1] - p1[1]) * ny
        dim = ctr.add_aligned_dim(p1=p1, p2=p2, distance=dist, text=text, dimstyle="PDF_DIM",
                                  override=override, dxfattribs={"layer": "PDF_DIMENSIONS"})
        dim.set_location(T(d.text.center), leader=False, relative=False)
        dim.render()
        self.n["dimensions"] += 1
        self.by_layer["PDF_DIMENSIONS"] += 1

    def leader(self, ctr, ld: _Leader, T, f: float):
        from ezdxf.math import Vec2
        from ezdxf.render import mleader
        t = ld.text
        verts = [Vec2(T(v)) for v in ld.vertices]
        ml = ctr.add_multileader_mtext("Standard", dxfattribs={"layer": t.layer})
        ml.set_content(t.text, char_height=t.height * f, alignment=mleader.TextAlignment.left)
        ml.set_arrow_properties(name=ld.arrow, size=t.height * f * 0.8)
        ml.set_connection_properties(landing_gap=t.height * f * 0.2, dogleg_length=0.0)
        tx = T(t.insert)
        side = mleader.ConnectionSide.left if verts[-1].x <= tx[0] + t.width * f / 2 else \
            mleader.ConnectionSide.right
        ml.add_leader_line(side, verts)
        ml.build(insert=Vec2(tx[0], tx[1] + t.height * f), rotation=t.angle)
        self.n["leaders"] += 1
        self.by_layer[t.layer] += 1

    def image(self, ctr, im: _Image):
        if "PDF_IMAGES" not in self.doc.layers:
            self.doc.layers.add("PDF_IMAGES", color=7)
        idef = self.doc.add_image_def(filename=str(im.path), size_in_pixel=im.pixels)
        img = ctr.add_image(idef, insert=im.insert, size_in_units=im.size, dxfattribs={"layer": "PDF_IMAGES"})
        img.dxf.flags = 1 | 2 | 8                       # hiện ảnh, hiện khi không thẳng hàng, dùng nền trong suốt
        self.n["images"] += 1
        self.by_layer["PDF_IMAGES"] += 1

    def item(self, ctr, it, T, f, lfac_of):
        if isinstance(it, _Prim):
            self.prim(ctr, it, T, f)
        elif isinstance(it, _Text):
            self.text(ctr, it, T, f)
        elif isinstance(it, _Dim):
            self.dim(ctr, it, T, f, lfac_of(it))
        elif isinstance(it, _Leader):
            self.leader(ctr, it, T, f)


def _dimstyle(doc, dims: list[_Dim], main: float) -> None:
    if "PDF_DIM" in doc.dimstyles or not dims:
        return
    h = statistics.median(d.text.height for d in dims)
    ds = doc.dimstyles.new("PDF_DIM")
    ds.dxf.dimtxt = h
    ds.dxf.dimasz = h * 0.8
    ds.dxf.dimexe = h * 0.5
    ds.dxf.dimexo = h * 0.3
    ds.dxf.dimgap = h * 0.25
    ds.dxf.dimtad = 1
    ds.dxf.dimtih = 0
    ds.dxf.dimtoh = 0
    ds.dxf.dimdec = 0
    ds.dxf.dimlfac = _nice(main)


# ------------------------------------------------------------------ chính
def convert(source: Path, target: Path, *, dimensions: bool = True, keep_color: bool = True,
            leaders: bool = True, images: bool = True, real_scale: bool = False,
            assets_dir: Path | None = None, layout: str = "A1-SEMANTIC") -> dict:
    """real_scale=True: model space vẽ 1:1 theo kích thước thật, layout ``layout`` khổ A1 chứa khung tên, ảnh,
    ghi chú và một viewport đúng tỷ lệ cho mỗi hình. False: mọi thứ ở model space theo toạ độ giấy A1."""
    pdf = pymupdf.open(str(source))
    if len(pdf) != 1:
        raise ValueError(f"Expected one PDF page, got {len(pdf)}")
    page = pdf[0]
    tf = _Transform(float(page.mediabox.width), float(page.mediabox.height), int(page.rotation) % 360)

    doc = ezdxf.new("R2018", setup=True)
    doc.units = ezdxf.units.MM
    doc.header["$INSUNITS"] = 4
    doc.header["$MEASUREMENT"] = 1
    doc.header["$LWDISPLAY"] = 1
    for name, color in LAYER_COLORS.items():
        if name not in doc.layers:
            doc.layers.add(name, color=color)
    msp = doc.modelspace()

    prims: list[_Prim] = []
    linetypes: dict = {}
    source_layer_map = {}
    path_items = 0
    for drawing in page.get_drawings():
        layer = _drawing_layer(drawing, tf)
        source_name = (drawing.get("layer") or "").strip()
        if source_name:
            source_layer_map[source_name] = layer
        path_items += len(drawing["items"])
        prims.extend(_primitives(drawing, tf, layer, linetypes, doc))
    texts = _texts(page, tf)

    dims = _find_dims(prims, texts) if dimensions else []
    for d in dims:
        d.text.used = True
        for p in d.parts:
            p.used = True
    lfac = _scale_clusters(dims)
    main = Counter(round(v, 6) for v in lfac.values()).most_common(1)[0][0] if lfac else 1.0
    _dimstyle(doc, dims, main)
    lds = _find_leaders(prims, texts) if leaders else []
    imgs = _images(pdf, page, tf, assets_dir or target.parent / f"{target.stem}_anh") if images else []

    w = _Writer(doc, keep_color)
    ident = (lambda q: (q[0], q[1]))
    lfac_of = (lambda d: lfac.get(id(d), main))
    items = [p for p in prims if not p.used] + [t for t in texts if not t.used] + dims + lds
    scale_info: list[dict] = []
    paper_layout = None

    if not real_scale:
        for it in items:
            w.item(msp, it, ident, 1.0, lfac_of)
        for im in imgs:
            w.image(msp, im)
    else:
        sheet_area = PAPER_W * PAPER_H

        def is_sheet(it) -> bool:
            if isinstance(it, (_Prim, _Text)) and it.layer in ("PDF_FRAME", "PDF_TITLE"):
                return True
            if isinstance(it, _Prim):
                b = it.bbox()
                return (b[2] - b[0]) * (b[3] - b[1]) > 0.25 * sheet_area     # khung bản vẽ
            return False

        sheet = [it for it in items if is_sheet(it)]
        rest = [it for it in items if not is_sheet(it)]
        views = _views(rest, gap=VIEW_GAP)
        labels = []
        for t in texts:
            m = _SCALE_RE.match(t.text.strip())
            if m:
                labels.append((t, float(m.group(1).replace(",", "."))))
        pt_mm = 25.4 / 72
        _assign_scales(views, labels, lfac, lambda n: n * pt_mm / tf.s)
        # nhóm hình cùng tỷ lệ (±1%): chung một phép biến đổi để vị trí tương đối giữa các cụm không đổi
        groups: list[tuple[float, list[_View]]] = []
        for v in sorted((v for v in views if v.factor), key=lambda v: v.factor):
            if groups and v.factor <= groups[-1][0] * 1.01:
                groups[-1][1].append(v)
            else:
                groups.append((v.factor, [v]))
        cursor = 0.0
        transforms: dict[int, tuple] = {}
        for f0, vs in groups:
            f = _nice(statistics.median(v.factor for v in vs))
            x0 = min(v.bbox[0] for v in vs)
            y0 = min(v.bbox[1] for v in vs)
            x1 = max(v.bbox[2] for v in vs)
            ox, oy = cursor - x0 * f, -y0 * f
            for v in vs:
                transforms[id(v)] = (f, ox, oy)
            cursor += (x1 - x0) * f * 1.15
        paper = doc.layouts.new(layout)
        paper.page_setup(size=(PAPER_W, PAPER_H), margins=(0, 0, 0, 0), units="mm", scale=1)
        for it in sheet:
            w.item(paper, it, ident, 1.0, lfac_of)
        for im in imgs:
            w.image(paper, im)
        for v in views:
            if id(v) not in transforms:                 # ghi chú, tên hình, bảng: để ở giấy như PDF
                for it in v.members:
                    w.item(paper, it, ident, 1.0, lfac_of)
                continue
            f, ox, oy = transforms[id(v)]
            T = (lambda q, f=f, ox=ox, oy=oy: (q[0] * f + ox, q[1] * f + oy))
            for it in v.members:
                w.item(msp, it, T, f, lfac_of)
            x0, y0, x1, y1 = v.bbox
            m = 1.0
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            paper.add_viewport(center=(cx, cy), size=(x1 - x0 + 2 * m, y1 - y0 + 2 * m),
                               view_center_point=T((cx, cy)), view_height=(y1 - y0 + 2 * m) * f)
            scale_info.append({"bbox_giay": [round(c, 1) for c in v.bbox], "ty_le": f"1:{_fmt(round(f / (pt_mm / tf.s), 2))}",
                               "he_so": f, "nguon": v.source, "doi_tuong": len(v.members)})
        paper_layout = {"layout": layout, "viewports": len(scale_info), "paper_mm": [PAPER_W, PAPER_H]}

    warnings = []
    n_img = len(page.get_images(full=True))
    if n_img and path_items == 0:
        warnings.append(f"PDF chỉ có {n_img} ảnh quét/raster, không có nét vector hay chữ: không dựng được hình "
                        "học. Cần bản PDF xuất trực tiếp từ CAD (Plot to PDF), không phải bản scan/chụp.")
    if real_scale and not scale_info:
        warnings.append("Không xác định được tỷ lệ hình nào (không có kích thước dựng được, không thấy nhãn 1:N): "
                        "toàn bộ để ở layout theo toạ độ giấy.")

    target.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(str(target))
    return {
        "warnings": warnings,
        "lines": w.n["lines"],
        "polylines": w.n["polylines"],
        "curves": w.n["polylines"],   # tên cũ, giữ cho client đang đọc trường này
        "hatches": w.n["hatches"],
        "text": w.n["text"],
        "dimensions": w.n["dimensions"],
        "dimension_text_override": w.n["dimension_text_override"],
        "dimension_lfac": _nice(main) if dims else None,
        "leaders": w.n["leaders"],
        "images": w.n["images"],
        "image_files": sorted({str(im.path) for im in imgs}),
        "real_scale": real_scale,
        "views": scale_info,
        "paper_layout": paper_layout,
        "pdf_path_items": path_items,
        "entities": len(msp),
        "layers": dict(sorted(w.by_layer.items())),
        "source_layer_map": dict(sorted(source_layer_map.items())),
        "linetypes": sorted(linetypes.values()),
    }

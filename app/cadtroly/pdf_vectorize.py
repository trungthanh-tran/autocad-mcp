"""PDF-to-DXF conversion used directly by the MCP ``pdf_vectorize`` tool."""

from __future__ import annotations

import math
import re
from collections import Counter
from pathlib import Path

import ezdxf
import pymupdf

PAPER_W = 841.0
PAPER_H = 594.0


def _display_xy(point, page_width, page_height, rotation):
    x, y = float(point.x), float(point.y)
    if rotation == 90:
        return page_height - y, x
    if rotation == 180:
        return page_width - x, page_height - y
    if rotation == 270:
        return y, page_width - x
    return x, y


def _xy(point, page_width, page_height, rotation):
    dx, dy = _display_xy(point, page_width, page_height, rotation)
    display_width, display_height = page_height, page_width
    return (
        dx * PAPER_W / display_width,
        (display_height - dy) * PAPER_H / display_height,
    )


def _screen_rect(rect, page_width, page_height, rotation):
    points = [
        pymupdf.Point(rect.x0, rect.y0),
        pymupdf.Point(rect.x1, rect.y0),
        pymupdf.Point(rect.x1, rect.y1),
        pymupdf.Point(rect.x0, rect.y1),
    ]
    coords = [_display_xy(p, page_width, page_height, rotation) for p in points]
    xs, ys = zip(*coords)
    return min(xs), min(ys), max(xs), max(ys)


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


def _text_layer(text, bbox, size, page_width, page_height, rotation):
    x0, y0, x1, y1 = _screen_rect(pymupdf.Rect(*bbox), page_width, page_height, rotation)
    nx, ny = (x0 + x1) / (2 * page_height), (y0 + y1) / (2 * page_width)
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


def _drawing_layer(drawing, page_width, page_height, rotation):
    source_layer = (drawing.get("layer") or "").strip().upper()
    if source_layer in _SOURCE_TO_GROUP:
        return _SOURCE_TO_GROUP[source_layer]
    x0, y0, x1, y1 = _screen_rect(drawing["rect"], page_width, page_height, rotation)
    width, height = x1 - x0, y1 - y0
    area = width * height
    nx, ny = (x0 + x1) / (2 * page_height), (y0 + y1) / (2 * page_width)
    if drawing.get("fill") is not None:
        return "PDF_HATCH"
    if nx < 0.025 or nx > 0.975 or ny < 0.025 or ny > 0.975:
        return "PDF_FRAME"
    if area < 180 or max(width, height) < 22:
        return "PDF_SYMBOLS"
    if len(drawing.get("items", ())) >= 20 and max(width, height) < 80:
        return "PDF_SYMBOLS"
    return "PDF_GEOMETRY"


def convert(source: Path, target: Path) -> dict:
    pdf = pymupdf.open(str(source))
    if len(pdf) != 1:
        raise ValueError(f"Expected one PDF page, got {len(pdf)}")
    page = pdf[0]
    pw, ph = float(page.mediabox.width), float(page.mediabox.height)
    rotation = int(page.rotation) % 360

    doc = ezdxf.new("R2018", setup=True)
    doc.units = ezdxf.units.MM
    doc.header["$INSUNITS"] = 4
    doc.header["$MEASUREMENT"] = 1
    layer_colors = {
        "PDF_FRAME": 8,
        "PDF_GEOMETRY": 7,
        "PDF_HATCH": 9,
        "PDF_COLUMNS": 30,
        "PDF_WALLS": 31,
        "PDF_DOORS": 32,
        "PDF_WINDOWS": 33,
        "PDF_FURNITURE": 34,
        "PDF_SANITARY": 35,
        "PDF_STRUCTURE": 36,
        "PDF_FINISHES": 37,
        "PDF_CEILING": 38,
        "PDF_LIGHTING": 39,
        "PDF_SECTIONS_ELEVATIONS": 40,
        "PDF_SITE": 41,
        "PDF_REFERENCE": 42,
        "PDF_DETAIL_LINES": 43,
        "PDF_SYMBOLS": 4,
        "PDF_DIMENSIONS": 3,
        "PDF_TEXT": 2,
        "PDF_NOTES": 6,
        "PDF_TITLE": 1,
    }
    for name, color in layer_colors.items():
        if name not in doc.layers:
            doc.layers.add(name, color=color)
    msp = doc.modelspace()

    lines = 0
    curves = 0
    by_layer = Counter()
    source_layer_map = {}
    for drawing in page.get_drawings():
        layer = _drawing_layer(drawing, pw, ph, rotation)
        source_name = (drawing.get("layer") or "").strip()
        if source_name:
            source_layer_map[source_name] = layer
        for item in drawing["items"]:
            kind = item[0]
            if kind == "l":
                a, b = _xy(item[1], pw, ph, rotation), _xy(item[2], pw, ph, rotation)
                if math.dist(a, b) > 1e-5:
                    msp.add_line(a, b, dxfattribs={"layer": layer})
                    lines += 1
                    by_layer[layer] += 1
            elif kind == "c":
                p0, p1, p2, p3 = item[1:5]
                points = []
                for i in range(9):
                    t = i / 8.0
                    u = 1.0 - t
                    q = pymupdf.Point(
                        u**3 * p0.x + 3 * u**2 * t * p1.x + 3 * u * t**2 * p2.x + t**3 * p3.x,
                        u**3 * p0.y + 3 * u**2 * t * p1.y + 3 * u * t**2 * p2.y + t**3 * p3.y,
                    )
                    points.append(_xy(q, pw, ph, rotation))
                msp.add_lwpolyline(points, dxfattribs={"layer": layer})
                curves += 1
                by_layer[layer] += 1
            elif kind == "qu":
                quad = item[1]
                points = [_xy(p, pw, ph, rotation) for p in (quad.ul, quad.ur, quad.lr, quad.ll)]
                if len(points) >= 2:
                    msp.add_lwpolyline(points, dxfattribs={"layer": layer})
                    curves += 1
                    by_layer[layer] += 1

    text_count = 0
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span.get("text", "").strip()
                if not text:
                    continue
                x0, y0, _x1, _y1 = span["bbox"]
                x, y = _xy(pymupdf.Point(x0, y0), pw, ph, rotation)
                size = float(span.get("size", 8.0))
                height = max(1.0, size * PAPER_W / ph)
                layer = _text_layer(text, span["bbox"], size, pw, ph, rotation)
                msp.add_text(text, dxfattribs={"layer": layer, "height": height, "insert": (x, y)})
                text_count += 1
                by_layer[layer] += 1

    target.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(str(target))
    return {
        "lines": lines,
        "curves": curves,
        "text": text_count,
        "entities": len(msp),
        "layers": dict(sorted(by_layer.items())),
        "source_layer_map": dict(sorted(source_layer_map.items())),
    }

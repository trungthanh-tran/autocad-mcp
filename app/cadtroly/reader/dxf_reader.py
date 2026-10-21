"""Đọc DXF/DWG bằng ezdxf thành Drawing.

DWG: ezdxf chỉ đọc DWG khi có ODA File Converter (ezdxf.addons.odafc). Không có thì
báo lỗi rõ, không đoán.

Nguyên tắc đo: không shoelace trên đỉnh thô của polyline có bulge (mất diện tích cạnh
cong). Dùng ezdxf.path để flatten với dung sai nhỏ rồi mới tính, và ghi accuracy.
"""
from __future__ import annotations

import math
from pathlib import Path

import ezdxf
from ezdxf import path as ezpath
from ezdxf.math import Vec2

from .model import Drawing, Entity

INSUNITS = {0: "unknown", 1: "inch", 4: "mm", 5: "cm", 6: "m"}
FLATTEN_TOL = 0.01  # đơn vị bản vẽ; với mm là 0.01 mm


def _shoelace(pts: list[Vec2]) -> float:
    n = len(pts)
    if n < 3:
        return 0.0
    s = 0.0
    for i in range(n):
        x1, y1 = pts[i].x, pts[i].y
        x2, y2 = pts[(i + 1) % n].x, pts[(i + 1) % n].y
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0


def _bbox(pts) -> tuple[float, float, float, float] | None:
    xs = [p.x for p in pts]
    ys = [p.y for p in pts]
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


def _path_metrics(p: ezpath.Path) -> tuple[float, float, list[Vec2]]:
    pts = [Vec2(v) for v in p.flattening(FLATTEN_TOL)]
    length = sum((pts[i + 1] - pts[i]).magnitude for i in range(len(pts) - 1))
    area = _shoelace(pts) if len(pts) >= 3 else 0.0
    return length, area, pts


def _entity(e, space: str) -> Entity | None:
    t = e.dxftype()
    h = e.dxf.handle
    layer = e.dxf.layer
    try:
        if t in ("LWPOLYLINE", "POLYLINE"):
            p = ezpath.make_path(e)
            length, area, pts = _path_metrics(p)
            closed = bool(e.closed) if hasattr(e, "closed") else bool(e.is_closed)
            has_bulge = t == "LWPOLYLINE" and any(abs(v[4]) > 1e-9 for v in e.get_points())
            if closed:
                # đóng vòng: cộng cạnh cuối
                if pts and (pts[0] - pts[-1]).magnitude > 1e-9:
                    length += (pts[0] - pts[-1]).magnitude
            return Entity(h, t, layer, space, point=(pts[0].x, pts[0].y) if pts else None,
                          bbox=_bbox(pts), length=length, area=area if closed else None,
                          closed=closed, accuracy="flattened" if has_bulge else "exact")
        if t == "LINE":
            a, b = Vec2(e.dxf.start), Vec2(e.dxf.end)
            return Entity(h, t, layer, space, point=(a.x, a.y), bbox=_bbox([a, b]),
                          length=(b - a).magnitude)
        if t == "CIRCLE":
            c, r = Vec2(e.dxf.center), e.dxf.radius
            return Entity(h, t, layer, space, point=(c.x, c.y),
                          bbox=(c.x - r, c.y - r, c.x + r, c.y + r),
                          length=2 * math.pi * r, area=math.pi * r * r, closed=True)
        if t == "ARC":
            c, r = Vec2(e.dxf.center), e.dxf.radius
            ang = (e.dxf.end_angle - e.dxf.start_angle) % 360
            return Entity(h, t, layer, space, point=(c.x, c.y),
                          bbox=(c.x - r, c.y - r, c.x + r, c.y + r),
                          length=math.radians(ang) * r)
        if t == "HATCH":
            total = 0.0
            areas = []
            pts_all: list[Vec2] = []
            for p in ezpath.from_hatch(e):
                _, a, pts = _path_metrics(p)
                areas.append(a)
                pts_all.extend(pts)
            if areas:
                areas.sort(reverse=True)
                total = areas[0] - sum(areas[1:])   # ngoài trừ đảo (xấp xỉ, đủ cho bóc KL)
            return Entity(h, t, layer, space, point=(pts_all[0].x, pts_all[0].y) if pts_all else None,
                          bbox=_bbox(pts_all), area=max(total, 0.0), closed=True,
                          accuracy="flattened", extra={"pattern": e.dxf.pattern_name})
        if t == "INSERT":
            ins = Vec2(e.dxf.insert)
            attribs = {}
            for a in e.attribs:
                attribs[a.dxf.tag] = a.dxf.text
            return Entity(h, t, layer, space, point=(ins.x, ins.y), block_name=e.dxf.name,
                          attribs=attribs, extra={"rotation": e.dxf.rotation,
                                                  "scale": (e.dxf.xscale, e.dxf.yscale)})
        if t == "TEXT":
            ins = Vec2(e.dxf.insert)
            return Entity(h, t, layer, space, point=(ins.x, ins.y), text=e.dxf.text,
                          extra={"height": e.dxf.height, "style": e.dxf.style})
        if t == "MTEXT":
            ins = Vec2(e.dxf.insert)
            return Entity(h, t, layer, space, point=(ins.x, ins.y), text=e.plain_text(),
                          extra={"height": e.dxf.char_height, "style": e.dxf.style})
        if t.startswith("DIMENSION") or t == "DIMENSION":
            m = None
            try:
                m = e.get_measurement()
                if not isinstance(m, (int, float)):
                    m = None
            except Exception:
                m = None
            pt = Vec2(e.dxf.defpoint)
            override = e.dxf.text if e.dxf.hasattr("text") else ""
            return Entity(h, "DIMENSION", layer, space, point=(pt.x, pt.y), measurement=m,
                          text=override or None, extra={"override": bool(override and override != "<>"),
                                                         "dimstyle": e.dxf.dimstyle})
        if t == "ATTDEF":
            return None
    except Exception as ex:  # không để một entity hỏng làm sập cả bản vẽ
        return Entity(h, t, layer, space, accuracy="approx", extra={"error": str(ex)})
    return Entity(h, t, layer, space)


def read_dxf(path: str | Path, *, include_layouts: bool = False) -> Drawing:
    path = Path(path)
    if path.suffix.lower() == ".dwg":
        from ezdxf.addons import odafc
        if not odafc.is_installed():
            raise RuntimeError("Đọc DWG cần ODA File Converter (ezdxf.addons.odafc). "
                               "Cài ODA hoặc xuất DXF từ AutoCAD.")
        doc = odafc.readfile(str(path))
    else:
        doc = ezdxf.readfile(str(path))
    insunits = int(doc.header.get("$INSUNITS", 0))
    units = INSUNITS.get(insunits, "unknown")
    layers = sorted(l.dxf.name for l in doc.layers)
    ents: list[Entity] = []
    block_defs: dict[str, int] = {}
    spaces = [("model", doc.modelspace())]
    if include_layouts:
        spaces += [(lay.name, lay) for lay in doc.layouts if lay.name.lower() != "model"]
    for name, sp in spaces:
        for e in sp:
            ent = _entity(e, name)
            if ent is None:
                continue
            ents.append(ent)
            if ent.block_name:
                block_defs[ent.block_name] = block_defs.get(ent.block_name, 0) + 1
    return Drawing(path=str(path), units=units, insunits=insunits, layers=layers,
                   entities=ents, block_defs=block_defs,
                   layouts=[l.name for l in doc.layouts],
                   header={"$ACADVER": doc.header.get("$ACADVER", "")})

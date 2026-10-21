"""Sinh bản vẽ DXF mẫu để test và demo khi chưa có bản vẽ thật.

Mặt bằng tầng 3 giả định: 3 phòng, hành lang, tường 220/100, cửa đi block có attribute,
cửa sổ block tên lạ (WD_2), text H=3300, một ít line rời trên layer 0, hatch lát nền,
dimension bị override, text nhỏ trên layer 0 để test kiểm tra chuẩn.
"""
from __future__ import annotations

from pathlib import Path

import ezdxf
from ezdxf.enums import TextEntityAlignment


def make_sample(out: str | Path) -> Path:
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = ezdxf.new("R2018", setup=True)
    doc.header["$INSUNITS"] = 4  # mm
    for name, color in [("TUONG220", 1), ("tuong-100", 2), ("A-DOOR", 3), ("A-GLAZ", 4),
                        ("SAN-LAT", 5), ("DIM", 6), ("TEXT", 7), ("COT", 1)]:
        doc.layers.add(name, color=color)
    msp = doc.modelspace()

    # block cửa đi có attribute
    blk = doc.blocks.new("CUA-D1")
    blk.add_lwpolyline([(0, 0), (900, 0), (900, 50), (0, 50)], close=True)
    blk.add_attdef("KICHTHUOC", (0, 100), dxfattribs={"height": 100}).dxf.text = "900x2200"
    blk.add_attdef("MA", (0, 250), dxfattribs={"height": 100}).dxf.text = "D1"
    # block cửa sổ tên lạ, không attribute
    wd = doc.blocks.new("WD_2")
    wd.add_lwpolyline([(0, 0), (1200, 0), (1200, 50), (0, 50)], close=True)
    # block cột
    col = doc.blocks.new("COT-C1")
    col.add_lwpolyline([(0, 0), (300, 0), (300, 300), (0, 300)], close=True)

    # tường ngoài 220 (polyline hở theo tim tường) + tường ngăn 100
    msp.add_lwpolyline([(0, 0), (12000, 0), (12000, 8000), (0, 8000), (0, 0)], dxfattribs={"layer": "TUONG220"})
    msp.add_lwpolyline([(4000, 0), (4000, 5000)], dxfattribs={"layer": "tuong-100"})
    msp.add_lwpolyline([(8000, 0), (8000, 5000)], dxfattribs={"layer": "tuong-100"})
    msp.add_lwpolyline([(0, 5000), (12000, 5000)], dxfattribs={"layer": "tuong-100"})
    # cột 4 góc
    for p in [(0, 0), (12000, 0), (12000, 8000), (0, 8000)]:
        msp.add_blockref("COT-C1", p, dxfattribs={"layer": "COT"})
    # cửa đi 3 phòng, cửa sổ 6
    for x in (2000, 6000, 10000):
        ref = msp.add_blockref("CUA-D1", (x, 5000), dxfattribs={"layer": "A-DOOR"})
        ref.add_auto_attribs({"KICHTHUOC": "900x2200", "MA": "D1"})
    for x in (1000, 2500, 5000, 6500, 9000, 10500):
        msp.add_blockref("WD_2", (x, 0), dxfattribs={"layer": "A-GLAZ"})
    # hatch lát nền 3 phòng
    for x0 in (0, 4000, 8000):
        h = msp.add_hatch(color=5, dxfattribs={"layer": "SAN-LAT"})
        h.paths.add_polyline_path([(x0 + 110, 110), (x0 + 3890, 110), (x0 + 3890, 4950), (x0 + 110, 4950)], is_closed=True)
        h.set_pattern_fill("ANSI31", scale=50)
    # text phòng, chiều cao tầng
    for i, x0 in enumerate((0, 4000, 8000), 1):
        msp.add_text(f"P.30{i}", dxfattribs={"layer": "TEXT", "height": 250}).set_placement((x0 + 500, 4500))
    msp.add_text("HÀNH LANG", dxfattribs={"layer": "TEXT", "height": 250}).set_placement((500, 7000))
    msp.add_text("H=3300", dxfattribs={"layer": "TEXT", "height": 250}).set_placement((500, 8500))
    # text nhỏ sai layer (để test check)
    for i in range(12):
        msp.add_text(f"ghi chu {i}", dxfattribs={"layer": "0", "height": 180}).set_placement((500 + i * 900, -800))
    # line rời layer 0 (không bóc được)
    for i in range(10):
        msp.add_line((13000, i * 300), (16000, i * 300), dxfattribs={"layer": "0"})
    # dimension: 1 bình thường, 1 override
    msp.add_linear_dim(base=(0, -1500), p1=(0, 0), p2=(4000, 0), dxfattribs={"layer": "DIM"}).render()
    d = msp.add_linear_dim(base=(0, -2000), p1=(4000, 0), p2=(8000, 0), dxfattribs={"layer": "DIM"})
    d.dimension.dxf.text = "4500"
    d.render()
    doc.saveas(out)
    return out


if __name__ == "__main__":
    import sys
    p = make_sample(sys.argv[1] if len(sys.argv) > 1 else "samples/mat-bang-tang-3.dxf")
    print(p)

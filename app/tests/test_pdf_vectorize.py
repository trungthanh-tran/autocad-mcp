"""PDF → DXF giữ nét liền, chữ đúng chân/góc, dim thành DIMENSION thật."""
import math

import ezdxf
import pymupdf
import pytest

from cadtroly.pdf_vectorize import convert

# Trang A3 ngang (pt). Bản vẽ "tỷ lệ": 1 pt trên PDF = 10 mm thực → số ghi = chiều dài pt × 10
W, H = 1190.55, 841.89


def _path(page, pts, *, close=False, width=0.5, dashes=None, fill=None, color=(0, 0, 0)):
    sh = page.new_shape()
    for a, b in zip(pts, pts[1:]):
        sh.draw_line(a, b)
    if close:
        sh.draw_line(pts[-1], pts[0])
    sh.finish(width=width, color=color, fill=fill, dashes=dashes, closePath=close)
    sh.commit()


def _seg(page, a, b, width=0.25):
    _path(page, [a, b], width=width)


def make_pdf(path):
    doc = pymupdf.open()
    page = doc.new_page(width=W, height=H)
    # khung: một path 4 đoạn nối nhau
    _path(page, [(100, 100), (700, 100), (700, 500), (100, 500)], close=True, width=1.0)
    # hình chữ nhật dạng 're'
    sh = page.new_shape()
    sh.draw_rect(pymupdf.Rect(150, 150, 300, 250))
    sh.finish(width=0.35)
    sh.commit()
    # đường tim nét đứt
    _path(page, [(100, 300), (700, 300)], dashes="[6 2 1 2] 0", width=0.18, color=(1, 0, 0))

    # dim ngang 600 pt → "6000": đường gióng + vạch chặn xiên, chữ phía trên đường dim
    y = 560
    _seg(page, (100, 505), (100, y + 6))
    _seg(page, (700, 505), (700, y + 6))
    _seg(page, (100, y), (700, y))
    for x in (100, 700):
        _seg(page, (x - 3, y + 3), (x + 3, y - 3), width=0.5)
    page.insert_text((388, y - 3), "6000", fontsize=9)

    # dim đứng 400 pt → "4000", chữ xoay 90°
    x = 760
    _seg(page, (705, 100), (x + 6, 100))
    _seg(page, (705, 500), (x + 6, 500))
    _seg(page, (x, 100), (x, 500))
    for yy in (100, 500):
        _seg(page, (x - 3, yy + 3), (x + 3, yy - 3), width=0.5)
    page.insert_text((x - 3, 320), "4000", fontsize=9, rotate=90)

    # dim mũi tên đặc, đường dim bị cắt quanh chữ, chữ dạng 25x250=6250 (625 pt)
    y2 = 620
    _seg(page, (100, y2), (380, y2))
    _seg(page, (445, y2), (725, y2))
    for xa, d in ((100, 1), (725, -1)):
        _path(page, [(xa, y2), (xa + 6 * d, y2 - 1.5), (xa + 6 * d, y2 + 1.5)], close=True, fill=(0, 0, 0))
    _seg(page, (100, 600), (100, y2 + 5))
    _seg(page, (725, 600), (725, y2 + 5))
    page.insert_text((385, y2 + 3), "25x250=6250", fontsize=7)

    # nhãn thép tách 2 span
    page.insert_text((150, 400), "S2-D25", fontsize=8)
    page.insert_text((178, 400), "-250", fontsize=8)
    doc.save(str(path))


@pytest.fixture
def converted(tmp_path):
    pdf = tmp_path / "ban-ve.pdf"
    make_pdf(pdf)
    out = tmp_path / "ban-ve.dxf"
    stats = convert(pdf, out)
    return stats, ezdxf.readfile(str(out))


def test_paths_stay_whole(converted):
    stats, doc = converted
    msp = doc.modelspace()
    closed = [e for e in msp.query("LWPOLYLINE") if e.closed and len(e) == 4]
    assert len(closed) >= 2                                   # khung 4 đoạn + 're' đều thành polyline kín
    frame = max(closed, key=lambda e: abs(e[0][0] - e[2][0]))
    xs = sorted({round(p[0], 3) for p in frame.get_points("xy")})
    ys = sorted({round(p[1], 3) for p in frame.get_points("xy")})
    s = min(841.0 / W, 594.0 / H)
    assert math.isclose(xs[1] - xs[0], 600 * s, rel_tol=1e-6)
    assert math.isclose(ys[1] - ys[0], 400 * s, rel_tol=1e-6)  # cùng hệ số hai trục
    assert frame.dxf.lineweight == 35                          # 1 pt ≈ 0.35 mm × hệ số → lineweight gần nhất
    dashed = [e for e in msp if e.dxf.hasattr("linetype") and e.dxf.linetype.startswith("PDF_DASH")]
    assert dashed and dashed[0].dxf.hasattr("true_color")
    assert stats["linetypes"]


def test_dimensions_rebuilt(converted):
    stats, doc = converted
    dims = list(doc.modelspace().query("DIMENSION"))
    assert stats["dimensions"] == 3 and len(dims) == 3
    by_text = {}
    for d in dims:
        m = d.get_measurement()
        lfac = d.dimstyle_override().get("dimlfac", 1.0) if hasattr(d, "dimstyle_override") else 1.0
        by_text[d.dxf.text] = (m, lfac)
    # hai dim số thuần: hiển thị theo đo thật × DIMLFAC, không override chữ
    assert "<>" in by_text
    for d in dims:
        ov = d.override()
        if d.dxf.text == "<>":
            assert round(d.get_measurement() * ov.get("dimlfac")) in (6000, 4000)
    assert "25x250=6250" in by_text                           # chữ đặc biệt giữ nguyên làm override
    # các mảnh dim (chữ số) không còn nằm rời
    texts = [e.dxf.text for e in doc.modelspace().query("TEXT")]
    assert not ({"6000", "4000", "25x250=6250"} & set(texts))


def test_text_baseline_rotation_and_join(converted):
    _, doc = converted
    texts = {e.dxf.text: e for e in doc.modelspace().query("TEXT")}
    assert "S2-D25-250" in texts or "S2-D25 -250" in texts     # hai span gộp một dòng
    t = texts.get("S2-D25-250") or texts["S2-D25 -250"]
    s = min(841.0 / W, 594.0 / H)
    assert math.isclose(t.dxf.insert.y, (H - 400) * s, abs_tol=0.3)   # chân chữ, không phải mép trên


def test_rotated_text_kept(tmp_path):
    pdf = tmp_path / "r.pdf"
    doc = pymupdf.open()
    page = doc.new_page(width=W, height=H)
    page.insert_text((500, 400), "GHI CHU DUNG", fontsize=10, rotate=90)
    doc.save(str(pdf))
    convert(pdf, tmp_path / "r.dxf")
    t = next(iter(ezdxf.readfile(str(tmp_path / "r.dxf")).modelspace().query("TEXT")))
    assert round(t.dxf.rotation) % 360 == 90

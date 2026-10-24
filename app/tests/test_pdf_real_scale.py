"""PDF → DXF 1:1: mỗi hình thành model space đúng kích thước thật + viewport đúng tỷ lệ; nhãn thép → MLEADER;
dấu/chữ ký → IMAGE."""
import math

import ezdxf
import pymupdf
import pytest

from cadtroly.pdf_vectorize import convert

W, H = 1190.55, 841.89          # A3 ngang, pt
PT_MM = 25.4 / 72


def _path(page, pts, *, close=False, width=0.35, fill=None):
    sh = page.new_shape()
    for a, b in zip(pts, pts[1:]):
        sh.draw_line(a, b)
    if close:
        sh.draw_line(pts[-1], pts[0])
    sh.finish(width=width, color=(0, 0, 0), fill=fill, closePath=close)
    sh.commit()


def _seg(page, a, b, width=0.25):
    _path(page, [a, b], width=width)


def _stamp_png(path):
    from PIL import Image, ImageDraw
    im = Image.new("RGBA", (60, 40), (0, 0, 0, 0))     # nền trong suốt
    ImageDraw.Draw(im).rectangle((5, 5, 54, 34), outline=(220, 30, 30, 255), width=2)
    im.save(str(path))


def make_sheet(path, stamp):
    doc = pymupdf.open()
    page = doc.new_page(width=W, height=H)
    # khung bản vẽ + khung tên (lớp giấy)
    _path(page, [(20, 20), (W - 20, 20), (W - 20, H - 20), (20, H - 20)], close=True, width=0.7)
    _path(page, [(20, H - 80), (W - 20, H - 80)], width=0.5)
    page.insert_text((40, H - 50), "CONG TY CO PHAN BOT", fontsize=10)

    # Hình 1 "LƯỚI L1 (1:60)": chữ nhật 360 × 240 pt → thực 7620 × 5080 mm, có dim 7620 bên dưới
    page.insert_text((200, 90), "LUOI L1", fontsize=12)
    page.insert_text((205, 104), "(1:60)", fontsize=7)
    _path(page, [(100, 120), (460, 120), (460, 360), (100, 360)], close=True)
    _path(page, [(100, 240), (460, 240)], width=0.5)          # một thanh thép giữa
    y = 400
    _seg(page, (100, 365), (100, y + 6))
    _seg(page, (460, 365), (460, y + 6))
    _seg(page, (100, y), (460, y))
    for x in (100, 460):
        _seg(page, (x - 3, y + 3), (x + 3, y - 3), width=0.5)
    page.insert_text((265, y - 3), "7620", fontsize=8)
    # nhãn thép + đường dẫn xiên tới thanh, chấm đặc ở đầu
    page.insert_text((300, 200), "S4-D14", fontsize=7)
    _path(page, [(298, 198), (280, 240)], width=0.25)
    sh = page.new_shape()
    sh.draw_circle((280, 240), 1.2)
    sh.finish(color=(0, 0, 0), fill=(0, 0, 0))
    sh.commit()

    # Hình 2 "(1:100)" không có dim: chữ nhật 200 × 100 pt → thực 7055.6 × 3527.8 mm
    page.insert_text((700, 90), "SO HOA", fontsize=12)
    page.insert_text((705, 104), "(1:100)", fontsize=7)
    _path(page, [(650, 130), (850, 130), (850, 230), (650, 230)], close=True)
    _path(page, [(660, 140), (840, 220)], width=0.5)

    # dấu thẩm tra (ảnh có alpha) trong hình 2
    page.insert_image(pymupdf.Rect(700, 150, 790, 210), filename=str(stamp))
    doc.save(str(path))


@pytest.fixture
def sheet(tmp_path):
    stamp = tmp_path / "dau.png"
    _stamp_png(stamp)
    pdf = tmp_path / "hcds.pdf"
    make_sheet(pdf, stamp)
    out = tmp_path / "hcds.dxf"
    stats = convert(pdf, out, real_scale=True, assets_dir=tmp_path / "anh")
    return stats, ezdxf.readfile(str(out)), tmp_path


def _rect_sizes(space):
    out = []
    for e in space.query("LWPOLYLINE"):
        if e.closed and len(e) == 4:
            xs = [p[0] for p in e.get_points("xy")]
            ys = [p[1] for p in e.get_points("xy")]
            out.append((max(xs) - min(xs), max(ys) - min(ys)))
    return out


def test_views_real_size(sheet):
    stats, doc, _ = sheet
    assert {v["ty_le"] for v in stats["views"]} >= {"1:60", "1:100"}
    msp = doc.modelspace()
    sizes = _rect_sizes(msp)
    assert any(math.isclose(w, 7620, rel_tol=1e-4) and math.isclose(h, 5080, rel_tol=1e-4) for w, h in sizes)
    assert any(math.isclose(w, 200 * PT_MM * 100, rel_tol=1e-3) for w, _ in sizes)
    dim = next(iter(msp.query("DIMENSION")))
    ov = dim.override()
    assert math.isclose(dim.get_measurement(), 7620, rel_tol=1e-4) and math.isclose(ov.get("dimlfac"), 1.0)
    assert dim.dxf.text == "<>"


def test_layout_has_sheet_and_viewports(sheet):
    stats, doc, _ = sheet
    paper = doc.layouts.get("A1-SEMANTIC")
    vps = [v for v in paper.query("VIEWPORT") if v.dxf.id != 1]
    assert len(vps) == stats["paper_layout"]["viewports"] >= 2
    # viewport hình 1 hiển thị đúng tỷ lệ: chiều cao mô hình / chiều cao viewport = hệ số 1:60 trên khổ A1
    texts = [t.dxf.text for t in paper.query("TEXT")]
    assert "CONG TY CO PHAN BOT" in texts and "LUOI L1" in texts and "(1:60)" in texts
    assert any(math.isclose(w, (W - 40) * min(841 / W, 594 / H), rel_tol=1e-4) for w, _ in _rect_sizes(paper))
    assert not list(doc.modelspace().query("IMAGE"))


def test_leader_and_image(sheet):
    stats, doc, tmp = sheet
    assert stats["leaders"] == 1
    ml = next(iter(doc.modelspace().query("MULTILEADER")))
    assert "S4-D14" in ml.context.mtext.default_content
    assert "S4-D14" not in [t.dxf.text for t in doc.query("TEXT")]
    img = next(iter(doc.layouts.get("A1-SEMANTIC").query("IMAGE")))
    assert img.dxf.flags & 8                               # nền trong suốt
    png = tmp / "anh" / "anh-01.png"
    assert stats["image_files"] and png.is_file()
    from PIL import Image
    assert Image.open(png).convert("RGBA").getpixel((0, 0))[3] == 0     # giữ nền trong suốt (SMask)


def test_paper_mode_unchanged(tmp_path):
    stamp = tmp_path / "dau.png"
    _stamp_png(stamp)
    make_sheet(tmp_path / "a.pdf", stamp)
    stats = convert(tmp_path / "a.pdf", tmp_path / "a.dxf")
    assert stats["real_scale"] is False and stats["paper_layout"] is None and stats["dimensions"] == 1

"""Bộ tiêu chuẩn tcvn-cot-thep: số liệu khớp văn bản đã đối chiếu, mỗi quy tắc bắt đúng trường hợp."""
import json
from pathlib import Path

import ezdxf

from cadtroly.check.engine import check_drawing, load_ruleset
from cadtroly.reader import read_dxf
from cadtroly.takeoff.civil import MASS_TOLERANCE_PCT, NOMINAL_KG_PER_M, rebar

STD = Path(__file__).parent.parent / "kho-mac-dinh" / "tieu-chuan" / "tcvn-cot-thep.rules.json"

# Chép tay từ Bảng 2 TCVN 1651-2:2018 (đọc ảnh trang văn bản 2026-10-24) — đối chiếu độc lập với code và JSON
BANG_2 = {6: (0.222, 8), 8: (0.395, 8), 10: (0.617, 6), 12: (0.888, 6), 14: (1.21, 5), 16: (1.58, 5),
          18: (2.00, 5), 20: (2.47, 5), 22: (2.98, 5), 25: (3.85, 4), 28: (4.83, 4), 32: (6.31, 4),
          36: (7.99, 4), 40: (9.86, 4), 50: (15.42, 4)}


def test_mass_table_matches_standard_and_json():
    data = json.loads(STD.read_text(encoding="utf-8"))
    kg = {int(k): v for k, v in data["bang_khoi_luong"]["kg_m"].items()}
    tol = {int(k): v for k, v in data["bang_khoi_luong"]["sai_lech_phan_tram"].items()}
    assert kg == NOMINAL_KG_PER_M == {d: v[0] for d, v in BANG_2.items()}
    assert tol == MASS_TOLERANCE_PCT == {d: v[1] for d, v in BANG_2.items()}
    # mỗi giá trị bảng khớp công thức của chính Bảng 2 khi làm tròn
    for d, (v, _) in BANG_2.items():
        assert abs(7.85e-3 * 0.7854 * d * d - v) / v < 0.005


def test_no_unverified_numbers():
    data = json.loads(STD.read_text(encoding="utf-8"))
    loai = {r["loai"] for r in data["rules"]}
    assert not loai & {"rebar_clear_spacing_min", "rebar_spacing_max"}      # TCVN 5574 chưa đối chiếu → không có
    assert set(data["rules"][1]["gia_tri"]) == {"CB240-T", "CB300-T", "CB400-T", "CB300-V", "CB400-V", "CB500-V", "CB600-V"}
    for r in data["rules"]:
        assert r["dieu"], r["id"]                                           # mọi quy tắc ghi nguồn
        if r["id"].startswith("H-"):
            assert "không phải điều khoản" in r["dieu"] or "thể hiện hồ sơ" in r["dieu"].lower()


def _dxf(path, notes):
    doc = ezdxf.new()
    msp = doc.modelspace()
    for i, s in enumerate(notes):
        msp.add_text(s, dxfattribs={"height": 250}).set_placement((0, -i * 600))
    doc.saveas(path)
    return path


def test_rules_fire(tmp_path):
    p = _dxf(tmp_path / "t.dxf", ["N1 12Ø16 L=5200 CB400-V", "F1-D25-125", "N9 Ø15 a200",
                                  "N7 4Ø20 L=3000 CB450-V", "S1 6Ø12 L=2000 CB600-V", "N5 8Ø25"])
    fs = {f.rule_id: f for f in check_drawing(read_dxf(p), load_ruleset(STD))}
    assert "Ø15" in fs["T-01"].gia_tri and fs["T-01"].muc == "canh_bao"
    assert fs["T-02"].muc == "loi" and "N7" in fs["T-02"].mo_ta
    assert fs["T-03"].muc == "xac_nhan" and "S1" in fs["T-03"].mo_ta
    assert "N5" in fs["H-01"].mo_ta and "F1" not in fs["H-01"].mo_ta       # F1 có bước → đủ
    assert "H-02" not in fs                                                 # đã có mác CB…
    assert "H-03" in fs                                                     # chưa ghi lớp bảo vệ
    items = {i.so_hieu: i for i in rebar(read_dxf(p))}
    assert items["F1"].buoc_mm == 125 and items["F1"].d_mm == 25
    assert items["N1"].mac == "CB400-V" and items["N1"].tong_kg == round(12 * 5.2 * 1.58, 2)


def test_listed_in_kho(kho_dir):
    from cadtroly.config import Config
    from cadtroly.kho.store import Kho
    rows = Kho(Config(kho=kho_dir)).standard_list("structural")
    assert any(r["id"] == "tcvn-cot-thep" and r["cho_duyet"] == 0 for r in rows)

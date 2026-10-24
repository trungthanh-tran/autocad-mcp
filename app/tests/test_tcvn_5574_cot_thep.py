"""Bộ tcvn-5574-2018-cot-thep: chỉ chứa nội dung có trích nguyên văn; mức 'loi' chỉ khi đúng mọi trường hợp."""
import json
from pathlib import Path

import ezdxf

from cadtroly.check.engine import _COVER, _ascii, check_drawing, load_ruleset
from cadtroly.reader import read_dxf

STD = Path(__file__).parent.parent / "kho-mac-dinh" / "tieu-chuan" / "tcvn-5574-2018-cot-thep.rules.json"


def _dxf(path, notes):
    doc = ezdxf.new()
    msp = doc.modelspace()
    for i, s in enumerate(notes):
        msp.add_text(s, dxfattribs={"height": 250}).set_placement((0, -i * 600))
    doc.saveas(path)
    return path


def test_every_rule_quotes_source():
    data = json.loads(STD.read_text(encoding="utf-8"))
    for r in data["rules"]:
        assert r["dieu"].startswith("TCVN 5574:2018 mục 10.3"), r["id"]
        assert len(r.get("trich", "")) > 40, r["id"]              # có nguyên văn
    # chỉ C-01 là 'loi' (giới hạn "trong mọi trường hợp"); giới hạn có điều kiện không được là 'loi'
    assert [r["id"] for r in data["rules"] if r["muc"] == "loi"] == ["C-01"]


def test_cover_parse():
    for s, v in [("Lớp bê tông bảo vệ cốt thép chịu lực 25mm", "25"), ("abv=15", "15"),
                 ("LỚP BT BẢO VỆ: 40", "40"), ("Chiều dày lớp bảo vệ 30", "30")]:
        assert _COVER.search(_ascii(s)).group(1) == v


def test_rules_fire(tmp_path):
    p = _dxf(tmp_path / "a.dxf", ["N1 12Ø25 L=5200", "Lớp bê tông bảo vệ 15", "F1-D16-30", "S2-D12-450", "S3-D12-250"])
    fs = {f.rule_id: f for f in check_drawing(read_dxf(p), load_ruleset(STD))}
    # 15 < Ø25 → vi phạm "không nhỏ hơn đường kính thanh" (đúng mọi trường hợp)
    assert fs["C-01"].muc == "loi" and "Ø25" in fs["C-01"].mo_ta
    assert fs["C-02"].muc == "xac_nhan"                          # < 20: đối chiếu Bảng 19, không tự kết luận
    assert "F1" in fs["K-01"].mo_ta and fs["K-01"].muc == "canh_bao"   # 30 − 16 = 14 < max(16, 25)
    assert "S2" in fs["K-02"].mo_ta and "S3" not in fs["K-02"].mo_ta  # 450 > 400
    assert "S3" in fs["K-03"].mo_ta and fs["K-03"].muc == "xac_nhan"  # 250 > 200, phụ thuộc h


def test_no_cover_note_no_conclusion(tmp_path):
    p = _dxf(tmp_path / "b.dxf", ["N1 12Ø16 L=5200"])
    fs = {f.rule_id for f in check_drawing(read_dxf(p), load_ruleset(STD))}
    assert not fs & {"C-01", "C-02"}                             # không ghi lớp bảo vệ → không suy ra vi phạm

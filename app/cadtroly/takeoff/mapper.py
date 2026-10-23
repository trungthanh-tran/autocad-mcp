"""Bước 2 của luồng A: gom đối tượng theo layer/block và đề xuất ánh xạ về công tác.

Mỗi nhóm có tin cậy:
  A  khớp quy tắc đơn vị hoặc đọc được từ attribute block
  B  đoán từ từ khoá trong tên (heuristic) hoặc AI đề xuất → cần người xác nhận
  C  không xác định (layer 0, tên lạ, line rời) → khoanh để người đếm
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from ..kho.rules import MappingRule, RuleStore, heuristic
from ..reader.model import Drawing, Entity

GEOM = {"LWPOLYLINE", "POLYLINE", "LINE", "ARC", "CIRCLE", "HATCH"}
SKIP_LAYERS = {"defpoints"}


@dataclass
class Group:
    kind: str                       # layer | block
    name: str
    entities: list[Entity]
    cong_tac: str = ""
    don_vi: str = ""
    cach_tinh: str = "count"
    tham_so: dict = field(default_factory=dict)
    tin_cay: str = "C"
    ly_do: str = ""
    ma_dinh_muc: str = ""
    rule: MappingRule | None = None
    skip: bool = False

    @property
    def count(self) -> int:
        return len(self.entities)

    def describe(self) -> str:
        kinds: dict[str, int] = {}
        for e in self.entities:
            kinds[e.dxftype] = kinds.get(e.dxftype, 0) + 1
        return ", ".join(f"{v} {k.lower()}" for k, v in sorted(kinds.items(), key=lambda x: -x[1]))

    def to_dict(self) -> dict:
        return {
            "kind": self.kind, "name": self.name, "count": self.count, "mo_ta": self.describe(),
            "cong_tac": self.cong_tac, "don_vi": self.don_vi, "cach_tinh": self.cach_tinh,
            "tham_so": self.tham_so, "tin_cay": self.tin_cay, "ly_do": self.ly_do, "skip": self.skip,
            "ma_dinh_muc": self.ma_dinh_muc,
            "handles": [e.handle for e in self.entities[:50]],
        }


def _block_size_from_attribs(ents: list[Entity]) -> str | None:
    """Đọc kích thước từ attribute: WxH, 900x2200, KICHTHUOC..."""
    for e in ents[:5]:
        for k, v in e.attribs.items():
            if re.search(r"\d{3,4}\s*[xX×]\s*\d{3,4}", v or ""):
                return v.strip()
    return None


def propose_mapping(dwg: Drawing, rules: RuleStore) -> list[Group]:
    groups: list[Group] = []

    # 1. block theo tên
    for name, ents in dwg.by_block().items():
        g = Group("block", name, ents)
        rule = rules.find("block", name)
        size = _block_size_from_attribs(ents)
        if rule:
            g.rule, g.cong_tac, g.don_vi, g.cach_tinh, g.tham_so = rule, rule.cong_tac, rule.don_vi, rule.cach_tinh, dict(rule.tham_so)
            g.tin_cay, g.ly_do, g.ma_dinh_muc = "A", f"quy tắc {rule.nguon}", rule.ma_dinh_muc
        else:
            h = heuristic("block", name)
            if h and h[2] == "skip":
                g.skip, g.tin_cay, g.ly_do = True, "A", "không phải công tác (ghi chú/khung)"
            elif h:
                g.cong_tac, g.don_vi, g.cach_tinh, g.tham_so = h
                g.tin_cay, g.ly_do = "B", "đoán từ tên block"
            else:
                # tên block lạ: thử layer chứa INSERT (A-GLAZ, CUA...) làm gợi ý
                layers = {e.layer for e in ents}
                hint = None
                for ly in layers:
                    hl = heuristic("layer", ly)
                    if hl and hl[2] != "skip":
                        hint = (hl, ly)
                        break
                if hint:
                    (ct, dv, _, _), ly = hint
                    g.cong_tac, g.don_vi, g.cach_tinh = ct, dv if dv in ("bộ", "cái") else "bộ", "count"
                    g.tin_cay, g.ly_do = "B", f"tên block lạ, đoán từ layer {ly}"
                else:
                    g.cong_tac, g.don_vi, g.cach_tinh = "", "bộ", "count"
                    g.tin_cay, g.ly_do = "B", "tên block lạ, cần chọn công tác"
        if size:
            g.cong_tac = (g.cong_tac + f" {size}").strip()
            if g.tin_cay == "B" and g.cong_tac.strip() != size:
                g.ly_do += " · kích thước từ attribute"
        groups.append(g)

    # 2. hình học theo layer (bỏ INSERT đã tính, bỏ text/dim)
    for layer, ents in dwg.by_layer().items():
        geo = [e for e in ents if e.dxftype in GEOM]
        if not geo:
            continue
        g = Group("layer", layer, geo)
        if layer.lower() in SKIP_LAYERS:
            g.skip, g.tin_cay, g.ly_do = True, "A", "layer hệ thống"
            groups.append(g)
            continue
        rule = rules.find("layer", layer)
        if rule:
            g.rule, g.cong_tac, g.don_vi, g.cach_tinh, g.tham_so = rule, rule.cong_tac, rule.don_vi, rule.cach_tinh, dict(rule.tham_so)
            g.tin_cay, g.ly_do, g.ma_dinh_muc = "A", f"quy tắc {rule.nguon}", rule.ma_dinh_muc
        elif layer == "0":
            g.tin_cay, g.ly_do = "C", "layer 0: không xác định, khoanh để người đếm"
        else:
            h = heuristic("layer", layer)
            if h and h[2] == "skip":
                g.skip, g.tin_cay, g.ly_do = True, "A", "không phải công tác (ghi chú/kích thước)"
            elif h:
                g.cong_tac, g.don_vi, g.cach_tinh, g.tham_so = h
                g.tin_cay, g.ly_do = "B", "đoán từ tên layer"
            else:
                g.tin_cay, g.ly_do = "C", "tên layer lạ"
        # line rời không khép kín trên layer tường: hạ xuống B/C
        if g.cach_tinh in ("area", "volume_by_height") and all(e.dxftype == "LINE" for e in geo):
            if g.tin_cay == "A":
                g.tin_cay, g.ly_do = "B", g.ly_do + " · toàn line rời, không có polyline kín"
        groups.append(g)

    order = {"A": 0, "B": 1, "C": 2}
    groups.sort(key=lambda g: (g.skip, order[g.tin_cay], -g.count))
    return groups


def apply_decision(g: Group, rules: RuleStore, *, cong_tac: str, don_vi: str, cach_tinh: str,
                   tham_so: dict | None = None, ma_dinh_muc: str = "", save: bool = True) -> Group:
    """Kỹ sư xác nhận một nhóm. save=True → lưu thành quy tắc đơn vị."""
    g.cong_tac, g.don_vi, g.cach_tinh, g.ma_dinh_muc = cong_tac, don_vi, cach_tinh, ma_dinh_muc.strip()
    g.tham_so = dict(tham_so or {})
    g.tin_cay, g.ly_do, g.skip = "A", "kỹ sư xác nhận", cach_tinh == "skip"
    if save:
        g.rule = rules.upsert(MappingRule(kind=g.kind, pattern=g.name, cong_tac=cong_tac, don_vi=don_vi,
                                          cach_tinh=cach_tinh, tham_so=g.tham_so,
                                          ma_dinh_muc=g.ma_dinh_muc, nguon="don-vi"))
    return g

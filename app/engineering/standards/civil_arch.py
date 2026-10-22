"""Reference catalogue and layer kits for building, road and bridge CAD.

The references are project starting points, not a substitute for the approved
project standards register.  Editions and local/client requirements must be
verified before issuing a drawing.
"""

from __future__ import annotations

from typing import Any

LayerRow = tuple[str, int, str, float, str]


BUILDING_LAYERS: list[LayerRow] = [
    ("0", 7, "Continuous", 0.25, "default"),
    ("A-WALL-E-N", 7, "Continuous", 0.50, "walls"),
    ("A-WALL-H-N", 8, "Continuous", 0.13, "wall hatch"),
    ("A-DOOR-E-N", 2, "Continuous", 0.25, "doors"),
    ("A-WIND-E-N", 4, "Continuous", 0.25, "windows"),
    ("A-STAIR-E-N", 3, "Continuous", 0.35, "stairs"),
    ("A-FURN-E-N", 6, "Continuous", 0.18, "furniture"),
    ("A-SANR-E-N", 5, "Continuous", 0.18, "sanitary fixtures"),
    ("A-GRID-E-N", 1, "CENTER", 0.18, "grids"),
    ("A-ROOM-T-N", 7, "Continuous", 0.18, "room labels"),
    ("A-DIMEN-T-N", 2, "Continuous", 0.18, "dimensions"),
    ("A-SYMB-T-N", 6, "Continuous", 0.18, "symbols and tags"),
    ("A-OVHD-E-N", 8, "HIDDEN", 0.18, "overhead elements"),
    ("A-CONST-E-N", 250, "Continuous", 0.05, "construction"),
]

ROAD_LAYERS: list[LayerRow] = [
    ("0", 7, "Continuous", 0.25, "default"),
    ("C-ROAD-EXIST", 8, "Continuous", 0.18, "existing survey"),
    ("C-ROAD-ALIGN", 1, "CENTER", 0.25, "alignment and stationing"),
    ("C-ROAD-EDGE", 7, "Continuous", 0.50, "pavement edges"),
    ("C-ROAD-SURF", 2, "Continuous", 0.35, "surface and pavement"),
    ("C-ROAD-DRAIN", 4, "Continuous", 0.25, "drainage"),
    ("C-ROAD-SIGN", 5, "Continuous", 0.18, "signage and markings"),
    ("C-ROAD-HATCH", 8, "Continuous", 0.13, "materials and earthwork hatch"),
    ("C-ROAD-DIM", 2, "Continuous", 0.18, "dimensions"),
    ("C-ROAD-TEXT", 7, "Continuous", 0.25, "notes"),
    ("C-ROAD-TEMP", 250, "Continuous", 0.05, "construction"),
]

BRIDGE_LAYERS: list[LayerRow] = [
    ("0", 7, "Continuous", 0.25, "default"),
    ("S-BRIDGE-DECK", 7, "Continuous", 0.50, "deck and slab"),
    ("S-BRIDGE-GIRDER", 1, "Continuous", 0.50, "girders and beams"),
    ("S-BRIDGE-PIER", 3, "Continuous", 0.50, "piers and columns"),
    ("S-BRIDGE-ABUT", 4, "Continuous", 0.50, "abutments and wing walls"),
    ("S-BRIDGE-REBAR", 2, "Continuous", 0.25, "reinforcement"),
    ("S-BRIDGE-BEARING", 5, "Continuous", 0.25, "bearings and joints"),
    ("S-BRIDGE-HIDDEN", 3, "HIDDEN", 0.18, "hidden elements"),
    ("S-BRIDGE-CENTER", 1, "CENTER", 0.18, "centerlines"),
    ("S-BRIDGE-HATCH", 8, "Continuous", 0.13, "material hatch"),
    ("S-BRIDGE-DIM", 2, "Continuous", 0.18, "dimensions"),
    ("S-BRIDGE-TEXT", 7, "Continuous", 0.25, "notes"),
    ("S-BRIDGE-TEMP", 250, "Continuous", 0.05, "construction"),
]

REFERENCE_SETS: dict[str, dict[str, Any]] = {
    "building": {
        "name": "Nhà / kiến trúc",
        "layer_set": "building",
        "roles": {"dim": "A-DIMEN-T-N", "construction": "A-CONST-E-N"},
        "references": [
            {"code": "ISO 128", "purpose": "quy tắc trình bày nét vẽ"},
            {"code": "ISO 129-1", "purpose": "ghi kích thước"},
            {"code": "ISO 13567-1", "purpose": "tổ chức và đặt tên layer CAD"},
            {"code": "ISO 5457", "purpose": "khổ giấy và bố trí bản vẽ"},
            {"code": "TCVN 5574:2018", "purpose": "kết cấu bê tông và bê tông cốt thép"},
            {"code": "TCVN 2737:2023", "purpose": "tải trọng và tác động"},
        ],
    },
    "road": {
        "name": "Đường",
        "layer_set": "road",
        "roles": {"dim": "C-ROAD-DIM", "construction": "C-ROAD-TEMP"},
        "references": [
            {"code": "TCVN 4054:2005", "purpose": "đường ô tô - yêu cầu thiết kế"},
            {"code": "TCVN 5729:2012", "purpose": "đường ô tô cao tốc - yêu cầu thiết kế"},
            {"code": "TCVN 9436:2012", "purpose": "nền đường ô tô - thi công và nghiệm thu"},
            {"code": "ISO 128", "purpose": "quy tắc trình bày nét vẽ"},
            {"code": "ISO 13567-1", "purpose": "tổ chức và đặt tên layer CAD"},
        ],
    },
    "bridge": {
        "name": "Cầu",
        "layer_set": "bridge",
        "roles": {"dim": "S-BRIDGE-DIM", "construction": "S-BRIDGE-TEMP"},
        "references": [
            {"code": "TCVN 11823:2017", "purpose": "thiết kế cầu đường bộ"},
            {"code": "TCVN 4054:2005", "purpose": "yếu tố hình học đường dẫn và tuyến"},
            {"code": "ISO 128", "purpose": "quy tắc trình bày nét vẽ"},
            {"code": "ISO 13567-1", "purpose": "tổ chức và đặt tên layer CAD"},
        ],
    },
}

REFERENCE_ALIASES = {
    "nha": "building", "building": "building", "architecture": "building", "arch": "building",
    "duong": "road", "road": "road", "roads": "road",
    "cau": "bridge", "bridge": "bridge", "bridges": "bridge",
}


def resolve_reference_set(name: str) -> tuple[str, dict[str, Any]]:
    key = REFERENCE_ALIASES.get(str(name).strip().lower(), str(name).strip().lower())
    if key not in REFERENCE_SETS:
        raise ValueError(f"unknown discipline {name!r}; use building, road or bridge")
    return key, REFERENCE_SETS[key]


__all__ = ["BUILDING_LAYERS", "ROAD_LAYERS", "BRIDGE_LAYERS", "REFERENCE_SETS", "resolve_reference_set"]

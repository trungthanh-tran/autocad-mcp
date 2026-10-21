"""Mô hình số liệu bản vẽ, độc lập với engine (ezdxf hay COM).

Mỗi Entity giữ đủ để truy vết: handle, layer, loại, toạ độ. Số đo (dài, diện tích)
kèm cờ độ chính xác để bảng khối lượng ghi rõ số nào là đo thật, số nào xấp xỉ.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Entity:
    handle: str
    dxftype: str
    layer: str
    space: str = "model"                 # model | <layout name>
    point: tuple[float, float] | None = None      # điểm đại diện (insert / start / center)
    bbox: tuple[float, float, float, float] | None = None
    length: float | None = None          # chiều dài (polyline, line, arc, circle chu vi)
    area: float | None = None            # diện tích vùng kín (polyline closed, hatch, circle)
    closed: bool = False
    block_name: str | None = None        # INSERT
    attribs: dict[str, str] = field(default_factory=dict)
    text: str | None = None              # TEXT / MTEXT / ATTRIB / DIMENSION text
    measurement: float | None = None     # DIMENSION
    accuracy: str = "exact"              # exact | flattened | approx
    extra: dict[str, Any] = field(default_factory=dict)

    def as_trace(self) -> str:
        p = f"({self.point[0]:.0f}, {self.point[1]:.0f})" if self.point else ""
        return f"{self.dxftype} {self.handle} @{self.layer} {p}".strip()


@dataclass
class Drawing:
    path: str
    units: str                           # mm | m | cm | inch | unknown
    insunits: int
    layers: list[str]
    entities: list[Entity]
    block_defs: dict[str, int] = field(default_factory=dict)   # tên block -> số INSERT
    layouts: list[str] = field(default_factory=list)
    header: dict[str, Any] = field(default_factory=dict)

    # ---- tiện ích truy vấn ----
    def by_layer(self) -> dict[str, list[Entity]]:
        out: dict[str, list[Entity]] = {}
        for e in self.entities:
            out.setdefault(e.layer, []).append(e)
        return out

    def by_block(self) -> dict[str, list[Entity]]:
        out: dict[str, list[Entity]] = {}
        for e in self.entities:
            if e.block_name:
                out.setdefault(e.block_name, []).append(e)
        return out

    def texts(self) -> list[Entity]:
        return [e for e in self.entities if e.text]

    def find(self, handle: str) -> Entity | None:
        for e in self.entities:
            if e.handle == handle:
                return e
        return None

    def summary(self) -> dict[str, Any]:
        kinds: dict[str, int] = {}
        for e in self.entities:
            kinds[e.dxftype] = kinds.get(e.dxftype, 0) + 1
        return {
            "path": self.path,
            "units": self.units,
            "entities": len(self.entities),
            "layers": len(self.layers),
            "blocks": len(self.block_defs),
            "inserts": sum(self.block_defs.values()),
            "kinds": kinds,
            "layouts": self.layouts,
        }

    # hệ số đổi về mét
    @property
    def to_m(self) -> float:
        return {"mm": 0.001, "cm": 0.01, "m": 1.0, "inch": 0.0254}.get(self.units, 1.0)

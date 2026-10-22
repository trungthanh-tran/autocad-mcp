"""Conservative structural-drawing and CAD-optimization checks.

These checks validate drawing organization and visible geometry only. They do
not certify strength, stability, fire resistance or code compliance without
loads, materials, restraints and an approved calculation model.
"""

from __future__ import annotations

from collections import defaultdict
from math import hypot


def _kind(entity) -> str:
    return str(getattr(entity, "type", "")).upper()


def _layer(entity) -> str:
    return str(getattr(entity, "layer", "") or "")


def _geometry_signature(entity):
    props = getattr(entity, "properties", {}) or {}
    kind = _kind(entity)
    def point(value):
        if not isinstance(value, (list, tuple)) or len(value) < 2:
            return None
        return tuple(round(float(v), 3) for v in value[:3])
    if kind == "LINE":
        a, b = point(props.get("start")), point(props.get("end"))
        if a is not None and b is not None:
            return kind, tuple(sorted((a, b)))
    if kind in {"CIRCLE", "ARC"}:
        center = point(props.get("center"))
        radius = props.get("radius")
        if center is not None and radius is not None:
            return kind, center, round(float(radius), 3)
    if kind in {"LWPOLYLINE", "POLYLINE"}:
        points = props.get("points") or []
        if points:
            return kind, tuple(point(item) for item in points), bool(props.get("closed"))
    return None


def check_structural_drawing(layers, entities, *, discipline: str = "building") -> dict:
    """Return findings and non-destructive optimization suggestions."""
    discipline = discipline.strip().lower()
    if discipline not in {"building", "road", "bridge"}:
        raise ValueError("discipline must be building, road or bridge")
    layer_names = {str(getattr(layer, "name", "")) for layer in layers}
    upper_layers = {name: name.upper() for name in layer_names}
    structural_layers = {
        name for name, upper in upper_layers.items()
        if upper.startswith(("KC-", "S-", "CAU-"))
        or any(token in upper for token in ("COT", "COL", "DAM", "BEAM", "GIRD", "TRU", "PIER", "ABUT", "MONG", "FOUND"))
    }
    findings: list[dict] = []
    suggestions: list[dict] = []

    if not structural_layers:
        findings.append({
            "severity": "warning",
            "code": "structural_layers_not_detected",
            "message": "Không nhận diện được layer kết cấu; cần chọn chuẩn layer hoặc xác nhận quy ước dự án.",
            "detail": {"discipline": discipline},
        })

    used = defaultdict(int)
    for entity in entities:
        used[_layer(entity)] += 1
    for name in sorted(structural_layers - set(used)):
        findings.append({
            "severity": "warning",
            "code": "empty_structural_layer",
            "message": f"Layer kết cấu '{name}' đang rỗng.",
            "detail": {"layer": name},
        })

    seen = {}
    for entity in entities:
        props = getattr(entity, "properties", {}) or {}
        if _kind(entity) == "LINE" and _layer(entity) in structural_layers:
            start, end = props.get("start"), props.get("end")
            if isinstance(start, (list, tuple)) and isinstance(end, (list, tuple)) and len(start) >= 2 and len(end) >= 2:
                if hypot(float(end[0]) - float(start[0]), float(end[1]) - float(start[1])) < 0.001:
                    findings.append({
                        "severity": "error",
                        "code": "structural_zero_length",
                        "message": "Đối tượng kết cấu có chiều dài bằng 0.",
                        "detail": {"handle": getattr(entity, "handle", None), "layer": _layer(entity)},
                    })
        signature = _geometry_signature(entity)
        if signature is not None and _layer(entity) in structural_layers:
            key = (_layer(entity), signature)
            if key in seen:
                findings.append({
                    "severity": "warning",
                    "code": "structural_duplicate_geometry",
                    "message": "Hình học kết cấu trùng trên cùng layer.",
                    "detail": {"handles": [seen[key], getattr(entity, "handle", None)], "layer": _layer(entity)},
                })
            else:
                seen[key] = getattr(entity, "handle", None)

    for name in sorted(layer_names):
        upper = name.upper()
        if name in {"0", "DEFPOINTS"}:
            continue
        if any(token in upper for token in ("COT", "COL", "DAM", "BEAM", "GIRD", "TRU", "PIER", "ABUT", "MONG", "FOUND")) and not (
            upper.startswith(("KC-", "S-", "CAU-"))
        ):
            suggestions.append({
                "code": "structural_layer_naming",
                "message": f"Layer '{name}' có vẻ là kết cấu nhưng chưa theo tiền tố KC-/S-/CAU-.",
                "detail": {"layer": name},
            })

    suggestions.append({
        "code": "engineering_calculation_required",
        "message": "Cần đối chiếu tải trọng, vật liệu, liên kết, móng và hồ sơ tính toán được duyệt.",
        "detail": {"discipline": discipline},
    })
    errors = sum(1 for item in findings if item["severity"] == "error")
    warnings = sum(1 for item in findings if item["severity"] == "warning")
    return {
        "ok": errors == 0,
        "discipline": discipline,
        "summary": {"errors": errors, "warnings": warnings, "entities": len(entities), "structural_layers": len(structural_layers)},
        "findings": findings,
        "optimization_suggestions": suggestions,
        "limitation": "Không phải kiểm định hoặc chứng nhận an toàn kết cấu.",
    }

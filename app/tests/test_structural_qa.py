from types import SimpleNamespace

from engineering.structural_qa import check_structural_drawing


def _entity(handle, layer, start, end):
    return SimpleNamespace(
        handle=handle,
        type="LINE",
        layer=layer,
        properties={"start": start, "end": end},
    )


def test_structural_qa_reports_error_and_duplicate_warning():
    layers = [SimpleNamespace(name="KC-COT"), SimpleNamespace(name="KC-DAM")]
    entities = [
        _entity("A1", "KC-COT", [0, 0], [0, 0]),
        _entity("A2", "KC-DAM", [0, 0], [1000, 0]),
        _entity("A3", "KC-DAM", [0, 0], [1000, 0]),
    ]

    result = check_structural_drawing(layers, entities)

    assert result["ok"] is False
    codes = {finding["code"] for finding in result["findings"]}
    assert "structural_zero_length" in codes
    assert "structural_duplicate_geometry" in codes
    assert result["optimization_suggestions"]


def test_structural_qa_warns_when_layer_convention_is_unknown():
    result = check_structural_drawing(
        [SimpleNamespace(name="Columns")],
        [_entity("B1", "Columns", [0, 0], [100, 0])],
    )

    assert result["ok"] is True
    assert any(item["code"] == "structural_layer_naming" for item in result["optimization_suggestions"])

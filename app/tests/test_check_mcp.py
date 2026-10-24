import json
from pathlib import Path

import pytest

from cadtroly.check.engine import check_drawing, load_ruleset, summarize
from cadtroly.reader import read_dxf


def test_check_engine(sample_dxf, kho_dir):
    rs = load_ruleset(kho_dir / "quy-tac" / "chuan-cong-ty.rules.json")
    fs = check_drawing(read_dxf(sample_dxf), rs)
    ids = {f.rule_id: f for f in fs}
    assert "L-01" in ids and ids["L-01"].tu_sua_duoc and len(ids["L-01"].handles) == 22
    assert "L-02" in ids and len(ids["L-02"].handles) == 12
    assert ids["L-03"].muc == "canh_bao"
    assert "L-04" not in ids                      # layer DIM có
    assert ids["S-01"].muc == "xac_nhan"
    assert "L-99" not in ids                      # chưa duyệt → không chạy
    fs2 = check_drawing(read_dxf(sample_dxf), rs, only_approved=False)
    assert any(f.rule_id == "L-99" for f in fs2)
    assert summarize(fs)["loi"] == 2


def _data(r):
    return r.data if getattr(r, "data", None) is not None else json.loads(r.content[0].text)


@pytest.mark.asyncio
async def test_mcp_flow(sample_dxf, kho_dir):
    from fastmcp import Client
    from cadtroly.mcp.server import build_server
    mcp = build_server()
    P = str(sample_dxf)
    async with Client(mcp) as c:
        names = [t.name for t in await c.list_tools()]
        assert {"drawing_read", "takeoff_propose", "takeoff_decide", "takeoff_export", "check_run", "knowledge_status"} <= set(names)
        assert {"drawing_open", "drawing_info", "transaction_begin", "view_screenshot"} <= set(names)   # tool upstream cùng server (lean)
        st = _data(await c.call_tool("knowledge_status", {}))
        assert st["backend"] == "ezdxf"
        r = _data(await c.call_tool("takeoff_propose", {"path": P}))
        assert r["stats"]["A"] == 0
        r = _data(await c.call_tool("takeoff_decide", {"path": P, "kind": "block", "name": "WD_2",
                                                       "cong_tac": "Cửa sổ nhôm", "don_vi": "bộ", "cach_tinh": "count"}))
        assert r["ok"] and r["rules_total"] == 1
        r = _data(await c.call_tool("takeoff_export", {"path": P}))
        assert r["excel"] is None and {q["ma"] for q in r["can_hoi"]} == {"anh_xa", "chieu_cao"}   # còn đề xuất B
        r = _data(await c.call_tool("takeoff_export", {"path": P, "chap_nhan_B": True}))
        assert Path(r["excel"]).exists() and r["stats"]["A"] > 0
        r = _data(await c.call_tool("check_run", {"path": P, "ruleset": "chuan-cong-ty"}))
        assert r["summary"]["loi"] == 2
        r = _data(await c.call_tool("drawing_open", {"path": P}))
        assert r.get("ok") or r.get("name")
        r = _data(await c.call_tool("drawing_info", {}))
        assert "entity_count" in str(r)
        with pytest.raises(Exception):
            await c.call_tool("takeoff_decide", {"path": P, "kind": "block", "name": "KHONG-CO",
                                                 "cong_tac": "x", "don_vi": "x", "cach_tinh": "count"})
        r = _data(await c.call_tool("knowledge_rules_export", {}))
        assert r["rules"][0]["pattern"] == "WD_2"
    assert (kho_dir / "log").glob("*.log")

"""Bước duyệt thao tác phá huỷ: token, elicitation, tắt, và tool an toàn không bị chặn."""
import json

import pytest
from fastmcp import Client
from fastmcp.client.elicitation import ElicitResult

from cadtroly.mcp.approval import needs_approval


def _data(r):
    return r.structured_content if getattr(r, "structured_content", None) else json.loads(r.content[0].text)


def test_rules(tmp_path):
    f = tmp_path / "a.dxf"
    f.write_text("x")
    assert needs_approval("entity_delete", {"handle": "1A"})
    assert needs_approval("entity_create_line", {}) is None
    assert needs_approval("drawing_save", {}) == "ghi đè file đang mở"
    assert needs_approval("drawing_save", {"path": str(tmp_path / "moi.dxf")}) is None
    assert needs_approval("drawing_save_as", {"path": str(f)})
    assert needs_approval("text_find_replace", {"find": "a", "replace": "b", "dry_run": True}) is None
    assert needs_approval("xref_manage", {"action": "list"}) is None
    batch = {"steps": [{"tool": "entity_create_line", "args": {}}, {"tool": "entity_delete", "args": {"handle": "1"}}]}
    assert "bước 1" in needs_approval("cad_batch", batch)
    assert needs_approval("cad_batch", batch | {"dry_run": True}) is None
    assert needs_approval("cad_batch", {"steps": [{"tool": "entity_create_line", "args": {}}]}) is None


async def _line(c) -> str:
    await c.call_tool("drawing_new", {})
    r = _data(await c.call_tool("entity_create_line", {"x1": 0, "y1": 0, "x2": 10, "y2": 0}))
    return r.get("handle") or r["entity"]["handle"]


async def _count(c) -> int:
    info = _data(await c.call_tool("drawing_info", {}))
    return info.get("entity_count", info.get("entities", 0))


@pytest.mark.asyncio
async def test_token_flow(kho_dir, monkeypatch):
    monkeypatch.setenv("CADTROLY_APPROVAL", "token")
    from cadtroly.mcp.server import build_server
    async with Client(build_server()) as c:
        h = await _line(c)
        n0 = await _count(c)
        r = await c.call_tool("entity_delete", {"handle": h}, raise_on_error=False)
        assert r.is_error
        d = _data(r)
        assert d["kind"] == "approval_required" and d["arguments"] == {"handle": h}
        assert await _count(c) == n0                      # chưa xoá
        ok = await c.call_tool("approval_execute", {"token": d["token"]})
        assert not ok.is_error
        assert await _count(c) == n0 - 1
        again = await c.call_tool("approval_execute", {"token": d["token"]}, raise_on_error=False)
        assert again.is_error and _data(again)["kind"] == "approval_invalid"   # dùng một lần
    log = "".join(p.read_text(encoding="utf-8") for p in (kho_dir / "log").glob("*.log"))
    assert '"approval"' in log and "execute" in log


@pytest.mark.asyncio
@pytest.mark.parametrize("choice,deleted", [("dong_y", True), ("huy", False)])
async def test_elicitation(kho_dir, monkeypatch, choice, deleted):
    monkeypatch.setenv("CADTROLY_APPROVAL", "auto")
    asked = []

    async def handler(message, response_type, params, context):
        asked.append(message)
        return ElicitResult(action="accept", content={"value": choice})

    from cadtroly.mcp.server import build_server
    async with Client(build_server(), elicitation_handler=handler) as c:
        h = await _line(c)
        n0 = await _count(c)
        r = await c.call_tool("entity_delete", {"handle": h}, raise_on_error=False)
        assert asked and "xoá đối tượng" in asked[0]
        assert r.is_error is (not deleted)
        assert await _count(c) == (n0 - 1 if deleted else n0)


@pytest.mark.asyncio
async def test_off_and_safe_tools(kho_dir, monkeypatch):
    monkeypatch.setenv("CADTROLY_APPROVAL", "off")
    from cadtroly.mcp.server import build_server
    async with Client(build_server()) as c:
        h = await _line(c)
        r = await c.call_tool("entity_delete", {"handle": h})
        assert not r.is_error
    monkeypatch.setenv("CADTROLY_APPROVAL", "token")
    async with Client(build_server()) as c:
        await _line(c)                                   # tạo mới không cần duyệt

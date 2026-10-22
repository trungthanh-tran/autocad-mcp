"""Generate the end-user Markdown guide for every registered MCP tool.

The upstream inventory supplies grouping and safety metadata.  The live
FastMCP registry supplies the authoritative description and JSON schema, so
the generated guide also covers cadtroly extensions.
"""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "docs" / "tool-inventory.json"
OUTPUT = ROOT / "docs" / "MCP-TOOL-USAGE.md"


WHEN_BY_GROUP = {
    "analysis": "Khi cần đọc, đo, thống kê hoặc phân tích bản vẽ mà không sửa dữ liệu.",
    "architecture": "Khi làm mặt bằng, mặt đứng, mặt cắt và các thành phần kiến trúc.",
    "batch": "Khi cần xử lý nhiều bản vẽ hoặc nhiều đối tượng trong một lượt.",
    "blocks": "Khi tạo, chèn, đọc hoặc quản lý block và block reference.",
    "dimensions": "Khi tạo hoặc hiệu chỉnh kích thước, ghi chú kích thước.",
    "drawing": "Khi mở, lưu, đóng, xuất hoặc kiểm tra trạng thái bản vẽ.",
    "engineering": "Khi cần kiểm tra hoặc thao tác theo yêu cầu kỹ thuật.",
    "entity_creation": "Khi cần vẽ thêm đối tượng hình học vào bản vẽ.",
    "entity_modification": "Khi cần sửa, di chuyển, xoay, scale hoặc biến đổi đối tượng.",
    "entity_query": "Khi cần tìm và đọc thuộc tính đối tượng theo handle hoặc điều kiện.",
    "environment": "Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.",
    "layers": "Khi tạo, đổi tên, bật/tắt, đóng băng hoặc quản lý layer.",
    "layouts": "Khi quản lý layout, viewport và không gian giấy.",
    "mechanical": "Khi dựng hoặc kiểm tra bản vẽ cơ khí, chi tiết và dung sai.",
    "page_setup": "Khi thiết lập khổ giấy, máy in, tỷ lệ và cấu hình xuất bản.",
    "pid": "Khi dựng hoặc kiểm tra sơ đồ P&ID, đường ống và thiết bị.",
    "plant": "Khi làm bản vẽ plant hoặc bố trí thiết bị công nghiệp.",
    "premium": "Khi dùng chức năng nâng cao; kiểm tra capability trước nếu backend không hỗ trợ.",
    "sheet": "Khi tạo và quản lý sheet, title block và hồ sơ phát hành.",
    "solids": "Khi tạo hoặc kiểm tra solid/3D geometry.",
    "styles": "Khi quản lý text style, dimension style, linetype và kiểu hiển thị.",
    "system": "Khi cần chẩn đoán server hoặc trạng thái kết nối.",
    "templates": "Khi tạo bản vẽ từ template hoặc mẫu có sẵn.",
    "transactions": "Khi muốn gom thay đổi thành giao dịch có thể xác nhận hoặc hoàn tác.",
    "understanding": "Khi cần LLM hiểu cấu trúc, ngữ cảnh hoặc nội dung bản vẽ.",
    "validation": "Khi kiểm tra tính hợp lệ và lỗi kỹ thuật của bản vẽ.",
    "view": "Khi đổi góc nhìn, zoom, chụp ảnh hoặc render vùng bản vẽ.",
}

EXAMPLE_OVERRIDES = {
    "pdf_to_dwg": {
        "source": r"D:\DuAn\mat-bang.pdf",
        "target": r"D:\DuAn\mat-bang_semantic.dwg",
        "paper": "A1",
        "orientation": "landscape",
    },
    "kho_standards": {"industry": "architecture"},
    "kho_standard_add": {
        "industry": "architecture",
        "standard": {"code": "TCVN-EXAMPLE", "title": "Tiêu chuẩn dự án", "source": "internal"},
    },
    "kho_skill_add": {
        "name": "my-project-rule",
        "content": "---\ntitle: Quy tắc dự án\n---\nNội dung hướng dẫn cho LLM.",
        "overwrite": False,
    },
}


def _first_sentence(text: str) -> str:
    text = " ".join((text or "").strip().split())
    return text.split(". ", 1)[0].rstrip(".") + ("." if text else "")


def _annotation(tool: Any, key: str) -> Any:
    annotations = getattr(tool, "annotations", None)
    if isinstance(annotations, dict):
        return annotations.get(key)
    return getattr(annotations, key, None)


def _value(name: str, schema: dict[str, Any]) -> Any:
    if "default" in schema:
        return schema["default"]
    if schema.get("enum"):
        return schema["enum"][0]
    typ = schema.get("type")
    lname = name.lower()
    if typ == "boolean":
        return True
    if typ == "integer":
        return 1
    if typ == "number":
        return 1.0
    if typ == "array":
        return []
    if typ == "object":
        return {}
    if any(word in lname for word in ("path", "source", "target", "file")):
        return r"D:\DuAn\drawing.dwg"
    if "handle" in lname:
        return "A1B2"
    if "name" in lname:
        return "example"
    if "point" in lname:
        return [0, 0, 0]
    return "example"


def _compact_type(schema: dict[str, Any]) -> str:
    typ = schema.get("type", "any")
    if typ == "array" and schema.get("items"):
        return f"array<{schema['items'].get('type', 'any')}>"
    if schema.get("enum"):
        return "enum: " + ", ".join(map(str, schema["enum"]))
    return typ


def _parameter_rows(schema: dict[str, Any]) -> tuple[str, str]:
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))
    rows = []
    values = {}
    for name, item in properties.items():
        item = item if isinstance(item, dict) else {}
        desc = " ".join(str(item.get("description", "")).split()) or "—"
        default = item.get("default", "—")
        rows.append(f"| `{name}` | `{_compact_type(item)}` | {'có' if name in required else 'không'} | `{default}` | {desc} |")
        values[name] = _value(name, item)
    if not rows:
        rows.append("| — | — | — | — | Tool không yêu cầu tham số. |")
    return "\n".join(rows), json.dumps(values, ensure_ascii=False, indent=2)


def _when(group: str, name: str) -> str:
    return WHEN_BY_GROUP.get(group, f"Khi cần dùng chức năng `{name}` trong quy trình CAD.")


def generate() -> None:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    upstream = {item["name"]: item for item in inventory["tools"]}

    # Import only after the repository root is known; server.py is the live registry.
    os.environ.setdefault("TOOL_PROFILE", "full")
    os.environ.setdefault("TOOL_PACKS", "all")
    import sys

    sys.path.insert(0, str(ROOT))
    import server  # type: ignore  # noqa: PLC0415

    tools = asyncio.run(server._registered_tools())
    asyncio.run(server._apply_tool_profile("full"))
    live = {tool.name: tool for tool in tools}

    sections = []
    for name in sorted(live):
        tool = live[name]
        meta = upstream.get(name, {})
        group = meta.get("group", "cadtroly")
        description = getattr(tool, "description", "") or meta.get("summary", "")
        schema = getattr(tool, "parameters", {}) or {"properties": {}}
        if not isinstance(schema, dict):
            schema = {"properties": {}}
        table, example = _parameter_rows(schema)
        if name in EXAMPLE_OVERRIDES:
            example = json.dumps(EXAMPLE_OVERRIDES[name], ensure_ascii=False, indent=2)
        readonly = _annotation(tool, "readOnlyHint")
        safety = "Chỉ đọc; có thể dùng trước khi chỉnh sửa." if readonly else "Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng."
        sections.append(
            f"### `{name}`\n\n"
            f"**Nhóm:** `{group}`  \n"
            f"**Làm gì:** {description.strip()}\n\n"
            f"**Dùng khi nào:** {_when(group, name)}\n\n"
            f"**Tham số**\n\n| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |\n|---|---|---:|---|---|\n{table}\n\n"
            f"**Ví dụ gọi**\n\n```json\n{example}\n```\n\n"
            f"**Lưu ý:** {safety}\n"
        )

    registered = len(tools)
    body = """# MCP tool usage guide

Tài liệu này mô tả **từng tool đang đăng ký trong project cadtroly**: tool làm gì, dùng khi nào, tham số, ví dụ và lưu ý an toàn. File được sinh từ registry FastMCP hiện tại; không sửa thủ công.

## Tổng quan

- Registered tools: **{registered}**
- Enabled với `TOOL_PROFILE=full`, `TOOL_PACKS=all`: **267**
- Hidden/giới hạn backend: **5**
- Resources: **9**; prompt templates: **5**
- Tool upstream trong `tool-inventory.json`: **247**; phần còn lại là extension của project.

## Cách gọi chung

LLM gọi đúng tên tool và truyền một JSON object theo bảng tham số:

```json
{{
  "name": "tool_name",
  "arguments": {{}}
}}
```

Đối với tool làm thay đổi bản vẽ, nên đọc/chụp trạng thái trước, chạy tool, sau đó kiểm tra lại và lưu ra file đích. Với PDF, dùng `pdf_to_dwg` để tạo DWG semantic và tự dọn file trung gian.

## Chi tiết từng tool

""".format(registered=registered)
    OUTPUT.write_text(body + "\n".join(sections), encoding="utf-8")
    print(f"Wrote {OUTPUT} ({registered} tools)")


if __name__ == "__main__":
    generate()

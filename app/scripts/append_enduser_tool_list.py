"""Append the complete live tool list to the Vietnamese end-user guide."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "HUONG-DAN-ENDUSER.md"
INVENTORY = ROOT / "docs" / "tool-inventory.json"
MARKER = "<!-- GENERATED-ALL-TOOLS -->"

GROUP_WHEN = {
    "analysis": "đọc/đo/phân tích, không sửa bản vẽ",
    "architecture": "mặt bằng, mặt đứng, mặt cắt kiến trúc",
    "batch": "xử lý hàng loạt",
    "blocks": "block và block reference",
    "dimensions": "kích thước và ghi chú dim",
    "drawing": "mở, lưu, đóng hoặc xuất bản vẽ",
    "engineering": "kiểm tra kỹ thuật",
    "entity_creation": "vẽ thêm đối tượng",
    "entity_modification": "sửa hoặc biến đổi đối tượng",
    "entity_query": "tìm và đọc thuộc tính đối tượng",
    "environment": "kiểm tra kết nối và cấu hình",
    "layers": "tạo và quản lý layer",
    "layouts": "layout và viewport",
    "mechanical": "bản vẽ cơ khí",
    "page_setup": "khổ giấy, tỷ lệ và in ấn",
    "pid": "sơ đồ P&ID",
    "plant": "bố trí thiết bị plant",
    "premium": "chức năng nâng cao",
    "sheet": "sheet, khung tên và phát hành",
    "solids": "hình học 3D/solid",
    "styles": "style và hiển thị",
    "system": "trạng thái server",
    "templates": "template bản vẽ",
    "transactions": "giao dịch thay đổi có kiểm soát",
    "understanding": "đọc hiểu cấu trúc bản vẽ",
    "validation": "kiểm tra hợp lệ",
    "view": "zoom, góc nhìn và ảnh chụp",
}


def main() -> None:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    upstream = {x["name"]: x for x in inventory["tools"]}
    os.environ.setdefault("TOOL_PROFILE", "full")
    os.environ.setdefault("TOOL_PACKS", "all")
    sys.path.insert(0, str(ROOT))
    import server  # type: ignore

    tools = asyncio.run(server._registered_tools())
    live = {tool.name: tool for tool in tools}
    rows = []
    for name in sorted(live):
        tool = live[name]
        meta = upstream.get(name, {})
        group = meta.get("group", "cadtroly")
        text = meta.get("summary") or getattr(tool, "description", "") or "Chức năng mở rộng của project."
        text = " ".join(str(text).split()).replace("|", "\\|")
        when = GROUP_WHEN.get(group, "chức năng mở rộng của cadtroly")
        rows.append(f"| `{name}` | `{group}` | {text} | Khi cần {when}. |")
    generated = (
        f"{MARKER}\n\n## Danh sách đầy đủ tất cả tool\n\n"
        f"Bảng này gồm **{len(rows)} tool** đang đăng ký, bao gồm cả **247 tool upstream** và tool mở rộng của cadtroly. Bạn có thể nói tên tool trong yêu cầu nếu muốn gọi trực tiếp.\n\n"
        "| Tool | Nhóm | Làm gì | Dùng khi nào |\n|---|---|---|---|\n"
        + "\n".join(rows)
        + "\n"
    )
    text = DOC.read_text(encoding="utf-8")
    text = text.split(MARKER, 1)[0].rstrip() + "\n\n" + generated
    DOC.write_text(text, encoding="utf-8")
    print(f"Updated {DOC} with {len(rows)} tools")


if __name__ == "__main__":
    main()

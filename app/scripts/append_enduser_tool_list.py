"""Append the complete live tool list to docs/6-danh-muc-chuc-nang.md (Vietnamese end-user catalog)."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT.parent / "docs" / "6-danh-muc-chuc-nang.md"
INVENTORY = ROOT / "docs" / "tool-inventory.json"
MARKER = "<!-- GENERATED-ALL-TOOLS -->"

GROUP_WHEN = {
    "analysis": "đọc/đo/phân tích, không sửa bản vẽ",
    "architecture": "mặt bằng, mặt đứng, mặt cắt kiến trúc",
    "batch": "xử lý hàng loạt",
    "blocks": "khối và tham chiếu khối",
    "dimensions": "kích thước và ghi chú đo",
    "drawing": "mở, lưu, đóng hoặc xuất bản vẽ",
    "engineering": "kiểm tra kỹ thuật",
    "entity_creation": "vẽ thêm đối tượng",
    "entity_modification": "sửa hoặc biến đổi đối tượng",
    "entity_query": "tìm và đọc thuộc tính đối tượng",
    "environment": "kiểm tra kết nối và cấu hình",
    "layers": "tạo và quản lý lớp bản vẽ",
    "layouts": "bố cục và khung nhìn",
    "mechanical": "bản vẽ cơ khí",
    "page_setup": "khổ giấy, tỷ lệ và in ấn",
    "pid": "sơ đồ P&ID",
    "plant": "bố trí thiết bị nhà máy",
    "premium": "chức năng nâng cao",
    "sheet": "tờ bản vẽ, khung tên và phát hành",
    "solids": "hình học ba chiều và khối đặc",
    "styles": "kiểu và hiển thị",
    "system": "trạng thái máy chủ",
    "templates": "mẫu bản vẽ",
    "transactions": "giao dịch thay đổi có kiểm soát",
    "understanding": "đọc hiểu cấu trúc bản vẽ",
    "validation": "kiểm tra hợp lệ",
    "view": "thu phóng, góc nhìn và ảnh chụp",
}
GROUP_VI = {
    "analysis": "phân tích", "architecture": "thành phần kiến trúc", "batch": "xử lý hàng loạt",
    "blocks": "khối", "corner_ops": "bo góc và cắt nối", "dimensions": "kích thước", "drawing": "bản vẽ", "engineering": "kỹ thuật",
    "entity_creation": "tạo đối tượng", "entity_modification": "sửa đối tượng", "entity_query": "tra cứu đối tượng",
    "environment": "môi trường", "layers": "lớp bản vẽ", "layouts": "bố cục", "mechanical": "cơ khí",
    "page_setup": "thiết lập trang", "pid": "P&ID", "plant": "nhà máy", "premium": "nâng cao",
    "sheet": "tờ bản vẽ", "solids": "khối đặc", "styles": "kiểu hiển thị", "system": "hệ thống",
    "templates": "mẫu bản vẽ", "transactions": "giao dịch", "understanding": "đọc hiểu",
    "validation": "xác nhận", "view": "góc nhìn", "cadtroly": "mở rộng cadtroly",
}

INDUSTRY_ORDER = [
    "Dùng chung",
    "Kiến trúc",
    "Cơ khí",
    "P&ID",
    "Nhà máy",
    "Kỹ thuật và 3D",
    "Nâng cao",
    "Mở rộng cadtroly",
]

INDUSTRY_GROUPS = {
    "Kiến trúc": {"architecture"},
    "Cơ khí": {"mechanical"},
    "P&ID": {"pid"},
    "Nhà máy": {"plant"},
    "Kỹ thuật và 3D": {"engineering", "solids"},
    "Nâng cao": {"premium"},
    "Mở rộng cadtroly": {"cadtroly"},
}

INDUSTRY_DESCRIPTION = {
    "Dùng chung": "Các chức năng có thể dùng cho hầu hết bản vẽ và ngành kỹ thuật.",
    "Kiến trúc": "Mặt bằng, mặt đứng, mặt cắt, phòng, cửa, tường và hồ sơ kiến trúc.",
    "Cơ khí": "Chi tiết cơ khí, ký hiệu mối hàn và các thao tác phục vụ bản vẽ cơ khí.",
    "P&ID": "Sơ đồ đường ống và thiết bị đo lường điều khiển.",
    "Nhà máy": "Bố trí thiết bị và bản vẽ nhà máy công nghiệp.",
    "Kỹ thuật và 3D": "Kiểm tra kỹ thuật và hình học khối ba chiều.",
    "Nâng cao": "Các chức năng nâng cao cần kiểm tra khả năng backend trước khi dùng.",
    "Mở rộng cadtroly": "Các chức năng riêng của project cadtroly như tiêu chuẩn, QA và khối lượng.",
}


def industry_for(group: str) -> str:
    for industry, groups in INDUSTRY_GROUPS.items():
        if group in groups:
            return industry
    return "Dùng chung"


WORD_VI = {
    "analysis": "phân tích", "bounding": "giới hạn", "box": "khung", "entity": "đối tượng",
    "stats": "thống kê", "find": "tìm", "region": "vùng", "layer": "lớp", "list": "liệt kê",
    "properties": "thuộc tính", "measure": "đo", "area": "diện tích", "distance": "khoảng cách",
    "select": "chọn", "architecture": "kiến trúc", "floor": "tầng", "plan": "mặt bằng",
    "elevation": "mặt đứng", "section": "mặt cắt", "batch": "hàng loạt", "block": "khối",
    "insert": "chèn", "create": "tạo", "delete": "xóa", "remove": "xóa", "update": "cập nhật",
    "modify": "sửa", "move": "di chuyển", "copy": "sao chép", "rotate": "xoay", "scale": "tỷ lệ",
    "mirror": "đối xứng", "trim": "cắt", "extend": "kéo dài", "offset": "song song",
    "dimension": "kích thước", "style": "kiểu", "drawing": "bản vẽ", "open": "mở", "save": "lưu",
    "close": "đóng", "export": "xuất", "import": "nhập", "check": "kiểm tra", "validate": "xác nhận",
    "query": "tra cứu", "read": "đọc", "write": "ghi", "environment": "môi trường", "status": "trạng thái",
    "settings": "thiết lập", "layout": "bố cục", "viewport": "khung nhìn", "page": "trang",
    "setup": "cài đặt", "mechanical": "cơ khí", "pid": "P&ID", "plant": "nhà máy", "sheet": "tờ bản vẽ",
    "solid": "khối đặc", "solids": "khối đặc", "text": "chữ", "line": "đường", "polyline": "đa tuyến",
    "circle": "đường tròn", "arc": "cung", "rectangle": "hình chữ nhật", "point": "điểm",
    "hatch": "tô mặt", "curve": "đường cong", "symbol": "ký hiệu", "weld": "mối hàn",
    "template": "mẫu", "transaction": "giao dịch", "understanding": "đọc hiểu", "view": "góc nhìn",
    "zoom": "thu phóng", "render": "kết xuất", "image": "hình ảnh", "capture": "chụp",
    "xref": "tham chiếu ngoài", "attach": "đính kèm", "manage": "quản lý", "rename": "đổi tên",
    "layout": "bố cục", "viewport": "khung nhìn", "lock": "khóa", "set": "đặt", "scale": "tỷ lệ",
    "by": "theo", "from": "từ", "to": "đến", "with": "với", "all": "tất cả", "and": "và",
    "or": "hoặc", "on": "trên", "in": "trong", "of": "của", "at": "tại", "entities": "đối tượng",
    "define": "định nghĩa", "references": "tham chiếu", "reference": "tham chiếu", "find": "tìm",
    "type": "loại", "opening": "ô cửa", "rooms": "phòng", "room": "phòng", "wall": "tường",
    "grid": "lưới trục", "stair": "cầu thang", "catalogue": "danh mục", "schedule": "bảng thống kê",
    "load": "nạp", "reload": "nạp lại", "bind": "gắn", "detach": "tháo", "repath": "đổi đường dẫn",
    "current": "hiện tại", "active": "đang hoạt động", "name": "tên", "names": "tên", "all": "tất cả",
    "inside": "bên trong", "outside": "bên ngoài", "near": "gần", "parallel": "song song",
    "closed": "kín", "open": "mở", "closed": "kín", "break": "ngắt", "at": "tại",
    "purge": "dọn dẹp", "explode": "phá khối", "join": "nối", "break": "ngắt", "connect": "kết nối",
    "property": "thuộc tính", "properties": "thuộc tính", "data": "dữ liệu", "table": "bảng",
    "about": "thông tin", "system": "hệ thống", "capability": "khả năng", "available": "khả dụng",
    "circle": "đường tròn", "polygon": "đa giác", "region": "vùng", "leader": "đường dẫn",
    "kho": "kho", "standard": "tiêu chuẩn", "standards": "tiêu chuẩn", "add": "thêm",
    "toggle": "bật tắt", "skill": "kỹ năng", "skills": "kỹ năng", "industry": "ngành",
    "industries": "ngành", "ruleset": "bộ quy tắc", "rulesets": "bộ quy tắc", "rule": "quy tắc",
    "run": "chạy", "export": "xuất", "import": "nhập", "delete": "xóa", "check": "kiểm tra",
    "takeoff": "bóc tách khối lượng", "compute": "tính toán", "decide": "quyết định", "propose": "đề xuất",
    "execute": "thực thi", "report": "báo cáo", "render": "kết xuất", "semantic": "ngữ nghĩa",
    "vectorize": "chuyển thành véc-tơ", "discipline": "bộ môn", "structural": "kết cấu",
    "qa": "kiểm tra chất lượng", "pdf": "PDF", "dwg": "DWG", "dxf": "DXF", "screenshot": "ảnh chụp",
    "extents": "phạm vi", "window": "cửa sổ", "audit": "kiểm tra tổng thể", "redo": "làm lại",
    "undo": "hoàn tác", "new": "mới", "as": "thành", "plot": "in bản vẽ", "lisp": "LISP",
    "variable": "biến", "variables": "biến", "command": "lệnh", "opening": "ô cửa", "arch": "kiến trúc",
    "spec": "đặc tả", "room": "phòng", "rooms": "phòng", "wall": "tường", "stair": "cầu thang",
    "catalogue": "danh mục", "schedule": "bảng thống kê", "attributes": "thuộc tính", "attribute": "thuộc tính",
    "settings": "thiết lập", "property": "thuộc tính", "properties": "thuộc tính", "table": "bảng",
}


def vietnamese_name(name: str) -> str:
    if name.startswith("kho_"):
        return vietnamese_name(name.replace("kho_", "knowledge_", 1))
    special = {
        "knowledge_industries": "liệt kê các ngành trong kho",
        "knowledge_standards": "liệt kê tiêu chuẩn trong kho",
        "knowledge_standard_add": "thêm tiêu chuẩn vào kho",
        "knowledge_standard_delete": "xóa tiêu chuẩn khỏi kho",
        "knowledge_skills": "liệt kê kỹ năng trong kho",
        "knowledge_skill_add": "thêm kỹ năng vào kho",
        "knowledge_skill_toggle": "bật hoặc tắt kỹ năng trong kho",
        "knowledge_rules_export": "xuất bộ quy tắc trong kho",
        "knowledge_rules_import": "nhập bộ quy tắc vào kho",
        "knowledge_status": "kiểm tra trạng thái kho",
        "check_rulesets": "kiểm tra các bộ quy tắc",
        "check_run": "chạy kiểm tra bản vẽ",
        "drawing_entities": "đọc các đối tượng trong bản vẽ",
        "drawing_read": "đọc bản vẽ",
        "takeoff_compute": "tính toán khối lượng",
        "takeoff_decide": "xác nhận quyết định bóc tách",
        "takeoff_export": "xuất bảng khối lượng",
        "takeoff_propose": "đề xuất phương án bóc tách",
        "takeoff_run": "chạy bóc tách khối lượng",
        "takeoff_earthwork": "bóc khối lượng đào đắp từ trắc ngang",
        "takeoff_rebar": "thống kê cốt thép từ ghi chú",
        "approval_execute": "thực hiện thao tác đã được đồng ý",
        "pdf_to_dwg": "chuyển PDF sang DWG",
        "pdf_vectorize": "chuyển PDF thành hình học véc-tơ",
        "drawing_apply_discipline_standard": "áp dụng tiêu chuẩn bộ môn cho bản vẽ",
        "standards_reference": "tra cứu tiêu chuẩn",
        "structural_qa": "kiểm tra chất lượng kết cấu",
        "view_render_report": "kết xuất báo cáo hình ảnh",
    }
    if name in special:
        return special[name]
    words = []
    for token in name.split("_"):
        words.append(WORD_VI.get(token, token))
    return " ".join(words)


def request_example(name: str, group: str) -> str:
    """Return a natural Vietnamese instruction, not merely a tool-name echo."""
    if name == "view_screenshot":
        return "Chụp riêng vùng mặt bằng tầng 1, vùng khung tên và vùng kích thước bên phải."
    if name == "view_zoom_and_screenshot":
        return "Thu toàn bộ bản vẽ vào màn hình rồi chụp ảnh để tôi kiểm tra nhanh."
    if name == "view_zoom_window":
        return "Phóng to riêng vùng mặt bằng tầng 1 để nhìn rõ cửa, thiết bị và kích thước."
    if name == "view_zoom_extents":
        return "Thu phóng để toàn bộ đối tượng của bản vẽ nằm vừa trên màn hình."
    if name == "takeoff_earthwork":
        return ("Bóc đào đắp file trắc ngang D:\\DuAn\\tn.dwg ra Excel; liệt kê trắc ngang không có diện tích "
                "và các đoạn tin cậy B.")
    if name == "takeoff_rebar":
        return "Thống kê thép bản vẽ trụ T1 theo đường kính, chỉ ra ghi chú thiếu số thanh hoặc chiều dài."
    if name == "approval_execute":
        return "Tôi đồng ý xoá các đối tượng vừa liệt kê, thực hiện đi."
    action = vietnamese_name(name)
    templates = {
        "analysis": f"Đọc bản vẽ và báo cáo {action}; không sửa file gốc.",
        "architecture": f"Trên mặt bằng kiến trúc, hãy {action} và giữ đúng tỷ lệ bản vẽ.",
        "batch": f"Thực hiện {action} cho tất cả bản vẽ trong thư mục dự án và báo cáo từng file.",
        "blocks": f"Trong bản vẽ hiện tại, hãy {action} cho các khối cửa và thiết bị.",
        "dimensions": f"Kiểm tra và thực hiện {action} cho các kích thước của mặt bằng tầng 1.",
        "drawing": f"Mở bản vẽ, thực hiện {action}, sau đó lưu ra file mới và không ghi đè file gốc.",
        "engineering": f"Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo {action} thành lỗi hoặc cảnh báo.",
        "entity_creation": f"Vẽ thêm đối tượng cần thiết để {action}, đặt đúng lớp bản vẽ và ghi chú rõ ràng.",
        "entity_modification": f"Chụp ảnh trước, thực hiện {action}, chụp ảnh sau và liệt kê các đối tượng đã đổi.",
        "entity_query": f"Tìm các đối tượng liên quan rồi báo cáo {action}, không thay đổi hình học.",
        "environment": f"Kiểm tra kết nối AutoCAD và báo cáo {action} trước khi thao tác bản vẽ.",
        "layers": f"Tổ chức các đối tượng theo lớp bản vẽ bằng cách {action}, không tự đổi tiêu chuẩn nếu chưa hỏi.",
        "layouts": f"Thiết lập bố cục A1 và thực hiện {action} cho khung tên và khung nhìn.",
        "mechanical": f"Trên bản vẽ cơ khí, hãy {action} theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn.",
        "page_setup": f"Thiết lập khổ A1, tỷ lệ 1:100 rồi thực hiện {action} để chuẩn bị phát hành.",
        "pid": f"Trên sơ đồ P&ID, hãy {action} và kiểm tra ký hiệu, đường ống cùng nhãn thiết bị.",
        "plant": f"Trong bản vẽ nhà máy, hãy {action} và kiểm tra khoảng cách an toàn thiết bị.",
        "premium": f"Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện {action} nếu backend cho phép.",
        "sheet": f"Chuẩn bị tờ bản vẽ phát hành và thực hiện {action} trong khung tên.",
        "solids": f"Kiểm tra hình học ba chiều rồi thực hiện {action}; không làm hỏng đối tượng gốc.",
        "styles": f"Kiểm tra kiểu hiển thị hiện tại và thực hiện {action} cho toàn bộ bản vẽ.",
        "system": f"Báo cáo trạng thái MCP, AutoCAD và backend bằng cách {action}.",
        "templates": f"Tạo bản vẽ mới từ mẫu dự án rồi thực hiện {action} theo tiêu chuẩn đã chọn.",
        "transactions": f"Bắt đầu giao dịch, thực hiện {action}, cho tôi xem thay đổi rồi mới xác nhận.",
        "understanding": f"Đọc hiểu bản vẽ và giải thích {action} bằng ngôn ngữ dễ hiểu cho người dùng.",
        "validation": f"Kiểm tra bản vẽ và báo cáo {action} theo mức Error, Warning và Info.",
        "view": f"Hiển thị bản vẽ để tôi kiểm tra trực quan việc {action}.",
        "cadtroly": f"Thực hiện {action} trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.",
    }
    return templates.get(group, f"Hãy thực hiện {action} trên bản vẽ và báo cáo kết quả.")


def main() -> None:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    upstream = {x["name"]: x for x in inventory["tools"]}
    os.environ.setdefault("TOOL_PROFILE", "full")
    os.environ.setdefault("TOOL_PACKS", "all")
    sys.path.insert(0, str(ROOT))
    import server  # type: ignore

    tools = asyncio.run(server._registered_tools())
    # Legacy kho_* names remain callable in runtime, but end users should see
    # only the canonical English knowledge_* names in the guide.
    live = {tool.name: tool for tool in tools if not tool.name.startswith("kho_")}
    index_by_industry = {industry: {} for industry in INDUSTRY_ORDER}
    details_by_industry = {industry: {} for industry in INDUSTRY_ORDER}
    for name in sorted(live):
        tool = live[name]
        meta = upstream.get(name, {})
        group = meta.get("group", "cadtroly")
        text = f"Thực hiện thao tác {vietnamese_name(name)} trong bản vẽ CAD."
        when = GROUP_WHEN.get(group, "chức năng mở rộng của cadtroly")
        request = request_example(name, group)
        industry = industry_for(group)
        group_name = GROUP_VI.get(group, group)
        index_by_industry[industry].setdefault(group_name, []).append(
            f"- [`{name}`](#{name}) — {GROUP_VI.get(group, group)}: "
            f"dùng để {vietnamese_name(name)} trong bản vẽ CAD."
        )
        details_by_industry[industry].setdefault(group_name, []).append(
            f"#### {name}\n\n"
            f"- **Nhóm:** {GROUP_VI.get(group, group)}\n"
            f"- **Làm gì:** {text}\n"
            f"- **Dùng khi nào:** Khi cần {when}.\n"
            f"- **Ví dụ gõ vào LLM:**\n\n"
            f"  > {request}\n"
        )
    index_rows = []
    detail_sections = []
    for industry in INDUSTRY_ORDER:
        index_rows.append(f"### {industry}")
        index_rows.append(f"_{INDUSTRY_DESCRIPTION[industry]}_")
        for group_name in sorted(index_by_industry[industry]):
            index_rows.append(f"#### {group_name}")
            index_rows.extend(index_by_industry[industry][group_name])
        detail_sections.append(f"## {industry}")
        detail_sections.append(INDUSTRY_DESCRIPTION[industry])
        for group_name in sorted(details_by_industry[industry]):
            detail_sections.append(f"### {group_name}")
            detail_sections.extend(details_by_industry[industry][group_name])
    generated = (
        f"{MARKER}\n\n## Mục lục theo ngành\n\n"
        f"Có **{len(live)} chức năng chính**, gồm **247 chức năng nền tảng** và chức năng mở rộng. Tên chuẩn mới dùng tiếng Anh; các tên cũ vẫn được MCP hỗ trợ tương thích nhưng không liệt kê trong tài liệu enduser. Các chức năng được xếp theo ngành; chức năng dùng chung nằm ở nhóm đầu. Bấm vào tên để đi đến phần hướng dẫn tương ứng.\n\n"
        + "\n".join(index_rows)
        + "\n\n## Chi tiết từng chức năng\n\n"
        + "\n".join(detail_sections)
        + "\n"
    )
    text = DOC.read_text(encoding="utf-8")
    text = text.split(MARKER, 1)[0].rstrip() + "\n\n" + generated
    DOC.write_text(text, encoding="utf-8")
    print(f"Updated {DOC} with {len(live)} tools")


if __name__ == "__main__":
    main()

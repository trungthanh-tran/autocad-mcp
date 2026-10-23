# Tài liệu cadtroly MCP

MCP server cho AutoCAD: Claude, Gemini CLI, Copilot trong VS Code, Cursor… gọi vào để đọc, vẽ, sửa và kiểm tra bản vẽ
DWG/DXF/PDF bằng tiếng Việt. Phiên bản **0.2.0**.

| # | Trang | Dành cho | Nội dung |
|---|---|---|---|
| 1 | [Cài đặt](1-cai-dat.md) | Mọi người | Yêu cầu máy, cài bằng ZIP + `CAI_DAT.bat`, cài từ mã nguồn, cập nhật |
| 2 | [Kết nối client](2-ket-noi-client.md) | Mọi người | Nối MCP vào VS Code, Claude Code, Claude Desktop, Gemini CLI, Cursor |
| 3 | [Cấu hình](3-cau-hinh.md) | Người quản trị | Toàn bộ biến môi trường, `config.json`, chọn backend AutoCAD/DXF |
| 4 | [Hướng dẫn sử dụng](4-huong-dan-su-dung.md) | Người dùng cuối | Cách ra yêu cầu, quy trình sửa an toàn, mẫu câu theo công việc |
| 5 | [Kho, tiêu chuẩn, skill](5-kho-tieu-chuan-skill.md) | Kỹ sư, quản trị | Kho tri thức, tiêu chuẩn 18 ngành, skill, bóc khối lượng A/B/C, mức kết quả kiểm tra |
| 6 | [Danh mục chức năng](6-danh-muc-chuc-nang.md) | Tra cứu | Mọi chức năng theo ngành, mô tả tiếng Việt + câu lệnh mẫu (sinh tự động) |
| 7 | [Xử lý sự cố](7-xu-ly-su-co.md) | Mọi người | MCP không hiện, không thấy AutoCAD, không đọc DWG, LLM làm sai |
| 8 | [Phát triển](8-phat-trien.md) | Dev | Cấu trúc mã, CLI, test, sinh lại tài liệu, phát hành |

Tham khảo kỹ thuật (sinh tự động từ registry):

- [MCP-TOOL-CATALOG.md](../app/docs/MCP-TOOL-CATALOG.md) — số lượng tool, nhóm, resource, prompt template.
- [MCP-TOOL-USAGE.md](../app/docs/MCP-TOOL-USAGE.md) — từng tool: làm gì, khi nào dùng, tham số, ví dụ JSON, lưu ý an toàn.
- [tool-inventory.json](../app/docs/tool-inventory.json) — 247 tool upstream, dạng máy đọc.
- [STANDARDS-SAFETY-BY-INDUSTRY.md](../app/docs/STANDARDS-SAFETY-BY-INDUSTRY.md) — 18 ngành, tiêu chuẩn tham chiếu, giới hạn an toàn.

**Mới dùng lần đầu?** Đọc lần lượt 1 → 2 → 4.

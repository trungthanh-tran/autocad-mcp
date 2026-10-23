# cadtroly — MCP server cho AutoCAD

Phiên bản **0.2.0**. MCP server (stdio) cho Claude, Gemini CLI, Copilot, Cursor… để đọc, vẽ, sửa và kiểm tra bản vẽ
DWG/DXF/PDF: PDF → DWG có phân lớp, bóc khối lượng ra Excel, kiểm tra theo bộ quy tắc, kho tiêu chuẩn và skill chuyên ngành.

Fork của [U-C4N/Autocad-MCP](https://github.com/U-C4N/Autocad-MCP) (MIT, xem `UPSTREAM.md`); mã upstream nằm ngay trong
thư mục này, lớp riêng ở `cadtroly/`.

```bash
pip install -e .
python -m cadtroly.mcp
```

Tài liệu đầy đủ ở [`../docs/`](../docs/README.md):
[cài đặt](../docs/1-cai-dat.md) ·
[kết nối client](../docs/2-ket-noi-client.md) ·
[cấu hình](../docs/3-cau-hinh.md) ·
[hướng dẫn sử dụng](../docs/4-huong-dan-su-dung.md) ·
[kho, tiêu chuẩn, skill](../docs/5-kho-tieu-chuan-skill.md) ·
[danh mục chức năng](../docs/6-danh-muc-chuc-nang.md) ·
[xử lý sự cố](../docs/7-xu-ly-su-co.md) ·
[phát triển](../docs/8-phat-trien.md).

Tham khảo kỹ thuật trong `docs/` của thư mục này:
[MCP-TOOL-CATALOG.md](docs/MCP-TOOL-CATALOG.md) ·
[MCP-TOOL-USAGE.md](docs/MCP-TOOL-USAGE.md) ·
[STANDARDS-SAFETY-BY-INDUSTRY.md](docs/STANDARDS-SAFETY-BY-INDUSTRY.md).

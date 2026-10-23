# autocad-mcp — MCP server cho AutoCAD

MCP server (stdio) để một LLM — Claude, Gemini CLI, Copilot trong VS Code, Cursor… — đọc, vẽ, sửa và kiểm tra bản vẽ
AutoCAD DWG/DXF/PDF bằng tiếng Việt. Mô hình AI nằm ở phía client; server chỉ cung cấp công cụ, không cần đăng nhập.

Fork của [U-C4N/Autocad-MCP](https://github.com/U-C4N/Autocad-MCP) (MIT) cộng lớp riêng `cadtroly`:

- **PDF → DWG** có phân lớp theo bộ môn, chuẩn layer Việt Nam (`KT-`, `KC-`…) hoặc NCS quốc tế.
- **Bóc khối lượng** ra Excel có truy vết handle, độ tin cậy A/B/C và cột mã định mức (TT 38/2026/TT-BXD).
- **Cầu đường không cần Civil 3D**: đào đắp từ trắc ngang (Nova-TDN, vẽ tay), thống kê thép từ ghi chú.
- **Duyệt thao tác phá huỷ** trong server: xoá, ghi đè, lệnh thô chỉ chạy khi người dùng đồng ý.
- **Kiểm tra bản vẽ** theo bộ quy tắc, tiêu chuẩn 18 ngành, QA kết cấu/PCCC sơ bộ.
- **Kho tri thức** dạng thư mục: tiêu chuẩn, quy tắc, 16 skill chuyên ngành, mở rộng được bằng LLM.
- Toàn bộ ~270 tool upstream: vẽ/sửa entity, layer, block, dimension, layout, transaction/undo, screenshot, kiến trúc, cơ khí, P&ID.

Chạy được **không cần AutoCAD** (engine ezdxf, DXF). Có AutoCAD mở sẵn thì tự dùng COM để sửa bản vẽ đang mở.

## Cài nhanh

```bash
cd app
pip install -e .
python -m cadtroly.mcp        # client MCP sẽ tự gọi lệnh này
```

In sẵn cấu hình cho client với đường dẫn máy bạn: `python -m cadtroly.cli connect` (thêm `--prompt` để lấy đoạn dán
cho LLM nhờ tự cấu hình). Hoặc khai báo tay (Claude Desktop, Gemini CLI, Cursor):

```json
{"mcpServers": {"cadtroly": {"command": "python", "args": ["-m", "cadtroly.mcp"], "cwd": "D:\\autocad-mcp\\app",
  "env": {"CADTROLY_KHO": "D:\\CAD-kho", "AUTOCAD_MCP_BACKEND": "auto", "PYTHONIOENCODING": "utf-8"}}}}
```

Người dùng cuối trên Windows: dùng gói ZIP + `CAI_DAT.bat`, xem [Cài đặt](docs/1-cai-dat.md).

## Tài liệu

| | |
|---|---|
| [1. Cài đặt](docs/1-cai-dat.md) | Yêu cầu máy, gói ZIP, cài từ mã nguồn, cập nhật |
| [2. Kết nối client](docs/2-ket-noi-client.md) | VS Code, Claude Code, Claude Desktop, Gemini CLI, Cursor |
| [3. Cấu hình](docs/3-cau-hinh.md) | Biến môi trường, chọn backend, giới hạn an toàn |
| [4. Hướng dẫn sử dụng](docs/4-huong-dan-su-dung.md) | Cách ra yêu cầu, quy trình sửa an toàn, mẫu câu |
| [5. Kho, tiêu chuẩn, skill](docs/5-kho-tieu-chuan-skill.md) | Kho tri thức, 18 ngành, skill, bóc khối lượng A/B/C |
| [6. Danh mục chức năng](docs/6-danh-muc-chuc-nang.md) | Mọi chức năng theo ngành, câu lệnh mẫu |
| [7. Xử lý sự cố](docs/7-xu-ly-su-co.md) | Lỗi kết nối, AutoCAD, DWG, LLM làm sai |
| [8. Phát triển](docs/8-phat-trien.md) | Cấu trúc mã, CLI, test, sinh tài liệu, phát hành |
| [Tham khảo tool](app/docs/MCP-TOOL-USAGE.md) | Tham số, ví dụ JSON từng tool (kỹ thuật) |

## Giấy phép

MIT. Mã upstream © U-C4N, xem `app/LICENSE` và `app/UPSTREAM.md`.

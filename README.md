# autocad-mcp — AI Trợ lý AutoCAD

Fork của [U-C4N/Autocad-MCP](https://github.com/U-C4N/Autocad-MCP) (MIT) cộng lớp riêng `cadtroly`: bóc khối lượng ra Excel
có truy vết, kiểm tra bản vẽ theo bộ quy tắc, kho tri thức dạng thư mục, skill chuyên ngành, giao diện cho người dùng cuối
và bản đóng gói chạy ngay (Windows exe).

| Thư mục / file | Nội dung |
|---|---|
| `app/` | Mã nguồn: MCP server (fork + cadtroly), web UI, CLI, đóng gói. Xem `app/README.md`. |
| `plan-tong.html` | Kế hoạch tổng (3 mong muốn, 4 luồng A/B/C/D, lộ trình) |
| `plan-bptc.html` | Kế hoạch kỹ thuật: agent tự gom tiêu chuẩn + dự án tương đương → vẽ biện pháp thi công |
| `plan-nguoi-dung.html` | Bản giới thiệu cho kỹ sư / chỉ huy trưởng |
| `doi-thu.html` | Khảo sát AI AutoCAD trên thị trường (Autodesk Assistant, MCP mã nguồn mở, tool bóc KL, sxCAD AI) |
| `design.html` | Mockup palette trong AutoCAD (9 màn) |

Chạy nhanh: `cd app && pip install -e ".[dev,web,llm]" && cadtroly sample && cadtroly ui`. Test: `python -m pytest -q`.
Bản giao đối tác: `app\build\build.bat` → `app\dist\AI-Tro-ly-AutoCAD\`.

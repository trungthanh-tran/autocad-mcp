# autocad-mcp — AI Trợ lý AutoCAD

Fork của [U-C4N/Autocad-MCP](https://github.com/U-C4N/Autocad-MCP) cộng lớp riêng
`cadtroly`: PDF/DWG/DXF, tách layer, bóc khối lượng Excel, kiểm tra chất lượng
bản vẽ, kho tiêu chuẩn và skill chuyên ngành.

| Thư mục / file | Nội dung |
|---|---|
| `app/` | Mã nguồn MCP server, backend AutoCAD/DXF, CLI, web UI và dữ liệu mặc định. |
| `CAI_DAT.bat` | Tự cài Python 3.14 và cài MCP trên Windows. |
| `DEPLOY_VSCODE.md` | Hướng dẫn triển khai cho người dùng cuối trong VSCode. |
| `dist/` | Các gói ZIP triển khai; không chứa bản vẽ người dùng. |

Chạy nhanh: `cd app && pip install -e .`. Test và MCP dùng cùng một bộ phụ thuộc;
không cần chọn thêm `dev`, `web` hay `llm`.
Gói mới nhất cho người dùng: `dist\cadtroly-0.2.0-vscode-qa.zip`.

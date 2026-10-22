"""cadtroly: AI Trợ lý cho AutoCAD.

Lớp riêng trên nền autocad-mcp-pro (U-C4N, MIT):
- reader:  đọc bản vẽ thành số liệu (ezdxf headless; COM khi có AutoCAD)
- kho:     kho tri thức dạng thư mục (quy tắc ánh xạ, tiêu chuẩn, chi tiết, skill)
- takeoff: bóc khối lượng ra Excel có truy vết, trạng thái A/B/C
- check:   kiểm tra bản vẽ theo bộ quy tắc
- llm:     gọi LLM (Claude mặc định, Gemini/OpenAI-compatible dự phòng)
- mcp:     MCP server cho Claude Code / Claude Desktop
- web:     API + palette HTML (sau này nhúng vào AutoCAD qua WebView2)
"""

__version__ = "0.2.0"

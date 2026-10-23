# 2. Kết nối client

[← Mục lục tài liệu](README.md) · Trước: [1. Cài đặt](1-cai-dat.md) · Tiếp: [4. Hướng dẫn sử dụng](4-huong-dan-su-dung.md)

MCP `cadtroly` chạy qua **stdio**: client tự khởi động lệnh `python -m cadtroly.mcp` và nói chuyện với nó. Bạn chỉ cần
khai báo lệnh này trong cấu hình của client.

## Cách nhanh: sinh sẵn cấu hình

Trong thư mục `code` (bản ZIP thì dùng `.venv\Scripts\python.exe`):

```bash
python -m cadtroly.cli connect                       # mọi client, đường dẫn thật của máy này
python -m cadtroly.cli connect --client vscode       # vscode | claude-code | claude-desktop | gemini | json
python -m cadtroly.cli connect --prompt | clip       # copy một đoạn nhờ LLM tự cấu hình
```

Lệnh tự điền python, thư mục `code`, kho và gấp đôi `\` trong JSON. `--prompt` in một đoạn để dán vào Claude, Gemini,
Copilot… — nó nhờ LLM đăng ký server vào công cụ của chính nó rồi gọi `knowledge_status` để kiểm tra. Lệnh
`gemini mcp add` chưa thử trên máy thật; báo lỗi cú pháp thì dùng `--client json`.

Muốn tự viết tay thì làm theo các mục dưới. Đổi `D:\cadtroly\code` thành nơi bạn cài (thư mục chứa `pyproject.toml`).
Trong JSON, mỗi dấu `\` phải viết thành `\\`.

## VS Code (GitHub Copilot)

1. `Ctrl+Shift+P` → **MCP: Open User Configuration**.
2. Dán cấu hình dưới, sửa đường dẫn, lưu.
3. `Ctrl+Shift+P` → **MCP: List Servers** → chọn `cadtroly` → **Start**.

```json
{
  "servers": {
    "cadtroly": {
      "type": "stdio",
      "command": "D:\\cadtroly\\code\\.venv\\Scripts\\python.exe",
      "args": ["-m", "cadtroly.mcp"],
      "cwd": "D:\\cadtroly\\code",
      "env": {
        "CADTROLY_KHO": "D:\\CAD-kho",
        "DWG_MCP_ALLOWED_ROOTS": "D:\\CAD-kho",
        "AUTOCAD_MCP_BACKEND": "auto",
        "TOOL_PROFILE": "full",
        "TOOL_PACKS": "all",
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

VS Code dùng khoá gốc `servers` và cần `"type": "stdio"`; các client khác dùng `mcpServers`.

## Claude Code

Mở thư mục `app` là dùng được ngay: `app/.mcp.json` đã khai báo sẵn server. Hoặc thêm bằng lệnh:

```bash
claude mcp add cadtroly -e CADTROLY_KHO=D:\CAD-kho -e PYTHONIOENCODING=utf-8 -- "D:\cadtroly\code\.venv\Scripts\python.exe" -m cadtroly.mcp
```

Kiểm tra: `claude mcp list`, hoặc gõ `/mcp` trong phiên Claude Code.

## Claude Desktop

Mở `%APPDATA%\Claude\claude_desktop_config.json` (Settings → Developer → Edit Config), thêm khối dưới, rồi thoát hẳn và mở
lại Claude Desktop.

```json
{
  "mcpServers": {
    "cadtroly": {
      "command": "D:\\cadtroly\\code\\.venv\\Scripts\\python.exe",
      "args": ["-m", "cadtroly.mcp"],
      "cwd": "D:\\cadtroly\\code",
      "env": {
        "CADTROLY_KHO": "D:\\CAD-kho",
        "DWG_MCP_ALLOWED_ROOTS": "D:\\CAD-kho",
        "AUTOCAD_MCP_BACKEND": "auto",
        "TOOL_PROFILE": "full",
        "TOOL_PACKS": "all",
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

## Gemini CLI

Thêm cùng khối `mcpServers` như Claude Desktop vào `%USERPROFILE%\.gemini\settings.json` (Linux/macOS:
`~/.gemini/settings.json`). Kiểm tra bằng lệnh `/mcp` trong Gemini CLI.

## Cursor, Cline và client khác

Dùng cùng khối `mcpServers` trong file cấu hình MCP của client (Cursor: `~/.cursor/mcp.json` hoặc `.cursor/mcp.json` trong
dự án). Nếu client giới hạn số tool, đặt `TOOL_PROFILE=lean` hoặc `DISCOVERY_MODE=search` — xem
[3. Cấu hình](3-cau-hinh.md#chọn-tool-và-backend).

## Ý nghĩa các trường

| Trường | Ý nghĩa | Có cần sửa? |
|---|---|---|
| `command` | Python trong `.venv` của cadtroly. Dùng `python` nếu đã có trong PATH và đã cài gói | Sửa theo nơi cài |
| `args` | Chạy module `cadtroly.mcp` | Giữ nguyên |
| `cwd` | Thư mục `code` (chứa `pyproject.toml`) | Sửa theo nơi cài |
| `env` | Thiết lập gửi cho MCP khi khởi động | Xem [3. Cấu hình](3-cau-hinh.md) |

## Kiểm tra kết nối

Hỏi client: *"MCP cadtroly đang chạy bằng AutoCAD hay DXF?"* (LLM sẽ gọi `knowledge_status`). Kết quả phải có backend
(`com` hoặc `ezdxf`), đường dẫn kho và phiên bản. Không ra kết quả → [7. Xử lý sự cố](7-xu-ly-su-co.md).

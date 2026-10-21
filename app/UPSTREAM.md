# Nguồn gốc fork

Thư mục này là **fork** của [U-C4N/Autocad-MCP](https://github.com/U-C4N/Autocad-MCP) (AutoCAD MCP Pro, giấy phép MIT,
giữ nguyên `LICENSE`), lấy tại commit `cdb10638963898b3ea9b10cdd96a2c9bc495f184` ngày 21/10/2026.

## Giữ nguyên từ upstream
`server.py` (phần lớn), `backends/`, `engineering/`, `discovery/`, `templates/`, `scripts/`, `config.py`, `security.py`,
`version.py`, `server.json`, `docs/`, test upstream chuyển vào `upstream_tests/`. Tài liệu gốc: `UPSTREAM-README.md`,
`UPSTREAM-CLAUDE.md`, `UPSTREAM-CHANGELOG.md`.

## Đã sửa trong fork
- `server.py`: tên server → `cadtroly`; thêm hướng dẫn tiếng Việt vào `instructions`; lifespan gắn thêm `cfg`, `kho`,
  `state` (từ `cadtroly/mcp/state.py`); cuối file gọi `cadtroly.mcp.tools.register(mcp)` để đăng ký tool cadtroly
  vào **cùng một server** (không mount, không tiền tố).
- `pyproject.toml`: gộp phụ thuộc, tên gói `cadtroly`, không còn kéo upstream từ GitHub.
- Mặc định `TOOL_PROFILE=lean`, `TOOL_PACKS=core,arch` khi chạy qua `python -m cadtroly.mcp`.

## Phần riêng (thư mục `cadtroly/`)
reader (ezdxf, đo flatten), kho (quy tắc ánh xạ, tiêu chuẩn, skill), takeoff (A/B/C, Excel truy vết), check (bộ quy
tắc JSON), llm (Claude/Gemini/OpenAI-compatible), cli, mcp/tools.

## Cập nhật từ upstream
Không có git remote; muốn kéo bản mới thì diff thủ công với tag upstream rồi áp lại ba chỗ sửa trong `server.py` ở trên.

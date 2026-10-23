# 8. Phát triển

[← Mục lục tài liệu](README.md)

## Cấu trúc mã

`app/` là fork của [U-C4N/Autocad-MCP](https://github.com/U-C4N/Autocad-MCP) (MIT, xem `app/UPSTREAM.md`). Mã upstream nằm
ngay trong repo, không cài từ GitHub. Tất cả chạy trong **một server** tên `cadtroly`; tool upstream giữ nguyên tên.

| Đường dẫn | Nội dung |
|---|---|
| `app/server.py`, `backends/`, `engineering/`, `discovery/`, `templates/` | Upstream: registry tool, backend COM/ezdxf, tính toán kỹ thuật |
| `app/cadtroly/mcp/` | Entry MCP (`python -m cadtroly.mcp`), bootstrap tự cài gói, đăng ký tool cadtroly |
| `app/cadtroly/mcp/approval.py` | Middleware duyệt thao tác phá huỷ (elicitation hoặc token dùng một lần); bảng `RULES` quyết định tool nào cần duyệt |
| `app/cadtroly/reader/`, `takeoff/`, `check/`, `kho/` | Đọc bản vẽ, bóc khối lượng (`takeoff/civil.py`: đào đắp, thép), kiểm tra theo quy tắc, kho tri thức |
| `app/cadtroly/pdf_vectorize.py` | Bóc vector/text/dimension từ PDF |
| `app/kho-mac-dinh/` | Tiêu chuẩn, quy tắc, skill đi kèm |
| `app/tests/`, `app/upstream_tests/` | Test cadtroly / test upstream |
| `app/scripts/` | Sinh tài liệu, smoke test COM, render ảnh README |
| `app/docs/` | Catalog/usage sinh tự động, tiêu chuẩn theo ngành, phân tích và thiết kế nội bộ |
| `CAI_DAT.bat`, `dist/` | Cài cho người dùng cuối, gói ZIP |

## Lệnh CLI

Tuỳ chọn chung: `--kho <thư mục>` (mặc định `CADTROLY_KHO`).

| Lệnh | Việc |
|---|---|
| `cadtroly init` | Tạo kho + `config.json` |
| `cadtroly sample [out.dxf]` | Sinh bản vẽ mẫu |
| `cadtroly read <dxf>` | In tóm tắt bản vẽ (JSON) |
| `cadtroly takeoff <dxf\|thư mục> [--h 3.3] [--out x.xlsx]` | Bóc khối lượng ra Excel |
| `cadtroly check <dxf> <ruleset>` | Kiểm tra theo bộ quy tắc (`.rules.json` hoặc id trong kho) |
| `cadtroly mcp` | Chạy MCP server (stdio), giống `python -m cadtroly.mcp` |
| `cadtroly update` | Cập nhật code và gói từ GitHub; dừng nếu có sửa chưa commit |
| `cadtroly connect [--client X] [--prompt]` | In cấu hình nối MCP cho VS Code/Claude/Gemini/Cursor với đường dẫn máy này, hoặc prompt dán cho LLM |

## Test

```bash
cd app
python -m pytest -q                  # test cadtroly + suite hiện tại
python -m pytest -q upstream_tests/  # test upstream, chạy lâu
```

Backend COM có smoke test riêng trong `app/scripts/smoke_*_com.py`, cần AutoCAD thật.

## Sinh lại tài liệu

Khi thêm/đổi tool, chạy lại để tài liệu khớp registry:

```bash
cd app
python scripts/generate_tool_usage.py          # → app/docs/MCP-TOOL-USAGE.md
python scripts/append_enduser_tool_list.py     # → docs/6-danh-muc-chuc-nang.md (phần sau marker GENERATED-ALL-TOOLS)
python scripts/generate_tool_inventory.py      # → app/docs/tool-inventory.json (upstream)
```

Cập nhật tay con số trong `app/docs/MCP-TOOL-CATALOG.md` nếu tổng số tool đổi.

## Phát hành

Gói người dùng là ZIP `dist/cadtroly-<version>-vscode-dwg.zip` (thư mục `code` + `CAI_DAT.bat`), không chứa bản vẽ người
dùng. Khi đổi phiên bản: `app/pyproject.toml`, `app/server.json`, dòng phiên bản trong `CAI_DAT.bat` và tài liệu.
Quy trình phát hành upstream (PyPI, MCP registry) giữ trong [RELEASE-DISTRIBUTION.md](../app/docs/RELEASE-DISTRIBUTION.md).

## Giới hạn đã biết

- Backend COM live (preview revision cloud, UNDO group, PostMessage không cướp focus) có code nền trong
  `backends/com_backend.py` nhưng **chưa test đầy đủ trên AutoCAD thật**.
- `tieu-chuan/qcvn-18-2021.rules.json` là mẫu, mọi dòng `duyet=false`.
- Không đọc được DWG nếu thiếu cả AutoCAD lẫn ODA File Converter.

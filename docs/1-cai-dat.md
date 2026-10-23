# 1. Cài đặt

[← Mục lục tài liệu](README.md) · Tiếp: [2. Kết nối client](2-ket-noi-client.md)

## Yêu cầu

| Thành phần | Bắt buộc? | Ghi chú |
|---|---|---|
| Windows 10/11 | Với bản ZIP | Mã nguồn chạy được cả Linux/macOS nhưng chỉ ở chế độ DXF |
| Python 3.11+ | Có | Bản ZIP tự cài Python 3.14 nếu máy chưa có |
| Client AI có MCP | Có | VS Code (Copilot), Claude Code/Desktop, Gemini CLI, Cursor… |
| AutoCAD | Không | Có thì sửa trực tiếp bản vẽ đang mở (COM). Không có thì đọc/vẽ DXF |
| ODA File Converter | Không | Cần để đọc DWG khi **không** có AutoCAD |

Không cần tài khoản hay đăng nhập riêng cho MCP: mô hình AI là của client bạn đang dùng.

## Cách A — Người dùng cuối: gói ZIP

1. Tải `cadtroly-0.2.0-vscode-dwg.zip` (trong `dist/`).
2. Nhấp chuột phải → **Extract All…**, chọn nơi dễ nhớ, ví dụ `D:\cadtroly`. Mã chương trình nằm trong thư mục `code`.
3. Nhấp đúp `CAI_DAT.bat`. Nếu Windows hỏi quyền, chọn **Yes**.
4. Chờ tới dòng **CÀI ĐẶT HOÀN TẤT**.

`CAI_DAT.bat` làm các việc:

- Nếu chưa có Python 3.14: tải bản 64-bit từ `python.org`, kiểm tra SHA-256 rồi mới chạy bộ cài.
- Tạo môi trường riêng `code\.venv`, cài gói theo `requirements-mcp.lock` (đúng phiên bản đã kiểm thử), rồi `pip install -e .`.
- Chạy `cadtroly init` để tạo kho người dùng `D:\CAD-kho` (hoặc `%USERPROFILE%\CAD-kho`).

Bộ tiêu chuẩn/quy tắc/skill nền nằm sẵn trong `code\kho-mac-dinh`, MCP đọc trực tiếp, không cần chép. `CAD-kho` chỉ chứa
dữ liệu của bạn: log, Excel, cấu hình và phần bổ sung.

Mở VS Code: **File → Open Folder…** → chọn thư mục `code`. Nếu được hỏi Python interpreter, chọn `.venv\Scripts\python.exe`.
Sau đó sang [2. Kết nối client](2-ket-noi-client.md).

## Cách B — Từ mã nguồn (dev)

```bash
git clone git@github.com:trungthanh-tran/autocad-mcp.git
cd autocad-mcp/app
python -m venv .venv && .venv\Scripts\activate      # Linux/macOS: source .venv/bin/activate
pip install -r requirements-mcp.lock                # tuỳ chọn, để có đúng phiên bản đã kiểm thử
pip install -e .                                    # một bộ phụ thuộc duy nhất, không cần extras
cadtroly init --kho D:\CAD-kho                      # tạo kho + config.json
cadtroly sample                                     # sinh samples/mat-bang-tang-3.dxf để thử
python -m cadtroly.mcp                              # chạy thử server (stdio); Ctrl+C để thoát
```

Khi khởi động, `python -m cadtroly.mcp` tự kiểm tra và **chỉ cài gói còn thiếu** (theo file lock), không cài lại mỗi lần.
Tắt bằng `CADTROLY_AUTO_INSTALL=false` nếu máy bị giới hạn mạng.

## Cập nhật

**Bản ZIP**

1. Đóng VS Code.
2. Đổi tên thư mục `code` cũ thành `code-cu` để dự phòng.
3. Giải nén ZIP mới, rồi nhấp đúp `CAI_DAT.bat` cạnh thư mục `code`.
4. Mở lại VS Code và khởi động lại MCP.

**Bản cài từ GitHub**

```bash
cd app
python -m cadtroly.cli update
```

Lệnh chỉ cập nhật khi code local sạch; nếu có sửa chưa commit, lệnh dừng để không ghi đè.

Không xoá `CAD-kho` khi cập nhật: đó là cấu hình, log, Excel và dữ liệu bổ sung của bạn.

## Gỡ cài đặt

Xoá thư mục cài (`D:\cadtroly`) và mục `cadtroly` trong cấu hình MCP của client. Giữ hoặc xoá `CAD-kho` tuỳ bạn.

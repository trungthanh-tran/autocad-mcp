# Hướng dẫn cài cadtroly MCP cho người dùng cuối

Phiên bản: **cadtroly 0.2.0**.

Tài liệu này dành cho người chỉ cần dùng AutoCAD + VSCode, không cần biết lập
trình.

## A. Chuẩn bị một lần

Trên máy mới, cài ba phần mềm:

1. Python 3.14: tải từ `python.org`, khi cài nhớ chọn **Add Python to PATH**.
2. VSCode: tải từ `code.visualstudio.com`.
3. Extension **Python** của Microsoft trong VSCode.

Nếu muốn MCP sửa bản vẽ trực tiếp trong AutoCAD, máy phải có AutoCAD đã cài.
Nếu không có AutoCAD, MCP vẫn đọc/vẽ DXF; để chuyển DWG cần cài thêm ODA File
Converter.

## B. Cài cadtroly

1. Tải file `cadtroly-0.2.0-vscode.zip`.
2. Nhấp chuột phải → **Extract All…**.
3. Chọn nơi dễ nhớ, ví dụ `D:\cadtroly`.
4. Mở thư mục đã giải nén, vào thư mục `app`.
5. Nhấp đúp file `Cài đặt.bat`.

Chờ đến khi cửa sổ hiện dòng **CÀI ĐẶT HOÀN TẤT**. Nếu Windows hỏi quyền,
chọn **Yes**.

## C. Mở bằng VSCode

1. Mở VSCode.
2. Chọn **File → Open Folder…**.
3. Chọn đúng thư mục `app`.
4. Nếu VSCode hỏi chọn Python interpreter, chọn:
   `.venv\Scripts\python.exe`.

## D. Kết nối MCP

Trong VSCode:

1. Nhấn `Ctrl+Shift+P`.
2. Gõ **MCP: Open User Configuration** rồi chọn mục đó.
3. Dán cấu hình dưới đây.
4. Sửa `D:\cadtroly\app` thành đúng nơi đã giải nén nếu khác.
5. Lưu file.
6. Nhấn `Ctrl+Shift+P` → **MCP: List Servers** → chọn `cadtroly` → **Start**.

```json
{
  "servers": {
    "cadtroly": {
      "type": "stdio",
      "command": "D:\\cadtroly\\app\\.venv\\Scripts\\python.exe",
      "args": ["-m", "cadtroly.mcp"],
      "cwd": "D:\\cadtroly\\app",
      "env": {
        "CADTROLY_KHO": "D:\\CAD-kho",
        "AUTOCAD_MCP_BACKEND": "auto",
        "TOOL_PROFILE": "lean",
        "TOOL_PACKS": "core,arch",
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

## E. Dùng thử

Mở một cuộc trò chuyện trong VSCode và nói:

- “Đọc file PDF này và bóc tách thành DWG.”
- “Mở file DWG này.”
- “Tách layer tường, cột, nội thất và kích thước.”
- “Áp dụng chuẩn layer Việt Nam cho bản vẽ nhà.”
- “Bóc khối lượng bản vẽ này ra Excel.”

Khi cần chọn bộ layer, dùng `vn` cho quy ước Việt Nam hoặc `ncs` cho quy ước
quốc tế. Nếu không xác định được, MCP sẽ hỏi lại, không tự chọn bừa.

## F. Cập nhật phiên bản mới

Khi có ZIP phiên bản mới:

1. Đóng VSCode.
2. Đổi tên thư mục cũ thành `app-cu` để dự phòng.
3. Giải nén ZIP mới thành thư mục `app`.
4. Nhấp đúp `Cài đặt.bat`.
5. Mở lại VSCode và khởi động lại MCP.

Không xóa thư mục `D:\CAD-kho`; đó là nơi lưu cấu hình, tiêu chuẩn, log và file
Excel của người dùng.

## G. Khi gặp lỗi

- MCP không hiện: đóng VSCode, mở lại và chọn **MCP: List Servers → Start**.
- Không thấy AutoCAD: mở AutoCAD trước khi gọi MCP.
- Không đọc được DWG: kiểm tra ODA File Converter hoặc chuyển sang DXF.
- Không cài được: gửi ảnh màn hình lỗi và phiên bản Python cho người quản trị.

Không xóa `.venv`, `D:\CAD-kho` hoặc file DWG/PDF nguồn khi chưa hỏi người quản
trị.

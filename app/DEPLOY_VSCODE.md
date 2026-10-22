# Triển khai cadtroly MCP trên máy khác bằng VSCode

Phiên bản gói: **cadtroly 0.2.0**.

## 1. Cài phần mềm nền

Trên Windows, cài:

- Python 3.11 trở lên, nhớ chọn **Add Python to PATH**.
- Git.
- VSCode và extension Python của Microsoft.
- AutoCAD nếu muốn MCP sửa DWG trực tiếp qua COM.
- ODA File Converter nếu cần đọc/ghi DWG khi không dùng AutoCAD.

AutoCAD và ODA File Converter là phần mềm ngoài Python, không được cài tự động
bởi MCP.

## 2. Giải nén và mở bằng VSCode

Giải nén gói ZIP vào một thư mục không có dấu cách, ví dụ:

```powershell
D:\cadtroly\app
```

Trong VSCode chọn **File → Open Folder…** và mở thư mục `app`.

Mở Terminal trong VSCode và chạy:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-mcp.lock
python -m pip install -e .
```

Nếu PowerShell chặn activate, có thể chạy trực tiếp bằng Python trong môi trường:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-mcp.lock
.\.venv\Scripts\python.exe -m pip install -e .
```

## 3. Kiểm tra cài đặt

```powershell
python -m pytest -q tests
python -c "import version; print(version.__version__)"
```

Kết quả version phải là `0.2.0`.

## 4. Kết nối MCP trong VSCode

Trong VSCode mở Command Palette, chọn **MCP: Open User Configuration** và
thêm server sau. Sửa `cwd` nếu giải nén ở nơi khác:

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

Sau đó chạy **MCP: List Servers**, chọn `cadtroly` và **Start**. Có thể kiểm
tra bằng tool `system_status` hoặc gọi `standards_reference`.

## 5. Cập nhật lần sau

Nếu máy được clone từ GitHub:

```powershell
python -m cadtroly.cli update
```

Lệnh này kéo code mới, cài lại dependency theo lock và báo version. Lệnh dừng
nếu có file local chưa commit để tránh ghi đè.

Nếu chỉ nhận ZIP mới, giải nén bản mới vào thư mục mới rồi cài lại bằng bước 2.

## 6. Chạy MCP thủ công để xem log

```powershell
python -m cadtroly.mcp
```

MCP dùng stdio nên không gõ lệnh vào cửa sổ này; hãy để VSCode/MCP client quản
lý tiến trình. Khi thiếu package, bootstrap sẽ tự cài từ `requirements-mcp.lock`.
Có thể tắt tự cài bằng:

```powershell
$env:CADTROLY_AUTO_INSTALL = "false"
```

## 7. Các lỗi thường gặp

- `No module named cadtroly`: kiểm tra `cwd` là thư mục `app` và dùng Python
  trong `.venv`.
- Không điều khiển được AutoCAD: mở AutoCAD trước và đặt
  `AUTOCAD_MCP_BACKEND=auto` hoặc `com`.
- Không ghi được DWG khi không có AutoCAD: cài ODA File Converter; backend
  `ezdxf` chỉ đảm bảo DXF, không phải DWG native.
- MCP không hiện tool: kiểm tra server đã **Start** và xem log trong VSCode.

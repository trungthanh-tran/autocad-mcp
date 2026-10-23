# 7. Xử lý sự cố

[← Mục lục tài liệu](README.md)

## Kết nối và cài đặt

| Hiện tượng | Cách xử lý |
|---|---|
| MCP không hiện trong client | VS Code: đóng/mở lại, **MCP: List Servers → cadtroly → Start**. Claude Desktop: thoát hẳn rồi mở lại. Kiểm tra JSON hợp lệ và mọi `\` đã viết thành `\\` |
| Server khởi động rồi tắt ngay | Đường dẫn `command`/`cwd` sai, hoặc Python không phải bản trong `.venv`. Chạy thử `"<command>" -m cadtroly.mcp` trong terminal để xem lỗi (log ra stderr) |
| Lần đầu khởi động lâu | Server đang tự cài gói còn thiếu. Máy bị chặn mạng: đặt `CADTROLY_AUTO_INSTALL=false` và cài trước bằng `pip install -r requirements-mcp.lock` |
| Không thấy AutoCAD (backend báo `ezdxf`) | Mở AutoCAD **trước** khi khởi động MCP; dùng `AUTOCAD_MCP_BACKEND=auto` hoặc `com`; khởi động lại server |
| Không đọc được DWG | Cần AutoCAD (COM) hoặc ODA File Converter; hoặc chuyển sang DXF |
| Từ chối mở file | File nằm ngoài `DWG_MCP_ALLOWED_ROOTS`/`ALLOWED_PATHS`, hoặc DXF vượt `MAX_DXF_BYTES` |
| Lệnh treo rồi báo timeout | AutoCAD đang mở hộp thoại hoặc regen lâu. Đóng hộp thoại; tăng `COM_CALL_TIMEOUT` nếu cần |
| Tiếng Việt lỗi font trong kết quả | Đặt `PYTHONIOENCODING=utf-8` |
| Client báo quá nhiều tool | `TOOL_PROFILE=lean` hoặc `DISCOVERY_MODE=search` |
| `CAI_DAT.bat` thất bại | Chụp màn hình cửa sổ lỗi, ghi phiên bản Python, gửi người quản trị |

Không xoá `.venv`, `CAD-kho` hoặc file DWG/PDF nguồn khi chưa hỏi người quản trị.

## LLM làm chưa đúng

Dừng lại và yêu cầu báo trạng thái:

> Dừng lại, không sửa thêm. Hãy báo file đang mở, tool đã dùng, các tham số, lỗi gặp phải và trạng thái file đích.

Hoặc làm lại có kiểm soát:

> Làm lại từ file gốc, giữ nguyên hình học, chỉ sửa layer. Chụp ảnh trước/sau và xuất danh sách đối tượng đã đổi layer.

Nếu đã sửa trong transaction, yêu cầu rollback về checkpoint trước đó.

## Nhật ký

Thao tác của tool ghi JSONL theo ngày tại `CAD-kho/log/YYYY-MM-DD.log`. Gửi file log của ngày gặp lỗi khi báo cho người quản trị.

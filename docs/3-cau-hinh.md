# 3. Cấu hình

[← Mục lục tài liệu](README.md)

MCP được cấu hình bằng **biến môi trường**, đặt trong khối `env` của client (xem [2. Kết nối client](2-ket-noi-client.md)).
Ngoài ra chỉ có `CAD-kho/config.json` cho vài tuỳ chọn AutoCAD.

## Cấu hình khuyến nghị

| Tình huống | Đặt |
|---|---|
| Mặc định, đủ chức năng | `TOOL_PROFILE=full`, `TOOL_PACKS=all`, `AUTOCAD_MCP_BACKEND=auto` |
| Client giới hạn số tool (một số bản Copilot, Cursor) | `TOOL_PROFILE=lean`, `TOOL_PACKS=core,arch`; hoặc `DISCOVERY_MODE=search` |
| Sửa trực tiếp AutoCAD đang mở, chụp ảnh live | Mở AutoCAD trước, `AUTOCAD_MCP_BACKEND=auto` hoặc `com` |
| Máy không có AutoCAD, chỉ DXF | `AUTOCAD_MCP_BACKEND=ezdxf` |
| Khoá MCP vào thư mục dự án | `DWG_MCP_ALLOWED_ROOTS=D:\CAD-kho;D:\DuAn` |
| Máy bị chặn mạng | `CADTROLY_AUTO_INSTALL=false` (cài gói trước bằng file lock) |

## Chọn tool và backend

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `AUTOCAD_MCP_BACKEND` | `auto` | `auto`: COM nếu có AutoCAD đang chạy, không thì ezdxf · `com`: bắt buộc AutoCAD · `ezdxf`: không cần AutoCAD |
| `CAD_PROGID` | `AutoCAD.Application` | ProgID COM, đổi để nối CAD tương thích khác (GstarCAD, ZWCAD…). Chỉ AutoCAD được test |
| `TOOL_PROFILE` | `full` | `full` = mọi tool; `lean` = bộ gọn cho client giới hạn số tool |
| `TOOL_PACKS` | `all` | `all` hoặc danh sách gói, ví dụ `core,arch,pid`. `core` luôn bật |
| `DISCOVERY_MODE` | `off` | `search`: chỉ lộ tool tìm kiếm + `call_tool` proxy, giảm token cho client |
| `ENABLE_3D` | `false` | Bật tool 3D solid (chỉ với backend COM) |

## Kho và an toàn

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `CADTROLY_KHO` | `~/CAD-kho` | Kho người dùng: log, Excel xuất ra, tiêu chuẩn/quy tắc/skill bổ sung |
| `DWG_MCP_ALLOWED_ROOTS` | không giới hạn | Thư mục DWG/PDF được phép đọc/ghi, ngăn cách bằng `;`. Nên đặt |
| `ALLOWED_PATHS` | không giới hạn | Giới hạn đường dẫn mở/lưu của tool upstream, ngăn cách bằng `,` |
| `CADTROLY_APPROVAL` | `auto` | Duyệt thao tác phá huỷ, xem [dưới](#duyệt-thao-tác-phá-huỷ) |
| `DANGEROUS_COMMANDS_ENABLED` | `false` | `true` tắt bộ lọc an toàn cho lệnh/LISP thô. **Không nên bật** |
| `CADTROLY_AUTO_INSTALL` | `true` | Tự cài gói còn thiếu khi khởi động |
| `PYTHONIOENCODING` | — | Đặt `utf-8` để tiếng Việt hiển thị đúng |

## Duyệt thao tác phá huỷ

Xoá đối tượng/layer/layout, phá block, purge, lệnh AutoCAD/LISP thô, đóng bản vẽ, ghi đè file đã có, thay text
hàng loạt, xref (trừ `list`) và `cad_batch` có bước như trên **không chạy** cho tới khi người dùng đồng ý.

| `CADTROLY_APPROVAL` | Cách duyệt |
|---|---|
| `auto` (mặc định) | Client hỗ trợ elicitation → hộp **Đồng ý / Huỷ** hiện thẳng cho người dùng. Không hỗ trợ → như `token` |
| `token` | Tool trả về nội dung sẽ làm + token. LLM phải cho người dùng xem; người dùng đồng ý thì LLM gọi `approval_execute(token)`. Token dùng một lần, hết hạn sau 5 phút, chạy đúng tham số đã xem (LLM không đổi được) |
| `off` | Tắt. Chỉ dùng cho script tự động có kiểm soát |

Lưu file sang đường dẫn mới, tạo/vẽ/sửa thông thường và mọi tool chỉ đọc không cần duyệt. Mọi lần yêu cầu, đồng ý,
từ chối đều ghi vào `CAD-kho/log`.

## Giới hạn, timeout, log

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `MAX_UNDO_STACK` | `5` | Số bước undo của transaction |
| `EZDXF_UNDO_DEPTH` | `0` | Bước undo cho backend ezdxf. 0 = tắt; mỗi bước là một bản chụp DXF, tốn với bản vẽ lớn |
| `MAX_DXF_BYTES` | 512 MB | Từ chối mở DXF lớn hơn. 0 = tắt kiểm tra |
| `MAX_LIST_LIMIT` | `5000` | Trần số phần tử trả về mỗi lần liệt kê |
| `COM_CALL_TIMEOUT` | `60` | Giây tối đa cho một lệnh COM (tránh treo khi AutoCAD bật hộp thoại) |
| `EZDXF_CALL_TIMEOUT` | `120` | Giây tối đa cho một lệnh ezdxf. 0 = tắt |
| `LOG_LEVEL` | `INFO` | Mức log của server (ra stderr) |
| `CADTROLY_LOG` | `WARNING` | Mức log của entry `cadtroly.mcp` |

## Chạy qua HTTP (nâng cao)

Mặc định là stdio. Nếu chạy transport HTTP:

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `ALLOW_REMOTE_HTTP` | `false` | Cho phép bind ngoài loopback |
| `MCP_AUTH_TOKEN` | rỗng | Token client phải gửi kèm |

## `CAD-kho/config.json`

Tạo bởi `cadtroly init`. Mục `acad`:

| Khoá | Mặc định | Ý nghĩa |
|---|---|---|
| `backend` | `auto` | Như `AUTOCAD_MCP_BACKEND` |
| `preview_before_run` | `true` | Xem trước trước khi chạy thay đổi |
| `undo_group_per_run` | `true` | Gom mỗi lần chạy thành một nhóm UNDO |
| `screenshot_after_run` | `true` | Chụp ảnh sau khi chạy |
| `never_autosave` | `true` | Không tự lưu đè bản vẽ |
| `mark_layer` | `_AI_MARK` | Layer dùng để khoanh/đánh dấu |

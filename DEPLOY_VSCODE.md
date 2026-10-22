# Hướng dẫn cài cadtroly MCP cho người dùng cuối

Phiên bản: **cadtroly 0.2.0**.

Tài liệu này dành cho người chỉ cần dùng AutoCAD + VSCode, không cần biết lập
trình.

## A. Chuẩn bị một lần

Trên máy mới, cài hai phần mềm:

1. VSCode: tải từ `code.visualstudio.com`.
2. Extension **Python** của Microsoft trong VSCode.

Không cần cài Python thủ công. `CAI_DAT.bat` sẽ tự tải và cài Python 3.14.9
64-bit từ `python.org` nếu máy chưa có Python 3.14, sau đó kiểm tra SHA-256
trước khi chạy bộ cài.

Nếu muốn MCP sửa bản vẽ trực tiếp trong AutoCAD, máy phải có AutoCAD đã cài.
Nếu không có AutoCAD, MCP vẫn đọc/vẽ DXF; để chuyển DWG cần cài thêm ODA File
Converter.

## B. Cài cadtroly

1. Tải file `cadtroly-0.2.0-vscode-dwg.zip`.
2. Nhấp chuột phải → **Extract All…**.
3. Chọn nơi dễ nhớ, ví dụ `D:\cadtroly`.
4. Mở thư mục đã giải nén; mã chương trình nằm trong thư mục `code`.
5. Nhấp đúp file `CAI_DAT.bat`.

Chờ đến khi cửa sổ hiện dòng **CÀI ĐẶT HOÀN TẤT**. Nếu Windows hỏi quyền,
chọn **Yes**.

Bộ tiêu chuẩn/quy tắc/skill nền đã nằm sẵn trong thư mục MCP tại
`code\kho-mac-dinh`, không cần chép vào `D:\CAD-kho`. MCP đọc trực tiếp bộ này;
`D:\CAD-kho` chỉ dành cho dữ liệu người dùng, log, Excel và phần bổ sung sau này.

## C. Mở bằng VSCode

1. Mở VSCode.
2. Chọn **File → Open Folder…**.
3. Chọn đúng thư mục `code`.
4. Nếu VSCode hỏi chọn Python interpreter, chọn:
   `.venv\Scripts\python.exe`.

## D. Kết nối MCP

Trong VSCode:

1. Nhấn `Ctrl+Shift+P`.
2. Gõ **MCP: Open User Configuration** rồi chọn mục đó.
3. Dán cấu hình dưới đây.
4. Sửa `D:\cadtroly\code` thành đúng nơi đã giải nén nếu khác.
5. Lưu file.
6. Nhấn `Ctrl+Shift+P` → **MCP: List Servers** → chọn `cadtroly` → **Start**.

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
        "TOOL_PROFILE": "lean",
        "TOOL_PACKS": "core,arch",
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

### Giải thích từng trường cấu hình

| Trường | Ý nghĩa | Người dùng có cần sửa không? |
|---|---|---|
| `servers` | Danh sách các MCP server mà VSCode được phép kết nối. | Giữ nguyên. |
| `cadtroly` | Tên server cadtroly; có thể dùng tên khác nhưng nên giữ để dễ nhận biết. | Không cần sửa. |
| `type: "stdio"` | VSCode giao tiếp với MCP qua tiến trình chạy trên chính máy này. | Giữ nguyên. |
| `command` | Đường dẫn Python trong môi trường `.venv` của cadtroly. | Chỉ sửa nếu giải nén ở ổ/thư mục khác. |
| `args` | Lệnh Python yêu cầu chạy module `cadtroly.mcp`. | Giữ nguyên. |
| `cwd` | Thư mục làm việc chính, phải trỏ tới thư mục `code`. | Chỉ sửa nếu đường dẫn khác. |
| `env` | Các thiết lập môi trường gửi cho MCP khi khởi động. | Có thể sửa theo nhu cầu. |
| `CADTROLY_KHO` | Thư mục dữ liệu cá nhân: log, Excel, cấu hình và phần bổ sung. Bộ mặc định vẫn nằm trong MCP. | Có thể đổi, nhưng nên giữ `D:\CAD-kho`. |
| `DWG_MCP_ALLOWED_ROOTS` | Giới hạn thư mục DWG/PDF được MCP phép đọc/ghi; nhiều thư mục ngăn cách bằng dấu `;`. | Nên đặt thư mục dự án. |
| `AUTOCAD_MCP_BACKEND` | Cách MCP kết nối bản vẽ: `auto` tự chọn, `com` dùng AutoCAD đang mở, `ezdxf` chạy không cần AutoCAD. | Nên giữ `auto`. |
| `TOOL_PROFILE` | Số lượng chức năng được hiện ra. `lean` gọn hơn; `full` hiện đầy đủ. | Người mới nên giữ `lean`. |
| `TOOL_PACKS` | Nhóm chức năng được bật. `core,arch` gồm chức năng cơ bản và kiến trúc. | Giữ nguyên; đổi thành `all` khi cần toàn bộ. |
| `PYTHONIOENCODING` | Mã chữ giúp tiếng Việt hiển thị đúng trong giao tiếp MCP. | Giữ nguyên `utf-8`. |

### Chỉ cần sửa hai chỗ khi đổi thư mục

Nếu giải nén vào `E:\PhanMem\cadtroly\code`, sửa:

```json
"command": "E:\\PhanMem\\cadtroly\\code\\.venv\\Scripts\\python.exe",
"cwd": "E:\\PhanMem\\cadtroly\\code"
```

Các dấu `\\` trong JSON là bắt buộc; không đổi thành một dấu `\`.

## E. Dùng thử

Mở một cuộc trò chuyện trong VSCode và nói:

- “Đọc file PDF này và bóc tách thành DWG.”
- “Mở file DWG này.”
- “Tách layer tường, cột, nội thất và kích thước.”
- “Áp dụng chuẩn layer Việt Nam cho bản vẽ nhà.”
- “Bóc khối lượng bản vẽ này ra Excel.”

Khi cần chọn bộ layer, dùng `vn` cho quy ước Việt Nam hoặc `ncs` cho quy ước
quốc tế. Nếu không xác định được, MCP sẽ hỏi lại, không tự chọn bừa.

## E.1. Cách dùng LLM với MCP

LLM là người hiểu yêu cầu và gọi các tool MCP; MCP là lớp thực hiện trong+AutoCAD/DXF. Người dùng không cần nói tên tool, chỉ cần mô tả rõ việc muốn làm.

### Quy trình nên dùng cho mọi lần sửa bản vẽ+
1. **Khoanh phạm vi**: nói tên file, layout, khu vực, trục hoặc handle.
2. **Đọc trước**: yêu cầu LLM đọc units, extents, layer, entity và bản vẽ hiện tại.
3. **Chụp trước**: yêu cầu chụp toàn bản vẽ hoặc một vùng cụ thể.
4. **Nêu thay đổi**: nói rõ đối tượng nào, đổi gì, layer nào, kích thước nào.
5. **Xác nhận trước khi ghi**: với xóa, đổi hàng loạt hoặc ghi đè file, yêu cầu
   LLM liệt kê đối tượng và hỏi lại trước khi thực hiện.
6. **Sửa trong transaction**: nếu có nhiều bước, yêu cầu tạo checkpoint để có
   thể rollback khi kết quả không đúng.
7. **Chụp sau và kiểm tra**: yêu cầu chụp lại đúng vùng, chạy `drawing_diff`,
   `validation_check` hoặc `view_render_report`.
8. **Lưu bản mới**: luôn nói rõ đường dẫn và không ghi đè bản gốc nếu chưa yêu cầu.

### Mẫu câu dùng ngay

```text
Mở file D:\DuAn\mat-bang.dwg. Đọc units, layout, layer và extents trước.
Chụp ảnh toàn bản vẽ trước khi sửa.
```

```text
Trong vùng trục A-B/1-2, tách tường, cửa, nội thất và dimension thành layer
riêng. Không tự đoán các đối tượng không rõ; đưa chúng vào danh sách REVIEW.
Chụp vùng này trước và sau khi sửa, rồi liệt kê handle đã thay đổi.
```

```text
Chỉ sửa khu vực phòng vệ sinh tại tọa độ (x1,y1)-(x2,y2). Đổi tường sang
KT-TUONG, cửa sang KT-CUA, giữ nguyên kích thước. Chụp trước, tạo checkpoint,
sửa, chụp sau, chạy kiểm tra trùng hình học và lưu thành bản mới.
```

```text
Tìm tất cả đối tượng hình học trùng nhau. Chưa xóa gì cả; trả về layer, handle,
tọa độ và đề xuất nhóm nào có thể xóa để tôi xác nhận.
```

```text
Chụp riêng layout A1, vùng mặt bằng tầng 1 và vùng chi tiết vệ sinh. Kiểm tra
preview có type đối tượng nào không được render hoặc cần xem lại thủ công.
```

### Khi muốn sửa từng phần bằng ảnh

- Nói **tên vùng**: “phòng vệ sinh góc Đông Bắc”, “khu trục A-B/1-2”.
- Nếu tên vùng chưa đủ, nói **tọa độ góc** hoặc yêu cầu LLM dùng `view_zoom_window`.
- Nếu cần sửa chính xác, yêu cầu `view_screenshot(overlay_handles=true)` để ảnh
  có handle; sau đó nói “sửa handle `AB12`”.
- Với nhiều khu vực, xử lý từng vùng một và chụp ảnh sau mỗi vùng; không yêu cầu
  sửa cả bản vẽ nếu chưa có bản đồ layer và phạm vi rõ.

### Chọn chế độ kết nối

| Tình huống | Cách dùng |
|---|---|
| Sửa trực tiếp AutoCAD | Mở AutoCAD, dùng `AUTOCAD_MCP_BACKEND=auto` hoặc `com`. |
| Đọc/vẽ DXF không cần AutoCAD | Dùng `AUTOCAD_MCP_BACKEND=ezdxf`. |
| Cần ảnh trước/sau live | Phải dùng backend COM và AutoCAD đang mở. |
| PDF raster hoặc kích thước mờ | Yêu cầu LLM đánh dấu `REVIEW`, không tự suy luận. |

### Quy tắc an toàn khi ra lệnh cho LLM

- Không nói “sửa hết cho đúng” nếu chưa chỉ rõ chuẩn, phạm vi và file đầu ra.
- Không cho phép xóa hàng loạt khi chưa có danh sách handle và ảnh trước.
- Kích thước mâu thuẫn phải được báo lại, không tự chọn số lớn/nhỏ hơn.
- Không coi ảnh preview là bằng chứng đầy đủ nếu `view_render_report` báo thiếu type.
- Sau khi sửa phải yêu cầu báo cáo: file nào, layer nào, handle nào, trước/sau ra sao.

## F. Các chức năng chính

### 1. Đọc PDF và dựng DWG

MCP đọc được PDF bản vẽ có vector, giữ đường nét, chữ, ký hiệu, kích thước và
phân loại thành layer để tiếp tục chỉnh sửa.

Ví dụ:

> Đọc `mat-bang.pdf`, dựng thành DWG A1, giữ kích thước và tách layer tường,
> cột, cửa, nội thất, hatch, text và dimension.

MCP sẽ hỏi lại nếu khổ giấy, tỷ lệ, hướng giấy hoặc hệ tên layer chưa rõ.

### 2. Tách và tổ chức layer

- Nhà: tường, cột, dầm, sàn, cửa, cửa sổ, nội thất, thiết bị, hatch, text,
  kích thước.
- Đường: tim tuyến, mặt đường, lề đường, thoát nước, cấp nước, biển báo,
  hiện trạng, kích thước.
- Cầu: mặt cầu, dầm, trụ, mố, gối cầu, cốt thép, mặt cắt, kích thước.

MCP nhận diện `KT-`, `KC-`, `HT-`, `CAU-` là quy ước Việt Nam; `A-`, `C-`,
`S-` là NCS quốc tế. Nếu không đủ bằng chứng, MCP hỏi lại `vn` hay `ncs`.

### 3. Áp dụng chuẩn tên layer

> Áp dụng chuẩn layer Việt Nam cho bản vẽ nhà.

> Áp dụng chuẩn NCS quốc tế cho bản vẽ cầu.

```text
Việt Nam: KT-TUONG, KC-COT, HT-MATDUONG, CAU-TRU
NCS:      A-WALL, S-DECK, C-ROAD, S-PIER
```

### 4. Vẽ và sửa bản vẽ

MCP có thể vẽ đường, polyline, cung, hình tròn, hatch, text, block, ký hiệu,
dim và khung bản vẽ; đồng thời di chuyển, copy, xoay, scale, trim, fillet,
chamfer, xóa và đổi layer.

> Vẽ thêm vách ngăn dài 3.2 m, đặt vào layer tường, ghi kích thước và lưu thành
> bản mới.

### 5. Bóc khối lượng ra Excel

MCP đọc block, line, polyline, text và layer để đề xuất công tác rồi xuất Excel
có nguồn truy vết. Các kết quả chưa chắc chắn được đánh dấu để người dùng xác
nhận, không tự điền bừa.

> Bóc khối lượng cửa, tường và sàn trong bản vẽ này ra Excel.

### 6. Kiểm tra bản vẽ

MCP có thể kiểm tra layer, kích thước, text, block, đơn vị, phạm vi bản vẽ và
một số quy tắc công ty; kết quả kèm vị trí để dễ tìm và sửa.

> Kiểm tra bản vẽ theo chuẩn công ty và liệt kê các lỗi cần sửa.

### 7. Lưu, xuất và dọn file tạm

MCP có thể lưu DWG/DXF, xuất PDF/ảnh xem trước và dọn thư mục trung gian sau
khi hoàn tất PDF → DWG. File nguồn và file kết quả không tự xóa.

> Chuyển PDF thành DWG, lưu kết quả, xóa DXF và file tạm nhưng giữ PDF nguồn.

### 8. Skill mặc định

Skill nằm trong `code\\kho-mac-dinh\\skill` và được MCP đọc trực tiếp:

- `quan-tri-layer-cad`: tách và quản trị layer.
- `tai-tao-pdf-sang-cad`: dựng PDF thành CAD có thể sửa.
- `annotation-dim-qa`: kiểm tra text, dim, hatch và tỷ lệ.
- `bo-tri-ho-so-thiet-ke`: quản lý tên file, sheet và revision.
- `kiem-tra-ban-ve-civil-bridge`: kiểm tra bản vẽ đường và cầu.
- `bien-phap-thi-cong-vn`: biện pháp thi công Việt Nam.

Tên thư mục kỹ thuật dùng ASCII; nội dung hướng dẫn và trao đổi với người dùng
vẫn bằng tiếng Việt.

## G. Bảng chức năng MCP cho người dùng

| Nhóm | Chức năng | Người dùng có thể nói | Kết quả |
|---|---|---|---|
| Bản vẽ | Đọc bản vẽ | “Đọc file này và cho biết có những layer nào.” | Danh sách layer, block, đối tượng, kích thước và đơn vị. |
| Bản vẽ | PDF → DWG | “Dựng PDF này thành DWG A1.” | File DWG mới, các lớp đường nét và chữ được phân loại. |
| Bản vẽ | Mở/lưu | “Mở file này”, “Lưu thành bản mới.” | Mở bản vẽ, lưu bản sao, không tự ghi đè file gốc nếu chưa yêu cầu. |
| Bản vẽ | Vẽ thêm | “Vẽ tường dài 3 m trên layer tường.” | Đối tượng mới đúng vị trí và layer được yêu cầu. |
| Bản vẽ | Sửa/xóa | “Đổi layer cửa”, “Xóa phần được chọn.” | Chỉnh sửa có thể kiểm tra lại hoặc undo. |
| Layer | Tách layer | “Tách tường, cột, nội thất, dim thành layer riêng.” | Các nhóm layer rõ ràng để bật/tắt, sửa hoặc xóa. |
| Layer | Áp dụng chuẩn | “Dùng chuẩn Việt Nam cho nhà” hoặc “Dùng NCS cho cầu.” | Tạo layer theo `KT/KC/HT/CAU` hoặc `A/C/S`. |
| Layer | Tự nhận diện | “Tự nhận diện chuẩn layer.” | Chỉ tự áp dụng khi đủ bằng chứng; nếu không sẽ hỏi lại. |
| Kiểm tra | Kiểm tra bản vẽ | “Kiểm tra theo chuẩn công ty.” | Danh sách lỗi/cảnh báo, vị trí và đề xuất xử lý. |
| Khối lượng | Đề xuất bóc | “Bóc thử tường, cửa, sàn.” | Nhóm công tác và cách tính dự kiến. |
| Khối lượng | Xác nhận cách tính | “Nhóm này tính theo m2.” | Ghi nhớ lựa chọn cho lần bóc sau. |
| Khối lượng | Xuất Excel | “Xuất khối lượng ra Excel.” | File Excel có tổng hợp, chi tiết và nguồn truy vết. |
| Kho dữ liệu | Tiêu chuẩn/quy tắc | “Liệt kê các bộ tiêu chuẩn đang có.” | Danh sách bộ mặc định trong MCP và bộ người dùng thêm. |
| Kho dữ liệu | Skill | “Đọc skill biện pháp thi công.” | Hướng dẫn chuyên ngành đang được MCP sử dụng. |
| Hệ thống | Trạng thái | “MCP đang chạy bằng AutoCAD hay DXF?” | Backend, version, kho dữ liệu và tình trạng kết nối. |
| Hệ thống | Cập nhật | “Cập nhật MCP.” | Kéo bản mới và cài package theo file lock. |
| Hệ thống | Báo cáo render | “Kiểm tra preview có thiếu đối tượng không.” | Thống kê type đã render và type cần kiểm tra thủ công. |

### Các cột trong bảng Excel khối lượng

| Cột | Ý nghĩa |
|---|---|
| `Công tác` | Tên việc, ví dụ xây tường, cửa, sàn. |
| `Đơn vị` | `m`, `m2`, `m3`, `bộ`, `cái`… |
| `Khối lượng` | Giá trị MCP tính được từ bản vẽ. |
| `Cách tính` | Đếm, chiều dài, diện tích, thể tích hoặc diện tích × chiều cao. |
| `Nguồn` | Layer, block, text hoặc quy tắc đã dùng để tính. |
| `Tin cậy` | `A` = đo/đếm trực tiếp; `B` = suy luận cần kiểm tra; `C` = chưa đủ dữ liệu. |
| `Handle` | Mã đối tượng trong CAD để tìm lại đúng vị trí. |
| `Ghi chú` | Điều kiện thiếu, giả định hoặc việc kỹ sư cần xác nhận. |

### Các mức kết quả kiểm tra

| Mức | Ý nghĩa |
|---|---|
| `Lỗi` | Cần sửa trước khi phát hành bản vẽ. |
| `Cảnh báo` | Có dấu hiệu chưa phù hợp, người dùng kiểm tra lại. |
| `Xác nhận` | MCP không đủ căn cứ kết luận; kỹ sư quyết định. |
| `Đạt` | Không phát hiện vấn đề theo bộ quy tắc đã chọn. |

## H. Cập nhật phiên bản mới

Khi có ZIP phiên bản mới:

1. Đóng VSCode.
2. Đổi tên thư mục cũ thành `code-cu` để dự phòng.
3. Giải nén ZIP mới, giữ thư mục `code` và hai file hướng dẫn ở ngoài.
4. Nhấp đúp `CAI_DAT.bat` ở thư mục ngoài, cạnh thư mục `code`.
5. Mở lại VSCode và khởi động lại MCP.

Không xóa thư mục `D:\CAD-kho`; đó là nơi lưu cấu hình, log, Excel và dữ liệu
bổ sung của người dùng. Bộ mặc định nằm trong thư mục MCP.

## I. Khi gặp lỗi

- MCP không hiện: đóng VSCode, mở lại và chọn **MCP: List Servers → Start**.
- Không thấy AutoCAD: mở AutoCAD trước khi gọi MCP.
- Không đọc được DWG: kiểm tra ODA File Converter hoặc chuyển sang DXF.
- Không cài được: gửi ảnh màn hình lỗi và phiên bản Python cho người quản trị.

Không xóa `.venv`, `D:\CAD-kho` hoặc file DWG/PDF nguồn khi chưa hỏi người quản
trị.

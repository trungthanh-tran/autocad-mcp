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

Lần cài đầu, bộ tiêu chuẩn/quy tắc/skill mẫu được tự động nạp vào
`D:\CAD-kho`: chuẩn vẽ công ty mẫu, QCVN 18:2021/BXD mẫu và skill biện pháp thi
công Việt Nam. Đây là dữ liệu nền đã đi kèm MCP; sau này người quản trị có thể
bổ sung thêm, không làm mất dữ liệu cũ.

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

## G. Cập nhật phiên bản mới

Khi có ZIP phiên bản mới:

1. Đóng VSCode.
2. Đổi tên thư mục cũ thành `app-cu` để dự phòng.
3. Giải nén ZIP mới thành thư mục `app`.
4. Nhấp đúp `Cài đặt.bat`.
5. Mở lại VSCode và khởi động lại MCP.

Không xóa thư mục `D:\CAD-kho`; đó là nơi lưu cấu hình, tiêu chuẩn, log và file
Excel của người dùng.

## H. Khi gặp lỗi

- MCP không hiện: đóng VSCode, mở lại và chọn **MCP: List Servers → Start**.
- Không thấy AutoCAD: mở AutoCAD trước khi gọi MCP.
- Không đọc được DWG: kiểm tra ODA File Converter hoặc chuyển sang DXF.
- Không cài được: gửi ảnh màn hình lỗi và phiên bản Python cho người quản trị.

Không xóa `.venv`, `D:\CAD-kho` hoặc file DWG/PDF nguồn khi chưa hỏi người quản
trị.

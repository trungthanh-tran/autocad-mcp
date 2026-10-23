# 4. Hướng dẫn sử dụng

[← Mục lục tài liệu](README.md) · Trước: [2. Kết nối client](2-ket-noi-client.md) · Tiếp: [5. Kho, tiêu chuẩn, skill](5-kho-tieu-chuan-skill.md)

Bạn không cần biết Python, JSON hay tên tool. Mô tả việc cần làm bằng tiếng Việt trong ô chat; LLM sẽ hiểu, tự chọn tool
(tên tool bằng tiếng Anh, ví dụ `pdf_to_dwg`, `view_screenshot`), tự điền tham số và gọi MCP. MCP mới là phần thật sự đọc/sửa
bản vẽ.

## Bắt đầu nhanh

1. Đã cài và kết nối MCP ([1](1-cai-dat.md), [2](2-ket-noi-client.md)).
2. Muốn sửa trực tiếp trong AutoCAD: mở AutoCAD trước.
3. Đặt file DWG/PDF trong thư mục dự án (thuộc `DWG_MCP_ALLOWED_ROOTS`) hoặc đưa đường dẫn đầy đủ.
4. Gõ yêu cầu. Ví dụ:

> Đọc file `D:\DuAn\mat-bang.pdf`, dựng thành DWG A1 ngang, tách layer tường, cột, cửa, nội thất, kích thước và ghi chú.
> Lưu thành `D:\DuAn\mat-bang_semantic.dwg`. Sau đó kiểm tra lại kích thước và chụp ảnh kết quả.

## Viết yêu cầu tốt

Nên nêu:

- File nguồn và file đích.
- Muốn đọc, kiểm tra, sửa hay tạo mới.
- Khổ giấy, tỷ lệ, đơn vị, hướng giấy nếu liên quan.
- Layer cần tạo hoặc cần giữ nguyên.
- Có được ghi đè file gốc không. Mặc định **không ghi đè**.
- Có muốn chụp ảnh trước/sau, xuất báo cáo không.

Mẫu:

> Làm [công việc] trên file [đường dẫn]. Giữ nguyên file gốc, lưu kết quả vào [đường dẫn đích]. Dùng đơn vị [mm/m],
> khổ [A1/A3], tách layer [danh sách]. Kiểm tra [nội dung] và báo lỗi trước khi kết thúc.

## Quy trình cho mọi lần sửa bản vẽ

1. **Khoanh phạm vi** — tên file, layout, khu vực, trục hoặc handle.
2. **Đọc trước** — units, extents, layer, entity.
3. **Chụp trước** — toàn bản vẽ hoặc một vùng.
4. **Nêu thay đổi** — đối tượng nào, đổi gì, layer nào, kích thước nào.
5. **Xác nhận trước khi ghi** — với xoá, đổi hàng loạt, ghi đè: yêu cầu LLM liệt kê đối tượng và hỏi lại.
6. **Sửa trong transaction** — nhiều bước thì tạo checkpoint để rollback được.
7. **Chụp sau và kiểm tra** — chụp lại đúng vùng, chạy `drawing_diff`, `validation_check`, `view_render_report`.
8. **Lưu bản mới** — nói rõ đường dẫn.

```text
Mở D:\DuAn\mat-bang.dwg, đọc units, layout, layer và extents trước. Chụp vùng trục A-B/1-2.
Tách tường, cửa và dimension thành layer riêng. Không đoán đối tượng mờ; đưa vào danh sách REVIEW.
Tạo checkpoint, sửa, chụp lại, báo handle đã đổi và lưu thành bản mới.
```

### Sửa từng phần bằng ảnh

- Nói **tên vùng**: "phòng vệ sinh góc Đông Bắc", "khu trục A-B/1-2".
- Chưa đủ thì nói **toạ độ góc**, hoặc yêu cầu LLM dùng `view_zoom_window`.
- Cần chính xác: yêu cầu ảnh có handle (`view_screenshot` với `overlay_handles=true`), rồi nói "sửa handle `AB12`".
- Nhiều khu vực: xử lý từng vùng, chụp sau mỗi vùng.

## Công việc thường dùng

| Công việc | Mẫu câu |
|---|---|
| PDF → DWG | Chuyển `D:\DuAn\sheet.pdf` sang `D:\DuAn\sheet.dwg`. Khổ A1, đúng hướng bản vẽ, tách layer kiến trúc, giữ đủ text và kích thước. Chụp trước và sau. |
| Đọc, thống kê | Đọc `D:\DuAn\existing.dwg`, thống kê đối tượng và layer, xác định tường, cột, cửa, nội thất, dim, text. Không sửa file. |
| Tách layer | Tách thành `A-WALL`, `A-COLS`, `A-DOOR`, `A-FURN`, `A-DIMS`, `A-TEXT`, `A-HATCH`. Chưa rõ chuẩn Việt Nam hay quốc tế thì hỏi tôi. |
| Áp dụng chuẩn layer | Áp dụng chuẩn layer Việt Nam cho bản vẽ nhà. / Áp dụng chuẩn NCS quốc tế cho bản vẽ cầu. |
| Sửa bản vẽ | Mở `plan.dwg`, chụp hiện trạng, sửa các dim sai và đưa cửa về đúng layer. Lưu `plan_fixed.dwg`, chụp sau, báo danh sách thay đổi. |
| Kiểm tra | Kiểm tra theo chuẩn kiến trúc: layer, đơn vị, tỷ lệ, text, dim, đối tượng trùng, đường hở, khung tên. Phân loại Error/Warning/Info. Không tự sửa. |
| Bóc khối lượng | Bóc tường, cửa, sàn, thiết bị. Hiện công thức, đơn vị, layer nguồn, độ tin cậy; đối tượng không chắc đưa vào danh sách cần xác nhận. Xuất Excel. |
| Vẽ mới | Vẽ mặt bằng WC 3500 x 5200 mm, tường 200 mm, bố trí thiết bị, dim và text, layer kiến trúc, khung A1, lưu DWG mới. |
| Cơ khí, P&ID | Tạo bản vẽ cơ khí/P&ID theo mô tả, dùng layer và ký hiệu đúng ngành. Chưa có tiêu chuẩn thì hỏi trước. |
| Dọn dẹp | Tìm đối tượng hình học trùng nhau. Chưa xoá; trả layer, handle, toạ độ và đề xuất nhóm nên xoá để tôi xác nhận. |
| Lưu, dọn file tạm | Chuyển PDF thành DWG, lưu kết quả, xoá DXF và file tạm nhưng giữ PDF nguồn. |
| Kết cấu, PCCC | Kiểm tra sơ bộ lối thoát nạn, cửa thoát, hành lang, cầu thang, ký hiệu PCCC. Thiếu tiêu chuẩn hoặc số người thì hỏi, không tự điền. |

Chuẩn layer: `KT-`, `KC-`, `HT-`, `CAU-` là quy ước Việt Nam (`vn`); `A-`, `C-`, `S-` là NCS quốc tế (`ncs`). Không đủ bằng
chứng thì MCP hỏi lại, không chọn bừa.

```text
Việt Nam: KT-TUONG, KC-COT, HT-MATDUONG, CAU-TRU
NCS:      A-WALL,   S-DECK, C-ROAD,      S-PIER
```

## Chụp ảnh

> Chụp ảnh toàn bản vẽ trước và sau khi sửa.

> Chụp riêng vùng mặt bằng tầng 1, vùng khung tên và vùng kích thước bên phải.

LLM phải báo file ảnh, vùng chụp và thay đổi quan sát được. Ảnh chỉ là bằng chứng trực quan; kích thước và QA vẫn kiểm bằng
dữ liệu CAD. Nếu `view_render_report` báo có loại đối tượng không render được, phải kiểm tra lại trong AutoCAD.

Ảnh live trước/sau cần backend COM và AutoCAD đang mở.

## An toàn

- Luôn lưu sang file mới khi chưa kiểm tra kết quả.
- Không nói "sửa hết cho đúng" khi chưa chỉ rõ chuẩn, phạm vi và file đầu ra.
- Không cho xoá hàng loạt khi chưa có danh sách handle và ảnh trước.
- Kích thước mâu thuẫn phải được báo lại, không tự chọn số lớn/nhỏ hơn.
- PDF raster hoặc kích thước mờ: yêu cầu đánh dấu `REVIEW`, không suy luận.
- Có `Error` thì dừng phát hành cho tới khi xử lý hoặc xác nhận ngoại lệ.
- Kết cấu, chịu lực, PCCC, an toàn công trình: kết quả chỉ là rà soát hỗ trợ; kỹ sư có thẩm quyền phải phê duyệt.

## Báo cáo kết thúc nên có

Yêu cầu LLM trả về:

- File nguồn và file kết quả.
- Số đối tượng/layer đã xử lý, thay đổi chính, handle đã đổi.
- Error, Warning, Info.
- Ảnh trước/sau nếu đã yêu cầu.
- Phần chưa chắc chắn cần kỹ sư xác nhận.

## Tra cứu thêm

- Mọi chức năng theo ngành, kèm câu lệnh mẫu: [6. Danh mục chức năng](6-danh-muc-chuc-nang.md).
- Tiêu chuẩn, skill, bóc khối lượng, mức kết quả: [5. Kho, tiêu chuẩn, skill](5-kho-tieu-chuan-skill.md).
- LLM làm sai: [7. Xử lý sự cố](7-xu-ly-su-co.md#llm-làm-chưa-đúng).

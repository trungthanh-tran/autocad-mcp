# Hướng dẫn sử dụng MCP CAD cho người dùng

Tài liệu này dành cho người dùng cuối làm việc qua VS Code và LLM. Bạn không cần biết Python, JSON hay cách MCP hoạt động bên trong. Chỉ cần mô tả việc cần làm bằng tiếng Việt.

## 1. Bắt đầu nhanh

1. Mở VS Code tại thư mục project.
2. Chạy `CAI_DAT.bat` một lần nếu máy chưa được cài đặt.
3. Kết nối MCP `cadtroly` trong VS Code.
4. Đặt file DWG/PDF vào thư mục dự án hoặc cung cấp đường dẫn đầy đủ.
5. Gõ yêu cầu rõ ràng cho LLM.

Ví dụ:

> Đọc file `D:\DuAn\mat-bang.pdf`, dựng thành DWG A1 ngang, tách layer tường, cột, cửa, nội thất, kích thước và ghi chú. Lưu thành `D:\DuAn\mat-bang_semantic.dwg`. Sau đó kiểm tra lại kích thước và chụp ảnh kết quả.

LLM sẽ tự chọn tool phù hợp. Không cần tự gõ tên tool, trừ khi bạn muốn kiểm soát chính xác.

## 2. Cách viết yêu cầu tốt

Trong yêu cầu nên nêu:

- File nguồn và file đích.
- Muốn đọc, kiểm tra, sửa hay tạo mới.
- Khổ giấy, tỷ lệ, đơn vị và hướng giấy nếu liên quan.
- Layer cần tạo hoặc cần giữ nguyên.
- Có được ghi đè file gốc hay không. Mặc định nên **không ghi đè**.
- Muốn chụp ảnh trước/sau hoặc xuất báo cáo hay không.

Mẫu câu:

> Làm [công việc] trên file [đường dẫn]. Giữ nguyên file gốc, lưu kết quả vào [đường dẫn đích]. Dùng đơn vị [mm/m], khổ [A1/A3], tách layer [danh sách]. Kiểm tra [nội dung] và báo lỗi trước khi kết thúc.

## 3. Các công việc thường dùng

### PDF sang DWG

> Chuyển `D:\DuAn\sheet.pdf` sang `D:\DuAn\sheet.dwg`. Dùng khổ A1, đúng hướng bản vẽ, tách layer kiến trúc hợp lý, giữ đầy đủ text và kích thước. Chụp ảnh trước và sau.

Tool chính: `pdf_to_dwg`. File trung gian được tạo trong vùng tạm riêng và tự xóa sau khi DWG được lưu.

### Đọc và bóc tách DWG

> Đọc `D:\DuAn\existing.dwg`, thống kê đối tượng và layer, xác định tường, cột, cửa, nội thất, dim và text. Không sửa file. Xuất báo cáo khối lượng.

### Tách layer

> Tách file thành các layer rõ ràng: `A-WALL`, `A-COLS`, `A-DOOR`, `A-FURN`, `A-DIMS`, `A-TEXT`, `A-HATCH`. Không tự đoán tiêu chuẩn layer; nếu chưa rõ dùng quốc tế hay Việt Nam thì hỏi tôi trước.

### Sửa bản vẽ

> Mở file `D:\DuAn\plan.dwg`, chụp ảnh hiện trạng, sửa các dim bị sai và đưa cửa về đúng layer. Lưu bản mới thành `plan_fixed.dwg`, chụp ảnh sau sửa và báo danh sách thay đổi.

### Kiểm tra bản vẽ

> Kiểm tra file theo tiêu chuẩn kiến trúc: layer, đơn vị, tỷ lệ, text, dim, đối tượng trùng, đường hở và khung tên. Phân loại kết quả thành Error, Warning và Info. Không tự sửa khi chưa hỏi.

### Bóc tách khối lượng

> Bóc tách tường, cửa, sàn và thiết bị từ file DWG. Hiển thị công thức, đơn vị, layer nguồn và độ tin cậy. Các đối tượng không chắc chắn phải đưa vào danh sách cần xác nhận.

### Vẽ mới

> Vẽ mặt bằng phòng vệ sinh 3500 x 5200 mm, tường 200 mm, bố trí thiết bị theo mô tả, tạo dim và text, dùng layer kiến trúc, khung A1 và lưu thành file DWG mới.

### Cơ khí và P&ID

> Tạo bản vẽ cơ khí/P&ID theo mô tả, dùng layer và ký hiệu phù hợp ngành. Nếu tiêu chuẩn hoặc phiên bản chưa được chỉ định, hỏi lại trước khi vẽ.

## 4. Chụp ảnh và kiểm tra thay đổi

Bạn có thể yêu cầu:

> Chụp ảnh toàn bản vẽ trước và sau khi sửa.

Hoặc:

> Chụp riêng vùng mặt bằng tầng 1, vùng khung tên và vùng kích thước bên phải.

LLM cần báo rõ file ảnh, vùng chụp và những thay đổi quan sát được. Ảnh chỉ là bằng chứng trực quan; kích thước và kết quả QA vẫn phải được kiểm tra bằng dữ liệu CAD.

## 5. Tiêu chuẩn và ngành

MCP có danh sách ngành và bộ tiêu chuẩn trong kho cấu hình. Có thể yêu cầu:

> Liệt kê các ngành và tiêu chuẩn đang có.

> Dùng tiêu chuẩn kiến trúc Việt Nam cho lần kiểm tra này.

> Kiểm tra tiêu chuẩn P&ID đang bật, không tự thêm tiêu chuẩn mới.

Nếu có nhiều lựa chọn hoặc chưa xác định được quốc tế hay Việt Nam, MCP phải hỏi lại; không được tự điền bừa.

Các nhóm ngành hiện có gồm kiến trúc, kết cấu, cầu đường, cơ khí, điện, HVAC, P&ID, cấp thoát nước, PCCC, plant, hạ tầng và các nhóm kỹ thuật liên quan.

## 6. An toàn khi thao tác

- Luôn yêu cầu lưu sang file mới khi chưa kiểm tra kết quả.
- Không cho phép ghi đè file gốc nếu không thật sự cần.
- Với thao tác xóa, yêu cầu LLM liệt kê đối tượng và hỏi xác nhận trước.
- Với kết cấu, chịu lực, PCCC và an toàn công trình, kết quả MCP chỉ là kiểm tra hỗ trợ; kỹ sư có thẩm quyền phải phê duyệt.
- Nếu backend AutoCAD không kết nối, yêu cầu kiểm tra trạng thái trước; không xem việc tạo DXF tạm là kết quả DWG cuối cùng.
- Khi có `Error`, dừng phát hành bản vẽ cho đến khi xử lý hoặc xác nhận ngoại lệ.

## 7. Nếu LLM làm chưa đúng

Gửi yêu cầu bổ sung theo mẫu:

> Dừng lại, không sửa thêm. Hãy báo file đang mở, tool đã dùng, các tham số, lỗi gặp phải và trạng thái file đích.

Hoặc:

> Làm lại từ file gốc, giữ nguyên hình học, chỉ sửa layer. Chụp ảnh trước/sau và xuất danh sách đối tượng đã đổi layer.

## 8. Xem danh sách tool đầy đủ

File [MCP-TOOL-USAGE.md](MCP-TOOL-USAGE.md) là tài liệu kỹ thuật; file này chỉ dành cho enduser và tập trung vào câu lệnh gõ vào LLM.

Người dùng cuối thường không cần gọi trực tiếp tên tool. Chỉ dùng danh sách này khi cần kiểm tra LLM đã chọn đúng chức năng hoặc muốn yêu cầu một tool cụ thể.

## 9. Báo cáo kết thúc nên có

Sau mỗi công việc, yêu cầu MCP/LLM trả về:

- File nguồn và file kết quả.
- Số lượng đối tượng/layer đã xử lý.
- Các thay đổi chính.
- Error, Warning và Info.
- Ảnh trước/sau nếu đã yêu cầu.
- Các phần chưa chắc chắn cần kỹ sư xác nhận.

<!-- GENERATED-ALL-TOOLS -->

## Danh sách đầy đủ tất cả tool

Bảng này gồm **272 tool** đang đăng ký, bao gồm cả **247 tool nền tảng** và tool mở rộng của cadtroly. Bạn có thể nói tên tool trong yêu cầu nếu muốn gọi trực tiếp.

| Tên chức năng | Nhóm | Làm gì | Dùng khi nào | Ví dụ câu gõ vào LLM |
|---|---|---|---|---|
| `analysis_bounding_box` | phân tích | Thực hiện thao tác phân tích giới hạn khung trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | Đọc bản vẽ và báo cáo phân tích giới hạn khung; không sửa file gốc. |
| `analysis_entity_stats` | phân tích | Thực hiện thao tác phân tích đối tượng thống kê trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | Đọc bản vẽ và báo cáo phân tích đối tượng thống kê; không sửa file gốc. |
| `analysis_find_in_region` | phân tích | Thực hiện thao tác phân tích tìm trong vùng trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | Đọc bản vẽ và báo cáo phân tích tìm trong vùng; không sửa file gốc. |
| `analysis_layer_stats` | phân tích | Thực hiện thao tác phân tích lớp thống kê trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | Đọc bản vẽ và báo cáo phân tích lớp thống kê; không sửa file gốc. |
| `analysis_list_properties` | phân tích | Thực hiện thao tác phân tích liệt kê thuộc tính trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | Đọc bản vẽ và báo cáo phân tích liệt kê thuộc tính; không sửa file gốc. |
| `analysis_measure_area` | phân tích | Thực hiện thao tác phân tích đo diện tích trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | Đọc bản vẽ và báo cáo phân tích đo diện tích; không sửa file gốc. |
| `analysis_measure_distance` | phân tích | Thực hiện thao tác phân tích đo khoảng cách trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | Đọc bản vẽ và báo cáo phân tích đo khoảng cách; không sửa file gốc. |
| `analysis_measure_entity` | phân tích | Thực hiện thao tác phân tích đo đối tượng trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | Đọc bản vẽ và báo cáo phân tích đo đối tượng; không sửa file gốc. |
| `analysis_select_by_layer` | phân tích | Thực hiện thao tác phân tích chọn theo lớp trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | Đọc bản vẽ và báo cáo phân tích chọn theo lớp; không sửa file gốc. |
| `analysis_select_by_type` | phân tích | Thực hiện thao tác phân tích chọn theo type trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | Đọc bản vẽ và báo cáo phân tích chọn theo type; không sửa file gốc. |
| `arch_catalogue_insert` | kiến trúc | Thực hiện thao tác arch catalogue chèn trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | Trên mặt bằng kiến trúc, hãy arch catalogue chèn và giữ đúng tỷ lệ bản vẽ. |
| `arch_catalogue_list` | kiến trúc | Thực hiện thao tác arch catalogue liệt kê trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | Trên mặt bằng kiến trúc, hãy arch catalogue liệt kê và giữ đúng tỷ lệ bản vẽ. |
| `arch_dimension_chains` | kiến trúc | Thực hiện thao tác arch kích thước chains trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | Trên mặt bằng kiến trúc, hãy arch kích thước chains và giữ đúng tỷ lệ bản vẽ. |
| `arch_grid` | kiến trúc | Thực hiện thao tác arch grid trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | Trên mặt bằng kiến trúc, hãy arch grid và giữ đúng tỷ lệ bản vẽ. |
| `arch_opening` | kiến trúc | Thực hiện thao tác arch opening trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | Trên mặt bằng kiến trúc, hãy arch opening và giữ đúng tỷ lệ bản vẽ. |
| `arch_plan_from_spec` | kiến trúc | Thực hiện thao tác arch mặt bằng từ spec trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | Trên mặt bằng kiến trúc, hãy arch mặt bằng từ spec và giữ đúng tỷ lệ bản vẽ. |
| `arch_room` | kiến trúc | Thực hiện thao tác arch room trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | Trên mặt bằng kiến trúc, hãy arch room và giữ đúng tỷ lệ bản vẽ. |
| `arch_rooms_detect` | kiến trúc | Thực hiện thao tác arch rooms detect trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | Trên mặt bằng kiến trúc, hãy arch rooms detect và giữ đúng tỷ lệ bản vẽ. |
| `arch_schedule` | kiến trúc | Thực hiện thao tác arch schedule trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | Trên mặt bằng kiến trúc, hãy arch schedule và giữ đúng tỷ lệ bản vẽ. |
| `arch_stair` | kiến trúc | Thực hiện thao tác arch stair trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | Trên mặt bằng kiến trúc, hãy arch stair và giữ đúng tỷ lệ bản vẽ. |
| `arch_symbol` | kiến trúc | Thực hiện thao tác arch ký hiệu trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | Trên mặt bằng kiến trúc, hãy arch ký hiệu và giữ đúng tỷ lệ bản vẽ. |
| `arch_wall` | kiến trúc | Thực hiện thao tác arch wall trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | Trên mặt bằng kiến trúc, hãy arch wall và giữ đúng tỷ lệ bản vẽ. |
| `balloon_add` | tờ bản vẽ | Thực hiện thao tác balloon add trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | Chuẩn bị tờ bản vẽ phát hành và thực hiện balloon add trong khung tên. |
| `batch_plot` | thiết lập trang | Thực hiện thao tác hàng loạt plot trong bản vẽ CAD. | Khi cần khổ giấy, tỷ lệ và in ấn. | Thiết lập khổ A1, tỷ lệ 1:100 rồi thực hiện hàng loạt plot để chuẩn bị phát hành. |
| `block_create_from_entities` | khối | Thực hiện thao tác khối tạo từ đối tượng trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. | Trong bản vẽ hiện tại, hãy khối tạo từ đối tượng cho các khối cửa và thiết bị. |
| `block_define` | khối | Thực hiện thao tác khối định nghĩa trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. | Trong bản vẽ hiện tại, hãy khối định nghĩa cho các khối cửa và thiết bị. |
| `block_explode` | khối | Thực hiện thao tác khối phá khối trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. | Trong bản vẽ hiện tại, hãy khối phá khối cho các khối cửa và thiết bị. |
| `block_find_references` | khối | Thực hiện thao tác khối tìm tham chiếu trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. | Trong bản vẽ hiện tại, hãy khối tìm tham chiếu cho các khối cửa và thiết bị. |
| `block_get_attributes` | khối | Thực hiện thao tác khối get attributes trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. | Trong bản vẽ hiện tại, hãy khối get attributes cho các khối cửa và thiết bị. |
| `block_insert` | khối | Thực hiện thao tác khối chèn trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. | Trong bản vẽ hiện tại, hãy khối chèn cho các khối cửa và thiết bị. |
| `block_list` | khối | Thực hiện thao tác khối liệt kê trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. | Trong bản vẽ hiện tại, hãy khối liệt kê cho các khối cửa và thiết bị. |
| `block_set_attributes` | khối | Thực hiện thao tác khối đặt attributes trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. | Trong bản vẽ hiện tại, hãy khối đặt attributes cho các khối cửa và thiết bị. |
| `bom_extract` | tờ bản vẽ | Thực hiện thao tác bom extract trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | Chuẩn bị tờ bản vẽ phát hành và thực hiện bom extract trong khung tên. |
| `bom_table` | tờ bản vẽ | Thực hiện thao tác bom bảng trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | Chuẩn bị tờ bản vẽ phát hành và thực hiện bom bảng trong khung tên. |
| `boundary_from_entities` | phân tích | Thực hiện thao tác boundary từ đối tượng trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | Đọc bản vẽ và báo cáo boundary từ đối tượng; không sửa file gốc. |
| `boundary_trace` | phân tích | Thực hiện thao tác boundary trace trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | Đọc bản vẽ và báo cáo boundary trace; không sửa file gốc. |
| `cable_takeoff` | nhà máy | Thực hiện thao tác cable takeoff trong bản vẽ CAD. | Khi cần bố trí thiết bị nhà máy. | Trong bản vẽ nhà máy, hãy cable takeoff và kiểm tra khoảng cách an toàn thiết bị. |
| `cad_batch` | xử lý hàng loạt | Thực hiện thao tác cad hàng loạt trong bản vẽ CAD. | Khi cần xử lý hàng loạt. | Thực hiện cad hàng loạt cho tất cả bản vẽ trong thư mục dự án và báo cáo từng file. |
| `centre_marks` | cơ khí | Thực hiện thao tác centre marks trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | Trên bản vẽ cơ khí, hãy centre marks theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn. |
| `check_rulesets` | mở rộng cadtroly | Thực hiện thao tác kiểm tra rulesets trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện kiểm tra rulesets trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `check_run` | mở rộng cadtroly | Thực hiện thao tác kiểm tra run trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện kiểm tra run trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `construction_clear` | nâng cao | Thực hiện thao tác construction clear trong bản vẽ CAD. | Khi cần chức năng nâng cao. | Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện construction clear nếu backend cho phép. |
| `construction_xline` | nâng cao | Thực hiện thao tác construction xline trong bản vẽ CAD. | Khi cần chức năng nâng cao. | Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện construction xline nếu backend cho phép. |
| `data_extract` | tờ bản vẽ | Thực hiện thao tác dữ liệu extract trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | Chuẩn bị tờ bản vẽ phát hành và thực hiện dữ liệu extract trong khung tên. |
| `datum_feature` | kỹ thuật | Thực hiện thao tác datum feature trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo datum feature thành lỗi hoặc cảnh báo. |
| `dimension_aligned` | kích thước | Thực hiện thao tác kích thước aligned trong bản vẽ CAD. | Khi cần kích thước và ghi chú đo. | Kiểm tra và thực hiện kích thước aligned cho các kích thước của mặt bằng tầng 1. |
| `dimension_angular` | kích thước | Thực hiện thao tác kích thước angular trong bản vẽ CAD. | Khi cần kích thước và ghi chú đo. | Kiểm tra và thực hiện kích thước angular cho các kích thước của mặt bằng tầng 1. |
| `dimension_auto` | nâng cao | Thực hiện thao tác kích thước auto trong bản vẽ CAD. | Khi cần chức năng nâng cao. | Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện kích thước auto nếu backend cho phép. |
| `dimension_diameter` | kích thước | Thực hiện thao tác kích thước diameter trong bản vẽ CAD. | Khi cần kích thước và ghi chú đo. | Kiểm tra và thực hiện kích thước diameter cho các kích thước của mặt bằng tầng 1. |
| `dimension_linear` | kích thước | Thực hiện thao tác kích thước linear trong bản vẽ CAD. | Khi cần kích thước và ghi chú đo. | Kiểm tra và thực hiện kích thước linear cho các kích thước của mặt bằng tầng 1. |
| `dimension_radius` | kích thước | Thực hiện thao tác kích thước radius trong bản vẽ CAD. | Khi cần kích thước và ghi chú đo. | Kiểm tra và thực hiện kích thước radius cho các kích thước của mặt bằng tầng 1. |
| `dimstyle_create` | kiểu hiển thị | Thực hiện thao tác dimstyle tạo trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | Kiểm tra kiểu hiển thị hiện tại và thực hiện dimstyle tạo cho toàn bộ bản vẽ. |
| `dimstyle_list` | kiểu hiển thị | Thực hiện thao tác dimstyle liệt kê trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | Kiểm tra kiểu hiển thị hiện tại và thực hiện dimstyle liệt kê cho toàn bộ bản vẽ. |
| `dimstyle_modify` | kiểu hiển thị | Thực hiện thao tác dimstyle sửa trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | Kiểm tra kiểu hiển thị hiện tại và thực hiện dimstyle sửa cho toàn bộ bản vẽ. |
| `dimstyle_set_current` | kiểu hiển thị | Thực hiện thao tác dimstyle đặt hiện tại trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | Kiểm tra kiểu hiển thị hiện tại và thực hiện dimstyle đặt hiện tại cho toàn bộ bản vẽ. |
| `document_activate` | môi trường | Thực hiện thao tác document activate trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo document activate trước khi thao tác bản vẽ. |
| `document_close` | môi trường | Thực hiện thao tác document đóng trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo document đóng trước khi thao tác bản vẽ. |
| `document_list` | môi trường | Thực hiện thao tác document liệt kê trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo document liệt kê trước khi thao tác bản vẽ. |
| `drawing_apply_discipline_standard` | mở rộng cadtroly | Thực hiện thao tác bản vẽ apply discipline standard trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện bản vẽ apply discipline standard trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `drawing_apply_iso_layers` | nâng cao | Thực hiện thao tác bản vẽ apply iso layers trong bản vẽ CAD. | Khi cần chức năng nâng cao. | Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện bản vẽ apply iso layers nếu backend cho phép. |
| `drawing_apply_standard` | kiểu hiển thị | Thực hiện thao tác bản vẽ apply standard trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | Kiểm tra kiểu hiển thị hiện tại và thực hiện bản vẽ apply standard cho toàn bộ bản vẽ. |
| `drawing_audit` | bản vẽ | Thực hiện thao tác bản vẽ audit trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | Mở bản vẽ, thực hiện bản vẽ audit, sau đó lưu ra file mới và không ghi đè file gốc. |
| `drawing_close` | bản vẽ | Thực hiện thao tác bản vẽ đóng trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | Mở bản vẽ, thực hiện bản vẽ đóng, sau đó lưu ra file mới và không ghi đè file gốc. |
| `drawing_critique` | nâng cao | Thực hiện thao tác bản vẽ critique trong bản vẽ CAD. | Khi cần chức năng nâng cao. | Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện bản vẽ critique nếu backend cho phép. |
| `drawing_deliver` | kỹ thuật | Thực hiện thao tác bản vẽ deliver trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo bản vẽ deliver thành lỗi hoặc cảnh báo. |
| `drawing_diff` | đọc hiểu | Thực hiện thao tác bản vẽ diff trong bản vẽ CAD. | Khi cần đọc hiểu cấu trúc bản vẽ. | Đọc hiểu bản vẽ và giải thích bản vẽ diff bằng ngôn ngữ dễ hiểu cho người dùng. |
| `drawing_entities` | mở rộng cadtroly | Thực hiện thao tác bản vẽ đối tượng trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện bản vẽ đối tượng trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `drawing_export_dwg` | tờ bản vẽ | Thực hiện thao tác bản vẽ xuất dwg trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | Chuẩn bị tờ bản vẽ phát hành và thực hiện bản vẽ xuất dwg trong khung tên. |
| `drawing_export_dxf` | bản vẽ | Thực hiện thao tác bản vẽ xuất dxf trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | Mở bản vẽ, thực hiện bản vẽ xuất dxf, sau đó lưu ra file mới và không ghi đè file gốc. |
| `drawing_export_pdf` | bản vẽ | Thực hiện thao tác bản vẽ xuất pdf trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | Mở bản vẽ, thực hiện bản vẽ xuất pdf, sau đó lưu ra file mới và không ghi đè file gốc. |
| `drawing_finalize` | kỹ thuật | Thực hiện thao tác bản vẽ finalize trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo bản vẽ finalize thành lỗi hoặc cảnh báo. |
| `drawing_info` | tra cứu đối tượng | Thực hiện thao tác bản vẽ info trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. | Tìm các đối tượng liên quan rồi báo cáo bản vẽ info, không thay đổi hình học. |
| `drawing_new` | bản vẽ | Thực hiện thao tác bản vẽ new trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | Mở bản vẽ, thực hiện bản vẽ new, sau đó lưu ra file mới và không ghi đè file gốc. |
| `drawing_open` | bản vẽ | Thực hiện thao tác bản vẽ mở trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | Mở bản vẽ, thực hiện bản vẽ mở, sau đó lưu ra file mới và không ghi đè file gốc. |
| `drawing_plan` | nâng cao | Thực hiện thao tác bản vẽ mặt bằng trong bản vẽ CAD. | Khi cần chức năng nâng cao. | Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện bản vẽ mặt bằng nếu backend cho phép. |
| `drawing_preflight` | nâng cao | Thực hiện thao tác bản vẽ preflight trong bản vẽ CAD. | Khi cần chức năng nâng cao. | Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện bản vẽ preflight nếu backend cho phép. |
| `drawing_properties_get` | môi trường | Thực hiện thao tác bản vẽ thuộc tính get trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo bản vẽ thuộc tính get trước khi thao tác bản vẽ. |
| `drawing_properties_set` | môi trường | Thực hiện thao tác bản vẽ thuộc tính đặt trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo bản vẽ thuộc tính đặt trước khi thao tác bản vẽ. |
| `drawing_purge` | bản vẽ | Thực hiện thao tác bản vẽ dọn dẹp trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | Mở bản vẽ, thực hiện bản vẽ dọn dẹp, sau đó lưu ra file mới và không ghi đè file gốc. |
| `drawing_read` | mở rộng cadtroly | Thực hiện thao tác bản vẽ đọc trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện bản vẽ đọc trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `drawing_redo` | bản vẽ | Thực hiện thao tác bản vẽ redo trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | Mở bản vẽ, thực hiện bản vẽ redo, sau đó lưu ra file mới và không ghi đè file gốc. |
| `drawing_refine` | nâng cao | Thực hiện thao tác bản vẽ refine trong bản vẽ CAD. | Khi cần chức năng nâng cao. | Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện bản vẽ refine nếu backend cho phép. |
| `drawing_save` | bản vẽ | Thực hiện thao tác bản vẽ lưu trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | Mở bản vẽ, thực hiện bản vẽ lưu, sau đó lưu ra file mới và không ghi đè file gốc. |
| `drawing_save_as` | bản vẽ | Thực hiện thao tác bản vẽ lưu as trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | Mở bản vẽ, thực hiện bản vẽ lưu as, sau đó lưu ra file mới và không ghi đè file gốc. |
| `drawing_scale_check` | đọc hiểu | Thực hiện thao tác bản vẽ tỷ lệ kiểm tra trong bản vẽ CAD. | Khi cần đọc hiểu cấu trúc bản vẽ. | Đọc hiểu bản vẽ và giải thích bản vẽ tỷ lệ kiểm tra bằng ngôn ngữ dễ hiểu cho người dùng. |
| `drawing_settings` | hệ thống | Thực hiện thao tác bản vẽ thiết lập trong bản vẽ CAD. | Khi cần trạng thái máy chủ. | Báo cáo trạng thái MCP, AutoCAD và backend bằng cách bản vẽ thiết lập. |
| `drawing_template_list` | thiết lập trang | Thực hiện thao tác bản vẽ mẫu liệt kê trong bản vẽ CAD. | Khi cần khổ giấy, tỷ lệ và in ấn. | Thiết lập khổ A1, tỷ lệ 1:100 rồi thực hiện bản vẽ mẫu liệt kê để chuẩn bị phát hành. |
| `drawing_template_save` | thiết lập trang | Thực hiện thao tác bản vẽ mẫu lưu trong bản vẽ CAD. | Khi cần khổ giấy, tỷ lệ và in ấn. | Thiết lập khổ A1, tỷ lệ 1:100 rồi thực hiện bản vẽ mẫu lưu để chuẩn bị phát hành. |
| `drawing_topology_check` | đọc hiểu | Thực hiện thao tác bản vẽ topology kiểm tra trong bản vẽ CAD. | Khi cần đọc hiểu cấu trúc bản vẽ. | Đọc hiểu bản vẽ và giải thích bản vẽ topology kiểm tra bằng ngôn ngữ dễ hiểu cho người dùng. |
| `drawing_understand` | đọc hiểu | Thực hiện thao tác bản vẽ understand trong bản vẽ CAD. | Khi cần đọc hiểu cấu trúc bản vẽ. | Đọc hiểu bản vẽ và giải thích bản vẽ understand bằng ngôn ngữ dễ hiểu cho người dùng. |
| `drawing_undo` | bản vẽ | Thực hiện thao tác bản vẽ undo trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | Mở bản vẽ, thực hiện bản vẽ undo, sau đó lưu ra file mới và không ghi đè file gốc. |
| `entity_array_polar` | sửa đối tượng | Thực hiện thao tác đối tượng array polar trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | Chụp ảnh trước, thực hiện đối tượng array polar, chụp ảnh sau và liệt kê các đối tượng đã đổi. |
| `entity_array_rectangular` | sửa đối tượng | Thực hiện thao tác đối tượng array rectangular trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | Chụp ảnh trước, thực hiện đối tượng array rectangular, chụp ảnh sau và liệt kê các đối tượng đã đổi. |
| `entity_batch_create` | xử lý hàng loạt | Thực hiện thao tác đối tượng hàng loạt tạo trong bản vẽ CAD. | Khi cần xử lý hàng loạt. | Thực hiện đối tượng hàng loạt tạo cho tất cả bản vẽ trong thư mục dự án và báo cáo từng file. |
| `entity_batch_modify` | xử lý hàng loạt | Thực hiện thao tác đối tượng hàng loạt sửa trong bản vẽ CAD. | Khi cần xử lý hàng loạt. | Thực hiện đối tượng hàng loạt sửa cho tất cả bản vẽ trong thư mục dự án và báo cáo từng file. |
| `entity_chamfer` | corner_ops | Thực hiện thao tác đối tượng chamfer trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Hãy thực hiện đối tượng chamfer trên bản vẽ và báo cáo kết quả. |
| `entity_change_space` | bố cục | Thực hiện thao tác đối tượng change space trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | Thiết lập bố cục A1 và thực hiện đối tượng change space cho khung tên và khung nhìn. |
| `entity_copy` | sửa đối tượng | Thực hiện thao tác đối tượng sao chép trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | Chụp ảnh trước, thực hiện đối tượng sao chép, chụp ảnh sau và liệt kê các đối tượng đã đổi. |
| `entity_create_arc` | tạo đối tượng | Thực hiện thao tác đối tượng tạo cung trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | Vẽ thêm đối tượng cần thiết để đối tượng tạo cung, đặt đúng lớp bản vẽ và ghi chú rõ ràng. |
| `entity_create_block_ref` | khối | Thực hiện thao tác đối tượng tạo khối ref trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. | Trong bản vẽ hiện tại, hãy đối tượng tạo khối ref cho các khối cửa và thiết bị. |
| `entity_create_circle` | tạo đối tượng | Thực hiện thao tác đối tượng tạo đường tròn trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | Vẽ thêm đối tượng cần thiết để đối tượng tạo đường tròn, đặt đúng lớp bản vẽ và ghi chú rõ ràng. |
| `entity_create_ellipse` | tạo đối tượng | Thực hiện thao tác đối tượng tạo ellipse trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | Vẽ thêm đối tượng cần thiết để đối tượng tạo ellipse, đặt đúng lớp bản vẽ và ghi chú rõ ràng. |
| `entity_create_hatch` | tạo đối tượng | Thực hiện thao tác đối tượng tạo tô mặt trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | Vẽ thêm đối tượng cần thiết để đối tượng tạo tô mặt, đặt đúng lớp bản vẽ và ghi chú rõ ràng. |
| `entity_create_line` | tạo đối tượng | Thực hiện thao tác đối tượng tạo đường trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | Vẽ thêm đối tượng cần thiết để đối tượng tạo đường, đặt đúng lớp bản vẽ và ghi chú rõ ràng. |
| `entity_create_mtext` | tạo đối tượng | Thực hiện thao tác đối tượng tạo mtext trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | Vẽ thêm đối tượng cần thiết để đối tượng tạo mtext, đặt đúng lớp bản vẽ và ghi chú rõ ràng. |
| `entity_create_point` | tạo đối tượng | Thực hiện thao tác đối tượng tạo điểm trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | Vẽ thêm đối tượng cần thiết để đối tượng tạo điểm, đặt đúng lớp bản vẽ và ghi chú rõ ràng. |
| `entity_create_polyline` | tạo đối tượng | Thực hiện thao tác đối tượng tạo đa tuyến trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | Vẽ thêm đối tượng cần thiết để đối tượng tạo đa tuyến, đặt đúng lớp bản vẽ và ghi chú rõ ràng. |
| `entity_create_rectangle` | tạo đối tượng | Thực hiện thao tác đối tượng tạo hình chữ nhật trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | Vẽ thêm đối tượng cần thiết để đối tượng tạo hình chữ nhật, đặt đúng lớp bản vẽ và ghi chú rõ ràng. |
| `entity_create_revcloud` | tạo đối tượng | Thực hiện thao tác đối tượng tạo revcloud trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | Vẽ thêm đối tượng cần thiết để đối tượng tạo revcloud, đặt đúng lớp bản vẽ và ghi chú rõ ràng. |
| `entity_create_spline` | tạo đối tượng | Thực hiện thao tác đối tượng tạo spline trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | Vẽ thêm đối tượng cần thiết để đối tượng tạo spline, đặt đúng lớp bản vẽ và ghi chú rõ ràng. |
| `entity_create_table` | tạo đối tượng | Thực hiện thao tác đối tượng tạo bảng trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | Vẽ thêm đối tượng cần thiết để đối tượng tạo bảng, đặt đúng lớp bản vẽ và ghi chú rõ ràng. |
| `entity_create_text` | tạo đối tượng | Thực hiện thao tác đối tượng tạo chữ trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | Vẽ thêm đối tượng cần thiết để đối tượng tạo chữ, đặt đúng lớp bản vẽ và ghi chú rõ ràng. |
| `entity_create_wipeout` | tạo đối tượng | Thực hiện thao tác đối tượng tạo wipeout trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | Vẽ thêm đối tượng cần thiết để đối tượng tạo wipeout, đặt đúng lớp bản vẽ và ghi chú rõ ràng. |
| `entity_delete` | sửa đối tượng | Thực hiện thao tác đối tượng xóa trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | Chụp ảnh trước, thực hiện đối tượng xóa, chụp ảnh sau và liệt kê các đối tượng đã đổi. |
| `entity_delete_many` | sửa đối tượng | Thực hiện thao tác đối tượng xóa many trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | Chụp ảnh trước, thực hiện đối tượng xóa many, chụp ảnh sau và liệt kê các đối tượng đã đổi. |
| `entity_edit_geometry` | sửa đối tượng | Thực hiện thao tác đối tượng edit geometry trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | Chụp ảnh trước, thực hiện đối tượng edit geometry, chụp ảnh sau và liệt kê các đối tượng đã đổi. |
| `entity_edit_text` | sửa đối tượng | Thực hiện thao tác đối tượng edit chữ trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | Chụp ảnh trước, thực hiện đối tượng edit chữ, chụp ảnh sau và liệt kê các đối tượng đã đổi. |
| `entity_extend` | corner_ops | Thực hiện thao tác đối tượng kéo dài trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Hãy thực hiện đối tượng kéo dài trên bản vẽ và báo cáo kết quả. |
| `entity_fillet` | corner_ops | Thực hiện thao tác đối tượng fillet trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Hãy thực hiện đối tượng fillet trên bản vẽ và báo cáo kết quả. |
| `entity_get` | tra cứu đối tượng | Thực hiện thao tác đối tượng get trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. | Tìm các đối tượng liên quan rồi báo cáo đối tượng get, không thay đổi hình học. |
| `entity_get_xdata` | tra cứu đối tượng | Thực hiện thao tác đối tượng get xdata trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. | Tìm các đối tượng liên quan rồi báo cáo đối tượng get xdata, không thay đổi hình học. |
| `entity_list` | tra cứu đối tượng | Thực hiện thao tác đối tượng liệt kê trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. | Tìm các đối tượng liên quan rồi báo cáo đối tượng liệt kê, không thay đổi hình học. |
| `entity_mirror` | sửa đối tượng | Thực hiện thao tác đối tượng đối xứng trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | Chụp ảnh trước, thực hiện đối tượng đối xứng, chụp ảnh sau và liệt kê các đối tượng đã đổi. |
| `entity_move` | sửa đối tượng | Thực hiện thao tác đối tượng di chuyển trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | Chụp ảnh trước, thực hiện đối tượng di chuyển, chụp ảnh sau và liệt kê các đối tượng đã đổi. |
| `entity_offset` | sửa đối tượng | Thực hiện thao tác đối tượng song song trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | Chụp ảnh trước, thực hiện đối tượng song song, chụp ảnh sau và liệt kê các đối tượng đã đổi. |
| `entity_rotate` | sửa đối tượng | Thực hiện thao tác đối tượng xoay trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | Chụp ảnh trước, thực hiện đối tượng xoay, chụp ảnh sau và liệt kê các đối tượng đã đổi. |
| `entity_scale` | sửa đối tượng | Thực hiện thao tác đối tượng tỷ lệ trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | Chụp ảnh trước, thực hiện đối tượng tỷ lệ, chụp ảnh sau và liệt kê các đối tượng đã đổi. |
| `entity_select_smart` | nâng cao | Thực hiện thao tác đối tượng chọn smart trong bản vẽ CAD. | Khi cần chức năng nâng cao. | Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện đối tượng chọn smart nếu backend cho phép. |
| `entity_set_properties` | sửa đối tượng | Thực hiện thao tác đối tượng đặt thuộc tính trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | Chụp ảnh trước, thực hiện đối tượng đặt thuộc tính, chụp ảnh sau và liệt kê các đối tượng đã đổi. |
| `entity_set_xdata` | sửa đối tượng | Thực hiện thao tác đối tượng đặt xdata trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | Chụp ảnh trước, thực hiện đối tượng đặt xdata, chụp ảnh sau và liệt kê các đối tượng đã đổi. |
| `entity_trim` | corner_ops | Thực hiện thao tác đối tượng cắt trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Hãy thực hiện đối tượng cắt trên bản vẽ và báo cáo kết quả. |
| `gd_frame` | kỹ thuật | Thực hiện thao tác gd frame trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo gd frame thành lỗi hoặc cảnh báo. |
| `gear_draw_helical_front_view` | kỹ thuật | Thực hiện thao tác gear draw helical front góc nhìn trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo gear draw helical front góc nhìn thành lỗi hoặc cảnh báo. |
| `gear_draw_section_aa` | kỹ thuật | Thực hiện thao tác gear draw mặt cắt aa trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo gear draw mặt cắt aa thành lỗi hoặc cảnh báo. |
| `gear_draw_spur_front_view` | kỹ thuật | Thực hiện thao tác gear draw spur front góc nhìn trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo gear draw spur front góc nhìn thành lỗi hoặc cảnh báo. |
| `hatch_add_boundary` | tạo đối tượng | Thực hiện thao tác tô mặt add boundary trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | Vẽ thêm đối tượng cần thiết để tô mặt add boundary, đặt đúng lớp bản vẽ và ghi chú rõ ràng. |
| `hatch_edit` | tạo đối tượng | Thực hiện thao tác tô mặt edit trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | Vẽ thêm đối tượng cần thiết để tô mặt edit, đặt đúng lớp bản vẽ và ghi chú rõ ràng. |
| `hatch_material` | cơ khí | Thực hiện thao tác tô mặt material trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | Trên bản vẽ cơ khí, hãy tô mặt material theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn. |
| `hatch_set_gradient` | tạo đối tượng | Thực hiện thao tác tô mặt đặt gradient trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | Vẽ thêm đối tượng cần thiết để tô mặt đặt gradient, đặt đúng lớp bản vẽ và ghi chú rõ ràng. |
| `image_attach` | tờ bản vẽ | Thực hiện thao tác hình ảnh đính kèm trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | Chuẩn bị tờ bản vẽ phát hành và thực hiện hình ảnh đính kèm trong khung tên. |
| `keyway_draw_keyed_bore` | kỹ thuật | Thực hiện thao tác keyway draw keyed bore trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo keyway draw keyed bore thành lỗi hoặc cảnh báo. |
| `keyway_draw_section` | kỹ thuật | Thực hiện thao tác keyway draw mặt cắt trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo keyway draw mặt cắt thành lỗi hoặc cảnh báo. |
| `kho_industries` | mở rộng cadtroly | Thực hiện thao tác kho industries trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện kho industries trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `kho_rules_export` | mở rộng cadtroly | Thực hiện thao tác kho rules xuất trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện kho rules xuất trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `kho_rules_import` | mở rộng cadtroly | Thực hiện thao tác kho rules nhập trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện kho rules nhập trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `kho_skill_add` | mở rộng cadtroly | Thực hiện thao tác kho skill add trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện kho skill add trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `kho_skill_toggle` | mở rộng cadtroly | Thực hiện thao tác kho skill toggle trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện kho skill toggle trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `kho_skills` | mở rộng cadtroly | Thực hiện thao tác kho skills trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện kho skills trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `kho_standard_add` | mở rộng cadtroly | Thực hiện thao tác kho standard add trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện kho standard add trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `kho_standard_delete` | mở rộng cadtroly | Thực hiện thao tác kho standard xóa trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện kho standard xóa trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `kho_standards` | mở rộng cadtroly | Thực hiện thao tác kho standards trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện kho standards trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `kho_status` | mở rộng cadtroly | Thực hiện thao tác kho trạng thái trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện kho trạng thái trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `layer_create` | lớp bản vẽ | Thực hiện thao tác lớp tạo trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp tạo, không tự đổi tiêu chuẩn nếu chưa hỏi. |
| `layer_delete` | lớp bản vẽ | Thực hiện thao tác lớp xóa trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp xóa, không tự đổi tiêu chuẩn nếu chưa hỏi. |
| `layer_freeze` | lớp bản vẽ | Thực hiện thao tác lớp freeze trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp freeze, không tự đổi tiêu chuẩn nếu chưa hỏi. |
| `layer_hide` | lớp bản vẽ | Thực hiện thao tác lớp hide trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp hide, không tự đổi tiêu chuẩn nếu chưa hỏi. |
| `layer_isolate` | lớp bản vẽ | Thực hiện thao tác lớp isolate trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp isolate, không tự đổi tiêu chuẩn nếu chưa hỏi. |
| `layer_list` | lớp bản vẽ | Thực hiện thao tác lớp liệt kê trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp liệt kê, không tự đổi tiêu chuẩn nếu chưa hỏi. |
| `layer_lock` | lớp bản vẽ | Thực hiện thao tác lớp khóa trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp khóa, không tự đổi tiêu chuẩn nếu chưa hỏi. |
| `layer_modify` | lớp bản vẽ | Thực hiện thao tác lớp sửa trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp sửa, không tự đổi tiêu chuẩn nếu chưa hỏi. |
| `layer_set_current` | lớp bản vẽ | Thực hiện thao tác lớp đặt hiện tại trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp đặt hiện tại, không tự đổi tiêu chuẩn nếu chưa hỏi. |
| `layer_show` | lớp bản vẽ | Thực hiện thao tác lớp show trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp show, không tự đổi tiêu chuẩn nếu chưa hỏi. |
| `layer_state_delete` | môi trường | Thực hiện thao tác lớp state xóa trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo lớp state xóa trước khi thao tác bản vẽ. |
| `layer_state_list` | môi trường | Thực hiện thao tác lớp state liệt kê trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo lớp state liệt kê trước khi thao tác bản vẽ. |
| `layer_state_restore` | môi trường | Thực hiện thao tác lớp state restore trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo lớp state restore trước khi thao tác bản vẽ. |
| `layer_state_save` | môi trường | Thực hiện thao tác lớp state lưu trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo lớp state lưu trước khi thao tác bản vẽ. |
| `layer_thaw` | lớp bản vẽ | Thực hiện thao tác lớp thaw trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp thaw, không tự đổi tiêu chuẩn nếu chưa hỏi. |
| `layer_unlock` | lớp bản vẽ | Thực hiện thao tác lớp unlock trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp unlock, không tự đổi tiêu chuẩn nếu chưa hỏi. |
| `layout_copy` | bố cục | Thực hiện thao tác bố cục sao chép trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | Thiết lập bố cục A1 và thực hiện bố cục sao chép cho khung tên và khung nhìn. |
| `layout_create` | bố cục | Thực hiện thao tác bố cục tạo trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | Thiết lập bố cục A1 và thực hiện bố cục tạo cho khung tên và khung nhìn. |
| `layout_delete` | bố cục | Thực hiện thao tác bố cục xóa trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | Thiết lập bố cục A1 và thực hiện bố cục xóa cho khung tên và khung nhìn. |
| `layout_list` | bố cục | Thực hiện thao tác bố cục liệt kê trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | Thiết lập bố cục A1 và thực hiện bố cục liệt kê cho khung tên và khung nhìn. |
| `layout_rename` | bố cục | Thực hiện thao tác bố cục đổi tên trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | Thiết lập bố cục A1 và thực hiện bố cục đổi tên cho khung tên và khung nhìn. |
| `layout_set_current` | bố cục | Thực hiện thao tác bố cục đặt hiện tại trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | Thiết lập bố cục A1 và thực hiện bố cục đặt hiện tại cho khung tên và khung nhìn. |
| `leader_create_mleader` | tạo đối tượng | Thực hiện thao tác đường dẫn tạo mleader trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | Vẽ thêm đối tượng cần thiết để đường dẫn tạo mleader, đặt đúng lớp bản vẽ và ghi chú rõ ràng. |
| `linetype_list` | lớp bản vẽ | Thực hiện thao tác linetype liệt kê trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | Tổ chức các đối tượng theo lớp bản vẽ bằng cách linetype liệt kê, không tự đổi tiêu chuẩn nếu chưa hỏi. |
| `linetype_load` | lớp bản vẽ | Thực hiện thao tác linetype nạp trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | Tổ chức các đối tượng theo lớp bản vẽ bằng cách linetype nạp, không tự đổi tiêu chuẩn nếu chưa hỏi. |
| `mech_dimension_part` | cơ khí | Thực hiện thao tác mech kích thước part trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | Trên bản vẽ cơ khí, hãy mech kích thước part theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn. |
| `mech_hole_pattern` | cơ khí | Thực hiện thao tác mech hole pattern trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | Trên bản vẽ cơ khí, hãy mech hole pattern theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn. |
| `mech_part_draw` | cơ khí | Thực hiện thao tác mech part draw trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | Trên bản vẽ cơ khí, hãy mech part draw theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn. |
| `mech_part_from_spec` | cơ khí | Thực hiện thao tác mech part từ spec trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | Trên bản vẽ cơ khí, hãy mech part từ spec theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn. |
| `mech_part_inspect` | cơ khí | Thực hiện thao tác mech part inspect trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | Trên bản vẽ cơ khí, hãy mech part inspect theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn. |
| `mech_view_add` | cơ khí | Thực hiện thao tác mech góc nhìn add trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | Trên bản vẽ cơ khí, hãy mech góc nhìn add theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn. |
| `mleaderstyle_create` | kiểu hiển thị | Thực hiện thao tác mleaderstyle tạo trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | Kiểm tra kiểu hiển thị hiện tại và thực hiện mleaderstyle tạo cho toàn bộ bản vẽ. |
| `mleaderstyle_list` | kiểu hiển thị | Thực hiện thao tác mleaderstyle liệt kê trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | Kiểm tra kiểu hiển thị hiện tại và thực hiện mleaderstyle liệt kê cho toàn bộ bản vẽ. |
| `page_setup_apply` | thiết lập trang | Thực hiện thao tác trang cài đặt apply trong bản vẽ CAD. | Khi cần khổ giấy, tỷ lệ và in ấn. | Thiết lập khổ A1, tỷ lệ 1:100 rồi thực hiện trang cài đặt apply để chuẩn bị phát hành. |
| `page_setup_list` | thiết lập trang | Thực hiện thao tác trang cài đặt liệt kê trong bản vẽ CAD. | Khi cần khổ giấy, tỷ lệ và in ấn. | Thiết lập khổ A1, tỷ lệ 1:100 rồi thực hiện trang cài đặt liệt kê để chuẩn bị phát hành. |
| `pdf_to_dwg` | mở rộng cadtroly | Thực hiện thao tác pdf đến dwg trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện pdf đến dwg trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `pdf_vectorize` | mở rộng cadtroly | Thực hiện thao tác pdf vectorize trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện pdf vectorize trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `pid_equipment_list` | P&ID | Thực hiện thao tác P&ID equipment liệt kê trong bản vẽ CAD. | Khi cần sơ đồ P&ID. | Trên sơ đồ P&ID, hãy P&ID equipment liệt kê và kiểm tra ký hiệu, đường ống cùng nhãn thiết bị. |
| `pid_from_spec` | P&ID | Thực hiện thao tác P&ID từ spec trong bản vẽ CAD. | Khi cần sơ đồ P&ID. | Trên sơ đồ P&ID, hãy P&ID từ spec và kiểm tra ký hiệu, đường ống cùng nhãn thiết bị. |
| `pid_graph` | P&ID | Thực hiện thao tác P&ID graph trong bản vẽ CAD. | Khi cần sơ đồ P&ID. | Trên sơ đồ P&ID, hãy P&ID graph và kiểm tra ký hiệu, đường ống cùng nhãn thiết bị. |
| `pid_instrument_index` | P&ID | Thực hiện thao tác P&ID instrument index trong bản vẽ CAD. | Khi cần sơ đồ P&ID. | Trên sơ đồ P&ID, hãy P&ID instrument index và kiểm tra ký hiệu, đường ống cùng nhãn thiết bị. |
| `pid_line_draw` | P&ID | Thực hiện thao tác P&ID đường draw trong bản vẽ CAD. | Khi cần sơ đồ P&ID. | Trên sơ đồ P&ID, hãy P&ID đường draw và kiểm tra ký hiệu, đường ống cùng nhãn thiết bị. |
| `pid_line_list` | P&ID | Thực hiện thao tác P&ID đường liệt kê trong bản vẽ CAD. | Khi cần sơ đồ P&ID. | Trên sơ đồ P&ID, hãy P&ID đường liệt kê và kiểm tra ký hiệu, đường ống cùng nhãn thiết bị. |
| `pid_symbol_insert` | P&ID | Thực hiện thao tác P&ID ký hiệu chèn trong bản vẽ CAD. | Khi cần sơ đồ P&ID. | Trên sơ đồ P&ID, hãy P&ID ký hiệu chèn và kiểm tra ký hiệu, đường ống cùng nhãn thiết bị. |
| `pid_symbol_list` | P&ID | Thực hiện thao tác P&ID ký hiệu liệt kê trong bản vẽ CAD. | Khi cần sơ đồ P&ID. | Trên sơ đồ P&ID, hãy P&ID ký hiệu liệt kê và kiểm tra ký hiệu, đường ống cùng nhãn thiết bị. |
| `pid_tag_parse` | P&ID | Thực hiện thao tác P&ID tag parse trong bản vẽ CAD. | Khi cần sơ đồ P&ID. | Trên sơ đồ P&ID, hãy P&ID tag parse và kiểm tra ký hiệu, đường ống cùng nhãn thiết bị. |
| `pipe_takeoff` | nhà máy | Thực hiện thao tác pipe takeoff trong bản vẽ CAD. | Khi cần bố trí thiết bị nhà máy. | Trong bản vẽ nhà máy, hãy pipe takeoff và kiểm tra khoảng cách an toàn thiết bị. |
| `plot_style_list` | thiết lập trang | Thực hiện thao tác plot kiểu liệt kê trong bản vẽ CAD. | Khi cần khổ giấy, tỷ lệ và in ấn. | Thiết lập khổ A1, tỷ lệ 1:100 rồi thực hiện plot kiểu liệt kê để chuẩn bị phát hành. |
| `point_from_snap` | nâng cao | Thực hiện thao tác điểm từ snap trong bản vẽ CAD. | Khi cần chức năng nâng cao. | Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện điểm từ snap nếu backend cho phép. |
| `point_intersection` | nâng cao | Thực hiện thao tác điểm intersection trong bản vẽ CAD. | Khi cần chức năng nâng cao. | Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện điểm intersection nếu backend cho phép. |
| `point_tangent` | nâng cao | Thực hiện thao tác điểm tangent trong bản vẽ CAD. | Khi cần chức năng nâng cao. | Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện điểm tangent nếu backend cho phép. |
| `revision_add` | tờ bản vẽ | Thực hiện thao tác revision add trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | Chuẩn bị tờ bản vẽ phát hành và thực hiện revision add trong khung tên. |
| `section_line` | cơ khí | Thực hiện thao tác mặt cắt đường trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | Trên bản vẽ cơ khí, hãy mặt cắt đường theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn. |
| `selection_filter` | tra cứu đối tượng | Thực hiện thao tác selection filter trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. | Tìm các đối tượng liên quan rồi báo cáo selection filter, không thay đổi hình học. |
| `selection_get` | tra cứu đối tượng | Thực hiện thao tác selection get trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. | Tìm các đối tượng liên quan rồi báo cáo selection get, không thay đổi hình học. |
| `selection_polygon` | tra cứu đối tượng | Thực hiện thao tác selection đa giác trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. | Tìm các đối tượng liên quan rồi báo cáo selection đa giác, không thay đổi hình học. |
| `selection_window` | tra cứu đối tượng | Thực hiện thao tác selection window trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. | Tìm các đối tượng liên quan rồi báo cáo selection window, không thay đổi hình học. |
| `sheet_frame` | tờ bản vẽ | Thực hiện thao tác tờ bản vẽ frame trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | Chuẩn bị tờ bản vẽ phát hành và thực hiện tờ bản vẽ frame trong khung tên. |
| `solid_boolean` | khối đặc | Thực hiện thao tác khối đặc boolean trong bản vẽ CAD. | Khi cần hình học ba chiều và khối đặc. | Kiểm tra hình học ba chiều rồi thực hiện khối đặc boolean; không làm hỏng đối tượng gốc. |
| `solid_box` | khối đặc | Thực hiện thao tác khối đặc khung trong bản vẽ CAD. | Khi cần hình học ba chiều và khối đặc. | Kiểm tra hình học ba chiều rồi thực hiện khối đặc khung; không làm hỏng đối tượng gốc. |
| `solid_cylinder` | khối đặc | Thực hiện thao tác khối đặc cylinder trong bản vẽ CAD. | Khi cần hình học ba chiều và khối đặc. | Kiểm tra hình học ba chiều rồi thực hiện khối đặc cylinder; không làm hỏng đối tượng gốc. |
| `solid_extrude` | khối đặc | Thực hiện thao tác khối đặc extrude trong bản vẽ CAD. | Khi cần hình học ba chiều và khối đặc. | Kiểm tra hình học ba chiều rồi thực hiện khối đặc extrude; không làm hỏng đối tượng gốc. |
| `solid_revolve` | khối đặc | Thực hiện thao tác khối đặc revolve trong bản vẽ CAD. | Khi cần hình học ba chiều và khối đặc. | Kiểm tra hình học ba chiều rồi thực hiện khối đặc revolve; không làm hỏng đối tượng gốc. |
| `standards_reference` | mở rộng cadtroly | Thực hiện thao tác standards tham chiếu trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện standards tham chiếu trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `std_feature_draw` | cơ khí | Thực hiện thao tác std feature draw trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | Trên bản vẽ cơ khí, hãy std feature draw theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn. |
| `std_part_insert` | cơ khí | Thực hiện thao tác std part chèn trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | Trên bản vẽ cơ khí, hãy std part chèn theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn. |
| `std_part_list` | cơ khí | Thực hiện thao tác std part liệt kê trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | Trên bản vẽ cơ khí, hãy std part liệt kê theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn. |
| `structural_qa` | mở rộng cadtroly | Thực hiện thao tác structural qa trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện structural qa trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `surface_texture` | cơ khí | Thực hiện thao tác surface texture trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | Trên bản vẽ cơ khí, hãy surface texture theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn. |
| `system_about` | hệ thống | Thực hiện thao tác hệ thống thông tin trong bản vẽ CAD. | Khi cần trạng thái máy chủ. | Báo cáo trạng thái MCP, AutoCAD và backend bằng cách hệ thống thông tin. |
| `system_capabilities` | tra cứu đối tượng | Thực hiện thao tác hệ thống capabilities trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. | Tìm các đối tượng liên quan rồi báo cáo hệ thống capabilities, không thay đổi hình học. |
| `system_get_variable` | hệ thống | Thực hiện thao tác hệ thống get variable trong bản vẽ CAD. | Khi cần trạng thái máy chủ. | Báo cáo trạng thái MCP, AutoCAD và backend bằng cách hệ thống get variable. |
| `system_launch` | môi trường | Thực hiện thao tác hệ thống launch trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo hệ thống launch trước khi thao tác bản vẽ. |
| `system_preferences_get` | môi trường | Thực hiện thao tác hệ thống preferences get trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo hệ thống preferences get trước khi thao tác bản vẽ. |
| `system_preferences_set` | môi trường | Thực hiện thao tác hệ thống preferences đặt trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo hệ thống preferences đặt trước khi thao tác bản vẽ. |
| `system_prompt_message` | môi trường | Thực hiện thao tác hệ thống prompt message trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo hệ thống prompt message trước khi thao tác bản vẽ. |
| `system_run_command` | hệ thống | Thực hiện thao tác hệ thống run command trong bản vẽ CAD. | Khi cần trạng thái máy chủ. | Báo cáo trạng thái MCP, AutoCAD và backend bằng cách hệ thống run command. |
| `system_run_lisp` | hệ thống | Thực hiện thao tác hệ thống run lisp trong bản vẽ CAD. | Khi cần trạng thái máy chủ. | Báo cáo trạng thái MCP, AutoCAD và backend bằng cách hệ thống run lisp. |
| `system_set_variable` | hệ thống | Thực hiện thao tác hệ thống đặt variable trong bản vẽ CAD. | Khi cần trạng thái máy chủ. | Báo cáo trạng thái MCP, AutoCAD và backend bằng cách hệ thống đặt variable. |
| `system_status` | hệ thống | Thực hiện thao tác hệ thống trạng thái trong bản vẽ CAD. | Khi cần trạng thái máy chủ. | Báo cáo trạng thái MCP, AutoCAD và backend bằng cách hệ thống trạng thái. |
| `system_variable_describe` | môi trường | Thực hiện thao tác hệ thống variable describe trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo hệ thống variable describe trước khi thao tác bản vẽ. |
| `takeoff_compute` | mở rộng cadtroly | Thực hiện thao tác takeoff compute trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện takeoff compute trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `takeoff_decide` | mở rộng cadtroly | Thực hiện thao tác takeoff decide trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện takeoff decide trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `takeoff_export` | mở rộng cadtroly | Thực hiện thao tác takeoff xuất trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện takeoff xuất trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `takeoff_propose` | mở rộng cadtroly | Thực hiện thao tác takeoff propose trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện takeoff propose trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `takeoff_run` | mở rộng cadtroly | Thực hiện thao tác takeoff run trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện takeoff run trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `template_apply_layers` | mẫu bản vẽ | Thực hiện thao tác mẫu apply layers trong bản vẽ CAD. | Khi cần mẫu bản vẽ. | Tạo bản vẽ mới từ mẫu dự án rồi thực hiện mẫu apply layers theo tiêu chuẩn đã chọn. |
| `template_list` | mẫu bản vẽ | Thực hiện thao tác mẫu liệt kê trong bản vẽ CAD. | Khi cần mẫu bản vẽ. | Tạo bản vẽ mới từ mẫu dự án rồi thực hiện mẫu liệt kê theo tiêu chuẩn đã chọn. |
| `text_find_replace` | sửa đối tượng | Thực hiện thao tác chữ tìm replace trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | Chụp ảnh trước, thực hiện chữ tìm replace, chụp ảnh sau và liệt kê các đối tượng đã đổi. |
| `text_set_background` | sửa đối tượng | Thực hiện thao tác chữ đặt background trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | Chụp ảnh trước, thực hiện chữ đặt background, chụp ảnh sau và liệt kê các đối tượng đã đổi. |
| `textstyle_create` | kiểu hiển thị | Thực hiện thao tác textstyle tạo trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | Kiểm tra kiểu hiển thị hiện tại và thực hiện textstyle tạo cho toàn bộ bản vẽ. |
| `textstyle_list` | kiểu hiển thị | Thực hiện thao tác textstyle liệt kê trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | Kiểm tra kiểu hiển thị hiện tại và thực hiện textstyle liệt kê cho toàn bộ bản vẽ. |
| `textstyle_set_current` | kiểu hiển thị | Thực hiện thao tác textstyle đặt hiện tại trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | Kiểm tra kiểu hiển thị hiện tại và thực hiện textstyle đặt hiện tại cho toàn bộ bản vẽ. |
| `titleblock_apply` | tờ bản vẽ | Thực hiện thao tác titleblock apply trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | Chuẩn bị tờ bản vẽ phát hành và thực hiện titleblock apply trong khung tên. |
| `titleblock_apply_iso_a3` | kỹ thuật | Thực hiện thao tác titleblock apply iso a3 trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo titleblock apply iso a3 thành lỗi hoặc cảnh báo. |
| `transaction_begin` | giao dịch | Thực hiện thao tác giao dịch begin trong bản vẽ CAD. | Khi cần giao dịch thay đổi có kiểm soát. | Bắt đầu giao dịch, thực hiện giao dịch begin, cho tôi xem thay đổi rồi mới xác nhận. |
| `transaction_commit` | giao dịch | Thực hiện thao tác giao dịch commit trong bản vẽ CAD. | Khi cần giao dịch thay đổi có kiểm soát. | Bắt đầu giao dịch, thực hiện giao dịch commit, cho tôi xem thay đổi rồi mới xác nhận. |
| `transaction_rollback` | giao dịch | Thực hiện thao tác giao dịch rollback trong bản vẽ CAD. | Khi cần giao dịch thay đổi có kiểm soát. | Bắt đầu giao dịch, thực hiện giao dịch rollback, cho tôi xem thay đổi rồi mới xác nhận. |
| `ucs_list` | môi trường | Thực hiện thao tác ucs liệt kê trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo ucs liệt kê trước khi thao tác bản vẽ. |
| `ucs_restore` | môi trường | Thực hiện thao tác ucs restore trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo ucs restore trước khi thao tác bản vẽ. |
| `ucs_set` | môi trường | Thực hiện thao tác ucs đặt trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo ucs đặt trước khi thao tác bản vẽ. |
| `user_pick_point` | môi trường | Thực hiện thao tác user pick điểm trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo user pick điểm trước khi thao tác bản vẽ. |
| `user_select` | môi trường | Thực hiện thao tác user chọn trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo user chọn trước khi thao tác bản vẽ. |
| `validation_check` | xác nhận | Thực hiện thao tác validation kiểm tra trong bản vẽ CAD. | Khi cần kiểm tra hợp lệ. | Kiểm tra bản vẽ và báo cáo validation kiểm tra theo mức Error, Warning và Info. |
| `view_named_list` | môi trường | Thực hiện thao tác góc nhìn named liệt kê trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo góc nhìn named liệt kê trước khi thao tác bản vẽ. |
| `view_named_restore` | môi trường | Thực hiện thao tác góc nhìn named restore trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo góc nhìn named restore trước khi thao tác bản vẽ. |
| `view_named_save` | môi trường | Thực hiện thao tác góc nhìn named lưu trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | Kiểm tra kết nối AutoCAD và báo cáo góc nhìn named lưu trước khi thao tác bản vẽ. |
| `view_render_report` | mở rộng cadtroly | Thực hiện thao tác góc nhìn kết xuất report trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | Thực hiện góc nhìn kết xuất report trên bản vẽ, báo cáo kết quả và không ghi đè file gốc. |
| `view_screenshot` | góc nhìn | Thực hiện thao tác góc nhìn screenshot trong bản vẽ CAD. | Khi cần thu phóng, góc nhìn và ảnh chụp. | Chụp riêng vùng mặt bằng tầng 1, vùng khung tên và vùng kích thước bên phải. |
| `view_zoom_and_screenshot` | góc nhìn | Thực hiện thao tác góc nhìn thu phóng và screenshot trong bản vẽ CAD. | Khi cần thu phóng, góc nhìn và ảnh chụp. | Thu toàn bộ bản vẽ vào màn hình rồi chụp ảnh để tôi kiểm tra nhanh. |
| `view_zoom_extents` | góc nhìn | Thực hiện thao tác góc nhìn thu phóng extents trong bản vẽ CAD. | Khi cần thu phóng, góc nhìn và ảnh chụp. | Thu phóng để toàn bộ đối tượng của bản vẽ nằm vừa trên màn hình. |
| `view_zoom_window` | góc nhìn | Thực hiện thao tác góc nhìn thu phóng window trong bản vẽ CAD. | Khi cần thu phóng, góc nhìn và ảnh chụp. | Phóng to riêng vùng mặt bằng tầng 1 để nhìn rõ cửa, thiết bị và kích thước. |
| `viewport_create` | bố cục | Thực hiện thao tác khung nhìn tạo trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | Thiết lập bố cục A1 và thực hiện khung nhìn tạo cho khung tên và khung nhìn. |
| `viewport_delete` | bố cục | Thực hiện thao tác khung nhìn xóa trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | Thiết lập bố cục A1 và thực hiện khung nhìn xóa cho khung tên và khung nhìn. |
| `viewport_list` | bố cục | Thực hiện thao tác khung nhìn liệt kê trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | Thiết lập bố cục A1 và thực hiện khung nhìn liệt kê cho khung tên và khung nhìn. |
| `viewport_lock` | bố cục | Thực hiện thao tác khung nhìn khóa trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | Thiết lập bố cục A1 và thực hiện khung nhìn khóa cho khung tên và khung nhìn. |
| `viewport_set_scale` | bố cục | Thực hiện thao tác khung nhìn đặt tỷ lệ trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | Thiết lập bố cục A1 và thực hiện khung nhìn đặt tỷ lệ cho khung tên và khung nhìn. |
| `weld_symbol` | cơ khí | Thực hiện thao tác mối hàn ký hiệu trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | Trên bản vẽ cơ khí, hãy mối hàn ký hiệu theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn. |
| `xref_attach` | tờ bản vẽ | Thực hiện thao tác tham chiếu ngoài đính kèm trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | Chuẩn bị tờ bản vẽ phát hành và thực hiện tham chiếu ngoài đính kèm trong khung tên. |
| `xref_manage` | tờ bản vẽ | Thực hiện thao tác tham chiếu ngoài quản lý trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | Chuẩn bị tờ bản vẽ phát hành và thực hiện tham chiếu ngoài quản lý trong khung tên. |

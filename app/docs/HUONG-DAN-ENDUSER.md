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

File [MCP-TOOL-USAGE.md](MCP-TOOL-USAGE.md) chứa chi tiết từng tool: tên, chức năng, thời điểm dùng, tham số, ví dụ JSON và lưu ý an toàn.

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

| Tên tool | Nhóm | Làm gì | Dùng khi nào |
|---|---|---|---|
| `analysis_bounding_box` | phân tích | Thực hiện thao tác phân tích giới hạn khung trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `analysis_entity_stats` | phân tích | Thực hiện thao tác phân tích đối tượng thống kê trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `analysis_find_in_region` | phân tích | Thực hiện thao tác phân tích tìm in vùng trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `analysis_layer_stats` | phân tích | Thực hiện thao tác phân tích lớp thống kê trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `analysis_list_properties` | phân tích | Thực hiện thao tác phân tích liệt kê thuộc tính trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `analysis_measure_area` | phân tích | Thực hiện thao tác phân tích đo diện tích trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `analysis_measure_distance` | phân tích | Thực hiện thao tác phân tích đo khoảng cách trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `analysis_measure_entity` | phân tích | Thực hiện thao tác phân tích đo đối tượng trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `analysis_select_by_layer` | phân tích | Thực hiện thao tác phân tích chọn by lớp trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `analysis_select_by_type` | phân tích | Thực hiện thao tác phân tích chọn by type trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `arch_catalogue_insert` | kiến trúc | Thực hiện thao tác arch catalogue chèn trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_catalogue_list` | kiến trúc | Thực hiện thao tác arch catalogue liệt kê trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_dimension_chains` | kiến trúc | Thực hiện thao tác arch kích thước chains trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_grid` | kiến trúc | Thực hiện thao tác arch grid trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_opening` | kiến trúc | Thực hiện thao tác arch opening trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_plan_from_spec` | kiến trúc | Thực hiện thao tác arch mặt bằng from spec trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_room` | kiến trúc | Thực hiện thao tác arch room trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_rooms_detect` | kiến trúc | Thực hiện thao tác arch rooms detect trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_schedule` | kiến trúc | Thực hiện thao tác arch schedule trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_stair` | kiến trúc | Thực hiện thao tác arch stair trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_symbol` | kiến trúc | Thực hiện thao tác arch ký hiệu trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_wall` | kiến trúc | Thực hiện thao tác arch wall trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `balloon_add` | tờ bản vẽ | Thực hiện thao tác balloon add trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. |
| `batch_plot` | thiết lập trang | Thực hiện thao tác hàng loạt plot trong bản vẽ CAD. | Khi cần khổ giấy, tỷ lệ và in ấn. |
| `block_create_from_entities` | khối | Thực hiện thao tác khối tạo from entities trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. |
| `block_define` | khối | Thực hiện thao tác khối define trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. |
| `block_explode` | khối | Thực hiện thao tác khối phá khối trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. |
| `block_find_references` | khối | Thực hiện thao tác khối tìm references trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. |
| `block_get_attributes` | khối | Thực hiện thao tác khối get attributes trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. |
| `block_insert` | khối | Thực hiện thao tác khối chèn trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. |
| `block_list` | khối | Thực hiện thao tác khối liệt kê trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. |
| `block_set_attributes` | khối | Thực hiện thao tác khối đặt attributes trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. |
| `bom_extract` | tờ bản vẽ | Thực hiện thao tác bom extract trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. |
| `bom_table` | tờ bản vẽ | Thực hiện thao tác bom bảng trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. |
| `boundary_from_entities` | phân tích | Thực hiện thao tác boundary from entities trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `boundary_trace` | phân tích | Thực hiện thao tác boundary trace trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `cable_takeoff` | nhà máy | Thực hiện thao tác cable takeoff trong bản vẽ CAD. | Khi cần bố trí thiết bị nhà máy. |
| `cad_batch` | xử lý hàng loạt | Thực hiện thao tác cad hàng loạt trong bản vẽ CAD. | Khi cần xử lý hàng loạt. |
| `centre_marks` | cơ khí | Thực hiện thao tác centre marks trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. |
| `check_rulesets` | mở rộng cadtroly | Thực hiện thao tác kiểm tra rulesets trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `check_run` | mở rộng cadtroly | Thực hiện thao tác kiểm tra run trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `construction_clear` | nâng cao | Thực hiện thao tác construction clear trong bản vẽ CAD. | Khi cần chức năng nâng cao. |
| `construction_xline` | nâng cao | Thực hiện thao tác construction xline trong bản vẽ CAD. | Khi cần chức năng nâng cao. |
| `data_extract` | tờ bản vẽ | Thực hiện thao tác dữ liệu extract trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. |
| `datum_feature` | kỹ thuật | Thực hiện thao tác datum feature trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. |
| `dimension_aligned` | kích thước | Thực hiện thao tác kích thước aligned trong bản vẽ CAD. | Khi cần kích thước và ghi chú đo. |
| `dimension_angular` | kích thước | Thực hiện thao tác kích thước angular trong bản vẽ CAD. | Khi cần kích thước và ghi chú đo. |
| `dimension_auto` | nâng cao | Thực hiện thao tác kích thước auto trong bản vẽ CAD. | Khi cần chức năng nâng cao. |
| `dimension_diameter` | kích thước | Thực hiện thao tác kích thước diameter trong bản vẽ CAD. | Khi cần kích thước và ghi chú đo. |
| `dimension_linear` | kích thước | Thực hiện thao tác kích thước linear trong bản vẽ CAD. | Khi cần kích thước và ghi chú đo. |
| `dimension_radius` | kích thước | Thực hiện thao tác kích thước radius trong bản vẽ CAD. | Khi cần kích thước và ghi chú đo. |
| `dimstyle_create` | kiểu hiển thị | Thực hiện thao tác dimstyle tạo trong bản vẽ CAD. | Khi cần kiểu và hiển thị. |
| `dimstyle_list` | kiểu hiển thị | Thực hiện thao tác dimstyle liệt kê trong bản vẽ CAD. | Khi cần kiểu và hiển thị. |
| `dimstyle_modify` | kiểu hiển thị | Thực hiện thao tác dimstyle sửa trong bản vẽ CAD. | Khi cần kiểu và hiển thị. |
| `dimstyle_set_current` | kiểu hiển thị | Thực hiện thao tác dimstyle đặt current trong bản vẽ CAD. | Khi cần kiểu và hiển thị. |
| `document_activate` | môi trường | Thực hiện thao tác document activate trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `document_close` | môi trường | Thực hiện thao tác document đóng trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `document_list` | môi trường | Thực hiện thao tác document liệt kê trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `drawing_apply_discipline_standard` | mở rộng cadtroly | Thực hiện thao tác bản vẽ apply discipline standard trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `drawing_apply_iso_layers` | nâng cao | Thực hiện thao tác bản vẽ apply iso layers trong bản vẽ CAD. | Khi cần chức năng nâng cao. |
| `drawing_apply_standard` | kiểu hiển thị | Thực hiện thao tác bản vẽ apply standard trong bản vẽ CAD. | Khi cần kiểu và hiển thị. |
| `drawing_audit` | bản vẽ | Thực hiện thao tác bản vẽ audit trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_close` | bản vẽ | Thực hiện thao tác bản vẽ đóng trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_critique` | nâng cao | Thực hiện thao tác bản vẽ critique trong bản vẽ CAD. | Khi cần chức năng nâng cao. |
| `drawing_deliver` | kỹ thuật | Thực hiện thao tác bản vẽ deliver trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. |
| `drawing_diff` | đọc hiểu | Thực hiện thao tác bản vẽ diff trong bản vẽ CAD. | Khi cần đọc hiểu cấu trúc bản vẽ. |
| `drawing_entities` | mở rộng cadtroly | Thực hiện thao tác bản vẽ entities trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `drawing_export_dwg` | tờ bản vẽ | Thực hiện thao tác bản vẽ xuất dwg trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. |
| `drawing_export_dxf` | bản vẽ | Thực hiện thao tác bản vẽ xuất dxf trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_export_pdf` | bản vẽ | Thực hiện thao tác bản vẽ xuất pdf trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_finalize` | kỹ thuật | Thực hiện thao tác bản vẽ finalize trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. |
| `drawing_info` | tra cứu đối tượng | Thực hiện thao tác bản vẽ info trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. |
| `drawing_new` | bản vẽ | Thực hiện thao tác bản vẽ new trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_open` | bản vẽ | Thực hiện thao tác bản vẽ mở trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_plan` | nâng cao | Thực hiện thao tác bản vẽ mặt bằng trong bản vẽ CAD. | Khi cần chức năng nâng cao. |
| `drawing_preflight` | nâng cao | Thực hiện thao tác bản vẽ preflight trong bản vẽ CAD. | Khi cần chức năng nâng cao. |
| `drawing_properties_get` | môi trường | Thực hiện thao tác bản vẽ thuộc tính get trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `drawing_properties_set` | môi trường | Thực hiện thao tác bản vẽ thuộc tính đặt trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `drawing_purge` | bản vẽ | Thực hiện thao tác bản vẽ dọn dẹp trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_read` | mở rộng cadtroly | Thực hiện thao tác bản vẽ đọc trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `drawing_redo` | bản vẽ | Thực hiện thao tác bản vẽ redo trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_refine` | nâng cao | Thực hiện thao tác bản vẽ refine trong bản vẽ CAD. | Khi cần chức năng nâng cao. |
| `drawing_save` | bản vẽ | Thực hiện thao tác bản vẽ lưu trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_save_as` | bản vẽ | Thực hiện thao tác bản vẽ lưu as trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_scale_check` | đọc hiểu | Thực hiện thao tác bản vẽ tỷ lệ kiểm tra trong bản vẽ CAD. | Khi cần đọc hiểu cấu trúc bản vẽ. |
| `drawing_settings` | hệ thống | Thực hiện thao tác bản vẽ thiết lập trong bản vẽ CAD. | Khi cần trạng thái máy chủ. |
| `drawing_template_list` | thiết lập trang | Thực hiện thao tác bản vẽ mẫu liệt kê trong bản vẽ CAD. | Khi cần khổ giấy, tỷ lệ và in ấn. |
| `drawing_template_save` | thiết lập trang | Thực hiện thao tác bản vẽ mẫu lưu trong bản vẽ CAD. | Khi cần khổ giấy, tỷ lệ và in ấn. |
| `drawing_topology_check` | đọc hiểu | Thực hiện thao tác bản vẽ topology kiểm tra trong bản vẽ CAD. | Khi cần đọc hiểu cấu trúc bản vẽ. |
| `drawing_understand` | đọc hiểu | Thực hiện thao tác bản vẽ understand trong bản vẽ CAD. | Khi cần đọc hiểu cấu trúc bản vẽ. |
| `drawing_undo` | bản vẽ | Thực hiện thao tác bản vẽ undo trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `entity_array_polar` | sửa đối tượng | Thực hiện thao tác đối tượng array polar trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_array_rectangular` | sửa đối tượng | Thực hiện thao tác đối tượng array rectangular trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_batch_create` | xử lý hàng loạt | Thực hiện thao tác đối tượng hàng loạt tạo trong bản vẽ CAD. | Khi cần xử lý hàng loạt. |
| `entity_batch_modify` | xử lý hàng loạt | Thực hiện thao tác đối tượng hàng loạt sửa trong bản vẽ CAD. | Khi cần xử lý hàng loạt. |
| `entity_chamfer` | corner_ops | Thực hiện thao tác đối tượng chamfer trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `entity_change_space` | bố cục | Thực hiện thao tác đối tượng change space trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. |
| `entity_copy` | sửa đối tượng | Thực hiện thao tác đối tượng sao chép trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_create_arc` | tạo đối tượng | Thực hiện thao tác đối tượng tạo cung trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. |
| `entity_create_block_ref` | khối | Thực hiện thao tác đối tượng tạo khối ref trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. |
| `entity_create_circle` | tạo đối tượng | Thực hiện thao tác đối tượng tạo đường tròn trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. |
| `entity_create_ellipse` | tạo đối tượng | Thực hiện thao tác đối tượng tạo ellipse trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. |
| `entity_create_hatch` | tạo đối tượng | Thực hiện thao tác đối tượng tạo tô mặt trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. |
| `entity_create_line` | tạo đối tượng | Thực hiện thao tác đối tượng tạo đường trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. |
| `entity_create_mtext` | tạo đối tượng | Thực hiện thao tác đối tượng tạo mtext trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. |
| `entity_create_point` | tạo đối tượng | Thực hiện thao tác đối tượng tạo điểm trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. |
| `entity_create_polyline` | tạo đối tượng | Thực hiện thao tác đối tượng tạo đa tuyến trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. |
| `entity_create_rectangle` | tạo đối tượng | Thực hiện thao tác đối tượng tạo hình chữ nhật trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. |
| `entity_create_revcloud` | tạo đối tượng | Thực hiện thao tác đối tượng tạo revcloud trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. |
| `entity_create_spline` | tạo đối tượng | Thực hiện thao tác đối tượng tạo spline trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. |
| `entity_create_table` | tạo đối tượng | Thực hiện thao tác đối tượng tạo bảng trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. |
| `entity_create_text` | tạo đối tượng | Thực hiện thao tác đối tượng tạo chữ trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. |
| `entity_create_wipeout` | tạo đối tượng | Thực hiện thao tác đối tượng tạo wipeout trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. |
| `entity_delete` | sửa đối tượng | Thực hiện thao tác đối tượng xóa trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_delete_many` | sửa đối tượng | Thực hiện thao tác đối tượng xóa many trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_edit_geometry` | sửa đối tượng | Thực hiện thao tác đối tượng edit geometry trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_edit_text` | sửa đối tượng | Thực hiện thao tác đối tượng edit chữ trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_extend` | corner_ops | Thực hiện thao tác đối tượng kéo dài trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `entity_fillet` | corner_ops | Thực hiện thao tác đối tượng fillet trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `entity_get` | tra cứu đối tượng | Thực hiện thao tác đối tượng get trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. |
| `entity_get_xdata` | tra cứu đối tượng | Thực hiện thao tác đối tượng get xdata trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. |
| `entity_list` | tra cứu đối tượng | Thực hiện thao tác đối tượng liệt kê trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. |
| `entity_mirror` | sửa đối tượng | Thực hiện thao tác đối tượng đối xứng trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_move` | sửa đối tượng | Thực hiện thao tác đối tượng di chuyển trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_offset` | sửa đối tượng | Thực hiện thao tác đối tượng song song trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_rotate` | sửa đối tượng | Thực hiện thao tác đối tượng xoay trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_scale` | sửa đối tượng | Thực hiện thao tác đối tượng tỷ lệ trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_select_smart` | nâng cao | Thực hiện thao tác đối tượng chọn smart trong bản vẽ CAD. | Khi cần chức năng nâng cao. |
| `entity_set_properties` | sửa đối tượng | Thực hiện thao tác đối tượng đặt thuộc tính trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_set_xdata` | sửa đối tượng | Thực hiện thao tác đối tượng đặt xdata trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_trim` | corner_ops | Thực hiện thao tác đối tượng cắt trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `gd_frame` | kỹ thuật | Thực hiện thao tác gd frame trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. |
| `gear_draw_helical_front_view` | kỹ thuật | Thực hiện thao tác gear draw helical front góc nhìn trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. |
| `gear_draw_section_aa` | kỹ thuật | Thực hiện thao tác gear draw mặt cắt aa trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. |
| `gear_draw_spur_front_view` | kỹ thuật | Thực hiện thao tác gear draw spur front góc nhìn trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. |
| `hatch_add_boundary` | tạo đối tượng | Thực hiện thao tác tô mặt add boundary trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. |
| `hatch_edit` | tạo đối tượng | Thực hiện thao tác tô mặt edit trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. |
| `hatch_material` | cơ khí | Thực hiện thao tác tô mặt material trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. |
| `hatch_set_gradient` | tạo đối tượng | Thực hiện thao tác tô mặt đặt gradient trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. |
| `image_attach` | tờ bản vẽ | Thực hiện thao tác hình ảnh đính kèm trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. |
| `keyway_draw_keyed_bore` | kỹ thuật | Thực hiện thao tác keyway draw keyed bore trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. |
| `keyway_draw_section` | kỹ thuật | Thực hiện thao tác keyway draw mặt cắt trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. |
| `kho_industries` | mở rộng cadtroly | Thực hiện thao tác kho industries trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `kho_rules_export` | mở rộng cadtroly | Thực hiện thao tác kho rules xuất trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `kho_rules_import` | mở rộng cadtroly | Thực hiện thao tác kho rules nhập trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `kho_skill_add` | mở rộng cadtroly | Thực hiện thao tác kho skill add trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `kho_skill_toggle` | mở rộng cadtroly | Thực hiện thao tác kho skill toggle trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `kho_skills` | mở rộng cadtroly | Thực hiện thao tác kho skills trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `kho_standard_add` | mở rộng cadtroly | Thực hiện thao tác kho standard add trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `kho_standard_delete` | mở rộng cadtroly | Thực hiện thao tác kho standard xóa trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `kho_standards` | mở rộng cadtroly | Thực hiện thao tác kho standards trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `kho_status` | mở rộng cadtroly | Thực hiện thao tác kho trạng thái trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `layer_create` | lớp bản vẽ | Thực hiện thao tác lớp tạo trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. |
| `layer_delete` | lớp bản vẽ | Thực hiện thao tác lớp xóa trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. |
| `layer_freeze` | lớp bản vẽ | Thực hiện thao tác lớp freeze trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. |
| `layer_hide` | lớp bản vẽ | Thực hiện thao tác lớp hide trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. |
| `layer_isolate` | lớp bản vẽ | Thực hiện thao tác lớp isolate trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. |
| `layer_list` | lớp bản vẽ | Thực hiện thao tác lớp liệt kê trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. |
| `layer_lock` | lớp bản vẽ | Thực hiện thao tác lớp khóa trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. |
| `layer_modify` | lớp bản vẽ | Thực hiện thao tác lớp sửa trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. |
| `layer_set_current` | lớp bản vẽ | Thực hiện thao tác lớp đặt current trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. |
| `layer_show` | lớp bản vẽ | Thực hiện thao tác lớp show trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. |
| `layer_state_delete` | môi trường | Thực hiện thao tác lớp state xóa trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `layer_state_list` | môi trường | Thực hiện thao tác lớp state liệt kê trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `layer_state_restore` | môi trường | Thực hiện thao tác lớp state restore trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `layer_state_save` | môi trường | Thực hiện thao tác lớp state lưu trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `layer_thaw` | lớp bản vẽ | Thực hiện thao tác lớp thaw trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. |
| `layer_unlock` | lớp bản vẽ | Thực hiện thao tác lớp unlock trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. |
| `layout_copy` | bố cục | Thực hiện thao tác bố cục sao chép trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. |
| `layout_create` | bố cục | Thực hiện thao tác bố cục tạo trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. |
| `layout_delete` | bố cục | Thực hiện thao tác bố cục xóa trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. |
| `layout_list` | bố cục | Thực hiện thao tác bố cục liệt kê trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. |
| `layout_rename` | bố cục | Thực hiện thao tác bố cục đổi tên trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. |
| `layout_set_current` | bố cục | Thực hiện thao tác bố cục đặt current trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. |
| `leader_create_mleader` | tạo đối tượng | Thực hiện thao tác đường dẫn tạo mleader trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. |
| `linetype_list` | lớp bản vẽ | Thực hiện thao tác linetype liệt kê trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. |
| `linetype_load` | lớp bản vẽ | Thực hiện thao tác linetype load trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. |
| `mech_dimension_part` | cơ khí | Thực hiện thao tác mech kích thước part trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. |
| `mech_hole_pattern` | cơ khí | Thực hiện thao tác mech hole pattern trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. |
| `mech_part_draw` | cơ khí | Thực hiện thao tác mech part draw trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. |
| `mech_part_from_spec` | cơ khí | Thực hiện thao tác mech part from spec trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. |
| `mech_part_inspect` | cơ khí | Thực hiện thao tác mech part inspect trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. |
| `mech_view_add` | cơ khí | Thực hiện thao tác mech góc nhìn add trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. |
| `mleaderstyle_create` | kiểu hiển thị | Thực hiện thao tác mleaderstyle tạo trong bản vẽ CAD. | Khi cần kiểu và hiển thị. |
| `mleaderstyle_list` | kiểu hiển thị | Thực hiện thao tác mleaderstyle liệt kê trong bản vẽ CAD. | Khi cần kiểu và hiển thị. |
| `page_setup_apply` | thiết lập trang | Thực hiện thao tác trang cài đặt apply trong bản vẽ CAD. | Khi cần khổ giấy, tỷ lệ và in ấn. |
| `page_setup_list` | thiết lập trang | Thực hiện thao tác trang cài đặt liệt kê trong bản vẽ CAD. | Khi cần khổ giấy, tỷ lệ và in ấn. |
| `pdf_to_dwg` | mở rộng cadtroly | Thực hiện thao tác pdf to dwg trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `pdf_vectorize` | mở rộng cadtroly | Thực hiện thao tác pdf vectorize trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `pid_equipment_list` | P&ID | Thực hiện thao tác P&ID equipment liệt kê trong bản vẽ CAD. | Khi cần sơ đồ P&ID. |
| `pid_from_spec` | P&ID | Thực hiện thao tác P&ID from spec trong bản vẽ CAD. | Khi cần sơ đồ P&ID. |
| `pid_graph` | P&ID | Thực hiện thao tác P&ID graph trong bản vẽ CAD. | Khi cần sơ đồ P&ID. |
| `pid_instrument_index` | P&ID | Thực hiện thao tác P&ID instrument index trong bản vẽ CAD. | Khi cần sơ đồ P&ID. |
| `pid_line_draw` | P&ID | Thực hiện thao tác P&ID đường draw trong bản vẽ CAD. | Khi cần sơ đồ P&ID. |
| `pid_line_list` | P&ID | Thực hiện thao tác P&ID đường liệt kê trong bản vẽ CAD. | Khi cần sơ đồ P&ID. |
| `pid_symbol_insert` | P&ID | Thực hiện thao tác P&ID ký hiệu chèn trong bản vẽ CAD. | Khi cần sơ đồ P&ID. |
| `pid_symbol_list` | P&ID | Thực hiện thao tác P&ID ký hiệu liệt kê trong bản vẽ CAD. | Khi cần sơ đồ P&ID. |
| `pid_tag_parse` | P&ID | Thực hiện thao tác P&ID tag parse trong bản vẽ CAD. | Khi cần sơ đồ P&ID. |
| `pipe_takeoff` | nhà máy | Thực hiện thao tác pipe takeoff trong bản vẽ CAD. | Khi cần bố trí thiết bị nhà máy. |
| `plot_style_list` | thiết lập trang | Thực hiện thao tác plot kiểu liệt kê trong bản vẽ CAD. | Khi cần khổ giấy, tỷ lệ và in ấn. |
| `point_from_snap` | nâng cao | Thực hiện thao tác điểm from snap trong bản vẽ CAD. | Khi cần chức năng nâng cao. |
| `point_intersection` | nâng cao | Thực hiện thao tác điểm intersection trong bản vẽ CAD. | Khi cần chức năng nâng cao. |
| `point_tangent` | nâng cao | Thực hiện thao tác điểm tangent trong bản vẽ CAD. | Khi cần chức năng nâng cao. |
| `revision_add` | tờ bản vẽ | Thực hiện thao tác revision add trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. |
| `section_line` | cơ khí | Thực hiện thao tác mặt cắt đường trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. |
| `selection_filter` | tra cứu đối tượng | Thực hiện thao tác selection filter trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. |
| `selection_get` | tra cứu đối tượng | Thực hiện thao tác selection get trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. |
| `selection_polygon` | tra cứu đối tượng | Thực hiện thao tác selection đa giác trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. |
| `selection_window` | tra cứu đối tượng | Thực hiện thao tác selection window trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. |
| `sheet_frame` | tờ bản vẽ | Thực hiện thao tác tờ bản vẽ frame trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. |
| `solid_boolean` | khối đặc | Thực hiện thao tác khối đặc boolean trong bản vẽ CAD. | Khi cần hình học ba chiều và khối đặc. |
| `solid_box` | khối đặc | Thực hiện thao tác khối đặc khung trong bản vẽ CAD. | Khi cần hình học ba chiều và khối đặc. |
| `solid_cylinder` | khối đặc | Thực hiện thao tác khối đặc cylinder trong bản vẽ CAD. | Khi cần hình học ba chiều và khối đặc. |
| `solid_extrude` | khối đặc | Thực hiện thao tác khối đặc extrude trong bản vẽ CAD. | Khi cần hình học ba chiều và khối đặc. |
| `solid_revolve` | khối đặc | Thực hiện thao tác khối đặc revolve trong bản vẽ CAD. | Khi cần hình học ba chiều và khối đặc. |
| `standards_reference` | mở rộng cadtroly | Thực hiện thao tác standards reference trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `std_feature_draw` | cơ khí | Thực hiện thao tác std feature draw trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. |
| `std_part_insert` | cơ khí | Thực hiện thao tác std part chèn trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. |
| `std_part_list` | cơ khí | Thực hiện thao tác std part liệt kê trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. |
| `structural_qa` | mở rộng cadtroly | Thực hiện thao tác structural qa trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `surface_texture` | cơ khí | Thực hiện thao tác surface texture trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. |
| `system_about` | hệ thống | Thực hiện thao tác hệ thống thông tin trong bản vẽ CAD. | Khi cần trạng thái máy chủ. |
| `system_capabilities` | tra cứu đối tượng | Thực hiện thao tác hệ thống capabilities trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. |
| `system_get_variable` | hệ thống | Thực hiện thao tác hệ thống get variable trong bản vẽ CAD. | Khi cần trạng thái máy chủ. |
| `system_launch` | môi trường | Thực hiện thao tác hệ thống launch trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `system_preferences_get` | môi trường | Thực hiện thao tác hệ thống preferences get trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `system_preferences_set` | môi trường | Thực hiện thao tác hệ thống preferences đặt trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `system_prompt_message` | môi trường | Thực hiện thao tác hệ thống prompt message trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `system_run_command` | hệ thống | Thực hiện thao tác hệ thống run command trong bản vẽ CAD. | Khi cần trạng thái máy chủ. |
| `system_run_lisp` | hệ thống | Thực hiện thao tác hệ thống run lisp trong bản vẽ CAD. | Khi cần trạng thái máy chủ. |
| `system_set_variable` | hệ thống | Thực hiện thao tác hệ thống đặt variable trong bản vẽ CAD. | Khi cần trạng thái máy chủ. |
| `system_status` | hệ thống | Thực hiện thao tác hệ thống trạng thái trong bản vẽ CAD. | Khi cần trạng thái máy chủ. |
| `system_variable_describe` | môi trường | Thực hiện thao tác hệ thống variable describe trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `takeoff_compute` | mở rộng cadtroly | Thực hiện thao tác takeoff compute trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `takeoff_decide` | mở rộng cadtroly | Thực hiện thao tác takeoff decide trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `takeoff_export` | mở rộng cadtroly | Thực hiện thao tác takeoff xuất trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `takeoff_propose` | mở rộng cadtroly | Thực hiện thao tác takeoff propose trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `takeoff_run` | mở rộng cadtroly | Thực hiện thao tác takeoff run trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `template_apply_layers` | mẫu bản vẽ | Thực hiện thao tác mẫu apply layers trong bản vẽ CAD. | Khi cần mẫu bản vẽ. |
| `template_list` | mẫu bản vẽ | Thực hiện thao tác mẫu liệt kê trong bản vẽ CAD. | Khi cần mẫu bản vẽ. |
| `text_find_replace` | sửa đối tượng | Thực hiện thao tác chữ tìm replace trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. |
| `text_set_background` | sửa đối tượng | Thực hiện thao tác chữ đặt background trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. |
| `textstyle_create` | kiểu hiển thị | Thực hiện thao tác textstyle tạo trong bản vẽ CAD. | Khi cần kiểu và hiển thị. |
| `textstyle_list` | kiểu hiển thị | Thực hiện thao tác textstyle liệt kê trong bản vẽ CAD. | Khi cần kiểu và hiển thị. |
| `textstyle_set_current` | kiểu hiển thị | Thực hiện thao tác textstyle đặt current trong bản vẽ CAD. | Khi cần kiểu và hiển thị. |
| `titleblock_apply` | tờ bản vẽ | Thực hiện thao tác titleblock apply trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. |
| `titleblock_apply_iso_a3` | kỹ thuật | Thực hiện thao tác titleblock apply iso a3 trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. |
| `transaction_begin` | giao dịch | Thực hiện thao tác giao dịch begin trong bản vẽ CAD. | Khi cần giao dịch thay đổi có kiểm soát. |
| `transaction_commit` | giao dịch | Thực hiện thao tác giao dịch commit trong bản vẽ CAD. | Khi cần giao dịch thay đổi có kiểm soát. |
| `transaction_rollback` | giao dịch | Thực hiện thao tác giao dịch rollback trong bản vẽ CAD. | Khi cần giao dịch thay đổi có kiểm soát. |
| `ucs_list` | môi trường | Thực hiện thao tác ucs liệt kê trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `ucs_restore` | môi trường | Thực hiện thao tác ucs restore trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `ucs_set` | môi trường | Thực hiện thao tác ucs đặt trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `user_pick_point` | môi trường | Thực hiện thao tác user pick điểm trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `user_select` | môi trường | Thực hiện thao tác user chọn trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `validation_check` | xác nhận | Thực hiện thao tác validation kiểm tra trong bản vẽ CAD. | Khi cần kiểm tra hợp lệ. |
| `view_named_list` | môi trường | Thực hiện thao tác góc nhìn named liệt kê trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `view_named_restore` | môi trường | Thực hiện thao tác góc nhìn named restore trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `view_named_save` | môi trường | Thực hiện thao tác góc nhìn named lưu trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. |
| `view_render_report` | mở rộng cadtroly | Thực hiện thao tác góc nhìn kết xuất report trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. |
| `view_screenshot` | góc nhìn | Thực hiện thao tác góc nhìn screenshot trong bản vẽ CAD. | Khi cần thu phóng, góc nhìn và ảnh chụp. |
| `view_zoom_and_screenshot` | góc nhìn | Thực hiện thao tác góc nhìn thu phóng and screenshot trong bản vẽ CAD. | Khi cần thu phóng, góc nhìn và ảnh chụp. |
| `view_zoom_extents` | góc nhìn | Thực hiện thao tác góc nhìn thu phóng extents trong bản vẽ CAD. | Khi cần thu phóng, góc nhìn và ảnh chụp. |
| `view_zoom_window` | góc nhìn | Thực hiện thao tác góc nhìn thu phóng window trong bản vẽ CAD. | Khi cần thu phóng, góc nhìn và ảnh chụp. |
| `viewport_create` | bố cục | Thực hiện thao tác khung nhìn tạo trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. |
| `viewport_delete` | bố cục | Thực hiện thao tác khung nhìn xóa trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. |
| `viewport_list` | bố cục | Thực hiện thao tác khung nhìn liệt kê trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. |
| `viewport_lock` | bố cục | Thực hiện thao tác khung nhìn khóa trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. |
| `viewport_set_scale` | bố cục | Thực hiện thao tác khung nhìn đặt tỷ lệ trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. |
| `weld_symbol` | cơ khí | Thực hiện thao tác mối hàn ký hiệu trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. |
| `xref_attach` | tờ bản vẽ | Thực hiện thao tác tham chiếu ngoài đính kèm trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. |
| `xref_manage` | tờ bản vẽ | Thực hiện thao tác tham chiếu ngoài quản lý trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. |

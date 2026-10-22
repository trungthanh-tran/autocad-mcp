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

File [MCP-TOOL-USAGE.md](app/docs/MCP-TOOL-USAGE.md) là tài liệu kỹ thuật; file này chỉ dành cho enduser và tập trung vào câu lệnh gõ vào LLM.

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

## 11. Mục lục chức năng theo ngành

Có **272 chức năng**, gồm **247 chức năng nền tảng** và chức năng mở rộng của cadtroly. Các chức năng được xếp theo ngành; chức năng dùng chung nằm ở nhóm đầu. Bấm vào tên để đi đến phần hướng dẫn tương ứng.

### Dùng chung
_Các chức năng có thể dùng cho hầu hết bản vẽ và ngành kỹ thuật._
#### bo góc và cắt nối
- [`entity_chamfer`](#entity_chamfer) — bo góc và cắt nối: dùng để đối tượng chamfer trong bản vẽ CAD.
- [`entity_extend`](#entity_extend) — bo góc và cắt nối: dùng để đối tượng kéo dài trong bản vẽ CAD.
- [`entity_fillet`](#entity_fillet) — bo góc và cắt nối: dùng để đối tượng fillet trong bản vẽ CAD.
- [`entity_trim`](#entity_trim) — bo góc và cắt nối: dùng để đối tượng cắt trong bản vẽ CAD.
#### bản vẽ
- [`drawing_audit`](#drawing_audit) — bản vẽ: dùng để bản vẽ audit trong bản vẽ CAD.
- [`drawing_close`](#drawing_close) — bản vẽ: dùng để bản vẽ đóng trong bản vẽ CAD.
- [`drawing_export_dxf`](#drawing_export_dxf) — bản vẽ: dùng để bản vẽ xuất dxf trong bản vẽ CAD.
- [`drawing_export_pdf`](#drawing_export_pdf) — bản vẽ: dùng để bản vẽ xuất pdf trong bản vẽ CAD.
- [`drawing_new`](#drawing_new) — bản vẽ: dùng để bản vẽ new trong bản vẽ CAD.
- [`drawing_open`](#drawing_open) — bản vẽ: dùng để bản vẽ mở trong bản vẽ CAD.
- [`drawing_purge`](#drawing_purge) — bản vẽ: dùng để bản vẽ dọn dẹp trong bản vẽ CAD.
- [`drawing_redo`](#drawing_redo) — bản vẽ: dùng để bản vẽ redo trong bản vẽ CAD.
- [`drawing_save`](#drawing_save) — bản vẽ: dùng để bản vẽ lưu trong bản vẽ CAD.
- [`drawing_save_as`](#drawing_save_as) — bản vẽ: dùng để bản vẽ lưu as trong bản vẽ CAD.
- [`drawing_undo`](#drawing_undo) — bản vẽ: dùng để bản vẽ undo trong bản vẽ CAD.
#### bố cục
- [`entity_change_space`](#entity_change_space) — bố cục: dùng để đối tượng change space trong bản vẽ CAD.
- [`layout_copy`](#layout_copy) — bố cục: dùng để bố cục sao chép trong bản vẽ CAD.
- [`layout_create`](#layout_create) — bố cục: dùng để bố cục tạo trong bản vẽ CAD.
- [`layout_delete`](#layout_delete) — bố cục: dùng để bố cục xóa trong bản vẽ CAD.
- [`layout_list`](#layout_list) — bố cục: dùng để bố cục liệt kê trong bản vẽ CAD.
- [`layout_rename`](#layout_rename) — bố cục: dùng để bố cục đổi tên trong bản vẽ CAD.
- [`layout_set_current`](#layout_set_current) — bố cục: dùng để bố cục đặt hiện tại trong bản vẽ CAD.
- [`viewport_create`](#viewport_create) — bố cục: dùng để khung nhìn tạo trong bản vẽ CAD.
- [`viewport_delete`](#viewport_delete) — bố cục: dùng để khung nhìn xóa trong bản vẽ CAD.
- [`viewport_list`](#viewport_list) — bố cục: dùng để khung nhìn liệt kê trong bản vẽ CAD.
- [`viewport_lock`](#viewport_lock) — bố cục: dùng để khung nhìn khóa trong bản vẽ CAD.
- [`viewport_set_scale`](#viewport_set_scale) — bố cục: dùng để khung nhìn đặt tỷ lệ trong bản vẽ CAD.
#### giao dịch
- [`transaction_begin`](#transaction_begin) — giao dịch: dùng để giao dịch begin trong bản vẽ CAD.
- [`transaction_commit`](#transaction_commit) — giao dịch: dùng để giao dịch commit trong bản vẽ CAD.
- [`transaction_rollback`](#transaction_rollback) — giao dịch: dùng để giao dịch rollback trong bản vẽ CAD.
#### góc nhìn
- [`view_screenshot`](#view_screenshot) — góc nhìn: dùng để góc nhìn screenshot trong bản vẽ CAD.
- [`view_zoom_and_screenshot`](#view_zoom_and_screenshot) — góc nhìn: dùng để góc nhìn thu phóng và screenshot trong bản vẽ CAD.
- [`view_zoom_extents`](#view_zoom_extents) — góc nhìn: dùng để góc nhìn thu phóng extents trong bản vẽ CAD.
- [`view_zoom_window`](#view_zoom_window) — góc nhìn: dùng để góc nhìn thu phóng window trong bản vẽ CAD.
#### hệ thống
- [`drawing_settings`](#drawing_settings) — hệ thống: dùng để bản vẽ thiết lập trong bản vẽ CAD.
- [`system_about`](#system_about) — hệ thống: dùng để hệ thống thông tin trong bản vẽ CAD.
- [`system_get_variable`](#system_get_variable) — hệ thống: dùng để hệ thống get variable trong bản vẽ CAD.
- [`system_run_command`](#system_run_command) — hệ thống: dùng để hệ thống run command trong bản vẽ CAD.
- [`system_run_lisp`](#system_run_lisp) — hệ thống: dùng để hệ thống run lisp trong bản vẽ CAD.
- [`system_set_variable`](#system_set_variable) — hệ thống: dùng để hệ thống đặt variable trong bản vẽ CAD.
- [`system_status`](#system_status) — hệ thống: dùng để hệ thống trạng thái trong bản vẽ CAD.
#### khối
- [`block_create_from_entities`](#block_create_from_entities) — khối: dùng để khối tạo từ đối tượng trong bản vẽ CAD.
- [`block_define`](#block_define) — khối: dùng để khối định nghĩa trong bản vẽ CAD.
- [`block_explode`](#block_explode) — khối: dùng để khối phá khối trong bản vẽ CAD.
- [`block_find_references`](#block_find_references) — khối: dùng để khối tìm tham chiếu trong bản vẽ CAD.
- [`block_get_attributes`](#block_get_attributes) — khối: dùng để khối get attributes trong bản vẽ CAD.
- [`block_insert`](#block_insert) — khối: dùng để khối chèn trong bản vẽ CAD.
- [`block_list`](#block_list) — khối: dùng để khối liệt kê trong bản vẽ CAD.
- [`block_set_attributes`](#block_set_attributes) — khối: dùng để khối đặt attributes trong bản vẽ CAD.
- [`entity_create_block_ref`](#entity_create_block_ref) — khối: dùng để đối tượng tạo khối ref trong bản vẽ CAD.
#### kiểu hiển thị
- [`dimstyle_create`](#dimstyle_create) — kiểu hiển thị: dùng để dimstyle tạo trong bản vẽ CAD.
- [`dimstyle_list`](#dimstyle_list) — kiểu hiển thị: dùng để dimstyle liệt kê trong bản vẽ CAD.
- [`dimstyle_modify`](#dimstyle_modify) — kiểu hiển thị: dùng để dimstyle sửa trong bản vẽ CAD.
- [`dimstyle_set_current`](#dimstyle_set_current) — kiểu hiển thị: dùng để dimstyle đặt hiện tại trong bản vẽ CAD.
- [`drawing_apply_standard`](#drawing_apply_standard) — kiểu hiển thị: dùng để bản vẽ apply standard trong bản vẽ CAD.
- [`mleaderstyle_create`](#mleaderstyle_create) — kiểu hiển thị: dùng để mleaderstyle tạo trong bản vẽ CAD.
- [`mleaderstyle_list`](#mleaderstyle_list) — kiểu hiển thị: dùng để mleaderstyle liệt kê trong bản vẽ CAD.
- [`textstyle_create`](#textstyle_create) — kiểu hiển thị: dùng để textstyle tạo trong bản vẽ CAD.
- [`textstyle_list`](#textstyle_list) — kiểu hiển thị: dùng để textstyle liệt kê trong bản vẽ CAD.
- [`textstyle_set_current`](#textstyle_set_current) — kiểu hiển thị: dùng để textstyle đặt hiện tại trong bản vẽ CAD.
#### kích thước
- [`dimension_aligned`](#dimension_aligned) — kích thước: dùng để kích thước aligned trong bản vẽ CAD.
- [`dimension_angular`](#dimension_angular) — kích thước: dùng để kích thước angular trong bản vẽ CAD.
- [`dimension_diameter`](#dimension_diameter) — kích thước: dùng để kích thước diameter trong bản vẽ CAD.
- [`dimension_linear`](#dimension_linear) — kích thước: dùng để kích thước linear trong bản vẽ CAD.
- [`dimension_radius`](#dimension_radius) — kích thước: dùng để kích thước radius trong bản vẽ CAD.
#### lớp bản vẽ
- [`layer_create`](#layer_create) — lớp bản vẽ: dùng để lớp tạo trong bản vẽ CAD.
- [`layer_delete`](#layer_delete) — lớp bản vẽ: dùng để lớp xóa trong bản vẽ CAD.
- [`layer_freeze`](#layer_freeze) — lớp bản vẽ: dùng để lớp freeze trong bản vẽ CAD.
- [`layer_hide`](#layer_hide) — lớp bản vẽ: dùng để lớp hide trong bản vẽ CAD.
- [`layer_isolate`](#layer_isolate) — lớp bản vẽ: dùng để lớp isolate trong bản vẽ CAD.
- [`layer_list`](#layer_list) — lớp bản vẽ: dùng để lớp liệt kê trong bản vẽ CAD.
- [`layer_lock`](#layer_lock) — lớp bản vẽ: dùng để lớp khóa trong bản vẽ CAD.
- [`layer_modify`](#layer_modify) — lớp bản vẽ: dùng để lớp sửa trong bản vẽ CAD.
- [`layer_set_current`](#layer_set_current) — lớp bản vẽ: dùng để lớp đặt hiện tại trong bản vẽ CAD.
- [`layer_show`](#layer_show) — lớp bản vẽ: dùng để lớp show trong bản vẽ CAD.
- [`layer_thaw`](#layer_thaw) — lớp bản vẽ: dùng để lớp thaw trong bản vẽ CAD.
- [`layer_unlock`](#layer_unlock) — lớp bản vẽ: dùng để lớp unlock trong bản vẽ CAD.
- [`linetype_list`](#linetype_list) — lớp bản vẽ: dùng để linetype liệt kê trong bản vẽ CAD.
- [`linetype_load`](#linetype_load) — lớp bản vẽ: dùng để linetype nạp trong bản vẽ CAD.
#### môi trường
- [`document_activate`](#document_activate) — môi trường: dùng để document activate trong bản vẽ CAD.
- [`document_close`](#document_close) — môi trường: dùng để document đóng trong bản vẽ CAD.
- [`document_list`](#document_list) — môi trường: dùng để document liệt kê trong bản vẽ CAD.
- [`drawing_properties_get`](#drawing_properties_get) — môi trường: dùng để bản vẽ thuộc tính get trong bản vẽ CAD.
- [`drawing_properties_set`](#drawing_properties_set) — môi trường: dùng để bản vẽ thuộc tính đặt trong bản vẽ CAD.
- [`layer_state_delete`](#layer_state_delete) — môi trường: dùng để lớp state xóa trong bản vẽ CAD.
- [`layer_state_list`](#layer_state_list) — môi trường: dùng để lớp state liệt kê trong bản vẽ CAD.
- [`layer_state_restore`](#layer_state_restore) — môi trường: dùng để lớp state restore trong bản vẽ CAD.
- [`layer_state_save`](#layer_state_save) — môi trường: dùng để lớp state lưu trong bản vẽ CAD.
- [`system_launch`](#system_launch) — môi trường: dùng để hệ thống launch trong bản vẽ CAD.
- [`system_preferences_get`](#system_preferences_get) — môi trường: dùng để hệ thống preferences get trong bản vẽ CAD.
- [`system_preferences_set`](#system_preferences_set) — môi trường: dùng để hệ thống preferences đặt trong bản vẽ CAD.
- [`system_prompt_message`](#system_prompt_message) — môi trường: dùng để hệ thống prompt message trong bản vẽ CAD.
- [`system_variable_describe`](#system_variable_describe) — môi trường: dùng để hệ thống variable describe trong bản vẽ CAD.
- [`ucs_list`](#ucs_list) — môi trường: dùng để ucs liệt kê trong bản vẽ CAD.
- [`ucs_restore`](#ucs_restore) — môi trường: dùng để ucs restore trong bản vẽ CAD.
- [`ucs_set`](#ucs_set) — môi trường: dùng để ucs đặt trong bản vẽ CAD.
- [`user_pick_point`](#user_pick_point) — môi trường: dùng để user pick điểm trong bản vẽ CAD.
- [`user_select`](#user_select) — môi trường: dùng để user chọn trong bản vẽ CAD.
- [`view_named_list`](#view_named_list) — môi trường: dùng để góc nhìn named liệt kê trong bản vẽ CAD.
- [`view_named_restore`](#view_named_restore) — môi trường: dùng để góc nhìn named restore trong bản vẽ CAD.
- [`view_named_save`](#view_named_save) — môi trường: dùng để góc nhìn named lưu trong bản vẽ CAD.
#### mẫu bản vẽ
- [`template_apply_layers`](#template_apply_layers) — mẫu bản vẽ: dùng để mẫu apply layers trong bản vẽ CAD.
- [`template_list`](#template_list) — mẫu bản vẽ: dùng để mẫu liệt kê trong bản vẽ CAD.
#### phân tích
- [`analysis_bounding_box`](#analysis_bounding_box) — phân tích: dùng để phân tích giới hạn khung trong bản vẽ CAD.
- [`analysis_entity_stats`](#analysis_entity_stats) — phân tích: dùng để phân tích đối tượng thống kê trong bản vẽ CAD.
- [`analysis_find_in_region`](#analysis_find_in_region) — phân tích: dùng để phân tích tìm trong vùng trong bản vẽ CAD.
- [`analysis_layer_stats`](#analysis_layer_stats) — phân tích: dùng để phân tích lớp thống kê trong bản vẽ CAD.
- [`analysis_list_properties`](#analysis_list_properties) — phân tích: dùng để phân tích liệt kê thuộc tính trong bản vẽ CAD.
- [`analysis_measure_area`](#analysis_measure_area) — phân tích: dùng để phân tích đo diện tích trong bản vẽ CAD.
- [`analysis_measure_distance`](#analysis_measure_distance) — phân tích: dùng để phân tích đo khoảng cách trong bản vẽ CAD.
- [`analysis_measure_entity`](#analysis_measure_entity) — phân tích: dùng để phân tích đo đối tượng trong bản vẽ CAD.
- [`analysis_select_by_layer`](#analysis_select_by_layer) — phân tích: dùng để phân tích chọn theo lớp trong bản vẽ CAD.
- [`analysis_select_by_type`](#analysis_select_by_type) — phân tích: dùng để phân tích chọn theo loại trong bản vẽ CAD.
- [`boundary_from_entities`](#boundary_from_entities) — phân tích: dùng để boundary từ đối tượng trong bản vẽ CAD.
- [`boundary_trace`](#boundary_trace) — phân tích: dùng để boundary trace trong bản vẽ CAD.
#### sửa đối tượng
- [`entity_array_polar`](#entity_array_polar) — sửa đối tượng: dùng để đối tượng array polar trong bản vẽ CAD.
- [`entity_array_rectangular`](#entity_array_rectangular) — sửa đối tượng: dùng để đối tượng array rectangular trong bản vẽ CAD.
- [`entity_copy`](#entity_copy) — sửa đối tượng: dùng để đối tượng sao chép trong bản vẽ CAD.
- [`entity_delete`](#entity_delete) — sửa đối tượng: dùng để đối tượng xóa trong bản vẽ CAD.
- [`entity_delete_many`](#entity_delete_many) — sửa đối tượng: dùng để đối tượng xóa many trong bản vẽ CAD.
- [`entity_edit_geometry`](#entity_edit_geometry) — sửa đối tượng: dùng để đối tượng edit geometry trong bản vẽ CAD.
- [`entity_edit_text`](#entity_edit_text) — sửa đối tượng: dùng để đối tượng edit chữ trong bản vẽ CAD.
- [`entity_mirror`](#entity_mirror) — sửa đối tượng: dùng để đối tượng đối xứng trong bản vẽ CAD.
- [`entity_move`](#entity_move) — sửa đối tượng: dùng để đối tượng di chuyển trong bản vẽ CAD.
- [`entity_offset`](#entity_offset) — sửa đối tượng: dùng để đối tượng song song trong bản vẽ CAD.
- [`entity_rotate`](#entity_rotate) — sửa đối tượng: dùng để đối tượng xoay trong bản vẽ CAD.
- [`entity_scale`](#entity_scale) — sửa đối tượng: dùng để đối tượng tỷ lệ trong bản vẽ CAD.
- [`entity_set_properties`](#entity_set_properties) — sửa đối tượng: dùng để đối tượng đặt thuộc tính trong bản vẽ CAD.
- [`entity_set_xdata`](#entity_set_xdata) — sửa đối tượng: dùng để đối tượng đặt xdata trong bản vẽ CAD.
- [`text_find_replace`](#text_find_replace) — sửa đối tượng: dùng để chữ tìm replace trong bản vẽ CAD.
- [`text_set_background`](#text_set_background) — sửa đối tượng: dùng để chữ đặt background trong bản vẽ CAD.
#### thiết lập trang
- [`batch_plot`](#batch_plot) — thiết lập trang: dùng để hàng loạt plot trong bản vẽ CAD.
- [`drawing_template_list`](#drawing_template_list) — thiết lập trang: dùng để bản vẽ mẫu liệt kê trong bản vẽ CAD.
- [`drawing_template_save`](#drawing_template_save) — thiết lập trang: dùng để bản vẽ mẫu lưu trong bản vẽ CAD.
- [`page_setup_apply`](#page_setup_apply) — thiết lập trang: dùng để trang cài đặt apply trong bản vẽ CAD.
- [`page_setup_list`](#page_setup_list) — thiết lập trang: dùng để trang cài đặt liệt kê trong bản vẽ CAD.
- [`plot_style_list`](#plot_style_list) — thiết lập trang: dùng để plot kiểu liệt kê trong bản vẽ CAD.
#### tra cứu đối tượng
- [`drawing_info`](#drawing_info) — tra cứu đối tượng: dùng để bản vẽ info trong bản vẽ CAD.
- [`entity_get`](#entity_get) — tra cứu đối tượng: dùng để đối tượng get trong bản vẽ CAD.
- [`entity_get_xdata`](#entity_get_xdata) — tra cứu đối tượng: dùng để đối tượng get xdata trong bản vẽ CAD.
- [`entity_list`](#entity_list) — tra cứu đối tượng: dùng để đối tượng liệt kê trong bản vẽ CAD.
- [`selection_filter`](#selection_filter) — tra cứu đối tượng: dùng để selection filter trong bản vẽ CAD.
- [`selection_get`](#selection_get) — tra cứu đối tượng: dùng để selection get trong bản vẽ CAD.
- [`selection_polygon`](#selection_polygon) — tra cứu đối tượng: dùng để selection đa giác trong bản vẽ CAD.
- [`selection_window`](#selection_window) — tra cứu đối tượng: dùng để selection window trong bản vẽ CAD.
- [`system_capabilities`](#system_capabilities) — tra cứu đối tượng: dùng để hệ thống capabilities trong bản vẽ CAD.
#### tạo đối tượng
- [`entity_create_arc`](#entity_create_arc) — tạo đối tượng: dùng để đối tượng tạo cung trong bản vẽ CAD.
- [`entity_create_circle`](#entity_create_circle) — tạo đối tượng: dùng để đối tượng tạo đường tròn trong bản vẽ CAD.
- [`entity_create_ellipse`](#entity_create_ellipse) — tạo đối tượng: dùng để đối tượng tạo ellipse trong bản vẽ CAD.
- [`entity_create_hatch`](#entity_create_hatch) — tạo đối tượng: dùng để đối tượng tạo tô mặt trong bản vẽ CAD.
- [`entity_create_line`](#entity_create_line) — tạo đối tượng: dùng để đối tượng tạo đường trong bản vẽ CAD.
- [`entity_create_mtext`](#entity_create_mtext) — tạo đối tượng: dùng để đối tượng tạo mtext trong bản vẽ CAD.
- [`entity_create_point`](#entity_create_point) — tạo đối tượng: dùng để đối tượng tạo điểm trong bản vẽ CAD.
- [`entity_create_polyline`](#entity_create_polyline) — tạo đối tượng: dùng để đối tượng tạo đa tuyến trong bản vẽ CAD.
- [`entity_create_rectangle`](#entity_create_rectangle) — tạo đối tượng: dùng để đối tượng tạo hình chữ nhật trong bản vẽ CAD.
- [`entity_create_revcloud`](#entity_create_revcloud) — tạo đối tượng: dùng để đối tượng tạo revcloud trong bản vẽ CAD.
- [`entity_create_spline`](#entity_create_spline) — tạo đối tượng: dùng để đối tượng tạo spline trong bản vẽ CAD.
- [`entity_create_table`](#entity_create_table) — tạo đối tượng: dùng để đối tượng tạo bảng trong bản vẽ CAD.
- [`entity_create_text`](#entity_create_text) — tạo đối tượng: dùng để đối tượng tạo chữ trong bản vẽ CAD.
- [`entity_create_wipeout`](#entity_create_wipeout) — tạo đối tượng: dùng để đối tượng tạo wipeout trong bản vẽ CAD.
- [`hatch_add_boundary`](#hatch_add_boundary) — tạo đối tượng: dùng để tô mặt add boundary trong bản vẽ CAD.
- [`hatch_edit`](#hatch_edit) — tạo đối tượng: dùng để tô mặt edit trong bản vẽ CAD.
- [`hatch_set_gradient`](#hatch_set_gradient) — tạo đối tượng: dùng để tô mặt đặt gradient trong bản vẽ CAD.
- [`leader_create_mleader`](#leader_create_mleader) — tạo đối tượng: dùng để đường dẫn tạo mleader trong bản vẽ CAD.
#### tờ bản vẽ
- [`balloon_add`](#balloon_add) — tờ bản vẽ: dùng để balloon add trong bản vẽ CAD.
- [`bom_extract`](#bom_extract) — tờ bản vẽ: dùng để bom extract trong bản vẽ CAD.
- [`bom_table`](#bom_table) — tờ bản vẽ: dùng để bom bảng trong bản vẽ CAD.
- [`data_extract`](#data_extract) — tờ bản vẽ: dùng để dữ liệu extract trong bản vẽ CAD.
- [`drawing_export_dwg`](#drawing_export_dwg) — tờ bản vẽ: dùng để bản vẽ xuất dwg trong bản vẽ CAD.
- [`image_attach`](#image_attach) — tờ bản vẽ: dùng để hình ảnh đính kèm trong bản vẽ CAD.
- [`revision_add`](#revision_add) — tờ bản vẽ: dùng để revision add trong bản vẽ CAD.
- [`sheet_frame`](#sheet_frame) — tờ bản vẽ: dùng để tờ bản vẽ frame trong bản vẽ CAD.
- [`titleblock_apply`](#titleblock_apply) — tờ bản vẽ: dùng để titleblock apply trong bản vẽ CAD.
- [`xref_attach`](#xref_attach) — tờ bản vẽ: dùng để tham chiếu ngoài đính kèm trong bản vẽ CAD.
- [`xref_manage`](#xref_manage) — tờ bản vẽ: dùng để tham chiếu ngoài quản lý trong bản vẽ CAD.
#### xác nhận
- [`validation_check`](#validation_check) — xác nhận: dùng để validation kiểm tra trong bản vẽ CAD.
#### xử lý hàng loạt
- [`cad_batch`](#cad_batch) — xử lý hàng loạt: dùng để cad hàng loạt trong bản vẽ CAD.
- [`entity_batch_create`](#entity_batch_create) — xử lý hàng loạt: dùng để đối tượng hàng loạt tạo trong bản vẽ CAD.
- [`entity_batch_modify`](#entity_batch_modify) — xử lý hàng loạt: dùng để đối tượng hàng loạt sửa trong bản vẽ CAD.
#### đọc hiểu
- [`drawing_diff`](#drawing_diff) — đọc hiểu: dùng để bản vẽ diff trong bản vẽ CAD.
- [`drawing_scale_check`](#drawing_scale_check) — đọc hiểu: dùng để bản vẽ tỷ lệ kiểm tra trong bản vẽ CAD.
- [`drawing_topology_check`](#drawing_topology_check) — đọc hiểu: dùng để bản vẽ topology kiểm tra trong bản vẽ CAD.
- [`drawing_understand`](#drawing_understand) — đọc hiểu: dùng để bản vẽ understand trong bản vẽ CAD.
### Kiến trúc
_Mặt bằng, mặt đứng, mặt cắt, phòng, cửa, tường và hồ sơ kiến trúc._
#### thành phần kiến trúc
- [`arch_catalogue_insert`](#arch_catalogue_insert) — thành phần kiến trúc: dùng để arch danh mục chèn trong bản vẽ CAD.
- [`arch_catalogue_list`](#arch_catalogue_list) — thành phần kiến trúc: dùng để arch danh mục liệt kê trong bản vẽ CAD.
- [`arch_dimension_chains`](#arch_dimension_chains) — thành phần kiến trúc: dùng để arch kích thước chains trong bản vẽ CAD.
- [`arch_grid`](#arch_grid) — thành phần kiến trúc: dùng để arch lưới trục trong bản vẽ CAD.
- [`arch_opening`](#arch_opening) — thành phần kiến trúc: dùng để arch ô cửa trong bản vẽ CAD.
- [`arch_plan_from_spec`](#arch_plan_from_spec) — thành phần kiến trúc: dùng để arch mặt bằng từ spec trong bản vẽ CAD.
- [`arch_room`](#arch_room) — thành phần kiến trúc: dùng để arch phòng trong bản vẽ CAD.
- [`arch_rooms_detect`](#arch_rooms_detect) — thành phần kiến trúc: dùng để arch phòng detect trong bản vẽ CAD.
- [`arch_schedule`](#arch_schedule) — thành phần kiến trúc: dùng để arch bảng thống kê trong bản vẽ CAD.
- [`arch_stair`](#arch_stair) — thành phần kiến trúc: dùng để arch cầu thang trong bản vẽ CAD.
- [`arch_symbol`](#arch_symbol) — thành phần kiến trúc: dùng để arch ký hiệu trong bản vẽ CAD.
- [`arch_wall`](#arch_wall) — thành phần kiến trúc: dùng để arch tường trong bản vẽ CAD.
### Cơ khí
_Chi tiết cơ khí, ký hiệu mối hàn và các thao tác phục vụ bản vẽ cơ khí._
#### cơ khí
- [`centre_marks`](#centre_marks) — cơ khí: dùng để centre marks trong bản vẽ CAD.
- [`hatch_material`](#hatch_material) — cơ khí: dùng để tô mặt material trong bản vẽ CAD.
- [`mech_dimension_part`](#mech_dimension_part) — cơ khí: dùng để mech kích thước part trong bản vẽ CAD.
- [`mech_hole_pattern`](#mech_hole_pattern) — cơ khí: dùng để mech hole pattern trong bản vẽ CAD.
- [`mech_part_draw`](#mech_part_draw) — cơ khí: dùng để mech part draw trong bản vẽ CAD.
- [`mech_part_from_spec`](#mech_part_from_spec) — cơ khí: dùng để mech part từ spec trong bản vẽ CAD.
- [`mech_part_inspect`](#mech_part_inspect) — cơ khí: dùng để mech part inspect trong bản vẽ CAD.
- [`mech_view_add`](#mech_view_add) — cơ khí: dùng để mech góc nhìn add trong bản vẽ CAD.
- [`section_line`](#section_line) — cơ khí: dùng để mặt cắt đường trong bản vẽ CAD.
- [`std_feature_draw`](#std_feature_draw) — cơ khí: dùng để std feature draw trong bản vẽ CAD.
- [`std_part_insert`](#std_part_insert) — cơ khí: dùng để std part chèn trong bản vẽ CAD.
- [`std_part_list`](#std_part_list) — cơ khí: dùng để std part liệt kê trong bản vẽ CAD.
- [`surface_texture`](#surface_texture) — cơ khí: dùng để surface texture trong bản vẽ CAD.
- [`weld_symbol`](#weld_symbol) — cơ khí: dùng để mối hàn ký hiệu trong bản vẽ CAD.
### P&ID
_Sơ đồ đường ống và thiết bị đo lường điều khiển._
#### P&ID
- [`pid_equipment_list`](#pid_equipment_list) — P&ID: dùng để P&ID equipment liệt kê trong bản vẽ CAD.
- [`pid_from_spec`](#pid_from_spec) — P&ID: dùng để P&ID từ spec trong bản vẽ CAD.
- [`pid_graph`](#pid_graph) — P&ID: dùng để P&ID graph trong bản vẽ CAD.
- [`pid_instrument_index`](#pid_instrument_index) — P&ID: dùng để P&ID instrument index trong bản vẽ CAD.
- [`pid_line_draw`](#pid_line_draw) — P&ID: dùng để P&ID đường draw trong bản vẽ CAD.
- [`pid_line_list`](#pid_line_list) — P&ID: dùng để P&ID đường liệt kê trong bản vẽ CAD.
- [`pid_symbol_insert`](#pid_symbol_insert) — P&ID: dùng để P&ID ký hiệu chèn trong bản vẽ CAD.
- [`pid_symbol_list`](#pid_symbol_list) — P&ID: dùng để P&ID ký hiệu liệt kê trong bản vẽ CAD.
- [`pid_tag_parse`](#pid_tag_parse) — P&ID: dùng để P&ID tag parse trong bản vẽ CAD.
### Nhà máy
_Bố trí thiết bị và bản vẽ nhà máy công nghiệp._
#### nhà máy
- [`cable_takeoff`](#cable_takeoff) — nhà máy: dùng để cable takeoff trong bản vẽ CAD.
- [`pipe_takeoff`](#pipe_takeoff) — nhà máy: dùng để pipe takeoff trong bản vẽ CAD.
### Kỹ thuật và 3D
_Kiểm tra kỹ thuật và hình học khối ba chiều._
#### khối đặc
- [`solid_boolean`](#solid_boolean) — khối đặc: dùng để khối đặc boolean trong bản vẽ CAD.
- [`solid_box`](#solid_box) — khối đặc: dùng để khối đặc khung trong bản vẽ CAD.
- [`solid_cylinder`](#solid_cylinder) — khối đặc: dùng để khối đặc cylinder trong bản vẽ CAD.
- [`solid_extrude`](#solid_extrude) — khối đặc: dùng để khối đặc extrude trong bản vẽ CAD.
- [`solid_revolve`](#solid_revolve) — khối đặc: dùng để khối đặc revolve trong bản vẽ CAD.
#### kỹ thuật
- [`datum_feature`](#datum_feature) — kỹ thuật: dùng để datum feature trong bản vẽ CAD.
- [`drawing_deliver`](#drawing_deliver) — kỹ thuật: dùng để bản vẽ deliver trong bản vẽ CAD.
- [`drawing_finalize`](#drawing_finalize) — kỹ thuật: dùng để bản vẽ finalize trong bản vẽ CAD.
- [`gd_frame`](#gd_frame) — kỹ thuật: dùng để gd frame trong bản vẽ CAD.
- [`gear_draw_helical_front_view`](#gear_draw_helical_front_view) — kỹ thuật: dùng để gear draw helical front góc nhìn trong bản vẽ CAD.
- [`gear_draw_section_aa`](#gear_draw_section_aa) — kỹ thuật: dùng để gear draw mặt cắt aa trong bản vẽ CAD.
- [`gear_draw_spur_front_view`](#gear_draw_spur_front_view) — kỹ thuật: dùng để gear draw spur front góc nhìn trong bản vẽ CAD.
- [`keyway_draw_keyed_bore`](#keyway_draw_keyed_bore) — kỹ thuật: dùng để keyway draw keyed bore trong bản vẽ CAD.
- [`keyway_draw_section`](#keyway_draw_section) — kỹ thuật: dùng để keyway draw mặt cắt trong bản vẽ CAD.
- [`titleblock_apply_iso_a3`](#titleblock_apply_iso_a3) — kỹ thuật: dùng để titleblock apply iso a3 trong bản vẽ CAD.
### Nâng cao
_Các chức năng nâng cao cần kiểm tra khả năng backend trước khi dùng._
#### nâng cao
- [`construction_clear`](#construction_clear) — nâng cao: dùng để construction clear trong bản vẽ CAD.
- [`construction_xline`](#construction_xline) — nâng cao: dùng để construction xline trong bản vẽ CAD.
- [`dimension_auto`](#dimension_auto) — nâng cao: dùng để kích thước auto trong bản vẽ CAD.
- [`drawing_apply_iso_layers`](#drawing_apply_iso_layers) — nâng cao: dùng để bản vẽ apply iso layers trong bản vẽ CAD.
- [`drawing_critique`](#drawing_critique) — nâng cao: dùng để bản vẽ critique trong bản vẽ CAD.
- [`drawing_plan`](#drawing_plan) — nâng cao: dùng để bản vẽ mặt bằng trong bản vẽ CAD.
- [`drawing_preflight`](#drawing_preflight) — nâng cao: dùng để bản vẽ preflight trong bản vẽ CAD.
- [`drawing_refine`](#drawing_refine) — nâng cao: dùng để bản vẽ refine trong bản vẽ CAD.
- [`entity_select_smart`](#entity_select_smart) — nâng cao: dùng để đối tượng chọn smart trong bản vẽ CAD.
- [`point_from_snap`](#point_from_snap) — nâng cao: dùng để điểm từ snap trong bản vẽ CAD.
- [`point_intersection`](#point_intersection) — nâng cao: dùng để điểm intersection trong bản vẽ CAD.
- [`point_tangent`](#point_tangent) — nâng cao: dùng để điểm tangent trong bản vẽ CAD.
### Mở rộng cadtroly
_Các chức năng riêng của project cadtroly như tiêu chuẩn, QA và khối lượng._
#### mở rộng cadtroly
- [`check_rulesets`](#check_rulesets) — mở rộng cadtroly: dùng để kiểm tra rulesets trong bản vẽ CAD.
- [`check_run`](#check_run) — mở rộng cadtroly: dùng để kiểm tra run trong bản vẽ CAD.
- [`drawing_apply_discipline_standard`](#drawing_apply_discipline_standard) — mở rộng cadtroly: dùng để bản vẽ apply discipline standard trong bản vẽ CAD.
- [`drawing_entities`](#drawing_entities) — mở rộng cadtroly: dùng để bản vẽ đối tượng trong bản vẽ CAD.
- [`drawing_read`](#drawing_read) — mở rộng cadtroly: dùng để bản vẽ đọc trong bản vẽ CAD.
- [`kho_industries`](#kho_industries) — mở rộng cadtroly: dùng để kho industries trong bản vẽ CAD.
- [`kho_rules_export`](#kho_rules_export) — mở rộng cadtroly: dùng để kho rules xuất trong bản vẽ CAD.
- [`kho_rules_import`](#kho_rules_import) — mở rộng cadtroly: dùng để kho rules nhập trong bản vẽ CAD.
- [`kho_skill_add`](#kho_skill_add) — mở rộng cadtroly: dùng để kho skill add trong bản vẽ CAD.
- [`kho_skill_toggle`](#kho_skill_toggle) — mở rộng cadtroly: dùng để kho skill toggle trong bản vẽ CAD.
- [`kho_skills`](#kho_skills) — mở rộng cadtroly: dùng để kho skills trong bản vẽ CAD.
- [`kho_standard_add`](#kho_standard_add) — mở rộng cadtroly: dùng để kho standard add trong bản vẽ CAD.
- [`kho_standard_delete`](#kho_standard_delete) — mở rộng cadtroly: dùng để kho standard xóa trong bản vẽ CAD.
- [`kho_standards`](#kho_standards) — mở rộng cadtroly: dùng để kho standards trong bản vẽ CAD.
- [`kho_status`](#kho_status) — mở rộng cadtroly: dùng để kho trạng thái trong bản vẽ CAD.
- [`pdf_to_dwg`](#pdf_to_dwg) — mở rộng cadtroly: dùng để pdf đến dwg trong bản vẽ CAD.
- [`pdf_vectorize`](#pdf_vectorize) — mở rộng cadtroly: dùng để pdf vectorize trong bản vẽ CAD.
- [`standards_reference`](#standards_reference) — mở rộng cadtroly: dùng để standards tham chiếu trong bản vẽ CAD.
- [`structural_qa`](#structural_qa) — mở rộng cadtroly: dùng để structural qa trong bản vẽ CAD.
- [`takeoff_compute`](#takeoff_compute) — mở rộng cadtroly: dùng để takeoff compute trong bản vẽ CAD.
- [`takeoff_decide`](#takeoff_decide) — mở rộng cadtroly: dùng để takeoff decide trong bản vẽ CAD.
- [`takeoff_export`](#takeoff_export) — mở rộng cadtroly: dùng để takeoff xuất trong bản vẽ CAD.
- [`takeoff_propose`](#takeoff_propose) — mở rộng cadtroly: dùng để takeoff propose trong bản vẽ CAD.
- [`takeoff_run`](#takeoff_run) — mở rộng cadtroly: dùng để takeoff run trong bản vẽ CAD.
- [`view_render_report`](#view_render_report) — mở rộng cadtroly: dùng để góc nhìn kết xuất report trong bản vẽ CAD.

## 12. Hướng dẫn chi tiết từng chức năng

## Dùng chung
Các chức năng có thể dùng cho hầu hết bản vẽ và ngành kỹ thuật.
### bo góc và cắt nối
#### entity_chamfer

- **Nhóm:** bo góc và cắt nối
- **Làm gì:** Thực hiện thao tác đối tượng chamfer trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Hãy thực hiện đối tượng chamfer trên bản vẽ và báo cáo kết quả.

#### entity_extend

- **Nhóm:** bo góc và cắt nối
- **Làm gì:** Thực hiện thao tác đối tượng kéo dài trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Hãy thực hiện đối tượng kéo dài trên bản vẽ và báo cáo kết quả.

#### entity_fillet

- **Nhóm:** bo góc và cắt nối
- **Làm gì:** Thực hiện thao tác đối tượng fillet trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Hãy thực hiện đối tượng fillet trên bản vẽ và báo cáo kết quả.

#### entity_trim

- **Nhóm:** bo góc và cắt nối
- **Làm gì:** Thực hiện thao tác đối tượng cắt trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Hãy thực hiện đối tượng cắt trên bản vẽ và báo cáo kết quả.

### bản vẽ
#### drawing_audit

- **Nhóm:** bản vẽ
- **Làm gì:** Thực hiện thao tác bản vẽ audit trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mở, lưu, đóng hoặc xuất bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Mở bản vẽ, thực hiện bản vẽ audit, sau đó lưu ra file mới và không ghi đè file gốc.

#### drawing_close

- **Nhóm:** bản vẽ
- **Làm gì:** Thực hiện thao tác bản vẽ đóng trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mở, lưu, đóng hoặc xuất bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Mở bản vẽ, thực hiện bản vẽ đóng, sau đó lưu ra file mới và không ghi đè file gốc.

#### drawing_export_dxf

- **Nhóm:** bản vẽ
- **Làm gì:** Thực hiện thao tác bản vẽ xuất dxf trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mở, lưu, đóng hoặc xuất bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Mở bản vẽ, thực hiện bản vẽ xuất dxf, sau đó lưu ra file mới và không ghi đè file gốc.

#### drawing_export_pdf

- **Nhóm:** bản vẽ
- **Làm gì:** Thực hiện thao tác bản vẽ xuất pdf trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mở, lưu, đóng hoặc xuất bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Mở bản vẽ, thực hiện bản vẽ xuất pdf, sau đó lưu ra file mới và không ghi đè file gốc.

#### drawing_new

- **Nhóm:** bản vẽ
- **Làm gì:** Thực hiện thao tác bản vẽ new trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mở, lưu, đóng hoặc xuất bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Mở bản vẽ, thực hiện bản vẽ new, sau đó lưu ra file mới và không ghi đè file gốc.

#### drawing_open

- **Nhóm:** bản vẽ
- **Làm gì:** Thực hiện thao tác bản vẽ mở trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mở, lưu, đóng hoặc xuất bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Mở bản vẽ, thực hiện bản vẽ mở, sau đó lưu ra file mới và không ghi đè file gốc.

#### drawing_purge

- **Nhóm:** bản vẽ
- **Làm gì:** Thực hiện thao tác bản vẽ dọn dẹp trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mở, lưu, đóng hoặc xuất bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Mở bản vẽ, thực hiện bản vẽ dọn dẹp, sau đó lưu ra file mới và không ghi đè file gốc.

#### drawing_redo

- **Nhóm:** bản vẽ
- **Làm gì:** Thực hiện thao tác bản vẽ redo trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mở, lưu, đóng hoặc xuất bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Mở bản vẽ, thực hiện bản vẽ redo, sau đó lưu ra file mới và không ghi đè file gốc.

#### drawing_save

- **Nhóm:** bản vẽ
- **Làm gì:** Thực hiện thao tác bản vẽ lưu trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mở, lưu, đóng hoặc xuất bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Mở bản vẽ, thực hiện bản vẽ lưu, sau đó lưu ra file mới và không ghi đè file gốc.

#### drawing_save_as

- **Nhóm:** bản vẽ
- **Làm gì:** Thực hiện thao tác bản vẽ lưu as trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mở, lưu, đóng hoặc xuất bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Mở bản vẽ, thực hiện bản vẽ lưu as, sau đó lưu ra file mới và không ghi đè file gốc.

#### drawing_undo

- **Nhóm:** bản vẽ
- **Làm gì:** Thực hiện thao tác bản vẽ undo trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mở, lưu, đóng hoặc xuất bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Mở bản vẽ, thực hiện bản vẽ undo, sau đó lưu ra file mới và không ghi đè file gốc.

### bố cục
#### entity_change_space

- **Nhóm:** bố cục
- **Làm gì:** Thực hiện thao tác đối tượng change space trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bố cục và khung nhìn.
- **Ví dụ gõ vào LLM:**

  > Thiết lập bố cục A1 và thực hiện đối tượng change space cho khung tên và khung nhìn.

#### layout_copy

- **Nhóm:** bố cục
- **Làm gì:** Thực hiện thao tác bố cục sao chép trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bố cục và khung nhìn.
- **Ví dụ gõ vào LLM:**

  > Thiết lập bố cục A1 và thực hiện bố cục sao chép cho khung tên và khung nhìn.

#### layout_create

- **Nhóm:** bố cục
- **Làm gì:** Thực hiện thao tác bố cục tạo trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bố cục và khung nhìn.
- **Ví dụ gõ vào LLM:**

  > Thiết lập bố cục A1 và thực hiện bố cục tạo cho khung tên và khung nhìn.

#### layout_delete

- **Nhóm:** bố cục
- **Làm gì:** Thực hiện thao tác bố cục xóa trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bố cục và khung nhìn.
- **Ví dụ gõ vào LLM:**

  > Thiết lập bố cục A1 và thực hiện bố cục xóa cho khung tên và khung nhìn.

#### layout_list

- **Nhóm:** bố cục
- **Làm gì:** Thực hiện thao tác bố cục liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bố cục và khung nhìn.
- **Ví dụ gõ vào LLM:**

  > Thiết lập bố cục A1 và thực hiện bố cục liệt kê cho khung tên và khung nhìn.

#### layout_rename

- **Nhóm:** bố cục
- **Làm gì:** Thực hiện thao tác bố cục đổi tên trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bố cục và khung nhìn.
- **Ví dụ gõ vào LLM:**

  > Thiết lập bố cục A1 và thực hiện bố cục đổi tên cho khung tên và khung nhìn.

#### layout_set_current

- **Nhóm:** bố cục
- **Làm gì:** Thực hiện thao tác bố cục đặt hiện tại trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bố cục và khung nhìn.
- **Ví dụ gõ vào LLM:**

  > Thiết lập bố cục A1 và thực hiện bố cục đặt hiện tại cho khung tên và khung nhìn.

#### viewport_create

- **Nhóm:** bố cục
- **Làm gì:** Thực hiện thao tác khung nhìn tạo trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bố cục và khung nhìn.
- **Ví dụ gõ vào LLM:**

  > Thiết lập bố cục A1 và thực hiện khung nhìn tạo cho khung tên và khung nhìn.

#### viewport_delete

- **Nhóm:** bố cục
- **Làm gì:** Thực hiện thao tác khung nhìn xóa trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bố cục và khung nhìn.
- **Ví dụ gõ vào LLM:**

  > Thiết lập bố cục A1 và thực hiện khung nhìn xóa cho khung tên và khung nhìn.

#### viewport_list

- **Nhóm:** bố cục
- **Làm gì:** Thực hiện thao tác khung nhìn liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bố cục và khung nhìn.
- **Ví dụ gõ vào LLM:**

  > Thiết lập bố cục A1 và thực hiện khung nhìn liệt kê cho khung tên và khung nhìn.

#### viewport_lock

- **Nhóm:** bố cục
- **Làm gì:** Thực hiện thao tác khung nhìn khóa trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bố cục và khung nhìn.
- **Ví dụ gõ vào LLM:**

  > Thiết lập bố cục A1 và thực hiện khung nhìn khóa cho khung tên và khung nhìn.

#### viewport_set_scale

- **Nhóm:** bố cục
- **Làm gì:** Thực hiện thao tác khung nhìn đặt tỷ lệ trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bố cục và khung nhìn.
- **Ví dụ gõ vào LLM:**

  > Thiết lập bố cục A1 và thực hiện khung nhìn đặt tỷ lệ cho khung tên và khung nhìn.

### giao dịch
#### transaction_begin

- **Nhóm:** giao dịch
- **Làm gì:** Thực hiện thao tác giao dịch begin trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần giao dịch thay đổi có kiểm soát.
- **Ví dụ gõ vào LLM:**

  > Bắt đầu giao dịch, thực hiện giao dịch begin, cho tôi xem thay đổi rồi mới xác nhận.

#### transaction_commit

- **Nhóm:** giao dịch
- **Làm gì:** Thực hiện thao tác giao dịch commit trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần giao dịch thay đổi có kiểm soát.
- **Ví dụ gõ vào LLM:**

  > Bắt đầu giao dịch, thực hiện giao dịch commit, cho tôi xem thay đổi rồi mới xác nhận.

#### transaction_rollback

- **Nhóm:** giao dịch
- **Làm gì:** Thực hiện thao tác giao dịch rollback trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần giao dịch thay đổi có kiểm soát.
- **Ví dụ gõ vào LLM:**

  > Bắt đầu giao dịch, thực hiện giao dịch rollback, cho tôi xem thay đổi rồi mới xác nhận.

### góc nhìn
#### view_screenshot

- **Nhóm:** góc nhìn
- **Làm gì:** Thực hiện thao tác góc nhìn screenshot trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần thu phóng, góc nhìn và ảnh chụp.
- **Ví dụ gõ vào LLM:**

  > Chụp riêng vùng mặt bằng tầng 1, vùng khung tên và vùng kích thước bên phải.

#### view_zoom_and_screenshot

- **Nhóm:** góc nhìn
- **Làm gì:** Thực hiện thao tác góc nhìn thu phóng và screenshot trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần thu phóng, góc nhìn và ảnh chụp.
- **Ví dụ gõ vào LLM:**

  > Thu toàn bộ bản vẽ vào màn hình rồi chụp ảnh để tôi kiểm tra nhanh.

#### view_zoom_extents

- **Nhóm:** góc nhìn
- **Làm gì:** Thực hiện thao tác góc nhìn thu phóng extents trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần thu phóng, góc nhìn và ảnh chụp.
- **Ví dụ gõ vào LLM:**

  > Thu phóng để toàn bộ đối tượng của bản vẽ nằm vừa trên màn hình.

#### view_zoom_window

- **Nhóm:** góc nhìn
- **Làm gì:** Thực hiện thao tác góc nhìn thu phóng window trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần thu phóng, góc nhìn và ảnh chụp.
- **Ví dụ gõ vào LLM:**

  > Phóng to riêng vùng mặt bằng tầng 1 để nhìn rõ cửa, thiết bị và kích thước.

### hệ thống
#### drawing_settings

- **Nhóm:** hệ thống
- **Làm gì:** Thực hiện thao tác bản vẽ thiết lập trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần trạng thái máy chủ.
- **Ví dụ gõ vào LLM:**

  > Báo cáo trạng thái MCP, AutoCAD và backend bằng cách bản vẽ thiết lập.

#### system_about

- **Nhóm:** hệ thống
- **Làm gì:** Thực hiện thao tác hệ thống thông tin trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần trạng thái máy chủ.
- **Ví dụ gõ vào LLM:**

  > Báo cáo trạng thái MCP, AutoCAD và backend bằng cách hệ thống thông tin.

#### system_get_variable

- **Nhóm:** hệ thống
- **Làm gì:** Thực hiện thao tác hệ thống get variable trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần trạng thái máy chủ.
- **Ví dụ gõ vào LLM:**

  > Báo cáo trạng thái MCP, AutoCAD và backend bằng cách hệ thống get variable.

#### system_run_command

- **Nhóm:** hệ thống
- **Làm gì:** Thực hiện thao tác hệ thống run command trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần trạng thái máy chủ.
- **Ví dụ gõ vào LLM:**

  > Báo cáo trạng thái MCP, AutoCAD và backend bằng cách hệ thống run command.

#### system_run_lisp

- **Nhóm:** hệ thống
- **Làm gì:** Thực hiện thao tác hệ thống run lisp trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần trạng thái máy chủ.
- **Ví dụ gõ vào LLM:**

  > Báo cáo trạng thái MCP, AutoCAD và backend bằng cách hệ thống run lisp.

#### system_set_variable

- **Nhóm:** hệ thống
- **Làm gì:** Thực hiện thao tác hệ thống đặt variable trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần trạng thái máy chủ.
- **Ví dụ gõ vào LLM:**

  > Báo cáo trạng thái MCP, AutoCAD và backend bằng cách hệ thống đặt variable.

#### system_status

- **Nhóm:** hệ thống
- **Làm gì:** Thực hiện thao tác hệ thống trạng thái trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần trạng thái máy chủ.
- **Ví dụ gõ vào LLM:**

  > Báo cáo trạng thái MCP, AutoCAD và backend bằng cách hệ thống trạng thái.

### khối
#### block_create_from_entities

- **Nhóm:** khối
- **Làm gì:** Thực hiện thao tác khối tạo từ đối tượng trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần khối và tham chiếu khối.
- **Ví dụ gõ vào LLM:**

  > Trong bản vẽ hiện tại, hãy khối tạo từ đối tượng cho các khối cửa và thiết bị.

#### block_define

- **Nhóm:** khối
- **Làm gì:** Thực hiện thao tác khối định nghĩa trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần khối và tham chiếu khối.
- **Ví dụ gõ vào LLM:**

  > Trong bản vẽ hiện tại, hãy khối định nghĩa cho các khối cửa và thiết bị.

#### block_explode

- **Nhóm:** khối
- **Làm gì:** Thực hiện thao tác khối phá khối trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần khối và tham chiếu khối.
- **Ví dụ gõ vào LLM:**

  > Trong bản vẽ hiện tại, hãy khối phá khối cho các khối cửa và thiết bị.

#### block_find_references

- **Nhóm:** khối
- **Làm gì:** Thực hiện thao tác khối tìm tham chiếu trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần khối và tham chiếu khối.
- **Ví dụ gõ vào LLM:**

  > Trong bản vẽ hiện tại, hãy khối tìm tham chiếu cho các khối cửa và thiết bị.

#### block_get_attributes

- **Nhóm:** khối
- **Làm gì:** Thực hiện thao tác khối get attributes trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần khối và tham chiếu khối.
- **Ví dụ gõ vào LLM:**

  > Trong bản vẽ hiện tại, hãy khối get attributes cho các khối cửa và thiết bị.

#### block_insert

- **Nhóm:** khối
- **Làm gì:** Thực hiện thao tác khối chèn trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần khối và tham chiếu khối.
- **Ví dụ gõ vào LLM:**

  > Trong bản vẽ hiện tại, hãy khối chèn cho các khối cửa và thiết bị.

#### block_list

- **Nhóm:** khối
- **Làm gì:** Thực hiện thao tác khối liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần khối và tham chiếu khối.
- **Ví dụ gõ vào LLM:**

  > Trong bản vẽ hiện tại, hãy khối liệt kê cho các khối cửa và thiết bị.

#### block_set_attributes

- **Nhóm:** khối
- **Làm gì:** Thực hiện thao tác khối đặt attributes trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần khối và tham chiếu khối.
- **Ví dụ gõ vào LLM:**

  > Trong bản vẽ hiện tại, hãy khối đặt attributes cho các khối cửa và thiết bị.

#### entity_create_block_ref

- **Nhóm:** khối
- **Làm gì:** Thực hiện thao tác đối tượng tạo khối ref trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần khối và tham chiếu khối.
- **Ví dụ gõ vào LLM:**

  > Trong bản vẽ hiện tại, hãy đối tượng tạo khối ref cho các khối cửa và thiết bị.

### kiểu hiển thị
#### dimstyle_create

- **Nhóm:** kiểu hiển thị
- **Làm gì:** Thực hiện thao tác dimstyle tạo trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểu và hiển thị.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kiểu hiển thị hiện tại và thực hiện dimstyle tạo cho toàn bộ bản vẽ.

#### dimstyle_list

- **Nhóm:** kiểu hiển thị
- **Làm gì:** Thực hiện thao tác dimstyle liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểu và hiển thị.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kiểu hiển thị hiện tại và thực hiện dimstyle liệt kê cho toàn bộ bản vẽ.

#### dimstyle_modify

- **Nhóm:** kiểu hiển thị
- **Làm gì:** Thực hiện thao tác dimstyle sửa trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểu và hiển thị.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kiểu hiển thị hiện tại và thực hiện dimstyle sửa cho toàn bộ bản vẽ.

#### dimstyle_set_current

- **Nhóm:** kiểu hiển thị
- **Làm gì:** Thực hiện thao tác dimstyle đặt hiện tại trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểu và hiển thị.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kiểu hiển thị hiện tại và thực hiện dimstyle đặt hiện tại cho toàn bộ bản vẽ.

#### drawing_apply_standard

- **Nhóm:** kiểu hiển thị
- **Làm gì:** Thực hiện thao tác bản vẽ apply standard trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểu và hiển thị.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kiểu hiển thị hiện tại và thực hiện bản vẽ apply standard cho toàn bộ bản vẽ.

#### mleaderstyle_create

- **Nhóm:** kiểu hiển thị
- **Làm gì:** Thực hiện thao tác mleaderstyle tạo trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểu và hiển thị.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kiểu hiển thị hiện tại và thực hiện mleaderstyle tạo cho toàn bộ bản vẽ.

#### mleaderstyle_list

- **Nhóm:** kiểu hiển thị
- **Làm gì:** Thực hiện thao tác mleaderstyle liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểu và hiển thị.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kiểu hiển thị hiện tại và thực hiện mleaderstyle liệt kê cho toàn bộ bản vẽ.

#### textstyle_create

- **Nhóm:** kiểu hiển thị
- **Làm gì:** Thực hiện thao tác textstyle tạo trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểu và hiển thị.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kiểu hiển thị hiện tại và thực hiện textstyle tạo cho toàn bộ bản vẽ.

#### textstyle_list

- **Nhóm:** kiểu hiển thị
- **Làm gì:** Thực hiện thao tác textstyle liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểu và hiển thị.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kiểu hiển thị hiện tại và thực hiện textstyle liệt kê cho toàn bộ bản vẽ.

#### textstyle_set_current

- **Nhóm:** kiểu hiển thị
- **Làm gì:** Thực hiện thao tác textstyle đặt hiện tại trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểu và hiển thị.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kiểu hiển thị hiện tại và thực hiện textstyle đặt hiện tại cho toàn bộ bản vẽ.

### kích thước
#### dimension_aligned

- **Nhóm:** kích thước
- **Làm gì:** Thực hiện thao tác kích thước aligned trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kích thước và ghi chú đo.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra và thực hiện kích thước aligned cho các kích thước của mặt bằng tầng 1.

#### dimension_angular

- **Nhóm:** kích thước
- **Làm gì:** Thực hiện thao tác kích thước angular trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kích thước và ghi chú đo.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra và thực hiện kích thước angular cho các kích thước của mặt bằng tầng 1.

#### dimension_diameter

- **Nhóm:** kích thước
- **Làm gì:** Thực hiện thao tác kích thước diameter trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kích thước và ghi chú đo.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra và thực hiện kích thước diameter cho các kích thước của mặt bằng tầng 1.

#### dimension_linear

- **Nhóm:** kích thước
- **Làm gì:** Thực hiện thao tác kích thước linear trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kích thước và ghi chú đo.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra và thực hiện kích thước linear cho các kích thước của mặt bằng tầng 1.

#### dimension_radius

- **Nhóm:** kích thước
- **Làm gì:** Thực hiện thao tác kích thước radius trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kích thước và ghi chú đo.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra và thực hiện kích thước radius cho các kích thước của mặt bằng tầng 1.

### lớp bản vẽ
#### layer_create

- **Nhóm:** lớp bản vẽ
- **Làm gì:** Thực hiện thao tác lớp tạo trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tạo và quản lý lớp bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp tạo, không tự đổi tiêu chuẩn nếu chưa hỏi.

#### layer_delete

- **Nhóm:** lớp bản vẽ
- **Làm gì:** Thực hiện thao tác lớp xóa trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tạo và quản lý lớp bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp xóa, không tự đổi tiêu chuẩn nếu chưa hỏi.

#### layer_freeze

- **Nhóm:** lớp bản vẽ
- **Làm gì:** Thực hiện thao tác lớp freeze trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tạo và quản lý lớp bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp freeze, không tự đổi tiêu chuẩn nếu chưa hỏi.

#### layer_hide

- **Nhóm:** lớp bản vẽ
- **Làm gì:** Thực hiện thao tác lớp hide trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tạo và quản lý lớp bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp hide, không tự đổi tiêu chuẩn nếu chưa hỏi.

#### layer_isolate

- **Nhóm:** lớp bản vẽ
- **Làm gì:** Thực hiện thao tác lớp isolate trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tạo và quản lý lớp bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp isolate, không tự đổi tiêu chuẩn nếu chưa hỏi.

#### layer_list

- **Nhóm:** lớp bản vẽ
- **Làm gì:** Thực hiện thao tác lớp liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tạo và quản lý lớp bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp liệt kê, không tự đổi tiêu chuẩn nếu chưa hỏi.

#### layer_lock

- **Nhóm:** lớp bản vẽ
- **Làm gì:** Thực hiện thao tác lớp khóa trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tạo và quản lý lớp bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp khóa, không tự đổi tiêu chuẩn nếu chưa hỏi.

#### layer_modify

- **Nhóm:** lớp bản vẽ
- **Làm gì:** Thực hiện thao tác lớp sửa trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tạo và quản lý lớp bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp sửa, không tự đổi tiêu chuẩn nếu chưa hỏi.

#### layer_set_current

- **Nhóm:** lớp bản vẽ
- **Làm gì:** Thực hiện thao tác lớp đặt hiện tại trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tạo và quản lý lớp bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp đặt hiện tại, không tự đổi tiêu chuẩn nếu chưa hỏi.

#### layer_show

- **Nhóm:** lớp bản vẽ
- **Làm gì:** Thực hiện thao tác lớp show trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tạo và quản lý lớp bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp show, không tự đổi tiêu chuẩn nếu chưa hỏi.

#### layer_thaw

- **Nhóm:** lớp bản vẽ
- **Làm gì:** Thực hiện thao tác lớp thaw trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tạo và quản lý lớp bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp thaw, không tự đổi tiêu chuẩn nếu chưa hỏi.

#### layer_unlock

- **Nhóm:** lớp bản vẽ
- **Làm gì:** Thực hiện thao tác lớp unlock trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tạo và quản lý lớp bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Tổ chức các đối tượng theo lớp bản vẽ bằng cách lớp unlock, không tự đổi tiêu chuẩn nếu chưa hỏi.

#### linetype_list

- **Nhóm:** lớp bản vẽ
- **Làm gì:** Thực hiện thao tác linetype liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tạo và quản lý lớp bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Tổ chức các đối tượng theo lớp bản vẽ bằng cách linetype liệt kê, không tự đổi tiêu chuẩn nếu chưa hỏi.

#### linetype_load

- **Nhóm:** lớp bản vẽ
- **Làm gì:** Thực hiện thao tác linetype nạp trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tạo và quản lý lớp bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Tổ chức các đối tượng theo lớp bản vẽ bằng cách linetype nạp, không tự đổi tiêu chuẩn nếu chưa hỏi.

### môi trường
#### document_activate

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác document activate trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo document activate trước khi thao tác bản vẽ.

#### document_close

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác document đóng trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo document đóng trước khi thao tác bản vẽ.

#### document_list

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác document liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo document liệt kê trước khi thao tác bản vẽ.

#### drawing_properties_get

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác bản vẽ thuộc tính get trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo bản vẽ thuộc tính get trước khi thao tác bản vẽ.

#### drawing_properties_set

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác bản vẽ thuộc tính đặt trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo bản vẽ thuộc tính đặt trước khi thao tác bản vẽ.

#### layer_state_delete

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác lớp state xóa trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo lớp state xóa trước khi thao tác bản vẽ.

#### layer_state_list

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác lớp state liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo lớp state liệt kê trước khi thao tác bản vẽ.

#### layer_state_restore

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác lớp state restore trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo lớp state restore trước khi thao tác bản vẽ.

#### layer_state_save

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác lớp state lưu trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo lớp state lưu trước khi thao tác bản vẽ.

#### system_launch

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác hệ thống launch trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo hệ thống launch trước khi thao tác bản vẽ.

#### system_preferences_get

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác hệ thống preferences get trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo hệ thống preferences get trước khi thao tác bản vẽ.

#### system_preferences_set

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác hệ thống preferences đặt trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo hệ thống preferences đặt trước khi thao tác bản vẽ.

#### system_prompt_message

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác hệ thống prompt message trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo hệ thống prompt message trước khi thao tác bản vẽ.

#### system_variable_describe

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác hệ thống variable describe trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo hệ thống variable describe trước khi thao tác bản vẽ.

#### ucs_list

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác ucs liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo ucs liệt kê trước khi thao tác bản vẽ.

#### ucs_restore

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác ucs restore trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo ucs restore trước khi thao tác bản vẽ.

#### ucs_set

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác ucs đặt trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo ucs đặt trước khi thao tác bản vẽ.

#### user_pick_point

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác user pick điểm trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo user pick điểm trước khi thao tác bản vẽ.

#### user_select

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác user chọn trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo user chọn trước khi thao tác bản vẽ.

#### view_named_list

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác góc nhìn named liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo góc nhìn named liệt kê trước khi thao tác bản vẽ.

#### view_named_restore

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác góc nhìn named restore trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo góc nhìn named restore trước khi thao tác bản vẽ.

#### view_named_save

- **Nhóm:** môi trường
- **Làm gì:** Thực hiện thao tác góc nhìn named lưu trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kết nối và cấu hình.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra kết nối AutoCAD và báo cáo góc nhìn named lưu trước khi thao tác bản vẽ.

### mẫu bản vẽ
#### template_apply_layers

- **Nhóm:** mẫu bản vẽ
- **Làm gì:** Thực hiện thao tác mẫu apply layers trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mẫu bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Tạo bản vẽ mới từ mẫu dự án rồi thực hiện mẫu apply layers theo tiêu chuẩn đã chọn.

#### template_list

- **Nhóm:** mẫu bản vẽ
- **Làm gì:** Thực hiện thao tác mẫu liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mẫu bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Tạo bản vẽ mới từ mẫu dự án rồi thực hiện mẫu liệt kê theo tiêu chuẩn đã chọn.

### phân tích
#### analysis_bounding_box

- **Nhóm:** phân tích
- **Làm gì:** Thực hiện thao tác phân tích giới hạn khung trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần đọc/đo/phân tích, không sửa bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Đọc bản vẽ và báo cáo phân tích giới hạn khung; không sửa file gốc.

#### analysis_entity_stats

- **Nhóm:** phân tích
- **Làm gì:** Thực hiện thao tác phân tích đối tượng thống kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần đọc/đo/phân tích, không sửa bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Đọc bản vẽ và báo cáo phân tích đối tượng thống kê; không sửa file gốc.

#### analysis_find_in_region

- **Nhóm:** phân tích
- **Làm gì:** Thực hiện thao tác phân tích tìm trong vùng trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần đọc/đo/phân tích, không sửa bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Đọc bản vẽ và báo cáo phân tích tìm trong vùng; không sửa file gốc.

#### analysis_layer_stats

- **Nhóm:** phân tích
- **Làm gì:** Thực hiện thao tác phân tích lớp thống kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần đọc/đo/phân tích, không sửa bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Đọc bản vẽ và báo cáo phân tích lớp thống kê; không sửa file gốc.

#### analysis_list_properties

- **Nhóm:** phân tích
- **Làm gì:** Thực hiện thao tác phân tích liệt kê thuộc tính trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần đọc/đo/phân tích, không sửa bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Đọc bản vẽ và báo cáo phân tích liệt kê thuộc tính; không sửa file gốc.

#### analysis_measure_area

- **Nhóm:** phân tích
- **Làm gì:** Thực hiện thao tác phân tích đo diện tích trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần đọc/đo/phân tích, không sửa bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Đọc bản vẽ và báo cáo phân tích đo diện tích; không sửa file gốc.

#### analysis_measure_distance

- **Nhóm:** phân tích
- **Làm gì:** Thực hiện thao tác phân tích đo khoảng cách trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần đọc/đo/phân tích, không sửa bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Đọc bản vẽ và báo cáo phân tích đo khoảng cách; không sửa file gốc.

#### analysis_measure_entity

- **Nhóm:** phân tích
- **Làm gì:** Thực hiện thao tác phân tích đo đối tượng trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần đọc/đo/phân tích, không sửa bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Đọc bản vẽ và báo cáo phân tích đo đối tượng; không sửa file gốc.

#### analysis_select_by_layer

- **Nhóm:** phân tích
- **Làm gì:** Thực hiện thao tác phân tích chọn theo lớp trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần đọc/đo/phân tích, không sửa bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Đọc bản vẽ và báo cáo phân tích chọn theo lớp; không sửa file gốc.

#### analysis_select_by_type

- **Nhóm:** phân tích
- **Làm gì:** Thực hiện thao tác phân tích chọn theo loại trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần đọc/đo/phân tích, không sửa bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Đọc bản vẽ và báo cáo phân tích chọn theo loại; không sửa file gốc.

#### boundary_from_entities

- **Nhóm:** phân tích
- **Làm gì:** Thực hiện thao tác boundary từ đối tượng trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần đọc/đo/phân tích, không sửa bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Đọc bản vẽ và báo cáo boundary từ đối tượng; không sửa file gốc.

#### boundary_trace

- **Nhóm:** phân tích
- **Làm gì:** Thực hiện thao tác boundary trace trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần đọc/đo/phân tích, không sửa bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Đọc bản vẽ và báo cáo boundary trace; không sửa file gốc.

### sửa đối tượng
#### entity_array_polar

- **Nhóm:** sửa đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng array polar trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sửa hoặc biến đổi đối tượng.
- **Ví dụ gõ vào LLM:**

  > Chụp ảnh trước, thực hiện đối tượng array polar, chụp ảnh sau và liệt kê các đối tượng đã đổi.

#### entity_array_rectangular

- **Nhóm:** sửa đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng array rectangular trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sửa hoặc biến đổi đối tượng.
- **Ví dụ gõ vào LLM:**

  > Chụp ảnh trước, thực hiện đối tượng array rectangular, chụp ảnh sau và liệt kê các đối tượng đã đổi.

#### entity_copy

- **Nhóm:** sửa đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng sao chép trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sửa hoặc biến đổi đối tượng.
- **Ví dụ gõ vào LLM:**

  > Chụp ảnh trước, thực hiện đối tượng sao chép, chụp ảnh sau và liệt kê các đối tượng đã đổi.

#### entity_delete

- **Nhóm:** sửa đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng xóa trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sửa hoặc biến đổi đối tượng.
- **Ví dụ gõ vào LLM:**

  > Chụp ảnh trước, thực hiện đối tượng xóa, chụp ảnh sau và liệt kê các đối tượng đã đổi.

#### entity_delete_many

- **Nhóm:** sửa đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng xóa many trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sửa hoặc biến đổi đối tượng.
- **Ví dụ gõ vào LLM:**

  > Chụp ảnh trước, thực hiện đối tượng xóa many, chụp ảnh sau và liệt kê các đối tượng đã đổi.

#### entity_edit_geometry

- **Nhóm:** sửa đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng edit geometry trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sửa hoặc biến đổi đối tượng.
- **Ví dụ gõ vào LLM:**

  > Chụp ảnh trước, thực hiện đối tượng edit geometry, chụp ảnh sau và liệt kê các đối tượng đã đổi.

#### entity_edit_text

- **Nhóm:** sửa đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng edit chữ trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sửa hoặc biến đổi đối tượng.
- **Ví dụ gõ vào LLM:**

  > Chụp ảnh trước, thực hiện đối tượng edit chữ, chụp ảnh sau và liệt kê các đối tượng đã đổi.

#### entity_mirror

- **Nhóm:** sửa đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng đối xứng trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sửa hoặc biến đổi đối tượng.
- **Ví dụ gõ vào LLM:**

  > Chụp ảnh trước, thực hiện đối tượng đối xứng, chụp ảnh sau và liệt kê các đối tượng đã đổi.

#### entity_move

- **Nhóm:** sửa đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng di chuyển trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sửa hoặc biến đổi đối tượng.
- **Ví dụ gõ vào LLM:**

  > Chụp ảnh trước, thực hiện đối tượng di chuyển, chụp ảnh sau và liệt kê các đối tượng đã đổi.

#### entity_offset

- **Nhóm:** sửa đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng song song trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sửa hoặc biến đổi đối tượng.
- **Ví dụ gõ vào LLM:**

  > Chụp ảnh trước, thực hiện đối tượng song song, chụp ảnh sau và liệt kê các đối tượng đã đổi.

#### entity_rotate

- **Nhóm:** sửa đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng xoay trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sửa hoặc biến đổi đối tượng.
- **Ví dụ gõ vào LLM:**

  > Chụp ảnh trước, thực hiện đối tượng xoay, chụp ảnh sau và liệt kê các đối tượng đã đổi.

#### entity_scale

- **Nhóm:** sửa đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng tỷ lệ trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sửa hoặc biến đổi đối tượng.
- **Ví dụ gõ vào LLM:**

  > Chụp ảnh trước, thực hiện đối tượng tỷ lệ, chụp ảnh sau và liệt kê các đối tượng đã đổi.

#### entity_set_properties

- **Nhóm:** sửa đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng đặt thuộc tính trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sửa hoặc biến đổi đối tượng.
- **Ví dụ gõ vào LLM:**

  > Chụp ảnh trước, thực hiện đối tượng đặt thuộc tính, chụp ảnh sau và liệt kê các đối tượng đã đổi.

#### entity_set_xdata

- **Nhóm:** sửa đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng đặt xdata trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sửa hoặc biến đổi đối tượng.
- **Ví dụ gõ vào LLM:**

  > Chụp ảnh trước, thực hiện đối tượng đặt xdata, chụp ảnh sau và liệt kê các đối tượng đã đổi.

#### text_find_replace

- **Nhóm:** sửa đối tượng
- **Làm gì:** Thực hiện thao tác chữ tìm replace trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sửa hoặc biến đổi đối tượng.
- **Ví dụ gõ vào LLM:**

  > Chụp ảnh trước, thực hiện chữ tìm replace, chụp ảnh sau và liệt kê các đối tượng đã đổi.

#### text_set_background

- **Nhóm:** sửa đối tượng
- **Làm gì:** Thực hiện thao tác chữ đặt background trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sửa hoặc biến đổi đối tượng.
- **Ví dụ gõ vào LLM:**

  > Chụp ảnh trước, thực hiện chữ đặt background, chụp ảnh sau và liệt kê các đối tượng đã đổi.

### thiết lập trang
#### batch_plot

- **Nhóm:** thiết lập trang
- **Làm gì:** Thực hiện thao tác hàng loạt plot trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần khổ giấy, tỷ lệ và in ấn.
- **Ví dụ gõ vào LLM:**

  > Thiết lập khổ A1, tỷ lệ 1:100 rồi thực hiện hàng loạt plot để chuẩn bị phát hành.

#### drawing_template_list

- **Nhóm:** thiết lập trang
- **Làm gì:** Thực hiện thao tác bản vẽ mẫu liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần khổ giấy, tỷ lệ và in ấn.
- **Ví dụ gõ vào LLM:**

  > Thiết lập khổ A1, tỷ lệ 1:100 rồi thực hiện bản vẽ mẫu liệt kê để chuẩn bị phát hành.

#### drawing_template_save

- **Nhóm:** thiết lập trang
- **Làm gì:** Thực hiện thao tác bản vẽ mẫu lưu trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần khổ giấy, tỷ lệ và in ấn.
- **Ví dụ gõ vào LLM:**

  > Thiết lập khổ A1, tỷ lệ 1:100 rồi thực hiện bản vẽ mẫu lưu để chuẩn bị phát hành.

#### page_setup_apply

- **Nhóm:** thiết lập trang
- **Làm gì:** Thực hiện thao tác trang cài đặt apply trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần khổ giấy, tỷ lệ và in ấn.
- **Ví dụ gõ vào LLM:**

  > Thiết lập khổ A1, tỷ lệ 1:100 rồi thực hiện trang cài đặt apply để chuẩn bị phát hành.

#### page_setup_list

- **Nhóm:** thiết lập trang
- **Làm gì:** Thực hiện thao tác trang cài đặt liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần khổ giấy, tỷ lệ và in ấn.
- **Ví dụ gõ vào LLM:**

  > Thiết lập khổ A1, tỷ lệ 1:100 rồi thực hiện trang cài đặt liệt kê để chuẩn bị phát hành.

#### plot_style_list

- **Nhóm:** thiết lập trang
- **Làm gì:** Thực hiện thao tác plot kiểu liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần khổ giấy, tỷ lệ và in ấn.
- **Ví dụ gõ vào LLM:**

  > Thiết lập khổ A1, tỷ lệ 1:100 rồi thực hiện plot kiểu liệt kê để chuẩn bị phát hành.

### tra cứu đối tượng
#### drawing_info

- **Nhóm:** tra cứu đối tượng
- **Làm gì:** Thực hiện thao tác bản vẽ info trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tìm và đọc thuộc tính đối tượng.
- **Ví dụ gõ vào LLM:**

  > Tìm các đối tượng liên quan rồi báo cáo bản vẽ info, không thay đổi hình học.

#### entity_get

- **Nhóm:** tra cứu đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng get trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tìm và đọc thuộc tính đối tượng.
- **Ví dụ gõ vào LLM:**

  > Tìm các đối tượng liên quan rồi báo cáo đối tượng get, không thay đổi hình học.

#### entity_get_xdata

- **Nhóm:** tra cứu đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng get xdata trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tìm và đọc thuộc tính đối tượng.
- **Ví dụ gõ vào LLM:**

  > Tìm các đối tượng liên quan rồi báo cáo đối tượng get xdata, không thay đổi hình học.

#### entity_list

- **Nhóm:** tra cứu đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tìm và đọc thuộc tính đối tượng.
- **Ví dụ gõ vào LLM:**

  > Tìm các đối tượng liên quan rồi báo cáo đối tượng liệt kê, không thay đổi hình học.

#### selection_filter

- **Nhóm:** tra cứu đối tượng
- **Làm gì:** Thực hiện thao tác selection filter trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tìm và đọc thuộc tính đối tượng.
- **Ví dụ gõ vào LLM:**

  > Tìm các đối tượng liên quan rồi báo cáo selection filter, không thay đổi hình học.

#### selection_get

- **Nhóm:** tra cứu đối tượng
- **Làm gì:** Thực hiện thao tác selection get trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tìm và đọc thuộc tính đối tượng.
- **Ví dụ gõ vào LLM:**

  > Tìm các đối tượng liên quan rồi báo cáo selection get, không thay đổi hình học.

#### selection_polygon

- **Nhóm:** tra cứu đối tượng
- **Làm gì:** Thực hiện thao tác selection đa giác trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tìm và đọc thuộc tính đối tượng.
- **Ví dụ gõ vào LLM:**

  > Tìm các đối tượng liên quan rồi báo cáo selection đa giác, không thay đổi hình học.

#### selection_window

- **Nhóm:** tra cứu đối tượng
- **Làm gì:** Thực hiện thao tác selection window trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tìm và đọc thuộc tính đối tượng.
- **Ví dụ gõ vào LLM:**

  > Tìm các đối tượng liên quan rồi báo cáo selection window, không thay đổi hình học.

#### system_capabilities

- **Nhóm:** tra cứu đối tượng
- **Làm gì:** Thực hiện thao tác hệ thống capabilities trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tìm và đọc thuộc tính đối tượng.
- **Ví dụ gõ vào LLM:**

  > Tìm các đối tượng liên quan rồi báo cáo hệ thống capabilities, không thay đổi hình học.

### tạo đối tượng
#### entity_create_arc

- **Nhóm:** tạo đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng tạo cung trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần vẽ thêm đối tượng.
- **Ví dụ gõ vào LLM:**

  > Vẽ thêm đối tượng cần thiết để đối tượng tạo cung, đặt đúng lớp bản vẽ và ghi chú rõ ràng.

#### entity_create_circle

- **Nhóm:** tạo đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng tạo đường tròn trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần vẽ thêm đối tượng.
- **Ví dụ gõ vào LLM:**

  > Vẽ thêm đối tượng cần thiết để đối tượng tạo đường tròn, đặt đúng lớp bản vẽ và ghi chú rõ ràng.

#### entity_create_ellipse

- **Nhóm:** tạo đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng tạo ellipse trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần vẽ thêm đối tượng.
- **Ví dụ gõ vào LLM:**

  > Vẽ thêm đối tượng cần thiết để đối tượng tạo ellipse, đặt đúng lớp bản vẽ và ghi chú rõ ràng.

#### entity_create_hatch

- **Nhóm:** tạo đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng tạo tô mặt trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần vẽ thêm đối tượng.
- **Ví dụ gõ vào LLM:**

  > Vẽ thêm đối tượng cần thiết để đối tượng tạo tô mặt, đặt đúng lớp bản vẽ và ghi chú rõ ràng.

#### entity_create_line

- **Nhóm:** tạo đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng tạo đường trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần vẽ thêm đối tượng.
- **Ví dụ gõ vào LLM:**

  > Vẽ thêm đối tượng cần thiết để đối tượng tạo đường, đặt đúng lớp bản vẽ và ghi chú rõ ràng.

#### entity_create_mtext

- **Nhóm:** tạo đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng tạo mtext trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần vẽ thêm đối tượng.
- **Ví dụ gõ vào LLM:**

  > Vẽ thêm đối tượng cần thiết để đối tượng tạo mtext, đặt đúng lớp bản vẽ và ghi chú rõ ràng.

#### entity_create_point

- **Nhóm:** tạo đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng tạo điểm trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần vẽ thêm đối tượng.
- **Ví dụ gõ vào LLM:**

  > Vẽ thêm đối tượng cần thiết để đối tượng tạo điểm, đặt đúng lớp bản vẽ và ghi chú rõ ràng.

#### entity_create_polyline

- **Nhóm:** tạo đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng tạo đa tuyến trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần vẽ thêm đối tượng.
- **Ví dụ gõ vào LLM:**

  > Vẽ thêm đối tượng cần thiết để đối tượng tạo đa tuyến, đặt đúng lớp bản vẽ và ghi chú rõ ràng.

#### entity_create_rectangle

- **Nhóm:** tạo đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng tạo hình chữ nhật trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần vẽ thêm đối tượng.
- **Ví dụ gõ vào LLM:**

  > Vẽ thêm đối tượng cần thiết để đối tượng tạo hình chữ nhật, đặt đúng lớp bản vẽ và ghi chú rõ ràng.

#### entity_create_revcloud

- **Nhóm:** tạo đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng tạo revcloud trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần vẽ thêm đối tượng.
- **Ví dụ gõ vào LLM:**

  > Vẽ thêm đối tượng cần thiết để đối tượng tạo revcloud, đặt đúng lớp bản vẽ và ghi chú rõ ràng.

#### entity_create_spline

- **Nhóm:** tạo đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng tạo spline trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần vẽ thêm đối tượng.
- **Ví dụ gõ vào LLM:**

  > Vẽ thêm đối tượng cần thiết để đối tượng tạo spline, đặt đúng lớp bản vẽ và ghi chú rõ ràng.

#### entity_create_table

- **Nhóm:** tạo đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng tạo bảng trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần vẽ thêm đối tượng.
- **Ví dụ gõ vào LLM:**

  > Vẽ thêm đối tượng cần thiết để đối tượng tạo bảng, đặt đúng lớp bản vẽ và ghi chú rõ ràng.

#### entity_create_text

- **Nhóm:** tạo đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng tạo chữ trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần vẽ thêm đối tượng.
- **Ví dụ gõ vào LLM:**

  > Vẽ thêm đối tượng cần thiết để đối tượng tạo chữ, đặt đúng lớp bản vẽ và ghi chú rõ ràng.

#### entity_create_wipeout

- **Nhóm:** tạo đối tượng
- **Làm gì:** Thực hiện thao tác đối tượng tạo wipeout trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần vẽ thêm đối tượng.
- **Ví dụ gõ vào LLM:**

  > Vẽ thêm đối tượng cần thiết để đối tượng tạo wipeout, đặt đúng lớp bản vẽ và ghi chú rõ ràng.

#### hatch_add_boundary

- **Nhóm:** tạo đối tượng
- **Làm gì:** Thực hiện thao tác tô mặt add boundary trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần vẽ thêm đối tượng.
- **Ví dụ gõ vào LLM:**

  > Vẽ thêm đối tượng cần thiết để tô mặt add boundary, đặt đúng lớp bản vẽ và ghi chú rõ ràng.

#### hatch_edit

- **Nhóm:** tạo đối tượng
- **Làm gì:** Thực hiện thao tác tô mặt edit trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần vẽ thêm đối tượng.
- **Ví dụ gõ vào LLM:**

  > Vẽ thêm đối tượng cần thiết để tô mặt edit, đặt đúng lớp bản vẽ và ghi chú rõ ràng.

#### hatch_set_gradient

- **Nhóm:** tạo đối tượng
- **Làm gì:** Thực hiện thao tác tô mặt đặt gradient trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần vẽ thêm đối tượng.
- **Ví dụ gõ vào LLM:**

  > Vẽ thêm đối tượng cần thiết để tô mặt đặt gradient, đặt đúng lớp bản vẽ và ghi chú rõ ràng.

#### leader_create_mleader

- **Nhóm:** tạo đối tượng
- **Làm gì:** Thực hiện thao tác đường dẫn tạo mleader trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần vẽ thêm đối tượng.
- **Ví dụ gõ vào LLM:**

  > Vẽ thêm đối tượng cần thiết để đường dẫn tạo mleader, đặt đúng lớp bản vẽ và ghi chú rõ ràng.

### tờ bản vẽ
#### balloon_add

- **Nhóm:** tờ bản vẽ
- **Làm gì:** Thực hiện thao tác balloon add trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tờ bản vẽ, khung tên và phát hành.
- **Ví dụ gõ vào LLM:**

  > Chuẩn bị tờ bản vẽ phát hành và thực hiện balloon add trong khung tên.

#### bom_extract

- **Nhóm:** tờ bản vẽ
- **Làm gì:** Thực hiện thao tác bom extract trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tờ bản vẽ, khung tên và phát hành.
- **Ví dụ gõ vào LLM:**

  > Chuẩn bị tờ bản vẽ phát hành và thực hiện bom extract trong khung tên.

#### bom_table

- **Nhóm:** tờ bản vẽ
- **Làm gì:** Thực hiện thao tác bom bảng trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tờ bản vẽ, khung tên và phát hành.
- **Ví dụ gõ vào LLM:**

  > Chuẩn bị tờ bản vẽ phát hành và thực hiện bom bảng trong khung tên.

#### data_extract

- **Nhóm:** tờ bản vẽ
- **Làm gì:** Thực hiện thao tác dữ liệu extract trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tờ bản vẽ, khung tên và phát hành.
- **Ví dụ gõ vào LLM:**

  > Chuẩn bị tờ bản vẽ phát hành và thực hiện dữ liệu extract trong khung tên.

#### drawing_export_dwg

- **Nhóm:** tờ bản vẽ
- **Làm gì:** Thực hiện thao tác bản vẽ xuất dwg trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tờ bản vẽ, khung tên và phát hành.
- **Ví dụ gõ vào LLM:**

  > Chuẩn bị tờ bản vẽ phát hành và thực hiện bản vẽ xuất dwg trong khung tên.

#### image_attach

- **Nhóm:** tờ bản vẽ
- **Làm gì:** Thực hiện thao tác hình ảnh đính kèm trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tờ bản vẽ, khung tên và phát hành.
- **Ví dụ gõ vào LLM:**

  > Chuẩn bị tờ bản vẽ phát hành và thực hiện hình ảnh đính kèm trong khung tên.

#### revision_add

- **Nhóm:** tờ bản vẽ
- **Làm gì:** Thực hiện thao tác revision add trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tờ bản vẽ, khung tên và phát hành.
- **Ví dụ gõ vào LLM:**

  > Chuẩn bị tờ bản vẽ phát hành và thực hiện revision add trong khung tên.

#### sheet_frame

- **Nhóm:** tờ bản vẽ
- **Làm gì:** Thực hiện thao tác tờ bản vẽ frame trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tờ bản vẽ, khung tên và phát hành.
- **Ví dụ gõ vào LLM:**

  > Chuẩn bị tờ bản vẽ phát hành và thực hiện tờ bản vẽ frame trong khung tên.

#### titleblock_apply

- **Nhóm:** tờ bản vẽ
- **Làm gì:** Thực hiện thao tác titleblock apply trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tờ bản vẽ, khung tên và phát hành.
- **Ví dụ gõ vào LLM:**

  > Chuẩn bị tờ bản vẽ phát hành và thực hiện titleblock apply trong khung tên.

#### xref_attach

- **Nhóm:** tờ bản vẽ
- **Làm gì:** Thực hiện thao tác tham chiếu ngoài đính kèm trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tờ bản vẽ, khung tên và phát hành.
- **Ví dụ gõ vào LLM:**

  > Chuẩn bị tờ bản vẽ phát hành và thực hiện tham chiếu ngoài đính kèm trong khung tên.

#### xref_manage

- **Nhóm:** tờ bản vẽ
- **Làm gì:** Thực hiện thao tác tham chiếu ngoài quản lý trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần tờ bản vẽ, khung tên và phát hành.
- **Ví dụ gõ vào LLM:**

  > Chuẩn bị tờ bản vẽ phát hành và thực hiện tham chiếu ngoài quản lý trong khung tên.

### xác nhận
#### validation_check

- **Nhóm:** xác nhận
- **Làm gì:** Thực hiện thao tác validation kiểm tra trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra hợp lệ.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra bản vẽ và báo cáo validation kiểm tra theo mức Error, Warning và Info.

### xử lý hàng loạt
#### cad_batch

- **Nhóm:** xử lý hàng loạt
- **Làm gì:** Thực hiện thao tác cad hàng loạt trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần xử lý hàng loạt.
- **Ví dụ gõ vào LLM:**

  > Thực hiện cad hàng loạt cho tất cả bản vẽ trong thư mục dự án và báo cáo từng file.

#### entity_batch_create

- **Nhóm:** xử lý hàng loạt
- **Làm gì:** Thực hiện thao tác đối tượng hàng loạt tạo trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần xử lý hàng loạt.
- **Ví dụ gõ vào LLM:**

  > Thực hiện đối tượng hàng loạt tạo cho tất cả bản vẽ trong thư mục dự án và báo cáo từng file.

#### entity_batch_modify

- **Nhóm:** xử lý hàng loạt
- **Làm gì:** Thực hiện thao tác đối tượng hàng loạt sửa trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần xử lý hàng loạt.
- **Ví dụ gõ vào LLM:**

  > Thực hiện đối tượng hàng loạt sửa cho tất cả bản vẽ trong thư mục dự án và báo cáo từng file.

### đọc hiểu
#### drawing_diff

- **Nhóm:** đọc hiểu
- **Làm gì:** Thực hiện thao tác bản vẽ diff trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần đọc hiểu cấu trúc bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Đọc hiểu bản vẽ và giải thích bản vẽ diff bằng ngôn ngữ dễ hiểu cho người dùng.

#### drawing_scale_check

- **Nhóm:** đọc hiểu
- **Làm gì:** Thực hiện thao tác bản vẽ tỷ lệ kiểm tra trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần đọc hiểu cấu trúc bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Đọc hiểu bản vẽ và giải thích bản vẽ tỷ lệ kiểm tra bằng ngôn ngữ dễ hiểu cho người dùng.

#### drawing_topology_check

- **Nhóm:** đọc hiểu
- **Làm gì:** Thực hiện thao tác bản vẽ topology kiểm tra trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần đọc hiểu cấu trúc bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Đọc hiểu bản vẽ và giải thích bản vẽ topology kiểm tra bằng ngôn ngữ dễ hiểu cho người dùng.

#### drawing_understand

- **Nhóm:** đọc hiểu
- **Làm gì:** Thực hiện thao tác bản vẽ understand trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần đọc hiểu cấu trúc bản vẽ.
- **Ví dụ gõ vào LLM:**

  > Đọc hiểu bản vẽ và giải thích bản vẽ understand bằng ngôn ngữ dễ hiểu cho người dùng.

## Kiến trúc
Mặt bằng, mặt đứng, mặt cắt, phòng, cửa, tường và hồ sơ kiến trúc.
### thành phần kiến trúc
#### arch_catalogue_insert

- **Nhóm:** thành phần kiến trúc
- **Làm gì:** Thực hiện thao tác arch danh mục chèn trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc.
- **Ví dụ gõ vào LLM:**

  > Trên mặt bằng kiến trúc, hãy arch danh mục chèn và giữ đúng tỷ lệ bản vẽ.

#### arch_catalogue_list

- **Nhóm:** thành phần kiến trúc
- **Làm gì:** Thực hiện thao tác arch danh mục liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc.
- **Ví dụ gõ vào LLM:**

  > Trên mặt bằng kiến trúc, hãy arch danh mục liệt kê và giữ đúng tỷ lệ bản vẽ.

#### arch_dimension_chains

- **Nhóm:** thành phần kiến trúc
- **Làm gì:** Thực hiện thao tác arch kích thước chains trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc.
- **Ví dụ gõ vào LLM:**

  > Trên mặt bằng kiến trúc, hãy arch kích thước chains và giữ đúng tỷ lệ bản vẽ.

#### arch_grid

- **Nhóm:** thành phần kiến trúc
- **Làm gì:** Thực hiện thao tác arch lưới trục trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc.
- **Ví dụ gõ vào LLM:**

  > Trên mặt bằng kiến trúc, hãy arch lưới trục và giữ đúng tỷ lệ bản vẽ.

#### arch_opening

- **Nhóm:** thành phần kiến trúc
- **Làm gì:** Thực hiện thao tác arch ô cửa trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc.
- **Ví dụ gõ vào LLM:**

  > Trên mặt bằng kiến trúc, hãy arch ô cửa và giữ đúng tỷ lệ bản vẽ.

#### arch_plan_from_spec

- **Nhóm:** thành phần kiến trúc
- **Làm gì:** Thực hiện thao tác arch mặt bằng từ spec trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc.
- **Ví dụ gõ vào LLM:**

  > Trên mặt bằng kiến trúc, hãy arch mặt bằng từ spec và giữ đúng tỷ lệ bản vẽ.

#### arch_room

- **Nhóm:** thành phần kiến trúc
- **Làm gì:** Thực hiện thao tác arch phòng trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc.
- **Ví dụ gõ vào LLM:**

  > Trên mặt bằng kiến trúc, hãy arch phòng và giữ đúng tỷ lệ bản vẽ.

#### arch_rooms_detect

- **Nhóm:** thành phần kiến trúc
- **Làm gì:** Thực hiện thao tác arch phòng detect trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc.
- **Ví dụ gõ vào LLM:**

  > Trên mặt bằng kiến trúc, hãy arch phòng detect và giữ đúng tỷ lệ bản vẽ.

#### arch_schedule

- **Nhóm:** thành phần kiến trúc
- **Làm gì:** Thực hiện thao tác arch bảng thống kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc.
- **Ví dụ gõ vào LLM:**

  > Trên mặt bằng kiến trúc, hãy arch bảng thống kê và giữ đúng tỷ lệ bản vẽ.

#### arch_stair

- **Nhóm:** thành phần kiến trúc
- **Làm gì:** Thực hiện thao tác arch cầu thang trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc.
- **Ví dụ gõ vào LLM:**

  > Trên mặt bằng kiến trúc, hãy arch cầu thang và giữ đúng tỷ lệ bản vẽ.

#### arch_symbol

- **Nhóm:** thành phần kiến trúc
- **Làm gì:** Thực hiện thao tác arch ký hiệu trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc.
- **Ví dụ gõ vào LLM:**

  > Trên mặt bằng kiến trúc, hãy arch ký hiệu và giữ đúng tỷ lệ bản vẽ.

#### arch_wall

- **Nhóm:** thành phần kiến trúc
- **Làm gì:** Thực hiện thao tác arch tường trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc.
- **Ví dụ gõ vào LLM:**

  > Trên mặt bằng kiến trúc, hãy arch tường và giữ đúng tỷ lệ bản vẽ.

## Cơ khí
Chi tiết cơ khí, ký hiệu mối hàn và các thao tác phục vụ bản vẽ cơ khí.
### cơ khí
#### centre_marks

- **Nhóm:** cơ khí
- **Làm gì:** Thực hiện thao tác centre marks trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bản vẽ cơ khí.
- **Ví dụ gõ vào LLM:**

  > Trên bản vẽ cơ khí, hãy centre marks theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn.

#### hatch_material

- **Nhóm:** cơ khí
- **Làm gì:** Thực hiện thao tác tô mặt material trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bản vẽ cơ khí.
- **Ví dụ gõ vào LLM:**

  > Trên bản vẽ cơ khí, hãy tô mặt material theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn.

#### mech_dimension_part

- **Nhóm:** cơ khí
- **Làm gì:** Thực hiện thao tác mech kích thước part trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bản vẽ cơ khí.
- **Ví dụ gõ vào LLM:**

  > Trên bản vẽ cơ khí, hãy mech kích thước part theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn.

#### mech_hole_pattern

- **Nhóm:** cơ khí
- **Làm gì:** Thực hiện thao tác mech hole pattern trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bản vẽ cơ khí.
- **Ví dụ gõ vào LLM:**

  > Trên bản vẽ cơ khí, hãy mech hole pattern theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn.

#### mech_part_draw

- **Nhóm:** cơ khí
- **Làm gì:** Thực hiện thao tác mech part draw trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bản vẽ cơ khí.
- **Ví dụ gõ vào LLM:**

  > Trên bản vẽ cơ khí, hãy mech part draw theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn.

#### mech_part_from_spec

- **Nhóm:** cơ khí
- **Làm gì:** Thực hiện thao tác mech part từ spec trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bản vẽ cơ khí.
- **Ví dụ gõ vào LLM:**

  > Trên bản vẽ cơ khí, hãy mech part từ spec theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn.

#### mech_part_inspect

- **Nhóm:** cơ khí
- **Làm gì:** Thực hiện thao tác mech part inspect trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bản vẽ cơ khí.
- **Ví dụ gõ vào LLM:**

  > Trên bản vẽ cơ khí, hãy mech part inspect theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn.

#### mech_view_add

- **Nhóm:** cơ khí
- **Làm gì:** Thực hiện thao tác mech góc nhìn add trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bản vẽ cơ khí.
- **Ví dụ gõ vào LLM:**

  > Trên bản vẽ cơ khí, hãy mech góc nhìn add theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn.

#### section_line

- **Nhóm:** cơ khí
- **Làm gì:** Thực hiện thao tác mặt cắt đường trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bản vẽ cơ khí.
- **Ví dụ gõ vào LLM:**

  > Trên bản vẽ cơ khí, hãy mặt cắt đường theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn.

#### std_feature_draw

- **Nhóm:** cơ khí
- **Làm gì:** Thực hiện thao tác std feature draw trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bản vẽ cơ khí.
- **Ví dụ gõ vào LLM:**

  > Trên bản vẽ cơ khí, hãy std feature draw theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn.

#### std_part_insert

- **Nhóm:** cơ khí
- **Làm gì:** Thực hiện thao tác std part chèn trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bản vẽ cơ khí.
- **Ví dụ gõ vào LLM:**

  > Trên bản vẽ cơ khí, hãy std part chèn theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn.

#### std_part_list

- **Nhóm:** cơ khí
- **Làm gì:** Thực hiện thao tác std part liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bản vẽ cơ khí.
- **Ví dụ gõ vào LLM:**

  > Trên bản vẽ cơ khí, hãy std part liệt kê theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn.

#### surface_texture

- **Nhóm:** cơ khí
- **Làm gì:** Thực hiện thao tác surface texture trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bản vẽ cơ khí.
- **Ví dụ gõ vào LLM:**

  > Trên bản vẽ cơ khí, hãy surface texture theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn.

#### weld_symbol

- **Nhóm:** cơ khí
- **Làm gì:** Thực hiện thao tác mối hàn ký hiệu trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bản vẽ cơ khí.
- **Ví dụ gõ vào LLM:**

  > Trên bản vẽ cơ khí, hãy mối hàn ký hiệu theo tiêu chuẩn đã chọn và báo cáo phần chưa chắc chắn.

## P&ID
Sơ đồ đường ống và thiết bị đo lường điều khiển.
### P&ID
#### pid_equipment_list

- **Nhóm:** P&ID
- **Làm gì:** Thực hiện thao tác P&ID equipment liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sơ đồ P&ID.
- **Ví dụ gõ vào LLM:**

  > Trên sơ đồ P&ID, hãy P&ID equipment liệt kê và kiểm tra ký hiệu, đường ống cùng nhãn thiết bị.

#### pid_from_spec

- **Nhóm:** P&ID
- **Làm gì:** Thực hiện thao tác P&ID từ spec trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sơ đồ P&ID.
- **Ví dụ gõ vào LLM:**

  > Trên sơ đồ P&ID, hãy P&ID từ spec và kiểm tra ký hiệu, đường ống cùng nhãn thiết bị.

#### pid_graph

- **Nhóm:** P&ID
- **Làm gì:** Thực hiện thao tác P&ID graph trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sơ đồ P&ID.
- **Ví dụ gõ vào LLM:**

  > Trên sơ đồ P&ID, hãy P&ID graph và kiểm tra ký hiệu, đường ống cùng nhãn thiết bị.

#### pid_instrument_index

- **Nhóm:** P&ID
- **Làm gì:** Thực hiện thao tác P&ID instrument index trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sơ đồ P&ID.
- **Ví dụ gõ vào LLM:**

  > Trên sơ đồ P&ID, hãy P&ID instrument index và kiểm tra ký hiệu, đường ống cùng nhãn thiết bị.

#### pid_line_draw

- **Nhóm:** P&ID
- **Làm gì:** Thực hiện thao tác P&ID đường draw trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sơ đồ P&ID.
- **Ví dụ gõ vào LLM:**

  > Trên sơ đồ P&ID, hãy P&ID đường draw và kiểm tra ký hiệu, đường ống cùng nhãn thiết bị.

#### pid_line_list

- **Nhóm:** P&ID
- **Làm gì:** Thực hiện thao tác P&ID đường liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sơ đồ P&ID.
- **Ví dụ gõ vào LLM:**

  > Trên sơ đồ P&ID, hãy P&ID đường liệt kê và kiểm tra ký hiệu, đường ống cùng nhãn thiết bị.

#### pid_symbol_insert

- **Nhóm:** P&ID
- **Làm gì:** Thực hiện thao tác P&ID ký hiệu chèn trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sơ đồ P&ID.
- **Ví dụ gõ vào LLM:**

  > Trên sơ đồ P&ID, hãy P&ID ký hiệu chèn và kiểm tra ký hiệu, đường ống cùng nhãn thiết bị.

#### pid_symbol_list

- **Nhóm:** P&ID
- **Làm gì:** Thực hiện thao tác P&ID ký hiệu liệt kê trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sơ đồ P&ID.
- **Ví dụ gõ vào LLM:**

  > Trên sơ đồ P&ID, hãy P&ID ký hiệu liệt kê và kiểm tra ký hiệu, đường ống cùng nhãn thiết bị.

#### pid_tag_parse

- **Nhóm:** P&ID
- **Làm gì:** Thực hiện thao tác P&ID tag parse trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần sơ đồ P&ID.
- **Ví dụ gõ vào LLM:**

  > Trên sơ đồ P&ID, hãy P&ID tag parse và kiểm tra ký hiệu, đường ống cùng nhãn thiết bị.

## Nhà máy
Bố trí thiết bị và bản vẽ nhà máy công nghiệp.
### nhà máy
#### cable_takeoff

- **Nhóm:** nhà máy
- **Làm gì:** Thực hiện thao tác cable takeoff trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bố trí thiết bị nhà máy.
- **Ví dụ gõ vào LLM:**

  > Trong bản vẽ nhà máy, hãy cable takeoff và kiểm tra khoảng cách an toàn thiết bị.

#### pipe_takeoff

- **Nhóm:** nhà máy
- **Làm gì:** Thực hiện thao tác pipe takeoff trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần bố trí thiết bị nhà máy.
- **Ví dụ gõ vào LLM:**

  > Trong bản vẽ nhà máy, hãy pipe takeoff và kiểm tra khoảng cách an toàn thiết bị.

## Kỹ thuật và 3D
Kiểm tra kỹ thuật và hình học khối ba chiều.
### khối đặc
#### solid_boolean

- **Nhóm:** khối đặc
- **Làm gì:** Thực hiện thao tác khối đặc boolean trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần hình học ba chiều và khối đặc.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra hình học ba chiều rồi thực hiện khối đặc boolean; không làm hỏng đối tượng gốc.

#### solid_box

- **Nhóm:** khối đặc
- **Làm gì:** Thực hiện thao tác khối đặc khung trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần hình học ba chiều và khối đặc.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra hình học ba chiều rồi thực hiện khối đặc khung; không làm hỏng đối tượng gốc.

#### solid_cylinder

- **Nhóm:** khối đặc
- **Làm gì:** Thực hiện thao tác khối đặc cylinder trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần hình học ba chiều và khối đặc.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra hình học ba chiều rồi thực hiện khối đặc cylinder; không làm hỏng đối tượng gốc.

#### solid_extrude

- **Nhóm:** khối đặc
- **Làm gì:** Thực hiện thao tác khối đặc extrude trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần hình học ba chiều và khối đặc.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra hình học ba chiều rồi thực hiện khối đặc extrude; không làm hỏng đối tượng gốc.

#### solid_revolve

- **Nhóm:** khối đặc
- **Làm gì:** Thực hiện thao tác khối đặc revolve trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần hình học ba chiều và khối đặc.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra hình học ba chiều rồi thực hiện khối đặc revolve; không làm hỏng đối tượng gốc.

### kỹ thuật
#### datum_feature

- **Nhóm:** kỹ thuật
- **Làm gì:** Thực hiện thao tác datum feature trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kỹ thuật.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo datum feature thành lỗi hoặc cảnh báo.

#### drawing_deliver

- **Nhóm:** kỹ thuật
- **Làm gì:** Thực hiện thao tác bản vẽ deliver trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kỹ thuật.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo bản vẽ deliver thành lỗi hoặc cảnh báo.

#### drawing_finalize

- **Nhóm:** kỹ thuật
- **Làm gì:** Thực hiện thao tác bản vẽ finalize trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kỹ thuật.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo bản vẽ finalize thành lỗi hoặc cảnh báo.

#### gd_frame

- **Nhóm:** kỹ thuật
- **Làm gì:** Thực hiện thao tác gd frame trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kỹ thuật.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo gd frame thành lỗi hoặc cảnh báo.

#### gear_draw_helical_front_view

- **Nhóm:** kỹ thuật
- **Làm gì:** Thực hiện thao tác gear draw helical front góc nhìn trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kỹ thuật.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo gear draw helical front góc nhìn thành lỗi hoặc cảnh báo.

#### gear_draw_section_aa

- **Nhóm:** kỹ thuật
- **Làm gì:** Thực hiện thao tác gear draw mặt cắt aa trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kỹ thuật.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo gear draw mặt cắt aa thành lỗi hoặc cảnh báo.

#### gear_draw_spur_front_view

- **Nhóm:** kỹ thuật
- **Làm gì:** Thực hiện thao tác gear draw spur front góc nhìn trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kỹ thuật.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo gear draw spur front góc nhìn thành lỗi hoặc cảnh báo.

#### keyway_draw_keyed_bore

- **Nhóm:** kỹ thuật
- **Làm gì:** Thực hiện thao tác keyway draw keyed bore trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kỹ thuật.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo keyway draw keyed bore thành lỗi hoặc cảnh báo.

#### keyway_draw_section

- **Nhóm:** kỹ thuật
- **Làm gì:** Thực hiện thao tác keyway draw mặt cắt trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kỹ thuật.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo keyway draw mặt cắt thành lỗi hoặc cảnh báo.

#### titleblock_apply_iso_a3

- **Nhóm:** kỹ thuật
- **Làm gì:** Thực hiện thao tác titleblock apply iso a3 trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần kiểm tra kỹ thuật.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra bản vẽ theo yêu cầu kỹ thuật và báo cáo titleblock apply iso a3 thành lỗi hoặc cảnh báo.

## Nâng cao
Các chức năng nâng cao cần kiểm tra khả năng backend trước khi dùng.
### nâng cao
#### construction_clear

- **Nhóm:** nâng cao
- **Làm gì:** Thực hiện thao tác construction clear trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng nâng cao.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện construction clear nếu backend cho phép.

#### construction_xline

- **Nhóm:** nâng cao
- **Làm gì:** Thực hiện thao tác construction xline trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng nâng cao.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện construction xline nếu backend cho phép.

#### dimension_auto

- **Nhóm:** nâng cao
- **Làm gì:** Thực hiện thao tác kích thước auto trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng nâng cao.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện kích thước auto nếu backend cho phép.

#### drawing_apply_iso_layers

- **Nhóm:** nâng cao
- **Làm gì:** Thực hiện thao tác bản vẽ apply iso layers trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng nâng cao.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện bản vẽ apply iso layers nếu backend cho phép.

#### drawing_critique

- **Nhóm:** nâng cao
- **Làm gì:** Thực hiện thao tác bản vẽ critique trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng nâng cao.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện bản vẽ critique nếu backend cho phép.

#### drawing_plan

- **Nhóm:** nâng cao
- **Làm gì:** Thực hiện thao tác bản vẽ mặt bằng trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng nâng cao.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện bản vẽ mặt bằng nếu backend cho phép.

#### drawing_preflight

- **Nhóm:** nâng cao
- **Làm gì:** Thực hiện thao tác bản vẽ preflight trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng nâng cao.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện bản vẽ preflight nếu backend cho phép.

#### drawing_refine

- **Nhóm:** nâng cao
- **Làm gì:** Thực hiện thao tác bản vẽ refine trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng nâng cao.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện bản vẽ refine nếu backend cho phép.

#### entity_select_smart

- **Nhóm:** nâng cao
- **Làm gì:** Thực hiện thao tác đối tượng chọn smart trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng nâng cao.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện đối tượng chọn smart nếu backend cho phép.

#### point_from_snap

- **Nhóm:** nâng cao
- **Làm gì:** Thực hiện thao tác điểm từ snap trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng nâng cao.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện điểm từ snap nếu backend cho phép.

#### point_intersection

- **Nhóm:** nâng cao
- **Làm gì:** Thực hiện thao tác điểm intersection trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng nâng cao.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện điểm intersection nếu backend cho phép.

#### point_tangent

- **Nhóm:** nâng cao
- **Làm gì:** Thực hiện thao tác điểm tangent trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng nâng cao.
- **Ví dụ gõ vào LLM:**

  > Kiểm tra khả năng hỗ trợ trước, sau đó thực hiện điểm tangent nếu backend cho phép.

## Mở rộng cadtroly
Các chức năng riêng của project cadtroly như tiêu chuẩn, QA và khối lượng.
### mở rộng cadtroly
#### check_rulesets

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác kiểm tra rulesets trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện kiểm tra rulesets trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### check_run

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác kiểm tra run trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện kiểm tra run trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### drawing_apply_discipline_standard

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác bản vẽ apply discipline standard trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện bản vẽ apply discipline standard trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### drawing_entities

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác bản vẽ đối tượng trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện bản vẽ đối tượng trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### drawing_read

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác bản vẽ đọc trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện bản vẽ đọc trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### kho_industries

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác kho industries trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện kho industries trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### kho_rules_export

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác kho rules xuất trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện kho rules xuất trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### kho_rules_import

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác kho rules nhập trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện kho rules nhập trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### kho_skill_add

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác kho skill add trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện kho skill add trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### kho_skill_toggle

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác kho skill toggle trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện kho skill toggle trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### kho_skills

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác kho skills trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện kho skills trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### kho_standard_add

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác kho standard add trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện kho standard add trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### kho_standard_delete

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác kho standard xóa trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện kho standard xóa trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### kho_standards

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác kho standards trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện kho standards trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### kho_status

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác kho trạng thái trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện kho trạng thái trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### pdf_to_dwg

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác pdf đến dwg trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện pdf đến dwg trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### pdf_vectorize

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác pdf vectorize trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện pdf vectorize trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### standards_reference

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác standards tham chiếu trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện standards tham chiếu trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### structural_qa

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác structural qa trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện structural qa trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### takeoff_compute

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác takeoff compute trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện takeoff compute trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### takeoff_decide

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác takeoff decide trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện takeoff decide trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### takeoff_export

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác takeoff xuất trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện takeoff xuất trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### takeoff_propose

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác takeoff propose trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện takeoff propose trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### takeoff_run

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác takeoff run trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện takeoff run trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.

#### view_render_report

- **Nhóm:** mở rộng cadtroly
- **Làm gì:** Thực hiện thao tác góc nhìn kết xuất report trong bản vẽ CAD.
- **Dùng khi nào:** Khi cần chức năng mở rộng của cadtroly.
- **Ví dụ gõ vào LLM:**

  > Thực hiện góc nhìn kết xuất report trên bản vẽ, báo cáo kết quả và không ghi đè file gốc.


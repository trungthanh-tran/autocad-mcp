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

| Tên tool | Nhóm | Làm gì | Dùng khi nào | Ví dụ tham số |
|---|---|---|---|---|
| `analysis_bounding_box` | phân tích | Thực hiện thao tác phân tích giới hạn khung trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | `{}` |
| `analysis_entity_stats` | phân tích | Thực hiện thao tác phân tích đối tượng thống kê trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | `{}` |
| `analysis_find_in_region` | phân tích | Thực hiện thao tác phân tích tìm trong vùng trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | `{"x1": 1, "y1": 1, "x2": 1, "y2": 1, "fields": null, "compact": false}` |
| `analysis_layer_stats` | phân tích | Thực hiện thao tác phân tích lớp thống kê trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | `{}` |
| `analysis_list_properties` | phân tích | Thực hiện thao tác phân tích liệt kê thuộc tính trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | `{"handle": "A1B2"}` |
| `analysis_measure_area` | phân tích | Thực hiện thao tác phân tích đo diện tích trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | `{"points": []}` |
| `analysis_measure_distance` | phân tích | Thực hiện thao tác phân tích đo khoảng cách trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | `{"x1": 1, "y1": 1, "x2": 1, "y2": 1}` |
| `analysis_measure_entity` | phân tích | Thực hiện thao tác phân tích đo đối tượng trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | `{"handle": "A1B2", "flatten_tolerance": 0.001}` |
| `analysis_select_by_layer` | phân tích | Thực hiện thao tác phân tích chọn theo lớp trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | `{"layer_name": "vi-du", "fields": null, "compact": false}` |
| `analysis_select_by_type` | phân tích | Thực hiện thao tác phân tích chọn theo type trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | `{"entity_type": "vi-du", "fields": null, "compact": false}` |
| `arch_catalogue_insert` | kiến trúc | Thực hiện thao tác arch catalogue chèn trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | `{"name": "vi-du", "x": 1, "y": 1, "rotation": 0.0}` |
| `arch_catalogue_list` | kiến trúc | Thực hiện thao tác arch catalogue liệt kê trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | `{"query": null, "family": null, "lang": "en"}` |
| `arch_dimension_chains` | kiến trúc | Thực hiện thao tác arch kích thước chains trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | `{"sides": null, "scale": 50.0, "first_offset": null, "step": null}` |
| `arch_grid` | kiến trúc | Thực hiện thao tác arch grid trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | `{"x_axes": [], "y_axes": [], "labels": null, "extension": 1500.0, "scale": 50.0}` |
| `arch_opening` | kiến trúc | Thực hiện thao tác arch opening trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | `{"wall": "vi-du", "offset": 1, "width": 1, "kind": "door", "swing": "in", "hand": "left", "sill": null, "height": null, "tag": null, "opening_id": null, "lang": "en", "poche": true}` |
| `arch_plan_from_spec` | kiến trúc | Thực hiện thao tác arch mặt bằng từ spec trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | `{"spec": {}}` |
| `arch_room` | kiến trúc | Thực hiện thao tác arch room trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | `{"name": "vi-du", "x": 1, "y": 1, "number": null, "room_id": null, "lang": "en", "scale": 50.0}` |
| `arch_rooms_detect` | kiến trúc | Thực hiện thao tác arch rooms detect trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | `{"layers": null, "min_area": 1000000.0, "tol": 1.0}` |
| `arch_schedule` | kiến trúc | Thực hiện thao tác arch schedule trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | `{"kind": "vi-du", "x": 1, "y": 1, "lang": "en", "scale": 50.0}` |
| `arch_stair` | kiến trúc | Thực hiện thao tác arch stair trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | `{"stair_id": "vi-du", "start_x": 1, "start_y": 1, "width": 1, "risers": 1, "riser_height": 1, "going": 1, "direction_deg": 0.0, "kind": "straight", "turn": "left", "lang": "en", "scale": 50.0}` |
| `arch_symbol` | kiến trúc | Thực hiện thao tác arch ký hiệu trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | `{"kind": "vi-du", "x": 1, "y": 1, "params": null, "lang": "en", "scale": 50.0}` |
| `arch_wall` | kiến trúc | Thực hiện thao tác arch wall trong bản vẽ CAD. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. | `{"walls": [], "poche": true}` |
| `balloon_add` | tờ bản vẽ | Thực hiện thao tác balloon add trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | `{"item": 1, "x": 1, "y": 1, "leader_x": 1, "leader_y": 1, "targets": null, "radius": 4.0, "layer": "DIM", "layout": ""}` |
| `batch_plot` | thiết lập trang | Thực hiện thao tác hàng loạt plot trong bản vẽ CAD. | Khi cần khổ giấy, tỷ lệ và in ấn. | `{"output_dir": "vi-du", "layouts": null, "format": "pdf", "file_pattern": "{drawing}-{layout}.pdf"}` |
| `block_create_from_entities` | khối | Thực hiện thao tác khối tạo từ đối tượng trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. | `{"name": "vi-du", "handles": [], "base_x": 0.0, "base_y": 0.0}` |
| `block_define` | khối | Thực hiện thao tác khối định nghĩa trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. | `{"name": "vi-du", "entities": [], "attdefs": null, "base_x": 0.0, "base_y": 0.0, "overwrite": false, "create_layers": false}` |
| `block_explode` | khối | Thực hiện thao tác khối phá khối trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. | `{"handle": "A1B2"}` |
| `block_find_references` | khối | Thực hiện thao tác khối tìm tham chiếu trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. | `{"name": "vi-du", "fields": null, "compact": false}` |
| `block_get_attributes` | khối | Thực hiện thao tác khối get attributes trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. | `{"handle": "A1B2"}` |
| `block_insert` | khối | Thực hiện thao tác khối chèn trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. | `{"name": "vi-du", "x": 1, "y": 1, "scale_x": 1.0, "scale_y": 1.0, "rotation": 0.0, "attributes": null, "layer": null}` |
| `block_list` | khối | Thực hiện thao tác khối liệt kê trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. | `{"fields": null, "compact": false}` |
| `block_set_attributes` | khối | Thực hiện thao tác khối đặt attributes trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. | `{"handle": "A1B2", "attributes": {}}` |
| `bom_extract` | tờ bản vẽ | Thực hiện thao tác bom extract trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | `{"layer": "", "group_by": "designation", "columns": null, "limit": 0}` |
| `bom_table` | tờ bản vẽ | Thực hiện thao tác bom bảng trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | `{"rows": null, "size": "A3", "orientation": "landscape", "origin_x": 0.0, "origin_y": 0.0, "at_x": null, "at_y": null, "direction": "up", "columns": null, "row_height": 7.0, "layout": ""}` |
| `boundary_from_entities` | phân tích | Thực hiện thao tác boundary từ đối tượng trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | `{"handles": [], "tolerance": 1e-09}` |
| `boundary_trace` | phân tích | Thực hiện thao tác boundary trace trong bản vẽ CAD. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. | `{"x": 1, "y": 1, "layer": "", "tolerance": 1e-09}` |
| `cable_takeoff` | nhà máy | Thực hiện thao tác cable takeoff trong bản vẽ CAD. | Khi cần bố trí thiết bị nhà máy. | `{"pid_path": null, "layout_path": null, "output": null, "lang": "en", "allowance": 0.2, "section_rules": null, "panel_rule": "nearest"}` |
| `cad_batch` | xử lý hàng loạt | Thực hiện thao tác cad hàng loạt trong bản vẽ CAD. | Khi cần xử lý hàng loạt. | `{"steps": [], "on_error": "stop", "dry_run": false, "verbose": false}` |
| `centre_marks` | cơ khí | Thực hiện thao tác centre marks trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | `{"handles": null, "centers": null, "style": "mark", "extension": 3.0, "layer": null}` |
| `check_rulesets` | mở rộng cadtroly | Thực hiện thao tác kiểm tra rulesets trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{}` |
| `check_run` | mở rộng cadtroly | Thực hiện thao tác kiểm tra run trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"path": "D:\\DuAn\\ban-ve.dwg", "ruleset": "vi-du", "include_unapproved": false}` |
| `construction_clear` | nâng cao | Thực hiện thao tác construction clear trong bản vẽ CAD. | Khi cần chức năng nâng cao. | `{"layer": "CONSTRUCTION"}` |
| `construction_xline` | nâng cao | Thực hiện thao tác construction xline trong bản vẽ CAD. | Khi cần chức năng nâng cao. | `{"x": 1, "y": 1, "angle_deg": 1, "layer": "CONSTRUCTION"}` |
| `data_extract` | tờ bản vẽ | Thực hiện thao tác dữ liệu extract trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | `{"path": "D:\\DuAn\\ban-ve.dwg", "fmt": "csv", "layer": "", "group_by": "designation", "columns": null}` |
| `datum_feature` | kỹ thuật | Thực hiện thao tác datum feature trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | `{"letter": "vi-du", "x": 1, "y": 1, "size": 5.0, "layer": null}` |
| `dimension_aligned` | kích thước | Thực hiện thao tác kích thước aligned trong bản vẽ CAD. | Khi cần kích thước và ghi chú đo. | `{"x1": 1, "y1": 1, "x2": 1, "y2": 1, "dim_x": 1, "dim_y": 1, "layer": null}` |
| `dimension_angular` | kích thước | Thực hiện thao tác kích thước angular trong bản vẽ CAD. | Khi cần kích thước và ghi chú đo. | `{"vertex_x": 1, "vertex_y": 1, "x1": 1, "y1": 1, "x2": 1, "y2": 1, "text_x": 1, "text_y": 1, "layer": null}` |
| `dimension_auto` | nâng cao | Thực hiện thao tác kích thước auto trong bản vẽ CAD. | Khi cần chức năng nâng cao. | `{"handles": [], "style": "chain", "offset": 10.0}` |
| `dimension_diameter` | kích thước | Thực hiện thao tác kích thước diameter trong bản vẽ CAD. | Khi cần kích thước và ghi chú đo. | `{"x1": 1, "y1": 1, "x2": 1, "y2": 1, "leader_length": 10.0, "layer": null, "tol_upper": null, "tol_lower": null, "tol_mode": "none", "text_override": null, "fit": null}` |
| `dimension_linear` | kích thước | Thực hiện thao tác kích thước linear trong bản vẽ CAD. | Khi cần kích thước và ghi chú đo. | `{"x1": 1, "y1": 1, "x2": 1, "y2": 1, "dim_x": 1, "dim_y": 1, "rotation": 0.0, "layer": null, "tol_upper": null, "tol_lower": null, "tol_mode": "none", "text_override": null, "fit": null}` |
| `dimension_radius` | kích thước | Thực hiện thao tác kích thước radius trong bản vẽ CAD. | Khi cần kích thước và ghi chú đo. | `{"center_x": 1, "center_y": 1, "chord_x": 1, "chord_y": 1, "leader_length": 10.0, "layer": null, "tol_upper": null, "tol_lower": null, "tol_mode": "none", "text_override": null, "fit": null}` |
| `dimstyle_create` | kiểu hiển thị | Thực hiện thao tác dimstyle tạo trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | `{"name": "vi-du", "preset": null, "overrides": null, "set_current": false}` |
| `dimstyle_list` | kiểu hiển thị | Thực hiện thao tác dimstyle liệt kê trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | `{}` |
| `dimstyle_modify` | kiểu hiển thị | Thực hiện thao tác dimstyle sửa trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | `{"name": "vi-du", "overrides": {}}` |
| `dimstyle_set_current` | kiểu hiển thị | Thực hiện thao tác dimstyle đặt hiện tại trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | `{"name": "vi-du"}` |
| `document_activate` | môi trường | Thực hiện thao tác document activate trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{"name_or_path": "D:\\DuAn\\ban-ve.dwg"}` |
| `document_close` | môi trường | Thực hiện thao tác document đóng trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{"name_or_path": null, "save": false, "discard": false}` |
| `document_list` | môi trường | Thực hiện thao tác document liệt kê trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{}` |
| `drawing_apply_discipline_standard` | mở rộng cadtroly | Thực hiện thao tác bản vẽ apply discipline standard trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"discipline": "vi-du", "layers": true, "units": true, "naming": "auto"}` |
| `drawing_apply_iso_layers` | nâng cao | Thực hiện thao tác bản vẽ apply iso layers trong bản vẽ CAD. | Khi cần chức năng nâng cao. | `{"standard": "mech"}` |
| `drawing_apply_standard` | kiểu hiển thị | Thực hiện thao tác bản vẽ apply standard trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | `{"standard": "vi-du", "layers": true, "units": true}` |
| `drawing_audit` | bản vẽ | Thực hiện thao tác bản vẽ audit trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | `{}` |
| `drawing_close` | bản vẽ | Thực hiện thao tác bản vẽ đóng trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | `{"save": true}` |
| `drawing_critique` | nâng cao | Thực hiện thao tác bản vẽ critique trong bản vẽ CAD. | Khi cần chức năng nâng cao. | `{"focus": null}` |
| `drawing_deliver` | kỹ thuật | Thực hiện thao tác bản vẽ deliver trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | `{"output_dir": "vi-du", "formats": null, "min_score": 95.0, "strict_critique": true, "expected": null}` |
| `drawing_diff` | đọc hiểu | Thực hiện thao tác bản vẽ diff trong bản vẽ CAD. | Khi cần đọc hiểu cấu trúc bản vẽ. | `{"old_path": "D:\\DuAn\\ban-ve.dwg", "new_path": null, "tol": 0.01, "move_tol": null, "limit": 200, "markup": false, "rev": "", "description": ""}` |
| `drawing_entities` | mở rộng cadtroly | Thực hiện thao tác bản vẽ đối tượng trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"path": "D:\\DuAn\\ban-ve.dwg", "layer": null, "block": null, "kind": null, "limit": 100}` |
| `drawing_export_dwg` | tờ bản vẽ | Thực hiện thao tác bản vẽ xuất dwg trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | `{"path": "D:\\DuAn\\ban-ve.dwg", "version": "R2018"}` |
| `drawing_export_dxf` | bản vẽ | Thực hiện thao tác bản vẽ xuất dxf trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | `{"path": "D:\\DuAn\\ban-ve.dwg"}` |
| `drawing_export_pdf` | bản vẽ | Thực hiện thao tác bản vẽ xuất pdf trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | `{"path": "D:\\DuAn\\ban-ve.dwg", "layout": null}` |
| `drawing_finalize` | kỹ thuật | Thực hiện thao tác bản vẽ finalize trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | `{"save_path": null, "screenshot_path": null, "expected": null, "strict_critique": false}` |
| `drawing_info` | tra cứu đối tượng | Thực hiện thao tác bản vẽ info trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. | `{}` |
| `drawing_new` | bản vẽ | Thực hiện thao tác bản vẽ new trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | `{"template": null, "bootstrap": true}` |
| `drawing_open` | bản vẽ | Thực hiện thao tác bản vẽ mở trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | `{"path": "D:\\DuAn\\ban-ve.dwg"}` |
| `drawing_plan` | nâng cao | Thực hiện thao tác bản vẽ mặt bằng trong bản vẽ CAD. | Khi cần chức năng nâng cao. | `{"intent": "vi-du", "sheet_size": "A3", "scale": 1.0, "layer_set_id": "mech", "view_count": 1, "dim_style": "chain", "notes": null, "requirements": null, "spec_hash": null}` |
| `drawing_preflight` | nâng cao | Thực hiện thao tác bản vẽ preflight trong bản vẽ CAD. | Khi cần chức năng nâng cao. | `{"intent": "vi-du", "requirements": null, "sheet_size": "A3", "scale": 1.0, "layer_set_id": "mech", "view_count": 1, "dim_style": "chain", "allow_assumptions": false}` |
| `drawing_properties_get` | môi trường | Thực hiện thao tác bản vẽ thuộc tính get trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{}` |
| `drawing_properties_set` | môi trường | Thực hiện thao tác bản vẽ thuộc tính đặt trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{"title": null, "subject": null, "author": null, "keywords": null, "comments": null, "custom": null}` |
| `drawing_purge` | bản vẽ | Thực hiện thao tác bản vẽ dọn dẹp trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | `{}` |
| `drawing_read` | mở rộng cadtroly | Thực hiện thao tác bản vẽ đọc trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"path": "D:\\DuAn\\ban-ve.dwg"}` |
| `drawing_redo` | bản vẽ | Thực hiện thao tác bản vẽ redo trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | `{}` |
| `drawing_refine` | nâng cao | Thực hiện thao tác bản vẽ refine trong bản vẽ CAD. | Khi cần chức năng nâng cao. | `{"max_rounds": 3, "min_score": 95.0, "focus": null, "allowed_repairs": null, "dry_run": false}` |
| `drawing_save` | bản vẽ | Thực hiện thao tác bản vẽ lưu trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | `{"path": null}` |
| `drawing_save_as` | bản vẽ | Thực hiện thao tác bản vẽ lưu as trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | `{"path": "D:\\DuAn\\ban-ve.dwg", "format": ""}` |
| `drawing_scale_check` | đọc hiểu | Thực hiện thao tác bản vẽ tỷ lệ kiểm tra trong bản vẽ CAD. | Khi cần đọc hiểu cấu trúc bản vẽ. | `{"reference": "vi-du", "path": null, "min_pair_mm": 2000.0}` |
| `drawing_settings` | hệ thống | Thực hiện thao tác bản vẽ thiết lập trong bản vẽ CAD. | Khi cần trạng thái máy chủ. | `{"settings": null}` |
| `drawing_template_list` | thiết lập trang | Thực hiện thao tác bản vẽ mẫu liệt kê trong bản vẽ CAD. | Khi cần khổ giấy, tỷ lệ và in ấn. | `{}` |
| `drawing_template_save` | thiết lập trang | Thực hiện thao tác bản vẽ mẫu lưu trong bản vẽ CAD. | Khi cần khổ giấy, tỷ lệ và in ấn. | `{"path": "D:\\DuAn\\ban-ve.dwg", "name": null, "description": null}` |
| `drawing_topology_check` | đọc hiểu | Thực hiện thao tác bản vẽ topology kiểm tra trong bản vẽ CAD. | Khi cần đọc hiểu cấu trúc bản vẽ. | `{"layers": null, "path": null, "gap": null, "tol": 0.01, "limit": 200}` |
| `drawing_understand` | đọc hiểu | Thực hiện thao tác bản vẽ understand trong bản vẽ CAD. | Khi cần đọc hiểu cấu trúc bản vẽ. | `{"path": null}` |
| `drawing_undo` | bản vẽ | Thực hiện thao tác bản vẽ undo trong bản vẽ CAD. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. | `{}` |
| `entity_array_polar` | sửa đối tượng | Thực hiện thao tác đối tượng array polar trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | `{"handle": "A1B2", "count": 1, "fill_angle": 1, "center_x": 1, "center_y": 1, "fields": null, "compact": false}` |
| `entity_array_rectangular` | sửa đối tượng | Thực hiện thao tác đối tượng array rectangular trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | `{"handle": "A1B2", "rows": 1, "cols": 1, "row_spacing": 1, "col_spacing": 1, "fields": null, "compact": false}` |
| `entity_batch_create` | xử lý hàng loạt | Thực hiện thao tác đối tượng hàng loạt tạo trong bản vẽ CAD. | Khi cần xử lý hàng loạt. | `{"entities": []}` |
| `entity_batch_modify` | xử lý hàng loạt | Thực hiện thao tác đối tượng hàng loạt sửa trong bản vẽ CAD. | Khi cần xử lý hàng loạt. | `{"operations": []}` |
| `entity_chamfer` | corner_ops | Thực hiện thao tác đối tượng chamfer trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"handle1": "A1B2", "handle2": "A1B2", "dist1": 1, "dist2": null, "trim": true}` |
| `entity_change_space` | bố cục | Thực hiện thao tác đối tượng change space trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | `{"handles": [], "viewport_handle": "A1B2", "direction": "to_paper", "freeze_dimensions": false}` |
| `entity_copy` | sửa đối tượng | Thực hiện thao tác đối tượng sao chép trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | `{"handle": "A1B2", "dx": 1, "dy": 1, "dz": 0.0}` |
| `entity_create_arc` | tạo đối tượng | Thực hiện thao tác đối tượng tạo cung trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | `{"cx": 1, "cy": 1, "radius": 1, "start_angle": 1, "end_angle": 1, "layer": null, "color": null}` |
| `entity_create_block_ref` | khối | Thực hiện thao tác đối tượng tạo khối ref trong bản vẽ CAD. | Khi cần khối và tham chiếu khối. | `{"name": "vi-du", "x": 1, "y": 1, "scale_x": 1.0, "scale_y": 1.0, "rotation": 0.0, "layer": null}` |
| `entity_create_circle` | tạo đối tượng | Thực hiện thao tác đối tượng tạo đường tròn trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | `{"cx": 1, "cy": 1, "radius": 1, "layer": null, "color": null}` |
| `entity_create_ellipse` | tạo đối tượng | Thực hiện thao tác đối tượng tạo ellipse trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | `{"cx": 1, "cy": 1, "major_x": 1, "major_y": 1, "ratio": 0.5, "layer": null, "color": null}` |
| `entity_create_hatch` | tạo đối tượng | Thực hiện thao tác đối tượng tạo tô mặt trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | `{"pattern": "vi-du", "boundary_points": [], "scale": 1.0, "angle": 0.0, "layer": null, "color": null}` |
| `entity_create_line` | tạo đối tượng | Thực hiện thao tác đối tượng tạo đường trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | `{"x1": 1, "y1": 1, "x2": 1, "y2": 1, "z1": 0.0, "z2": 0.0, "layer": null, "color": null, "linetype": null}` |
| `entity_create_mtext` | tạo đối tượng | Thực hiện thao tác đối tượng tạo mtext trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | `{"text": "vi-du", "x": 1, "y": 1, "width": 100.0, "height": 2.5, "rotation": 0.0, "layer": null, "color": null}` |
| `entity_create_point` | tạo đối tượng | Thực hiện thao tác đối tượng tạo điểm trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | `{"x": 1, "y": 1, "layer": null, "color": null}` |
| `entity_create_polyline` | tạo đối tượng | Thực hiện thao tác đối tượng tạo đa tuyến trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | `{"points": [], "closed": false, "layer": null, "color": null}` |
| `entity_create_rectangle` | tạo đối tượng | Thực hiện thao tác đối tượng tạo hình chữ nhật trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | `{"x1": 1, "y1": 1, "x2": 1, "y2": 1, "layer": null, "color": null}` |
| `entity_create_revcloud` | tạo đối tượng | Thực hiện thao tác đối tượng tạo revcloud trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | `{"points": [], "segment_length": 1, "layer": "", "closed": true}` |
| `entity_create_spline` | tạo đối tượng | Thực hiện thao tác đối tượng tạo spline trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | `{"fit_points": [], "layer": null, "color": null}` |
| `entity_create_table` | tạo đối tượng | Thực hiện thao tác đối tượng tạo bảng trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | `{"x": 1, "y": 1, "rows": [], "headers": null, "column_widths": null, "row_height": 7.0, "text_height": 2.5, "title": null, "layer": "TEXT"}` |
| `entity_create_text` | tạo đối tượng | Thực hiện thao tác đối tượng tạo chữ trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | `{"text": "vi-du", "x": 1, "y": 1, "height": 2.5, "rotation": 0.0, "layer": null, "color": null}` |
| `entity_create_wipeout` | tạo đối tượng | Thực hiện thao tác đối tượng tạo wipeout trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | `{"points": [], "layer": ""}` |
| `entity_delete` | sửa đối tượng | Thực hiện thao tác đối tượng xóa trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | `{"handle": "A1B2"}` |
| `entity_delete_many` | sửa đối tượng | Thực hiện thao tác đối tượng xóa many trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | `{"handles": []}` |
| `entity_edit_geometry` | sửa đối tượng | Thực hiện thao tác đối tượng edit geometry trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | `{"handle": "A1B2", "cx": null, "cy": null, "radius": null, "x1": null, "y1": null, "x2": null, "y2": null, "start_angle": null, "end_angle": null}` |
| `entity_edit_text` | sửa đối tượng | Thực hiện thao tác đối tượng edit chữ trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | `{"handle": "A1B2", "text": null, "height": null, "rotation": null}` |
| `entity_extend` | corner_ops | Thực hiện thao tác đối tượng kéo dài trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"target_handle": "D:\\DuAn\\ban-ve.dwg", "boundary_handle": "A1B2", "end_x": null, "end_y": null}` |
| `entity_fillet` | corner_ops | Thực hiện thao tác đối tượng fillet trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"handle1": "A1B2", "handle2": "A1B2", "radius": 1, "trim": true}` |
| `entity_get` | tra cứu đối tượng | Thực hiện thao tác đối tượng get trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. | `{"handle": "A1B2"}` |
| `entity_get_xdata` | tra cứu đối tượng | Thực hiện thao tác đối tượng get xdata trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. | `{"handle": "A1B2", "app_name": null}` |
| `entity_list` | tra cứu đối tượng | Thực hiện thao tác đối tượng liệt kê trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. | `{"type_filter": null, "layer_filter": null, "limit": 100, "offset": 0, "fields": null, "compact": false}` |
| `entity_mirror` | sửa đối tượng | Thực hiện thao tác đối tượng đối xứng trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | `{"handle": "A1B2", "x1": 1, "y1": 1, "x2": 1, "y2": 1, "delete_original": false}` |
| `entity_move` | sửa đối tượng | Thực hiện thao tác đối tượng di chuyển trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | `{"handle": "A1B2", "dx": 1, "dy": 1, "dz": 0.0}` |
| `entity_offset` | sửa đối tượng | Thực hiện thao tác đối tượng song song trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | `{"handle": "A1B2", "distance": 1, "side_x": null, "side_y": null}` |
| `entity_rotate` | sửa đối tượng | Thực hiện thao tác đối tượng xoay trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | `{"handle": "A1B2", "base_x": 1, "base_y": 1, "angle_deg": 1}` |
| `entity_scale` | sửa đối tượng | Thực hiện thao tác đối tượng tỷ lệ trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | `{"handle": "A1B2", "base_x": 1, "base_y": 1, "factor": 1}` |
| `entity_select_smart` | nâng cao | Thực hiện thao tác đối tượng chọn smart trong bản vẽ CAD. | Khi cần chức năng nâng cao. | `{"predicate": {}, "fields": null, "compact": false}` |
| `entity_set_properties` | sửa đối tượng | Thực hiện thao tác đối tượng đặt thuộc tính trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | `{"handle": "A1B2", "layer": null, "color": null, "linetype": null, "lineweight": null, "visible": null}` |
| `entity_set_xdata` | sửa đối tượng | Thực hiện thao tác đối tượng đặt xdata trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | `{"handle": "A1B2", "app_name": "vi-du", "values": []}` |
| `entity_trim` | corner_ops | Thực hiện thao tác đối tượng cắt trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"target_handle": "D:\\DuAn\\ban-ve.dwg", "cutter_handle": "A1B2", "keep_x": 1, "keep_y": 1}` |
| `gd_frame` | kỹ thuật | Thực hiện thao tác gd frame trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | `{"symbol": "vi-du", "tolerance": 1, "x": 1, "y": 1, "datums": null, "height": 5.0, "diameter": false, "modifier": null, "layer": null}` |
| `gear_draw_helical_front_view` | kỹ thuật | Thực hiện thao tác gear draw helical front góc nhìn trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | `{"module": 1, "teeth": 1, "helix_angle": 1, "pressure_angle": 20.0, "hand": "RH", "center_x": 0.0, "center_y": 0.0, "bore_diameter": null, "keyway_width": null, "keyway_depth": null}` |
| `gear_draw_section_aa` | kỹ thuật | Thực hiện thao tác gear draw mặt cắt aa trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | `{"gear_metadata": {}, "x_offset": 1, "face_width": 1}` |
| `gear_draw_spur_front_view` | kỹ thuật | Thực hiện thao tác gear draw spur front góc nhìn trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | `{"module": 1, "teeth": 1, "pressure_angle": 20.0, "center_x": 0.0, "center_y": 0.0, "bore_diameter": null, "keyway_width": null, "keyway_depth": null}` |
| `hatch_add_boundary` | tạo đối tượng | Thực hiện thao tác tô mặt add boundary trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | `{"handle": "A1B2", "edges": []}` |
| `hatch_edit` | tạo đối tượng | Thực hiện thao tác tô mặt edit trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | `{"handle": "A1B2", "pattern": "", "scale": null, "angle": null, "color": null, "style": ""}` |
| `hatch_material` | cơ khí | Thực hiện thao tác tô mặt material trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | `{"material": "steel", "boundary": null, "handles": null, "scale": 1.0, "angle": null, "layer": null}` |
| `hatch_set_gradient` | tạo đối tượng | Thực hiện thao tác tô mặt đặt gradient trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | `{"handle": "A1B2", "color1": [], "color2": [], "rotation": 0.0, "centered": 0.0, "one_color": false, "tint": 0.0, "name": "LINEAR"}` |
| `image_attach` | tờ bản vẽ | Thực hiện thao tác hình ảnh đính kèm trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | `{"path": "D:\\DuAn\\ban-ve.dwg", "x": 0.0, "y": 0.0, "scale": 1.0, "rotation": 0.0, "auto_layout": false, "layout": "", "paper": "A1", "orientation": "landscape"}` |
| `keyway_draw_keyed_bore` | kỹ thuật | Thực hiện thao tác keyway draw keyed bore trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | `{"center_x": 1, "center_y": 1, "bore_diameter": 1, "keyway_width": null, "keyway_depth": null, "layer": "GEOMETRY"}` |
| `keyway_draw_section` | kỹ thuật | Thực hiện thao tác keyway draw mặt cắt trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | `{"center_x": 1, "center_y": 1, "bore_diameter": 1, "face_width": 1, "keyway_width": null, "keyway_depth": null}` |
| `kho_industries` | mở rộng cadtroly | Thực hiện thao tác kho industries trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{}` |
| `kho_rules_export` | mở rộng cadtroly | Thực hiện thao tác kho rules xuất trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{}` |
| `kho_rules_import` | mở rộng cadtroly | Thực hiện thao tác kho rules nhập trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"rules": []}` |
| `kho_skill_add` | mở rộng cadtroly | Thực hiện thao tác kho skill add trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"name": "vi-du", "content": "vi-du", "overwrite": false}` |
| `kho_skill_toggle` | mở rộng cadtroly | Thực hiện thao tác kho skill toggle trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"name": "vi-du", "enabled": true}` |
| `kho_skills` | mở rộng cadtroly | Thực hiện thao tác kho skills trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{}` |
| `kho_standard_add` | mở rộng cadtroly | Thực hiện thao tác kho standard add trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"standard": {}, "overwrite": false}` |
| `kho_standard_delete` | mở rộng cadtroly | Thực hiện thao tác kho standard xóa trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"standard_id": "vi-du", "confirm": false}` |
| `kho_standards` | mở rộng cadtroly | Thực hiện thao tác kho standards trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"industry": null}` |
| `kho_status` | mở rộng cadtroly | Thực hiện thao tác kho trạng thái trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{}` |
| `layer_create` | lớp bản vẽ | Thực hiện thao tác lớp tạo trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | `{"name": "vi-du", "color": 7, "linetype": "Continuous", "lineweight": -3}` |
| `layer_delete` | lớp bản vẽ | Thực hiện thao tác lớp xóa trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | `{"name": "vi-du"}` |
| `layer_freeze` | lớp bản vẽ | Thực hiện thao tác lớp freeze trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | `{"name": "vi-du"}` |
| `layer_hide` | lớp bản vẽ | Thực hiện thao tác lớp hide trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | `{"name": "vi-du"}` |
| `layer_isolate` | lớp bản vẽ | Thực hiện thao tác lớp isolate trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | `{"name": "vi-du"}` |
| `layer_list` | lớp bản vẽ | Thực hiện thao tác lớp liệt kê trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | `{"fields": null, "compact": false}` |
| `layer_lock` | lớp bản vẽ | Thực hiện thao tác lớp khóa trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | `{"name": "vi-du"}` |
| `layer_modify` | lớp bản vẽ | Thực hiện thao tác lớp sửa trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | `{"name": "vi-du", "color": null, "linetype": null, "lineweight": null}` |
| `layer_set_current` | lớp bản vẽ | Thực hiện thao tác lớp đặt hiện tại trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | `{"name": "vi-du"}` |
| `layer_show` | lớp bản vẽ | Thực hiện thao tác lớp show trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | `{"name": "vi-du"}` |
| `layer_state_delete` | môi trường | Thực hiện thao tác lớp state xóa trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{"name": "vi-du"}` |
| `layer_state_list` | môi trường | Thực hiện thao tác lớp state liệt kê trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{}` |
| `layer_state_restore` | môi trường | Thực hiện thao tác lớp state restore trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{"name": "vi-du", "properties": null}` |
| `layer_state_save` | môi trường | Thực hiện thao tác lớp state lưu trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{"name": "vi-du", "description": null}` |
| `layer_thaw` | lớp bản vẽ | Thực hiện thao tác lớp thaw trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | `{"name": "vi-du"}` |
| `layer_unlock` | lớp bản vẽ | Thực hiện thao tác lớp unlock trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | `{"name": "vi-du"}` |
| `layout_copy` | bố cục | Thực hiện thao tác bố cục sao chép trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | `{"source": "D:\\DuAn\\ban-ve.dwg", "new_name": "vi-du"}` |
| `layout_create` | bố cục | Thực hiện thao tác bố cục tạo trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | `{"name": "vi-du"}` |
| `layout_delete` | bố cục | Thực hiện thao tác bố cục xóa trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | `{"name": "vi-du"}` |
| `layout_list` | bố cục | Thực hiện thao tác bố cục liệt kê trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | `{}` |
| `layout_rename` | bố cục | Thực hiện thao tác bố cục đổi tên trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | `{"old_name": "vi-du", "new_name": "vi-du"}` |
| `layout_set_current` | bố cục | Thực hiện thao tác bố cục đặt hiện tại trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | `{"name": "vi-du"}` |
| `leader_create_mleader` | tạo đối tượng | Thực hiện thao tác đường dẫn tạo mleader trong bản vẽ CAD. | Khi cần vẽ thêm đối tượng. | `{"points": [], "text": "vi-du", "text_height": 2.5, "landing_gap": 1.0, "arrow_size": 2.5, "layer": "DIM"}` |
| `linetype_list` | lớp bản vẽ | Thực hiện thao tác linetype liệt kê trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | `{}` |
| `linetype_load` | lớp bản vẽ | Thực hiện thao tác linetype nạp trong bản vẽ CAD. | Khi cần tạo và quản lý lớp bản vẽ. | `{"name": "vi-du", "file": null}` |
| `mech_dimension_part` | cơ khí | Thực hiện thao tác mech kích thước part trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | `{"part_id": null, "style": "chain", "hole_table_threshold": 8, "fits": null, "views": null}` |
| `mech_hole_pattern` | cơ khí | Thực hiện thao tác mech hole pattern trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | `{"pattern": "vi-du", "x": 1, "y": 1, "diameter": 1, "count": 2, "spacing": 0.0, "count_y": 1, "spacing_y": 0.0, "pcd": 0.0, "start_angle": 0.0, "angle": 0.0, "layer": null, "centre_marks": true, "dimension": false}` |
| `mech_part_draw` | cơ khí | Thực hiện thao tác mech part draw trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | `{"spec": {}, "at_x": 0.0, "at_y": 0.0, "rotation": 0.0, "views": null, "projection": "first", "dimension": true, "style": "chain"}` |
| `mech_part_from_spec` | cơ khí | Thực hiện thao tác mech part từ spec trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | `{"spec": {}}` |
| `mech_part_inspect` | cơ khí | Thực hiện thao tác mech part inspect trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | `{"part_id": null}` |
| `mech_view_add` | cơ khí | Thực hiện thao tác mech góc nhìn add trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | `{"part_id": null, "kind": "section", "side": "right", "style": "full", "plane": null, "detail": null, "gap": 20.0, "scale": 1.0}` |
| `mleaderstyle_create` | kiểu hiển thị | Thực hiện thao tác mleaderstyle tạo trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | `{"name": "vi-du", "preset": "vi-du", "overrides": null}` |
| `mleaderstyle_list` | kiểu hiển thị | Thực hiện thao tác mleaderstyle liệt kê trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | `{}` |
| `page_setup_apply` | thiết lập trang | Thực hiện thao tác trang cài đặt apply trong bản vẽ CAD. | Khi cần khổ giấy, tỷ lệ và in ấn. | `{"layout": "vi-du", "paper": "vi-du", "orientation": "landscape", "plot_style": "monochrome.ctb", "scale": "fit", "plot_area": "layout", "device": "DWG To PDF.pc3", "margins_mm": null, "center": true}` |
| `page_setup_list` | thiết lập trang | Thực hiện thao tác trang cài đặt liệt kê trong bản vẽ CAD. | Khi cần khổ giấy, tỷ lệ và in ấn. | `{"layout": null}` |
| `pdf_to_dwg` | mở rộng cadtroly | Thực hiện thao tác pdf đến dwg trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"source": "D:\\DuAn\\ban-ve.dwg", "target": "D:\\DuAn\\ban-ve.dwg", "paper": "A1", "orientation": "landscape", "layout": "A1-SEMANTIC"}` |
| `pdf_vectorize` | mở rộng cadtroly | Thực hiện thao tác pdf vectorize trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"source": "D:\\DuAn\\ban-ve.dwg", "target": "D:\\DuAn\\ban-ve.dwg"}` |
| `pid_equipment_list` | P&ID | Thực hiện thao tác P&ID equipment liệt kê trong bản vẽ CAD. | Khi cần sơ đồ P&ID. | `{"csv_path": null, "tolerance": 0.5, "scope": "current_space"}` |
| `pid_from_spec` | P&ID | Thực hiện thao tác P&ID từ spec trong bản vẽ CAD. | Khi cần sơ đồ P&ID. | `{"spec": {}, "dry_run": false}` |
| `pid_graph` | P&ID | Thực hiện thao tác P&ID graph trong bản vẽ CAD. | Khi cần sơ đồ P&ID. | `{"tolerance": 0.5, "label_search": 15.0, "scope": "current_space", "include_foreign": true, "include_geometry": false}` |
| `pid_instrument_index` | P&ID | Thực hiện thao tác P&ID instrument index trong bản vẽ CAD. | Khi cần sơ đồ P&ID. | `{"csv_path": null, "tolerance": 0.5, "scope": "current_space"}` |
| `pid_line_draw` | P&ID | Thực hiện thao tác P&ID đường draw trong bản vẽ CAD. | Khi cần sơ đồ P&ID. | `{"from_": {}, "to": {}, "line_class": "process_major", "route": "auto", "stub": 5.0, "line_number": null, "size": null, "service": null, "spec": null, "insulation": null, "number_format": null, "label": true, "arrow": null}` |
| `pid_line_list` | P&ID | Thực hiện thao tác P&ID đường liệt kê trong bản vẽ CAD. | Khi cần sơ đồ P&ID. | `{"csv_path": null, "tolerance": 0.5, "scope": "current_space"}` |
| `pid_symbol_insert` | P&ID | Thực hiện thao tác P&ID ký hiệu chèn trong bản vẽ CAD. | Khi cần sơ đồ P&ID. | `{"symbol": "vi-du", "x": 1, "y": 1, "rotation": 0.0, "scale": 1.0, "tag": null, "desc": null, "actuator": null, "fail": null, "type": null, "location": null, "params": null, "shape": null, "direction": null, "link": null, "layer": null}` |
| `pid_symbol_list` | P&ID | Thực hiện thao tác P&ID ký hiệu liệt kê trong bản vẽ CAD. | Khi cần sơ đồ P&ID. | `{"family": null}` |
| `pid_tag_parse` | P&ID | Thực hiện thao tác P&ID tag parse trong bản vẽ CAD. | Khi cần sơ đồ P&ID. | `{"tag": "vi-du", "kind": "auto", "equipment_prefixes": null}` |
| `pipe_takeoff` | nhà máy | Thực hiện thao tác pipe takeoff trong bản vẽ CAD. | Khi cần bố trí thiết bị nhà máy. | `{"pid_path": null, "layout_path": null, "output": null, "lang": "en", "services": null, "allowance": 0.2, "vertical_allowance": 0.0, "length_source": "auto", "force": false, "layers": null, "tol": null, "exclude_regions": null}` |
| `plot_style_list` | thiết lập trang | Thực hiện thao tác plot kiểu liệt kê trong bản vẽ CAD. | Khi cần khổ giấy, tỷ lệ và in ấn. | `{}` |
| `point_from_snap` | nâng cao | Thực hiện thao tác điểm từ snap trong bản vẽ CAD. | Khi cần chức năng nâng cao. | `{"handle": "A1B2", "snap": "vi-du", "ref_x": null, "ref_y": null}` |
| `point_intersection` | nâng cao | Thực hiện thao tác điểm intersection trong bản vẽ CAD. | Khi cần chức năng nâng cao. | `{"handle1": "A1B2", "handle2": "A1B2", "ref_x": null, "ref_y": null}` |
| `point_tangent` | nâng cao | Thực hiện thao tác điểm tangent trong bản vẽ CAD. | Khi cần chức năng nâng cao. | `{"circle_handle": "A1B2", "from_x": 1, "from_y": 1, "ref_x": null, "ref_y": null}` |
| `revision_add` | tờ bản vẽ | Thực hiện thao tác revision add trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | `{"rev": "vi-du", "description": "vi-du", "date": "", "by": "", "clouds": null, "tags": null, "size": "A3", "orientation": "landscape", "origin_x": 0.0, "origin_y": 0.0, "cloud_segment": 8.0, "layout": ""}` |
| `section_line` | cơ khí | Thực hiện thao tác mặt cắt đường trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | `{"x1": 1, "y1": 1, "x2": 1, "y2": 1, "label": "A", "direction": null, "style": "full", "height": 5.0, "layer": null}` |
| `selection_filter` | tra cứu đối tượng | Thực hiện thao tác selection filter trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. | `{"entity_type": "", "layer": "", "color": null, "linetype": "", "min_area": null}` |
| `selection_get` | tra cứu đối tượng | Thực hiện thao tác selection get trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. | `{"fields": null, "compact": false}` |
| `selection_polygon` | tra cứu đối tượng | Thực hiện thao tác selection đa giác trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. | `{"points": [], "mode": "window", "entity_type": "", "layer": ""}` |
| `selection_window` | tra cứu đối tượng | Thực hiện thao tác selection window trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. | `{"x1": 1, "y1": 1, "x2": 1, "y2": 1, "mode": "window", "entity_type": "", "layer": ""}` |
| `sheet_frame` | tờ bản vẽ | Thực hiện thao tác tờ bản vẽ frame trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | `{"size": "A3", "orientation": "landscape", "zones": true, "marks": true, "origin_x": 0.0, "origin_y": 0.0, "layout": ""}` |
| `solid_boolean` | khối đặc | Thực hiện thao tác khối đặc boolean trong bản vẽ CAD. | Khi cần hình học ba chiều và khối đặc. | `{"target_handle": "D:\\DuAn\\ban-ve.dwg", "tool_handle": "A1B2", "operation": "vi-du"}` |
| `solid_box` | khối đặc | Thực hiện thao tác khối đặc khung trong bản vẽ CAD. | Khi cần hình học ba chiều và khối đặc. | `{"cx": 1, "cy": 1, "cz": 1, "length": 1, "width": 1, "height": 1}` |
| `solid_cylinder` | khối đặc | Thực hiện thao tác khối đặc cylinder trong bản vẽ CAD. | Khi cần hình học ba chiều và khối đặc. | `{"cx": 1, "cy": 1, "cz": 1, "radius": 1, "height": 1}` |
| `solid_extrude` | khối đặc | Thực hiện thao tác khối đặc extrude trong bản vẽ CAD. | Khi cần hình học ba chiều và khối đặc. | `{"profile_handle": "D:\\DuAn\\ban-ve.dwg", "height": 1, "taper_angle": 0.0}` |
| `solid_revolve` | khối đặc | Thực hiện thao tác khối đặc revolve trong bản vẽ CAD. | Khi cần hình học ba chiều và khối đặc. | `{"profile_handle": "D:\\DuAn\\ban-ve.dwg", "axis_x1": 1, "axis_y1": 1, "axis_x2": 1, "axis_y2": 1, "angle": 360.0}` |
| `standards_reference` | mở rộng cadtroly | Thực hiện thao tác standards tham chiếu trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"discipline": null}` |
| `std_feature_draw` | cơ khí | Thực hiện thao tác std feature draw trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | `{"kind": "vi-du", "x": 1, "y": 1, "params": {}, "rotation": 0.0, "layer": null}` |
| `std_part_insert` | cơ khí | Thực hiện thao tác std part chèn trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | `{"designation": "vi-du", "x": 1, "y": 1, "view": "side", "rotation": 0.0, "layer": "GEOMETRY", "material": null}` |
| `std_part_list` | cơ khí | Thực hiện thao tác std part liệt kê trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | `{"query": null, "standard": null}` |
| `structural_qa` | mở rộng cadtroly | Thực hiện thao tác structural qa trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"discipline": "building"}` |
| `surface_texture` | cơ khí | Thực hiện thao tác surface texture trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | `{"x": 1, "y": 1, "ra": null, "rz": null, "machining": "any", "process": null, "lay": null, "allowance": null, "all_around": false, "leader_to": null, "height": 3.5, "rotation": 0.0, "standard": "ISO 21920-1", "layer": null}` |
| `system_about` | hệ thống | Thực hiện thao tác hệ thống thông tin trong bản vẽ CAD. | Khi cần trạng thái máy chủ. | `{}` |
| `system_capabilities` | tra cứu đối tượng | Thực hiện thao tác hệ thống capabilities trong bản vẽ CAD. | Khi cần tìm và đọc thuộc tính đối tượng. | `{}` |
| `system_get_variable` | hệ thống | Thực hiện thao tác hệ thống get variable trong bản vẽ CAD. | Khi cần trạng thái máy chủ. | `{"name": "vi-du"}` |
| `system_launch` | môi trường | Thực hiện thao tác hệ thống launch trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{"visible": true, "open_path": null}` |
| `system_preferences_get` | môi trường | Thực hiện thao tác hệ thống preferences get trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{"keys": null}` |
| `system_preferences_set` | môi trường | Thực hiện thao tác hệ thống preferences đặt trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{"key": "vi-du", "value": "vi-du"}` |
| `system_prompt_message` | môi trường | Thực hiện thao tác hệ thống prompt message trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{"text": "vi-du"}` |
| `system_run_command` | hệ thống | Thực hiện thao tác hệ thống run command trong bản vẽ CAD. | Khi cần trạng thái máy chủ. | `{"command": "vi-du"}` |
| `system_run_lisp` | hệ thống | Thực hiện thao tác hệ thống run lisp trong bản vẽ CAD. | Khi cần trạng thái máy chủ. | `{"expression": "vi-du"}` |
| `system_set_variable` | hệ thống | Thực hiện thao tác hệ thống đặt variable trong bản vẽ CAD. | Khi cần trạng thái máy chủ. | `{"name": "vi-du", "value": "vi-du"}` |
| `system_status` | hệ thống | Thực hiện thao tác hệ thống trạng thái trong bản vẽ CAD. | Khi cần trạng thái máy chủ. | `{}` |
| `system_variable_describe` | môi trường | Thực hiện thao tác hệ thống variable describe trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{"name": null, "search": null}` |
| `takeoff_compute` | mở rộng cadtroly | Thực hiện thao tác takeoff compute trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"path": "D:\\DuAn\\ban-ve.dwg", "height_m": null, "tru_lo_cua_m3": 0.0}` |
| `takeoff_decide` | mở rộng cadtroly | Thực hiện thao tác takeoff decide trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"path": "D:\\DuAn\\ban-ve.dwg", "kind": "vi-du", "name": "vi-du", "cong_tac": "vi-du", "don_vi": "vi-du", "cach_tinh": "vi-du", "tham_so": null, "save_rule": true}` |
| `takeoff_export` | mở rộng cadtroly | Thực hiện thao tác takeoff xuất trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"path": "D:\\DuAn\\ban-ve.dwg", "out": null, "height_m": null}` |
| `takeoff_propose` | mở rộng cadtroly | Thực hiện thao tác takeoff propose trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"path": "D:\\DuAn\\ban-ve.dwg"}` |
| `takeoff_run` | mở rộng cadtroly | Thực hiện thao tác takeoff run trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{"path": "D:\\DuAn\\ban-ve.dwg", "height_m": null}` |
| `template_apply_layers` | mẫu bản vẽ | Thực hiện thao tác mẫu apply layers trong bản vẽ CAD. | Khi cần mẫu bản vẽ. | `{"template": "vi-du"}` |
| `template_list` | mẫu bản vẽ | Thực hiện thao tác mẫu liệt kê trong bản vẽ CAD. | Khi cần mẫu bản vẽ. | `{}` |
| `text_find_replace` | sửa đối tượng | Thực hiện thao tác chữ tìm replace trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | `{"find": "vi-du", "replace": "vi-du", "layer": "", "match_case": true, "dry_run": false}` |
| `text_set_background` | sửa đối tượng | Thực hiện thao tác chữ đặt background trong bản vẽ CAD. | Khi cần sửa hoặc biến đổi đối tượng. | `{"handle": "A1B2", "enabled": true, "color": 0, "scale": 1.5}` |
| `textstyle_create` | kiểu hiển thị | Thực hiện thao tác textstyle tạo trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | `{"name": "vi-du", "font": "vi-du", "height": 0.0, "width_factor": 1.0, "oblique_deg": 0.0, "set_current": false}` |
| `textstyle_list` | kiểu hiển thị | Thực hiện thao tác textstyle liệt kê trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | `{}` |
| `textstyle_set_current` | kiểu hiển thị | Thực hiện thao tác textstyle đặt hiện tại trong bản vẽ CAD. | Khi cần kiểu và hiển thị. | `{"name": "vi-du"}` |
| `titleblock_apply` | tờ bản vẽ | Thực hiện thao tác titleblock apply trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | `{"title": "vi-du", "drawing_no": "vi-du", "size": "A3", "orientation": "landscape", "projection": "first", "part_no": "", "material": "", "scale": "1:1", "units": "mm", "drawn_by": "", "checked_by": "", "date": "", "sheet": "1/1", "revision": "A", "company": "Anka-Makine", "frame": true, "zones": false, "marks": false, "origin_x": 0.0, "origin_y": 0.0, "layout": ""}` |
| `titleblock_apply_iso_a3` | kỹ thuật | Thực hiện thao tác titleblock apply iso a3 trong bản vẽ CAD. | Khi cần kiểm tra kỹ thuật. | `{"title": "vi-du", "drawing_no": "vi-du", "part_no": "", "material": "", "scale": "1:1", "units": "mm", "drawn_by": "", "checked_by": "", "date": "", "sheet": "1/1", "revision": "A", "company": "Anka-Makine", "origin_x": 0.0, "origin_y": 0.0, "layout": ""}` |
| `transaction_begin` | giao dịch | Thực hiện thao tác giao dịch begin trong bản vẽ CAD. | Khi cần giao dịch thay đổi có kiểm soát. | `{}` |
| `transaction_commit` | giao dịch | Thực hiện thao tác giao dịch commit trong bản vẽ CAD. | Khi cần giao dịch thay đổi có kiểm soát. | `{}` |
| `transaction_rollback` | giao dịch | Thực hiện thao tác giao dịch rollback trong bản vẽ CAD. | Khi cần giao dịch thay đổi có kiểm soát. | `{}` |
| `ucs_list` | môi trường | Thực hiện thao tác ucs liệt kê trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{}` |
| `ucs_restore` | môi trường | Thực hiện thao tác ucs restore trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{"name": "vi-du"}` |
| `ucs_set` | môi trường | Thực hiện thao tác ucs đặt trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{"name": "vi-du", "origin": [], "x_axis": [], "y_axis": []}` |
| `user_pick_point` | môi trường | Thực hiện thao tác user pick điểm trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{"prompt": "vi-du"}` |
| `user_select` | môi trường | Thực hiện thao tác user chọn trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{"prompt": "vi-du", "mode": "single"}` |
| `validation_check` | xác nhận | Thực hiện thao tác validation kiểm tra trong bản vẽ CAD. | Khi cần kiểm tra hợp lệ. | `{"checks": null}` |
| `view_named_list` | môi trường | Thực hiện thao tác góc nhìn named liệt kê trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{}` |
| `view_named_restore` | môi trường | Thực hiện thao tác góc nhìn named restore trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{"name": "vi-du"}` |
| `view_named_save` | môi trường | Thực hiện thao tác góc nhìn named lưu trong bản vẽ CAD. | Khi cần kiểm tra kết nối và cấu hình. | `{"name": "vi-du", "center": null, "height": null, "width": null}` |
| `view_render_report` | mở rộng cadtroly | Thực hiện thao tác góc nhìn kết xuất report trong bản vẽ CAD. | Khi cần chức năng mở rộng của cadtroly. | `{}` |
| `view_screenshot` | góc nhìn | Thực hiện thao tác góc nhìn screenshot trong bản vẽ CAD. | Khi cần thu phóng, góc nhìn và ảnh chụp. | `{"overlay_handles": false}` |
| `view_zoom_and_screenshot` | góc nhìn | Thực hiện thao tác góc nhìn thu phóng và screenshot trong bản vẽ CAD. | Khi cần thu phóng, góc nhìn và ảnh chụp. | `{"x1": null, "y1": null, "x2": null, "y2": null}` |
| `view_zoom_extents` | góc nhìn | Thực hiện thao tác góc nhìn thu phóng extents trong bản vẽ CAD. | Khi cần thu phóng, góc nhìn và ảnh chụp. | `{}` |
| `view_zoom_window` | góc nhìn | Thực hiện thao tác góc nhìn thu phóng window trong bản vẽ CAD. | Khi cần thu phóng, góc nhìn và ảnh chụp. | `{"x1": 1, "y1": 1, "x2": 1, "y2": 1}` |
| `viewport_create` | bố cục | Thực hiện thao tác khung nhìn tạo trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | `{"layout": "vi-du", "center_x": 1, "center_y": 1, "width": 1, "height": 1, "view_center_x": 1, "view_center_y": 1, "scale": 1.0}` |
| `viewport_delete` | bố cục | Thực hiện thao tác khung nhìn xóa trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | `{"handle": "A1B2", "force": false}` |
| `viewport_list` | bố cục | Thực hiện thao tác khung nhìn liệt kê trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | `{"layout": ""}` |
| `viewport_lock` | bố cục | Thực hiện thao tác khung nhìn khóa trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | `{"handle": "A1B2", "locked": true}` |
| `viewport_set_scale` | bố cục | Thực hiện thao tác khung nhìn đặt tỷ lệ trong bản vẽ CAD. | Khi cần bố cục và khung nhìn. | `{"handle": "A1B2", "scale": 1}` |
| `weld_symbol` | cơ khí | Thực hiện thao tác mối hàn ký hiệu trong bản vẽ CAD. | Khi cần bản vẽ cơ khí. | `{"x": 1, "y": 1, "kind": "fillet", "size": null, "length": null, "pitch": null, "side": "arrow", "field_weld": false, "all_around": false, "process": null, "leader_to": null, "height": 3.5, "rotation": 0.0, "layer": null}` |
| `xref_attach` | tờ bản vẽ | Thực hiện thao tác tham chiếu ngoài đính kèm trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | `{"path": "D:\\DuAn\\ban-ve.dwg", "x": 0.0, "y": 0.0, "scale": 1.0, "rotation": 0.0, "kind": "attach"}` |
| `xref_manage` | tờ bản vẽ | Thực hiện thao tác tham chiếu ngoài quản lý trong bản vẽ CAD. | Khi cần tờ bản vẽ, khung tên và phát hành. | `{"action": "vi-du", "name": "", "new_path": ""}` |

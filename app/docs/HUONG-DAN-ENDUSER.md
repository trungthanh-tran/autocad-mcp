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

Bảng này gồm **272 tool** đang đăng ký, bao gồm cả **247 tool upstream** và tool mở rộng của cadtroly. Bạn có thể nói tên tool trong yêu cầu nếu muốn gọi trực tiếp.

| Tool | Nhóm | Làm gì | Dùng khi nào |
|---|---|---|---|
| `analysis_bounding_box` | `analysis` | Get the overall extents of everything drawn. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `analysis_entity_stats` | `analysis` | Count the drawing's objects, broken down by type and by layer. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `analysis_find_in_region` | `analysis` | List everything that falls inside a rectangular window. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `analysis_layer_stats` | `analysis` | Report how many entities, and which types, sit on each layer. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `analysis_list_properties` | `analysis` | Dump every DXF property of one entity, like LIST. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `analysis_measure_area` | `analysis` | Measure a polygon's area and perimeter from its vertices. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `analysis_measure_distance` | `analysis` | Measure the gap between two points: distance, dx/dy and angle. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `analysis_measure_entity` | `analysis` | Area and perimeter of an existing entity, by handle. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `analysis_select_by_layer` | `analysis` | Grab the handles of everything sitting on one layer. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `analysis_select_by_type` | `analysis` | Grab the handles of every entity of one type: all the circles, all the lines. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `arch_catalogue_insert` | `architecture` | Insert a furniture or sanitary item - bed, sofa, WC, basin, bathtub - as a block. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_catalogue_list` | `architecture` | Search the furniture and sanitary catalogue in English or Turkish. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_dimension_chains` | `architecture` | Dimension the plan's facades: openings, walls and overall chains outside each side. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_grid` | `architecture` | Draw a structural grid: axis lines with numbered and lettered bubbles at both ends. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_opening` | `architecture` | Host a door or a window in a drawn wall by distance along it; the wall is cut. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_plan_from_spec` | `architecture` | Draw a whole floor plan - walls, doors, windows, stairs, rooms, chains, schedules - in one transaction. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_room` | `architecture` | Label a room with its name, number and measured area. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_rooms_detect` | `architecture` | Find the rooms of any plan and measure them; never modifies it. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_schedule` | `architecture` | Draw a door, window or room schedule from the plan records. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_stair` | `architecture` | Draw a straight, L or U stair in plan and report its Blondel step rule. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_symbol` | `architecture` | Draw a plan symbol: north arrow, section mark, level mark or elevation mark. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `arch_wall` | `architecture` | Add walls to the plan: clean L/T/X junctions, cut openings, material poché. | Khi cần mặt bằng, mặt đứng, mặt cắt kiến trúc. |
| `balloon_add` | `sheet` | Add an ISO 6433 balloon linked to its item row. | Khi cần sheet, khung tên và phát hành. |
| `batch_plot` | `page_setup` | Plot every sheet (or the named ones) to PDF; each sheet size is read back from its PDF. | Khi cần khổ giấy, tỷ lệ và in ấn. |
| `block_create_from_entities` | `blocks` | Turn existing entities into a reusable block definition. | Khi cần block và block reference. |
| `block_define` | `blocks` | Define a block from typed primitives and attribute definitions, on both engines. | Khi cần block và block reference. |
| `block_explode` | `blocks` | Break a block reference apart into its component entities. | Khi cần block và block reference. |
| `block_find_references` | `blocks` | Find every place a given block is inserted. | Khi cần block và block reference. |
| `block_get_attributes` | `blocks` | Read the tag/value pairs off a block reference. | Khi cần block và block reference. |
| `block_insert` | `blocks` | Place a block, filling in its attribute values as you go. | Khi cần block và block reference. |
| `block_list` | `blocks` | List the block definitions the drawing already carries. | Khi cần block và block reference. |
| `block_set_attributes` | `blocks` | Fill in a block reference's attributes, such as title-block fields. | Khi cần block và block reference. |
| `bom_extract` | `sheet` | Read the bill of materials out of the drawing's block references. | Khi cần sheet, khung tên và phát hành. |
| `bom_table` | `sheet` | Draw the parts list as a real TABLE above the title block. | Khi cần sheet, khung tên và phát hành. |
| `boundary_from_entities` | `analysis` | Join named entities into one closed boundary polyline. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `boundary_trace` | `analysis` | Trace the closed boundary around a point, like BOUNDARY. | Khi cần đọc/đo/phân tích, không sửa bản vẽ. |
| `cable_takeoff` | `plant` | Cable takeoff: one row per load, Manhattan length to its panel, rounded up to the metre. | Khi cần bố trí thiết bị plant. |
| `cad_batch` | `batch` | Run an ordered list of tool calls in one round trip, binding results between steps. | Khi cần xử lý hàng loạt. |
| `centre_marks` | `mechanical` | Draw ISO 128-23 centre marks or centre lines on circles, read from the drawing. | Khi cần bản vẽ cơ khí. |
| `check_rulesets` | `cadtroly` | Liệt kê bộ quy tắc trong kho (tiêu chuẩn đã bóc + chuẩn công ty), kèm hiệu lực và số dòng chờ duyệt. | Khi cần chức năng mở rộng của cadtroly. |
| `check_run` | `cadtroly` | Luồng D: rà bản vẽ theo bộ quy tắc. Trả về từng vấn đề kèm điều khoản, handle, vị trí, có tự sửa được không. | Khi cần chức năng mở rộng của cadtroly. |
| `construction_clear` | `premium` | Wipe the construction scaffolding off the drawing before finalize. | Khi cần chức năng nâng cao. |
| `construction_xline` | `premium` | Lay down an infinite guide line to build geometry against. | Khi cần chức năng nâng cao. |
| `data_extract` | `sheet` | Write the bill of materials to a CSV file, or to XLSX when openpyxl is present. | Khi cần sheet, khung tên và phát hành. |
| `datum_feature` | `engineering` | Mark a datum on a feature: filled triangle plus the boxed datum letter. | Khi cần kiểm tra kỹ thuật. |
| `dimension_aligned` | `dimensions` | Dimension the true distance between two points, along a slope. | Khi cần kích thước và ghi chú dim. |
| `dimension_angular` | `dimensions` | Dimension the included angle between two rays from a vertex. | Khi cần kích thước và ghi chú dim. |
| `dimension_auto` | `premium` | Dimension a set of entities at once, as a chain, baseline or ordinate run. | Khi cần chức năng nâng cao. |
| `dimension_diameter` | `dimensions` | Call out a hole or shaft diameter, optionally to a fit such as H7. | Khi cần kích thước và ghi chú dim. |
| `dimension_linear` | `dimensions` | Dimension a horizontal or vertical size, with an ISO 129 tolerance or ISO 286 fit. | Khi cần kích thước và ghi chú dim. |
| `dimension_radius` | `dimensions` | Call out the radius of a circle or arc, optionally toleranced. | Khi cần kích thước và ghi chú dim. |
| `dimstyle_create` | `styles` | Create a dimension style from the ISO-25 or ANSI preset, with per-variable overrides. | Khi cần style và hiển thị. |
| `dimstyle_list` | `styles` | List dimension styles with their ISO-25/ANSI variables and the current one. | Khi cần style và hiển thị. |
| `dimstyle_modify` | `styles` | Change DIM* variables on an existing dimension style; reports only what moved. | Khi cần style và hiển thị. |
| `dimstyle_set_current` | `styles` | Make a dimension style current so new dimensions use it. | Khi cần style và hiển thị. |
| `document_activate` | `environment` | Switch which open document every later tool call targets. | Khi cần kiểm tra kết nối và cấu hình. |
| `document_close` | `environment` | Close one open document by name; never drops unsaved work unless told to. | Khi cần kiểm tra kết nối và cấu hình. |
| `document_list` | `environment` | List the open documents: which is active, which have unsaved changes. | Khi cần kiểm tra kết nối và cấu hình. |
| `drawing_apply_discipline_standard` | `cadtroly` | Set up a drawing for a civil/architectural discipline in one call. | Khi cần chức năng mở rộng của cadtroly. |
| `drawing_apply_iso_layers` | `premium` | Set up a standard ISO layer set with the right colours and lineweights. | Khi cần chức năng nâng cao. |
| `drawing_apply_standard` | `styles` | Put the drawing on ISO or ANSI in one call: dimstyle, text style, units, mech layers. | Khi cần style và hiển thị. |
| `drawing_audit` | `drawing` | Scan the drawing for structural errors and repair what it finds. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_close` | `drawing` | Close the drawing, saving first unless you say otherwise. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_critique` | `premium` | Review the drawing for drafting mistakes: must come back empty before finalize. | Khi cần chức năng nâng cao. |
| `drawing_deliver` | `engineering` | Hand the drawing off: a hashed, validated bundle of files plus a manifest. | Khi cần kiểm tra kỹ thuật. |
| `drawing_diff` | `understanding` | Compare two revisions of a drawing: what moved, changed, was added or removed. | Khi cần đọc hiểu cấu trúc bản vẽ. |
| `drawing_entities` | `cadtroly` | Liệt kê đối tượng theo layer/block/loại kèm handle, toạ độ, chiều dài, diện tích, text. | Khi cần chức năng mở rộng của cadtroly. |
| `drawing_export_dwg` | `sheet` | Write the drawing as a real DWG at a chosen AutoCAD version. | Khi cần sheet, khung tên và phát hành. |
| `drawing_export_dxf` | `drawing` | Write a DXF interchange copy of the drawing. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_export_pdf` | `drawing` | Plot the drawing, or one paper-space layout, to PDF. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_finalize` | `engineering` | Finish the drawing: validate, critique, save, screenshot and score it. | Khi cần kiểm tra kỹ thuật. |
| `drawing_info` | `entity_query` | Read the current drawing's name, path, extents and object counts. | Khi cần tìm và đọc thuộc tính đối tượng. |
| `drawing_new` | `drawing` | Start a drawing: blank with the engineering layers, or from a bundled/own template. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_open` | `drawing` | Load an existing DXF from disk (DWG only on the live AutoCAD backend). | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_plan` | `premium` | Commit sheet size, scale, layer set and dimension style before any geometry. | Khi cần chức năng nâng cao. |
| `drawing_preflight` | `premium` | Check the brief before you draw: units, part type, tolerances, missing inputs. | Khi cần chức năng nâng cao. |
| `drawing_properties_get` | `environment` | Read the drawing's title, subject, author, keywords, comments and custom properties. | Khi cần kiểm tra kết nối và cấu hình. |
| `drawing_properties_set` | `environment` | Set the drawing's summary fields and add, change or delete custom properties. | Khi cần kiểm tra kết nối và cấu hình. |
| `drawing_purge` | `drawing` | Strip unused layers, blocks, linetypes and styles out of the file. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_read` | `cadtroly` | Đọc bản vẽ thành số liệu: layer, block, số đối tượng, đơn vị. Không gửi gì đi. | Khi cần chức năng mở rộng của cadtroly. |
| `drawing_redo` | `drawing` | Reapply the operation you just undid. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_refine` | `premium` | Auto-repair what the critique found, then re-check, up to three rounds. | Khi cần chức năng nâng cao. |
| `drawing_save` | `drawing` | Write the drawing back to its file, or to a path you give. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_save_as` | `drawing` | Save a copy under a new name; the extension picks DXF, DWG or DWT. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `drawing_scale_check` | `understanding` | Is this drawing to scale against a reference? Tag distances, ratios, a verdict. | Khi cần đọc hiểu cấu trúc bản vẽ. |
| `drawing_settings` | `system` | Read or change drawing units, precision, linetype and dimension scale by name. | Khi cần trạng thái server. |
| `drawing_template_list` | `page_setup` | List the five bundled drawing templates: standard, sheet, layers, styles, page setup. | Khi cần khổ giấy, tỷ lệ và in ấn. |
| `drawing_template_save` | `page_setup` | Save the current drawing as a template: .dwt on live AutoCAD, .dxf headlessly. | Khi cần khổ giấy, tỷ lệ và in ấn. |
| `drawing_topology_check` | `understanding` | Find dangling ends, near misses and unjoined crossings in a pipe or cable network. | Khi cần đọc hiểu cấu trúc bản vẽ. |
| `drawing_understand` | `understanding` | Read a foreign drawing: units, extents, clusters, layers, tags, rooms, languages. | Khi cần đọc hiểu cấu trúc bản vẽ. |
| `drawing_undo` | `drawing` | Step back one operation. | Khi cần mở, lưu, đóng hoặc xuất bản vẽ. |
| `entity_array_polar` | `entity_modification` | Repeat an entity around a centre: a bolt circle or radial pattern. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_array_rectangular` | `entity_modification` | Repeat an entity in a grid of rows and columns. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_batch_create` | `batch` | Draw many entities in one call instead of one round trip each. | Khi cần xử lý hàng loạt. |
| `entity_batch_modify` | `batch` | Move, rotate, scale, restyle or delete many entities in one call. | Khi cần xử lý hàng loạt. |
| `entity_chamfer` | `corner_ops` | Bevel a corner between two lines by two setback distances. | Khi cần chức năng mở rộng của cadtroly. |
| `entity_change_space` | `layouts` | Move entities between model space and a sheet through a viewport. | Khi cần layout và viewport. |
| `entity_copy` | `entity_modification` | Duplicate an entity and offset the copy. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_create_arc` | `entity_creation` | Draw a circular arc from a centre, a radius and two angles. | Khi cần vẽ thêm đối tượng. |
| `entity_create_block_ref` | `blocks` | Drop an instance of an existing block definition into the drawing. | Khi cần block và block reference. |
| `entity_create_circle` | `entity_creation` | Draw a circle: a hole, a bore, a pitch circle. | Khi cần vẽ thêm đối tượng. |
| `entity_create_ellipse` | `entity_creation` | Draw an ellipse from its centre, major axis vector and axis ratio. | Khi cần vẽ thêm đối tượng. |
| `entity_create_hatch` | `entity_creation` | Fill a closed boundary with a section pattern such as ANSI31 or SOLID. | Khi cần vẽ thêm đối tượng. |
| `entity_create_line` | `entity_creation` | Draw a straight line between two points. | Khi cần vẽ thêm đối tượng. |
| `entity_create_mtext` | `entity_creation` | Place a wrapped paragraph note in a text box of a given width. | Khi cần vẽ thêm đối tượng. |
| `entity_create_point` | `entity_creation` | Place a point marker (node) at a coordinate. | Khi cần vẽ thêm đối tượng. |
| `entity_create_polyline` | `entity_creation` | Draw a connected outline or closed profile through a list of points. | Khi cần vẽ thêm đối tượng. |
| `entity_create_rectangle` | `entity_creation` | Draw a closed rectangle from two opposite corners. | Khi cần vẽ thêm đối tượng. |
| `entity_create_revcloud` | `entity_creation` | Draw a revision cloud around an area. | Khi cần vẽ thêm đối tượng. |
| `entity_create_spline` | `entity_creation` | Draw a smooth NURBS curve through fit points. | Khi cần vẽ thêm đối tượng. |
| `entity_create_table` | `entity_creation` | Place a parts list, BOM or schedule as a table with headers and rows. | Khi cần vẽ thêm đối tượng. |
| `entity_create_text` | `entity_creation` | Place a single-line text label. | Khi cần vẽ thêm đối tượng. |
| `entity_create_wipeout` | `entity_creation` | Mask whatever is behind a closed polygon on the sheet. | Khi cần vẽ thêm đối tượng. |
| `entity_delete` | `entity_modification` | Erase one entity by handle. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_delete_many` | `entity_modification` | Erase a whole list of entities in one call. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_edit_geometry` | `entity_modification` | Change a circle's radius, a line's endpoints or an arc's angles in place. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_edit_text` | `entity_modification` | Reword a label, or change its height or rotation, keeping its handle. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_extend` | `corner_ops` | Lengthen a line until it meets a boundary line. | Khi cần chức năng mở rộng của cadtroly. |
| `entity_fillet` | `corner_ops` | Round a corner between two lines with a tangent arc. | Khi cần chức năng mở rộng của cadtroly. |
| `entity_get` | `entity_query` | Inspect one entity by handle: type, layer, colour and geometry. | Khi cần tìm và đọc thuộc tính đối tượng. |
| `entity_get_xdata` | `entity_query` | Read an entity's extended data (XDATA) by application name. | Khi cần tìm và đọc thuộc tính đối tượng. |
| `entity_list` | `entity_query` | Browse the drawing's entities and their handles, filtered by type or layer. | Khi cần tìm và đọc thuộc tính đối tượng. |
| `entity_mirror` | `entity_modification` | Reflect an entity across a mirror line, keeping or dropping the original. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_move` | `entity_modification` | Shift an entity by a displacement vector. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_offset` | `entity_modification` | Make a parallel copy of a line, circle or polyline at a set distance. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_rotate` | `entity_modification` | Turn an entity about a base point by an angle in degrees. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_scale` | `entity_modification` | Resize an entity uniformly about a base point. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_select_smart` | `premium` | Pick every entity matching a description: type, layer, colour, length, location. | Khi cần chức năng nâng cao. |
| `entity_set_properties` | `entity_modification` | Change an entity's layer, colour, linetype, lineweight or visibility. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_set_xdata` | `entity_modification` | Attach or replace extended data (XDATA) on an entity. | Khi cần sửa hoặc biến đổi đối tượng. |
| `entity_trim` | `corner_ops` | Cut a line back to where another crosses it, keeping the side you point at. | Khi cần chức năng mở rộng của cadtroly. |
| `gd_frame` | `engineering` | Draw an ISO 1101 feature control frame: symbol, tolerance zone and datums. | Khi cần kiểm tra kỹ thuật. |
| `gear_draw_helical_front_view` | `engineering` | Draw a helical gear front view: true involute teeth, circles, bore and keyway. | Khi cần kiểm tra kỹ thuật. |
| `gear_draw_section_aa` | `engineering` | Draw the hatched side cross-section A-A of a gear you already drew. | Khi cần kiểm tra kỹ thuật. |
| `gear_draw_spur_front_view` | `engineering` | Draw a straight-tooth spur gear front view with true involute teeth. | Khi cần kiểm tra kỹ thuật. |
| `hatch_add_boundary` | `entity_creation` | Add a boundary path to a hatch, arcs and ellipses included. | Khi cần vẽ thêm đối tượng. |
| `hatch_edit` | `entity_creation` | Change a hatch's pattern, scale, angle, colour or island style. | Khi cần vẽ thêm đối tượng. |
| `hatch_material` | `mechanical` | Hatch a region with the ISO 128-50 section pattern for a named material. | Khi cần bản vẽ cơ khí. |
| `hatch_set_gradient` | `entity_creation` | Replace a hatch's fill with a two-colour gradient. | Khi cần vẽ thêm đối tượng. |
| `image_attach` | `sheet` | Attach a raster image (PNG/JPG) as an underlay. | Khi cần sheet, khung tên và phát hành. |
| `keyway_draw_keyed_bore` | `engineering` | Draw a bore with a DIN 6885 keyway, auto-sized from the bore diameter. | Khi cần kiểm tra kỹ thuật. |
| `keyway_draw_section` | `engineering` | Draw the side cross-section of a keyed bore. | Khi cần kiểm tra kỹ thuật. |
| `kho_industries` | `cadtroly` | Liệt kê danh mục ngành với mã máy và tên tiếng Việt để chọn tiêu chuẩn. | Khi cần chức năng mở rộng của cadtroly. |
| `kho_rules_export` | `cadtroly` | Xuất quy tắc ánh xạ của đơn vị (chỉ quy tắc, không bản vẽ) để chia sẻ. | Khi cần chức năng mở rộng của cadtroly. |
| `kho_rules_import` | `cadtroly` | Nhập quy tắc ánh xạ từ nơi khác (ghi đè theo pattern). | Khi cần chức năng mở rộng của cadtroly. |
| `kho_skill_add` | `cadtroly` | Thêm skill do LLM soạn vào kho người dùng; chỉ ghi SKILL.md, không chạy mã. | Khi cần chức năng mở rộng của cadtroly. |
| `kho_skill_toggle` | `cadtroly` | Bật/tắt một skill. | Khi cần chức năng mở rộng của cadtroly. |
| `kho_skills` | `cadtroly` | Skill chuyên ngành trong kho/skill (mỗi thư mục một SKILL.md), bật/tắt. | Khi cần chức năng mở rộng của cadtroly. |
| `kho_standard_add` | `cadtroly` | Thêm tiêu chuẩn/rule JSON vào kho người dùng; không ghi vào bộ mặc định. | Khi cần chức năng mở rộng của cadtroly. |
| `kho_standard_delete` | `cadtroly` | Xóa tiêu chuẩn do người dùng thêm; tiêu chuẩn mặc định không thể xóa. | Khi cần chức năng mở rộng của cadtroly. |
| `kho_standards` | `cadtroly` | Liệt kê tiêu chuẩn/rule theo ngành, phiên bản, nguồn và trạng thái duyệt. | Khi cần chức năng mở rộng của cadtroly. |
| `kho_status` | `cadtroly` | Tình trạng kho tri thức, backend AutoCAD, nguồn AI. | Khi cần chức năng mở rộng của cadtroly. |
| `layer_create` | `layers` | Add a layer with a colour, linetype and lineweight. | Khi cần tạo và quản lý layer. |
| `layer_delete` | `layers` | Remove an empty layer from the drawing. | Khi cần tạo và quản lý layer. |
| `layer_freeze` | `layers` | Freeze a layer so it stops drawing and regenerating. | Khi cần tạo và quản lý layer. |
| `layer_hide` | `layers` | Turn a layer off so its entities stop showing. | Khi cần tạo và quản lý layer. |
| `layer_isolate` | `layers` | Hide every layer except one, to work on it alone. | Khi cần tạo và quản lý layer. |
| `layer_list` | `layers` | List every layer with its colour, linetype and visibility state. | Khi cần tạo và quản lý layer. |
| `layer_lock` | `layers` | Lock a layer so its entities can be seen but not edited. | Khi cần tạo và quản lý layer. |
| `layer_modify` | `layers` | Change an existing layer's colour, linetype or lineweight. | Khi cần tạo và quản lý layer. |
| `layer_set_current` | `layers` | Choose the layer that new geometry lands on. | Khi cần tạo và quản lý layer. |
| `layer_show` | `layers` | Turn a layer that was switched off back on. | Khi cần tạo và quản lý layer. |
| `layer_state_delete` | `environment` | Delete one saved layer state from the drawing. | Khi cần kiểm tra kết nối và cấu hình. |
| `layer_state_list` | `environment` | List the layer states saved in this drawing. | Khi cần kiểm tra kết nối và cấu hình. |
| `layer_state_restore` | `environment` | Restore a saved layer state, all properties or a chosen subset. | Khi cần kiểm tra kết nối và cấu hình. |
| `layer_state_save` | `environment` | Save the layer table (on/frozen/locked/colour/linetype/lineweight/plot + current) under a name, in the file. | Khi cần kiểm tra kết nối và cấu hình. |
| `layer_thaw` | `layers` | Bring a frozen layer back into view. | Khi cần tạo và quản lý layer. |
| `layer_unlock` | `layers` | Unlock a layer so its entities can be edited again. | Khi cần tạo và quản lý layer. |
| `layout_copy` | `layouts` | Duplicate a sheet with its page setup and geometry. | Khi cần layout và viewport. |
| `layout_create` | `layouts` | Add a new paper-space sheet tab to the drawing. | Khi cần layout và viewport. |
| `layout_delete` | `layouts` | Delete a sheet tab and everything drawn on it. | Khi cần layout và viewport. |
| `layout_list` | `layouts` | List the sheet tabs: Model plus every paper-space layout. | Khi cần layout và viewport. |
| `layout_rename` | `layouts` | Rename a sheet tab, keeping its geometry and handles. | Khi cần layout và viewport. |
| `layout_set_current` | `layouts` | Switch to a sheet tab, or back to model space. | Khi cần layout và viewport. |
| `leader_create_mleader` | `entity_creation` | Add a callout: an arrow with a note on the end. | Khi cần vẽ thêm đối tượng. |
| `linetype_list` | `layers` | List the dash patterns currently loaded in the drawing. | Khi cần tạo và quản lý layer. |
| `linetype_load` | `layers` | Load a linetype such as CENTER or HIDDEN, without the FILEDIA dialog trap. | Khi cần tạo và quản lý layer. |
| `mech_dimension_part` | `mechanical` | Dimension a drawn part: ISO 129 dimensions, ISO 286 fits, a hole table. | Khi cần bản vẽ cơ khí. |
| `mech_hole_pattern` | `mechanical` | Draw a linear, grid or polar hole pattern with centre marks on any drawing. | Khi cần bản vẽ cơ khí. |
| `mech_part_draw` | `mechanical` | Draw a machine part from a segment list or an outline plus typed features. | Khi cần bản vẽ cơ khí. |
| `mech_part_from_spec` | `mechanical` | Draw a whole mechanical sheet - several parts and their views - in one transaction. | Khi cần bản vẽ cơ khí. |
| `mech_part_inspect` | `mechanical` | Read the part model back off the drawing: segments, features, views, omissions. | Khi cần bản vẽ cơ khí. |
| `mech_view_add` | `mechanical` | Add another view of a drawn part: side, top, section (full/half/offset) or detail. | Khi cần bản vẽ cơ khí. |
| `mleaderstyle_create` | `styles` | Create a multileader style from the ISO or ANSI preset, on both engines. | Khi cần style và hiển thị. |
| `mleaderstyle_list` | `styles` | List multileader styles: arrow size, landing gap, text style and height. | Khi cần style và hiển thị. |
| `page_setup_apply` | `page_setup` | Set a sheet's paper, orientation, ctb, plot scale and device (PAGESETUP). | Khi cần khổ giấy, tỷ lệ và in ấn. |
| `page_setup_list` | `page_setup` | Read each sheet's page setup: paper, orientation, ctb, scale, device. | Khi cần khổ giấy, tỷ lệ và in ấn. |
| `pdf_to_dwg` | `cadtroly` | Create the final semantic DWG in one MCP call. The PDF is vectorized to a private temporary DXF, opened through the live AutoCAD backend, placed on an A-series layout and saved as DWG. The temporary DXF and its lock files are removed in ``finally`` after the DWG is saved, so callers do not have to manage intermediate artifacts. | Khi cần chức năng mở rộng của cadtroly. |
| `pdf_vectorize` | `cadtroly` | Convert PDF vector artwork to editable DXF entities on semantic layers. Output is separated into technical layers such as ``PDF_COLUMNS``, ``PDF_WALLS``, ``PDF_DOORS``, ``PDF_WINDOWS``, ``PDF_FURNITURE``, ``PDF_SANITARY``, ``PDF_DIMENSIONS``, ``PDF_HATCH``, ``PDF_STRUCTURE``, ``PDF_TEXT``, ``PDF_NOTES``, ``PDF_TITLE`` and ``PDF_FRAME`` so an engineer can isolate, edit, delete or add each group. When available, the original DWG layer names embedded in the PDF are used as the classification source. Outlined PDF text remains geometry by design, so dimensions and symbols are not lost when the source font prevents text extraction. The returned counts are a quick audit before opening the DXF and saving it as DWG. | Khi cần chức năng mở rộng của cadtroly. |
| `pid_equipment_list` | `pid` | Equipment list derived from the P&ID graph (tag, kind, ports, connections); optional CSV. | Khi cần sơ đồ P&ID. |
| `pid_from_spec` | `pid` | Draw a whole P&ID from one declarative spec in one transaction; returns graph + critique. | Khi cần sơ đồ P&ID. |
| `pid_graph` | `pid` | Read the P&ID back as a graph: symbols, lines, junctions, dangling ends, confidence. | Khi cần sơ đồ P&ID. |
| `pid_instrument_index` | `pid` | Instrument index derived from the P&ID graph (tag, function, loop, connections); optional CSV. | Khi cần sơ đồ P&ID. |
| `pid_line_draw` | `pid` | Draw a P&ID line port-to-port: orthogonal route, ISA-5.1 class, line number, markers, arrow. | Khi cần sơ đồ P&ID. |
| `pid_line_list` | `pid` | Line list derived from the P&ID graph (number, class, size, spec, from/to); optional CSV. | Khi cần sơ đồ P&ID. |
| `pid_symbol_insert` | `pid` | Place a P&ID symbol (valve, pump, vessel, instrument bubble, connector) as a tagged block with ports. | Khi cần sơ đồ P&ID. |
| `pid_symbol_list` | `pid` | List the P&ID symbol catalogue: families, variants, ports, parameters. | Khi cần sơ đồ P&ID. |
| `pid_tag_parse` | `pid` | Parse an ISA-5.1 instrument tag or an equipment tag; explains every letter. | Khi cần sơ đồ P&ID. |
| `pipe_takeoff` | `plant` | Pipe takeoff from a P&ID and its layout: rows by room, service and diameter. | Khi cần bố trí thiết bị plant. |
| `plot_style_list` | `page_setup` | List the plot style tables (ctb): the AutoCAD catalogue, plus what is installed. | Khi cần khổ giấy, tỷ lệ và in ấn. |
| `point_from_snap` | `premium` | Get an exact endpoint, midpoint, centre, quadrant or perpendicular foot. | Khi cần chức năng nâng cao. |
| `point_intersection` | `premium` | Find where two lines or circles cross, exactly. | Khi cần chức năng nâng cao. |
| `point_tangent` | `premium` | Find where a line from an outside point touches a circle. | Khi cần chức năng nâng cao. |
| `revision_add` | `sheet` | Append a revision row, with optional revision clouds and triangular tags. | Khi cần sheet, khung tên và phát hành. |
| `section_line` | `mechanical` | Draw an ISO 128-40 cutting-plane line and return the plane the section view uses. | Khi cần bản vẽ cơ khí. |
| `selection_filter` | `entity_query` | Select entities by layer, type, colour, linetype or minimum area. | Khi cần tìm và đọc thuộc tính đối tượng. |
| `selection_get` | `entity_query` | Read what the user already picked in the AutoCAD viewport (COM backend). | Khi cần tìm và đọc thuộc tính đối tượng. |
| `selection_polygon` | `entity_query` | Select entities inside or crossing an arbitrary polygon. | Khi cần tìm và đọc thuộc tính đối tượng. |
| `selection_window` | `entity_query` | Select entities inside or crossing a rectangle. | Khi cần tìm và đọc thuộc tính đối tượng. |
| `sheet_frame` | `sheet` | Draw an ISO 5457 sheet frame with the zone grid and centring marks. | Khi cần sheet, khung tên và phát hành. |
| `solid_boolean` | `solids` | Union, subtract or intersect two 3D solids; the tool solid is consumed. | Khi cần hình học 3D/solid. |
| `solid_box` | `solids` | Create a 3D solid box (live AutoCAD, opt-in via ENABLE_3D). | Khi cần hình học 3D/solid. |
| `solid_cylinder` | `solids` | Create a 3D solid cylinder or shaft (live AutoCAD, opt-in via ENABLE_3D). | Khi cần hình học 3D/solid. |
| `solid_extrude` | `solids` | Pull a closed profile up into a 3D solid (live AutoCAD, opt-in via ENABLE_3D). | Khi cần hình học 3D/solid. |
| `solid_revolve` | `solids` | Spin a closed profile around an axis into a 3D solid (opt-in via ENABLE_3D). | Khi cần hình học 3D/solid. |
| `standards_reference` | `cadtroly` | Read the built-in project reference catalogue. These entries guide layer naming and drafting setup; they do not certify regulatory compliance. Confirm the approved edition in the project standards register before issuing construction documents. | Khi cần chức năng mở rộng của cadtroly. |
| `std_feature_draw` | `mechanical` | Draw a standard feature - thread, undercut, ring or O-ring groove, centre hole - onto existing geometry. | Khi cần bản vẽ cơ khí. |
| `std_part_insert` | `mechanical` | Insert an ISO standard part - hex bolt, nut, washer, cap screw or ball bearing - as a tagged block. | Khi cần bản vẽ cơ khí. |
| `std_part_list` | `mechanical` | Search the standard-parts catalogue: ISO bolts, nuts, washers, cap screws, bearings. | Khi cần bản vẽ cơ khí. |
| `structural_qa` | `cadtroly` | Check structural CAD quality and return error/warning findings. This is a drawing/layer/geometry check, not a strength or safety certification. Loads, materials, restraints and approved calculations are required for engineering conclusions. | Khi cần chức năng mở rộng của cadtroly. |
| `surface_texture` | `mechanical` | Draw an ISO 21920-1 surface-texture symbol: Ra/Rz, process, lay, allowance. | Khi cần bản vẽ cơ khí. |
| `system_about` | `system` | See what this server can do: version, tool groups and active profile. | Khi cần trạng thái server. |
| `system_capabilities` | `entity_query` | Ask the active backend which features it really supports. | Khi cần tìm và đọc thuộc tính đối tượng. |
| `system_get_variable` | `system` | Read one AutoCAD system variable, such as DIMSCALE or LTSCALE. | Khi cần trạng thái server. |
| `system_launch` | `environment` | Attach to the running AutoCAD or start it, optionally opening a file (live only). | Khi cần kiểm tra kết nối và cấu hình. |
| `system_preferences_get` | `environment` | Read AutoCAD preferences from the whitelist (OPTIONS dialog values; live only). | Khi cần kiểm tra kết nối và cấu hình. |
| `system_preferences_set` | `environment` | Change one whitelisted AutoCAD preference; reports old and new (live only). | Khi cần kiểm tra kết nối và cấu hình. |
| `system_prompt_message` | `environment` | Print a message on AutoCAD's command line (live only). | Khi cần kiểm tra kết nối và cấu hình. |
| `system_run_command` | `system` | Send a raw command string to the AutoCAD command line (COM only). | Khi cần trạng thái server. |
| `system_run_lisp` | `system` | Evaluate an AutoLISP expression inside AutoCAD (COM only). | Khi cần trạng thái server. |
| `system_set_variable` | `system` | Set one AutoCAD system variable by name. | Khi cần trạng thái server. |
| `system_status` | `system` | Check the connection: which engine is live and what document is open. | Khi cần trạng thái server. |
| `system_variable_describe` | `environment` | Explain a system variable: type, range, default, where it is saved, which engine honours it. | Khi cần kiểm tra kết nối và cấu hình. |
| `takeoff_compute` | `cadtroly` | Bước 3 luồng A: tính khối lượng. Mỗi dòng có nguồn truy vết và tin cậy; thiếu dữ liệu thì để trống. | Khi cần chức năng mở rộng của cadtroly. |
| `takeoff_decide` | `cadtroly` | Kỹ sư xác nhận ánh xạ một nhóm. Mặc định lưu thành quy tắc đơn vị (không train, chỉ ghi file). | Khi cần chức năng mở rộng của cadtroly. |
| `takeoff_export` | `cadtroly` | Bước 4 luồng A: xuất Excel 4 sheet (Khối lượng, Chi tiết từng handle + lệnh zoom, Ánh xạ, Kiểm soát). | Khi cần chức năng mở rộng của cadtroly. |
| `takeoff_propose` | `cadtroly` | Bước 2 luồng A: gom theo layer/block, đề xuất công tác với tin cậy A/B/C. B/C cần kỹ sư quyết. | Khi cần chức năng mở rộng của cadtroly. |
| `takeoff_run` | `cadtroly` | Chạy trọn luồng A không hỏi (dùng quy tắc đã có). Thư mục → mỗi file một Excel. Nhóm B/C vẫn ghi rõ trong Excel. | Khi cần chức năng mở rộng của cadtroly. |
| `template_apply_layers` | `templates` | Create a standard layer set: architectural, mechanical, electrical or piping. | Khi cần template bản vẽ. |
| `template_list` | `templates` | Show the available layer templates and the layers in each. | Khi cần template bản vẽ. |
| `text_find_replace` | `entity_modification` | Find and replace text across the drawing. | Khi cần sửa hoặc biến đổi đối tượng. |
| `text_set_background` | `entity_modification` | Put an opaque background box behind an MTEXT. | Khi cần sửa hoặc biến đổi đối tượng. |
| `textstyle_create` | `styles` | Create a text style from a bundled font (isocp, isocpeur, arial, romans) or any file. | Khi cần style và hiển thị. |
| `textstyle_list` | `styles` | List text styles: font file, height, width factor, oblique angle. | Khi cần style và hiển thị. |
| `textstyle_set_current` | `styles` | Make a text style current so new text uses it. | Khi cần style và hiển thị. |
| `titleblock_apply` | `sheet` | Stamp an ISO 7200 title block (and frame) on any sheet from A4 to A0. | Khi cần sheet, khung tên và phát hành. |
| `titleblock_apply_iso_a3` | `engineering` | Stamp an ISO 7200 title block and sheet frame onto an A3 drawing. | Khi cần kiểm tra kỹ thuật. |
| `transaction_begin` | `transactions` | Open a rollback checkpoint before a risky edit. | Khi cần giao dịch thay đổi có kiểm soát. |
| `transaction_commit` | `transactions` | Keep the changes and drop the checkpoint. | Khi cần giao dịch thay đổi có kiểm soát. |
| `transaction_rollback` | `transactions` | Throw away every change made since transaction_begin. | Khi cần giao dịch thay đổi có kiểm soát. |
| `ucs_list` | `environment` | List the user coordinate systems, with the implicit world one. | Khi cần kiểm tra kết nối và cấu hình. |
| `ucs_restore` | `environment` | Make a saved UCS current, or `world` to reset to WCS. | Khi cần kiểm tra kết nối và cấu hình. |
| `ucs_set` | `environment` | Define (or replace) a named UCS from an origin and two perpendicular axes, and make it current. | Khi cần kiểm tra kết nối và cấu hình. |
| `user_pick_point` | `environment` | Ask the operator to pick a point on screen (live only; blocks until they do). | Khi cần kiểm tra kết nối và cấu hình. |
| `user_select` | `environment` | Ask the operator to select one entity or a set on screen (live only). | Khi cần kiểm tra kết nối và cấu hình. |
| `validation_check` | `validation` | Sanity-check the drawing for empty layers, zero-length lines and duplicates. | Khi cần kiểm tra hợp lệ. |
| `view_named_list` | `environment` | List the named views saved in this drawing. | Khi cần kiểm tra kết nối và cấu hình. |
| `view_named_restore` | `environment` | Restore a named view. | Khi cần kiểm tra kết nối và cấu hình. |
| `view_named_save` | `environment` | Save a named view: a centre and height (and width) to come back to. | Khi cần kiểm tra kết nối và cấu hình. |
| `view_render_report` | `cadtroly` | Return render coverage before relying on a preview for QA. The report is deliberately conservative: common 2D entities are marked as covered, while uncommon/proxy/3D types are surfaced for manual checking. It never claims that a PNG proves the full DWG was rendered. | Khi cần chức năng mở rộng của cadtroly. |
| `view_screenshot` | `view` | Capture a PNG picture of the drawing as it currently looks. | Khi cần zoom, góc nhìn và ảnh chụp. |
| `view_zoom_and_screenshot` | `view` | Fit the drawing on screen, then capture it: the quickest visual check. | Khi cần zoom, góc nhìn và ảnh chụp. |
| `view_zoom_extents` | `view` | Zoom out until every entity fits on screen. | Khi cần zoom, góc nhìn và ảnh chụp. |
| `view_zoom_window` | `view` | Zoom in on a rectangular region of the drawing. | Khi cần zoom, góc nhìn và ảnh chụp. |
| `viewport_create` | `layouts` | Put a scaled window onto model space on a sheet, at 1:1, 1:2 and so on. | Khi cần layout và viewport. |
| `viewport_delete` | `layouts` | Remove a viewport from a sheet. | Khi cần layout và viewport. |
| `viewport_list` | `layouts` | List the viewports on a sheet with their scales and locks. | Khi cần layout và viewport. |
| `viewport_lock` | `layouts` | Lock a viewport so its scale cannot be zoomed away. | Khi cần layout và viewport. |
| `viewport_set_scale` | `layouts` | Set a viewport's scale, e.g. 1:2 or 1:50. | Khi cần layout và viewport. |
| `weld_symbol` | `mechanical` | Draw an ISO 2553 weld symbol: reference line, identification line, size and pitch. | Khi cần bản vẽ cơ khí. |
| `xref_attach` | `sheet` | Attach a DWG/DXF as an external reference (attachment or overlay). | Khi cần sheet, khung tên và phát hành. |
| `xref_manage` | `sheet` | List, reload, bind, detach or repath an external reference. | Khi cần sheet, khung tên và phát hành. |

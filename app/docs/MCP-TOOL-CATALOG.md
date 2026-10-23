# Catalog MCP của project cadtroly

Đây là số liệu của project hiện tại, không phải chỉ catalog upstream U-C4N.
Số liệu được kiểm tra từ registry của `app/server.py` với cấu hình:

```text
TOOL_PROFILE=full
TOOL_PACKS=all
```

## Tổng số runtime

| Thành phần | Số lượng | Ý nghĩa |
|---|---:|---|
| Tool đã đăng ký | **285** | 275 tool chính và 10 alias tương thích cũ |
| Tool đang bật | **280** | Tool client có thể gọi ở `full/all` |
| Tool bị ẩn/giới hạn | **5** | Cần điều kiện 3D hoặc capability tương ứng |
| Resource | **9** | 8 upstream + resource skill của cadtroly |
| Prompt template | **5** | Prompt dựng sơ đồ/mặt bằng/cơ khí/P&ID |

## 247 tool upstream

247 tool nền của U-C4N được chia thành 28 nhóm. File
[`tool-inventory.json`](tool-inventory.json) chứa đầy đủ tên, mô tả, tag, cost
và tham số của 247 tool này.

Để xem hướng dẫn thực hành cho **từng tool** (làm gì, dùng khi nào, tham số,
ví dụ JSON và lưu ý an toàn), mở
[`MCP-TOOL-USAGE.md`](MCP-TOOL-USAGE.md). Đây là tài liệu sinh từ registry
đang chạy và bao gồm cả tool mở rộng của cadtroly.

| Nhóm | Số tool |
|---|---:|
| analysis | 12 |
| architecture | 12 |
| batch | 3 |
| blocks | 9 |
| corner_ops | 4 |
| dimensions | 5 |
| drawing | 11 |
| engineering | 10 |
| entity_creation | 18 |
| entity_modification | 16 |
| entity_query | 9 |
| environment | 22 |
| layers | 14 |
| layouts | 12 |
| mechanical | 14 |
| page_setup | 6 |
| pid | 9 |
| plant | 2 |
| premium | 12 |
| sheet | 11 |
| solids | 5 |
| styles | 10 |
| system | 7 |
| templates | 2 |
| transactions | 3 |
| understanding | 4 |
| validation | 1 |
| view | 4 |
| **Tổng upstream** | **247** |

## 6 tool mở rộng trong `server.py`

Các tool này không nằm trong inventory 247 upstream:

Mười alias cũ `kho_*` vẫn được đăng ký để tương thích với client hiện hữu;
tên chuẩn mới tương ứng là `knowledge_*`. Vì vậy runtime có 10 tên gọi bổ sung,
nhưng không có thêm logic xử lý.

1. `pdf_to_dwg` — chuyển PDF bản vẽ thành DWG/DXF có phân lớp.
2. `pdf_vectorize` — bóc vector, text và dimension từ PDF.
3. `drawing_apply_discipline_standard` — áp dụng chuẩn layer theo bộ môn.
4. `standards_reference` — tra cứu chuẩn CAD xây dựng, đường và cầu.
5. `structural_qa` — kiểm tra layer/hình học kết cấu và trả error/warning.
6. `view_render_report` — báo cáo loại đối tượng có thể thiếu trong preview.

## 22 tool logic riêng của cadtroly

### Đọc và bóc khối lượng

`drawing_read`, `drawing_entities`, `takeoff_propose`, `takeoff_decide`,
`takeoff_compute`, `takeoff_export`, `takeoff_run`.

### Cầu đường

`takeoff_earthwork` (đào đắp từ trắc ngang), `takeoff_rebar` (thống kê thép từ ghi chú).

### Duyệt thao tác phá huỷ

`approval_execute` — chạy thao tác đã được người dùng đồng ý (xem `docs/3-cau-hinh.md`, mục duyệt).

### Kiểm tra và quản lý tiêu chuẩn

`check_rulesets`, `check_run`, `knowledge_industries`, `knowledge_standards`,
`knowledge_standard_add`, `knowledge_standard_delete`.

### Kho skill và trạng thái

`knowledge_status`, `knowledge_rules_export`, `knowledge_rules_import`, `knowledge_skills`,
`knowledge_skill_toggle`, `knowledge_skill_add`.

## 9 resources

### 8 resource upstream

1. `autocad://blocks`
2. `autocad://drawing/info`
3. `autocad://entities/stats`
4. `autocad://entities/{layer_name}`
5. `autocad://layers`
6. `autocad://pid/symbols`
7. `autocad://standards/isa51`
8. `autocad://system/status`

### Resource riêng cadtroly

9. `cadtroly://skill/{name}` — đọc nội dung `SKILL.md` theo tên skill.

## 5 prompt templates

1. `prompt_electrical_schematic` — tạo sơ đồ điện.
2. `prompt_floor_plan` — tạo mặt bằng kiến trúc.
3. `prompt_mechanical_drawing` — tạo bản vẽ cơ khí.
4. `prompt_pid_diagram` — tạo P&ID.
5. `prompt_quick_drawing` — tạo hướng dẫn vẽ từ mô tả.

## Kiểm tra trên máy

Yêu cầu LLM:

```text
Cho biết số tool đã đăng ký, số tool đang bật, resources và prompt templates
của project cadtroly hiện tại.
```

Hoặc gọi `system_about`/`tools/list`. `tool-inventory.json` là inventory
upstream 247; runtime của project mới là số liệu cuối cùng khi có tool mở rộng,
profile, pack hoặc capability phần cứng khác nhau.

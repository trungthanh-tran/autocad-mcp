# Danh mục MCP

## Phạm vi upstream U-C4N

Bản v1.6 upstream có **247 tools · 8 resources · 5 prompt templates** trong
**28 nhóm**. Danh sách tên đầy đủ, mô tả, tag, cost và tham số được lưu trong
[`tool-inventory.json`](tool-inventory.json), là file sinh tự động từ registry.

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
| **Tổng cộng** | **247** |

## 8 resources

1. `autocad://blocks`
2. `autocad://drawing/info`
3. `autocad://entities/stats`
4. `autocad://entities/{layer_name}`
5. `autocad://layers`
6. `autocad://pid/symbols`
7. `autocad://standards/isa51`
8. `autocad://system/status`

## 5 prompt templates

1. `prompt_electrical_schematic` — tạo sơ đồ điện.
2. `prompt_floor_plan` — tạo mặt bằng kiến trúc.
3. `prompt_mechanical_drawing` — tạo bản vẽ cơ khí.
4. `prompt_pid_diagram` — tạo P&ID.
5. `prompt_quick_drawing` — tạo hướng dẫn vẽ từ mô tả.

## Phần mở rộng cadtroly

Ngoài 247 tool upstream, cadtroly có các tool riêng cho kho tiêu chuẩn, skill,
bóc khối lượng, PDF→DWG và QA tiếng Việt. Vì vậy số tool MCP thực tế khi chạy
`TOOL_PROFILE=full`, `TOOL_PACKS=all` lớn hơn con số upstream; hãy gọi
`system_about` hoặc `tools/list` để lấy số lượng runtime chính xác.

Không dùng con số 247 để mô tả riêng phần mở rộng cadtroly. 247 là mốc catalog
upstream; `tool-inventory.json` là nguồn kiểm tra tên và nhóm, còn runtime là
nguồn kiểm tra tool đang bật trên máy.

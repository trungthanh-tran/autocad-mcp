# MCP tool usage guide

Tài liệu này mô tả **từng tool đang đăng ký trong project cadtroly**: tool làm gì, dùng khi nào, tham số, ví dụ và lưu ý an toàn. File được sinh từ registry FastMCP hiện tại; không sửa thủ công.

## Tổng quan

- Registered tools: **272**
- Enabled với `TOOL_PROFILE=full`, `TOOL_PACKS=all`: **267**
- Hidden/giới hạn backend: **5**
- Resources: **9**; prompt templates: **5**
- Tool upstream trong `tool-inventory.json`: **247**; phần còn lại là extension của project.

## Cách gọi chung

LLM gọi đúng tên tool và truyền một JSON object theo bảng tham số:

```json
{
  "name": "tool_name",
  "arguments": {}
}
```

Đối với tool làm thay đổi bản vẽ, nên đọc/chụp trạng thái trước, chạy tool, sau đó kiểm tra lại và lưu ra file đích. Với PDF, dùng `pdf_to_dwg` để tạo DWG semantic và tự dọn file trung gian.

## Chi tiết từng tool

### `analysis_bounding_box`

**Nhóm:** `analysis`  
**Làm gì:** Get the bounding box (extents) of all entities in the drawing.

**Dùng khi nào:** Khi cần đọc, đo, thống kê hoặc phân tích bản vẽ mà không sửa dữ liệu.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `analysis_entity_stats`

**Nhóm:** `analysis`  
**Làm gì:** Analyze the drawing and return entity counts grouped by type and by layer.

Returns: total_entities, by_type (sorted by count), by_layer (sorted by count).
This is unique to AutoCAD MCP Pro – no other MCP server provides this!

**Dùng khi nào:** Khi cần đọc, đo, thống kê hoặc phân tích bản vẽ mà không sửa dữ liệu.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `analysis_find_in_region`

**Nhóm:** `analysis`  
**Làm gì:** Find all entities within a rectangular region (crossing selection).

Uncapped: a window over a busy drawing returns every hit. Project with
`fields` and/or `compact` before widening the window.

**Dùng khi nào:** Khi cần đọc, đo, thống kê hoặc phân tích bản vẽ mà không sửa dữ liệu.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `x1` | `number` | có | `—` | Region minimum X |
| `y1` | `number` | có | `—` | Region minimum Y |
| `x2` | `number` | có | `—` | Region maximum X |
| `y2` | `number` | có | `—` | Region maximum Y |
| `fields` | `any` | không | `None` | Project to these fields, in this order (e.g. ['handle','type','layer']); 'properties.<key>' reaches one nested value. Omit for the full record; an unknown name errors and lists the valid ones. |
| `compact` | `boolean` | không | `False` | Return a columnar {fields, rows, count, offset, total, truncated, next_offset} envelope instead of dicts: much cheaper per row, and the only shape that reports truncation. |

**Ví dụ gọi**

```json
{
  "x1": 1.0,
  "y1": 1.0,
  "x2": 1.0,
  "y2": 1.0,
  "fields": null,
  "compact": false
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `analysis_layer_stats`

**Nhóm:** `analysis`  
**Làm gì:** Return detailed statistics for each layer: entity count, types present.

**Dùng khi nào:** Khi cần đọc, đo, thống kê hoặc phân tích bản vẽ mà không sửa dữ liệu.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `analysis_list_properties`

**Nhóm:** `analysis`  
**Làm gì:** AutoCAD's LIST: the full DXF attribute set for one handle.

`dxf_attributes` is the raw attribute set `entity_get` deliberately does
not carry. Coordinates in it are WCS, like everywhere else in this server,
and `extrusion` is reported so the entity's own frame is still visible.

**Dùng khi nào:** Khi cần đọc, đo, thống kê hoặc phân tích bản vẽ mà không sửa dữ liệu.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Handle of the entity to dump. |

**Ví dụ gọi**

```json
{
  "handle": "A1B2"
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `analysis_measure_area`

**Nhóm:** `analysis`  
**Làm gì:** Area and perimeter of a polygon you supply the vertices for.

This measures the numbers in the call, NOT the drawing. To measure something
that exists, use `analysis_measure_entity(handle)` — it reads the real
geometry, including curvature this tool can only see if you pass it.

Straight-edged polygons are exact. Pass a third `bulge` element per vertex
for arc edges; omitting it on curved geometry under-reports (28% on a
semicircular edge), which is why `assumes` says what was taken on faith.

**Dùng khi nào:** Khi cần đọc, đo, thống kê hoặc phân tích bản vẽ mà không sửa dữ liệu.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `points` | `array<array>` | có | `—` | Polygon vertices, min 3. Each is [x, y] or [x, y, bulge] — the bulge (DXF convention) makes the edge leaving that vertex a circular arc. |

**Ví dụ gọi**

```json
{
  "points": []
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `analysis_measure_distance`

**Nhóm:** `analysis`  
**Làm gì:** Measure the Euclidean distance between two points.

**Dùng khi nào:** Khi cần đọc, đo, thống kê hoặc phân tích bản vẽ mà không sửa dữ liệu.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `x1` | `number` | có | `—` | Point 1 X |
| `y1` | `number` | có | `—` | Point 1 Y |
| `x2` | `number` | có | `—` | Point 2 X |
| `y2` | `number` | có | `—` | Point 2 Y |

**Ví dụ gọi**

```json
{
  "x1": 1.0,
  "y1": 1.0,
  "x2": 1.0,
  "y2": 1.0
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `analysis_measure_entity`

**Nhóm:** `analysis`  
**Làm gì:** Measure something already in the drawing, by handle.

Reads the real geometry, so polyline bulges (arc edges) are included —
reading vertices back and shoelacing them yourself loses 28% of the area on
a semicircular edge, silently.

Measurable: LWPOLYLINE, 2D POLYLINE, CIRCLE, ELLIPSE, SPLINE, HATCH, SOLID,
TRACE, 3DFACE. REGION and 3DSOLID need the live COM backend (their area is
in ACIS data ezdxf cannot evaluate) and refuse with
`capability: "measure_area_acis"`. LINE/TEXT/INSERT bound no area on any
engine and are a plain error, not a capability gap.

The payload states its own accuracy: `exact` is false when the shape had to
be flattened (then `flatten_tolerance` says how finely), `assumed_closed` is
true when an open boundary was closed the way AutoCAD's AREA does, and
`self_intersecting` warns when the shoelace cancelled crossed lobes — a
bowtie measures 0.0 and that number is worse than useless unflagged.

**Dùng khi nào:** Khi cần đọc, đo, thống kê hoặc phân tích bản vẽ mà không sửa dữ liệu.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Entity handle (hex string) from create/list/select |
| `flatten_tolerance` | `number` | không | `0.001` | Max chord deviation when geometry has no closed form (splines, partial ellipses) |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "flatten_tolerance": 0.001
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `analysis_select_by_layer`

**Nhóm:** `analysis`  
**Làm gì:** Get all entities on a specific layer. Returns entity list with handles.

Capped at MAX_LIST_LIMIT (default 5000). The plain list cannot say it was
capped — the warning goes to the log stream, which most clients never show
the model — so use `compact=True` when the count matters: its `total` is the
layer's real population and `truncated` states whether the cap fired.

**Dùng khi nào:** Khi cần đọc, đo, thống kê hoặc phân tích bản vẽ mà không sửa dữ liệu.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `layer_name` | `string` | có | `—` | Layer name to select entities from |
| `fields` | `any` | không | `None` | Project to these fields, in this order (e.g. ['handle','type','layer']); 'properties.<key>' reaches one nested value. Omit for the full record; an unknown name errors and lists the valid ones. |
| `compact` | `boolean` | không | `False` | Return a columnar {fields, rows, count, offset, total, truncated, next_offset} envelope instead of dicts: much cheaper per row, and the only shape that reports truncation. |

**Ví dụ gọi**

```json
{
  "layer_name": "example",
  "fields": null,
  "compact": false
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `analysis_select_by_type`

**Nhóm:** `analysis`  
**Làm gì:** Get all entities of a specific type. Returns entity list with handles.

Capped at MAX_LIST_LIMIT (default 5000); as with analysis_select_by_layer,
`compact=True` is the only shape that reports `total` and `truncated`.

**Dùng khi nào:** Khi cần đọc, đo, thống kê hoặc phân tích bản vẽ mà không sửa dữ liệu.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `entity_type` | `string` | có | `—` | Entity type: LINE, CIRCLE, ARC, LWPOLYLINE, TEXT, MTEXT, INSERT, HATCH, SPLINE, ELLIPSE |
| `fields` | `any` | không | `None` | Project to these fields, in this order (e.g. ['handle','type','layer']); 'properties.<key>' reaches one nested value. Omit for the full record; an unknown name errors and lists the valid ones. |
| `compact` | `boolean` | không | `False` | Return a columnar {fields, rows, count, offset, total, truncated, next_offset} envelope instead of dicts: much cheaper per row, and the only shape that reports truncation. |

**Ví dụ gọi**

```json
{
  "entity_type": "example",
  "fields": null,
  "compact": false
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `arch_catalogue_insert`

**Nhóm:** `architecture`  
**Làm gì:** Define the item's block ARCH_<NAME> once, insert it on the furniture or sanitary layer.

The block carries an invisible ITEM attribute with the catalogue name. Its
size is a nominal catalogue dimension (reported with `size_basis`), not a
standards value; the outline is a plan symbol drawn inside that footprint.
The furniture / sanitary layer is created from the `arch` layer set when
the drawing lacks it. Refusals, all before any write: an unknown name
(with the nearest catalogue names) and a non-finite coordinate or rotation.

**Dùng khi nào:** Khi làm mặt bằng, mặt đứng, mặt cắt và các thành phần kiến trúc.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Catalogue name from arch_catalogue_list, e.g. 'double_bed', 'sofa_3_seat', 'wc', 'wall_basin', 'kitchen_counter' |
| `x` | `number` | có | `—` | X (WCS) of the item's back-left corner |
| `y` | `number` | có | `—` | Y (WCS) of the item's back-left corner |
| `rotation` | `number` | không | `0.0` | Degrees CCW about (x, y); 0 puts the item's back (its wall side) along +X with the item extending towards +Y |

**Ví dụ gọi**

```json
{
  "name": "example",
  "x": 1.0,
  "y": 1.0,
  "rotation": 0.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `arch_catalogue_list`

**Nhóm:** `architecture`  
**Làm gì:** Catalogue rows: name, family, both labels, nominal size [w, d] in mm, block name, layer.

Sizes are nominal catalogue dimensions - what a furniture or appliance
catalogue lists as a common size - and every row says so in `size_basis`;
they are not standards values. Twenty items: thirteen furniture, seven
sanitary. Refusals: a `family` other than furniture/sanitary and a `lang`
other than en/tr, each with the list.

**Dùng khi nào:** Khi làm mặt bằng, mặt đứng, mặt cắt và các thành phần kiến trúc.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `query` | `any` | không | `None` | Words matched against the item name, family and its English or Turkish label, ignoring case and Turkish diacritics - 'bed', 'yatak', 'klozet', 'buzdolabi'. Every word must match. |
| `family` | `any` | không | `None` | furniture | sanitary |
| `lang` | `string` | không | `en` | en | tr - the language of the 'label' column |

**Ví dụ gọi**

```json
{
  "query": null,
  "family": null,
  "lang": "en"
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `arch_dimension_chains`

**Nhóm:** `architecture`  
**Làm gì:** The three exterior chains an architectural plan carries, as real DIMENSIONs.

Nearest first: the openings row (every jamb in that facade), the walls row
(both faces of every wall meeting it - wall thickness, clear width, wall
thickness, ...) and the overall row. The points come from the wall engine's
own faces, read back from the plan on the drawing. A row that would only
restate a farther one is not drawn (ISO 129-1: each measurement once).
The row spacing defaults (10 mm, then 8 mm on paper) are this server's
drafting choices, not standard values. Text, arrows and gaps follow the
plot scale: each chain is drawn at DIMSCALE = `scale` (reported as
`dimscale`), and the drawing's own DIMSCALE is put back afterwards.

Refused by name: a drawing with no walls, an unknown or repeated side, a
non-positive scale, offset or step.

**Dùng khi nào:** Khi làm mặt bằng, mặt đứng, mặt cắt và các thành phần kiến trúc.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `sides` | `any` | không | `None` | Sides to dimension: bottom | top | left | right (default bottom, left) |
| `scale` | `number` | không | `50.0` | Plot-scale denominator: rows sit 10 mm and 8 mm apart on paper |
| `first_offset` | `any` | không | `None` | Distance of the first row from the building (drawing units) |
| `step` | `any` | không | `None` | Distance between rows (drawing units) |

**Ví dụ gọi**

```json
{
  "sides": null,
  "scale": 50.0,
  "first_offset": null,
  "step": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `arch_grid`

**Nhóm:** `architecture`  
**Làm gì:** Axis lines on the arch grid layer (its CENTER linetype comes from the layer) and a
5 mm bubble with its label at both ends of each axis, on the symbol layer.

Numbers run along x and letters along y (A..Z, then AA, AB - no letter is
skipped) unless `labels` names them. The bubble and label sizes are this
server's declared drafting sizes in paper millimetres, not a standards value.
Refusals, all before any write: an empty axis list in either direction, a
non-finite or duplicate position, a label list whose length does not match
its positions, a duplicate or empty label, an unknown `labels` key, and a
non-positive `extension` or `scale`.

**Dùng khi nào:** Khi làm mặt bằng, mặt đứng, mặt cắt và các thành phần kiến trúc.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `x_axes` | `array<number>` | có | `—` | X positions (WCS) of the vertical axes; numbered 1, 2, 3 left to right |
| `y_axes` | `array<number>` | có | `—` | Y positions (WCS) of the horizontal axes; lettered A, B, C bottom to top |
| `labels` | `any` | không | `None` | Override the labels: {'x': [...], 'y': [...]} (either key), one label per position in the order the positions were given |
| `extension` | `number` | không | `1500.0` | Drawing units each axis runs past the outermost crossing axis |
| `scale` | `number` | không | `50.0` | Plot-scale denominator (50 = 1:50): bubbles and labels are paper mm x scale |

**Ví dụ gọi**

```json
{
  "x_axes": [],
  "y_axes": [],
  "labels": null,
  "extension": 1500.0,
  "scale": 50.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `arch_opening`

**Nhóm:** `architecture`  
**Làm gì:** A door or a window in a wall already drawn, found by its id; the wall is redrawn cut.

The opening removes its width from both wall faces and each edge is closed
by a jamb. A door is drawn open at 90° - its leaf as long as the opening is
wide, hinged on `hand`, with a quarter-arc swing on the `swing` side; a
window is a frame line on each face and two glazing lines between them. The
opening's `ACADMCP_ARCH` record sits on the leaf or the frame, so a schedule
reads it back.

Refused before anything is drawn or erased: a wall id not on the drawing
(the drawn ids are named), an opening id already drawn, an opening that
runs past its wall segment or straddles an axis vertex, one overlapping
another opening on the same wall (both ids named), one that runs into a
junction (the solid stretch it must fit in is named), an unknown kind,
swing, hand or language.

**Dùng khi nào:** Khi làm mặt bằng, mặt đứng, mặt cắt và các thành phần kiến trúc.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `wall` | `string` | có | `—` | Id of the drawn wall that hosts the opening |
| `offset` | `number` | có | `—` | Distance along the wall's axis from its first point to the near jamb (mm) |
| `width` | `number` | có | `—` | Clear width of the opening (mm) |
| `kind` | `string` | không | `door` | door | window |
| `swing` | `string` | không | `in` | Doors: in = to the left of the axis (inside a CCW perimeter) | out |
| `hand` | `string` | không | `left` | Doors: the hinge jamb, seen from the swing side facing the wall: left | right |
| `sill` | `any` | không | `None` | Windows: sill height (schedule only, mm) |
| `height` | `any` | không | `None` | Opening height (schedule only, mm) |
| `tag` | `any` | không | `None` | Schedule tag; default the next D1/W1 (en) or K1/P1 (tr) |
| `opening_id` | `any` | không | `None` | Opening id; default its tag |
| `lang` | `string` | không | `en` | Tag language: en | tr |
| `poche` | `boolean` | không | `True` | Hatch the redrawn wall's cut faces |

**Ví dụ gọi**

```json
{
  "wall": "example",
  "offset": 1.0,
  "width": 1.0,
  "kind": "door",
  "swing": "in",
  "hand": "left",
  "sill": null,
  "height": null,
  "tag": null,
  "opening_id": null,
  "lang": "en",
  "poche": true
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `arch_plan_from_spec`

**Nhóm:** `architecture`  
**Làm gì:** A whole plan drawn inside one transaction: walls with their hosted doors and
windows, stairs, room labels whose areas are measured off the walls just drawn,
the exterior dimension chains and the door / window / room schedules.

Every item is validated before the transaction opens, so a refusal leaves the
drawing untouched and names its path (`walls[1].thickness: ...`,
`rooms[0].area: ...`). What only the drawing can refuse - a room point in no
closed face - rolls the transaction back, and so does a cancelled request (the
rollback runs under an anyio shield). The result carries each step's own
result, the wall engine's `omitted` list and the three `arch_*` critique
focuses run over the committed plan.

Refused by name: an unknown key, no walls, an unknown language or material, a
non-finite or non-positive number, an arc segment in a wall axis, an opening
that overlaps another or runs past its wall segment (both ids named), a typed
room `area` (areas are measured, never typed), an unknown chain side or
schedule kind, and a transaction that cannot be opened. Catalogue furniture,
the grid and symbols are separate tools (`arch_catalogue_insert`, `arch_grid`,
`arch_symbol`).

**Dùng khi nào:** Khi làm mặt bằng, mặt đứng, mặt cắt và các thành phần kiến trúc.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `spec` | `object` | có | `—` | {sheet: {intent, sheet_size, scale (denominator, 50 = 1:50)}, lang: 'en'|'tr', poche: bool, walls: [{id, axis: [[x,y],...], thickness, justification, material, closed}], openings: [{id, wall, kind: 'door'|'window', offset, width, swing, hand, sill, height, tag}], stairs: [{id, start, direction_deg, width, risers, riser_height, going, kind, turn}], rooms: [{id, name, number, at}], chains: {sides: ['bottom','left']}, schedules: [{kind: 'doors'|'windows'|'rooms', at: [x,y]}]} |

**Ví dụ gọi**

```json
{
  "spec": {}
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `arch_room`

**Nhóm:** `architecture`  
**Làm gì:** Label the room around (x, y) with its name, number and MEASURED area.

The area is never typed: the tool reads the wall faces on the `wall` layer
of the arch set (LINE and lightweight polyline, both engines; anything else
there is listed in `skipped`), finds the closed face
the point lies in and writes that face's area - net of the wall thickness
and of any column inside it - into the label and into an `ACADMCP_ARCH`
room record on the name text, which `arch_schedule` reads. A door or window
recorded on the drawing closes its gap along the wall faces, so two rooms
either side of a door stay two rooms.

Refused before anything is drawn: an unknown `lang` (named with en, tr), a
`number`/`name` the room model refuses, a `room_id` already labelled on the
drawing, a point in no closed face of the walls (draw or close them first,
or read a plan drawn by other means with `arch_rooms_detect`), a point
inside a wall body, and a point in a room that already carries a label (one
face, one room record - a retried call does not add a second area to the
schedule).

**Dùng khi nào:** Khi làm mặt bằng, mặt đứng, mặt cắt và các thành phần kiến trúc.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Room name, e.g. LIVING / SALON. |
| `x` | `number` | có | `—` | WCS X of a point inside the room; the label starts here. |
| `y` | `number` | có | `—` | WCS Y of a point inside the room. |
| `number` | `any` | không | `None` | Room number, e.g. 01; omit for none. |
| `room_id` | `any` | không | `None` | Record id; default is the first free R<n>. |
| `lang` | `string` | không | `en` | Label language: en | tr (tr writes 24,50 m²). |
| `scale` | `number` | không | `50.0` | Plot-scale denominator: 50 is 1:50 (text x 50). |

**Ví dụ gọi**

```json
{
  "name": "example",
  "x": 1.0,
  "y": 1.0,
  "number": null,
  "room_id": null,
  "lang": "en",
  "scale": 50.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `arch_rooms_detect`

**Nhóm:** `architecture`  
**Làm gì:** Read the rooms of a plan - ours or a foreign one made of plain lines.

Every LINE and lightweight polyline on the layers is split where lines
cross or touch, and the closed faces they bound are measured (mm², net of
nested pieces).
Faces under `min_area`, and thin faces (mean width under 600 mm - wall
bodies and reveals, this reader's heuristic) are left out. Each room
reports `confidence`: 1.0 when every edge lies on the arch wall layer, 0.6
when any edge is a plain line from elsewhere - read `confidence_min` before
trusting a foreign plan. Room labels already on the drawing are reported
in `labels` with the face they sit in; a face with more than one is listed
in `label_conflicts`.

Never modifies the drawing. Arcs and bulged polyline edges, old-style
POLYLINEs and block references are listed in `skipped` with their handle
and reason - never flattened into chords, never dropped silently. Read
`skipped` before trusting `count`. A foreign plan's open doorways are
not closed - two rooms joined by one read as one face. Refused: a named
layer the drawing does not have (with the list of the ones it has), and no
layer matching WALL or DUVAR when `layers` is omitted.

**Dùng khi nào:** Khi làm mặt bằng, mặt đứng, mặt cắt và các thành phần kiến trúc.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `layers` | `any` | không | `None` | Layers holding the walls; default: every layer whose name contains WALL or DUVAR. |
| `min_area` | `number` | không | `1000000.0` | Smallest room reported, mm² (1e6 = 1 m²). |
| `tol` | `number` | không | `1.0` | Endpoints closer than this (mm) are one corner. |

**Ví dụ gọi**

```json
{
  "layers": null,
  "min_area": 1000000.0,
  "tol": 1.0
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `arch_schedule`

**Nhóm:** `architecture`  
**Làm gì:** Draw a door, window or room schedule as a real TABLE - a read of the drawing.

The rows come from the `ACADMCP_ARCH` records on the drawing (what
`arch_wall` / `arch_opening` / `arch_room` write), never from the caller:
doors by tag with width, height, swing, hand and wall; windows by tag with
width, height, sill and wall; rooms by number with name and the measured
area, plus a total. An opening drawn without a tag gets the next free D1 /
W1 (K1 / P1 in Turkish) in wall order; an explicit tag is kept. A value the
model does not carry is an empty cell, never a default. `representation`
reports what was drawn: `native` (ACAD_TABLE, live) or `composite` (rules
and MTEXT, headless).

Refused before anything is drawn: an unknown `kind` or `lang` (named with
the list), nothing of that kind on the drawing, and more rows than one
TABLE takes (198).

**Dùng khi nào:** Khi làm mặt bằng, mặt đứng, mặt cắt và các thành phần kiến trúc.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `kind` | `string` | có | `—` | doors | windows | rooms |
| `x` | `number` | có | `—` | WCS X of the table's top-left corner. |
| `y` | `number` | có | `—` | WCS Y of the table's top-left corner. |
| `lang` | `string` | không | `en` | Headers and numbers: en | tr (decimal comma). |
| `scale` | `number` | không | `50.0` | Plot-scale denominator: 50 is 1:50. |

**Ví dụ gọi**

```json
{
  "kind": "example",
  "x": 1.0,
  "y": 1.0,
  "lang": "en",
  "scale": 50.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `arch_stair`

**Nhóm:** `architecture`  
**Làm gì:** A stair in plan: every riser as a line, the outline, the walking line with its arrow.

The label ("UP" / "ÇIKIŞ") sits on the first tread at 2.5 mm × `scale`. The
result reports `blondel` - 2R + G against 600-650 mm, the step-length rule
attributed to François Blondel (1675). It is a design rule reported for the
drafter, not a building code: no national stair regulation is checked and
a value outside the band is reported (`ok: false`), not refused.

Refused before anything is drawn: a stair id already on the drawing, a
non-positive width, riser height or going, fewer than 2 risers (4 for an L
or a U - two per flight), a non-integer riser count, an unknown kind, turn
or language.

**Dùng khi nào:** Khi làm mặt bằng, mặt đứng, mặt cắt và các thành phần kiến trúc.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `stair_id` | `string` | có | `—` | Stair id, unique on the drawing |
| `start_x` | `number` | có | `—` | WCS X of the midpoint of the bottom riser |
| `start_y` | `number` | có | `—` | WCS Y of the midpoint of the bottom riser |
| `width` | `number` | có | `—` | Flight width (mm) |
| `risers` | `integer` | có | `—` | Number of risers from floor to floor |
| `riser_height` | `number` | có | `—` | Riser height R (mm) |
| `going` | `number` | có | `—` | Tread going G (mm) |
| `direction_deg` | `number` | không | `0.0` | Direction up the first flight, degrees CCW from +X |
| `kind` | `string` | không | `straight` | straight | l | u |
| `turn` | `string` | không | `left` | L / U stairs: which way the second flight turns |
| `lang` | `string` | không | `en` | Label language: en | tr |
| `scale` | `number` | không | `50.0` | Plot-scale denominator for the label and arrow (50 = 1:50) |

**Ví dụ gọi**

```json
{
  "stair_id": "example",
  "start_x": 1.0,
  "start_y": 1.0,
  "width": 1.0,
  "risers": 1,
  "riser_height": 1.0,
  "going": 1.0,
  "direction_deg": 0.0,
  "kind": "straight",
  "turn": "left",
  "lang": "en",
  "scale": 50.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `arch_symbol`

**Nhóm:** `architecture`  
**Làm gì:** Draw one architectural symbol on the arch symbol layer.

Sizes are this server's declared drafting sizes in paper millimetres times
`scale` (a 16 mm north-arrow circle, 10 mm section and elevation bubbles),
not standards values. Refusals, all before any write: an unknown `kind`
(with the list), a parameter the kind does not take (with the ones it
does), a section mark without p1/p2, with an empty label, an unknown side
or a cut line too short for its two arrows, an elevation direction outside
up/right/down/left or named twice, a non-finite level value, and a `lang`
other than en/tr.

**Dùng khi nào:** Khi làm mặt bằng, mặt đứng, mặt cắt và các thành phần kiến trúc.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `kind` | `string` | có | `—` | north_arrow | section_mark | level | elevation_mark |
| `x` | `number` | có | `—` | Symbol origin X (WCS) |
| `y` | `number` | có | `—` | Symbol origin Y (WCS) |
| `params` | `any` | không | `None` | north_arrow: {rotation} (degrees CCW from +Y; 0 = north up). section_mark: {p1, p2, label, side} - p1/p2 are [x, y] relative to (x, y), side left|right is where the section looks, seen from p1 towards p2. level: {value} in metres (0 -> '±0.00'). elevation_mark: {label, directions} - directions from up|right|down|left |
| `lang` | `string` | không | `en` | en | tr - the north letter and the decimal separator |
| `scale` | `number` | không | `50.0` | Plot-scale denominator (50 = 1:50): symbol sizes are paper mm x scale |

**Ví dụ gọi**

```json
{
  "kind": "example",
  "x": 1.0,
  "y": 1.0,
  "params": null,
  "lang": "en",
  "scale": 50.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `arch_wall`

**Nhóm:** `architecture`  
**Làm gì:** Add walls to the plan network already on the drawing and resolve every junction.

Two ends at one point mitre into a clean L; an end inside another wall is a
T (the stem stops on the crossing wall's near face, which is cut there); two
axes crossing are an X (all four faces cut). A drawn wall whose outline the
new walls change is taken back out and redrawn with its openings - the
result lists it under `redrawn` - and a wall they do not touch is left alone.
Every wall carries an `ACADMCP_ARCH` record, so later calls find it by id.

Refused before anything is drawn or erased, by path: a wall id already on
the drawing or used twice, an axis of fewer than two points or with a
zero-length segment, a non-positive thickness, an unknown justification or
material (the list is named), two walls meeting at less than 5° (the mitre
would run away), a wall corner lying inside another wall off its axis, an
end inside a wall whose axis only meets it past that wall's end, and a new
wall that would leave a drawn opening uncuttable. A curved wall is not
supported: an axis is straight segments only.

**Dùng khi nào:** Khi làm mặt bằng, mặt đứng, mặt cắt và các thành phần kiến trúc.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `walls` | `array<object>` | có | `—` | Walls to add: [{id, axis:[[x,y],...] (2+ points, straight segments, WCS mm), thickness, justification:'center'|'left'|'right' (side of the axis looking along it), material:'brick'|'aac'|'concrete'|'reinforced_concrete'|'gypsum_board'|'stone'|'timber'|'generic', closed:bool}] |
| `poche` | `boolean` | không | `True` | Hatch the cut wall faces in their material (ISO 128-50) |

**Ví dụ gọi**

```json
{
  "walls": [],
  "poche": true
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `balloon_add`

**Nhóm:** `sheet`  
**Làm gì:** One ISO 6433 item reference: a numbered balloon, a leader, and a dot on
the item.

The balloon carries an ACADMCP_MECH payload naming its targets, so running
the balloon pass again after the bill of materials is regrouped *renumbers*
the existing balloon (`renumbered: true`) instead of drawing a second one.
Refusals, all before the first entity: an item number below 1, a leader
target inside the balloon, and an item number already used by another
balloon for different targets — named with that balloon's handle.

**Dùng khi nào:** Khi tạo và quản lý sheet, title block và hồ sơ phát hành.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `item` | `integer` | có | `—` | Item reference number, as bom_extract numbers it. |
| `x` | `number` | có | `—` | Balloon centre X (WCS). |
| `y` | `number` | có | `—` | Balloon centre Y (WCS). |
| `leader_x` | `number` | có | `—` | X of the dot on the item. |
| `leader_y` | `number` | có | `—` | Y of the dot on the item. |
| `targets` | `any` | không | `None` | Handles of the INSERTs this item is; the link a rerun renumbers by. |
| `radius` | `number` | không | `4.0` | Balloon radius (mm). The numeral is 1.4x this, so a sheet dimensioned at 3.5 mm wants 5.0 to satisfy ISO 6433. |
| `layer` | `string` | không | `DIM` | — |
| `layout` | `string` | không | `` | — |

**Ví dụ gọi**

```json
{
  "item": 1,
  "x": 1.0,
  "y": 1.0,
  "leader_x": 1.0,
  "leader_y": 1.0,
  "targets": null,
  "radius": 4.0,
  "layer": "DIM",
  "layout": ""
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `batch_plot`

**Nhóm:** `page_setup`  
**Làm gì:** AutoCAD's PUBLISH for a PDF set, through `drawing_export_pdf(layout=…)`.

One row per sheet: `path`, `bytes`, and `mediabox_mm` **parsed from the
PDF that was written** (`/MediaBox`, points → mm), with `paper` naming the
catalogue size it matches within 0.5 mm — so the sheet size is verified,
never assumed. Model space is included only when named.

Refused before any file is written: a format other than pdf, an empty
`layouts` list, a layout that does not exist, a `file_pattern` containing a
path separator or lacking `{layout}` when more than one sheet is plotted,
and any output path outside the allowed directories. A sheet whose PDF has
no readable MediaBox is reported with `mediabox_mm: null` and an `error`.

**Dùng khi nào:** Khi thiết lập khổ giấy, máy in, tỷ lệ và cấu hình xuất bản.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `output_dir` | `string` | có | `—` | Folder for the PDFs (created if missing). |
| `layouts` | `any` | không | `None` | Layouts to plot; omit for every paper-space layout. 'Model' only when named. |
| `format` | `string` | không | `pdf` | pdf (the only format this release plots). |
| `file_pattern` | `string` | không | `{drawing}-{layout}.pdf` | File name per sheet; {drawing} and {layout} are substituted. |

**Ví dụ gọi**

```json
{
  "output_dir": "example",
  "layouts": null,
  "format": "pdf",
  "file_pattern": "{drawing}-{layout}.pdf"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `block_create_from_entities`

**Nhóm:** `blocks`  
**Làm gì:** Create a new block definition from existing entities in the drawing.

Works on both engines. The originals stay in model space — this defines a
reusable block from them rather than consuming them the way AutoCAD's BLOCK
command does; use `block_insert` to place copies, and delete the originals
yourself if you want the command's behaviour.

Handles that do not resolve are listed in `skipped` rather than silently
dropped, and a call where none resolve fails instead of leaving an empty
definition behind.

**Dùng khi nào:** Khi tạo, chèn, đọc hoặc quản lý block và block reference.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | New block definition name |
| `handles` | `array<string>` | có | `—` | List of entity handles to include in the block |
| `base_x` | `number` | không | `0.0` | Block base point X |
| `base_y` | `number` | không | `0.0` | Block base point Y |

**Ví dụ gọi**

```json
{
  "name": "example",
  "handles": [],
  "base_x": 0.0,
  "base_y": 0.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `block_define`

**Nhóm:** `blocks`  
**Làm gì:** Create a block definition with attribute definitions from typed specs.

The whole request is validated before anything is written: one malformed
entry refuses the call and leaves no definition behind. Refusals: a
malformed primitive or ATTDEF (names `entities[i]`/`attdefs[i]` and the
key), a non-finite base point (names `base_x`/`base_y`), a name clash
without `overwrite`, an anonymous `*` name, and a primitive `layer` that
is not in the drawing's layer table (names the missing layers) unless
`create_layers=true`, which creates them and lists them in
`layers_created`. `overwrite=true` replaces the *contents* of an existing
block so its INSERTs keep pointing at the name and show the new geometry;
`replaced` reports it. Geometry inside the block is ByBlock so the
INSERT's layer supplies colour and lineweight. Insert with
`block_insert(attributes={TAG: value})`.

**Dùng khi nào:** Khi tạo, chèn, đọc hoặc quản lý block và block reference.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | New block definition name |
| `entities` | `array<object>` | có | `—` | Primitives in block-local coordinates. type=line {x1,y1,x2,y2} | circle {cx,cy,r} | arc {cx,cy,r,start_deg,end_deg} | polyline {points,closed,bulges?} | text {text,x,y,height,rotation_deg?,align?} | solid {points (3-4)}. Optional layer (default 0). |
| `attdefs` | `any` | không | `None` | Attribute definitions: {tag, x, y, height, prompt?, default?, rotation_deg?, align?, invisible?} |
| `base_x` | `number` | không | `0.0` | Block base point X |
| `base_y` | `number` | không | `0.0` | Block base point Y |
| `overwrite` | `boolean` | không | `False` | Replace the contents of an existing definition of this name |
| `create_layers` | `boolean` | không | `False` | Create primitive layers that do not exist yet (default: refuse and name them) |

**Ví dụ gọi**

```json
{
  "name": "example",
  "entities": [],
  "attdefs": null,
  "base_x": 0.0,
  "base_y": 0.0,
  "overwrite": false,
  "create_layers": false
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `block_explode`

**Nhóm:** `blocks`  
**Làm gì:** Explode a block reference into its component entities, keeping its
attribute text (the Express Tools BURST rule, on both engines).

Every attached ATTRIB becomes a TEXT with the same value, placement,
height, rotation and layer (an invisible attribute becomes an invisible
TEXT; a multi-line attribute becomes an MTEXT carrying every line), and
a constant attribute (which has no ATTRIB) becomes a TEXT of its value
too; AutoCAD's plain EXPLODE would keep only the tag-name placeholders
and drop the values. Everything lands in the layout that owns the
reference (model space or its paper-space sheet), whichever tab is
current. Returns `inserted_handles` (the geometry), `attribute_texts`
(one TEXT or MTEXT handle per attribute), `exploded_handle` and
`backend`. Refused, with nothing written: a handle that is not a block
reference, a reference nested inside a block definition (explode the
outer reference instead), an external reference (bind it first), a
MINSERT grid, and -- headless only, capability `explode_opaque_members`
-- a block holding a member ezdxf cannot transform (an OLE2FRAME logo, a
VIEWPORT, a proxy entity without proxy graphics), named by member; the
live engine hands those to AutoCAD. Not undoable except through
`drawing_undo` / a transaction.

**Dùng khi nào:** Khi tạo, chèn, đọc hoặc quản lý block và block reference.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Block reference (INSERT) entity handle |

**Ví dụ gọi**

```json
{
  "handle": "A1B2"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `block_find_references`

**Nhóm:** `blocks`  
**Làm gì:** Find all insert references to a specific block definition.

Bounded by the backend's own default entity_list page (200 INSERTs scanned),
which is a pre-existing limit, not a new one: the compact envelope's `total`
counts the references found within that scan.

**Dùng khi nào:** Khi tạo, chèn, đọc hoặc quản lý block và block reference.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Block definition name to search for |
| `fields` | `any` | không | `None` | Project to these fields, in this order (e.g. ['handle','type','layer']); 'properties.<key>' reaches one nested value. Omit for the full record; an unknown name errors and lists the valid ones. |
| `compact` | `boolean` | không | `False` | Return a columnar {fields, rows, count, offset, total, truncated, next_offset} envelope instead of dicts: much cheaper per row, and the only shape that reports truncation. |

**Ví dụ gọi**

```json
{
  "name": "example",
  "fields": null,
  "compact": false
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `block_get_attributes`

**Nhóm:** `blocks`  
**Làm gì:** Get all attribute values from a block reference as {TAG: value} dict.

A multi-line attribute reports its whole content with `\P` between the
lines (AutoCAD's `TextString`), on both engines.

**Dùng khi nào:** Khi tạo, chèn, đọc hoặc quản lý block và block reference.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Block reference (INSERT) entity handle |

**Ví dụ gọi**

```json
{
  "handle": "A1B2"
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `block_insert`

**Nhóm:** `blocks`  
**Làm gì:** Insert a block and optionally set attribute values.

Refused before any write, on both engines: an undefined or layout block
name, and an attribute value that is not text — a string is written as
is (one line), an int or finite float as its plain digits (`101` →
`"101"`), while `null`, booleans, lists and objects are refused naming
the tag (they used to be written as their Python repr). Values for tags
the block does not define are ignored.

**Dùng khi nào:** Khi tạo, chèn, đọc hoặc quản lý block và block reference.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Block definition name |
| `x` | `number` | có | `—` | Insertion X |
| `y` | `number` | có | `—` | Insertion Y |
| `scale_x` | `number` | không | `1.0` | X scale factor |
| `scale_y` | `number` | không | `1.0` | Y scale factor |
| `rotation` | `number` | không | `0.0` | Rotation angle in degrees |
| `attributes` | `any` | không | `None` | Attribute values: {TAG: value} |
| `layer` | `any` | không | `None` | Layer name |

**Ví dụ gọi**

```json
{
  "name": "example",
  "x": 1.0,
  "y": 1.0,
  "scale_x": 1.0,
  "scale_y": 1.0,
  "rotation": 0.0,
  "attributes": null,
  "layer": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `block_list`

**Nhóm:** `blocks`  
**Làm gì:** List all block definitions in the drawing (name, origin, attribute count, entity count).

Never truncated — the whole block table is returned — so a compact envelope
here always reports truncated=false.

**Dùng khi nào:** Khi tạo, chèn, đọc hoặc quản lý block và block reference.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `fields` | `any` | không | `None` | Project to these fields, in this order (e.g. ['handle','type','layer']); 'properties.<key>' reaches one nested value. Omit for the full record; an unknown name errors and lists the valid ones. |
| `compact` | `boolean` | không | `False` | Return a columnar {fields, rows, count, offset, total, truncated, next_offset} envelope instead of dicts: much cheaper per row, and the only shape that reports truncation. |

**Ví dụ gọi**

```json
{
  "fields": null,
  "compact": false
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `block_set_attributes`

**Nhóm:** `blocks`  
**Làm gì:** Update attribute values in a block reference.

Same value rule as `block_insert`: strings and numbers are written,
`null` / booleans / lists / objects are refused naming the tag before
anything changes. `updated_tags` lists the tags that exist on the
reference and were written; unknown tags are ignored.

A multi-line attribute takes `Line1\PLine2` and keeps every line; the
value written is the one `block_get_attributes` reads back and
`block_explode` bursts, on both engines.

**Dùng khi nào:** Khi tạo, chèn, đọc hoặc quản lý block và block reference.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Block reference (INSERT) entity handle |
| `attributes` | `object` | có | `—` | Attribute values to update: {TAG: new_value} |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "attributes": {}
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `bom_extract`

**Nhóm:** `sheet`  
**Làm gì:** Walk the INSERTs and return the ISO 7573 item rows. Never modifies the
drawing. `bom_table` is what draws them.

Each row's source is reported: `xdata` when the ACADMCP_MECH payload
supplied it (what `std_part_insert` writes), `attributes` when the block's
own ATTRIBs did. A block with neither a payload nor a DESIGNATION attribute
is skipped rather than guessed at, and `skipped` counts them.

The whole drawing is read by default — `entity_list`'s 200-entity page is
paged through, not taken as a cap, because an item list that stops at the
200th INSERT prints a wrong QTY rather than a shorter one. Pass `limit` to
cap it deliberately; `truncated` is then true if and only if the cap cut
the list. Refusals: an unknown column or group_by field, named with the
list of the ones there are.

**Dùng khi nào:** Khi tạo và quản lý sheet, title block và hồ sơ phát hành.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `layer` | `string` | không | `` | Only read INSERTs on this layer; empty reads all. |
| `group_by` | `string` | không | `designation` | Field to group identical parts by: designation, standard, material, or '' for one row per insert. |
| `columns` | `any` | không | `None` | Columns to return; default item, qty, designation, standard, material. |
| `limit` | `integer` | không | `0` | Stop after this many item records; 0 (the default) reads the whole drawing. `truncated` says whether the cap cut the list. |

**Ví dụ gọi**

```json
{
  "layer": "",
  "group_by": "designation",
  "columns": null,
  "limit": 0
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `bom_table`

**Nhóm:** `sheet`  
**Làm gì:** Draw the ISO 7573 item list as a real TABLE entity, 180 mm wide (the
title-block width), growing upwards from directly above the title block.

With `direction="up"` the heading row sits against the title block and item
1 is the row above it, so the list extends upwards as parts are added —
which is what ISO 7573 asks for on a drawing. Pass `rows` to draw a list
you already have, or omit it and the tool runs `bom_extract` first.
`representation` reports what was drawn: `native` (a real ACAD_TABLE on the
live engine) or `composite` (rules and MTEXT headlessly, whose `handle` is
the first child). Refusals: no rows to draw, an unknown column, an unknown
direction, a `layout` that does not exist.

**Dùng khi nào:** Khi tạo và quản lý sheet, title block và hồ sơ phát hành.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `rows` | `any` | không | `None` | Rows to draw; omit to extract them from the drawing first. |
| `size` | `string` | không | `A3` | Sheet the list is placed on. |
| `orientation` | `string` | không | `landscape` | — |
| `origin_x` | `number` | không | `0.0` | — |
| `origin_y` | `number` | không | `0.0` | — |
| `at_x` | `any` | không | `None` | Override the anchor X; default is the title block's. |
| `at_y` | `any` | không | `None` | — |
| `direction` | `string` | không | `up` | 'up' (ISO 7573 on a drawing: heading at the bottom, items ascending) or 'down'. |
| `columns` | `any` | không | `None` | — |
| `row_height` | `number` | không | `7.0` | — |
| `layout` | `string` | không | `` | — |

**Ví dụ gọi**

```json
{
  "rows": null,
  "size": "A3",
  "orientation": "landscape",
  "origin_x": 0.0,
  "origin_y": 0.0,
  "at_x": null,
  "at_y": null,
  "direction": "up",
  "columns": null,
  "row_height": 7.0,
  "layout": ""
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `boundary_from_entities`

**Nhóm:** `analysis`  
**Làm gì:** Chain the given entities into one closed polyline.

The handles may arrive in any order — putting them in chain order is the
tool's job. A chain that does not close is refused, and the error names the
coordinates of the gap.

**Dùng khi nào:** Khi cần đọc, đo, thống kê hoặc phân tích bản vẽ mà không sửa dữ liệu.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handles` | `array<string>` | có | `—` | Handles of the 2D entities that form the loop. |
| `tolerance` | `number` | không | `1e-09` | Gap tolerance for joining endpoints. |

**Ví dụ gọi**

```json
{
  "handles": [],
  "tolerance": 1e-09
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `boundary_trace`

**Nhóm:** `analysis`  
**Làm gì:** AutoCAD's BOUNDARY/BPOLY: create a closed polyline around a seed point.

Returns the *nearest enclosing* loop, so a seed inside an island gives the
island rather than the outer region. Straight edges are split where they
cross, so a line drawn across a shape divides it the way it looks like it
should. A seed with no enclosing loop is refused, and the error names the
gap when the edges nearly close.

**Dùng khi nào:** Khi cần đọc, đo, thống kê hoặc phân tích bản vẽ mà không sửa dữ liệu.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `x` | `number` | có | `—` | Seed point X, inside the region to trace. |
| `y` | `number` | có | `—` | Seed point Y, inside the region to trace. |
| `layer` | `string` | không | `` | Only consider edges on this layer. Empty considers all. |
| `tolerance` | `number` | không | `1e-09` | Gap tolerance for joining edges. |

**Ví dụ gọi**

```json
{
  "x": 1.0,
  "y": 1.0,
  "layer": "",
  "tolerance": 1e-09
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `cable_takeoff`

**Nhóm:** `plant`  
**Làm gì:** A cable takeoff: one row per electrical load, the shop's cable method made repeatable.

Power, phases, voltage, neutral and VFD come from the P&ID's electrical
texts near each tag (Russian, Turkish and English spellings). **Power is
never invented**: a load with no stated kW keeps an empty cell and an open
item. The panel comes from the layout's wiring callouts ('Wiring to CP1'
and its variants, normalised to CP-1), else from the P&ID ('к CP1'); a load
neither places takes the nearest panel on the layout, flagged
`panel_inferred` (`panel_rule='stated'` leaves it open). The length is the
Manhattan distance on the layout from the load's tag to its panel's tag,
and the cable is ROUNDUP(length x (1 + allowance)) to the metre. Room and
panel totals count known power once: a load wired to a panel that states
its own power is part of that package, and the package's power is counted
instead of its children's - the rule is written on the method sheet.
Sections only from `section_rules`; no standard table is applied. Open
items: missing power, missing panel, a tag or panel not on the layout, no
layout at all, a load no section rule covers.

Read-only on both drawings. With `output` it writes one workbook - Metraj,
Özet, Kontrol, Metodoloji - as XLSX and, always, as CSV beside it.

Refused before a drawing is read: `lang` outside tr / en / ru, an allowance
outside 0-1 and a malformed section rule (named by its path,
`section_rules[0].section: ...`). A missing, unreadable or oversize drawing
is refused by the reader, which names MAX_DXF_BYTES. Without openpyxl the
XLSX is not written and `files.refused` carries `capability: "xlsx_write"`
naming the `office` extra; the CSV files are written all the same.

**Dùng khi nào:** Khi làm bản vẽ plant hoặc bố trí thiết bị công nghiệp.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `pid_path` | `any` | không | `None` | The P&ID carrying the electrical texts (kW, phases, voltage, VFD). Omit to read the current drawing. |
| `layout_path` | `any` | không | `None` | The layout with the tags, the panels and the 'Wiring to CPn' callouts. Omitted, every length stays empty with an open item. |
| `output` | `any` | không | `None` | Workbook to write (.xlsx); the four sheets are also written as CSV beside it. Omit to return the rows only. |
| `lang` | `string` | không | `en` | Headers and method text: tr | en | ru. |
| `allowance` | `number` | không | `0.2` | Allowance before rounding up to the metre (0.20 = 20 %). |
| `section_rules` | `any` | không | `None` | Your own section table: [{max_kw, section, phases (1|3, optional)}], e.g. [{'max_kw': 5.5, 'section': '5x2.5'}]. Omitted, no section is proposed. |
| `panel_rule` | `string` | không | `nearest` | A load no wiring callout places: 'nearest' takes the nearest panel on the layout and flags the row panel_inferred; 'stated' leaves it open. |

**Ví dụ gọi**

```json
{
  "pid_path": null,
  "layout_path": null,
  "output": null,
  "lang": "en",
  "allowance": 0.2,
  "section_rules": null,
  "panel_rule": "nearest"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `cad_batch`

**Nhóm:** `batch`  
**Làm gì:** Execute an ordered list of tool calls in ONE round trip.

N calls collapse into one request/response pair, and `bind` lets a later
step reference an earlier step's result so handles never have to be echoed
back through the model.

    steps=[
      {"tool": "entity_create_line",  "args": {...}, "bind": "edge"},
      {"tool": "point_from_snap",     "args": {"handle": "$edge", "snap": "mid"},
                                      "bind": "mid"},
      {"tool": "entity_create_circle","args": {"cx": "$mid.x", "cy": "$mid.y",
                                               "radius": 4}},
    ]

Successful steps report only their handle; pass verbose=True for the full
result. Anything without a handle is returned whole.

VALIDATION runs first, always: an unknown tool, a schema-invalid argument or
a reference no earlier step binds refuses the whole batch before anything
executes. `on_error` governs run-time failures only. dry_run=True returns
that validation report and executes nothing.

ERRORS are typed, never text: each failed step carries error.kind - one of
unsupported (with the backend `capability`), invalid_args, refused, failed,
unknown_tool, unresolved_ref, denied, malformed_step.

ATOMICITY is reported, not assumed. Read the `atomicity` block: on the
headless backend rollback restores a full document snapshot; on live AutoCAD
it sends an UNDO whose landing AutoCAD never confirms. The default
on_error="stop" claims nothing and is exact on both.

NOT CALLABLE from a batch: the raw command/LISP escape hatches, and
cad_batch itself. Call those directly.

For a few hundred entities of the same kind, entity_batch_create is denser
still (no per-step tool name) - and it can be one step of a cad_batch.

**Dùng khi nào:** Khi cần xử lý nhiều bản vẽ hoặc nhiều đối tượng trong một lượt.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `steps` | `array<object>` | có | `—` | Ordered steps. Each: {'tool': <tool name>, 'args': {...}, 'bind': <optional name>}. 'bind' names this step's result so a later step can reference it as '$name' (its handle), '$name.field' or '$name.list.0'. '$$' is a literal dollar sign. |
| `on_error` | `string` | không | `stop` | stop (default): halt at the first failure, keep what already ran. continue: run every step. rollback: open a checkpoint first and undo on failure - read the returned `atomicity` block for what that is worth on this backend. |
| `dry_run` | `boolean` | không | `False` | Validate every step against its tool's real JSON Schema and execute nothing. |
| `verbose` | `boolean` | không | `False` | Return each step's full result instead of just its handle. |

**Ví dụ gọi**

```json
{
  "steps": [],
  "on_error": "stop",
  "dry_run": false,
  "verbose": false
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `centre_marks`

**Nhóm:** `mechanical`  
**Làm gì:** Centre marks on the CENTER layer, whose linetype carries ISO 128-23's dash pattern.

Pass `handles` and the radii are read back with `entity_get` rather than
restated — a radius from memory is the classic silent wrong number.
Refusals, all before the first entity is written: neither `handles` nor
`centers` given (or both), a handle that is not a CIRCLE or ARC, a circle
in a plane tilted out of WCS XY (capability `ocs_tilted_plane`, so it has
no radius in this frame), a `style` outside mark/lines, a non-positive
`extension`, and `style='lines'` on a centre given without a radius.

**Dùng khi nào:** Khi dựng hoặc kiểm tra bản vẽ cơ khí, chi tiết và dung sai.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handles` | `any` | không | `None` | Handles of CIRCLEs/ARCs; their real centre and radius are read from the drawing. |
| `centers` | `any` | không | `None` | Explicit centres as [x, y] or [x, y, radius]; style='lines' needs the radius. |
| `style` | `string` | không | `mark` | mark (short cross at the centre) | lines (full centre lines). |
| `extension` | `number` | không | `3.0` | Arm length (mark) or overrun past the outline (lines), mm. |
| `layer` | `any` | không | `None` | Override the CENTER role layer. |

**Ví dụ gọi**

```json
{
  "handles": null,
  "centers": null,
  "style": "mark",
  "extension": 3.0,
  "layer": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `check_rulesets`

**Nhóm:** `cadtroly`  
**Làm gì:** Liệt kê bộ quy tắc trong kho (tiêu chuẩn đã bóc + chuẩn công ty), kèm hiệu lực và số dòng chờ duyệt.

**Dùng khi nào:** Khi cần dùng chức năng `check_rulesets` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `check_run`

**Nhóm:** `cadtroly`  
**Làm gì:** Luồng D: rà bản vẽ theo bộ quy tắc. Trả về từng vấn đề kèm điều khoản, handle, vị trí, có tự sửa được không.

**Dùng khi nào:** Khi cần dùng chức năng `check_run` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `path` | `string` | có | `—` | — |
| `ruleset` | `string` | có | `—` | id bộ quy tắc hoặc đường dẫn .rules.json |
| `include_unapproved` | `boolean` | không | `False` | — |

**Ví dụ gọi**

```json
{
  "path": "D:\\DuAn\\drawing.dwg",
  "ruleset": "example",
  "include_unapproved": false
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `construction_clear`

**Nhóm:** `premium`  
**Làm gì:** Delete every entity on the CONSTRUCTION layer. Idempotent.
Must be called before `drawing_finalize` to satisfy `construction_left` critique.

**Dùng khi nào:** Khi dùng chức năng nâng cao; kiểm tra capability trước nếu backend không hỗ trợ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `layer` | `string` | không | `CONSTRUCTION` | Layer to clear |

**Ví dụ gọi**

```json
{
  "layer": "CONSTRUCTION"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `construction_xline`

**Nhóm:** `premium`  
**Làm gì:** Create an infinite construction line on the CONSTRUCTION layer.
Use as scaffolding; call `construction_clear()` before finalize.

**Dùng khi nào:** Khi dùng chức năng nâng cao; kiểm tra capability trước nếu backend không hỗ trợ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `x` | `number` | có | `—` | Base point X |
| `y` | `number` | có | `—` | Base point Y |
| `angle_deg` | `number` | có | `—` | Angle in degrees (0=horizontal, 90=vertical) |
| `layer` | `string` | không | `CONSTRUCTION` | Layer for the construction line |

**Ví dụ gọi**

```json
{
  "x": 1.0,
  "y": 1.0,
  "angle_deg": 1.0,
  "layer": "CONSTRUCTION"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `data_extract`

**Nhóm:** `sheet`  
**Làm gì:** The same rows `bom_extract` returns, written to a file.

Refusals: a format that is not 'csv' or 'xlsx'; a drawing with nothing to
itemise (nothing is written); and `fmt='xlsx'` without openpyxl, which
carries `capability: "xlsx_write"` and names both the package to install
and the CSV route that always works.

**Dùng khi nào:** Khi tạo và quản lý sheet, title block và hồ sơ phát hành.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `path` | `string` | có | `—` | File to write, ending .csv or .xlsx. |
| `fmt` | `string` | không | `csv` | 'csv' (always available) or 'xlsx' (needs openpyxl). |
| `layer` | `string` | không | `` | Only read INSERTs on this layer; empty reads all. |
| `group_by` | `string` | không | `designation` | Group identical parts by this field, or ''. |
| `columns` | `any` | không | `None` | — |

**Ví dụ gọi**

```json
{
  "path": "D:\\DuAn\\drawing.dwg",
  "fmt": "csv",
  "layer": "",
  "group_by": "designation",
  "columns": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `datum_feature`

**Nhóm:** `engineering`  
**Làm gì:** Place a datum feature symbol (filled triangle + boxed letter).

Establishes the datum so a feature control frame referencing this letter
passes the `gdt` critique focus.

**Dùng khi nào:** Khi cần kiểm tra hoặc thao tác theo yêu cầu kỹ thuật.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `letter` | `string` | có | `—` | Datum letter, e.g. 'A' (avoid I, O, Q per ISO 1101). |
| `x` | `number` | có | `—` | Datum triangle apex X (on the referenced feature). |
| `y` | `number` | có | `—` | Datum triangle apex Y. |
| `size` | `number` | không | `5.0` | Triangle/label size (mm). |
| `layer` | `any` | không | `None` | Layer (defaults to the active DIM layer). |

**Ví dụ gọi**

```json
{
  "letter": "example",
  "x": 1.0,
  "y": 1.0,
  "size": 5.0,
  "layer": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `dimension_aligned`

**Nhóm:** `dimensions`  
**Làm gì:** Create an aligned dimension that measures the true distance between two points.

**Dùng khi nào:** Khi tạo hoặc hiệu chỉnh kích thước, ghi chú kích thước.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `x1` | `number` | có | `—` | First point X |
| `y1` | `number` | có | `—` | First point Y |
| `x2` | `number` | có | `—` | Second point X |
| `y2` | `number` | có | `—` | Second point Y |
| `dim_x` | `number` | có | `—` | Dimension line position X |
| `dim_y` | `number` | có | `—` | Dimension line position Y |
| `layer` | `any` | không | `None` | Layer name |

**Ví dụ gọi**

```json
{
  "x1": 1.0,
  "y1": 1.0,
  "x2": 1.0,
  "y2": 1.0,
  "dim_x": 1.0,
  "dim_y": 1.0,
  "layer": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `dimension_angular`

**Nhóm:** `dimensions`  
**Làm gì:** Create an angular dimension measuring the angle between two lines from a vertex.

**Dùng khi nào:** Khi tạo hoặc hiệu chỉnh kích thước, ghi chú kích thước.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `vertex_x` | `number` | có | `—` | Angle vertex X |
| `vertex_y` | `number` | có | `—` | Angle vertex Y |
| `x1` | `number` | có | `—` | First ray endpoint X |
| `y1` | `number` | có | `—` | First ray endpoint Y |
| `x2` | `number` | có | `—` | Second ray endpoint X |
| `y2` | `number` | có | `—` | Second ray endpoint Y |
| `text_x` | `number` | có | `—` | Dimension text position X |
| `text_y` | `number` | có | `—` | Dimension text position Y |
| `layer` | `any` | không | `None` | Layer name |

**Ví dụ gọi**

```json
{
  "vertex_x": 1.0,
  "vertex_y": 1.0,
  "x1": 1.0,
  "y1": 1.0,
  "x2": 1.0,
  "y2": 1.0,
  "text_x": 1.0,
  "text_y": 1.0,
  "layer": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `dimension_auto`

**Nhóm:** `premium`  
**Làm gì:** Generate ISO 129 dimensions across the listed entities in the chosen style.
V1 supports LINE entities only.

**Dùng khi nào:** Khi dùng chức năng nâng cao; kiểm tra capability trước nếu backend không hỗ trợ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handles` | `array<string>` | có | `—` | List of entity handles to dimension |
| `style` | `string` | không | `chain` | chain | baseline | ordinate |
| `offset` | `number` | không | `10.0` | Dimension-line offset from the geometry (mm) |

**Ví dụ gọi**

```json
{
  "handles": [],
  "style": "chain",
  "offset": 10.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `dimension_diameter`

**Nhóm:** `dimensions`  
**Làm gì:** Create a diameter dimension for a circle, optionally toleranced (e.g. ⌀20 H7).

**Dùng khi nào:** Khi tạo hoặc hiệu chỉnh kích thước, ghi chú kích thước.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `x1` | `number` | có | `—` | First point on diameter X |
| `y1` | `number` | có | `—` | First point on diameter Y |
| `x2` | `number` | có | `—` | Second point on diameter (opposite side) X |
| `y2` | `number` | có | `—` | Second point on diameter Y |
| `leader_length` | `number` | không | `10.0` | Leader line length |
| `layer` | `any` | không | `None` | Layer name |
| `tol_upper` | `any` | không | `None` | Upper deviation (mm) |
| `tol_lower` | `any` | không | `None` | Lower deviation (mm) |
| `tol_mode` | `string` | không | `none` | ISO 129 tolerance display: none | symmetric | deviation | limit | basic. |
| `text_override` | `any` | không | `None` | Replace the measured text ('<>' keeps the measurement) |
| `fit` | `any` | không | `None` | ISO 286 fit code (e.g. 'H7' hole / 'g6' shaft) resolved for the measured diameter. Mutually exclusive with tol_*. |

**Ví dụ gọi**

```json
{
  "x1": 1.0,
  "y1": 1.0,
  "x2": 1.0,
  "y2": 1.0,
  "leader_length": 10.0,
  "layer": null,
  "tol_upper": null,
  "tol_lower": null,
  "tol_mode": "none",
  "text_override": null,
  "fit": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `dimension_linear`

**Nhóm:** `dimensions`  
**Làm gì:** Create a linear dimension, optionally toleranced (ISO 129 or ISO 286 fit).

**Dùng khi nào:** Khi tạo hoặc hiệu chỉnh kích thước, ghi chú kích thước.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `x1` | `number` | có | `—` | First extension line origin X |
| `y1` | `number` | có | `—` | First extension line origin Y |
| `x2` | `number` | có | `—` | Second extension line origin X |
| `y2` | `number` | có | `—` | Second extension line origin Y |
| `dim_x` | `number` | có | `—` | Dimension line position X |
| `dim_y` | `number` | có | `—` | Dimension line position Y |
| `rotation` | `number` | không | `0.0` | Angle of the measured dimension (0=horizontal, 90=vertical) |
| `layer` | `any` | không | `None` | Layer name |
| `tol_upper` | `any` | không | `None` | Upper deviation (mm), e.g. 0.02 for +0.02 |
| `tol_lower` | `any` | không | `None` | Lower deviation (mm), e.g. 0.01 for -0.01 |
| `tol_mode` | `string` | không | `none` | ISO 129 tolerance display: none | symmetric (±tol_upper) | deviation (+tol_upper/-tol_lower) | limit (stacked limits) | basic (boxed). |
| `text_override` | `any` | không | `None` | Replace the measured text ('<>' keeps the measurement) |
| `fit` | `any` | không | `None` | ISO 286 fit code (e.g. 'H7', 'g6', 'js9'); resolves deviations from the authored tables for the measured nominal. Mutually exclusive with tol_*. |

**Ví dụ gọi**

```json
{
  "x1": 1.0,
  "y1": 1.0,
  "x2": 1.0,
  "y2": 1.0,
  "dim_x": 1.0,
  "dim_y": 1.0,
  "rotation": 0.0,
  "layer": null,
  "tol_upper": null,
  "tol_lower": null,
  "tol_mode": "none",
  "text_override": null,
  "fit": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `dimension_radius`

**Nhóm:** `dimensions`  
**Làm gì:** Create a radius dimension for a circle or arc, optionally toleranced.

**Dùng khi nào:** Khi tạo hoặc hiệu chỉnh kích thước, ghi chú kích thước.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `center_x` | `number` | có | `—` | Circle/arc center X |
| `center_y` | `number` | có | `—` | Circle/arc center Y |
| `chord_x` | `number` | có | `—` | Point on the circle/arc X (determines angle) |
| `chord_y` | `number` | có | `—` | Point on the circle/arc Y |
| `leader_length` | `number` | không | `10.0` | Length of the leader line |
| `layer` | `any` | không | `None` | Layer name |
| `tol_upper` | `any` | không | `None` | Upper deviation (mm) |
| `tol_lower` | `any` | không | `None` | Lower deviation (mm) |
| `tol_mode` | `string` | không | `none` | ISO 129 tolerance display: none | symmetric | deviation | limit | basic. |
| `text_override` | `any` | không | `None` | Replace the measured text ('<>' keeps the measurement) |
| `fit` | `any` | không | `None` | ISO 286 fit code resolved for the measured radius value. Mutually exclusive with tol_*. |

**Ví dụ gọi**

```json
{
  "center_x": 1.0,
  "center_y": 1.0,
  "chord_x": 1.0,
  "chord_y": 1.0,
  "leader_length": 10.0,
  "layer": null,
  "tol_upper": null,
  "tol_lower": null,
  "tol_mode": "none",
  "text_override": null,
  "fit": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `dimstyle_create`

**Nhóm:** `styles`  
**Làm gì:** Create a dimension style: preset values first, then `overrides`.

Refuses, before anything is written: an unknown preset; an override key
outside the 33-variable whitelist (the 17 preset variables plus DIMTOL,
DIMTP, DIMTM, DIMTOLJ, DIMTFAC, DIMLFAC, DIMRND, DIMATFIT, DIMTMOVE,
DIMCLRD/E/T, DIMSAH, DIMBLK1/2, DIMCEN); a value outside its range
(DIMDEC 0-8, sizes > 0, DIMTAD 0-4, DIMDSEP one character, lineweights an
AutoCAD code); a name that already exists (use `dimstyle_modify`); a
user DIMBLK/DIMBLK1/DIMBLK2 naming a block the drawing does not define
(built-in arrowheads need none); a DIMTXSTY that is neither an existing
text style nor a bundled preset (ISOCP, ISOCPEUR, ARIAL, ROMANS — those
are created on both engines, `textstyle_created`; live, a preset whose
font file the seat lacks is refused the same way, nothing written). On
the live engine a write ActiveX still refuses after the style is added
is rolled back — previous style current, the half-made entry deleted.
With `set_current` the next dimension carries the style on both engines.

**Dùng khi nào:** Khi quản lý text style, dimension style, linetype và kiểu hiển thị.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | New dimension style name, e.g. ISO-25, ANSI, MECH-A3 |
| `preset` | `any` | không | `None` | iso-25 (ISO 129-1, 2.5 mm, comma) | ansi (ASME Y14.2, 3 mm, point); omit for the ISO-25 base |
| `overrides` | `any` | không | `None` | DIM* variables applied on top of the preset, e.g. {DIMTXT: 3.5, DIMDSEP: '.', DIMTAD: 0} |
| `set_current` | `boolean` | không | `False` | Also make it the current dimension style |

**Ví dụ gọi**

```json
{
  "name": "example",
  "preset": null,
  "overrides": null,
  "set_current": false
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `dimstyle_list`

**Nhóm:** `styles`  
**Làm gì:** Every DIMSTYLE table entry with the seventeen preset variables
(DIMTXT, DIMASZ, DIMEXE, DIMEXO, DIMGAP, DIMTAD, DIMTIH, DIMTOH, DIMDEC,
DIMDSEP, DIMLUNIT, DIMZIN, DIMBLK, DIMTXSTY, DIMLWD, DIMLWE, DIMSCALE).

Headless, `values` is what the DXF stores (the schema default where an
entry omits a code). On the live engine ActiveX has no per-style getters,
so `values` is read for the *current* style only and the other rows carry
`values: null`, `values_available: false` — `dimstyle_set_current` a
style to read it. Never refuses on an open drawing.

**Dùng khi nào:** Khi quản lý text style, dimension style, linetype và kiểu hiển thị.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `dimstyle_modify`

**Nhóm:** `styles`  
**Làm gì:** Change variables on an existing dimension style.

`changed` names only the variables that actually moved — re-setting a
value to itself is not a change. `dimensions_using_style` lists the
dimensions already drawn with it; headlessly `rerender_required: true`
says they still show the old style until redrawn (AutoCAD re-renders on
the next regen). Refuses a missing style, an empty `overrides`, a key
outside the whitelist, a value outside its range, a DIMTXSTY that does
not exist, a user arrowhead block the drawing does not define — all
before any write. On the live engine, editing a non-current style makes
it current for the duration of the call and the previous style is
restored — also when a write fails midway (its unsaved overrides are
discarded, which is AutoCAD's own DIMSTYLE rule).

**Dùng khi nào:** Khi quản lý text style, dimension style, linetype và kiểu hiển thị.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Existing dimension style name |
| `overrides` | `object` | có | `—` | DIM* variables to change, e.g. {DIMDEC: 3, DIMTXT: 3.5} |

**Ví dụ gọi**

```json
{
  "name": "example",
  "overrides": {}
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `dimstyle_set_current`

**Nhóm:** `styles`  
**Làm gì:** Set `$DIMSTYLE` and load the style's variables as the current DIM*
settings — what a live seat's DIMSTYLE Restore does — so `dimension_*`
and `dimension_auto` draw with it on both engines. Per-dimension
tolerances, fits and text overrides still apply on top. Refuses a style
the drawing does not hold. Returns `previous` and `changed`.

**Dùng khi nào:** Khi quản lý text style, dimension style, linetype và kiểu hiển thị.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Dimension style to make current (case-insensitive) |

**Ví dụ gọi**

```json
{
  "name": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `document_activate`

**Nhóm:** `environment`  
**Làm gì:** Make one open document the active one; reports `previous`.

Matches the full path first, then the file name; an ambiguous name is
refused with the candidates, an unknown one with the list of open
documents. Headless, a document quarantined after an abandoned call cannot
be switched away from — `drawing_new`, `drawing_open` or closing it are
the ways out. Pack: settings · lean: no.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name_or_path` | `string` | có | `—` | A name from document_list (`gear.dxf`, `untitled-2`) or the full path |

**Ví dụ gọi**

```json
{
  "name_or_path": "D:\\DuAn\\drawing.dwg"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `document_close`

**Nhóm:** `environment`  
**Làm gì:** Close a document and report `saved`, `discarded_changes` and the new `active`.

Refusals, all before anything is closed: unsaved changes with neither
`save` nor `discard`; `save` on a document that has never been saved (no
path to write — live, `Close(True)` would open AutoCAD's Save dialog and
block the COM thread); `save` together with `discard`. Closing the last
document leaves the backend with none open, which every tool already
reports. `drawing_close` is the same operation for the active document
with its 1.4 contract kept. Pack: settings · lean: no.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name_or_path` | `any` | không | `None` | A name from document_list or the full path; omit for the active document |
| `save` | `boolean` | không | `False` | Write unsaved changes to the document's own path first |
| `discard` | `boolean` | không | `False` | Close even with unsaved changes, dropping them |

**Ví dụ gọi**

```json
{
  "name_or_path": null,
  "save": false,
  "discard": false
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `document_list`

**Nhóm:** `environment`  
**Làm gì:** Every open document with `document_id`, `name`, `path`, `active`, `saved` and
`entity_count`.

Headless, the server keeps its own registry: `drawing_new` / `drawing_open`
add an entry (`untitled-N` or the file path) instead of replacing the only
one, and `document_activate` chooses which one every later tool targets.
Live, this is AutoCAD's `Documents` collection. No refusals: an empty
backend answers with an empty list. Pack: settings · lean: no.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `drawing_apply_discipline_standard`

**Nhóm:** `cadtroly`  
**Làm gì:** Set up a drawing for a civil/architectural discipline in one call.

**Dùng khi nào:** Khi cần dùng chức năng `drawing_apply_discipline_standard` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `discipline` | `string` | có | `—` | building | road | bridge (aliases: nha | duong | cau) |
| `layers` | `boolean` | không | `True` | Create the discipline layer set |
| `units` | `boolean` | không | `True` | Apply ISO-25/ISOCP and millimetre drafting units |
| `naming` | `string` | không | `auto` | auto | ncs (international) | vn (Vietnamese project convention) |

**Ví dụ gọi**

```json
{
  "discipline": "example",
  "layers": true,
  "units": true,
  "naming": "auto"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_apply_iso_layers`

**Nhóm:** `premium`  
**Làm gì:** Bootstrap a full ISO-conformant layer set with correct colors and lineweights.
Idempotent — existing layers are not modified.

Refused by name: a standard that is not one of mech, pid, iso13567, arch.

**Dùng khi nào:** Khi dùng chức năng nâng cao; kiểm tra capability trước nếu backend không hỗ trợ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `standard` | `string` | không | `mech` | Layer set: mech (DIN/ISO mechanical), pid (P&ID), iso13567 (CAD layer naming), arch (ISO 13567-style architectural: walls, poche, doors, windows, stairs, furniture, sanitary, grid, rooms, dimensions, symbols, overhead). |

**Ví dụ gọi**

```json
{
  "standard": "mech"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_apply_standard`

**Nhóm:** `styles`  
**Làm gì:** One call for the common case: the standard's dimension style (created
if missing, then current), its text style (created if missing, then
current), the shared units, and with `layers` the `mech` layer set (ANSI
layer naming is company-specific, so both standards share it).

Every item reports `created` or already present; `settings.changed`
names only the variables that moved, so a second call reports nothing.
An existing ISO-25 / ANSI style is reused as it is, not reset — use
`dimstyle_modify` to change one. Refuses an unknown standard, or a units
variable it cannot read back, before any write; the underlying style
refusals (`dimstyle_create`, `textstyle_create`) apply unchanged. In the
`lean` profile (Task 13).

**Dùng khi nào:** Khi quản lý text style, dimension style, linetype và kiểu hiển thị.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `standard` | `string` | có | `—` | iso (ISO-25 / ISOCP, decimal comma) | ansi (ANSI / ROMANS, decimal point) |
| `layers` | `boolean` | không | `True` | Also bootstrap the mech layer set with ISO 128 lineweights |
| `units` | `boolean` | không | `True` | Also write INSUNITS mm, LUNITS/AUNITS decimal, LTSCALE 1, DIMSCALE 1 |

**Ví dụ gọi**

```json
{
  "standard": "example",
  "layers": true,
  "units": true
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_audit`

**Nhóm:** `drawing`  
**Làm gì:** Audit the drawing: repair every fixable structural problem, and report it.

This mutates the drawing. `fixes` lists repairs that have ALREADY been
applied, so save afterwards to keep them; `errors` lists problems that could
not be repaired. On the live COM backend AutoCAD applies repairs but hands
back no counts, so they arrive as null with `detail: "unavailable"` rather
than as zero.

**Dùng khi nào:** Khi mở, lưu, đóng, xuất hoặc kiểm tra trạng thái bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_close`

**Nhóm:** `drawing`  
**Làm gì:** Close the active document. If save is True (default), the drawing is
saved to its current path before closing; an untitled document is closed
and `warning` says its changes were discarded (headless) or the call is
refused (live, where the alternative is a modal Save dialog). The
active-document case of `document_close`; after the last document is
closed, call drawing_new or drawing_open before any other tool.

**Dùng khi nào:** Khi mở, lưu, đóng, xuất hoặc kiểm tra trạng thái bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `save` | `boolean` | không | `True` | Save the drawing before closing |

**Ví dụ gọi**

```json
{
  "save": true
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_critique`

**Nhóm:** `premium`  
**Làm gì:** Run premium-quality checks. Returns zero issues for a clean drawing.

Standard production gate: must return [] before `drawing_finalize`.

**Dùng khi nào:** Khi dùng chức năng nâng cao; kiểm tra capability trước nếu backend không hỗ trợ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `focus` | `any` | không | `None` | Subset of: iso128, layer_color, dim_overlap, untrimmed_corner, duplicate_entities, construction_left, gdt, the P&ID focuses pid_dangling_line, pid_duplicate_tag, pid_incompatible_connection, pid_untagged_instrument, pid_illegal_tag, pid_unconnected_equipment (silent on a drawing with no P&ID symbols), and the mechanical focuses mech_missing_centreline, mech_unhatched_section, mech_view_misaligned, mech_duplicate_dimension, mech_thread_unrepresented, mech_bom_balloon_mismatch (silent on a drawing with no mechanical part), and the architectural focuses arch_room_unlabelled, arch_wall_gap, arch_opening_clash (silent on a drawing with no ACADMCP_ARCH record), and the topology focuses topo_dangling_endpoint, topo_near_miss, topo_interior_crossing (network layers no P&ID or architectural focus reads). None = run all. |

**Ví dụ gọi**

```json
{
  "focus": null
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `drawing_deliver`

**Nhóm:** `engineering`  
**Làm gì:** Create a hashed, validated delivery bundle and verify DXF save/reopen parity.

The result status is ``success``, ``failed_validation`` or ``failed_export``.
Failure intentionally keeps all generated artifacts for diagnosis.

**Dùng khi nào:** Khi cần kiểm tra hoặc thao tác theo yêu cầu kỹ thuật.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `output_dir` | `string` | có | `—` | Output directory for drawing artifacts and manifest.json. |
| `formats` | `any` | không | `None` | Requested formats: dxf, pdf, png. |
| `min_score` | `number` | không | `95.0` | Minimum accepted quality score. |
| `strict_critique` | `boolean` | không | `True` | Block delivery on every non-info critique issue. |
| `expected` | `any` | không | `None` | Optional validator expectations for the drawing. |

**Ví dụ gọi**

```json
{
  "output_dir": "example",
  "formats": null,
  "min_score": 95.0,
  "strict_critique": true,
  "expected": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_diff`

**Nhóm:** `understanding`  
**Làm gì:** Compare two revisions of one drawing by geometric signature (spec §10).

Entities are matched exactly first (type, layer, geometry rounded to `tol`,
text, block, attributes - handles do not matter), then by handle while
handles look stable, then by type + layer + nearest position within
`move_tol`; what is left is added or removed. The report counts changes by
layer and type, lists each changed entity with what changed (moved by, text
from -> to, attribute from -> to, radius from -> to, ...), compares the
block definitions when both revisions are DXF files or the headless current
document, and groups the changes into clusters.

Read-only unless `markup=True`: then revision clouds are drawn around the
model-space clusters on the current document, which must be the newer
revision, and filed as one revision row - the only write this tool makes.

Refused before anything is read: `markup=True` with `new_path` (the clouds go
on the current document), `markup=True` without a valid `rev`, `markup=True`
on an engine without the revcloud capability (the live engine -
`capability: "revcloud"`), a path that does not exist, a DXF over
MAX_DXF_BYTES (the size and the variable named), a file that is not a
readable DXF, and a non-positive `tol` or `move_tol`.

**Dùng khi nào:** Khi cần LLM hiểu cấu trúc, ngữ cảnh hoặc nội dung bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `old_path` | `string` | có | `—` | The OLDER revision: a DXF path (a DWG only on the live engine, which exports it read-only). |
| `new_path` | `any` | không | `None` | The NEWER revision: a DXF path, or omitted for the current document. |
| `tol` | `number` | không | `0.01` | Geometry is compared rounded to this many drawing units. |
| `move_tol` | `any` | không | `None` | An unmatched entity is paired with the nearest one of its type and layer within this distance and reported as changed; default 2 % of the drawing's robust diagonal. |
| `limit` | `integer` | không | `200` | Rows kept per list (changed, added, removed). |
| `markup` | `boolean` | không | `False` | Draw revision clouds around every cluster of change on the current document (the newer revision) and file them under `rev`. |
| `rev` | `string` | không | `` | Revision code for markup=True: one to three capitals or digits. |
| `description` | `string` | không | `` | Revision-row text for markup=True; default: the counts. |

**Ví dụ gọi**

```json
{
  "old_path": "D:\\DuAn\\drawing.dwg",
  "new_path": null,
  "tol": 0.01,
  "move_tol": null,
  "limit": 200,
  "markup": false,
  "rev": "",
  "description": ""
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_entities`

**Nhóm:** `cadtroly`  
**Làm gì:** Liệt kê đối tượng theo layer/block/loại kèm handle, toạ độ, chiều dài, diện tích, text.

**Dùng khi nào:** Khi cần dùng chức năng `drawing_entities` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `path` | `string` | có | `—` | — |
| `layer` | `any` | không | `None` | — |
| `block` | `any` | không | `None` | — |
| `kind` | `any` | không | `None` | — |
| `limit` | `integer` | không | `100` | — |

**Ví dụ gọi**

```json
{
  "path": "D:\\DuAn\\drawing.dwg",
  "layer": null,
  "block": null,
  "kind": null,
  "limit": 100
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `drawing_export_dwg`

**Nhóm:** `sheet`  
**Làm gì:** Write a real DWG — not a DXF under a .dwg name.

On a live AutoCAD seat this is `Document.SaveAs` with the matching
AcSaveAsType, which (as AutoCAD's own SaveAs does) leaves the session bound
to the file it just wrote. Headlessly it needs the ODA File Converter; when
that is absent the call is refused with `capability: "dwg_write"` and the
refusal names the install route and `drawing_export_dxf`, which writes a
DXF AutoCAD opens unchanged. Check `system_capabilities` first: the ezdxf
flag is re-evaluated at call time, so installing the converter changes it
without a restart. An unknown version is refused by name with the six.

**Dùng khi nào:** Khi tạo và quản lý sheet, title block và hồ sơ phát hành.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `path` | `string` | có | `—` | Full path of the .dwg to write. |
| `version` | `string` | không | `R2018` | R2000 | R2004 | R2007 | R2010 | R2013 | R2018. |

**Ví dụ gọi**

```json
{
  "path": "D:\\DuAn\\drawing.dwg",
  "version": "R2018"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_export_dxf`

**Nhóm:** `drawing`  
**Làm gì:** Export the current drawing as a DXF file.

**Dùng khi nào:** Khi mở, lưu, đóng, xuất hoặc kiểm tra trạng thái bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `path` | `string` | có | `—` | Output .dxf file path |

**Ví dụ gọi**

```json
{
  "path": "D:\\DuAn\\drawing.dwg"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_export_pdf`

**Nhóm:** `drawing`  
**Làm gì:** Export the current drawing (or a paper-space layout) to PDF.

**Dùng khi nào:** Khi mở, lưu, đóng, xuất hoặc kiểm tra trạng thái bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `path` | `string` | có | `—` | Output .pdf file path |
| `layout` | `any` | không | `None` | Paper-space layout to plot (default: model space). COM plots the layout natively incl. viewport content; ezdxf renders the layout's own entities. |

**Ví dụ gọi**

```json
{
  "path": "D:\\DuAn\\drawing.dwg",
  "layout": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_finalize`

**Nhóm:** `engineering`  
**Làm gì:** Premium completion gate: runs BOTH the 8-step validator AND the premium critique focuses
(iso128, layer_color, dim_overlap, untrimmed_corner, duplicate_entities, construction_left,
gdt, plus the P&ID focuses pid_dangling_line, pid_duplicate_tag,
pid_incompatible_connection, pid_untagged_instrument, pid_illegal_tag,
pid_unconnected_equipment — silent on a sheet with no P&ID symbols, plus the
mechanical focuses mech_missing_centreline, mech_unhatched_section,
mech_view_misaligned, mech_duplicate_dimension, mech_thread_unrepresented,
mech_bom_balloon_mismatch — silent on a sheet with no mechanical part, plus the
architectural focuses arch_room_unlabelled, arch_wall_gap, arch_opening_clash —
silent on a sheet with no ACADMCP_ARCH record, plus the topology focuses
topo_dangling_endpoint, topo_near_miss, topo_interior_crossing — on network
layers no P&ID or architectural focus reads, silent on every sheet this server draws),
then saves to disk, exports a screenshot, and returns the DWG path.

Raises ToolError if any validator 'error' finding is present, or if critique reports an
'error' (or, with strict_critique=True, any critique issue). Critique warnings are surfaced
under payload['critique'] without failing the gate by default.

**Dùng khi nào:** Khi cần kiểm tra hoặc thao tác theo yêu cầu kỹ thuật.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `save_path` | `any` | không | `None` | If given, save drawing here before validation. Pass full path including extension. |
| `screenshot_path` | `any` | không | `None` | If given, write PNG screenshot to this path. |
| `expected` | `any` | không | `None` | Optional contract: {'part_type', 'helix_angle', 'must_have_bore', 'must_have_keyway'} |
| `strict_critique` | `boolean` | không | `False` | If true, ANY critique issue (including warnings) fails the gate — the full premium discipline. Default false: only critique 'error' issues (e.g. leftover construction geometry) fail; warnings are surfaced in the payload. |

**Ví dụ gọi**

```json
{
  "save_path": null,
  "screenshot_path": null,
  "expected": null,
  "strict_critique": false
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_info`

**Nhóm:** `entity_query`  
**Làm gì:** Get comprehensive metadata for the current drawing.

Returns: name, path, entity_count, layer_count, block_count,
extents (min/max), units, version, backend name.

**Dùng khi nào:** Khi cần tìm và đọc thuộc tính đối tượng theo handle hoặc điều kiện.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `drawing_new`

**Nhóm:** `drawing`  
**Làm gì:** Create a new drawing, optionally from a template.

A bundled name resolves to `templates/<name>.dxf` headlessly and
`templates/<name>.dwt` on the live engine (falling back to the DXF with
`source: "bundled_dxf"` when no `.dwt` twin is committed); a path is used
as given. The result carries `template: {name|path, path, source}`.

On the live engine only a genuine `.dwt` reaches `Documents.Add` —
measured on AutoCAD 2026, `Add(<file.dxf>)` silently returns the default
drawing — so a `.dxf` template (bundled or a path) is first converted
through AutoCAD into a cached `.dwt` and `template.dwt` names it
(`template.dwt_cached` says whether the conversion was reused). The
drawing then really carries the template's layers, tabs and page setup.

Refused before anything is replaced: a bare name that is not in the
catalogue (the message lists the five), a template path that does not
exist, and a path outside the allowed directories. With `bootstrap=True`
(default) the standard engineering linetypes and layers are ensured
afterwards — idempotent on a template that already has them.

**Dùng khi nào:** Khi mở, lưu, đóng, xuất hoặc kiểm tra trạng thái bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `template` | `any` | không | `None` | Bundled template name (drawing_template_list: iso_a3_mech, iso_a1_arch, iso_a3_pid, ansi_b_mech, ansi_d_arch) or a path to a .dwt/.dxf template file. |
| `bootstrap` | `boolean` | không | `True` | Auto-load CENTER/HIDDEN/PHANTOM linetypes and create standard engineering layers (GEOMETRY, DIM, CENTER, HIDDEN, PHANTOM, HATCH, TEXT, TITLEBLOCK). Disable for vanilla DXF. |

**Ví dụ gọi**

```json
{
  "template": null,
  "bootstrap": true
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_open`

**Nhóm:** `drawing`  
**Làm gì:** Open an existing DXF drawing file (DWG too, on the live COM backend).

T0.2: a .dwg path is refused up front when the active backend has no `dwg`
capability. ezdxf sniffs content rather than extensions, so it would parse a
mislabelled DXF-in-a-.dwg and this tool would answer with a document that
does not exist in that format.

**Dùng khi nào:** Khi mở, lưu, đóng, xuất hoặc kiểm tra trạng thái bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `path` | `string` | có | `—` | Full path to the .dxf file. .dwg needs a backend that can read it (the live COM backend); the headless ezdxf backend refuses it. |

**Ví dụ gọi**

```json
{
  "path": "D:\\DuAn\\drawing.dwg"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_plan`

**Nhóm:** `premium`  
**Làm gì:** Commit a PlanSpec before any geometry is created.

The PlanSpec is stored on the backend and surfaced for reference during
the workflow (it is not replayed as a critique). Always call this FIRST
in a premium workflow.

**Dùng khi nào:** Khi dùng chức năng nâng cao; kiểm tra capability trước nếu backend không hỗ trợ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `intent` | `string` | có | `—` | One-line description of what this drawing represents. |
| `sheet_size` | `string` | không | `A3` | Paper size: A4 / A3 / A2 / A1 / A0. |
| `scale` | `number` | không | `1.0` | Drawing scale (1.0 = 1:1, 0.1 = 1:10, etc). |
| `layer_set_id` | `string` | không | `mech` | Layer set to bootstrap: mech / pid / iso13567. |
| `view_count` | `integer` | không | `1` | — |
| `dim_style` | `string` | không | `chain` | Default dimensioning style: chain / baseline / ordinate / mixed. |
| `notes` | `any` | không | `None` | Free-form constraint notes. |
| `requirements` | `any` | không | `None` | Normalized preflight requirements. |
| `spec_hash` | `any` | không | `None` | Hash returned by the latest ready drawing_preflight. |

**Ví dụ gọi**

```json
{
  "intent": "example",
  "sheet_size": "A3",
  "scale": 1.0,
  "layer_set_id": "mech",
  "view_count": 1,
  "dim_style": "chain",
  "notes": null,
  "requirements": null,
  "spec_hash": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_preflight`

**Nhóm:** `premium`  
**Làm gì:** Validate and normalize requirements before committing a drawing plan.

**Dùng khi nào:** Khi dùng chức năng nâng cao; kiểm tra capability trước nếu backend không hỗ trợ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `intent` | `string` | có | `—` | One-line description of what this drawing represents. |
| `requirements` | `any` | không | `None` | Units, part_type, dimensions, tolerance_policy and optional constraints. |
| `sheet_size` | `string` | không | `A3` | A4 / A3 / A2 / A1 / A0. |
| `scale` | `number` | không | `1.0` | — |
| `layer_set_id` | `string` | không | `mech` | mech / pid / iso13567. |
| `view_count` | `integer` | không | `1` | — |
| `dim_style` | `string` | không | `chain` | chain / baseline / ordinate / mixed. |
| `allow_assumptions` | `boolean` | không | `False` | Allow documented defaults for units and tolerance policy. |

**Ví dụ gọi**

```json
{
  "intent": "example",
  "requirements": null,
  "sheet_size": "A3",
  "scale": 1.0,
  "layer_set_id": "mech",
  "view_count": 1,
  "dim_style": "chain",
  "allow_assumptions": false
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `drawing_properties_get`

**Nhóm:** `environment`  
**Làm gì:** The DWGPROPS dialog as data: `summary` (title, subject, author, keywords,
comments), `summary_available`, and `custom` ({key: value}).

On the live engine the summary comes from the document's SummaryInfo. The
headless engine cannot read that stream, so the five summary fields are
`null` with `summary_available: false` — not empty strings, which would
claim the drawing has no title. Custom properties (`$CUSTOMPROPERTYTAG` /
`$CUSTOMPROPERTY` header pairs) are read on both engines.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `drawing_properties_set`

**Nhóm:** `environment`  
**Làm gì:** Write DWGPROPS fields. Only the arguments given are touched; returns
`summary_written`, `custom_written` and `custom_deleted` (a key that was
never there is not reported deleted).

Refusals, before anything is written: a summary field on the headless
engine (`capability: dwgprops` — SummaryInfo lives in the DWG, a DXF has
no slot for it; custom properties still work headlessly), a non-string
value (`TypeError` naming the field or key — nothing is coerced with
`str()`), an empty custom key, a custom key to *write* that AutoCAD's
AddCustomInfo would reject mid-write (measured on AutoCAD 2026: leading or
trailing whitespace, or any of the thirteen characters
`" * , / : ; < = > ? \ ` |` anywhere in the key; internal spaces, tabs
and unicode are fine — `ValueError` naming the key, on both engines; a
delete is exempt because RemoveCustomByKey never validates syntax, so a
key that reached the drawing another way stays removable), two keys in
one request that AutoCAD would call the same key (its key compare is a
simple per-character case compare: `Project`/`PROJECT` and `Grün`/`GRÜN`
are one key, `Straße`/`STRASSE` are two), a line break in a custom key or
value (it corrupts the DXF on save), and headlessly a document older than
R2004 (`ValueError` — ezdxf only writes the custom-property header pairs
for AC1018+, so they would vanish at save; save as R2004 or newer first).
A key is matched to the drawing by that same rule on both engines and
keeps its stored spelling when updated. On the live engine an exact
spelling is changed with SetCustomByKey; otherwise AutoCAD decides —
AddCustomInfo, and on its 'Duplicate key' SetCustomByKey; a delete is
RemoveCustomByKey, and its 'Key not found' is reported as not deleted.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `title` | `any` | không | `None` | SummaryInfo Title |
| `subject` | `any` | không | `None` | SummaryInfo Subject |
| `author` | `any` | không | `None` | SummaryInfo Author |
| `keywords` | `any` | không | `None` | SummaryInfo Keywords |
| `comments` | `any` | không | `None` | SummaryInfo Comments |
| `custom` | `any` | không | `None` | Custom properties to write: {key: text}; a null value deletes the key. Keys not mentioned are left alone. |

**Ví dụ gọi**

```json
{
  "title": null,
  "subject": null,
  "author": null,
  "keywords": null,
  "comments": null,
  "custom": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_purge`

**Nhóm:** `drawing`  
**Làm gì:** Purge all unused objects (layers, blocks, linetypes, styles) from the drawing.

**Dùng khi nào:** Khi mở, lưu, đóng, xuất hoặc kiểm tra trạng thái bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_read`

**Nhóm:** `cadtroly`  
**Làm gì:** Đọc bản vẽ thành số liệu: layer, block, số đối tượng, đơn vị. Không gửi gì đi.

**Dùng khi nào:** Khi cần dùng chức năng `drawing_read` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `path` | `string` | có | `—` | Đường dẫn DXF (DWG cần ODA converter) |

**Ví dụ gọi**

```json
{
  "path": "D:\\DuAn\\drawing.dwg"
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `drawing_redo`

**Nhóm:** `drawing`  
**Làm gì:** Reapply the operation you just undid.

Same history as `drawing_undo`, so the headless backend needs
`EZDXF_UNDO_DEPTH` set. Anything drawn after an undo discards the redo
branch — otherwise redo would restore a state that never existed, with
geometry you had removed reappearing beside geometry you drew afterwards.

**Dùng khi nào:** Khi mở, lưu, đóng, xuất hoặc kiểm tra trạng thái bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_refine`

**Nhóm:** `premium`  
**Làm gì:** Run a bounded, transaction-safe critique/repair/re-critique loop.

**Dùng khi nào:** Khi dùng chức năng nâng cao; kiểm tra capability trước nếu backend không hỗ trợ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `max_rounds` | `integer` | không | `3` | — |
| `min_score` | `number` | không | `95.0` | — |
| `focus` | `any` | không | `None` | Critique focuses to repair; None runs all. |
| `allowed_repairs` | `any` | không | `None` | Optional allowlist of repair focus names. |
| `dry_run` | `boolean` | không | `False` | Return the repair plan without modifying the drawing. |

**Ví dụ gọi**

```json
{
  "max_rounds": 3,
  "min_score": 95.0,
  "focus": null,
  "allowed_repairs": null,
  "dry_run": false
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_save`

**Nhóm:** `drawing`  
**Làm gì:** Save the current drawing. Optionally specify a new path.

**Dùng khi nào:** Khi mở, lưu, đóng, xuất hoặc kiểm tra trạng thái bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `path` | `any` | không | `None` | Optional save path; uses current path if omitted |

**Ví dụ gọi**

```json
{
  "path": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_save_as`

**Nhóm:** `drawing`  
**Làm gì:** Save current drawing to a new path/format (DWG, DXF, or DWT template).

The on-disk format is derived from the file extension so the bytes always
match the name (N2) — e.g. 'part.dxf' writes DXF, not DWG. `format` overrides
only when the path has no recognised extension.

**Dùng khi nào:** Khi mở, lưu, đóng, xuất hoặc kiểm tra trạng thái bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `path` | `string` | có | `—` | Full destination path including extension |
| `format` | `string` | không | `` | Output format override: dwg, dxf, dwt. Default: derive from the path extension (the extension is authoritative). |

**Ví dụ gọi**

```json
{
  "path": "D:\\DuAn\\drawing.dwg",
  "format": ""
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_scale_check`

**Nhóm:** `understanding`  
**Làm gì:** Is the drawing to scale against the reference - or a schematic whose lengths
are lengths of drawn line, not of pipe? Read-only on both drawings.

Equipment tags are matched between the two (a Cyrillic look-alike such as
`Т4100` is the Latin `T4100`). Only a tag found exactly once in each is used;
a tag found more than once (plan copies, a legend, a second sheet) is listed
in `ambiguous` and takes no part. When a drawing holds several bodies of
content (two copies of one plan), the pair of scopes - whole drawing or one
cluster on each side - that matches the most tags is used and named in
`scope`. For every two matched tags at least `min_pair_mm` apart on the
reference, the ratio of their distances is taken (both in millimetres by
each drawing's inferred unit, see `drawing_understand`). The result gives
the matched tags, the median ratio, the quartiles and their range, the
share of pairs within +/-10 % of the median, the same per room of the
reference (or per cluster for tags in no room) in `groups`, and a verdict:
`to_scale` (at least 80 % within the band; `factor` is the median, so a
uniform other scale is recognised), `schematic` (50 % or less), `partly`
in between, `insufficient` with fewer than three matched tags or no pair
above the floor. Tag labels are not equipment centres; the band and the
floor absorb that offset, and the result's `notes` say so.

Refused before anything is read: a `reference` or `path` that does not
exist, a DXF over `MAX_DXF_BYTES` (the refusal names the size and the
variable), a file the engine cannot parse (a DWG headlessly), and a
`min_pair_mm` that is not a positive finite number.

**Dùng khi nào:** Khi cần LLM hiểu cấu trúc, ngữ cảnh hoặc nội dung bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `reference` | `string` | có | `—` | The reference drawing of the same plant (a DXF, usually the layout): distances on it are the ones the other drawing is measured against. |
| `path` | `any` | không | `None` | The drawing to check (usually the P&ID); omitted: the current document. |
| `min_pair_mm` | `number` | không | `2000.0` | Tag pairs closer than this on the reference (mm) are left out: a tag label is not an equipment centre. |

**Ví dụ gọi**

```json
{
  "reference": "example",
  "path": null,
  "min_pair_mm": 2000.0
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `drawing_settings`

**Nhóm:** `system`  
**Làm gì:** Read or change common AutoCAD drawing settings by friendly name.

A convenience facade over the system variables (INSUNITS, LUPREC, LTSCALE,
DIMSCALE, DIMTXT, DIMASZ, DIMDEC, DIMDSEP, DIMZIN, TEXTSIZE, OSMODE, LIMMIN/
LIMMAX, GRIDMODE/GRIDUNIT, SNAPMODE/SNAPUNIT, ORTHOMODE, AUTOSNAP/POLARANG,
PSLTSCALE, CANNOSCALE, LUNITS, AUNITS, DIMSTYLE, TEXTSTYLE) so the user can
say "set units to mm, limits to A3 and the grid on" without memorising
sysvar names. Call with no argument for a full snapshot; a write returns
`applied`, `changed` ({key: [old, new]} — only what moved) and `errors`.

`dim_text_height` / `dim_arrow_size` / `dim_decimals` / `decimal_separator`
/ `zero_suppression` shape the *dimension* — `text_size` is TEXTSIZE, the
height of a standalone TEXT entity, and does not touch dimensions.

Refusals, per key, nothing else rolled back: an unknown key; a value outside
its range (grid/snap spacing > 0, polar_angle 0–360, precision 0–8, …); a
malformed `limits` or `annotation_scale`; `osmode` / `polar` / `polar_angle`
on the headless engine (`capability: registry_sysvar` — AutoCAD keeps them in
the registry, a file cannot, and a headless snapshot reports them as `None`);
`dimstyle` / `textstyle` when the backend has no styles contract. On the
live engine `annotation_scale` must name a scale in the drawing's scale list
(SCALELISTEDIT) and AutoCAD refuses the write on a
paper-space layout with no active viewport; the headless engine adds the
scale, seeding AutoCAD's default list first when the drawing has none,
and refuses it on an R12 file (no OBJECTS section, so the value would
vanish at save — save as R2000 or newer first; limits/grid/ortho survive).
Headlessly, grid/snap are stored on the active VPORT and the annotation
scale in the variable dictionary — the places AutoCAD reads them from.

**Dùng khi nào:** Khi cần chẩn đoán server hoặc trạng thái kết nối.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `settings` | `any` | không | `None` | Omit to READ every setting; pass a dict to CHANGE them. Friendly keys: units (mm/cm/m/inch/feet), linear_precision, angular_precision, ltscale, dimscale, dim_text_height, dim_arrow_size, dim_decimals, decimal_separator ("." or ","), zero_suppression, text_size, point_mode, point_size, osmode, fillet_radius, limits ([[xmin,ymin],[xmax,ymax]]), grid (bool), grid_spacing, snap (bool), snap_spacing, ortho (bool), polar (bool), polar_angle (degrees), psltscale (bool), annotation_scale ("1:50"), linear_units (decimal|engineering|architectural|fractional|scientific), angular_units (degrees|dms|grads|radians|surveyor), dimstyle, textstyle (current style names). Example: {"units": "mm", "limits": [[0, 0], [420, 297]], "grid": true}. |

**Ví dụ gọi**

```json
{
  "settings": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_template_list`

**Nhóm:** `page_setup`  
**Làm gì:** The templates `drawing_new(template=<name>)` can start from.

Each row: `standard` (ISO/ANSI), `sheet`, `paper`, `layout` (the sheet tab's
name), `layer_set` (mech / pid / iso13567), `dimstyle` / `textstyle`
(ISO-25 / ISOCP or ANSI / ROMANS), `scale`, `title_block` (the ISO 5457 A3
frame, A3 sheets only), the `settings` applied, and `files.dxf` /
`files.dwt` with `present` flags — the `.dwt` twins exist only once built
on a live AutoCAD (`scripts/smoke_settings_com.py --build-dwt`). Never
refuses; it reads a catalogue.

**Dùng khi nào:** Khi thiết lập khổ giấy, máy in, tỷ lệ và cấu hình xuất bản.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `drawing_template_save`

**Nhóm:** `page_setup`  
**Làm gì:** AutoCAD's SAVEAS → Drawing Template, on both engines.

Live AutoCAD writes a real `.dwt` (`SaveAs(path, ac2018_Template)`) and
puts `description` into the template's summary Comments; the active
document is rebound to the new file, as SAVEAS does. Headlessly a `.dxf`
template is written — `drawing_new(template=<path>)` opens it — and a
`.dwt` request is refused with capability `dwt_write` (the message names
the DXF route and the COM route); a description is reported
`description_written: false` because DXF has nowhere to keep it. Any other
suffix, and any path outside the allowed directories, is refused before
a byte is written.

Pack: core · lean: no (`drawing_save_as` is not lean either).

**Dùng khi nào:** Khi thiết lập khổ giấy, máy in, tỷ lệ và cấu hình xuất bản.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `path` | `string` | có | `—` | Destination .dwt (live AutoCAD) or .dxf (either engine). |
| `name` | `any` | không | `None` | Template name for the report (default: the file stem). |
| `description` | `any` | không | `None` | Template description → DWT summary Comments on the live engine. |

**Ví dụ gọi**

```json
{
  "path": "D:\\DuAn\\drawing.dwg",
  "name": null,
  "description": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `drawing_topology_check`

**Nhóm:** `understanding`  
**Làm gì:** Topology of a line network (spec §11): dangling ends, near misses (end to end and
end to line within `gap`) and interior crossings (two lines of one layer crossing
away from their ends). Never modifies the drawing.

An end that touches another network line, any curve on another layer (a tank
outline) or the box of any block reference (a valve, a pump) is connected. Arcs
and bulged polyline segments are measured as true arcs; arcs are not tested for
crossings. The default layers come with their classification as evidence.

Refused before any work: a `path` that does not exist or cannot be read, a
`layers` entry that is not a layer of the drawing (the drawing's layers named),
no layer classified as a network layer when `layers` is omitted (name them),
a non-positive `tol` or `gap`, and a `gap` that does not exceed `tol`.

**Dùng khi nào:** Khi cần LLM hiểu cấu trúc, ngữ cảnh hoặc nội dung bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `layers` | `any` | không | `None` | Layers to check; default: every layer the vocabulary classifies as piping or electrical with confidence >= 0.9. |
| `path` | `any` | không | `None` | A DXF to check instead of the current document; it is read, never opened or modified. |
| `gap` | `any` | không | `None` | Two ends, or an end and a line, closer than this without touching are a near miss; default 0.2 % of the network's diagonal (never under 10 x tol). |
| `tol` | `number` | không | `0.01` | Within this distance two ends are joined. |
| `limit` | `integer` | không | `200` | Rows kept per list; counts are complete. |

**Ví dụ gọi**

```json
{
  "layers": null,
  "path": null,
  "gap": null,
  "tol": 0.01,
  "limit": 200
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `drawing_understand`

**Nhóm:** `understanding`  
**Làm gì:** One report on a drawing somebody else made, every claim with its evidence
and a confidence. Never modifies the drawing: a file is read as it is, and
the current document through a snapshot (headless: the document in memory;
live: a `Document.Export` DXF copy in a temporary folder, deleted after).
An xref's own entities are not read - the host drawing is.

- `units`: `$INSUNITS` as declared against the unit the geometry implies
  (text heights, wall thickness, door swings, labelled room areas, overall
  size - each item with its median and its value under every candidate
  unit). A disagreement is a warning with the numbers, never a silent
  correction.
- `extents`: declared, computed and robust boxes and the `outliers` that
  stretch them, farthest first, by handle.
- `clusters`: separate bodies of model-space content (plan copies, sheets,
  details), each with its box, entity count, commonest layers and tallest
  labels.
- `layers`: entity count, drawn length (and metres in the inferred unit)
  and the discipline / service each most likely carries - the vocabulary's
  confidence (0.9) for a name keyword, 0.6 when most texts on the layer
  agree, 0.4 when fewer do.
- `equipment_tags` (a tag found more than once is `ambiguous`), `rooms`
  (room labels in five languages, each with the wall-layer face it sits in
  and its measured area), `languages` (Latin / Turkish / Cyrillic character
  classes), `blocks` (named / anonymous, kinds by name), `layouts`,
  `title_block` and `warnings`.

Refused before anything is read: a `path` that does not exist, a DXF over
`MAX_DXF_BYTES` (the refusal names the size and the variable), and a file
the engine cannot parse (a DWG headlessly: ezdxf reads DXF only).

**Dùng khi nào:** Khi cần LLM hiểu cấu trúc, ngữ cảnh hoặc nội dung bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `path` | `any` | không | `None` | DXF file to read (a DWG only on a live seat); omitted: the current document. |

**Ví dụ gọi**

```json
{
  "path": null
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `drawing_undo`

**Nhóm:** `drawing`  
**Làm gì:** Undo the last drawing operation.

On the live COM backend this is AutoCAD's own undo. The headless backend has
no journal, so a step is a full DXF snapshot and history is **off by
default** — set `EZDXF_UNDO_DEPTH` to the number of steps you want. Measured
cost of switching it on: 37x on entity creation (0.18 -> 6.65 ms per call).
For a single checkpoint around a risky sequence, `transaction_begin` /
`transaction_rollback` is far cheaper.

Drawing something after an undo discards the redo branch, as in AutoCAD.

**Dùng khi nào:** Khi mở, lưu, đóng, xuất hoặc kiểm tra trạng thái bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_array_polar`

**Nhóm:** `entity_modification`  
**Làm gì:** Create a polar (circular) array of copies around a center point.

`count` is unbounded, so the same result-shaping applies as for the
rectangular array: fields=["handle"] when the geometry is already known.

**Dùng khi nào:** Khi cần sửa, di chuyển, xoay, scale hoặc biến đổi đối tượng.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Entity handle to array |
| `count` | `integer` | có | `—` | Total number of items in the array |
| `fill_angle` | `number` | có | `—` | Total angle to fill in degrees (360 for full circle) |
| `center_x` | `number` | có | `—` | Array center X |
| `center_y` | `number` | có | `—` | Array center Y |
| `fields` | `any` | không | `None` | Project to these fields, in this order (e.g. ['handle','type','layer']); 'properties.<key>' reaches one nested value. Omit for the full record; an unknown name errors and lists the valid ones. |
| `compact` | `boolean` | không | `False` | Return a columnar {fields, rows, count, offset, total, truncated, next_offset} envelope instead of dicts: much cheaper per row, and the only shape that reports truncation. |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "count": 1,
  "fill_angle": 1.0,
  "center_x": 1.0,
  "center_y": 1.0,
  "fields": null,
  "compact": false
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_array_rectangular`

**Nhóm:** `entity_modification`  
**Làm gì:** Create a rectangular array of copies. Returns info of all created copies.

rows x cols is unbounded, so this is a result-heavy tool despite being a
create: a 40x40 grid hands back 1600 full records. fields=["handle"] is
usually all a caller needs from it.

**Dùng khi nào:** Khi cần sửa, di chuyển, xoay, scale hoặc biến đổi đối tượng.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Entity handle to array |
| `rows` | `integer` | có | `—` | Number of rows |
| `cols` | `integer` | có | `—` | Number of columns |
| `row_spacing` | `number` | có | `—` | Spacing between rows (Y direction) |
| `col_spacing` | `number` | có | `—` | Spacing between columns (X direction) |
| `fields` | `any` | không | `None` | Project to these fields, in this order (e.g. ['handle','type','layer']); 'properties.<key>' reaches one nested value. Omit for the full record; an unknown name errors and lists the valid ones. |
| `compact` | `boolean` | không | `False` | Return a columnar {fields, rows, count, offset, total, truncated, next_offset} envelope instead of dicts: much cheaper per row, and the only shape that reports truncation. |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "rows": 1,
  "cols": 1,
  "row_spacing": 1.0,
  "col_spacing": 1.0,
  "fields": null,
  "compact": false
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_batch_create`

**Nhóm:** `batch`  
**Làm gì:** Create multiple entities in a single call for better performance.

Each entity dict must have a 'type' key and the parameters for that type.
Example: [{"type": "line", "x1": 0, "y1": 0, "x2": 100, "y2": 0}, {"type": "circle", "cx": 50, "cy": 50, "radius": 25}]

Denser than cad_batch for many entities of the same kind (no per-step tool
name), and usable as one step *of* a cad_batch. Use cad_batch when the calls
differ, must be ordered, or must feed each other.

**Dùng khi nào:** Khi cần xử lý nhiều bản vẽ hoặc nhiều đối tượng trong một lượt.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `entities` | `array<object>` | có | `—` | List of entity definitions. Each dict must have 'type' and type-specific params. Types: line, circle, arc, polyline, rectangle, text, point |

**Ví dụ gọi**

```json
{
  "entities": []
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_batch_modify`

**Nhóm:** `batch`  
**Làm gì:** Apply multiple modifications in a single call.

Example: [{"handle": "1A", "action": "move", "dx": 10, "dy": 20}, {"handle": "2B", "action": "delete"}]

Covers move/rotate/scale/delete/set_properties only. For anything else, for
ordering, or to feed one step's result into the next, use cad_batch.

**Dùng khi nào:** Khi cần xử lý nhiều bản vẽ hoặc nhiều đối tượng trong một lượt.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `operations` | `array<object>` | có | `—` | List of operations. Each dict: {handle, action, ...params}. Actions: move(dx,dy), rotate(base_x,base_y,angle_deg), scale(base_x,base_y,factor), delete, set_properties(layer,color,...) |

**Ví dụ gọi**

```json
{
  "operations": []
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_chamfer`

**Nhóm:** `corner_ops`  
**Làm gì:** Bevel a corner with a chamfer line. Returns info on the new chamfer LINE.
V1 supports LINE+LINE only.

**Dùng khi nào:** Khi cần dùng chức năng `entity_chamfer` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle1` | `string` | có | `—` | First entity handle |
| `handle2` | `string` | có | `—` | Second entity handle |
| `dist1` | `number` | có | `—` | Chamfer distance along first line |
| `dist2` | `any` | không | `None` | Chamfer distance along second line (None = symmetric, dist2=dist1) |
| `trim` | `boolean` | không | `True` | If true, trim source entities to the tangent points (AutoCAD default) |

**Ví dụ gọi**

```json
{
  "handle1": "A1B2",
  "handle2": "A1B2",
  "dist1": 1.0,
  "dist2": null,
  "trim": true
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_change_space`

**Nhóm:** `layouts`  
**Làm gì:** AutoCAD's CHSPACE: move entities across spaces, rescaled by the viewport.

Geometry is transformed by the viewport's own matrix so it stays the same
size on screen — a move without that transform would leave a 100 mm feature
as 100 mm of paper inside a 1:2 viewport.

Refused per entity for dimensions (unless `freeze_dimensions`), ACIS solids,
tables and proxies, viewports, and entities already in the target space;
refused outright for a twisted or non-plan viewport. Entities that end up
outside the viewport or off the sheet are moved and flagged, not refused.

**Dùng khi nào:** Khi quản lý layout, viewport và không gian giấy.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handles` | `array<string>` | có | `—` | Entity handles to move. |
| `viewport_handle` | `string` | có | `—` | Viewport that defines the model-to-paper mapping. |
| `direction` | `string` | không | `to_paper` | to_paper (model -> sheet) or to_model (sheet -> model). |
| `freeze_dimensions` | `boolean` | không | `False` | Bake each dimension's current measurement into its text before scaling. |

**Ví dụ gọi**

```json
{
  "handles": [],
  "viewport_handle": "A1B2",
  "direction": "to_paper",
  "freeze_dimensions": false
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_copy`

**Nhóm:** `entity_modification`  
**Làm gì:** Copy an entity and move the copy by (dx, dy, dz). Returns info of the new copy.

**Dùng khi nào:** Khi cần sửa, di chuyển, xoay, scale hoặc biến đổi đối tượng.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Entity handle to copy |
| `dx` | `number` | có | `—` | X displacement for the copy |
| `dy` | `number` | có | `—` | Y displacement for the copy |
| `dz` | `number` | không | `0.0` | Z displacement |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "dx": 1.0,
  "dy": 1.0,
  "dz": 0.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_create_arc`

**Nhóm:** `entity_creation`  
**Làm gì:** Create a circular arc. Angles are in degrees, measured counter-clockwise from the positive X axis.

**Dùng khi nào:** Khi cần vẽ thêm đối tượng hình học vào bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `cx` | `number` | có | `—` | Center X |
| `cy` | `number` | có | `—` | Center Y |
| `radius` | `number` | có | `—` | Arc radius |
| `start_angle` | `number` | có | `—` | Start angle in degrees (0 = right, CCW positive) |
| `end_angle` | `number` | có | `—` | End angle in degrees |
| `layer` | `any` | không | `None` | Layer name |
| `color` | `any` | không | `None` | ACI color code |

**Ví dụ gọi**

```json
{
  "cx": 1.0,
  "cy": 1.0,
  "radius": 1.0,
  "start_angle": 1.0,
  "end_angle": 1.0,
  "layer": null,
  "color": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_create_block_ref`

**Nhóm:** `blocks`  
**Làm gì:** Insert a block reference (instance of an existing block definition).

Refused before any write, on both engines: a name that is not a block
definition in this drawing (`block 'X' is not defined` — check
`block_list`), a layout block (`*Model_Space` / `*Paper_Space`, a
reference cycle) and a non-string name. The same gate as `block_insert`;
this tool is the no-attributes form.

**Dùng khi nào:** Khi tạo, chèn, đọc hoặc quản lý block và block reference.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Block definition name (must exist in drawing) |
| `x` | `number` | có | `—` | Insertion X |
| `y` | `number` | có | `—` | Insertion Y |
| `scale_x` | `number` | không | `1.0` | X scale factor |
| `scale_y` | `number` | không | `1.0` | Y scale factor |
| `rotation` | `number` | không | `0.0` | Rotation angle in degrees |
| `layer` | `any` | không | `None` | Layer name |

**Ví dụ gọi**

```json
{
  "name": "example",
  "x": 1.0,
  "y": 1.0,
  "scale_x": 1.0,
  "scale_y": 1.0,
  "rotation": 0.0,
  "layer": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_create_circle`

**Nhóm:** `entity_creation`  
**Làm gì:** Create a circle at (cx, cy) with given radius.

**Dùng khi nào:** Khi cần vẽ thêm đối tượng hình học vào bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `cx` | `number` | có | `—` | Center X |
| `cy` | `number` | có | `—` | Center Y |
| `radius` | `number` | có | `—` | Circle radius |
| `layer` | `any` | không | `None` | Layer name |
| `color` | `any` | không | `None` | ACI color code |

**Ví dụ gọi**

```json
{
  "cx": 1.0,
  "cy": 1.0,
  "radius": 1.0,
  "layer": null,
  "color": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_create_ellipse`

**Nhóm:** `entity_creation`  
**Làm gì:** Create an ellipse. major_x/major_y define the major axis vector from the center.

**Dùng khi nào:** Khi cần vẽ thêm đối tượng hình học vào bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `cx` | `number` | có | `—` | Center X |
| `cy` | `number` | có | `—` | Center Y |
| `major_x` | `number` | có | `—` | Major axis endpoint X (relative to center) |
| `major_y` | `number` | có | `—` | Major axis endpoint Y (relative to center) |
| `ratio` | `number` | không | `0.5` | Minor-to-major axis ratio (0 < ratio ≤ 1) |
| `layer` | `any` | không | `None` | Layer name |
| `color` | `any` | không | `None` | ACI color code |

**Ví dụ gọi**

```json
{
  "cx": 1.0,
  "cy": 1.0,
  "major_x": 1.0,
  "major_y": 1.0,
  "ratio": 0.5,
  "layer": null,
  "color": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_create_hatch`

**Nhóm:** `entity_creation`  
**Làm gì:** Create a hatch fill pattern inside a closed boundary polygon.

**Dùng khi nào:** Khi cần vẽ thêm đối tượng hình học vào bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `pattern` | `string` | có | `—` | Hatch pattern name: SOLID, ANSI31, ANSI32, STEEL, GRAVEL, etc. |
| `boundary_points` | `array<array>` | có | `—` | Closed boundary as list of [x, y] points |
| `scale` | `number` | không | `1.0` | Pattern scale factor |
| `angle` | `number` | không | `0.0` | Pattern rotation angle in degrees |
| `layer` | `any` | không | `None` | Layer name |
| `color` | `any` | không | `None` | ACI color code |

**Ví dụ gọi**

```json
{
  "pattern": "example",
  "boundary_points": [],
  "scale": 1.0,
  "angle": 0.0,
  "layer": null,
  "color": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_create_line`

**Nhóm:** `entity_creation`  
**Làm gì:** Create a line from (x1,y1) to (x2,y2). Returns entity info with handle.

**Dùng khi nào:** Khi cần vẽ thêm đối tượng hình học vào bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `x1` | `number` | có | `—` | Start X coordinate |
| `y1` | `number` | có | `—` | Start Y coordinate |
| `x2` | `number` | có | `—` | End X coordinate |
| `y2` | `number` | có | `—` | End Y coordinate |
| `z1` | `number` | không | `0.0` | Start Z coordinate (default 0) |
| `z2` | `number` | không | `0.0` | End Z coordinate (default 0) |
| `layer` | `any` | không | `None` | Layer name (default: current layer) |
| `color` | `any` | không | `None` | ACI color code 1-255, 256=ByLayer, 0=ByBlock |
| `linetype` | `any` | không | `None` | Linetype name (e.g. 'DASHED', 'CENTER') |

**Ví dụ gọi**

```json
{
  "x1": 1.0,
  "y1": 1.0,
  "x2": 1.0,
  "y2": 1.0,
  "z1": 0.0,
  "z2": 0.0,
  "layer": null,
  "color": null,
  "linetype": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_create_mtext`

**Nhóm:** `entity_creation`  
**Làm gì:** Create a multi-line text entity (MTEXT) with word-wrap at the specified width.

**Dùng khi nào:** Khi cần vẽ thêm đối tượng hình học vào bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `text` | `string` | có | `—` | Text content (supports \P for paragraph breaks, {\H...;} for formatting) |
| `x` | `number` | có | `—` | Insertion point X |
| `y` | `number` | có | `—` | Insertion point Y |
| `width` | `number` | không | `100.0` | Text box width in drawing units |
| `height` | `number` | không | `2.5` | Character height in drawing units |
| `rotation` | `number` | không | `0.0` | Rotation in degrees, CCW from +X |
| `layer` | `any` | không | `None` | Layer name |
| `color` | `any` | không | `None` | ACI color code |

**Ví dụ gọi**

```json
{
  "text": "example",
  "x": 1.0,
  "y": 1.0,
  "width": 100.0,
  "height": 2.5,
  "rotation": 0.0,
  "layer": null,
  "color": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_create_point`

**Nhóm:** `entity_creation`  
**Làm gì:** Create a point marker entity at (x, y).

**Dùng khi nào:** Khi cần vẽ thêm đối tượng hình học vào bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `x` | `number` | có | `—` | Point X coordinate |
| `y` | `number` | có | `—` | Point Y coordinate |
| `layer` | `any` | không | `None` | Layer name |
| `color` | `any` | không | `None` | ACI color code |

**Ví dụ gọi**

```json
{
  "x": 1.0,
  "y": 1.0,
  "layer": null,
  "color": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_create_polyline`

**Nhóm:** `entity_creation`  
**Làm gì:** Create a lightweight 2D polyline through the given points.

Example: points=[[0,0],[100,0],[100,100],[0,100]], closed=true → rectangle

**Dùng khi nào:** Khi cần vẽ thêm đối tượng hình học vào bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `points` | `array<array>` | có | `—` | List of [x, y] coordinate pairs |
| `closed` | `boolean` | không | `False` | Whether to close the polyline |
| `layer` | `any` | không | `None` | Layer name |
| `color` | `any` | không | `None` | ACI color code |

**Ví dụ gọi**

```json
{
  "points": [],
  "closed": false,
  "layer": null,
  "color": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_create_rectangle`

**Nhóm:** `entity_creation`  
**Làm gì:** Create a closed rectangular polyline between two corner points.

Convenience wrapper around entity_create_polyline.

**Dùng khi nào:** Khi cần vẽ thêm đối tượng hình học vào bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `x1` | `number` | có | `—` | First corner X |
| `y1` | `number` | có | `—` | First corner Y |
| `x2` | `number` | có | `—` | Opposite corner X |
| `y2` | `number` | có | `—` | Opposite corner Y |
| `layer` | `any` | không | `None` | Layer name |
| `color` | `any` | không | `None` | ACI color code |

**Ví dụ gọi**

```json
{
  "x1": 1.0,
  "y1": 1.0,
  "x2": 1.0,
  "y2": 1.0,
  "layer": null,
  "color": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_create_revcloud`

**Nhóm:** `entity_creation`  
**Làm gì:** Draw a revision cloud: a polyline whose every segment carries an arc.

A `segment_length` longer than the shortest edge is refused — the result
would carry no arcs at all and would be a plain polyline reported as a
cloud.

**Dùng khi nào:** Khi cần vẽ thêm đối tượng hình học vào bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `points` | `array<array>` | có | `—` | Path corners as [[x, y], ...]. |
| `segment_length` | `number` | có | `—` | Approximate arc length of each cloud bump, in drawing units. |
| `layer` | `string` | không | `` | Target layer. Empty uses the current layer. |
| `closed` | `boolean` | không | `True` | Close the path back to the first point. |

**Ví dụ gọi**

```json
{
  "points": [],
  "segment_length": 1.0,
  "layer": "",
  "closed": true
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_create_spline`

**Nhóm:** `entity_creation`  
**Làm gì:** Create a NURBS spline curve passing through the specified fit points.

**Dùng khi nào:** Khi cần vẽ thêm đối tượng hình học vào bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `fit_points` | `array<array>` | có | `—` | List of [x, y] fit points the spline passes through |
| `layer` | `any` | không | `None` | Layer name |
| `color` | `any` | không | `None` | ACI color code |

**Ví dụ gọi**

```json
{
  "fit_points": [],
  "layer": null,
  "color": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_create_table`

**Nhóm:** `entity_creation`  
**Làm gì:** Create a native COM table or an explicitly-labelled ezdxf composite table.

**Dùng khi nào:** Khi cần vẽ thêm đối tượng hình học vào bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `x` | `number` | có | `—` | Top-left X coordinate |
| `y` | `number` | có | `—` | Top-left Y coordinate |
| `rows` | `array<array>` | có | `—` | Data rows; every row must have the same length |
| `headers` | `any` | không | `None` | Optional column header row |
| `column_widths` | `any` | không | `None` | Optional explicit widths per column |
| `row_height` | `number` | không | `7.0` | — |
| `text_height` | `number` | không | `2.5` | — |
| `title` | `any` | không | `None` | Optional title row |
| `layer` | `string` | không | `TEXT` | Target layer |

**Ví dụ gọi**

```json
{
  "x": 1.0,
  "y": 1.0,
  "rows": [],
  "headers": null,
  "column_widths": null,
  "row_height": 7.0,
  "text_height": 2.5,
  "title": null,
  "layer": "TEXT"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_create_text`

**Nhóm:** `entity_creation`  
**Làm gì:** Create a single-line text entity (DTEXT/TEXT).

**Dùng khi nào:** Khi cần vẽ thêm đối tượng hình học vào bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `text` | `string` | có | `—` | Text content to display |
| `x` | `number` | có | `—` | Insertion point X |
| `y` | `number` | có | `—` | Insertion point Y |
| `height` | `number` | không | `2.5` | Text height in drawing units |
| `rotation` | `number` | không | `0.0` | Rotation angle in degrees |
| `layer` | `any` | không | `None` | Layer name |
| `color` | `any` | không | `None` | ACI color code |

**Ví dụ gọi**

```json
{
  "text": "example",
  "x": 1.0,
  "y": 1.0,
  "height": 2.5,
  "rotation": 0.0,
  "layer": null,
  "color": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_create_wipeout`

**Nhóm:** `entity_creation`  
**Làm gì:** Create a WIPEOUT that hides drawing content behind its outline.

Refuses fewer than three points: a zero-area mask hides nothing while
reporting success.

**Dùng khi nào:** Khi cần vẽ thêm đối tượng hình học vào bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `points` | `array<array>` | có | `—` | Closed polygon as [[x, y], ...]; at least 3 points. |
| `layer` | `string` | không | `` | Target layer. Empty uses the current layer. |

**Ví dụ gọi**

```json
{
  "points": [],
  "layer": ""
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_delete`

**Nhóm:** `entity_modification`  
**Làm gì:** Permanently delete an entity by its handle.

**Dùng khi nào:** Khi cần sửa, di chuyển, xoay, scale hoặc biến đổi đối tượng.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Entity handle to delete |

**Ví dụ gọi**

```json
{
  "handle": "A1B2"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_delete_many`

**Nhóm:** `entity_modification`  
**Làm gì:** Delete multiple entities in one call. Returns count of deleted entities.

**Dùng khi nào:** Khi cần sửa, di chuyển, xoay, scale hoặc biến đổi đối tượng.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handles` | `array<string>` | có | `—` | List of entity handles to delete |

**Ví dụ gọi**

```json
{
  "handles": []
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_edit_geometry`

**Nhóm:** `entity_modification`  
**Làm gì:** Edit the defining geometry of an existing entity in place (no delete/recreate).

CIRCLE: cx/cy/radius · LINE: x1/y1/x2/y2 · ARC: cx/cy/radius/start_angle/end_angle.
Any argument left out is unchanged; the handle is preserved.

**Dùng khi nào:** Khi cần sửa, di chuyển, xoay, scale hoặc biến đổi đối tượng.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Handle of an existing CIRCLE, LINE, or ARC |
| `cx` | `any` | không | `None` | New center X (CIRCLE/ARC) |
| `cy` | `any` | không | `None` | New center Y (CIRCLE/ARC) |
| `radius` | `any` | không | `None` | New radius (CIRCLE/ARC) |
| `x1` | `any` | không | `None` | New start X (LINE) |
| `y1` | `any` | không | `None` | New start Y (LINE) |
| `x2` | `any` | không | `None` | New end X (LINE) |
| `y2` | `any` | không | `None` | New end Y (LINE) |
| `start_angle` | `any` | không | `None` | New start angle in degrees (ARC) |
| `end_angle` | `any` | không | `None` | New end angle in degrees (ARC) |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "cx": null,
  "cy": null,
  "radius": null,
  "x1": null,
  "y1": null,
  "x2": null,
  "y2": null,
  "start_angle": null,
  "end_angle": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_edit_text`

**Nhóm:** `entity_modification`  
**Làm gì:** Edit an existing text label in place — change its content, height, or rotation.

Use this to rename/relabel without deleting and recreating (which would lose
the handle). Works on both TEXT and MTEXT.

**Dùng khi nào:** Khi cần sửa, di chuyển, xoay, scale hoặc biến đổi đối tượng.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Handle of an existing TEXT or MTEXT entity |
| `text` | `any` | không | `None` | New text content (unchanged if omitted) |
| `height` | `any` | không | `None` | New text height (unchanged if omitted) |
| `rotation` | `any` | không | `None` | New rotation in degrees (unchanged if omitted) |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "text": null,
  "height": null,
  "rotation": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_extend`

**Nhóm:** `corner_ops`  
**Làm gì:** Extend `target` to meet `boundary`. If end_x/end_y is None, the target
endpoint nearest the boundary is auto-selected.

V1 supports LINE+LINE only. Raises if the lines are parallel.

**Dùng khi nào:** Khi cần dùng chức năng `entity_extend` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `target_handle` | `string` | có | `—` | Handle of the line being extended |
| `boundary_handle` | `string` | có | `—` | Handle of the boundary line |
| `end_x` | `any` | không | `None` | X of a point near the endpoint to extend (None = auto) |
| `end_y` | `any` | không | `None` | Y of a point near the endpoint to extend (None = auto) |

**Ví dụ gọi**

```json
{
  "target_handle": "D:\\DuAn\\drawing.dwg",
  "boundary_handle": "A1B2",
  "end_x": null,
  "end_y": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_fillet`

**Nhóm:** `corner_ops`  
**Làm gì:** Round a corner with a tangent arc. Returns info on the new ARC entity
(or the first source line for radius=0). V1 supports LINE+LINE only.

**Dùng khi nào:** Khi cần dùng chức năng `entity_fillet` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle1` | `string` | có | `—` | First entity handle |
| `handle2` | `string` | có | `—` | Second entity handle |
| `radius` | `number` | có | `—` | Fillet radius (>= 0; 0 = sharp corner / corner-merge) |
| `trim` | `boolean` | không | `True` | If true, trim source entities to the tangent points (AutoCAD default) |

**Ví dụ gọi**

```json
{
  "handle1": "A1B2",
  "handle2": "A1B2",
  "radius": 1.0,
  "trim": true
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_get`

**Nhóm:** `entity_query`  
**Làm gì:** Get all properties of a specific entity by its handle.

**Dùng khi nào:** Khi cần tìm và đọc thuộc tính đối tượng theo handle hoặc điều kiện.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Entity handle |

**Ví dụ gọi**

```json
{
  "handle": "A1B2"
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `entity_get_xdata`

**Nhóm:** `entity_query`  
**Làm gì:** Extended entity data as {app: [values]}. An app with no XDATA is simply absent.

**Dùng khi nào:** Khi cần tìm và đọc thuộc tính đối tượng theo handle hoặc điều kiện.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Entity handle |
| `app_name` | `any` | không | `None` | Registered application name; omit for every app |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "app_name": null
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `entity_list`

**Nhóm:** `entity_query`  
**Làm gì:** List entities in the drawing with optional type and layer filters.

Returns handle, type, layer, color, and type-specific properties.
Use handles with entity_get, entity_move, entity_delete, etc.

This is the most expensive result on the server — the full record runs
~250 characters per entity, and `properties.bounding_box` alone is about a
third of it. When all you need is handles, say so::

    entity_list(layer_filter="GEOMETRY", fields=["handle", "type"], compact=True)

Paging honesty: a plain list has nowhere to say that more entities followed
the page, so `compact=True` is the only mode that reports `total`,
`truncated` and `next_offset` — all measured against the same filters.

**Dùng khi nào:** Khi cần tìm và đọc thuộc tính đối tượng theo handle hoặc điều kiện.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `type_filter` | `any` | không | `None` | Filter by entity type: LINE, CIRCLE, ARC, LWPOLYLINE, TEXT, MTEXT, INSERT, HATCH, etc. |
| `layer_filter` | `any` | không | `None` | Filter by layer name |
| `limit` | `integer` | không | `100` | Maximum entities to return |
| `offset` | `integer` | không | `0` | Number of entities to skip |
| `fields` | `any` | không | `None` | Project to these fields, in this order (e.g. ['handle','type','layer']); 'properties.<key>' reaches one nested value. Omit for the full record; an unknown name errors and lists the valid ones. |
| `compact` | `boolean` | không | `False` | Return a columnar {fields, rows, count, offset, total, truncated, next_offset} envelope instead of dicts: much cheaper per row, and the only shape that reports truncation. |

**Ví dụ gọi**

```json
{
  "type_filter": null,
  "layer_filter": null,
  "limit": 100,
  "offset": 0,
  "fields": null,
  "compact": false
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `entity_mirror`

**Nhóm:** `entity_modification`  
**Làm gì:** Mirror an entity across a line defined by two points. Returns the mirrored copy.

**Dùng khi nào:** Khi cần sửa, di chuyển, xoay, scale hoặc biến đổi đối tượng.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Entity handle |
| `x1` | `number` | có | `—` | Mirror line first point X |
| `y1` | `number` | có | `—` | Mirror line first point Y |
| `x2` | `number` | có | `—` | Mirror line second point X |
| `y2` | `number` | có | `—` | Mirror line second point Y |
| `delete_original` | `boolean` | không | `False` | Delete original after mirroring |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "x1": 1.0,
  "y1": 1.0,
  "x2": 1.0,
  "y2": 1.0,
  "delete_original": false
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_move`

**Nhóm:** `entity_modification`  
**Làm gì:** Move an entity by the specified displacement vector (dx, dy, dz).

**Dùng khi nào:** Khi cần sửa, di chuyển, xoay, scale hoặc biến đổi đối tượng.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Entity handle (hex string from entity_list or entity_create_*) |
| `dx` | `number` | có | `—` | X displacement |
| `dy` | `number` | có | `—` | Y displacement |
| `dz` | `number` | không | `0.0` | Z displacement |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "dx": 1.0,
  "dy": 1.0,
  "dz": 0.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_offset`

**Nhóm:** `entity_modification`  
**Làm gì:** Create a parallel copy of a line, circle, or polyline at the given distance.

**Dùng khi nào:** Khi cần sửa, di chuyển, xoay, scale hoặc biến đổi đối tượng.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Entity handle (line, circle, or polyline) |
| `distance` | `number` | có | `—` | Offset distance (positive = outward/right) |
| `side_x` | `any` | không | `None` | X coordinate of a point on the offset side (optional) |
| `side_y` | `any` | không | `None` | Y coordinate of a point on the offset side (optional) |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "distance": 1.0,
  "side_x": null,
  "side_y": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_rotate`

**Nhóm:** `entity_modification`  
**Làm gì:** Rotate an entity around a base point by the specified angle.

**Dùng khi nào:** Khi cần sửa, di chuyển, xoay, scale hoặc biến đổi đối tượng.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Entity handle |
| `base_x` | `number` | có | `—` | Rotation base point X |
| `base_y` | `number` | có | `—` | Rotation base point Y |
| `angle_deg` | `number` | có | `—` | Rotation angle in degrees (positive = counter-clockwise) |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "base_x": 1.0,
  "base_y": 1.0,
  "angle_deg": 1.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_scale`

**Nhóm:** `entity_modification`  
**Làm gì:** Scale an entity uniformly from a base point.

**Dùng khi nào:** Khi cần sửa, di chuyển, xoay, scale hoặc biến đổi đối tượng.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Entity handle |
| `base_x` | `number` | có | `—` | Scale base point X |
| `base_y` | `number` | có | `—` | Scale base point Y |
| `factor` | `number` | có | `—` | Scale factor (>1 enlarges, <1 shrinks) |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "base_x": 1.0,
  "base_y": 1.0,
  "factor": 1.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_select_smart`

**Nhóm:** `premium`  
**Làm gì:** Select entities by semantic predicate instead of memorising handles.

Uncapped. The usual next step is dimension_auto(handles), so
fields=["handle"] is normally all this needs to return.

**Dùng khi nào:** Khi dùng chức năng nâng cao; kiểm tra capability trước nếu backend không hỗ trợ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `predicate` | `object` | có | `—` | Predicate dict (all keys optional, AND-ed): type (e.g. 'LINE'), layer (name), near ([x,y,radius]), length_range ([min,max], LINE/ARC only), color (ACI int). |
| `fields` | `any` | không | `None` | Project to these fields, in this order (e.g. ['handle','type','layer']); 'properties.<key>' reaches one nested value. Omit for the full record; an unknown name errors and lists the valid ones. |
| `compact` | `boolean` | không | `False` | Return a columnar {fields, rows, count, offset, total, truncated, next_offset} envelope instead of dicts: much cheaper per row, and the only shape that reports truncation. |

**Ví dụ gọi**

```json
{
  "predicate": {},
  "fields": null,
  "compact": false
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `entity_set_properties`

**Nhóm:** `entity_modification`  
**Làm gì:** Change one or more properties of an entity (layer, color, linetype, lineweight, visibility).

**Dùng khi nào:** Khi cần sửa, di chuyển, xoay, scale hoặc biến đổi đối tượng.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Entity handle |
| `layer` | `any` | không | `None` | New layer name |
| `color` | `any` | không | `None` | New ACI color (256=ByLayer, 0=ByBlock, 1-255=specific) |
| `linetype` | `any` | không | `None` | New linetype name (e.g. 'DASHED', 'CENTER', 'ByLayer') |
| `lineweight` | `any` | không | `None` | Lineweight in 0.01mm units (-3=ByLayer, -2=ByBlock) |
| `visible` | `any` | không | `None` | Set entity visibility |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "layer": null,
  "color": null,
  "linetype": null,
  "lineweight": null,
  "visible": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_set_xdata`

**Nhóm:** `entity_modification`  
**Làm gì:** Replace the named app's XDATA on one entity; an empty list removes it.

Limits are AutoCAD's and are enforced before writing: 255 characters per
string and 16 KB per entity.

**Dùng khi nào:** Khi cần sửa, di chuyển, xoay, scale hoặc biến đổi đối tượng.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Entity handle |
| `app_name` | `string` | có | `—` | Registered application name (created if missing) |
| `values` | `array` | có | `—` | Values typed by kind: strings (≤255 chars) → 1000, ints → 1071, floats → 1040, [x,y] → 1010 |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "app_name": "example",
  "values": []
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `entity_trim`

**Nhóm:** `corner_ops`  
**Làm gì:** Trim `target` against `cutter`, keeping the segment containing (keep_x, keep_y).

V1 supports LINE+LINE only. Cutter is treated as an infinite ray (AutoCAD's
default 'implied extend' trim mode). Raises if the lines are parallel.

**Dùng khi nào:** Khi cần dùng chức năng `entity_trim` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `target_handle` | `string` | có | `—` | Handle of the line being trimmed |
| `cutter_handle` | `string` | có | `—` | Handle of the cutting line |
| `keep_x` | `number` | có | `—` | X of a point on the side of the target to KEEP |
| `keep_y` | `number` | có | `—` | Y of a point on the side of the target to KEEP |

**Ví dụ gọi**

```json
{
  "target_handle": "D:\\DuAn\\drawing.dwg",
  "cutter_handle": "A1B2",
  "keep_x": 1.0,
  "keep_y": 1.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `gd_frame`

**Nhóm:** `engineering`  
**Làm gì:** Draw an ISO 1101 feature control frame from LINE + TEXT primitives.

Renders identically on COM and ezdxf. Referenced datums are recorded so the
`gdt` critique focus flags any datum with no matching datum feature.

**Dùng khi nào:** Khi cần kiểm tra hoặc thao tác theo yêu cầu kỹ thuật.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `symbol` | `string` | có | `—` | Geometric characteristic: straightness, flatness, circularity, cylindricity, profile_line, profile_surface, angularity, perpendicularity, parallelism, position, concentricity, symmetry, circular_runout, total_runout. |
| `tolerance` | `number` | có | `—` | Tolerance zone value (mm). |
| `x` | `number` | có | `—` | Frame bottom-left corner X. |
| `y` | `number` | có | `—` | Frame bottom-left corner Y. |
| `datums` | `any` | không | `None` | Ordered datum references, e.g. ['A','B']. Required for orientation/location/runout characteristics. |
| `height` | `number` | không | `5.0` | Frame height (mm); text scales with it. |
| `diameter` | `boolean` | không | `False` | Prefix ⌀ for a cylindrical (diametral) tolerance zone. |
| `modifier` | `any` | không | `None` | Material-condition modifier: M (MMC), L (LMC), S (RFS). |
| `layer` | `any` | không | `None` | Layer (defaults to the active DIM layer). |

**Ví dụ gọi**

```json
{
  "symbol": "example",
  "tolerance": 1.0,
  "x": 1.0,
  "y": 1.0,
  "datums": null,
  "height": 5.0,
  "diameter": false,
  "modifier": null,
  "layer": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `gear_draw_helical_front_view`

**Nhóm:** `engineering`  
**Làm gì:** Deterministic helical gear front view: full involute outline (40 pts/flank),
pitch/base/outer/root circles, helix symbol, optional bore + keyway.

Returns a handle bundle plus 'metadata' for downstream gear_draw_section_aa.

**Dùng khi nào:** Khi cần kiểm tra hoặc thao tác theo yêu cầu kỹ thuật.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `module` | `number` | có | `—` | Module (mm). Pitch radius = module*teeth/2. |
| `teeth` | `integer` | có | `—` | Number of teeth. |
| `helix_angle` | `number` | có | `—` | Helix angle in degrees. |
| `pressure_angle` | `number` | không | `20.0` | Pressure angle (deg). Standard: 20. |
| `hand` | `string` | không | `RH` | Helix hand: 'RH' (right) or 'LH' (left). |
| `center_x` | `number` | không | `0.0` | — |
| `center_y` | `number` | không | `0.0` | — |
| `bore_diameter` | `any` | không | `None` | Optional bore diameter (mm). Adds a centered hole. |
| `keyway_width` | `any` | không | `None` | Keyway width (b). Auto from DIN 6885 if bore set and this is None. |
| `keyway_depth` | `any` | không | `None` | Keyway depth into hub (t2). |

**Ví dụ gọi**

```json
{
  "module": 1.0,
  "teeth": 1,
  "helix_angle": 1.0,
  "pressure_angle": 20.0,
  "hand": "RH",
  "center_x": 0.0,
  "center_y": 0.0,
  "bore_diameter": null,
  "keyway_width": null,
  "keyway_depth": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `gear_draw_section_aa`

**Nhóm:** `engineering`  
**Làm gì:** Deterministic side cross-section of a gear created by gear_draw_*_front_view.
Includes top/bottom/left/right boundaries, bore lines, keyway notch, ANSI31 hatch.

**Dùng khi nào:** Khi cần kiểm tra hoặc thao tác theo yêu cầu kỹ thuật.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `gear_metadata` | `object` | có | `—` | The 'metadata' dict returned by gear_draw_helical_front_view or gear_draw_spur_front_view. |
| `x_offset` | `number` | có | `—` | X position to place the section view. |
| `face_width` | `number` | có | `—` | Gear face width (mm). |

**Ví dụ gọi**

```json
{
  "gear_metadata": {},
  "x_offset": 1.0,
  "face_width": 1.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `gear_draw_spur_front_view`

**Nhóm:** `engineering`  
**Làm gì:** Deterministic spur gear front view (no helix symbol).

**Dùng khi nào:** Khi cần kiểm tra hoặc thao tác theo yêu cầu kỹ thuật.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `module` | `number` | có | `—` | — |
| `teeth` | `integer` | có | `—` | — |
| `pressure_angle` | `number` | không | `20.0` | — |
| `center_x` | `number` | không | `0.0` | — |
| `center_y` | `number` | không | `0.0` | — |
| `bore_diameter` | `any` | không | `None` | — |
| `keyway_width` | `any` | không | `None` | — |
| `keyway_depth` | `any` | không | `None` | — |

**Ví dụ gọi**

```json
{
  "module": 1.0,
  "teeth": 1,
  "pressure_angle": 20.0,
  "center_x": 0.0,
  "center_y": 0.0,
  "bore_diameter": null,
  "keyway_width": null,
  "keyway_depth": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `hatch_add_boundary`

**Nhóm:** `entity_creation`  
**Làm gì:** Add one boundary path built from typed edges - an island inside the hatch.

Typed edges exist because a boundary that only accepts vertex lists
silently straightens every curve it is given. Every edge is validated
before any is written, so a malformed list refuses instead of leaving a
half-built path. Both engines: headlessly the edges become an edge path;
on a live seat each becomes a temporary LINE, true ARC or ELLIPSE appended
as an inner loop and then deleted (a chain of lines becomes one polyline).
A loop that does not close is refused by AutoCAD and nothing is added.

**Dùng khi nào:** Khi cần vẽ thêm đối tượng hình học vào bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Handle of an existing HATCH. |
| `edges` | `array<object>` | có | `—` | Typed edges: {'type':'line','start':[x,y],'end':[x,y]} | {'type':'arc','center':[x,y],'radius':r,'start_angle':a,'end_angle':b,'ccw':true} | {'type':'ellipse','center':[x,y],'major_axis':[x,y],'ratio':r} |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "edges": []
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `hatch_edit`

**Nhóm:** `entity_creation`  
**Làm gì:** Edit an existing hatch in place.

Omitted parameters are left alone — a partial edit that resets the rest is
data loss. `changed` reports which attributes actually moved, so re-setting
a value to what it already was comes back as an empty list rather than a
false positive.

**Dùng khi nào:** Khi cần vẽ thêm đối tượng hình học vào bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Handle of an existing HATCH. |
| `pattern` | `string` | không | `` | New pattern name. Empty leaves it alone. |
| `scale` | `any` | không | `None` | New pattern scale (> 0). |
| `angle` | `any` | không | `None` | New pattern angle in degrees. |
| `color` | `any` | không | `None` | New ACI colour. |
| `style` | `string` | không | `` | Island style: normal, outer or ignore. Empty leaves it alone. |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "pattern": "",
  "scale": null,
  "angle": null,
  "color": null,
  "style": ""
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `hatch_material`

**Nhóm:** `mechanical`  
**Làm gì:** Section-hatch a cut face with the pattern ISO 128-50 gives its material.

Refusals: an unknown material (named, with the full list, before anything
is drawn), neither `boundary` nor `handles` (or both), a boundary with
fewer than three points, and a non-positive `scale`. With `handles` the
loop is chained by `boundary_from_entities`, which the COM engine refuses
(capability `boundary_trace`) - pass `boundary` on a live seat, or run
headlessly. The HATCH layer is created first when the drawing lacks it:
ActiveX refuses an entity on an absent layer and would otherwise leave the
hatch orphaned on layer 0.

The payload states its own accuracy, as `analysis_measure_entity` does:
`area` is the polygon actually hatched, `boundary_area` the exact area of
the chained loop, and `accuracy` is `"exact"` or `"flatten_tolerance"` -
an arc edge reaches `entity_create_hatch` as chords, so a curved cut face
is hatched to within `HATCH_FLATTEN_SAGITTA` of itself rather than being
replaced by its chord polygon. With `handles`, the outline
`boundary_from_entities` draws is scaffolding and is deleted; `traced`
reports its handle and whether the delete succeeded. A loop enclosing no
area is refused instead of writing a HATCH of area 0.0.

**Dùng khi nào:** Khi dựng hoặc kiểm tra bản vẽ cơ khí, chi tiết và dung sai.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `material` | `string` | không | `steel` | Material name; an unknown one is refused with the list. |
| `boundary` | `any` | không | `None` | Closed boundary as [[x, y], ...] — at least three points. |
| `handles` | `any` | không | `None` | Entities to chain into one closed loop instead of a boundary. |
| `scale` | `number` | không | `1.0` | Multiplies the material's own pattern scale. |
| `angle` | `any` | không | `None` | Replaces the material's own pattern angle (degrees) when given. |
| `layer` | `any` | không | `None` | Override the HATCH role layer. |

**Ví dụ gọi**

```json
{
  "material": "steel",
  "boundary": null,
  "handles": null,
  "scale": 1.0,
  "angle": null,
  "layer": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `hatch_set_gradient`

**Nhóm:** `entity_creation`  
**Làm gì:** Fill a hatch with a gradient instead of a pattern.

**Dùng khi nào:** Khi cần vẽ thêm đối tượng hình học vào bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Handle of an existing HATCH. |
| `color1` | `array<integer>` | có | `—` | Start colour as [r, g, b]. |
| `color2` | `array<integer>` | có | `—` | End colour as [r, g, b]. |
| `rotation` | `number` | không | `0.0` | Gradient angle in degrees. |
| `centered` | `number` | không | `0.0` | 0 = one-sided, 1 = centred. |
| `one_color` | `boolean` | không | `False` | Blend color1 towards the background instead of color2. |
| `tint` | `number` | không | `0.0` | Tint value used with one_color (0-1). |
| `name` | `string` | không | `LINEAR` | Gradient name: LINEAR, CYLINDER, CURVED, SPHERICAL, HEMISPHERICAL. |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "color1": [],
  "color2": [],
  "rotation": 0.0,
  "centered": 0.0,
  "one_color": false,
  "tint": 0.0,
  "name": "LINEAR"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `image_attach`

**Nhóm:** `sheet`  
**Làm gì:** Attach a raster underlay at the file's own aspect ratio. Both engines.

`scale` is drawing units per pixel, so the placed size is the image's pixel
size times `scale` and the payload reports both. With `auto_layout=True`,
the server also creates (or reuses) a paper-space layout, applies the
requested paper setup, and creates a viewport that fits the image. This is
important for sheet underlays: attaching an image in Model space alone does
not make it visible on an A1/A0 tab.

Refusals, all before anything is written: a file that does not exist, a file
no image reader can open (named), a non-positive or non-finite scale.

**Dùng khi nào:** Khi tạo và quản lý sheet, title block và hồ sơ phát hành.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `path` | `string` | có | `—` | Full path of the raster image. |
| `x` | `number` | không | `0.0` | Insertion X (WCS). |
| `y` | `number` | không | `0.0` | Insertion Y (WCS). |
| `scale` | `number` | không | `1.0` | Drawing units per pixel: an 800x400 image at 0.1 is 80x40 mm. |
| `rotation` | `number` | không | `0.0` | Rotation in degrees. |
| `auto_layout` | `boolean` | không | `False` | Also create an A1/A0/etc paper-space layout, page setup, and a fit viewport centred on the attached image. |
| `layout` | `string` | không | `` | Layout name when auto_layout is true (default: paper name, e.g. A1). |
| `paper` | `string` | không | `A1` | ISO/ANSI paper when auto_layout is true (default: A1). |
| `orientation` | `string` | không | `landscape` | Paper orientation when auto_layout is true. |

**Ví dụ gọi**

```json
{
  "path": "D:\\DuAn\\drawing.dwg",
  "x": 0.0,
  "y": 0.0,
  "scale": 1.0,
  "rotation": 0.0,
  "auto_layout": false,
  "layout": "",
  "paper": "A1",
  "orientation": "landscape"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `keyway_draw_keyed_bore`

**Nhóm:** `engineering`  
**Làm gì:** Bore + DIN 6885 keyway in front view. Auto-sizes keyway from bore if width/depth omitted.

**Dùng khi nào:** Khi cần kiểm tra hoặc thao tác theo yêu cầu kỹ thuật.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `center_x` | `number` | có | `—` | — |
| `center_y` | `number` | có | `—` | — |
| `bore_diameter` | `number` | có | `—` | — |
| `keyway_width` | `any` | không | `None` | — |
| `keyway_depth` | `any` | không | `None` | — |
| `layer` | `string` | không | `GEOMETRY` | — |

**Ví dụ gọi**

```json
{
  "center_x": 1.0,
  "center_y": 1.0,
  "bore_diameter": 1.0,
  "keyway_width": null,
  "keyway_depth": null,
  "layer": "GEOMETRY"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `keyway_draw_section`

**Nhóm:** `engineering`  
**Làm gì:** Side cross-section view of a keyed bore.

**Dùng khi nào:** Khi cần kiểm tra hoặc thao tác theo yêu cầu kỹ thuật.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `center_x` | `number` | có | `—` | — |
| `center_y` | `number` | có | `—` | — |
| `bore_diameter` | `number` | có | `—` | — |
| `face_width` | `number` | có | `—` | — |
| `keyway_width` | `any` | không | `None` | — |
| `keyway_depth` | `any` | không | `None` | — |

**Ví dụ gọi**

```json
{
  "center_x": 1.0,
  "center_y": 1.0,
  "bore_diameter": 1.0,
  "face_width": 1.0,
  "keyway_width": null,
  "keyway_depth": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `kho_industries`

**Nhóm:** `cadtroly`  
**Làm gì:** Liệt kê danh mục ngành với mã máy và tên tiếng Việt để chọn tiêu chuẩn.

**Dùng khi nào:** Khi cần dùng chức năng `kho_industries` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `kho_rules_export`

**Nhóm:** `cadtroly`  
**Làm gì:** Xuất quy tắc ánh xạ của đơn vị (chỉ quy tắc, không bản vẽ) để chia sẻ.

**Dùng khi nào:** Khi cần dùng chức năng `kho_rules_export` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `kho_rules_import`

**Nhóm:** `cadtroly`  
**Làm gì:** Nhập quy tắc ánh xạ từ nơi khác (ghi đè theo pattern).

**Dùng khi nào:** Khi cần dùng chức năng `kho_rules_import` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `rules` | `array<object>` | có | `—` | — |

**Ví dụ gọi**

```json
{
  "rules": []
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `kho_skill_add`

**Nhóm:** `cadtroly`  
**Làm gì:** Thêm skill do LLM soạn vào kho người dùng; chỉ ghi SKILL.md, không chạy mã.

**Dùng khi nào:** Khi cần dùng chức năng `kho_skill_add` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Tên ASCII kebab-case, ví dụ qa-mep |
| `content` | `string` | có | `—` | Nội dung SKILL.md có YAML frontmatter |
| `overwrite` | `boolean` | không | `False` | Cho phép cập nhật skill do người dùng đã tạo |

**Ví dụ gọi**

```json
{
  "name": "my-project-rule",
  "content": "---\ntitle: Quy tắc dự án\n---\nNội dung hướng dẫn cho LLM.",
  "overwrite": false
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `kho_skill_toggle`

**Nhóm:** `cadtroly`  
**Làm gì:** Bật/tắt một skill.

**Dùng khi nào:** Khi cần dùng chức năng `kho_skill_toggle` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | — |
| `enabled` | `boolean` | có | `—` | — |

**Ví dụ gọi**

```json
{
  "name": "example",
  "enabled": true
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `kho_skills`

**Nhóm:** `cadtroly`  
**Làm gì:** Skill chuyên ngành trong kho/skill (mỗi thư mục một SKILL.md), bật/tắt.

**Dùng khi nào:** Khi cần dùng chức năng `kho_skills` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `kho_standard_add`

**Nhóm:** `cadtroly`  
**Làm gì:** Thêm tiêu chuẩn/rule JSON vào kho người dùng; không ghi vào bộ mặc định.

**Dùng khi nào:** Khi cần dùng chức năng `kho_standard_add` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `standard` | `object` | có | `—` | id, nganh, ten, phien_ban, nguon, hieu_luc và rules |
| `overwrite` | `boolean` | không | `False` | Cho phép cập nhật tiêu chuẩn do người dùng đã thêm |

**Ví dụ gọi**

```json
{
  "industry": "architecture",
  "standard": {
    "code": "TCVN-EXAMPLE",
    "title": "Tiêu chuẩn dự án",
    "source": "internal"
  }
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `kho_standard_delete`

**Nhóm:** `cadtroly`  
**Làm gì:** Xóa tiêu chuẩn do người dùng thêm; tiêu chuẩn mặc định không thể xóa.

**Dùng khi nào:** Khi cần dùng chức năng `kho_standard_delete` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `standard_id` | `string` | có | `—` | — |
| `confirm` | `boolean` | không | `False` | Bắt buộc True để xóa tiêu chuẩn người dùng |

**Ví dụ gọi**

```json
{
  "standard_id": "example",
  "confirm": false
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `kho_standards`

**Nhóm:** `cadtroly`  
**Làm gì:** Liệt kê tiêu chuẩn/rule theo ngành, phiên bản, nguồn và trạng thái duyệt.

**Dùng khi nào:** Khi cần dùng chức năng `kho_standards` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `industry` | `any` | không | `None` | building, structural, fire, mechanical, pid, architecture, civil hoặc bỏ trống |

**Ví dụ gọi**

```json
{
  "industry": "architecture"
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `kho_status`

**Nhóm:** `cadtroly`  
**Làm gì:** Tình trạng kho tri thức, backend AutoCAD, nguồn AI.

**Dùng khi nào:** Khi cần dùng chức năng `kho_status` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `layer_create`

**Nhóm:** `layers`  
**Làm gì:** Create a new layer with specified properties.

**Dùng khi nào:** Khi tạo, đổi tên, bật/tắt, đóng băng hoặc quản lý layer.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | New layer name |
| `color` | `integer` | không | `7` | ACI color code (1=Red, 2=Yellow, 3=Green, 4=Cyan, 5=Blue, 7=White) |
| `linetype` | `string` | không | `Continuous` | Linetype name |
| `lineweight` | `integer` | không | `-3` | Lineweight (-3=ByLayer, 0=0.00mm, 13=0.13mm, 25=0.25mm, 50=0.50mm) |

**Ví dụ gọi**

```json
{
  "name": "example",
  "color": 7,
  "linetype": "Continuous",
  "lineweight": -3
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `layer_delete`

**Nhóm:** `layers`  
**Làm gì:** Delete a layer. The layer must have no entities. Layer '0' cannot be deleted.

**Dùng khi nào:** Khi tạo, đổi tên, bật/tắt, đóng băng hoặc quản lý layer.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Layer name to delete (layer must be empty) |

**Ví dụ gọi**

```json
{
  "name": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `layer_freeze`

**Nhóm:** `layers`  
**Làm gì:** Freeze a layer (makes it invisible and unselectable, faster regeneration).

**Dùng khi nào:** Khi tạo, đổi tên, bật/tắt, đóng băng hoặc quản lý layer.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Layer name to freeze |

**Ví dụ gọi**

```json
{
  "name": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `layer_hide`

**Nhóm:** `layers`  
**Làm gì:** Turn off a layer (entities invisible but still processed in regeneration).

**Dùng khi nào:** Khi tạo, đổi tên, bật/tắt, đóng băng hoặc quản lý layer.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Layer name to turn off |

**Ví dụ gọi**

```json
{
  "name": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `layer_isolate`

**Nhóm:** `layers`  
**Làm gì:** Hide all layers except the specified one (layer isolation).

**Dùng khi nào:** Khi tạo, đổi tên, bật/tắt, đóng băng hoặc quản lý layer.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Layer name to keep visible (all others will be hidden) |

**Ví dụ gọi**

```json
{
  "name": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `layer_list`

**Nhóm:** `layers`  
**Làm gì:** List all layers with their properties (color, linetype, frozen, locked, visibility).

Never truncated — a drawing's whole layer table is returned — so a compact
envelope here always reports truncated=false.

**Dùng khi nào:** Khi tạo, đổi tên, bật/tắt, đóng băng hoặc quản lý layer.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `fields` | `any` | không | `None` | Project to these fields, in this order (e.g. ['handle','type','layer']); 'properties.<key>' reaches one nested value. Omit for the full record; an unknown name errors and lists the valid ones. |
| `compact` | `boolean` | không | `False` | Return a columnar {fields, rows, count, offset, total, truncated, next_offset} envelope instead of dicts: much cheaper per row, and the only shape that reports truncation. |

**Ví dụ gọi**

```json
{
  "fields": null,
  "compact": false
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `layer_lock`

**Nhóm:** `layers`  
**Làm gì:** Lock a layer (entities visible but cannot be selected or modified).

**Dùng khi nào:** Khi tạo, đổi tên, bật/tắt, đóng băng hoặc quản lý layer.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Layer name to lock |

**Ví dụ gọi**

```json
{
  "name": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `layer_modify`

**Nhóm:** `layers`  
**Làm gì:** Modify an existing layer's color, linetype, and/or lineweight.

**Dùng khi nào:** Khi tạo, đổi tên, bật/tắt, đóng băng hoặc quản lý layer.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Layer name to modify |
| `color` | `any` | không | `None` | New ACI color code |
| `linetype` | `any` | không | `None` | New linetype name |
| `lineweight` | `any` | không | `None` | New lineweight value |

**Ví dụ gọi**

```json
{
  "name": "example",
  "color": null,
  "linetype": null,
  "lineweight": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `layer_set_current`

**Nhóm:** `layers`  
**Làm gì:** Set the active/current layer for new entities.

**Dùng khi nào:** Khi tạo, đổi tên, bật/tắt, đóng băng hoặc quản lý layer.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Layer name to set as current |

**Ví dụ gọi**

```json
{
  "name": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `layer_show`

**Nhóm:** `layers`  
**Làm gì:** Turn on a layer that was previously turned off.

**Dùng khi nào:** Khi tạo, đổi tên, bật/tắt, đóng băng hoặc quản lý layer.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Layer name to turn on |

**Ví dụ gọi**

```json
{
  "name": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `layer_state_delete`

**Nhóm:** `environment`  
**Làm gì:** Remove the named state's XRECORD. Layers themselves are untouched.
Refusal: an unknown name (lists the saved ones). Pack: settings · lean: no.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | A name from layer_state_list |

**Ví dụ gọi**

```json
{
  "name": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `layer_state_list`

**Nhóm:** `environment`  
**Làm gì:** Every state under `ACADMCP_LAYERSTATES` with its description and layer
count. These are the server's portable states, not AutoCAD Layer States
Manager entries. No refusals. Pack: settings · lean: no.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `layer_state_restore`

**Nhóm:** `environment`  
**Làm gì:** Apply a saved state to the layers that still exist.

`missing_layers` (in the state, not in the drawing) are skipped, never
created; `new_layers` (in the drawing, not in the state) are untouched;
`applied` says how many layers and which properties moved. Refusals: an
unknown state name (lists the saved ones), a property outside the eight
(names the index). Live, a layer AutoCAD refuses to change (freezing the
active layer, making a frozen layer current) lands in `warnings` instead
of failing the call; the state's current layer is thawed before it is
made current when `frozen` is being restored, so save → freeze → restore
round-trips. Portable server states, not Layer States Manager entries.
Pack: settings · lean: no.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | A name from layer_state_list |
| `properties` | `any` | không | `None` | Subset of on, frozen, locked, color, linetype, lineweight, plot, current; omit for all |

**Ví dụ gọi**

```json
{
  "name": "example",
  "properties": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `layer_state_save`

**Nhóm:** `environment`  
**Làm gì:** Snapshot every layer's on/frozen/locked/color/linetype/lineweight/plot
flags plus the current layer as a named state stored in the drawing.

These are the server's own portable layer states: JSON chunks in an XRECORD
under the `ACADMCP_LAYERSTATES` dictionary. They live in the file and
travel with it, work on both engines, and do **not** appear in AutoCAD's
Layer States Manager (LAYERSTATE). Same name replaces (`replaced: true`).
Refusals: an empty or control-character name, a non-string description.
Pack: settings · lean: no.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | State name, e.g. PLOT-SET or DESIGN |
| `description` | `any` | không | `None` | Free text stored with the state |

**Ví dụ gọi**

```json
{
  "name": "example",
  "description": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `layer_thaw`

**Nhóm:** `layers`  
**Làm gì:** Thaw a frozen layer, making it visible and selectable again.

**Dùng khi nào:** Khi tạo, đổi tên, bật/tắt, đóng băng hoặc quản lý layer.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Layer name to thaw |

**Ví dụ gọi**

```json
{
  "name": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `layer_unlock`

**Nhóm:** `layers`  
**Làm gì:** Unlock a layer to allow entity selection and modification.

**Dùng khi nào:** Khi tạo, đổi tên, bật/tắt, đóng băng hoặc quản lý layer.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Layer name to unlock |

**Ví dụ gọi**

```json
{
  "name": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `layout_copy`

**Nhóm:** `layouts`  
**Làm gì:** Copy a paper-space layout: page setup, plot settings and all geometry.

`skipped` names any DXF types that could not be cloned — check it rather
than trusting `ok` alone. Associative hatch boundaries are re-pointed at the
cloned entities; `associativity_dropped` counts those that referenced
something outside the source layout and had to be cleared.

**Dùng khi nào:** Khi quản lý layout, viewport và không gian giấy.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `source` | `string` | có | `—` | Layout tab to copy from (never 'Model'). |
| `new_name` | `string` | có | `—` | Name for the new layout tab. |

**Ví dụ gọi**

```json
{
  "source": "D:\\DuAn\\drawing.dwg",
  "new_name": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `layout_create`

**Nhóm:** `layouts`  
**Làm gì:** Create a new paper-space layout tab.

**Dùng khi nào:** Khi quản lý layout, viewport và không gian giấy.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | New paper-space layout name (e.g. 'A3-Sheet'). |

**Ví dụ gọi**

```json
{
  "name": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `layout_delete`

**Nhóm:** `layouts`  
**Làm gì:** Delete a paper-space layout and every entity on it.

Refuses model space, a blank name, and the last remaining sheet. If the
deleted tab was the current one, the returned `current` is where geometry
goes next — and handles from the deleted sheet stop resolving.

**Dùng khi nào:** Khi quản lý layout, viewport và không gian giấy.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Paper-space layout tab to delete (never 'Model'). |

**Ví dụ gọi**

```json
{
  "name": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `layout_list`

**Nhóm:** `layouts`  
**Làm gì:** List all layout tabs (Model + paper-space layouts) and the current one.

**Dùng khi nào:** Khi quản lý layout, viewport và không gian giấy.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `layout_rename`

**Nhóm:** `layouts`  
**Làm gì:** Rename a paper-space layout. Entity handles are unaffected.

**Dùng khi nào:** Khi quản lý layout, viewport và không gian giấy.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `old_name` | `string` | có | `—` | Existing layout tab name. |
| `new_name` | `string` | có | `—` | New name; must not be blank or contain / \ * ? : ; , = ` |

**Ví dụ gọi**

```json
{
  "old_name": "example",
  "new_name": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `layout_set_current`

**Nhóm:** `layouts`  
**Làm gì:** Activate a layout tab.

**Dùng khi nào:** Khi quản lý layout, viewport và không gian giấy.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Layout tab to activate ('Model' or a paper-space layout). |

**Ví dụ gọi**

```json
{
  "name": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `leader_create_mleader`

**Nhóm:** `entity_creation`  
**Làm gì:** Create a native COM MLeader or an explicitly-labelled ezdxf composite.

**Dùng khi nào:** Khi cần vẽ thêm đối tượng hình học vào bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `points` | `array<array>` | có | `—` | Leader vertices as [x, y] pairs |
| `text` | `string` | có | `—` | Leader annotation text |
| `text_height` | `number` | không | `2.5` | — |
| `landing_gap` | `number` | không | `1.0` | — |
| `arrow_size` | `number` | không | `2.5` | — |
| `layer` | `string` | không | `DIM` | Target layer |

**Ví dụ gọi**

```json
{
  "points": [],
  "text": "example",
  "text_height": 2.5,
  "landing_gap": 1.0,
  "arrow_size": 2.5,
  "layer": "DIM"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `linetype_list`

**Nhóm:** `layers`  
**Làm gì:** Return the names of all linetypes currently loaded in the active drawing.

**Dùng khi nào:** Khi tạo, đổi tên, bật/tắt, đóng băng hoặc quản lý layer.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `linetype_load`

**Nhóm:** `layers`  
**Làm gì:** Load a single linetype safely.

Use this instead of `system_run_command('_-LINETYPE _LOAD ...')` — that
raw form deadlocks on the FILEDIA file-picker dialog and on the
-LINETYPE option-menu prompt (measured on AutoCAD 2026: it loads nothing
either way). This tool loads through the ActiveX `Linetypes.Load` member,
picks the right .lin file from MEASUREMENT, and verifies the linetype
actually loaded. Refuses a name that is not a valid symbol name, a file
outside the allowed paths, and reports a name the file does not carry
or a file AutoCAD cannot find as an error naming both.

**Dùng khi nào:** Khi tạo, đổi tên, bật/tắt, đóng băng hoặc quản lý layer.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Linetype name to load (e.g. 'CENTER', 'DASHED', 'HIDDEN') |
| `file` | `any` | không | `None` | Optional .lin file. Defaults to acadiso.lin (metric) or acad.lin (imperial), chosen from MEASUREMENT. Ignored by ezdxf backend. |

**Ví dụ gọi**

```json
{
  "name": "example",
  "file": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `mech_dimension_part`

**Nhóm:** `mechanical`  
**Làm gì:** Every dimension the part and its features ask for, laid out without overlaps.

Axial lengths are chained, stacked from a baseline or measured from an
origin; diameters stack outside the silhouette; fillets get a radius. Each
measurement appears once (ISO 129-1): every view record carries a
`dimensioned` flag, so after a `mech_part_draw` that dimensioned the front
view and a `mech_view_add`, this call dimensions only the new view, and
`views` naming a view already dimensioned is refused by name. `fits` resolves an ISO 286 code
against the measured nominal through the repository's authored tables and
appends the code to the dimension text; an explicit `tol` on a feature's own
intent does the same through the ISO 129 path.

Refused by name: a fit together with an explicit tolerance, a fit outside
the authored ISO 286 range (over 1 mm to 500 mm, IT4-IT11), a fit on an
intent with no measurable nominal, an unknown style, an unknown part_id, a
call when every view is already dimensioned (the message lists them), and
`part_id=None` on a drawing that holds more than one part. An angular intent
is reported in `skipped` rather than drawn, because a DimIntent carries no
vertex.

**Dùng khi nào:** Khi dựng hoặc kiểm tra bản vẽ cơ khí, chi tiết và dung sai.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `part_id` | `any` | không | `None` | Anchor handle from mech_part_draw; omit if the drawing holds one part |
| `style` | `string` | không | `chain` | Axial dimension style: chain | baseline | ordinate |
| `hole_table_threshold` | `integer` | không | `8` | Above this many holes the diameters move into a hole table |
| `fits` | `any` | không | `None` | ISO 286 fit per feature id, e.g. {'bearing_seat': 'k6', 'bore': 'H7'} |
| `views` | `any` | không | `None` | View indices to dimension, in mech_part_inspect order (default: every view not yet dimensioned) |

**Ví dụ gọi**

```json
{
  "part_id": null,
  "style": "chain",
  "hole_table_threshold": 8,
  "fits": null,
  "views": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `mech_hole_pattern`

**Nhóm:** `mechanical`  
**Làm gì:** A hole pattern on any drawing - the part model is not required.

The same expansion `HolePattern` performs inside a part, exposed for a
drawing that was not built from the model.

Refused before anything is drawn: an unknown pattern, a count below 1 (below
2 for polar), a linear pattern with no spacing, a grid with more than one
column or row and no pitch for it, a polar pattern with no pitch-circle
diameter, and a non-finite or non-positive diameter.

**Dùng khi nào:** Khi dựng hoặc kiểm tra bản vẽ cơ khí, chi tiết và dung sai.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `pattern` | `string` | có | `—` | linear | grid | polar |
| `x` | `number` | có | `—` | WCS X of the first hole (polar: the circle centre) |
| `y` | `number` | có | `—` | WCS Y of the first hole (polar: the circle centre) |
| `diameter` | `number` | có | `—` | Hole diameter in drawing units |
| `count` | `integer` | không | `2` | Holes along the pattern (polar: around the circle) |
| `spacing` | `number` | không | `0.0` | Pitch between holes (linear, grid columns) |
| `count_y` | `integer` | không | `1` | Rows, for a grid |
| `spacing_y` | `number` | không | `0.0` | Row pitch, for a grid |
| `pcd` | `number` | không | `0.0` | Pitch-circle diameter, for a polar pattern |
| `start_angle` | `number` | không | `0.0` | Angle of the first hole (polar), degrees CCW |
| `angle` | `number` | không | `0.0` | Direction of a linear pattern, degrees CCW |
| `layer` | `any` | không | `None` | Override the GEOMETRY layer for the circles |
| `centre_marks` | `boolean` | không | `True` | Draw ISO 128-23 centre marks |
| `dimension` | `boolean` | không | `False` | Add a '6x ⌀8' diameter callout |

**Ví dụ gọi**

```json
{
  "pattern": "example",
  "x": 1.0,
  "y": 1.0,
  "diameter": 1.0,
  "count": 2,
  "spacing": 0.0,
  "count_y": 1,
  "spacing_y": 0.0,
  "pcd": 0.0,
  "start_angle": 0.0,
  "angle": 0.0,
  "layer": null,
  "centre_marks": true,
  "dimension": false
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `mech_part_draw`

**Nhóm:** `mechanical`  
**Làm gì:** One part model - a turned profile or a plate outline plus typed features - drawn as views.

The model is written onto the drawing as `ACADMCP_MECH` XDATA on an anchor
POINT, so `mech_view_add` can add a section months later without the caller
re-describing the part, and `mech_part_inspect` reads it back.

Refused **before anything is drawn**, by path: a non-finite or non-positive
number (`segments[2].d_outer`), a bore that is not smaller than its outside,
an outline with fewer than three distinct vertices or one that crosses
itself, an unknown material, a feature whose placement is off the part, two
features that would remove the same material (both names given), a thread
outside the transcribed ISO 261 table, a keyway outside DIN 6885's bore
range, gear teeth whose tip diameter disagrees with their segment. A DIN 509
undercut, a DIN 471/472 groove, a DIN 332 centre hole and an ISO 3601-2
O-ring groove need explicit dimensions in this build: those tables are not
transcribed and the lookup refuses by name rather than interpolate. A
feature that cannot be projected into a requested view is listed in
`omitted`, never dropped.

**Dùng khi nào:** Khi dựng hoặc kiểm tra bản vẽ cơ khí, chi tiết và dung sai.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `spec` | `object` | có | `—` | The part: {kind: 'revolved'|'prismatic', name, material, segments:[{length, d_outer, d_inner, taper_to}] | outline:[[x,y]] + thickness, features:[{kind, id, ...}]} |
| `at_x` | `number` | không | `0.0` | WCS X of the first view's lower-left corner (the rotation pivot) |
| `at_y` | `number` | không | `0.0` | WCS Y of the first view's lower-left corner (the rotation pivot) |
| `rotation` | `number` | không | `0.0` | Degrees CCW; turns every view and its dimensions about (at_x, at_y) |
| `views` | `any` | không | `None` | Views to draw in order: front | side | top (default ['front']) |
| `projection` | `string` | không | `first` | first (ISO 128-30, default) | third |
| `dimension` | `boolean` | không | `True` | Also dimension the part (ISO 129 + ISO 286 fits) |
| `style` | `string` | không | `chain` | Axial dimension style: chain | baseline | ordinate |

**Ví dụ gọi**

```json
{
  "spec": {},
  "at_x": 0.0,
  "at_y": 0.0,
  "rotation": 0.0,
  "views": null,
  "projection": "first",
  "dimension": true,
  "style": "chain"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `mech_part_from_spec`

**Nhóm:** `mechanical`  
**Làm gì:** Several parts, their views and their dimensions, drawn inside one transaction.

Every part is validated before the transaction opens, so a refusal leaves
the drawing untouched and names the offending path (`parts[1]:
segments[0].d_outer: ...`). If a draw fails or the request is cancelled
part-way, the transaction is rolled back under an anyio shield, so a
cancelled call cannot leave half a sheet inside an open transaction.

Refused by name: an empty `parts` list, any part refusal from
`mech_part_draw`, and a transaction that cannot be opened.

**Dùng khi nào:** Khi dựng hoặc kiểm tra bản vẽ cơ khí, chi tiết và dung sai.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `spec` | `object` | có | `—` | {sheet: {intent, sheet_size, scale, layer_set}, parts: [{part: {...}, at: [x, y], rotation, views: ['front','side'], projection, dimension, style}]} |

**Ví dụ gọi**

```json
{
  "spec": {}
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `mech_part_inspect`

**Nhóm:** `mechanical`  
**Làm gì:** The `ACADMCP_MECH` payload a drawn part carries, decoded.

Never modifies the drawing. Returns the part model exactly as
`mech_part_draw` accepts it (`part`), the views drawn so far with their
placements, and the payload version.

Refused by name: an unknown part_id, a handle that carries no
`ACADMCP_MECH` payload, a corrupt or foreign payload, and `part_id=None` on
a drawing that holds no part or more than one (the message lists the
handles).

**Dùng khi nào:** Khi dựng hoặc kiểm tra bản vẽ cơ khí, chi tiết và dung sai.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `part_id` | `any` | không | `None` | Anchor handle from mech_part_draw; omit if the drawing holds one part |

**Ví dụ gọi**

```json
{
  "part_id": null
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `mech_view_add`

**Nhóm:** `mechanical`  
**Làm gì:** Another view of a part already on the drawing, laid out on its projection axis.

The part model comes back out of the drawing's `ACADMCP_MECH` XDATA, so the
caller never re-describes it, and the placement follows the projection angle
recorded when the part was drawn (first angle by default: the view from the
right goes to the left).

Refused by name: a section without a plane, or with a plane of zero length,
a plane that misses the part, or one that grazes an outline vertex so its
crossings cannot be paired; a half or offset section on the wrong kind of
plane (the message names the style that does apply); a detail without a
radius or with a scale of zero; an unknown part_id, and `part_id=None` on a
drawing that holds more than one part.

**Dùng khi nào:** Khi dựng hoặc kiểm tra bản vẽ cơ khí, chi tiết và dung sai.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `part_id` | `any` | không | `None` | Anchor handle from mech_part_draw; omit if the drawing holds one part |
| `kind` | `string` | không | `section` | front | side | top | section | detail |
| `side` | `string` | không | `right` | Which end an end view looks from: right | left |
| `style` | `string` | không | `full` | Section style: full | half | offset | revolved |
| `plane` | `any` | không | `None` | Cutting plane {p1:[x,y], p2:[x,y], label, direction:[dx,dy], via:[[x,y]]} - required for a section |
| `detail` | `any` | không | `None` | Detail region {center:[x,y], radius, scale, label, of:'front'} - required for a detail |
| `gap` | `number` | không | `20.0` | Gap between this view and its parent (mm) |
| `scale` | `number` | không | `1.0` | Must be 1.0: views are drawn full size (a detail takes its scale in detail.scale; a sheet scale is the viewport's) |

**Ví dụ gọi**

```json
{
  "part_id": null,
  "kind": "section",
  "side": "right",
  "style": "full",
  "plane": null,
  "detail": null,
  "gap": 20.0,
  "scale": 1.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `mleaderstyle_create`

**Nhóm:** `styles`  
**Làm gì:** Create a multileader style: preset values first, then `overrides`.

Headless it lands on `doc.mleader_styles`; live it is added through the
`ACAD_MLEADERSTYLE` dictionary (`AddObject(name, "AcDbMLeaderStyle")`)
and the object's properties are written. Refuses, before any write: an
unknown preset; an override key outside the four; `arrow_size` /
`text_height <= 0`, `landing_gap < 0`; a name that exists; a `text_style`
that is neither present nor a bundled preset (ISOCP, ISOCPEUR, ARIAL,
ROMANS — those are created on both engines, `textstyle_created`; live, a
preset whose font file the seat lacks is refused, nothing written).

**Dùng khi nào:** Khi quản lý text style, dimension style, linetype và kiểu hiển thị.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | New multileader style name |
| `preset` | `string` | có | `—` | iso (2.5 mm arrow, 1.0 landing, ISOCP 2.5) | ansi (3.0, 1.5, ROMANS 3.0) |
| `overrides` | `any` | không | `None` | arrow_size | landing_gap | text_style | text_height on top of the preset |

**Ví dụ gọi**

```json
{
  "name": "example",
  "preset": "example",
  "overrides": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `mleaderstyle_list`

**Nhóm:** `styles`  
**Làm gì:** Every MLEADERSTYLE with its four values on both engines
(`values_available: true`). Headless they are read from the MLEADERSTYLE
object; live from the `AcadMLeaderStyle` objects the `ACAD_MLEADERSTYLE`
dictionary holds (ActiveX exposes no *collection* property for them, but
the dictionary items are full objects). `leader_create_mleader` can still
override any of them per leader.

**Dùng khi nào:** Khi quản lý text style, dimension style, linetype và kiểu hiển thị.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `page_setup_apply`

**Nhóm:** `page_setup`  
**Làm gì:** AutoCAD's PAGESETUP as one call, on both engines.

Paper sizes are ISO 216 / ANSI Y14.1; the media is written in AutoCAD's own
spelling (`ISO_A3_(420.00_x_297.00_MM)`). `changed` lists only the values
that moved — re-applying the same setup reports `{}`. An unknown ctb is
written and reported `plot_style_known: false` (a missing ctb only matters
at plot time). Viewports on the sheet are never touched.

Refused before anything is written: an unknown paper, orientation, scale
or plot_area, an empty device or plot_style, margins that leave no
printable area, `Model`, an unknown layout. On the live engine `margins_mm`
is refused (the .pc3 owns them) and a media the device does not offer is
refused with the device's names for the same paper.

The proof is the PDF: `batch_plot` reads each sheet's `/MediaBox` back.

**Dùng khi nào:** Khi thiết lập khổ giấy, máy in, tỷ lệ và cấu hình xuất bản.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `layout` | `string` | có | `—` | Paper-space layout to set up (never 'Model'). |
| `paper` | `string` | có | `—` | ISO_A0…ISO_A4 or ANSI_A…ANSI_E (short forms A3, ansi_b accepted). |
| `orientation` | `string` | không | `landscape` | landscape | portrait |
| `plot_style` | `string` | không | `monochrome.ctb` | Plot style table, e.g. monochrome.ctb, acad.ctb, Grayscale.ctb (plot_style_list). |
| `scale` | `string` | không | `fit` | fit | 1:1 | 1:2 | 1:5 | 1:10 | 1:20 | 1:50 | 1:100 | 2:1 | 5:1 | 10:1 |
| `plot_area` | `string` | không | `layout` | layout | extents |
| `device` | `string` | không | `DWG To PDF.pc3` | Plotter configuration (.pc3) or printer name. |
| `margins_mm` | `any` | không | `None` | [top, bottom, left, right] in mm. Headless only: AutoCAD takes margins from the .pc3. |
| `center` | `boolean` | không | `True` | Centre the plot on the paper. |

**Ví dụ gọi**

```json
{
  "layout": "example",
  "paper": "example",
  "orientation": "landscape",
  "plot_style": "monochrome.ctb",
  "scale": "fit",
  "plot_area": "layout",
  "device": "DWG To PDF.pc3",
  "margins_mm": null,
  "center": true
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `page_setup_list`

**Nhóm:** `page_setup`  
**Làm gì:** The page setup stored on each paper-space layout.

`paper` is the catalogue name (ISO_A3, ANSI_B, …) when the stored size
matches one within 0.5 mm, otherwise the media name as stored; `size_mm`,
`orientation`, `plot_style` (ctb), `scale` ("fit", "1:50", or a custom
ratio), `plot_area`, `device`, `margins_mm` [top, bottom, left, right] and
`center` are read back from the LAYOUT object (headless) or the AutoCAD
Layout (live). Refuses an unknown layout name and `Model` (model space has
no sheet; plot it with `drawing_export_pdf(layout=None)`).

**Dùng khi nào:** Khi thiết lập khổ giấy, máy in, tỷ lệ và cấu hình xuất bản.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `layout` | `any` | không | `None` | One paper-space layout, or omit for every sheet (Model is never listed). |

**Ví dụ gọi**

```json
{
  "layout": null
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `pdf_to_dwg`

**Nhóm:** `cadtroly`  
**Làm gì:** Create the final semantic DWG in one MCP call.

The PDF is vectorized to a private temporary DXF, opened through the live
AutoCAD backend, placed on an A-series layout and saved as DWG. The
temporary DXF and its lock files are removed in ``finally`` after the DWG
is saved, so callers do not have to manage intermediate artifacts.

**Dùng khi nào:** Khi cần dùng chức năng `pdf_to_dwg` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `source` | `string` | có | `—` | Full path to a single-page PDF sheet. |
| `target` | `string` | có | `—` | Full output path ending in .dwg. |
| `paper` | `string` | không | `A1` | Paper size for the sheet layout, default A1. |
| `orientation` | `string` | không | `landscape` | landscape or portrait. |
| `layout` | `string` | không | `A1-SEMANTIC` | Paper-space layout name. |

**Ví dụ gọi**

```json
{
  "source": "D:\\DuAn\\mat-bang.pdf",
  "target": "D:\\DuAn\\mat-bang_semantic.dwg",
  "paper": "A1",
  "orientation": "landscape"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `pdf_vectorize`

**Nhóm:** `cadtroly`  
**Làm gì:** Convert PDF vector artwork to editable DXF entities on semantic layers.

Output is separated into technical layers such as ``PDF_COLUMNS``,
``PDF_WALLS``, ``PDF_DOORS``, ``PDF_WINDOWS``, ``PDF_FURNITURE``,
``PDF_SANITARY``, ``PDF_DIMENSIONS``, ``PDF_HATCH``, ``PDF_STRUCTURE``,
``PDF_TEXT``, ``PDF_NOTES``, ``PDF_TITLE`` and ``PDF_FRAME`` so an engineer
can isolate, edit, delete or add each group. When available, the original
DWG layer names embedded in the PDF are used as the classification source.
Outlined PDF text remains geometry by design, so dimensions and symbols
are not lost when the source font prevents text extraction. The returned
counts are a quick audit before opening the DXF and saving it as DWG.

**Dùng khi nào:** Khi cần dùng chức năng `pdf_vectorize` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `source` | `string` | có | `—` | Full path to a single-page PDF sheet. |
| `target` | `string` | có | `—` | Full output path ending in .dxf. |

**Ví dụ gọi**

```json
{
  "source": "D:\\DuAn\\drawing.dwg",
  "target": "D:\\DuAn\\drawing.dwg"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `pid_equipment_list`

**Nhóm:** `pid`  
**Làm gì:** Every equipment, valve and connector node with its ports and how many lines reach them.

Rows come from `pid_graph`; the drawing is not modified and `csv_path` is
the only file this tool writes.

**Dùng khi nào:** Khi dựng hoặc kiểm tra sơ đồ P&ID, đường ống và thiết bị.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `csv_path` | `any` | không | `None` | Write the rows as CSV here (inside ALLOWED_PATHS) |
| `tolerance` | `number` | không | `0.5` | Endpoint-to-port snap distance (mm) |
| `scope` | `string` | không | `current_space` | current_space | all |

**Ví dụ gọi**

```json
{
  "csv_path": null,
  "tolerance": 0.5,
  "scope": "current_space"
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `pid_from_spec`

**Nhóm:** `pid`  
**Làm gì:** Equipment, valves, instruments and connectors placed, then every line
drawn port-to-port, inside one transaction: any bad item rolls the whole
sheet back and the error names it (`lines[2].to`); so does an interruption
(a client cancellation mid-run leaves no half-drawn sheet and no open
transaction on either engine — the live one goes back to the UNDO Mark
`transaction_begin` set, so it never waits at an AutoCAD prompt; should
that rollback itself fail, the failure is logged, the cancellation is what
the client sees, and the drawing must be checked before a retry).
A non-finite coordinate, rotation, scale or stub is refused
by path before anything is placed. The response carries the graph read
back from the drawing and the P&ID critique issues, so the caller sees
dangling ends or duplicate tags in the same round trip. `dry_run` returns
the planned vertices and crossings without touching the drawing.

**Dùng khi nào:** Khi dựng hoặc kiểm tra sơ đồ P&ID, đường ống và thiết bị.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `spec` | `object` | có | `—` | {sheet, equipment[], valves[], instruments[], lines[], connectors[]} — see the P&ID prompt |
| `dry_run` | `boolean` | không | `False` | Validate and route in memory; draw nothing |

**Ví dụ gọi**

```json
{
  "spec": {},
  "dry_run": false
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `pid_graph`

**Nhóm:** `pid`  
**Làm gì:** Connectivity of the drawing as it *is*, not as it was drawn.

Nodes: symbol INSERTs classified by catalogue name (confidence 1.0),
ACADMCP_PID payload (0.95), tag attributes / block-name keywords (0.6) or
a line touching an unknown INSERT (0.3); every node reports its `source`.
Ports come from the INSERT's real rotation, scale and mirror, measured
(a stretched bubble drops the node to 0.6 with a note). Edges: lines and
polylines; each end resolves to a port, a junction on another line, or
`dangling` with the nearest port as a hint — always within its own
space, so `scope="all"` never joins two sheets. `stats.confidence_min`
is the number to read before trusting a foreign drawing.

**Dùng khi nào:** Khi dựng hoặc kiểm tra sơ đồ P&ID, đường ống và thiết bị.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `tolerance` | `number` | không | `0.5` | Endpoint-to-port snap distance (mm) |
| `label_search` | `number` | không | `15.0` | How far to look for tag/line-number text (mm) |
| `scope` | `string` | không | `current_space` | current_space | all (every layout, current restored afterwards) |
| `include_foreign` | `boolean` | không | `True` | Classify INSERTs not placed by this server (confidence < 1) |
| `include_geometry` | `boolean` | không | `False` | Include edge vertices |

**Ví dụ gọi**

```json
{
  "tolerance": 0.5,
  "label_search": 15.0,
  "scope": "current_space",
  "include_foreign": true,
  "include_geometry": false
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `pid_instrument_index`

**Nhóm:** `pid`  
**Làm gì:** Every instrument bubble with its ISA-5.1 reading and what it connects to.

Rows come from `pid_graph`, never from typed-in lists; the drawing is not
modified. `csv_path` is the only file this tool writes.

**Dùng khi nào:** Khi dựng hoặc kiểm tra sơ đồ P&ID, đường ống và thiết bị.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `csv_path` | `any` | không | `None` | Write the rows as CSV here (inside ALLOWED_PATHS) |
| `tolerance` | `number` | không | `0.5` | Endpoint-to-port snap distance (mm) |
| `scope` | `string` | không | `current_space` | current_space | all |

**Ví dụ gọi**

```json
{
  "csv_path": null,
  "tolerance": 0.5,
  "scope": "current_space"
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `pid_line_draw`

**Nhóm:** `pid`  
**Làm gì:** Connect two ports with one LWPOLYLINE on the class's layer.

Ports come from `pid_symbol_insert`; a bubble's radial port is entered
without a name. `auto` picks the shortest orthogonal route that leaves each
port straight for `stub` mm; when none exists the call refuses and says so
— pass waypoints. `crossings` counts existing P&ID lines the new one cuts
(reported, never refused) and `port_reuse` names ports that already had a
line (branching is legal). Signal classes get ISA-5.1 markers (`//`, `X`,
`L`, `o`) as small blocks on segments >= 15 mm; electric is dashed by layer.
A signal line carries no pipe line number: it gets no auto-built number
and no label, and does not consume the process sequence — a verbatim
`line_number` is still written and labelled. With waypoints, a bubble's
exit leaves towards the first waypoint (and the entry arrives from the
last one); `crossings` follows existing arcs, not their chords.

**Dùng khi nào:** Khi dựng hoặc kiểm tra sơ đồ P&ID, đường ống và thiết bị.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `from_` | `object` | có | `—` | {handle, port} of a placed symbol, or {x, y} |
| `to` | `object` | có | `—` | {handle, port} of a placed symbol, or {x, y} |
| `line_class` | `string` | không | `process_major` | process_major | process_minor | utility | pneumatic | electric | hydraulic | capillary | data |
| `route` | `any` | không | `auto` | auto (orthogonal) | direct | [[x, y], ...] waypoints |
| `stub` | `number` | không | `5.0` | Minimum straight run leaving each port (mm) |
| `line_number` | `any` | không | `None` | Verbatim line number; omit to build one from the fields |
| `size` | `any` | không | `None` | Nominal size, e.g. 100 |
| `service` | `any` | không | `None` | Service code, e.g. P |
| `spec` | `any` | không | `None` | Piping spec, e.g. CS1 |
| `insulation` | `any` | không | `None` | Insulation code, e.g. IH |
| `number_format` | `any` | không | `None` | Default {size}-{service}-{seq}-{spec}-{insulation}; empty fields drop out |
| `label` | `boolean` | không | `True` | Write the line number along the longest segment |
| `arrow` | `any` | không | `None` | Flow arrow at the end; default per class (process yes, signal no) |

**Ví dụ gọi**

```json
{
  "from_": {},
  "to": {},
  "line_class": "process_major",
  "route": "auto",
  "stub": 5.0,
  "line_number": null,
  "size": null,
  "service": null,
  "spec": null,
  "insulation": null,
  "number_format": null,
  "label": true,
  "arrow": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `pid_line_list`

**Nhóm:** `pid`  
**Làm gì:** Every P&ID line with its number, class, size/service/spec/insulation and endpoints.

Rows come from `pid_graph`; untagged lines sort last with `line_number: null`.
The drawing is not modified; `csv_path` is the only file this tool writes.

**Dùng khi nào:** Khi dựng hoặc kiểm tra sơ đồ P&ID, đường ống và thiết bị.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `csv_path` | `any` | không | `None` | Write the rows as CSV here (inside ALLOWED_PATHS) |
| `tolerance` | `number` | không | `0.5` | Endpoint-to-port snap distance (mm) |
| `scope` | `string` | không | `current_space` | current_space | all |

**Ví dụ gọi**

```json
{
  "csv_path": null,
  "tolerance": 0.5,
  "scope": "current_space"
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `pid_symbol_insert`

**Nhóm:** `pid`  
**Làm gì:** Insert a catalogue symbol as a real block with TAG attributes and named ports.

Defines the block on first use (`defined`), creates a missing family layer
from the P&ID layer set (`layers_created`), writes an ACADMCP_PID payload
so readers without the catalogue still see the ports, and returns every
port in WCS — connect them with `pid_line_draw`. An invalid ISA-5.1 tag is
written and reported in `tag_warnings`; `drawing_critique` flags it.

**Dùng khi nào:** Khi dựng hoặc kiểm tra sơ đồ P&ID, đường ống và thiết bị.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `symbol` | `string` | có | `—` | Catalogue symbol name, e.g. gate, centrifugal_pump, vertical_vessel, instrument, offpage |
| `x` | `number` | có | `—` | Insertion X (WCS) |
| `y` | `number` | có | `—` | Insertion Y (WCS) |
| `rotation` | `number` | không | `0.0` | Rotation in degrees; 0 = flow left to right |
| `scale` | `number` | không | `1.0` | Uniform scale |
| `tag` | `any` | không | `None` | Tag: equipment P-101, valve HV-101, instrument FIC-101 (split into FUNC/LOOP) |
| `desc` | `any` | không | `None` | Description attribute |
| `actuator` | `any` | không | `None` | Valves: none | diaphragm | piston | motor | solenoid | hand |
| `fail` | `any` | không | `None` | Actuated valves: FO | FC | FL |
| `type` | `any` | không | `None` | Instruments: discrete | dcs | computer | plc |
| `location` | `any` | không | `None` | Instruments: field | primary | auxiliary | primary_rear | auxiliary_rear |
| `params` | `any` | không | `None` | Parametric vessels: {width, height, nozzles: [{name, side, fraction}], roof, trays, jacketed} |
| `shape` | `any` | không | `None` | Reducer: concentric | eccentric |
| `direction` | `any` | không | `None` | Off-page connector: in | out |
| `link` | `any` | không | `None` | Off-page connector link id shared by both ends |
| `layer` | `any` | không | `None` | Override the family layer |

**Ví dụ gọi**

```json
{
  "symbol": "example",
  "x": 1.0,
  "y": 1.0,
  "rotation": 0.0,
  "scale": 1.0,
  "tag": null,
  "desc": null,
  "actuator": null,
  "fail": null,
  "type": null,
  "location": null,
  "params": null,
  "shape": null,
  "direction": null,
  "link": null,
  "layer": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `pid_symbol_list`

**Nhóm:** `pid`  
**Làm gì:** The symbols `pid_symbol_insert` can place, with their ports and variant options.

Authored from ISO 10628-2 (equipment, valves) and ISA-5.1 (instrumentation);
each row's `source` names the figure. Symbol-local sizes are millimetres at
A3/A1 paper scale (bubble Ø10, valve 8×4); `scale` at insertion rescales.

**Dùng khi nào:** Khi dựng hoặc kiểm tra sơ đồ P&ID, đường ống và thiết bị.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `family` | `any` | không | `None` | valve | rotating | vessel | heat | misc | instrument | connector | marker; omit for all |

**Ví dụ gọi**

```json
{
  "family": null
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `pid_tag_parse`

**Nhóm:** `pid`  
**Làm gì:** ISA-5.1-2009 Table 4.1 as a grammar: first letter, modifier, readout and
output functions, trailing high/low, loop number and suffix — with the
standard's description ("Flow Indicating Controller") or the first
offending letter. Equipment prefixes are not standardised, so the default
map (P pump, V vessel, E exchanger, ...) can be replaced per call.

**Dùng khi nào:** Khi dựng hoặc kiểm tra sơ đồ P&ID, đường ống và thiết bị.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `tag` | `string` | có | `—` | e.g. FIC-101, 10-PDT-203A, P-101A |
| `kind` | `string` | không | `auto` | auto | instrument | equipment |
| `equipment_prefixes` | `any` | không | `None` | Replace the default equipment prefix map, e.g. {'Q': 'quench tower'} |

**Ví dụ gọi**

```json
{
  "tag": "example",
  "kind": "auto",
  "equipment_prefixes": null
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `pipe_takeoff`

**Nhóm:** `plant`  
**Làm gì:** A pipe takeoff: topology from the P&ID, lengths from the layout, rows by room x service x diameter.

The P&ID gives the runs (junctions merged, tees split, a line drawn twice
counted once, valves and reducers bridged), each run's service (the layer,
overridden by a supply / return word near the line), its diameters exactly
as labelled (direct, carried by continuity - never across a reducer - or
unassigned) and the equipment tags at its ends. The length comes from the
layout unless the scale check calls the P&ID to scale: the rectilinear
minimum spanning tree of the run's tag positions on the layout, each
connection along x first then y, plus `vertical_allowance` per connection.
The P&ID's drawn length stays beside it as `schematic_m`, never as the
answer. Lengths are metres from the unit the geometry implies; an INSUNITS
that disagrees is a warning, never a factor. Status A / B / C per run: a C
run (an end on no equipment, a tag missing from or written twice on the
layout) is on the Kontrol sheet with its schematic length, counted in the
total and flagged.

Read-only on both drawings. With `output` it writes one workbook - Metraj,
Özet, Kontrol, Metodoloji - as XLSX and, always, as CSV beside it.

Refused before a drawing is read: `lang` outside tr / en / ru, an unknown
service or length source, an allowance outside 0-1, a negative vertical
allowance, a non-positive tolerance, and `length_source='layout'` without
a layout. A missing, unreadable or oversize drawing is refused by the
reader, which names MAX_DXF_BYTES. Refused after the scale check:
`length_source='pid'` on a P&ID it calls schematic, unless `force=True`
(the refusal quotes the statistics). Without openpyxl the XLSX is not
written and `files.refused` carries `capability: "xlsx_write"` naming the
`office` extra; the CSV files are written all the same.

**Dùng khi nào:** Khi làm bản vẽ plant hoặc bố trí thiết bị công nghiệp.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `pid_path` | `any` | không | `None` | The P&ID (DXF headlessly; DXF or DWG on a live seat). Omit to read the current drawing as the P&ID. |
| `layout_path` | `any` | không | `None` | The layout of the same plant. Omitted, every length is the P&ID's drawn length and is marked scale_verified: false. |
| `output` | `any` | không | `None` | Workbook to write (.xlsx); the four sheets are also written as CSV beside it. Omit to return the rows only. |
| `lang` | `string` | không | `en` | Headers and method text: tr | en | ru. |
| `services` | `any` | không | `None` | Services to take off; default product, cip_supply, cip_return. Also: glycol_supply, glycol_return, steam, condensate, cold_water, hot_water, ice_water, compressed_air, drain, electrical, unknown. |
| `allowance` | `number` | không | `0.2` | Allowance as a share of the net length (0.20 = 20 %); its own column. |
| `vertical_allowance` | `number` | không | `0.0` | Metres added per connection for rises and drops (layout lengths). |
| `length_source` | `string` | không | `auto` | auto | pid | layout. auto measures on the P&ID only when the scale check calls it to scale, else on the layout. |
| `force` | `boolean` | không | `False` | With length_source='pid', measure on a P&ID the scale check calls schematic anyway. |
| `layers` | `any` | không | `None` | P&ID layers holding the lines; default every layer the vocabulary files under piping or electrical with confidence >= 0.9. |
| `tol` | `any` | không | `None` | Line ends closer than this (P&ID drawing units) are one junction; default 1 mm in the unit the P&ID's geometry implies (1.0 on a millimetre drawing, 0.001 on a metre one). |
| `exclude_regions` | `any` | không | `None` | Ids of reported detail copies (detail_copies: D1, D2 ...) whose runs repeat pipes drawn elsewhere and are left out. Omitted, every copy is counted. |

**Ví dụ gọi**

```json
{
  "pid_path": null,
  "layout_path": null,
  "output": null,
  "lang": "en",
  "services": null,
  "allowance": 0.2,
  "vertical_allowance": 0.0,
  "length_source": "auto",
  "force": false,
  "layers": null,
  "tol": null,
  "exclude_regions": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `plot_style_list`

**Nhóm:** `page_setup`  
**Làm gì:** The ctb files AutoCAD ships (`monochrome.ctb`, `acad.ctb`, `Grayscale.ctb`,
the Screening set, …) and, on the live engine, the files actually present
in `Preferences.Files.PrinterStyleSheetPath` (`source: "installed"`,
`installed: true/false` per row). Headlessly `installed` is `null`: there
is no installation to scan, and the catalogue is not evidence of one.
Never refuses; an unreadable Preferences object degrades to the catalogue.

**Dùng khi nào:** Khi thiết lập khổ giấy, máy in, tỷ lệ và cấu hình xuất bản.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `point_from_snap`

**Nhóm:** `premium`  
**Làm gì:** Compute a deterministic snap point on an entity. Use this INSTEAD OF
guessing coordinates — eliminates the most common LLM drawing error.

**Dùng khi nào:** Khi dùng chức năng nâng cao; kiểm tra capability trước nếu backend không hỗ trợ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Entity handle to snap onto |
| `snap` | `string` | có | `—` | Snap type: end | mid | center | quad | perp | near |
| `ref_x` | `any` | không | `None` | Reference X (required for perp/near; disambiguates end/quad) |
| `ref_y` | `any` | không | `None` | Reference Y |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "snap": "example",
  "ref_x": null,
  "ref_y": null
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `point_intersection`

**Nhóm:** `premium`  
**Làm gì:** Compute the intersection of two geometry entities (LINE-LINE, LINE-CIRCLE,
CIRCLE-CIRCLE). When two candidates exist, ref_x/ref_y selects the nearest.
Returns {x, y}.

**Dùng khi nào:** Khi dùng chức năng nâng cao; kiểm tra capability trước nếu backend không hỗ trợ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle1` | `string` | có | `—` | First entity handle (LINE or CIRCLE) |
| `handle2` | `string` | có | `—` | Second entity handle (LINE or CIRCLE) |
| `ref_x` | `any` | không | `None` | Reference X to pick nearest candidate when multiple exist |
| `ref_y` | `any` | không | `None` | Reference Y |

**Ví dụ gọi**

```json
{
  "handle1": "A1B2",
  "handle2": "A1B2",
  "ref_x": null,
  "ref_y": null
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `point_tangent`

**Nhóm:** `premium`  
**Làm gì:** Compute the tangent point on a circle from an external point.
Returns {x, y}. Raises if the from-point is inside the circle.

**Dùng khi nào:** Khi dùng chức năng nâng cao; kiểm tra capability trước nếu backend không hỗ trợ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `circle_handle` | `string` | có | `—` | Handle of the CIRCLE entity |
| `from_x` | `number` | có | `—` | X of the external point |
| `from_y` | `number` | có | `—` | Y of the external point |
| `ref_x` | `any` | không | `None` | Reference X to pick nearest tangent point when two exist |
| `ref_y` | `any` | không | `None` | Reference Y |

**Ví dụ gọi**

```json
{
  "circle_handle": "A1B2",
  "from_x": 1.0,
  "from_y": 1.0,
  "ref_x": null,
  "ref_y": null
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `revision_add`

**Nhóm:** `sheet`  
**Làm gì:** Append one row to the revision block, creating the block on first use.

Idempotent per revision code: a code the drawing already carries returns
`created=false` and draws nothing, so re-running a revision pass cannot
stack duplicates. The block defaults to the upper-right corner of the
drawing frame, growing downwards, so it does not collide with the ISO 7573
parts list above the title block. Refusals, all before the first entity: a
malformed code, a cloud region that is not [x0, y0, x1, y1], and any
request for clouds on a backend whose `revcloud` capability is false (the
COM engine — REVCLOUD has no ActiveX member) — that one carries
`capability: "revcloud"`.

**Dùng khi nào:** Khi tạo và quản lý sheet, title block và hồ sơ phát hành.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `rev` | `string` | có | `—` | Revision code: one to three capitals or digits (A, B, 01). |
| `description` | `string` | có | `—` | What changed, verbatim. |
| `date` | `string` | không | `` | Issue date, verbatim. |
| `by` | `string` | không | `` | Who issued it. |
| `clouds` | `any` | không | `None` | Regions to cloud, each [x0, y0, x1, y1] in WCS. Refused before anything is written on an engine without the revcloud capability. |
| `tags` | `any` | không | `None` | Points [x, y] to put a triangular revision tag at. |
| `size` | `string` | không | `A3` | Sheet the block is placed on: A4-A0. |
| `orientation` | `string` | không | `landscape` | — |
| `origin_x` | `number` | không | `0.0` | — |
| `origin_y` | `number` | không | `0.0` | — |
| `cloud_segment` | `number` | không | `8.0` | Revision-cloud arc segment length (mm). |
| `layout` | `string` | không | `` | — |

**Ví dụ gọi**

```json
{
  "rev": "example",
  "description": "example",
  "date": "",
  "by": "",
  "clouds": null,
  "tags": null,
  "size": "A3",
  "orientation": "landscape",
  "origin_x": 0.0,
  "origin_y": 0.0,
  "cloud_segment": 8.0,
  "layout": ""
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `section_line`

**Nhóm:** `mechanical`  
**Làm gì:** Draw the cutting-plane line and hand back the plane a section view consumes.

Wide segments at the ends on GEOMETRY, the thin long-dash-dot middle on
CENTER, an arrow at each end whose head sits on the line end and points the
way the section is viewed, and the same letter beyond both arrows.
`payload["plane"]` is exactly `{p1, p2, label, direction, style}` — feed it
to the section view so the label on the plan and the label on the view
cannot disagree. Refusals, before any entity is written: `p1 == p2`, a zero
or parallel viewing direction, an empty `label`, a `style` outside
full/half/offset/revolved, and a non-positive `height`.

**Dùng khi nào:** Khi dựng hoặc kiểm tra bản vẽ cơ khí, chi tiết và dung sai.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `x1` | `number` | có | `—` | Cutting plane start X (WCS). |
| `y1` | `number` | có | `—` | Cutting plane start Y (WCS). |
| `x2` | `number` | có | `—` | Cutting plane end X (WCS). |
| `y2` | `number` | có | `—` | Cutting plane end Y (WCS). |
| `label` | `string` | không | `A` | Capital letter drawn at both ends, e.g. 'A'. |
| `direction` | `any` | không | `None` | Viewing direction as [dx, dy]; must not be parallel to the cutting plane. |
| `style` | `string` | không | `full` | full | half | offset | revolved — carried into the returned plane. |
| `height` | `number` | không | `5.0` | Label height (mm). |
| `layer` | `any` | không | `None` | Override the role layers (GEOMETRY/CENTER/TEXT). |

**Ví dụ gọi**

```json
{
  "x1": 1.0,
  "y1": 1.0,
  "x2": 1.0,
  "y2": 1.0,
  "label": "A",
  "direction": null,
  "style": "full",
  "height": 5.0,
  "layer": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `selection_filter`

**Nhóm:** `entity_query`  
**Làm gì:** AutoCAD's QSELECT: filter the drawing by properties.

Named parameters rather than a query string, deliberately — a mistyped
attribute name in a query language comes back as an empty result, which is
indistinguishable from "no matches". `filtered_by` reports which filters
actually ran.

**Dùng khi nào:** Khi cần tìm và đọc thuộc tính đối tượng theo handle hoặc điều kiện.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `entity_type` | `string` | không | `` | DXF type, e.g. LWPOLYLINE. Empty means any. |
| `layer` | `string` | không | `` | Layer name. Empty means any. |
| `color` | `any` | không | `None` | ACI colour to match. |
| `linetype` | `string` | không | `` | Linetype name. Empty means any. |
| `min_area` | `any` | không | `None` | Keep only closed shapes with at least this area. |

**Ví dụ gọi**

```json
{
  "entity_type": "",
  "layer": "",
  "color": null,
  "linetype": "",
  "min_area": null
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `selection_get`

**Nhóm:** `entity_query`  
**Làm gì:** Read the entities the user pre-selected in the AutoCAD viewport (COM backend only).

Returns the implied "pickfirst" selection — the entities highlighted with
grips before invoking the AI — so work can be scoped to exactly those
entities instead of the whole drawing. Typical use::

    sel = selection_get()
    dimension_auto(sel["handles"], style="chain")

Result keys:
    ok        — True on the COM backend (even for an empty selection)
    count     — number of selected entities
    handles   — list of entity handles (hex strings) to act on
    entities  — full per-entity info (type, layer, color, ...)
    pickfirst — state of the PICKFIRST sysvar (None if unknown)
    message   — guidance when nothing is selected

On the ezdxf headless backend there is no viewport, so this returns
ok=False with an empty handles list.

`fields` / `compact` shape the "entities" collection — this tool already
returns an object, so the columnar envelope lands *under* that key rather
than replacing the result. `handles` is unaffected, so a caller that only
wants handles can pass fields=["handle"] and still read `handles` directly.

**Dùng khi nào:** Khi cần tìm và đọc thuộc tính đối tượng theo handle hoặc điều kiện.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `fields` | `any` | không | `None` | Project to these fields, in this order (e.g. ['handle','type','layer']); 'properties.<key>' reaches one nested value. Omit for the full record; an unknown name errors and lists the valid ones. |
| `compact` | `boolean` | không | `False` | Return a columnar {fields, rows, count, offset, total, truncated, next_offset} envelope instead of dicts: much cheaper per row, and the only shape that reports truncation. |

**Ví dụ gọi**

```json
{
  "fields": null,
  "compact": false
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `selection_polygon`

**Nhóm:** `entity_query`  
**Làm gì:** Window or crossing selection against a polygon rather than a rectangle.

**Dùng khi nào:** Khi cần tìm và đọc thuộc tính đối tượng theo handle hoặc điều kiện.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `points` | `array<array>` | có | `—` | Polygon vertices as [[x, y], ...]; at least 3. |
| `mode` | `string` | không | `window` | window = wholly inside only; crossing = touching. |
| `entity_type` | `string` | không | `` | Restrict to a DXF type. Empty means any. |
| `layer` | `string` | không | `` | Restrict to a layer. Empty means any. |

**Ví dụ gọi**

```json
{
  "points": [],
  "mode": "window",
  "entity_type": "",
  "layer": ""
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `selection_window`

**Nhóm:** `entity_query`  
**Làm gì:** AutoCAD's ssget window/crossing selection.

Corners may be given in any order. Selection is by *drawn* position, so an
entity in a mirrored frame is found where `entity_get` reports it. A
zero-area box is refused rather than answered with an empty list.

**Dùng khi nào:** Khi cần tìm và đọc thuộc tính đối tượng theo handle hoặc điều kiện.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `x1` | `number` | có | `—` | First corner X. |
| `y1` | `number` | có | `—` | First corner Y. |
| `x2` | `number` | có | `—` | Opposite corner X. |
| `y2` | `number` | có | `—` | Opposite corner Y. |
| `mode` | `string` | không | `window` | window = wholly inside only; crossing = also entities straddling the edge. |
| `entity_type` | `string` | không | `` | Restrict to a DXF type, e.g. CIRCLE. Empty means any. |
| `layer` | `string` | không | `` | Restrict to a layer. Empty means any. |

**Ví dụ gọi**

```json
{
  "x1": 1.0,
  "y1": 1.0,
  "x2": 1.0,
  "y2": 1.0,
  "mode": "window",
  "entity_type": "",
  "layer": ""
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `sheet_frame`

**Nhóm:** `sheet`  
**Làm gì:** ISO 5457 drawing frame for A4-A0: a 20 mm filing margin, 10 mm on the
other three edges, the grid reference system and the centring/trimming marks.

Borders, rules and marks land on TITLEBLOCK; the zone lettering on TEXT.
Refusals, all before the first entity is drawn: a size outside A4-A0 is
refused by name and the five covered sizes are listed; an orientation that
is neither 'landscape' nor 'portrait'; a `layout` that does not exist. The
zone divisions drawn are equal -- ISO 5457's shorter corner fields are not
implemented -- while the division counts are the standard's.

**Dùng khi nào:** Khi tạo và quản lý sheet, title block và hồ sơ phát hành.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `size` | `string` | không | `A3` | ISO 216 sheet: A4, A3, A2, A1 or A0. |
| `orientation` | `string` | không | `landscape` | 'landscape' or 'portrait'. |
| `zones` | `boolean` | không | `True` | Draw the ISO 5457 grid reference system: letters down the vertical edges from the top, numbers along the horizontal edges from the left. |
| `marks` | `boolean` | không | `True` | Draw the four centring marks and the eight corner trimming rectangles. |
| `origin_x` | `number` | không | `0.0` | X of the sheet's lower-left corner (WCS). |
| `origin_y` | `number` | không | `0.0` | Y of the sheet's lower-left corner (WCS). |
| `layout` | `string` | không | `` | Paper-space layout to draw the sheet on (create it with layout_create). Empty draws in the current space. |

**Ví dụ gọi**

```json
{
  "size": "A3",
  "orientation": "landscape",
  "zones": true,
  "marks": true,
  "origin_x": 0.0,
  "origin_y": 0.0,
  "layout": ""
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `solid_boolean`

**Nhóm:** `solids`  
**Làm gì:** Boolean-combine two native 3D solids (COM backend, opt-in).

The tool solid is consumed; the target holds the result.

**Dùng khi nào:** Khi tạo hoặc kiểm tra solid/3D geometry.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `target_handle` | `string` | có | `—` | Handle of the solid that receives the result. |
| `tool_handle` | `string` | có | `—` | Handle of the solid consumed by the operation. |
| `operation` | `string` | có | `—` | union | subtract | intersect |

**Ví dụ gọi**

```json
{
  "target_handle": "D:\\DuAn\\drawing.dwg",
  "tool_handle": "A1B2",
  "operation": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `solid_box`

**Nhóm:** `solids`  
**Làm gì:** Create a native 3D solid box (COM backend, opt-in).

**Dùng khi nào:** Khi tạo hoặc kiểm tra solid/3D geometry.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `cx` | `number` | có | `—` | Box center X. |
| `cy` | `number` | có | `—` | Box center Y. |
| `cz` | `number` | có | `—` | Box center Z. |
| `length` | `number` | có | `—` | Length along X (mm). |
| `width` | `number` | có | `—` | Width along Y (mm). |
| `height` | `number` | có | `—` | Height along Z (mm). |

**Ví dụ gọi**

```json
{
  "cx": 1.0,
  "cy": 1.0,
  "cz": 1.0,
  "length": 1.0,
  "width": 1.0,
  "height": 1.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `solid_cylinder`

**Nhóm:** `solids`  
**Làm gì:** Create a native 3D solid cylinder (COM backend, opt-in).

**Dùng khi nào:** Khi tạo hoặc kiểm tra solid/3D geometry.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `cx` | `number` | có | `—` | Base-center X. |
| `cy` | `number` | có | `—` | Base-center Y. |
| `cz` | `number` | có | `—` | Center Z (AutoCAD places the cylinder center here). |
| `radius` | `number` | có | `—` | Cylinder radius (mm). |
| `height` | `number` | có | `—` | Cylinder height (mm). |

**Ví dụ gọi**

```json
{
  "cx": 1.0,
  "cy": 1.0,
  "cz": 1.0,
  "radius": 1.0,
  "height": 1.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `solid_extrude`

**Nhóm:** `solids`  
**Làm gì:** Extrude a closed profile into a native 3D solid (COM backend, opt-in).

**Dùng khi nào:** Khi tạo hoặc kiểm tra solid/3D geometry.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `profile_handle` | `string` | có | `—` | Handle of a closed profile (circle / closed polyline). |
| `height` | `number` | có | `—` | Extrusion height; negative extrudes downward. |
| `taper_angle` | `number` | không | `0.0` | Taper angle in degrees. |

**Ví dụ gọi**

```json
{
  "profile_handle": "D:\\DuAn\\drawing.dwg",
  "height": 1.0,
  "taper_angle": 0.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `solid_revolve`

**Nhóm:** `solids`  
**Làm gì:** Revolve a closed profile around an axis into a native 3D solid (COM, opt-in).

**Dùng khi nào:** Khi tạo hoặc kiểm tra solid/3D geometry.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `profile_handle` | `string` | có | `—` | Handle of a closed profile (circle / closed polyline). |
| `axis_x1` | `number` | có | `—` | Revolution axis start X. |
| `axis_y1` | `number` | có | `—` | Revolution axis start Y. |
| `axis_x2` | `number` | có | `—` | Revolution axis end X. |
| `axis_y2` | `number` | có | `—` | Revolution axis end Y. |
| `angle` | `number` | không | `360.0` | Revolution angle in degrees. |

**Ví dụ gọi**

```json
{
  "profile_handle": "D:\\DuAn\\drawing.dwg",
  "axis_x1": 1.0,
  "axis_y1": 1.0,
  "axis_x2": 1.0,
  "axis_y2": 1.0,
  "angle": 360.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `standards_reference`

**Nhóm:** `cadtroly`  
**Làm gì:** Read the built-in project reference catalogue.

These entries guide layer naming and drafting setup; they do not certify
regulatory compliance.  Confirm the approved edition in the project
standards register before issuing construction documents.

**Dùng khi nào:** Khi cần dùng chức năng `standards_reference` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `discipline` | `any` | không | `None` | building | road | bridge; omit to list all |

**Ví dụ gọi**

```json
{
  "discipline": null
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `std_feature_draw`

**Nhóm:** `mechanical`  
**Làm gì:** Add a standard feature to geometry that already exists - a foreign drawing being finished.

Local frame: `(x, y)` is on the axis, +X runs along the axis in the
direction the feature extends and +Y is radially outward. The thread is the
ISO 6410 representation (minor diameter at 0.8 x major, thread-length limit
to the major) and its pitch comes from ISO 261 via `size` or from an
explicit `pitch` - it is never guessed. Every other kind takes its
dimensions from the registered standards table and is refused by name when
that table is absent, when the size is outside its coverage, or when the row
lacks a dimension the feature needs: no value is interpolated and no profile
is reconstructed. DIN 332 form R is refused - only forms A and B are drawn.

**Dùng khi nào:** Khi dựng hoặc kiểm tra bản vẽ cơ khí, chi tiết và dung sai.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `kind` | `string` | có | `—` | thread | undercut | ring_groove | centre_hole | oring_groove |
| `x` | `number` | có | `—` | Feature origin X (WCS): a point on the axis |
| `y` | `number` | có | `—` | Feature origin Y (WCS): a point on the axis |
| `params` | `object` | có | `—` | thread: {d, length, size|pitch, internal} (a size must name d's own thread - 'M20' with d=8 is refused, not drawn); undercut: {d, form: E|F}; ring_groove: {d, kind: shaft|bore}; centre_hole: {size, form: A|B}; oring_groove: {d, cord, kind: shaft|bore} |
| `rotation` | `number` | không | `0.0` | Degrees CCW applied to the local +X (along the axis, into the feature) |
| `layer` | `any` | không | `None` | Override the visible primitives' layer; CENTER and HIDDEN keep theirs |

**Ví dụ gọi**

```json
{
  "kind": "example",
  "x": 1.0,
  "y": 1.0,
  "params": {},
  "rotation": 0.0,
  "layer": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `std_part_insert`

**Nhóm:** `mechanical`  
**Làm gì:** Define the part's block once, insert it, and write its `std_part` XDATA.

The block carries DESIG / STD / SIZE / MAT attributes and an ACADMCP_MECH
payload, so a parts list is a read of the drawing rather than a naming
convention. Refusals, all before any write: a designation outside the
transcribed tables (named, with the nearest catalogue entries - nothing is
drawn approximately), a malformed designation, a missing or stray nominal
length, a view the family does not have, an attribute tag the block does
not carry, and a non-finite coordinate or rotation.

**Dùng khi nào:** Khi dựng hoặc kiểm tra bản vẽ cơ khí, chi tiết và dung sai.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `designation` | `string` | có | `—` | 'ISO 4014 - M12x60', 'ISO 4032 - M12', 'ISO 7089 - M12', 'ISO 4762 - M8x30', 'ISO 15 - 6205' (a bare '6205' also works) |
| `x` | `number` | có | `—` | Insertion X (WCS) |
| `y` | `number` | có | `—` | Insertion Y (WCS) |
| `view` | `string` | không | `side` | Fasteners: side | top. Bearings: simplified (ISO 8826-1) | detailed (ISO 8826-2). The default 'side' falls back to the family's first view. |
| `rotation` | `number` | không | `0.0` | Degrees CCW; 0 puts the part's axis along +X |
| `layer` | `string` | không | `GEOMETRY` | Layer for the INSERT; the block's own primitives keep GEOMETRY / CENTER / HIDDEN |
| `material` | `any` | không | `None` | Property class or material for the MAT attribute and the XDATA, e.g. '8.8' |

**Ví dụ gọi**

```json
{
  "designation": "example",
  "x": 1.0,
  "y": 1.0,
  "view": "side",
  "rotation": 0.0,
  "layer": "GEOMETRY",
  "material": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `std_part_list`

**Nhóm:** `mechanical`  
**Làm gì:** Catalogue rows with the dimensions a drawing needs, and their provenance.

Every row is transcribed from the named standard's own table and carries
its `source`. Coverage is deliberately narrow: ISO 261 first-choice sizes
only (M5-M36, M3-M24 for ISO 4762) and ISO 15 bore numbers 00-10 in the
600x / 620x / 630x series. A size outside a table is refused by name by
`std_part_insert` with the nearest entries, never interpolated. An unknown
`standard` is refused with the list of catalogue standards.

**Dùng khi nào:** Khi dựng hoặc kiểm tra bản vẽ cơ khí, chi tiết và dung sai.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `query` | `any` | không | `None` | Free text matched against designation, standard, size and family - 'M12', 'ISO 4014', '6205', 'washer' |
| `standard` | `any` | không | `None` | One of ISO 4014, ISO 4017, ISO 4032, ISO 7089, ISO 4762, ISO 15 |

**Ví dụ gọi**

```json
{
  "query": null,
  "standard": null
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `structural_qa`

**Nhóm:** `cadtroly`  
**Làm gì:** Check structural CAD quality and return error/warning findings.

This is a drawing/layer/geometry check, not a strength or safety
certification. Loads, materials, restraints and approved calculations are
required for engineering conclusions.

**Dùng khi nào:** Khi cần dùng chức năng `structural_qa` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `discipline` | `string` | không | `building` | building, road or bridge |

**Ví dụ gọi**

```json
{
  "discipline": "building"
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `surface_texture`

**Nhóm:** `mechanical`  
**Làm gì:** Draw the 60° surface-texture vee with its annotation in the standard positions.

Refusals, all before the first entity reaches the drawing: a text height
outside the seven ISO 1302 rows (2.5/3.5/5/7/10/14/20 mm — never
interpolated), a `lay` that is not one of the seven ISO 1302 directions of
lay, a `machining` outside any/required/prohibited, and a `standard` other
than ISO 21920-1 or ISO 1302.

**Dùng khi nào:** Khi dựng hoặc kiểm tra bản vẽ cơ khí, chi tiết và dung sai.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `x` | `number` | có | `—` | Symbol apex X (WCS) — the point the leader attaches to. |
| `y` | `number` | có | `—` | Symbol apex Y (WCS). |
| `ra` | `any` | không | `None` | Ra value in µm, written as 'Ra 3.2'. |
| `rz` | `any` | không | `None` | Rz value in µm, written as 'Rz 12.5'. |
| `machining` | `string` | không | `any` | any (basic vee) | required (bar across the vee, material removal required) | prohibited (circle in the vee, material removal not allowed). |
| `process` | `any` | không | `None` | Manufacturing method, treatment or coating, e.g. 'milled'. |
| `lay` | `any` | không | `None` | Direction of lay: parallel, perpendicular, crossed, multidirectional, circular, radial, particulate. |
| `allowance` | `any` | không | `None` | Machining allowance in mm, written below the extension line. |
| `all_around` | `boolean` | không | `False` | Circle at the kink: the requirement applies all around. |
| `leader_to` | `any` | không | `None` | [x, y] on the surface; draws a leader with an arrowhead there. |
| `height` | `number` | không | `3.5` | Text height (mm). ISO 1302 tabulates 2.5, 3.5, 5, 7, 10, 14, 20. |
| `rotation` | `number` | không | `0.0` | Rotate the whole symbol about its apex (degrees CCW). |
| `standard` | `string` | không | `ISO 21920-1` | ISO 21920-1 (default) or ISO 1302 for drawings issued under the older designation. |
| `layer` | `any` | không | `None` | Override the role layers (DIM for geometry, TEXT for text). |

**Ví dụ gọi**

```json
{
  "x": 1.0,
  "y": 1.0,
  "ra": null,
  "rz": null,
  "machining": "any",
  "process": null,
  "lay": null,
  "allowance": null,
  "all_around": false,
  "leader_to": null,
  "height": 3.5,
  "rotation": 0.0,
  "standard": "ISO 21920-1",
  "layer": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `system_about`

**Nhóm:** `system`  
**Làm gì:** Get detailed information about AutoCAD MCP Pro capabilities and available tools.

**Dùng khi nào:** Khi cần chẩn đoán server hoặc trạng thái kết nối.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `system_capabilities`

**Nhóm:** `entity_query`  
**Làm gì:** Return machine-readable support modes for the active backend.

**Dùng khi nào:** Khi cần tìm và đọc thuộc tính đối tượng theo handle hoặc điều kiện.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `system_get_variable`

**Nhóm:** `system`  
**Làm gì:** Get an AutoCAD system variable value.

**Dùng khi nào:** Khi cần chẩn đoán server hoặc trạng thái kết nối.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | System variable name (e.g. DIMSCALE, LTSCALE, INSUNITS, CLAYER, MEASUREMENT) |

**Ví dụ gọi**

```json
{
  "name": "example"
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `system_launch`

**Nhóm:** `environment`  
**Làm gì:** Connect to the application named by `CAD_PROGID` (attach if running,
launch otherwise) and report `launched`, `attached`, `version` and the
active `document`. Refusals: headless, `capability: "live_application"`
(there is no application to launch); an `open_path` that fails path
validation. Pack: settings · lean: no.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `visible` | `boolean` | không | `True` | Show the application window |
| `open_path` | `any` | không | `None` | A .dwg/.dxf to open after attaching |

**Ví dụ gọi**

```json
{
  "visible": true,
  "open_path": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `system_preferences_get`

**Nhóm:** `environment`  
**Làm gì:** The whitelisted `Preferences.*` values, enum values as names
(`SaveAsType: "ac2018_dwg"`), with `read_only` naming the four `Files.*`
paths. Refusals: headless, `capability: "preferences"` (they live in the
running application, not in a file); a key outside the whitelist.
Pack: settings · lean: no.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `keys` | `any` | không | `None` | Subset of OpenSave.SaveAsType, OpenSave.AutoSaveInterval, OpenSave.CreateBackup, OpenSave.IncrementalSavePercent, Display.CursorSize, Drafting.AutoSnapMarkerSize, Drafting.AutoSnapTooltip, Selection.PickBoxSize, Output.DefaultPlotStyleTable, Output.DefaultOutputDevice, Files.SupportPath, Files.TemplateDwgPath, Files.PrinterStyleSheetPath, Files.PrinterConfigPath; omit for all |

**Ví dụ gọi**

```json
{
  "keys": null
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `system_preferences_set`

**Nhóm:** `environment`  
**Làm gì:** Write one preference and report `old`, `new` and `changed`.

Refusals, all before any write: a read-only key (`Files.*`), an unknown
key, a value of the wrong type, an int outside the authored range
(`AutoSaveInterval` 0–600 min, `CursorSize` 1–100, `PickBoxSize` 0–50, …),
an unknown `SaveAsType` name; headless, `capability: "preferences"`.
Pack: settings · lean: no.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `key` | `string` | có | `—` | A writable key from system_preferences_get |
| `value` | `any` | có | `—` | New value: bool, int within the key's range, string, or an enum name |

**Ví dụ gọi**

```json
{
  "key": "example",
  "value": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `system_prompt_message`

**Nhóm:** `environment`  
**Làm gì:** `Utility.Prompt`: tell the operator something where they are looking.
Nothing in the drawing changes. Refusals: an empty message; headless,
`capability: "interactive_prompt"`. Pack: settings · lean: no.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `text` | `string` | có | `—` | The message; one line is best |

**Ví dụ gọi**

```json
{
  "text": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `system_run_command`

**Nhóm:** `system`  
**Làm gì:** Execute an AutoCAD command string directly (COM backend only).

Append \n for Enter. Example: '_LINE 0,0 100,0 \n'.

IMPORTANT: commands that finish at an option menu (e.g. -LINETYPE, -LAYER,
-STYLE return to '[?/Create/Load/Set]:' after their action) need an EXTRA
blank line or '_X\n' to exit, otherwise AutoCAD stays at a prompt and the
next COM call will deadlock. Example: '_-LINETYPE _LOAD CENTER acad.lin\n\n'.

A verb denylist refuses obviously destructive commands, but it is a guardrail
against issuing `ERASE ALL` by accident, NOT a security boundary — AutoCAD
accepts hundreds of commands and any loaded ARX/LISP adds more. Prefer the
typed tools (entity_delete, drawing_save_as, block_insert, drawing_purge):
they validate their arguments, which a free-text command string cannot.

**Dùng khi nào:** Khi cần chẩn đoán server hoặc trạng thái kết nối.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `command` | `string` | có | `—` | AutoCAD command string (e.g. '_ZOOM E', '_REGEN', '_EXPLODE') |

**Ví dụ gọi**

```json
{
  "command": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `system_run_lisp`

**Nhóm:** `system`  
**Làm gì:** Execute an AutoLISP expression (COM backend only).

Example: '(setvar "DIMSCALE" 1.0)'

A symbol denylist refuses the known code-execution and file-I/O channels;
text inside double quotes is treated as data, so drawing notes are not
mistaken for code. It is a guardrail, NOT a security boundary — AutoLISP has
more write channels than any denylist enumerates. Prefer the typed tools.

**Dùng khi nào:** Khi cần chẩn đoán server hoặc trạng thái kết nối.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `expression` | `string` | có | `—` | AutoLISP expression to evaluate (e.g. '(command "ZOOM" "E")') |

**Ví dụ gọi**

```json
{
  "expression": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `system_set_variable`

**Nhóm:** `system`  
**Làm gì:** Set an AutoCAD system variable (e.g. DIMSCALE, LTSCALE, MEASUREMENT).

Refusals, before anything is written: a value outside the catalogued
range or enum of a known variable, or a write to a read-only variable
(DIMSTYLE, CANNOSCALEVALUE, DWGNAME, …), is refused with the catalogue's
message — `system_variable_describe(name)` shows the range. A variable the
catalogue does not know is passed through unchanged. The headless engine
additionally refuses registry-saved variables (`capability:
registry_sysvar`) because a file has nowhere to keep them, and names that
ezdxf has no header slot for (a `ValueError` naming the variable).

**Dùng khi nào:** Khi cần chẩn đoán server hoặc trạng thái kết nối.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | System variable name |
| `value` | `any` | có | `—` | New variable value |

**Ví dụ gọi**

```json
{
  "name": "example",
  "value": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `system_status`

**Nhóm:** `system`  
**Làm gì:** Get full status of the AutoCAD MCP Pro server and backend connection.

Returns backend name, connection status, capabilities, document info.

**Dùng khi nào:** Khi cần chẩn đoán server hoặc trạng thái kết nối.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `system_variable_describe`

**Nhóm:** `environment`  
**Làm gì:** What an AutoCAD system variable means, from an authored catalogue of 90.

With `name`: `{known, name, type, range|enum, default, meaning, saved_in
(drawing|registry|not_saved), engines: {ezdxf, com}, friendly_key,
read_only}` plus `current` when the active backend can read it (omitted,
with `current_unavailable`, when it cannot — no document open, or a
registry variable headlessly). An unknown name is never an error: `known:
false` and the nearest catalogue names come back. With `search`: every row
whose name or meaning contains all the words. With neither: the index of
names. `friendly_key` names the `drawing_settings` key that wraps the
variable, which is the preferred way to set it; `engines.ezdxf: false`
means the headless engine refuses a write (registry-saved, or no header
slot in ezdxf).

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `any` | không | `None` | System variable name, e.g. LTSCALE (case-insensitive, '$' optional) |
| `search` | `any` | không | `None` | Free text matched against names and meanings, e.g. 'decimal separator' |

**Ví dụ gọi**

```json
{
  "name": null,
  "search": null
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `takeoff_compute`

**Nhóm:** `cadtroly`  
**Làm gì:** Bước 3 luồng A: tính khối lượng. Mỗi dòng có nguồn truy vết và tin cậy; thiếu dữ liệu thì để trống.

**Dùng khi nào:** Khi cần dùng chức năng `takeoff_compute` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `path` | `string` | có | `—` | — |
| `height_m` | `any` | không | `None` | Chiều cao tầng (m); bỏ trống = tìm text H= |
| `tru_lo_cua_m3` | `number` | không | `0.0` | — |

**Ví dụ gọi**

```json
{
  "path": "D:\\DuAn\\drawing.dwg",
  "height_m": null,
  "tru_lo_cua_m3": 0.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `takeoff_decide`

**Nhóm:** `cadtroly`  
**Làm gì:** Kỹ sư xác nhận ánh xạ một nhóm. Mặc định lưu thành quy tắc đơn vị (không train, chỉ ghi file).

**Dùng khi nào:** Khi cần dùng chức năng `takeoff_decide` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `path` | `string` | có | `—` | — |
| `kind` | `string` | có | `—` | layer | block |
| `name` | `string` | có | `—` | — |
| `cong_tac` | `string` | có | `—` | — |
| `don_vi` | `string` | có | `—` | — |
| `cach_tinh` | `string` | có | `—` | — |
| `tham_so` | `any` | không | `None` | — |
| `save_rule` | `boolean` | không | `True` | Lưu thành quy tắc đơn vị để lần sau tự áp |

**Ví dụ gọi**

```json
{
  "path": "D:\\DuAn\\drawing.dwg",
  "kind": "example",
  "name": "example",
  "cong_tac": "example",
  "don_vi": "example",
  "cach_tinh": "example",
  "tham_so": null,
  "save_rule": true
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `takeoff_export`

**Nhóm:** `cadtroly`  
**Làm gì:** Bước 4 luồng A: xuất Excel 4 sheet (Khối lượng, Chi tiết từng handle + lệnh zoom, Ánh xạ, Kiểm soát).

**Dùng khi nào:** Khi cần dùng chức năng `takeoff_export` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `path` | `string` | có | `—` | — |
| `out` | `any` | không | `None` | File .xlsx; bỏ trống = kho/out/<ten>.xlsx |
| `height_m` | `any` | không | `None` | — |

**Ví dụ gọi**

```json
{
  "path": "D:\\DuAn\\drawing.dwg",
  "out": null,
  "height_m": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `takeoff_propose`

**Nhóm:** `cadtroly`  
**Làm gì:** Bước 2 luồng A: gom theo layer/block, đề xuất công tác với tin cậy A/B/C. B/C cần kỹ sư quyết.

**Dùng khi nào:** Khi cần dùng chức năng `takeoff_propose` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `path` | `string` | có | `—` | — |

**Ví dụ gọi**

```json
{
  "path": "D:\\DuAn\\drawing.dwg"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `takeoff_run`

**Nhóm:** `cadtroly`  
**Làm gì:** Chạy trọn luồng A không hỏi (dùng quy tắc đã có). Thư mục → mỗi file một Excel. Nhóm B/C vẫn ghi rõ trong Excel.

**Dùng khi nào:** Khi cần dùng chức năng `takeoff_run` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `path` | `string` | có | `—` | File DXF hoặc thư mục |
| `height_m` | `any` | không | `None` | — |

**Ví dụ gọi**

```json
{
  "path": "D:\\DuAn\\drawing.dwg",
  "height_m": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `template_apply_layers`

**Nhóm:** `templates`  
**Làm gì:** Apply a standard layer set from a predefined template.

Available templates: architectural, mechanical, electrical, piping.
Creates all layers defined in the template with standard colors and lineweights.

**Dùng khi nào:** Khi tạo bản vẽ từ template hoặc mẫu có sẵn.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `template` | `string` | có | `—` | Template name: architectural, mechanical, electrical, piping |

**Ví dụ gọi**

```json
{
  "template": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `template_list`

**Nhóm:** `templates`  
**Làm gì:** List all available layer templates and their contents.

**Dùng khi nào:** Khi tạo bản vẽ từ template hoặc mẫu có sẵn.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `text_find_replace`

**Nhóm:** `entity_modification`  
**Làm gì:** Replace text in TEXT, MTEXT and block attributes (ATTRIB and ATTDEF).

`searched_types` is on the response because "no matches" and "that type was
never searched" are different answers. Block *definitions* are included, so
the next insert does not reintroduce the old text. DIMENSION text is out of
scope: its text field holds the `<>` override placeholder rather than the
measurement, so editing it would break the association. A multi-line
attribute is matched and rewritten as the whole value (`Line1\PLine2`),
the same value `block_get_attributes` reports and `block_explode` bursts.

**Dùng khi nào:** Khi cần sửa, di chuyển, xoay, scale hoặc biến đổi đối tượng.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `find` | `string` | có | `—` | Literal text to search for (not a regex). |
| `replace` | `string` | có | `—` | Replacement text. |
| `layer` | `string` | không | `` | Restrict to one layer. Empty searches every layer. |
| `match_case` | `boolean` | không | `True` | Case-sensitive search. |
| `dry_run` | `boolean` | không | `False` | Report what would change without changing it. |

**Ví dụ gọi**

```json
{
  "find": "example",
  "replace": "example",
  "layer": "",
  "match_case": true,
  "dry_run": false
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `text_set_background`

**Nhóm:** `entity_modification`  
**Làm gì:** Mask what is behind an MTEXT so it stays readable over hatch or geometry.

MTEXT only: TEXT has no background-fill attribute, so setting one on it
would report success and change nothing.

**Dùng khi nào:** Khi cần sửa, di chuyển, xoay, scale hoặc biến đổi đối tượng.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Handle of an MTEXT entity. |
| `enabled` | `boolean` | không | `True` | False removes the background box. |
| `color` | `integer` | không | `0` | ACI background colour (1-255). 0 uses the drawing background. |
| `scale` | `number` | không | `1.5` | Box size as a multiple of the text box; must be >= 1. |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "enabled": true,
  "color": 0,
  "scale": 1.5
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `textstyle_create`

**Nhóm:** `styles`  
**Làm gì:** Create a text style.

Headlessly a font nobody can find is *written* and reported
`font_resolved: false` (AutoCAD substitutes at open; the headless
renderer falls back), because a DXF stores only the name. The live
engine cannot do that: ActiveX refuses a font AutoCAD cannot open, so a
file that is neither on its support path nor in the Windows Fonts folder
is refused there before any write (the message names the folders and the
presets); a TrueType font is written by its typeface (`SetFont`, what the
STYLE dialog does — the record carries `arial.ttf`, never a machine
path), an SHX by the file name. Refuses, before any write on both
engines: a name that exists, an empty font, `width_factor <= 0`,
`height < 0`, an oblique angle outside ±85°.

**Dùng khi nào:** Khi quản lý text style, dimension style, linetype và kiểu hiển thị.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | New text style name, e.g. ISOCP |
| `font` | `string` | có | `—` | isocp.shx | isocpeur.ttf | arial.ttf | romans.shx (name or file, any case) or any font file |
| `height` | `number` | không | `0.0` | Fixed height; 0 = ask per text |
| `width_factor` | `number` | không | `1.0` | Width factor |
| `oblique_deg` | `number` | không | `0.0` | Obliquing angle in degrees, -85..85 |
| `set_current` | `boolean` | không | `False` | Also make it the current text style |

**Ví dụ gọi**

```json
{
  "name": "example",
  "font": "example",
  "height": 0.0,
  "width_factor": 1.0,
  "oblique_deg": 0.0,
  "set_current": false
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `textstyle_list`

**Nhóm:** `styles`  
**Làm gì:** Every STYLE table entry and the one new TEXT/MTEXT will use.

**Dùng khi nào:** Khi quản lý text style, dimension style, linetype và kiểu hiển thị.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `textstyle_set_current`

**Nhóm:** `styles`  
**Làm gì:** Set `$TEXTSTYLE`; `entity_create_text` / `entity_create_mtext` then
carry the style on both engines. Refuses a style the drawing does not
hold. Returns `previous` and `changed`.

**Dùng khi nào:** Khi quản lý text style, dimension style, linetype và kiểu hiển thị.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | Text style to make current (case-insensitive) |

**Ví dụ gọi**

```json
{
  "name": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `titleblock_apply`

**Nhóm:** `sheet`  
**Làm gì:** ISO 7200 title block, 180 mm wide, in the lower-right corner of any
A4-A0 sheet. The title text is used verbatim.

Carries the ISO 128-30 projection-angle symbol: 'first' draws the cone on
the left and the concentric circles on the right, 'third' is its mirror.
Refusals, all before the first entity: an unknown size (the five covered
sizes are listed), an unknown orientation, a projection that is not
'first'/'third'/'', a `layout` that does not exist. `titleblock_apply_iso_a3`
is this tool with size='A3' and no symbol, kept so no caller breaks.

**Dùng khi nào:** Khi tạo và quản lý sheet, title block và hồ sơ phát hành.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `title` | `string` | có | `—` | Drawing title (verbatim, no transformation). |
| `drawing_no` | `string` | có | `—` | Identification number, e.g. 'AM-2026-001'. |
| `size` | `string` | không | `A3` | ISO 216 sheet: A4, A3, A2, A1 or A0. |
| `orientation` | `string` | không | `landscape` | 'landscape' or 'portrait'. |
| `projection` | `string` | không | `first` | Projection-angle symbol: 'first' (ISO/European, the default), 'third' (ANSI), or '' for no symbol. |
| `part_no` | `string` | không | `` | — |
| `material` | `string` | không | `` | — |
| `scale` | `string` | không | `1:1` | — |
| `units` | `string` | không | `mm` | — |
| `drawn_by` | `string` | không | `` | — |
| `checked_by` | `string` | không | `` | — |
| `date` | `string` | không | `` | — |
| `sheet` | `string` | không | `1/1` | — |
| `revision` | `string` | không | `A` | — |
| `company` | `string` | không | `Anka-Makine` | — |
| `frame` | `boolean` | không | `True` | Also draw the ISO 5457 frame around the block. |
| `zones` | `boolean` | không | `False` | Add the zone grid to that frame. |
| `marks` | `boolean` | không | `False` | Add the centring and trimming marks. |
| `origin_x` | `number` | không | `0.0` | — |
| `origin_y` | `number` | không | `0.0` | — |
| `layout` | `string` | không | `` | Paper-space layout to draw the sheet on; empty draws in the current space. |

**Ví dụ gọi**

```json
{
  "title": "example",
  "drawing_no": "example",
  "size": "A3",
  "orientation": "landscape",
  "projection": "first",
  "part_no": "",
  "material": "",
  "scale": "1:1",
  "units": "mm",
  "drawn_by": "",
  "checked_by": "",
  "date": "",
  "sheet": "1/1",
  "revision": "A",
  "company": "Anka-Makine",
  "frame": true,
  "zones": false,
  "marks": false,
  "origin_x": 0.0,
  "origin_y": 0.0,
  "layout": ""
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `titleblock_apply_iso_a3`

**Nhóm:** `engineering`  
**Làm gì:** ISO 7200 / A3 (420x297 mm) title block. Title text is used verbatim.

Pass `layout` to put the sheet on a paper-space layout, which is where a
title block belongs — the border frames the printed sheet, not the model.
Your current space is restored afterwards, so asking for a border does not
move you onto the sheet.

**Dùng khi nào:** Khi cần kiểm tra hoặc thao tác theo yêu cầu kỹ thuật.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `title` | `string` | có | `—` | Drawing title (verbatim, no LLM transformation). |
| `drawing_no` | `string` | có | `—` | Drawing number (e.g. 'AM-2026-001'). |
| `part_no` | `string` | không | `` | — |
| `material` | `string` | không | `` | — |
| `scale` | `string` | không | `1:1` | — |
| `units` | `string` | không | `mm` | — |
| `drawn_by` | `string` | không | `` | — |
| `checked_by` | `string` | không | `` | — |
| `date` | `string` | không | `` | — |
| `sheet` | `string` | không | `1/1` | — |
| `revision` | `string` | không | `A` | — |
| `company` | `string` | không | `Anka-Makine` | — |
| `origin_x` | `number` | không | `0.0` | — |
| `origin_y` | `number` | không | `0.0` | — |
| `layout` | `string` | không | `` | Paper-space layout to draw the sheet on (create it with layout_create). Empty draws in the current space, as before. |

**Ví dụ gọi**

```json
{
  "title": "example",
  "drawing_no": "example",
  "part_no": "",
  "material": "",
  "scale": "1:1",
  "units": "mm",
  "drawn_by": "",
  "checked_by": "",
  "date": "",
  "sheet": "1/1",
  "revision": "A",
  "company": "Anka-Makine",
  "origin_x": 0.0,
  "origin_y": 0.0,
  "layout": ""
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `transaction_begin`

**Nhóm:** `transactions`  
**Làm gì:** Begin a transaction (undo mark).

COM backend: Sets AutoCAD undo mark. All subsequent operations can be
rolled back to this point with transaction_rollback.

ezdxf backend: Saves a DXF snapshot. Rollback restores the full document
state to this point.

Always pair with transaction_commit or transaction_rollback.

**Dùng khi nào:** Khi muốn gom thay đổi thành giao dịch có thể xác nhận hoặc hoàn tác.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `transaction_commit`

**Nhóm:** `transactions`  
**Làm gì:** Commit the current transaction.

COM: Ends the undo mark (changes are permanent but still undoable via drawing_undo).
ezdxf: Discards the rollback snapshot (changes are kept).

**Dùng khi nào:** Khi muốn gom thay đổi thành giao dịch có thể xác nhận hoặc hoàn tác.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `transaction_rollback`

**Nhóm:** `transactions`  
**Làm gì:** Rollback the current transaction to the point of transaction_begin.

COM: Undoes all operations back to the UNDO Mark transaction_begin set;
refused (`ok: false`) when no transaction is active.
ezdxf: Restores the document from the saved DXF snapshot.

WARNING: This is destructive – all changes since transaction_begin are lost.

**Dùng khi nào:** Khi muốn gom thay đổi thành giao dịch có thể xác nhận hoặc hoàn tác.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `ucs_list`

**Nhóm:** `environment`  
**Làm gì:** The `world` row first, then every UCS table entry with origin and unit
axes, `current` on the active one. `world` is current only when the frame
IS the WCS (WORLDUCS live, the `$UCS*` header headless) — an unnamed UCS
(`UCS Origin` / `3P` without saving) has an empty name too and is
reported as a trailing row with `name: null` and its origin/axes, so
`current` is `null` then and never `world`. Tool coordinates stay WCS on
both engines whatever is current. No refusals. Pack: settings · lean: no.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `ucs_restore`

**Nhóm:** `environment`  
**Làm gì:** Live: `ActiveUCS` for a named entry; `world` runs `UCS World`, which is
refused while AutoCAD has an active command (CMDACTIVE — press ESC).
Headless: the `$UCSNAME/$UCSORG/$UCSXDIR/$UCSYDIR` header variables.
Refusal: an unknown name (lists the saved ones). Tool coordinates stay
WCS. Pack: settings · lean: no.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | A name from ucs_list, or `world` |

**Ví dụ gọi**

```json
{
  "name": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `ucs_set`

**Nhóm:** `environment`  
**Làm gì:** Store a UCS table entry and make it current (AutoCAD's UCS command).

Axes are normalised to unit vectors. **Every tool keeps taking and
returning WCS coordinates** — the repository rule; a UCS is for the
operator's own drafting, and no tool starts interpreting inputs in it.
Refusals, before any write: a name of `world` (reserved), a zero-length
axis, and non-perpendicular axes — the message carries the measured angle
(tolerance 0.001°). Pack: settings · lean: no.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | UCS name |
| `origin` | `array<number>` | có | `—` | [x, y, z] in WCS |
| `x_axis` | `array<number>` | có | `—` | Direction of the new X axis (any length) |
| `y_axis` | `array<number>` | có | `—` | Direction of the new Y axis; must be perpendicular to x_axis |

**Ví dụ gọi**

```json
{
  "name": "example",
  "origin": [],
  "x_axis": [],
  "y_axis": []
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `user_pick_point`

**Nhóm:** `environment`  
**Làm gì:** `Utility.GetPoint`: returns the WCS `x`, `y` (`z`) the operator clicks.

ESC is an answer, not an error: `cancelled: true` with AutoCAD's reason.
Waiting longer than `COM_CALL_TIMEOUT` returns `timed_out: true` (the
prompt is abandoned on AutoCAD's side; press ESC there). Refusals: an
empty prompt; headless, `capability: "interactive_prompt"` (no operator).
Pack: settings · lean: no.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `prompt` | `string` | có | `—` | Shown on the command line, e.g. 'Pick the base point' |

**Ví dụ gọi**

```json
{
  "prompt": "example"
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `user_select`

**Nhóm:** `environment`  
**Làm gì:** Returns `handles` the operator picked — one with `mode="single"` (plus
the `picked` point `[x, y]` in **WCS** — AutoCAD reports it in the current
UCS and the tool translates, so a UCS made current by `ucs_set` never
shifts it), any number with `mode="multiple"` (Enter with nothing
selected is `count: 0`, not a cancel). ESC → `cancelled: true`; a wait
longer than `COM_CALL_TIMEOUT` → `timed_out: true`. Refusals: a mode
outside the two, an empty prompt; headless, `capability:
"interactive_prompt"`. Pack: settings · lean: no.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `prompt` | `string` | có | `—` | Shown on the command line |
| `mode` | `string` | không | `single` | single (GetEntity) | multiple (SelectOnScreen) |

**Ví dụ gọi**

```json
{
  "prompt": "example",
  "mode": "single"
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `validation_check`

**Nhóm:** `validation`  
**Làm gì:** Run quality checks on the current drawing.

Available checks:
- empty_layers: Find layers with no entities
- zero_length: Find zero-length lines
- duplicate_entities: Find entities at the same position

**Dùng khi nào:** Khi kiểm tra tính hợp lệ và lỗi kỹ thuật của bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `checks` | `array<string>` | không | `None` | List of checks: empty_layers, zero_length, duplicate_entities |

**Ví dụ gọi**

```json
{
  "checks": null
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `view_named_list`

**Nhóm:** `environment`  
**Làm gì:** Every VIEW table entry with centre, height and width. No refusals.
Pack: settings · lean: no.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `view_named_restore`

**Nhóm:** `environment`  
**Làm gì:** Live: zooms the active viewport to the saved window the way `-VIEW _R`
does — VIEWCTR becomes the saved centre and VIEWSIZE the saved height
(or width / display aspect when the window is wider than the display);
`applied: "zoom_window"` plus the read-back `viewctr` / `viewsize`.
Headless there is no display: the saved window is fitted into the
`*Active` VPORT — the view AutoCAD opens the file on — whose aspect ratio
is left as the file carries it (AutoCAD reconciles a changed aspect by the
viewport's lower-left corner, which shifts the centre); the result says
`applied: "header_only"` with the written `vport_height` and the kept
`aspect_ratio`, the same reported-no-op rule as `view_zoom_extents`.
Refusal: an unknown name (lists the saved views). Pack: settings · lean:
no.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | A name from view_named_list |

**Ví dụ gọi**

```json
{
  "name": "example"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `view_named_save`

**Nhóm:** `environment`  
**Làm gì:** Store a VIEW table entry (AutoCAD's VIEW command). Same name replaces
(`replaced: true`). Refusals: `height`/`width` ≤ 0 or non-finite, a
malformed `center`, and headless an empty drawing with no `center`/`height`
(there are no extents to default to). Pack: settings · lean: no.

**Dùng khi nào:** Khi cần kiểm tra phiên AutoCAD, backend, biến môi trường hoặc cấu hình.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `name` | `string` | có | `—` | View name, e.g. DETAIL-A |
| `center` | `any` | không | `None` | [x, y] in WCS; default: the current view (live) or the drawing extents (headless) |
| `height` | `any` | không | `None` | View height in drawing units; default as for center |
| `width` | `any` | không | `None` | View width; default: height × the current viewport aspect |

**Ví dụ gọi**

```json
{
  "name": "example",
  "center": null,
  "height": null,
  "width": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `view_render_report`

**Nhóm:** `cadtroly`  
**Làm gì:** Return render coverage before relying on a preview for QA.

The report is deliberately conservative: common 2D entities are marked as
covered, while uncommon/proxy/3D types are surfaced for manual checking.
It never claims that a PNG proves the full DWG was rendered.

**Dùng khi nào:** Khi cần dùng chức năng `view_render_report` trong quy trình CAD.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `view_screenshot`

**Nhóm:** `view`  
**Làm gì:** Capture a screenshot of the current drawing view.

COM backend: captures live AutoCAD window at current view.
ezdxf backend: renders via matplotlib to PNG.

With `overlay_handles`, each entity is labelled with its handle at its own
centre — every modify tool takes a handle, and without the labels there is
nothing connecting "the circle at the top-left" to a hex string you can act
on. Crowded drawings are capped and the image says how many of how many were
labelled. Live AutoCAD captures its own window, so there is no render to
label there; it refuses with `capability: "handle_overlay"`.

Returns an Image content block with the PNG data.

**Dùng khi nào:** Khi đổi góc nhìn, zoom, chụp ảnh hoặc render vùng bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `overlay_handles` | `boolean` | không | `False` | Label each entity with its handle, so what you see maps to what you can modify. Headless backend only. |

**Ví dụ gọi**

```json
{
  "overlay_handles": false
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `view_zoom_and_screenshot`

**Nhóm:** `view`  
**Làm gì:** Zoom to extents (or window if coordinates given), then capture a screenshot.

The most useful tool for visually inspecting drawing state.

**Dùng khi nào:** Khi đổi góc nhìn, zoom, chụp ảnh hoặc render vùng bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `x1` | `any` | không | `None` | Optional: zoom to this window corner X1 |
| `y1` | `any` | không | `None` | Optional: zoom to window corner Y1 |
| `x2` | `any` | không | `None` | Optional: zoom to window corner X2 |
| `y2` | `any` | không | `None` | Optional: zoom to window corner Y2 |

**Ví dụ gọi**

```json
{
  "x1": null,
  "y1": null,
  "x2": null,
  "y2": null
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `view_zoom_extents`

**Nhóm:** `view`  
**Làm gì:** Zoom to show all entities in the drawing (fit drawing in viewport).

**Dùng khi nào:** Khi đổi góc nhìn, zoom, chụp ảnh hoặc render vùng bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| — | — | — | — | Tool không yêu cầu tham số. |

**Ví dụ gọi**

```json
{}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `view_zoom_window`

**Nhóm:** `view`  
**Làm gì:** Zoom to display the specified rectangular window region.

**Dùng khi nào:** Khi đổi góc nhìn, zoom, chụp ảnh hoặc render vùng bản vẽ.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `x1` | `number` | có | `—` | Window corner 1 X |
| `y1` | `number` | có | `—` | Window corner 1 Y |
| `x2` | `number` | có | `—` | Window corner 2 X |
| `y2` | `number` | có | `—` | Window corner 2 Y |

**Ví dụ gọi**

```json
{
  "x1": 1.0,
  "y1": 1.0,
  "x2": 1.0,
  "y2": 1.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `viewport_create`

**Nhóm:** `layouts`  
**Làm gì:** Place a scaled model-space viewport on a paper-space layout.

The viewport window shows the model region centered at
(view_center_x, view_center_y); view height = height / scale.

**Dùng khi nào:** Khi quản lý layout, viewport và không gian giấy.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `layout` | `string` | có | `—` | Paper-space layout that receives the viewport. |
| `center_x` | `number` | có | `—` | Viewport center X in paper units. |
| `center_y` | `number` | có | `—` | Viewport center Y in paper units. |
| `width` | `number` | có | `—` | Viewport width in paper units. |
| `height` | `number` | có | `—` | Viewport height in paper units. |
| `view_center_x` | `number` | có | `—` | Model-space X the viewport looks at. |
| `view_center_y` | `number` | có | `—` | Model-space Y the viewport looks at. |
| `scale` | `number` | không | `1.0` | Paper:model scale (1.0 = 1:1, 0.5 = 1:2, 2.0 = 2:1). |

**Ví dụ gọi**

```json
{
  "layout": "example",
  "center_x": 1.0,
  "center_y": 1.0,
  "width": 1.0,
  "height": 1.0,
  "view_center_x": 1.0,
  "view_center_y": 1.0,
  "scale": 1.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `viewport_delete`

**Nhóm:** `layouts`  
**Làm gì:** Delete a viewport.

The layout's main viewport needs `force=true`; deleting it removes the tab's
own view state, and the layout's current-viewport pointer is repaired so the
file does not carry a dangling reference that only CAD would notice.

**Dùng khi nào:** Khi quản lý layout, viewport và không gian giấy.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Viewport entity handle (from viewport_list). |
| `force` | `boolean` | không | `False` | Allow deleting the layout's main viewport. |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "force": false
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `viewport_list`

**Nhóm:** `layouts`  
**Làm gì:** List paper-space viewports: handle, geometry, scale and lock state.

The layout's own main viewport is included with `is_main: true` — it is the
tab's pan/zoom state rather than a drafting viewport, and it is what remains
after every drafting viewport is deleted. `scale` and `locked` are null on
documents that cannot store them (R12) rather than fabricated.

**Dùng khi nào:** Khi quản lý layout, viewport và không gian giấy.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `layout` | `string` | không | `` | Restrict to one paper-space layout. Empty covers every sheet. |

**Ví dụ gọi**

```json
{
  "layout": ""
}
```

**Lưu ý:** Chỉ đọc; có thể dùng trước khi chỉnh sửa.

### `viewport_lock`

**Nhóm:** `layouts`  
**Làm gì:** Lock or unlock a viewport's display scale.

**Dùng khi nào:** Khi quản lý layout, viewport và không gian giấy.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Viewport entity handle (from viewport_list). |
| `locked` | `boolean` | không | `True` | True to lock the display scale, False to unlock. |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "locked": true
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `viewport_set_scale`

**Nhóm:** `layouts`  
**Làm gì:** Rescale a viewport by adjusting its view height.

Geometric scale only: annotative text and dimensions do not resize with it.
Refuses the layout's main viewport, whose view height is the tab's own
pan/zoom state rather than a drafting scale.

**Dùng khi nào:** Khi quản lý layout, viewport và không gian giấy.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `handle` | `string` | có | `—` | Viewport entity handle (from viewport_list). |
| `scale` | `number` | có | `—` | Paper:model scale (1.0 = 1:1, 0.5 = 1:2, 0.02 = 1:50). |

**Ví dụ gọi**

```json
{
  "handle": "A1B2",
  "scale": 1.0
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `weld_symbol`

**Nhóm:** `mechanical`  
**Làm gì:** Draw an ISO 2553 weld annotation: reference line, identification line, symbol, dimensions.

Refusals, all before the first entity reaches the drawing: a `kind` outside
the six elementary symbols transcribed here (square, v, bevel, u, j,
fillet — the rest of the ISO 2553 table is deliberately not shipped rather
than guessed), a `side` outside arrow/other/both, a non-positive `height`,
and a `pitch` given without a `length`.

**Dùng khi nào:** Khi dựng hoặc kiểm tra bản vẽ cơ khí, chi tiết và dung sai.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `x` | `number` | có | `—` | Kink X (WCS) — where the arrow line meets the reference line. |
| `y` | `number` | có | `—` | Kink Y (WCS). |
| `kind` | `string` | không | `fillet` | Elementary symbol: square | v | bevel | u | j | fillet. |
| `size` | `any` | không | `None` | Written before the symbol. A number on a fillet takes the ISO 2553 design-throat prefix (5 → 'a5'); pass a string for leg length ('z7'). |
| `length` | `any` | không | `None` | Weld length (mm), written after the symbol. |
| `pitch` | `any` | không | `None` | Pitch (mm) of an intermittent weld, written in brackets after the length. |
| `side` | `string` | không | `arrow` | arrow (symbol on the reference line) | other (on the dashed identification line) | both (symmetrical; the identification line is omitted, per ISO 2553:2019). |
| `field_weld` | `boolean` | không | `False` | Flag at the kink: weld made on site. |
| `all_around` | `boolean` | không | `False` | Circle at the kink: weld all around. |
| `process` | `any` | không | `None` | Tail reference, e.g. an ISO 4063 process number. |
| `leader_to` | `any` | không | `None` | [x, y] on the joint; draws a leader with an arrowhead there. |
| `height` | `number` | không | `3.5` | Text height (mm). |
| `rotation` | `number` | không | `0.0` | Rotate the whole annotation about the kink (degrees CCW). |
| `layer` | `any` | không | `None` | Override the role layers (DIM for geometry, TEXT for text). |

**Ví dụ gọi**

```json
{
  "x": 1.0,
  "y": 1.0,
  "kind": "fillet",
  "size": null,
  "length": null,
  "pitch": null,
  "side": "arrow",
  "field_weld": false,
  "all_around": false,
  "process": null,
  "leader_to": null,
  "height": 3.5,
  "rotation": 0.0,
  "layer": null
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `xref_attach`

**Nhóm:** `sheet`  
**Làm gì:** Attach an external reference and insert it once. Both engines.

The block takes the referenced file's stem as its name. Refusals, all
before anything is written: a `kind` that is not 'attach' or 'overlay', a
file that does not exist, a non-positive or non-finite scale, and a block
name the drawing already holds — detach it first with
`xref_manage(action='detach')`.

**Dùng khi nào:** Khi tạo và quản lý sheet, title block và hồ sơ phát hành.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `path` | `string` | có | `—` | Full path of the drawing to reference. |
| `x` | `number` | không | `0.0` | Insertion X (WCS). |
| `y` | `number` | không | `0.0` | Insertion Y (WCS). |
| `scale` | `number` | không | `1.0` | Uniform scale. |
| `rotation` | `number` | không | `0.0` | Rotation in degrees, CCW from +X. |
| `kind` | `string` | không | `attach` | 'attach' (the reference's own xrefs come with it) or 'overlay' (they do not, so a circular reference cannot form). |

**Ví dụ gọi**

```json
{
  "path": "D:\\DuAn\\drawing.dwg",
  "x": 0.0,
  "y": 0.0,
  "scale": 1.0,
  "rotation": 0.0,
  "kind": "attach"
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

### `xref_manage`

**Nhóm:** `sheet`  
**Làm gì:** One operation on one external reference.

`list`, `detach` and `path` work on both engines. `reload` and `bind` need
a live AutoCAD seat's xref manager: headlessly they are refused with
`capability: "xref_live"` rather than pretended, and the refusal says which
engine does them. Other refusals: an action outside the five, an unknown
xref name, a 'path' action with no `new_path`. On the live engine a listed
row's `inserts` and `kind` are both null — ActiveX's block interface
carries neither a per-xref insert count nor an overlay indicator, and this
server does not invent them. Headlessly both are measured: `inserts`
counts every insert in the drawing, model space and paper space alike, and
`detach` removes exactly those.

**Dùng khi nào:** Khi tạo và quản lý sheet, title block và hồ sơ phát hành.

**Tham số**

| Tên | Kiểu | Bắt buộc | Mặc định | Ý nghĩa |
|---|---|---:|---|---|
| `action` | `string` | có | `—` | list | reload | bind | detach | path. |
| `name` | `string` | không | `` | Xref name; ignored by 'list'. |
| `new_path` | `string` | không | `` | Required by 'path': the reference's new location. |

**Ví dụ gọi**

```json
{
  "action": "example",
  "name": "",
  "new_path": ""
}
```

**Lưu ý:** Có thể thay đổi bản vẽ hoặc trạng thái; nên chụp/đọc bản vẽ trước và lưu ra file đích riêng.

# 5. Kho, tiêu chuẩn, skill

[← Mục lục tài liệu](README.md)

## Hai lớp kho

| Lớp | Nơi | Nội dung | Sửa được? |
|---|---|---|---|
| Mặc định | `app/kho-mac-dinh/` (bản ZIP: `code\kho-mac-dinh`) | Tiêu chuẩn, quy tắc chuẩn công ty, 16 skill | Không — đi kèm mã, thay khi cập nhật |
| Người dùng | `CADTROLY_KHO` (mặc định `~/CAD-kho`) | Log, Excel xuất ra, tiêu chuẩn/quy tắc/skill bổ sung | Có — không bị cập nhật đụng tới |

```
CAD-kho/
  tieu-chuan/   <id>.rules.json   bảng quy tắc bóc từ tiêu chuẩn, mỗi dòng có duyet true/false
  quy-tac/      anh-xa.json       ánh xạ layer/block → công tác, lớn dần khi kỹ sư xác nhận
                <id>.rules.json   chuẩn công ty
  chi-tiet/                       chi tiết tham số
  du-an-cu/<ten>/ho-so.json       hồ sơ dự án cũ
  skill/<ten>/SKILL.md            skill bổ sung (thêm file .disabled để tắt)
  log/                            nhật ký thao tác JSONL theo ngày
  out/                            Excel và file xuất
```

Mẫu trong `app/samples/kho/`. Kho là thư mục thường, không train mô hình; xem trạng thái bằng *"cho biết trạng thái kho"*
(`knowledge_status`).

## Tiêu chuẩn theo ngành

MCP có danh mục **18 ngành** (kiến trúc, kết cấu, cầu đường, cơ khí, điện, HVAC, P&ID, cấp thoát nước, PCCC, plant, hạ tầng…).
Chi tiết tiêu chuẩn tham chiếu và giới hạn an toàn: [STANDARDS-SAFETY-BY-INDUSTRY.md](../app/docs/STANDARDS-SAFETY-BY-INDUSTRY.md).

| Việc | Câu lệnh | Tool |
|---|---|---|
| Xem ngành | "Liệt kê các ngành đang có." | `knowledge_industries` |
| Liệt kê tiêu chuẩn | "Liệt kê tiêu chuẩn ngành fire và structural, kèm phiên bản, nguồn, ngày hiệu lực, số rule." | `knowledge_standards` |
| Thêm | "Thêm tiêu chuẩn fire-demo vào kho người dùng, ngành fire, phiên bản 2026.1, nguồn dự án; không ghi đè." | `knowledge_standard_add` |
| Xoá | "Xoá tiêu chuẩn fire-demo do người dùng thêm. Chỉ xoá sau khi tôi xác nhận." | `knowledge_standard_delete` (`confirm=true`) |
| Kiểm tra theo chuẩn | "Kiểm tra bản vẽ theo chuan-cong-ty." | `check_rulesets`, `check_run` |
| Tra chuẩn CAD | "Tra quy ước layer cho bản vẽ cầu." | `standards_reference` |

- Tiêu chuẩn mới được ghi vào `CAD-kho/tieu-chuan`. Tiêu chuẩn mặc định trong MCP **không xoá được**.
- Một dòng quy tắc chỉ có hiệu lực khi `duyet=true`; `check_run` bỏ qua dòng chưa duyệt.
- Có nhiều lựa chọn hoặc chưa rõ Việt Nam/quốc tế thì MCP phải hỏi lại.
- `tieu-chuan/qcvn-18-2021.rules.json` hiện là **mẫu**, chưa bóc từ văn bản thật.

## Skill

Skill là hướng dẫn chuyên ngành dạng `SKILL.md` mà LLM đọc trước khi làm (resource `cadtroly://skill/{name}`).

| Skill mặc định | Việc |
|---|---|
| `suc-khoe-ban-ve` | Kiểm tra trước khi sửa/bóc/phát hành: xref, đơn vị, layer, đối tượng lỗi, độ phủ ảnh — chỉ đọc |
| `qa-ban-ve-toan-dien` | Điều phối QA PDF/DWG/DXF, layer, annotation, kết cấu, đường-cầu, hồ sơ, sửa trước/sau |
| `quan-tri-layer-cad` | Tách và quản trị layer |
| `tai-tao-pdf-sang-cad` | Dựng PDF thành CAD sửa được |
| `annotation-dim-qa` | Kiểm tra text, dim, hatch, tỷ lệ |
| `bo-tri-ho-so-thiet-ke` | Tên file, sheet, revision |
| `kiem-tra-ban-ve-civil-bridge` | Kiểm tra bản vẽ đường và cầu, bóc đào đắp và thép |
| `kiem-tra-ket-cau` | Kiểm tra layer/hình học kết cấu, đề xuất tối ưu |
| `tinh-toan-chiu-luc` | Chuẩn bị dữ liệu và tính sơ bộ có giả định; không thay hồ sơ tính được phê duyệt |
| `an-toan-ket-cau` | Rà soát liên tục cấu kiện, dấu hiệu mất an toàn |
| `an-toan-cad-chuyen-sau` | Quy tắc an toàn khi thao tác CAD |
| `kiem-tra-pccc` | Rà soát sơ bộ lối thoát, khoang cháy, tiếp cận, ký hiệu PCCC |
| `thiet-ke-kien-truc`, `thiet-ke-co-khi`, `thiet-ke-pid` | Thiết kế theo ngành |
| `bien-phap-thi-cong-vn` | Biện pháp thi công Việt Nam |

Quản lý: `knowledge_skills` (xem), `knowledge_skill_toggle` (bật/tắt), `knowledge_skill_add` (thêm).

### Thêm skill bằng LLM

```text
Tạo skill qa-mep cho dự án này. Kiểm tra layer ống gió, ống nước, thiết bị, van, tag và khoảng bảo trì.
Dùng error, warning, review; ghi rõ tiêu chuẩn dự án cần hỏi lại. Sau đó thêm vào MCP và bật skill.
```

LLM sẽ: gọi `knowledge_skills` để tránh trùng tên → soạn `SKILL.md` có frontmatter `name`, `description`, `version` →
`knowledge_skill_add` ghi vào `CAD-kho\skill\qa-mep\SKILL.md` → `knowledge_skill_toggle(name="qa-mep", enabled=true)` →
đọc `cadtroly://skill/qa-mep`.

`knowledge_skill_add` chỉ ghi một file Markdown vào kho người dùng: không chạy Python/LISP, không ghi vào skill mặc định,
không ghi đè skill đã có.

## Bóc khối lượng

Luồng: `takeoff_propose` (đề xuất ánh xạ) → `takeoff_decide` (kỹ sư xác nhận) → `takeoff_compute` → `takeoff_export` (Excel).
`takeoff_run` chạy cả thư mục.

### Độ tin cậy A/B/C

- **A** — đếm/đo trực tiếp theo quy tắc đơn vị hoặc attribute block.
- **B** — đoán từ tên layer/block, hoặc chiều cao suy từ text `H=`. Cần kỹ sư xác nhận; xác nhận một lần là thành quy tắc
  trong `quy-tac/anh-xa.json`.
- **C** — không xác định (layer 0, line rời). Khối lượng để trống, Excel ghi "khoanh để người đếm". Không bịa.

### Cột trong Excel

| Cột | Ý nghĩa |
|---|---|
| `Công tác` | Tên việc: xây tường, cửa, sàn… |
| `Đơn vị` | `m`, `m2`, `m3`, `bộ`, `cái`… |
| `Khối lượng` | Giá trị tính từ bản vẽ |
| `Cách tính` | Đếm, chiều dài, diện tích, thể tích, diện tích × chiều cao |
| `Nguồn` | Layer, block, text hoặc quy tắc đã dùng |
| `Tin cậy` | A / B / C như trên |
| `Handle` | Mã đối tượng CAD để tìm lại đúng vị trí |
| `Ghi chú` | Điều kiện thiếu, giả định, việc cần kỹ sư xác nhận |

### Cầu đường: đào đắp và thép

Không cần Civil 3D — đọc text trên bản vẽ AutoCAD thường (Nova-TDN, vẽ tay).

| Tool | Đọc | Tính | Excel |
|---|---|---|---|
| `takeoff_earthwork` | Text lý trình `Km0+100` / `Lý trình: 0+100`; diện tích `F đào = 12.35`, `FĐắp=4,0`, hoặc ô "Diện tích đào" + ô số cùng hàng; tách `đắp K95/K98`, vét hữu cơ, đánh cấp | V = (F1 + F2) / 2 × L giữa hai trắc ngang liền kề | Tổng hợp · Khối lượng đoạn · Trắc ngang (F, handle, lệnh zoom) · Kiểm soát |
| `takeoff_rebar` | Ghi chú `N1 12Ø16 L=5200`, `6%%c22 L=12.5`, `2x10Φ12` | Số thanh × dài × 0.0061654·d² kg/m | Thống kê thép · Tổng hợp theo Ø · Kiểm soát |

Tin cậy: **A** đọc thẳng một text · **B** phải ghép (nhãn với ô số; diện tích giữa hai lý trình; một đầu đoạn thiếu
diện tích coi = 0; ghi chú thép trùng ở nhiều hình chiếu chỉ tính một lần) · **C** thiếu số thanh hoặc `L=`, để trống.

```text
Bóc đào đắp file D:\DuAn\trac-ngang.dwg ra Excel. Liệt kê trắc ngang không có diện tích và các đoạn tin cậy B.
Thống kê thép bản vẽ D:\DuAn\tru-T1.dwg theo đường kính, đối chiếu với bảng thống kê trên bản vẽ nếu có.
```

### Mã định mức

Bảng Excel có cột **Mã định mức**; sheet Kiểm soát ghi căn cứ NĐ 206/2026/NĐ-CP và TT 38/2026/TT-BXD (hiệu lực
01/7/2026, thay TT 12/2021/TT-BXD) và đếm số dòng chưa gán mã. MCP **không tự điền mã** — kỹ sư đưa mã qua
`takeoff_decide(..., ma_dinh_muc="…")` (lưu luôn vào quy tắc ánh xạ, lần sau tự áp) hoặc tham số `ma_dinh_muc` của
`takeoff_earthwork` / `takeoff_rebar`.

## Mức kết quả kiểm tra

| Mức | Ý nghĩa |
|---|---|
| `Lỗi` (error) | Phải sửa trước khi phát hành |
| `Cảnh báo` (warning) | Có dấu hiệu chưa phù hợp, cần kiểm tra lại |
| `Xác nhận` (review) | MCP không đủ căn cứ; kỹ sư quyết định |
| `Đạt` | Không phát hiện vấn đề theo bộ quy tắc đã chọn |

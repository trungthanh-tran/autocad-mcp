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

### Cốt thép

Hai bộ đi kèm, mọi quy tắc ghi điều khoản và **trích nguyên văn** (trường `trich`) đã đọc từ văn bản; nguồn bản đọc và
ngày đối chiếu ghi trong trường `doi_chieu` của file. Nên đối chiếu thêm bản chính thức trước khi phát hành hồ sơ.

| Bộ | Kiểm | Mức |
|---|---|---|
| `tcvn-cot-thep` (TCVN 1651-1/2:2018) | Đường kính ngoài Bảng 2 (chỉ dùng khi có thoả thuận NSX–người mua) · mác không thuộc CB240-T/CB300-T/CB400-T/CB300-V/CB400-V/CB500-V/CB600-V · có CB600-V (không được hàn) · hồ sơ thiếu mác, thiếu lớp bảo vệ, ghi chú thiếu số thanh/L/bước | cảnh báo · lỗi · xác nhận · cảnh báo |
| `tcvn-5574-2018-cot-thep` (mục 10.3.1–10.3.3) | Lớp bảo vệ ghi trên bản vẽ < đường kính thanh hoặc < 10 mm · < 20 mm (đối chiếu Bảng 19) · khoảng hở (bước − d) < max(d, 25) · bước > 400 · bước > 200 | lỗi · xác nhận · cảnh báo · cảnh báo · xác nhận |

Nguyên tắc: ghi chú thép không cho biết loại cấu kiện, chiều cao tiết diện, lớp thép hay cấp bê tông, nên chỉ báo
**lỗi** khi giới hạn đúng với mọi trường hợp văn bản liệt kê (ví dụ lớp bảo vệ "trong mọi trường hợp … không nhỏ hơn
đường kính thanh cốt thép và không nhỏ hơn 10 mm"). Giới hạn có điều kiện báo cảnh báo/xác nhận kèm điều kiện nguyên
văn. Bản vẽ không ghi lớp bảo vệ thì không suy ra vi phạm. Chưa đưa vào: cốt thép đai (10.3.4), neo và nối (10.3.5),
hàm lượng tối thiểu (10.3.3.1) — cần dữ liệu cấu kiện không có trên ghi chú.

```text
Kiểm tra bản vẽ cốt thép trụ T1 theo tcvn-cot-thep và tcvn-5574-2018-cot-thep. Liệt kê từng vấn đề kèm điều khoản và
trích nguyên văn; mục "xác nhận" để tôi quyết, không tự kết luận.
```

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
- **B** — đề xuất từ tên layer/block, hoặc chiều cao đọc từ text `H=`. **Khối lượng để trống** và tool trả câu hỏi
  (`can_hoi`) cho tới khi kỹ sư xác nhận: `takeoff_decide` cho từng nhóm (lưu thành quy tắc trong
  `quy-tac/anh-xa.json`, lần sau thành A), `height_m` cho chiều cao, hoặc `chap_nhan_B=true` khi người dùng nói rõ
  chấp nhận mọi đề xuất. `takeoff_export` không xuất Excel khi còn câu hỏi (trừ `xuat_khi_con_hoi=true` để xuất nháp).
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
| `takeoff_rebar` | Ghi chú `N1 12Ø16 L=5200`, `6%%c22 L=12.5`, `2x10Φ12`, `F1-D25-125` (số hiệu-D đường kính-bước), mác `CB400-V` | Số thanh × dài × khối lượng 1 m dài theo Bảng 2 TCVN 1651-2:2018 (D16 = 1,58 kg/m) | Thống kê thép · Tổng hợp theo Ø (kg/m, sai lệch cho phép, nguồn) · Kiểm soát |

Không suy diễn — chỗ không rõ để trống và hỏi lại (`can_hoi`), chỉ tính khi người dùng trả lời qua tham số:

| Tình huống | Câu hỏi | Tham số trả lời |
|---|---|---|
| Một đầu đoạn không ghi diện tích | Coi bằng 0, hay không tính đoạn? | `thieu_dien_tich`: `bang_0` / `bo_doan` |
| Diện tích nằm giữa hai lý trình | Thuộc trắc ngang nào? | `gan`: `{handle: "Km0+020"}` |
| Hai giá trị cùng loại ở một trắc ngang | Cộng lại, hay chỉ định lại? | `cong_trung`, `gan` |
| Ô nhãn có nhiều ô số cùng hàng | Ô nào là giá trị? | `gan_o_so`: `{handle nhãn: handle ô số}` |
| `L=` không ghi đơn vị | mm hay m? | `don_vi_L`: `mm` / `m` |
| Ghi chú thép giống nhau ở nhiều chỗ | Cùng một thanh hay thanh riêng? | `trung_lap`: `mot_lan` / `tung_cho` |

Tin cậy: **A** đọc thẳng một text hoặc theo câu trả lời của người dùng · **B** ghép ô nhãn với ô số duy nhất cùng
hàng · **C** thiếu dữ liệu hoặc chờ trả lời (để trống). Còn câu hỏi thì không xuất Excel, trừ khi
`xuat_khi_con_hoi=true` (bản nháp, ô chờ để trống).

```text
Bóc đào đắp file D:\DuAn\trac-ngang.dwg ra Excel. Chỗ nào không rõ thì hỏi tôi, không tự chọn.
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

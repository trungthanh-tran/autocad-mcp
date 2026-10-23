---
name: suc-khoe-ban-ve
description: Kiểm tra sức khoẻ bản vẽ trước khi sửa, bóc khối lượng hoặc phát hành — tham chiếu ngoài, đơn vị, layer, đối tượng lỗi/trùng, độ phủ ảnh — chỉ đọc, ra một báo cáo.
version: 0.1
---

# Kiểm tra sức khoẻ bản vẽ

Dùng khi người dùng nói "kiểm tra bản vẽ trước", "bản vẽ có ổn không", "trước khi bóc/sửa/phát hành", hoặc
trước bất kỳ thao tác hàng loạt nào trên bản vẽ người khác làm. Mục tiêu: một báo cáo, **không sửa gì**.

## Trình tự (chỉ dùng tool đọc)

1. **Kết nối** — `system_status`: backend `com` hay `ezdxf`. Ghi rõ trong báo cáo; với ezdxf, ảnh và một số
   kiểm tra là headless, không phải AutoCAD thật.
2. **Đọc hiểu** — `drawing_understand(path)`: loại bản vẽ, đơn vị, phạm vi, layer chính, mỗi nhận định kèm bằng chứng.
   Nếu chỉ cần số liệu nhanh: `drawing_read(path)`.
3. **Tham chiếu ngoài** — `xref_manage(action="list")`: xref thiếu file, đường dẫn tuyệt đối trỏ ra máy khác,
   overlay/attach. Xref thiếu → mọi khối lượng và kiểm tra trên phần đó là **không đầy đủ**.
4. **Đơn vị và tỷ lệ** — so `units` với kích thước thực tế của vài đối tượng quen (cửa ~900, làn xe ~3.5 m).
   Đơn vị `unknown` hoặc không khớp → dừng bóc khối lượng, hỏi người dùng.
5. **Layer** — `analysis_layer_stats`: layer rỗng, layer `0`/`Defpoints` chứa hình học, tên ngoài quy ước
   (`KT-`/`KC-`/`HT-`/`CAU-` hoặc NCS `A-`/`S-`/`C-`).
6. **Đối tượng lỗi** — `validation_check(checks=["empty_layers", "zero_length", "duplicate_entities"])`.
7. **Chất lượng** — `drawing_critique` (bỏ trống `focus` = chạy tất cả): text chồng, dim bị override, đường hở,
   đối tượng ngoài khung…
8. **Theo chuẩn** — nếu có bộ quy tắc phù hợp: `check_rulesets` → `check_run(path, ruleset)`.
9. **Ảnh** — `view_render_report` trước khi dựa vào ảnh chụp; loại nào báo chưa render được thì ghi
   "cần mở AutoCAD kiểm tra".

`drawing_audit` **sửa** bản vẽ (áp dụng repair ngay) — không chạy trong bước kiểm tra. Chỉ đề xuất, và nếu người dùng
đồng ý thì chạy trên bản sao rồi lưu thành file mới.

## Báo cáo

| Mục | Kết quả | Mức | Bằng chứng |
|---|---|---|---|
| Xref | 2 thiếu file | Lỗi | tên xref, đường dẫn |
| Đơn vị | mm, khớp cửa 900 | Đạt | handle cửa |
| … | | | |

- Mức: **Lỗi** (phải xử lý trước khi bóc/sửa/phát hành) · **Cảnh báo** · **Xác nhận** (không đủ căn cứ) · **Đạt**.
- Mỗi dòng có handle, tên layer hoặc tên xref để người dùng tìm lại được.
- Cuối báo cáo: "Có thể tiếp tục bóc khối lượng / sửa không?" — trả lời Có, Có với điều kiện (liệt kê), hoặc Không.

## Không làm

- Không tự sửa, purge, audit, bind xref hay lưu file trong khi kiểm tra.
- Không kết luận "bản vẽ đạt" khi còn xref thiếu, đơn vị không rõ, hoặc `view_render_report` báo thiếu loại.

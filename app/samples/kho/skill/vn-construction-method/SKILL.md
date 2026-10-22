---
name: vn-construction-method
description: Lập và kiểm tra bản vẽ biện pháp thi công theo QCVN 18:2021/BXD. Dùng khi yêu cầu nhắc tới biện pháp, an toàn, giàn giáo, lan can, lưới, hố đào, cốp pha.
version: 0.1
---

# Biện pháp thi công Việt Nam

## Khi nào dùng
Yêu cầu có các từ: biện pháp thi công, BPTC, an toàn, giàn giáo, lan can, lưới an toàn, rào chắn, hố đào, cốp pha, ván khuôn.

## Thứ tự làm
1. `drawing_read` bản vẽ kiến trúc/kết cấu để lấy số tầng, chiều cao tầng (text H=), kích thước mặt bằng.
2. `check_rulesets` → chọn `qcvn-18-2021` (chỉ dòng đã duyệt). Chưa có thì nói rõ và dừng, không tự bịa điều khoản.
3. Lập bảng tham số: mỗi số kèm nguồn (file + điều khoản). Thiếu thì hỏi một lần, gom mọi câu.
4. Vẽ qua `acad_*`: mở `acad_transaction_begin`, vẽ chi tiết từ kho/chi-tiet (LISP tham số qua `acad_system_run_lisp`), `acad_transaction_commit`. Mọi cụm có thể undo.
5. `check_run` lại bản vẽ vừa vẽ với cùng bộ quy tắc. Chưa đạt thì sửa, không nộp.

## Nguyên tắc
- Điều khoản ghi "theo điều kiện thực tế" / "theo thiết kế" → đánh dấu `xac_nhan`, kỹ sư quyết.
- Không tự lưu file. Không vẽ ngoài vùng đang xem khi người dùng chỉ định vùng.
- Thuyết minh sinh từ cùng bảng tham số với bản vẽ.

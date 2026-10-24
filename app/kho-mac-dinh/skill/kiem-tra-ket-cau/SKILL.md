---
name: kiem-tra-ket-cau
description: Kiểm tra tổ chức CAD và dấu hiệu hình học kết cấu, phân loại warning/error, không thay thế tính toán.
version: 0.2
---

# Kiểm tra kết cấu và tối ưu bản vẽ

Skill này là một nhánh của `qa-ban-ve-toan-dien`; khi kiểm tra kết cấu cần
kết hợp thêm `quan-tri-layer-cad` và `annotation-dim-qa` để không bỏ sót layer,
dim, text và khả năng in.

## Kiểm tra tự động

- `error`: nét kết cấu zero-length hoặc lỗi hình học chắc chắn cần sửa.
- `warning`: layer kết cấu rỗng, hình học trùng, tên layer chưa theo quy ước,
  không nhận diện được bộ layer.
- `suggestion`: tối ưu layer, purge có kiểm soát, chuẩn hóa ByLayer, kiểm tra
  dim/text và đối chiếu layout.

## Cốt thép

- Chạy `check_run` với `tcvn-cot-thep` (TCVN 1651-1/2:2018) và `tcvn-5574-2018-cot-thep` (TCVN 5574:2018 mục
  10.3.1–10.3.3). Báo lại đúng điều khoản và trường `trich` của từng phát hiện, không diễn giải thêm.
- Mục `xac_nhan` và `canh_bao` phụ thuộc loại cấu kiện, chiều cao tiết diện, lớp thép, cấp bê tông: hỏi kỹ sư, không
  tự chọn điều kiện.
- Không đưa ra giá trị neo, nối, cốt đai hay hàm lượng thép khi bộ quy tắc chưa có trích nguyên văn — nói rõ là chưa
  có trong kho.
- Khối lượng thép (`takeoff_rebar`) dùng Bảng 2 TCVN 1651-2:2018; cỡ ngoài bảng ghi rõ là tính theo công thức.

## Không tự kết luận

Không dùng kết quả này để kết luận đủ khả năng chịu lực, ổn định, chống cháy,
độ võng hoặc đạt tiêu chuẩn thiết kế nếu chưa có tải trọng, vật liệu, điều kiện
biên, mô hình tính và hồ sơ kỹ sư phê duyệt.

## Quy trình

1. Đọc layer, đơn vị, layout, entity và chuẩn dự án.
2. Chạy kiểm tra kết cấu và tối ưu hóa ở chế độ chỉ đọc.
3. Sửa từng lỗi có handle, chụp trước/sau.
4. Chạy lại kiểm tra; chỉ phát hành khi không còn `error` và các `warning` đã
   được kỹ sư xem xét.


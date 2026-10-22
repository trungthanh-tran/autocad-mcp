---
name: kiem-tra-ket-cau
description: Kiểm tra tổ chức CAD và dấu hiệu hình học kết cấu, phân loại warning/error, không thay thế tính toán.
version: 0.1
---

# Kiểm tra kết cấu và tối ưu bản vẽ

## Kiểm tra tự động

- `error`: nét kết cấu zero-length hoặc lỗi hình học chắc chắn cần sửa.
- `warning`: layer kết cấu rỗng, hình học trùng, tên layer chưa theo quy ước,
  không nhận diện được bộ layer.
- `suggestion`: tối ưu layer, purge có kiểm soát, chuẩn hóa ByLayer, kiểm tra
  dim/text và đối chiếu layout.

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


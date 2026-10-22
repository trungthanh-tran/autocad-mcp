---
name: tinh-toan-chiu-luc
description: Chuẩn bị, kiểm tra dữ liệu và hỗ trợ tính toán sơ bộ chịu lực; không thay thế mô hình tính và hồ sơ kỹ sư phê duyệt.
version: 0.1
---

# Tính toán chịu lực

## Có thể hỗ trợ

- Đọc lưới trục, nhịp, cao độ, tiết diện, vật liệu và sơ đồ cấu kiện từ CAD.
- Lập bảng đầu vào có nguồn: tải trọng, tổ hợp, vật liệu, liên kết, điều kiện
  biên và cấu kiện cột/dầm/sàn/móng.
- Kiểm tra thiếu dữ liệu, đơn vị, tải trọng bất thường, nhịp/tiết diện không
  hợp lý và sự thống nhất giữa mặt bằng, mặt đứng, mặt cắt.
- Tạo báo cáo tính sơ bộ, đánh dấu giả định và xuất bảng để kỹ sư kiểm tra.

## Không được tự kết luận

Không tự phát hành kết quả đạt/không đạt chịu lực nếu chưa có tiêu chuẩn thiết
kế áp dụng, mô hình phân tích, tải trọng được duyệt, vật liệu, điều kiện nền
móng và kỹ sư có thẩm quyền xác nhận.

## Mức kết quả

- `error`: thiếu hoặc mâu thuẫn dữ liệu làm không thể tính.
- `warning`: dữ liệu có dấu hiệu bất thường cần kiểm tra.
- `review`: giả định hoặc kết quả sơ bộ cần kỹ sư xác nhận.
- `suggestion`: đề xuất bổ sung dữ liệu hoặc chuẩn hóa mô hình.

## Use case mẫu

- “Đọc mặt bằng kết cấu, lập bảng cột/dầm/sàn theo trục và chỉ ra dữ liệu còn thiếu.”
- “Kiểm tra đơn vị, nhịp, tiết diện và vật liệu trước khi đưa vào mô hình tính.”
- “Lập tính sơ bộ dầm theo tải trọng tôi cung cấp, ghi rõ mọi giả định và xuất bảng để kỹ sư kiểm tra.”
- “So sánh mặt bằng kết cấu với mặt cắt, tìm cấu kiện lệch hoặc không liên tục.”

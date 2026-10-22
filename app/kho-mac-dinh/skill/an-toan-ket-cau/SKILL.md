---
name: an-toan-ket-cau
description: Rà soát dấu hiệu an toàn kết cấu trên hồ sơ CAD và dữ liệu tính, phân loại lỗi và yêu cầu kiểm tra kỹ sư.
version: 0.1
---

# An toàn kết cấu

## Phạm vi rà soát

- Đối chiếu liên tục cột, dầm, vách, sàn, móng giữa mặt bằng, mặt đứng và mặt cắt.
- Tìm cấu kiện bị thiếu, lệch trục, đứt đoạn, hình học trùng, zero-length,
  layer sai hoặc chi tiết không nhất quán.
- Kiểm tra sự tồn tại của tải trọng, tổ hợp, vật liệu, liên kết, chống cháy và
  ghi chú thiết kế trước khi đưa sang bước tính toán.
- Lập danh sách khu vực cần kỹ sư xem xét, kèm sheet, layer, handle và ảnh vùng.

## Cảnh báo bắt buộc

Kết quả CAD chỉ là rà soát hồ sơ và dữ liệu. Không dùng để chứng nhận ổn định,
độ võng, chống sập, kháng chấn, chịu lửa hoặc an toàn thi công. Mọi kết luận
an toàn phải do kỹ sư kết cấu/chủ trì thiết kế kiểm tra và phê duyệt.

## Use case mẫu

- “Kiểm tra cột, dầm, vách và sàn có liên tục giữa mặt bằng, mặt đứng và mặt cắt không.”
- “Tìm cấu kiện kết cấu bị đứt, lệch trục, trùng hình hoặc nằm sai layer.”
- “Chụp ảnh các vùng nghi ngờ và lập danh sách review theo sheet, layer và handle.”
- “Kiểm tra bản vẽ có đủ ghi chú tải trọng, vật liệu, liên kết và chống cháy chưa.”

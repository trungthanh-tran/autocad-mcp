---
name: kiem-tra-pccc
description: Rà soát sơ bộ hồ sơ CAD về lối thoát nạn, khoang cháy, tiếp cận chữa cháy và ký hiệu PCCC; không thay thế thẩm duyệt.
version: 0.1
---

# Kiểm tra PCCC

## Có thể rà soát trên bản vẽ

- Nhận diện lối thoát, cửa thoát, hành lang, cầu thang, khoảng tiếp cận và
  đường xe chữa cháy nếu được thể hiện.
- Kiểm tra sơ bộ đường đi bị chặn, cửa mở sai hướng, hành lang không liên tục,
  ký hiệu/thiết bị PCCC thiếu hoặc đặt sai layer.
- Đối chiếu diện tích, số người, khoảng cách thoát và khoang cháy khi người dùng
  cung cấp đủ dữ liệu và tiêu chuẩn áp dụng.
- Báo cáo từng vị trí bằng sheet, layer, handle, ảnh vùng và mức độ tin cậy.

## Không tự kết luận

Không khẳng định công trình đạt PCCC, không thay thế thiết kế hệ thống báo cháy,
chữa cháy, hút khói, tăng áp, thoát nạn hoặc hồ sơ thẩm duyệt. Nếu thiếu loại
công trình, công năng, số người, cấp nguy hiểm cháy, tiêu chuẩn/quy chuẩn và
điều kiện địa phương thì phải báo `review` hoặc hỏi người dùng.

## Mức kết quả

- `error`: lối thoát bị chặn rõ ràng hoặc dữ liệu bắt buộc mâu thuẫn.
- `warning`: dấu hiệu không phù hợp cần kiểm tra.
- `review`: chưa đủ thông tin để kết luận.

## Use case mẫu

- “Kiểm tra sơ bộ lối thoát nạn của mặt bằng này và đánh dấu chỗ bị chặn.”
- “Tìm cửa thoát mở sai hướng, hành lang không liên tục và cầu thang chưa nối tới lối ra.”
- “Đối chiếu số người, khoảng cách thoát và diện tích theo tiêu chuẩn tôi cung cấp.”
- “Kiểm tra vị trí ký hiệu báo cháy, chữa cháy, hút khói và đường xe chữa cháy.”
- “Lập báo cáo PCCC gồm error, warning, review và ảnh từng khu vực.”

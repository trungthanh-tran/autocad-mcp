---
name: annotation-dim-qa
description: Chuẩn hóa text, dim, mleader, hatch, nét và kiểm tra khả năng đọc khi in ở nhiều tỷ lệ.
version: 0.1
---

# Annotation và kiểm tra bản vẽ

## Nguyên tắc

- Model vẽ đúng kích thước thật; tỷ lệ thể hiện nằm ở Layout/viewport.
- Text, dim, mleader, hatch và ký hiệu phải nằm trên layer chức năng riêng.
- Dùng text style, dim style và linetype thống nhất; ưu tiên ByLayer.
- Annotative chỉ bật khi hệ thống viewport và quy trình dự án hỗ trợ rõ ràng.

## Kiểm tra trước khi phát hành

1. Tất cả dim có liên kết đúng hình học và không bị text che.
2. Dim tổng hợp phải khớp tổng các đoạn thành phần trong dung sai dự án.
3. Text không chồng nhau, không nằm ngoài khung, không dùng font thiếu.
4. Mũi tên, witness line, centerline, hidden line và hatch phân biệt khi plot.
5. Kiểm tra tại mọi tỷ lệ đã khai báo, cả Model và Layout.
6. Kiểm tra title block: mã bản vẽ, revision, scale, đơn vị, ngày và trạng thái.
7. Báo lỗi theo mức `error`, `warning`, `review`; không tự sửa số liệu thiết kế.

## Tham chiếu

- ISO 128-2/-3: quy ước nét, hình chiếu, mặt cắt.
- ISO 129-1: nguyên tắc ghi kích thước.
- ISO 5455: quy ước tỷ lệ.
- Autodesk: annotative text/dimensions và CAD Standards.


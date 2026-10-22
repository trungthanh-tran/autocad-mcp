---
name: an-toan-cad-chuyen-sau
description: QA CAD chuyên sâu về đơn vị, layer, hình học, annotation, giao cắt, plot, giao nhận và kiểm soát thay đổi.
version: 0.1
---

# An toàn CAD chuyên sâu

## Kiểm tra

- Đơn vị, hệ tọa độ, phạm vi, scale, layout, viewport và title block.
- Layer, màu, linetype, lineweight, ByLayer, layer rỗng và đối tượng sai layer.
- Hình học trùng, zero-length, đường hở, giao cắt bất thường, block lỗi và
  đối tượng không render được.
- Text, dimension, mleader, hatch, font thiếu, tỷ lệ in và khả năng đọc ở layout.
- Revision, source map, handle, diff trước/sau, checksum và bản sao phát hành.

## Quy tắc an toàn

Luôn đọc và chụp trước khi sửa; sửa theo vùng/handle; dùng checkpoint hoặc
transaction; chạy QA sau sửa; không ghi đè nguồn nếu chưa được yêu cầu.
Đối tượng không đủ bằng chứng phải là `review`, không được tự gán hoặc xóa.

## Tham chiếu

ISO 128, ISO 129-1, ISO 5455, ISO 5457, ISO 7200, ISO 13567 và quy định CAD
của dự án. Tiêu chuẩn áp dụng cuối cùng phải do chủ trì dự án xác nhận.

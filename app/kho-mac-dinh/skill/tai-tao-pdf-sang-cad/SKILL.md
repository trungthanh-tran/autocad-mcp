---
name: tai-tao-pdf-sang-cad
description: Tái tạo PDF bản vẽ thành DWG có hình học, kích thước, annotation và layer có thể chỉnh sửa.
version: 0.1
---

# Tái tạo PDF sang CAD

## Mục tiêu

Tạo DWG có thể sửa theo lớp, không chỉ là ảnh nền hoặc một lớp vector duy nhất.

## Quy trình

1. Xác định PDF là vector hay raster; đọc khổ giấy, orientation, viewport,
   scale ghi trên title block và đơn vị.
2. Giữ một lớp `PDF_REF` chỉ để đối chiếu; không coi nó là mô hình đã kiểm chứng.
3. Bóc vector/text/dim/block nếu có. Với raster, OCR và nhận dạng hình học chỉ
   là đề xuất, phải đánh dấu `review`.
4. Hiệu chỉnh tỷ lệ bằng ít nhất một kích thước có nguồn; nếu có nhiều kích
   thước kiểm tra sai số giữa chúng.
5. Tách các nhóm: model, cut, overhead, hatch, dimension, text, symbol,
   furniture/equipment, title block và review.
6. Giữ nguyên text kích thước gốc; không thay bằng số đo tự tính nếu chưa đối
   chiếu. Kích thước bị thiếu hoặc không đọc được ghi vào báo cáo.
7. Dựng Layout A1/A3 đúng khung, viewport và tỷ lệ; không phóng to hình học
   tùy tiện để vừa trang.
8. Chạy kiểm tra: khoảng cách giữa dim và hình học, dim trùng, text chồng,
   đường hở, nét rác, layer sai và sai lệch scale.
9. Xuất `source_map`, `uncertain_objects` và `qa_report` cùng DWG.

## Không được làm

- Không biến toàn bộ PDF thành một ảnh rồi gọi là DWG chuẩn.
- Không tự suy luận kích thước bị mờ, bị che hoặc mâu thuẫn.
- Không xóa lớp tham chiếu trước khi người dùng xác nhận kết quả.

## Tham chiếu

- ISO 128: nguyên tắc trình bày, nét, hình chiếu và mặt cắt.
- ISO 129-1: ghi kích thước.
- ISO 5455: biểu diễn và ghi tỷ lệ.
- ISO 5457: khổ giấy và bố trí bản vẽ.
- Autodesk, hướng dẫn CAD Standards và Annotative Text/Dimensions.


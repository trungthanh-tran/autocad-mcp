---
name: cad-layer-management
description: Tổ chức, đặt tên, ánh xạ và kiểm tra layer CAD để bản vẽ dễ đọc, sửa, bật/tắt và bàn giao.
version: 0.1
---

# Quản trị layer CAD

## Khi dùng

Dùng khi đọc bản vẽ lộn xộn, tách PDF/DWG thành nhóm có nghĩa, đổi chuẩn layer,
hoặc cần kiểm tra trước khi phát hành.

## Quy trình bắt buộc

1. Đọc inventory: đơn vị, extents, layer, màu, linetype, lineweight, block,
   text, dim và layout.
2. Nhận diện quy ước hiện có từ tên layer. Nếu có bằng chứng mâu thuẫn hoặc
   không đủ bằng chứng, hỏi người dùng chọn `vn`, `ncs` hoặc quy ước dự án;
   không tự đoán.
3. Tạo bảng ánh xạ `layer_goc -> layer_moi`, kèm lý do và độ tin cậy.
4. Tách theo đối tượng và chức năng: tường, cột, dầm, sàn, cửa, nội thất,
   thiết bị, hatch, dim, text, trục, ký hiệu, tham chiếu và không in.
5. Giữ nguyên hình học; chỉ đổi layer khi có căn cứ. Đối tượng không chắc chắn
   đưa vào `*_REVIEW`, không gán bừa.
6. Áp dụng ByLayer cho màu, linetype, lineweight; không để thuộc tính rời rạc
   nếu không có lý do kỹ thuật.
7. Kiểm tra layer rỗng, layer trùng nghĩa, đối tượng sai layer, nét zero-length,
   text/dim chồng nhau và khả năng plot.
8. Xuất báo cáo thay đổi trước/sau và lưu bản sao có hậu tố rõ ràng.

## Quy tắc đặt tên

- NCS/AIA: `DISCIPLINE-MAJOR-MINOR-STATUS`, ví dụ `A-WALL-FULL-N`,
  `S-COLS-N`, `C-ROAD-ALIGN`.
- ISO 13567: dùng các trường có dấu gạch nối theo sổ tay dự án; không trộn
  thứ tự trường giữa các hệ.
- Việt Nam trong MCP: dùng ASCII in hoa như `KT-TUONG`, `KC-COT`, `KT-DIM`,
  `HT-MATDUONG`, `CAU-TRU`.
- Tên mới phải duy nhất, mô tả được nội dung, không dùng tên chung như
  `Layer1`, `New Layer`, `Misc`.

## Phân loại khi bóc tách bản vẽ

Ưu tiên theo bằng chứng: tên layer gốc, màu/linetype, hình học, vị trí, text
gần đối tượng, block name và quan hệ giao cắt. Mỗi nhóm phải ghi `evidence`;
nhóm nhận diện yếu phải có trạng thái `review`.

## Tham chiếu

- ISO 13567-1/-2: tổ chức và đặt tên layer CAD.
- Autodesk, *Creating and Managing CAD Standards*: layer, text style,
  dim style, linetype, title block, ByLayer và DWS.
- NCS/AIA CAD Layer Guidelines: discipline, major/minor group, status.
- BS 1192 / ISO 19650 UK National Annex: quy ước thông tin và mã hóa hồ sơ.


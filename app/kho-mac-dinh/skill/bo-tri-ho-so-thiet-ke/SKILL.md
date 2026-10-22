---
name: bo-tri-ho-so-thiet-ke
description: Chuẩn hóa cấu trúc hồ sơ, tên file, sheet, revision và trạng thái phát hành cho dự án CAD.
version: 0.1
---

# Bố trí hồ sơ thiết kế

## Cách làm

- Tách rõ model, sheet/layout, tham chiếu, xuất bản và file tạm.
- Dùng tên file ASCII, không dấu, không khoảng trắng nếu dự án yêu cầu trao đổi
  đa hệ thống.
- Mỗi bản vẽ phải có mã, bộ môn, loại bản vẽ, số thứ tự, revision và trạng thái.
- Không ghi đè bản gốc; bản xử lý phải có hậu tố và nhật ký nguồn.
- Giữ liên kết và đường dẫn tương đối khi đóng gói bàn giao.

## Metadata cần đọc/ghi

`project`, `originator`, `discipline`, `volume_or_system`, `level_or_location`,
`drawing_type`, `role`, `number`, `revision`, `status`, `scale`, `units`.

## Quy tắc an toàn

Nếu thiếu mã dự án, revision hoặc trạng thái phát hành thì hỏi lại; không tự
điền. File trung gian chỉ được tạo trong thư mục tạm của MCP và phải dọn sau
khi hoàn tất, trừ khi người dùng yêu cầu giữ để kiểm tra.

## Tham chiếu

- ISO 19650-2 và UK National Annex NA2: mã hóa thông tin/hồ sơ.
- BS 1192: quy ước hồ sơ CAD/BIM đời trước và cách tổ chức thông tin.
- Autodesk CAD Standards: template, layer, style, title block và DWS.


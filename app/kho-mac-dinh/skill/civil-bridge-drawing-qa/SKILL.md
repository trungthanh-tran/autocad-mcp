---
name: civil-bridge-drawing-qa
description: Đọc, phân lớp và kiểm tra bản vẽ đường, cầu, thoát nước và hạ tầng theo vai trò kỹ thuật.
version: 0.1
---

# Kiểm tra bản vẽ đường và cầu

## Phân lớp tối thiểu

- Đường: hiện trạng/khảo sát, tim tuyến, hình học tuyến, mặt đường, lề/vỉa,
  thoát nước, tiện ích, biển báo–sơn, mặt cắt/hatch, dim, text, tạm.
- Cầu: mặt cầu/bản mặt cầu, dầm, trụ, mố/tường cánh, gối/khe, cốt thép,
  phần khuất, tim trục, mặt cắt/hatch, dim, text, tạm.

## Kiểm tra logic

- Tim tuyến, lý trình, cao độ và hướng tuyến phải thống nhất giữa plan/profile.
- Mặt cắt phải có đủ cao độ, bề rộng, độ dốc, lớp kết cấu và phạm vi thi công.
- Cầu phải liên kết đúng trục, nhịp, gối, dầm, trụ/mố và cao độ thiết kế.
- Thoát nước phải có hướng dòng, cao độ và điểm xả; không kết luận thủy lực
  nếu không có số liệu đầu vào.
- Phần suy đoán từ PDF phải là `review`, không đưa vào khối lượng chính thức.

## Tham chiếu Việt Nam

TCVN 4054:2005, TCVN 5729:2012, TCVN 9436:2012 và TCVN 11823:2017 được
dùng làm danh mục kiểm tra ban đầu; phải đối chiếu phiên bản hợp đồng/dự án
trước khi phát hành.

## Tham chiếu quốc tế

NCS Civil/Structural, ISO 128, ISO 13567 và ISO 19650 cho cách trình bày,
phân lớp và quản lý thông tin.

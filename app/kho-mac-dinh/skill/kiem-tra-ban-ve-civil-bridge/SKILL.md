---
name: kiem-tra-ban-ve-civil-bridge
description: Đọc, phân lớp và kiểm tra bản vẽ đường, cầu, thoát nước và hạ tầng theo vai trò kỹ thuật.
version: 0.2
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

## Khối lượng

Chạy skill `suc-khoe-ban-ve` trước (xref, đơn vị). Bản vẽ AutoCAD thường (Nova-TDN, vẽ tay) dùng được, không cần
Civil 3D.

- Đào đắp: `takeoff_earthwork(path, out)` đọc text lý trình (`Km0+100`, `Lý trình: 0+100`) và diện tích
  (`F đào = 12.35`, hoặc ô "Diện tích đắp" + ô số cùng hàng), tính mặt cắt trung bình giữa hai trắc ngang liền kề.
  Báo người dùng các trắc ngang không thấy diện tích và đoạn tin cậy B (một đầu thiếu diện tích coi = 0, hoặc
  diện tích nằm giữa hai lý trình).
- Thép: `takeoff_rebar(path, out)` đọc ghi chú `N1 12Ø16 L=5200`, `%%c` = Ø. Ghi chú trùng ở nhiều hình chiếu chỉ
  tính một lần (B) — hỏi người dùng có phải thanh khác nhau không. Ghi chú chỉ có bước `a200` hoặc thiếu `L=` → C.
- Nếu bản vẽ đã có bảng thống kê thép, đối chiếu tổng theo đường kính với bảng đó và báo chênh lệch, không thay số.
- Mã định mức (TT 38/2026/TT-BXD) chỉ điền khi người dùng đưa mã: tham số `ma_dinh_muc`.

## Tham chiếu Việt Nam

TCVN 4054:2005, TCVN 5729:2012, TCVN 9436:2012 và TCVN 11823:2017 được
dùng làm danh mục kiểm tra ban đầu; phải đối chiếu phiên bản hợp đồng/dự án
trước khi phát hành.

## Tham chiếu quốc tế

NCS Civil/Structural, ISO 128, ISO 13567 và ISO 19650 cho cách trình bày,
phân lớp và quản lý thông tin.

---
name: kiem-tra-ban-ve-civil-bridge
description: Đọc, phân lớp và kiểm tra bản vẽ đường, cầu, thoát nước và hạ tầng theo vai trò kỹ thuật.
version: 0.3
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
  Kết quả có `can_hoi` (một đầu đoạn không ghi diện tích, diện tích nằm giữa hai lý trình, hai giá trị cùng loại,
  ô nhãn có nhiều ô số) → hỏi người dùng đúng câu đó, gọi lại với `thieu_dien_tich` / `gan` / `cong_trung` /
  `gan_o_so` theo câu trả lời. Không tự chọn.
- Thép: `takeoff_rebar(path, out)` đọc ghi chú `N1 12Ø16 L=5200`, `F1-D25-125`, `%%c` = Ø. `L=` không ghi đơn vị
  hoặc ghi chú lặp ở nhiều chỗ → `can_hoi`; hỏi người dùng rồi gọi lại với `don_vi_L` (`mm`/`m`) và `trung_lap`
  (`mot_lan`/`tung_cho`). Ghi chú chỉ có bước `a200` hoặc thiếu `L=` → C, để trống.
- Nếu bản vẽ đã có bảng thống kê thép, đối chiếu tổng theo đường kính với bảng đó và báo chênh lệch, không thay số.
- Mã định mức (TT 38/2026/TT-BXD) chỉ điền khi người dùng đưa mã: tham số `ma_dinh_muc`.

## Tham chiếu Việt Nam

TCVN 4054:2005, TCVN 5729:2012, TCVN 9436:2012 và TCVN 11823:2017 được
dùng làm danh mục kiểm tra ban đầu; phải đối chiếu phiên bản hợp đồng/dự án
trước khi phát hành.

## Tham chiếu quốc tế

NCS Civil/Structural, ISO 128, ISO 13567 và ISO 19650 cho cách trình bày,
phân lớp và quản lý thông tin.

---
name: qa-ban-ve-toan-dien
description: Điều phối QA cho PDF, DWG và DXF từ đọc hiểu, tách layer, annotation, kết cấu, khối lượng đến kiểm tra trước và sau chỉnh sửa.
version: 0.1
---

# QA bản vẽ CAD toàn diện

## Phạm vi skill

Skill này gọi các skill chuyên môn theo bằng chứng của bản vẽ, không gộp mọi
đối tượng vào một kết luận chung:

- `tai-tao-pdf-sang-cad`: đọc PDF vector/raster và dựng PDF thành DWG có thể sửa.
- `quan-tri-layer-cad`: nhận diện, ánh xạ và tách layer theo chuẩn dự án.
- `annotation-dim-qa`: kiểm tra text, dim, mleader, hatch, nét và khả năng plot.
- `kiem-tra-ket-cau`: kiểm tra tổ chức/hình học layer kết cấu và đề xuất tối ưu.
- `tinh-toan-chiu-luc`: chuẩn bị dữ liệu, kiểm tra đầu vào và lập tính sơ bộ có giả định.
- `an-toan-ket-cau`: rà soát liên tục cấu kiện và dấu hiệu mất an toàn trên hồ sơ.
- `kiem-tra-pccc`: rà soát sơ bộ thoát nạn, khoang cháy, tiếp cận và ký hiệu PCCC.
- `an-toan-cad-chuyen-sau`: kiểm tra an toàn dữ liệu CAD, plot, giao nhận và thay đổi.
- `thiet-ke-co-khi`: bản vẽ cơ khí, GD&T, dung sai, mối hàn và bảng kê.
- `thiet-ke-pid`: P&ID, tag, port, topology, line list và instrument index.
- `thiet-ke-kien-truc`: tường, cửa, phòng, cầu thang, schedule và kiểm tra mặt bằng.
- `kiem-tra-ban-ve-civil-bridge`: kiểm tra bản vẽ đường, cầu, thoát nước và hạ tầng.
- `bo-tri-ho-so-thiet-ke`: kiểm tra sheet, mã hồ sơ, revision và trạng thái phát hành.

## Các use case

1. Kiểm tra bản vẽ trước phát hành: layer, đơn vị, extents, text, dim, block,
   hatch, layout, title block và khả năng in.
2. PDF → DWG: giữ kích thước, khổ giấy, layout, đường nét, text, dim và tạo
   `PDF_REF`, `*_REVIEW`, `source_map`, `uncertain_objects`, `qa_report`.
3. Tách bản vẽ: phân riêng tường, cột, dầm, sàn, cửa, nội thất, thiết bị,
   dim, text, hatch, trục, ký hiệu và tham chiếu.
4. Sửa DWG có kiểm soát: chụp trước, xác định vùng/handle, sửa, chụp sau,
   chạy diff và chỉ lưu bản mới sau khi người dùng xác nhận.
5. Tư vấn bố trí: đưa ra phương án sơ bộ, ghi rõ giả định và phần cần kỹ sư
   xác nhận; không tự biến tư vấn thành hồ sơ được phê duyệt.
6. Tự dựng bản vẽ: tạo hình học theo kích thước được cung cấp, đặt layer,
   dim, text và layout; thiếu dữ liệu thì hỏi hoặc đánh dấu `REVIEW`.
7. Bóc tách khối lượng: đếm block, đo chiều dài/diện tích và xuất dữ liệu có
   handle, layer, nguồn đo và độ tin cậy.
8. Tối ưu bản vẽ: phát hiện hình học trùng, layer sai, layer rỗng, thuộc tính
   không theo ByLayer, nét rác và đề xuất dọn dẹp không phá hủy.
9. Tính toán/rà soát an toàn kết cấu và PCCC: chỉ chạy khi đủ đầu vào, ghi rõ
   tiêu chuẩn áp dụng, giả định, độ tin cậy và yêu cầu kỹ sư xác nhận.

## Câu lệnh nhanh cho người dùng

- “Kiểm tra toàn bộ bản vẽ và báo lỗi trước khi phát hành.”
- “Đọc PDF này, dựng DWG, tách layer và báo phần không chắc chắn.”
- “Sửa khu vực được chọn, chụp trước/sau, chạy diff rồi lưu bản mới.”
- “Lập bảng cấu kiện và dữ liệu đầu vào cho tính chịu lực; không tự kết luận đạt.”
- “Rà soát an toàn kết cấu, đánh dấu mọi cấu kiện không liên tục.”
- “Kiểm tra PCCC sơ bộ và hỏi tôi nếu thiếu tiêu chuẩn hoặc số người.”
- “Bóc tách khối lượng cửa, thiết bị, tường và xuất Excel có handle truy vết.”

## Mức kết quả

- `error`: lỗi chắc chắn cần xử lý trước khi phát hành.
- `warning`: dấu hiệu bất thường cần người dùng/kỹ sư xem xét.
- `review`: chưa đủ bằng chứng, không được tự suy luận.
- `suggestion`: đề xuất tối ưu, không tự động áp dụng nếu làm thay đổi thiết kế.

## Quy trình bắt buộc

1. Đọc file, phiên bản, đơn vị, layout, layer và phạm vi được phép xử lý.
2. Xác định PDF vector/raster và quy ước layer; nếu không đủ bằng chứng thì hỏi.
3. Chạy các skill QA phù hợp, giữ liên kết tới source và handle.
4. Báo cáo riêng `error`, `warning`, `review`, `suggestion`.
5. Với thao tác sửa/vẽ: chụp trước, tạo checkpoint, chỉnh sửa, chụp sau,
   chạy diff và kiểm tra lại.
6. Không ghi đè file nguồn, không xóa file trung gian trước khi báo cáo hoàn tất.

## Giới hạn

QA CAD không thay thế tính toán kết cấu, thiết kế PCCC, thẩm tra pháp lý,
nghiệm thu hoặc phê duyệt của kỹ sư/chủ trì thiết kế.

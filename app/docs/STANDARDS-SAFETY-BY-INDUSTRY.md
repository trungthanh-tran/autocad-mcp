# Tiêu chuẩn an toàn CAD theo ngành

Tài liệu này là danh mục tham chiếu cho skill và rule trong MCP. Nó giúp chọn
đúng bộ tiêu chuẩn khi đọc, dựng, sửa hoặc kiểm tra bản vẽ. Đây không phải là
chứng nhận thiết kế, thẩm tra kết cấu hay thẩm duyệt PCCC.

## Cách dùng trong MCP

1. Gọi `knowledge_industries` để xem mã ngành và tên tiếng Việt.
2. Gọi `knowledge_standards(industry="...")` để xem tiêu chuẩn đã có trong kho.
3. Khi tiêu chuẩn thay đổi, dùng `knowledge_standard_add` với phiên bản/nguồn mới;
   giữ bản cũ cho hồ sơ đã phát hành.
4. Chạy `check_run` với đúng `ruleset`, phiên bản và ngày hiệu lực.
5. Nếu thiếu tiêu chuẩn hoặc dữ liệu, trả `review`, không tự suy luận.

## Mức kết quả

- `error`: lỗi CAD hoặc hồ sơ chắc chắn cần xử lý trước khi phát hành.
- `warning`: dấu hiệu không phù hợp, cần người thiết kế/kỹ sư kiểm tra.
- `review`: thiếu tiêu chuẩn, phiên bản, dữ liệu hoặc thẩm quyền để kết luận.
- `suggestion`: đề xuất chuẩn hóa, không tự thay đổi thiết kế.

## Danh mục 18 ngành

### `general-cad` — CAD tổng quát

**Tham chiếu:** ISO 128, ISO 129-1, ISO 5455, ISO 5457, ISO 7200, ISO 13567;
Autodesk CAD Standards/DWS.

**Kiểm tra:** đơn vị, WCS/UCS, layer, màu, linetype, lineweight, ByLayer, text
style, dim style, font, layout, viewport, khổ giấy, title block, revision, plot,
đối tượng trùng, zero-length, đối tượng không render và file nguồn.

**Cảnh báo:** `Layer1/Misc`, sai ByLayer, dim không liên kết, sai scale, text bị
che, thiếu revision hoặc bản vẽ không plot được.

### `building` — Xây dựng tổng hợp

**Tham chiếu:** ISO 19650 về quản lý thông tin; ISO 128/129/5457/7200 cho hồ sơ;
quy chuẩn xây dựng Việt Nam và yêu cầu CDE của dự án.

**Kiểm tra:** mã hồ sơ, bộ môn, revision, trạng thái phát hành, model/sheet,
xref, cao độ, trục, thống nhất giữa bộ môn và phạm vi thay đổi.

**Cảnh báo:** thiếu mã/revision, xref mất đường dẫn, mặt bằng và mặt cắt lệch,
không xác định được phiên bản hoặc dùng sai bộ môn.

### `architecture` — Kiến trúc

**Tham chiếu:** ISO 128, ISO 129-1, ISO 5455, ISO 5457, ISO 7200, ISO 13567;
QCVN/TCVN kiến trúc, tiếp cận và công năng do dự án chọn.

**Kiểm tra:** tường kín, cửa/cửa sổ, lối đi, cầu thang, cao độ, phòng, diện tích,
nội thất, kích thước chuỗi và room/door/window schedule.

**Cảnh báo:** phòng không kín, cửa trùng tường, cửa thiếu hướng mở, cầu thang
không nối tầng, schedule không khớp hình học, lối đi bị chặn.

### `structural` — Kết cấu

**Tham chiếu:** TCVN 2737, TCVN 5574, TCVN 5575, TCVN 9386 khi áp dụng; hoặc
EN 1990–1999, ACI 318, ASCE 7 theo yêu cầu dự án.

**Kiểm tra:** liên tục cột/dầm/vách/sàn/móng, lưới trục, cao độ, tiết diện, ký
hiệu thép, chi tiết liên kết, layer kết cấu và mặt bằng–mặt đứng–mặt cắt.

**Error/warning:** zero-length, trùng hình học, lệch trục, đứt đoạn, layer rỗng,
thiếu chi tiết hoặc mâu thuẫn giữa các hình.

**Bắt buộc kỹ sư:** tải trọng, tổ hợp, vật liệu, nền móng, kháng chấn, độ võng,
ổn định, chịu lửa và kết luận an toàn.

### `fire` — Phòng cháy chữa cháy

**Tham chiếu:** QCVN 06:2022/BXD và văn bản Việt Nam đang có hiệu lực; NFPA 1,
10, 13, 20, 25, 72, 101 khi dự án áp dụng.

**Kiểm tra:** lối thoát, cửa thoát, hướng mở, hành lang, cầu thang, khoảng cách
thoát, khoang/ngăn cháy, báo cháy, sprinkler, họng nước, bơm, hút khói, tăng áp,
đường xe chữa cháy và ký hiệu PCCC.

**Phân loại:** lối thoát bị chặn là `error`; thiếu ký hiệu/dữ liệu là `warning`;
thiếu công năng, số người, cấp nguy hiểm cháy hoặc tiêu chuẩn địa phương là
`review`. Không tự kết luận đạt PCCC hoặc đạt thẩm duyệt.

### `mechanical` — Cơ khí

**Tham chiếu:** ISO 1101, ISO 286, ISO 5459, ISO 14405, ISO 2553, ISO 21920-1,
ISO 12100; ASME Y14.5/Y14.2 khi dùng hệ ASME.

**Kiểm tra:** hình chiếu, mặt cắt, datum, GD&T, fit, ren, then, bề mặt, mối hàn,
vật liệu, bulông, ổ lăn, parts list, balloon, title block và revision.

**Cảnh báo:** datum không xác định, dung sai mâu thuẫn, ký hiệu hàn thiếu,
ren/fit không rõ, balloon không liên kết parts list hoặc chi tiết không đủ chế tạo.

### `pid` — P&ID / Quy trình công nghệ

**Tham chiếu:** ISO 10628-2, ISO 14617, ISA-5.1; IEC 60617 cho ký hiệu điện.

**Kiểm tra:** tag thiết bị/van, line number, line class, port, hướng dòng,
điểm nối, tín hiệu, instrument index, equipment list, line list và topology.

**Cảnh báo:** tag trùng, tuyến hở, port không nối, thiết bị thiếu, line class
không rõ, ký hiệu ngoài catalogue hoặc sơ đồ và layout không khớp.

**Không suy luận:** công suất, áp suất, vật liệu, nhiệt độ hoặc điều kiện vận
hành nếu P&ID không cung cấp.

### `electrical` — Điện

**Tham chiếu:** IEC 60617, IEC 60364, IEC 61439, IEC 60204-1, NFPA 70/NEC khi
được dự án yêu cầu.

**Kiểm tra:** ký hiệu, mạch, dây, cáp, tủ, panel, tag, bảo vệ, nối đất, đường
đi cáp, phân biệt nguồn/điều khiển và bảng tải.

**Cảnh báo:** dây hở, tag trùng, mạch không có bảo vệ, ký hiệu sai hoặc thiếu
điện áp/dòng/tải.

### `mep` — Cơ điện công trình

**Tham chiếu:** ASHRAE 62.1/62.2 và 90.1 khi áp dụng; NFPA liên quan; QCVN/TCVN
MEP của dự án.

**Kiểm tra:** HVAC, điện, cấp thoát nước, cao độ tuyến, khoảng bảo trì, shaft,
xuyên tường/sàn, va chạm với dầm/cột/trần và thiết bị.

**Cảnh báo:** giao cắt chưa xử lý, thiếu khoảng bảo trì, tuyến không liên tục,
thiết bị sai cao độ hoặc không có access panel.

### `water-supply` — Cấp nước

**Tham chiếu:** QCVN/TCVN cấp nước của dự án, EN 806 hoặc AWWA khi được chỉ định.

**Kiểm tra:** tuyến ống, đường kính, cao độ, van, đồng hồ, bể, bơm, hướng dòng,
áp lực thiết kế, bảo trì và giao cắt với kết cấu.

**Cảnh báo:** tuyến hở, thiếu đường kính, van không tiếp cận, giao cắt không có
chi tiết xuyên hoặc không có dữ liệu áp lực.

### `drainage` — Thoát nước

**Tham chiếu:** QCVN/TCVN thoát nước của dự án, EN 12056 khi áp dụng.

**Kiểm tra:** hướng dốc, cao độ đáy, hố ga, cửa thăm, ống thông khí, điểm xả,
tách nước mưa/nước thải và khả năng bảo trì.

**Cảnh báo:** dốc ngược, cao độ mâu thuẫn, tuyến không có điểm xả, thiếu cửa
thăm hoặc giao cắt với móng/sàn chưa xử lý.

### `civil` — Hạ tầng kỹ thuật

**Tham chiếu:** QCVN 07:2023/BXD và TCVN hạ tầng tương ứng; ISO 13567, ISO 19650.

**Kiểm tra:** san nền, cao độ, đường nội bộ, thoát nước, hạ tầng ngầm, ranh,
hành lang kỹ thuật, giao cắt và cao độ đấu nối.

**Cảnh báo:** cao độ không liên tục, hạ tầng chồng lấn, thiếu hành lang, tuyến
không nối hoặc không thể thi công/bảo trì.

### `transportation` — Giao thông đường bộ

**Tham chiếu:** TCVN 4054, QCVN 41, tiêu chuẩn thiết kế đường/nút giao của dự án;
AASHTO khi áp dụng.

**Kiểm tra:** tim tuyến, bình đồ, trắc dọc, trắc ngang, bán kính, dốc, siêu cao,
tầm nhìn, biển báo, vạch sơn, thoát nước và hành lang an toàn.

**Cảnh báo:** bán kính/dốc bất thường, thiếu tầm nhìn, biển báo/vạch sai vị trí,
thoát nước không liên tục hoặc xung đột công trình hiện hữu.

### `bridge` — Cầu

**Tham chiếu:** TCVN 11823 và tiêu chuẩn tải trọng/cầu của dự án; AASHTO LRFD
khi áp dụng.

**Kiểm tra:** tim cầu, mố, trụ, gối, khe co giãn, dầm, bản mặt cầu, lan can,
thoát nước, cao độ thông thuyền/khổ giới hạn và liên tục giữa các sheet.

**Cảnh báo:** sai trục, thiếu gối/khe, cao độ không khớp, lan can/thoát nước
thiếu hoặc chi tiết không liên kết với bản vẽ kết cấu.

### `landscape` — Cảnh quan

**Tham chiếu:** QCVN/TCVN cảnh quan, tiếp cận, cây xanh và hạ tầng của dự án;
ISO 21542 khi yêu cầu tiếp cận công trình.

**Kiểm tra:** cao độ sân, dốc thoát nước, cây, bồn, lát nền, lối tiếp cận,
chiếu sáng, tưới và khoảng tránh công trình ngầm.

**Cảnh báo:** dốc chảy vào nhà, cây xung đột hạ tầng, lối tiếp cận bị chặn,
thiếu khoảng bảo trì hoặc vật liệu chưa xác định.

### `surveying` — Trắc địa

**Tham chiếu:** ISO 17123, ISO 191xx khi áp dụng; quy chuẩn tọa độ/cao độ quốc
gia và yêu cầu dự án.

**Kiểm tra:** hệ tọa độ, datum, mốc, đơn vị, cao độ, điểm khống chế, độ chính
xác, metadata và truy nguyên nguồn đo.

**Cảnh báo:** thiếu hệ tọa độ, trộn datum, sai đơn vị, mốc không có nguồn hoặc
điểm đo không có độ chính xác.

### `geotechnical` — Địa kỹ thuật

**Tham chiếu:** TCVN 9362 và tiêu chuẩn nền móng/địa kỹ thuật của dự án;
Eurocode 7 (EN 1997) khi áp dụng.

**Kiểm tra:** hố khoan, lớp đất, mực nước, cao độ nền, taluy, móng, tường chắn,
tải truyền xuống nền và thống nhất giữa khảo sát với bản vẽ.

**Cảnh báo:** thiếu số liệu địa chất, móng ngoài lớp đất khảo sát, taluy không
có chi tiết ổn định hoặc cao độ đào đắp mâu thuẫn.

### `construction` — Biện pháp thi công

**Tham chiếu:** QCVN 18:2021/BXD, ISO 45001 và quy trình an toàn của dự án.

**Kiểm tra:** trình tự thi công, vùng nguy hiểm, giàn giáo, chống đỡ tạm, nâng
hạ, đào đất, làm việc trên cao, lối thoát, rào chắn, PPE và biển báo.

**Cảnh báo:** thiếu chống đỡ, vùng nguy hiểm không rào, đường công vụ xung đột,
thiếu lối thoát hoặc trình tự thể hiện không khả thi.

## Nguyên tắc cập nhật

- Tên tiêu chuẩn trong tài liệu không mặc định là phiên bản đang có hiệu lực cho
  mọi dự án.
- Mỗi rule phải có `id`, `nganh`, `phien_ban`, `nguon`, `hieu_luc`, `rules` và
  trạng thái duyệt.
- Khi tiêu chuẩn đổi, thêm bản mới với ID/phiên bản mới; không xóa bản cũ của
  hồ sơ đã phát hành.
- Không trộn yêu cầu giữa các hệ Việt Nam, ISO, EN, ACI, ASCE, NFPA hoặc ASME
  nếu dự án chưa xác nhận hệ áp dụng.
- Chỉ dùng bản tiêu chuẩn được phép sử dụng và lưu nguồn chính thức cùng metadata.

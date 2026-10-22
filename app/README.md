# cadtroly — AI Trợ lý cho AutoCAD (MCP)

Đây là **fork** của [U-C4N/Autocad-MCP](https://github.com/U-C4N/Autocad-MCP) (AutoCAD MCP Pro, MIT; xem `UPSTREAM.md`).
Mã upstream nằm ngay trong thư mục này (`server.py`, `backends/`, `engineering/`…), không cài từ GitHub. Lớp riêng
trong `cadtroly/`: bóc khối lượng ra Excel có truy vết, kiểm tra bản vẽ theo bộ quy tắc, kho tri thức dạng thư mục,
skill chuyên ngành. Tất cả chạy trong **một server** tên `cadtroly`, tool upstream giữ nguyên tên (không tiền tố).

Chạy được **không cần AutoCAD** (engine ezdxf, đọc DXF; DWG cần ODA File Converter). Có AutoCAD thì các tool upstream
tự chuyển sang COM để sửa vẽ live.

## Cài

```bash
pip install -e ".[dev,llm]"
cadtroly init --kho D:\CAD-kho   # tạo kho + config.json
cadtroly sample                  # sinh samples/mat-bang-tang-3.dxf để thử
```

## Người dùng cuối: giao diện, không gõ lệnh

Windows: bấm đúp `run.bat`. Linux/macOS: `./run.sh`. Lần đầu cài `pip install -e ".[web,llm]"`.
Mở cửa sổ "AI Trợ lý AutoCAD" (pywebview; không có thì mở trình duyệt tại http://127.0.0.1:8765):

1. **Chọn bản vẽ…** (hộp thoại) hoặc kéo thả file .dxf.
2. **Σ Bóc khối lượng**: bảng ánh xạ hiện ra, mỗi dòng chọn Công tác / ĐV / Cách tính từ danh sách thả xuống rồi bấm ✓.
   Hoặc **Duyệt tất cả B**. Bấm **Tính khối lượng**, rồi **Xuất Excel** (có nút tải về).
3. **Kiểm tra theo chuẩn**: chọn bộ quy tắc trong danh sách, bấm Kiểm tra. Nút ⌖ chép lệnh zoom để dán vào AutoCAD.
4. **Hỏi trợ lý**: gõ tiếng Việt, Claude tự bấm các nút thay anh.
5. **Cài đặt**: bấm **Đăng nhập Claude** → trình duyệt mở → đăng nhập → quay lại là xong (OAuth qua Anthropic CLI
   `ant auth login`, token lưu trong profile `%APPDATA%\Anthropic` / `~/.config/anthropic`, SDK tự đọc; đây là tài khoản
   tổ chức API tính tiền theo token, không phải gói Claude Pro/Max). Máy không có trình duyệt: nút "Không có trình duyệt…"
   hiện link, mở ở máy khác, dán mã vào ô. Chưa cài `ant` thì dán API key (lưu vào Credential Manager/keyring).

Mở thẳng một bản vẽ: `http://127.0.0.1:8765/?path=D:/x.dxf&auto=kl` (dùng cho nút gọi từ AutoCAD sau này).

## Bàn giao đối tác: bản chạy ngay, không cần Python

```bat
pip install -e ".[web,llm]" pyinstaller
build\build.bat            :: Windows → dist\AI-Tro-ly-AutoCAD\ (≈240 MB, onedir) ; Linux: build/build.sh trên máy Linux
```

Nén cả thư mục `dist\AI-Tro-ly-AutoCAD` gửi đi. Trong đó: `AI-Tro-ly-AutoCAD.exe`, `HUONG-DAN.txt`, `bin\ant.exe`
(Anthropic CLI 1.44.0, đã kiểm SHA-256, để nút Đăng nhập Claude chạy được), kho mẫu nhúng trong `_internal\kho-mac-dinh`
(tự chép vào `%USERPROFILE%\CAD-kho` lần chạy đầu). Exe không chứa MCP/FastMCP và mã upstream, chỉ phần UI + bóc KL + kiểm tra.
Đã chạy thử exe: mở bản vẽ, bóc, xuất Excel, kiểm tra, trạng thái đăng nhập đều đúng.
Cần WebView2 Runtime (Win10/11 có sẵn); thiếu thì tự mở trình duyệt. Tham số: `--browser --port 8765 --kho D:\CAD-kho`.

## Nhật ký và báo lỗi về dev

- Mọi log (kể cả lỗi chưa bắt, lỗi thread, lỗi HTTP) ghi **theo ngày** `CAD-kho/log/app-YYYY-MM-DD.log`, tự sang file
  mới sau nửa đêm, xoá file cũ hơn 30 ngày khi khởi động. Nhật ký thao tác (JSONL) cũng theo ngày: `log/YYYY-MM-DD.log`. `cadtroly/errlog.py`.
- API trả lỗi dạng `{code, message, hint, detail}`; UI hiện hộp tiếng Việt kèm nút **Gửi báo lỗi cho người phát triển**.
- Nút gửi: gom `log/`, `config.json` (che key), danh sách file kho, thông tin máy → zip → POST multipart tới
  `config.report.url` (Bearer `config.report.token`). Gửi không được thì lưu `CAD-kho/out/bao-loi-*.zip`. Crash lần trước
  → lần mở sau tự gửi (`report.auto_on_crash`).
- Phía dev: `tools/report_server.py` (FastAPI) nhận vào `<dir>/<ngày>/RPT-*.zip + .json`, có `GET /cadtroly/reports`,
  tuỳ chọn báo Telegram. Chạy sau nginx, đặt `client_max_body_size 50m`. Khi triển khai xong, ghi URL + token vào
  `ReportConfig` mặc định (cadtroly/config.py) rồi build lại để bản giao đối tác tự gửi.

## Dùng với Claude Code / Claude Desktop

Khi chạy MCP bằng `.mcp.json` hoặc `cadtroly mcp`, server tự kiểm tra các gói
cần cho PDF/DXF, AutoCAD COM và các tool vẽ. Chỉ gói còn thiếu mới được cài
qua `python -m pip install -e .`; không cài lại ở mỗi lần chạy. Tắt hành vi này
bằng `CADTROLY_AUTO_INSTALL=false` nếu máy bị giới hạn mạng.

`.mcp.json` (có sẵn trong thư mục này):

```json
{"mcpServers": {"cadtroly": {"command": "python", "args": ["-m", "cadtroly.mcp"],
  "env": {"CADTROLY_KHO": "D:\\CAD-kho", "AUTOCAD_MCP_BACKEND": "auto", "TOOL_PROFILE": "lean"}}}}
```

Rồi hỏi tự nhiên: *"bóc khối lượng file samples/mat-bang-tang-3.dxf"*, *"kiểm tra bản vẽ theo chuan-cong-ty"*.

## Tool

| Nhóm | Tool | Việc |
|---|---|---|
| đọc | `drawing_read`, `drawing_entities` | số liệu bản vẽ, handle, toạ độ, dài, diện tích, text |
| bóc KL (luồng A) | `takeoff_propose` → `takeoff_decide` → `takeoff_compute` → `takeoff_export`; `takeoff_run` cả thư mục | ánh xạ A/B/C, tính, Excel 4 sheet có handle + lệnh zoom |
| kiểm tra (luồng D) | `check_rulesets`, `check_run` | rà theo `.rules.json`, kết quả kèm điều khoản, handle, tự sửa được không |
| kho | `kho_status`, `kho_rules_export/import`, `kho_skills`, `kho_skill_toggle`, resource `cadtroly://skill/{name}` | kho thư mục, không train |
| AutoCAD (upstream) | `drawing_open`, `entity_*`, `layer_*`, `block_*`, `dimension_*`, `system_run_lisp`, `view_screenshot`, `transaction_*`, `arch_*`, `drawing_understand`, `drawing_diff`… (59 ở `TOOL_PROFILE=lean`, 247 ở `full`) | mở/lưu, tạo/sửa entity, layer, block, dimension, LISP, screenshot, transaction/undo, arch_*, understand, diff |

## Kho (thư mục trên máy người dùng)

```
CAD-kho/
  tieu-chuan/   <id>.rules.json   bảng quy tắc bóc từ tiêu chuẩn, mỗi dòng có duyet true/false
  quy-tac/      anh-xa.json       ánh xạ layer/block → công tác, tự lớn khi kỹ sư xác nhận
                <id>.rules.json   chuẩn công ty
  chi-tiet/                       chi tiết LISP tham số (chưa có mẫu)
  du-an-cu/<ten>/ho-so.json
  skill/<ten>/SKILL.md            skill chuyên ngành, bật/tắt bằng file .disabled
  log/  out/
```

Mẫu trong `samples/kho/`.

## Tin cậy A/B/C
- **A** đếm/đo trực tiếp theo quy tắc đơn vị hoặc attribute block.
- **B** đoán từ tên layer/block, hoặc chiều cao suy từ text `H=`. Cần kỹ sư xác nhận; xác nhận một lần là thành quy tắc.
- **C** không xác định (layer 0, line rời). Khối lượng để trống, Excel ghi "khoanh để người đếm". Không bịa.

## Test

```bash
python -m pytest -q                      # 11 test cadtroly (reader, bóc KL, Excel, check, MCP, web API, LLM mock)
python -m pytest -q upstream_tests/      # test của upstream (182 file, chạy lâu)
```

## Chưa làm / cần máy có AutoCAD
- COM live, preview revision cloud, UNDO group, PostMessage không cướp focus: code nền đã có trong `backends/com_backend.py`, **chưa test trên AutoCAD thật**.
- Palette WebView2 trong AutoCAD: giao diện web đã có (`cadtroly ui`), chưa nhúng vào AutoCAD (cần plugin .NET host WebView2 trỏ tới URL trên).
- `tieu-chuan/qcvn-18-2021.rules.json` là **mẫu**, chưa bóc từ văn bản thật; mọi dòng `duyet=false` nên `check_run` bỏ qua cho tới khi kỹ sư duyệt.
- LLM: Claude qua SDK `anthropic` (model fast/main/hard = Haiku/Sonnet/Opus 5.5), Gemini và OpenAI-compatible qua httpx. Mới test mock, chưa chạy key thật.

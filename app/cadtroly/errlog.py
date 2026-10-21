"""Ghi lỗi và báo lỗi cho người dùng cuối.

- Mọi log Python (kể cả lỗi chưa bắt, lỗi trong thread, lỗi uvicorn) ghi theo NGÀY: kho/log/app-YYYY-MM-DD.log,
  tự sang file mới khi qua ngày, giữ 30 ngày (xoá file cũ hơn khi khởi động).
  (kho/log/YYYY-MM-DD.log là nhật ký thao tác dạng JSONL của Kho.log, cũng theo ngày.)
- Mã lỗi + câu tiếng Việt dễ hiểu để hộp thoại UI hiện; chi tiết kỹ thuật chỉ nằm trong log.
- make_report(): gom log + config (đã che key) + thông tin máy thành một file zip trong kho/out để gửi cho người hỗ trợ.
"""
from __future__ import annotations

import io
import json
import logging
import os
import re
import platform
import sys
import threading
import traceback
import zipfile
from datetime import datetime
from pathlib import Path

LOG = logging.getLogger("cadtroly")

# mã lỗi → (câu cho người dùng, gợi ý xử lý)
ERRORS: dict[str, tuple[str, str]] = {
    "E-FILE-01": ("Không đọc được bản vẽ.", "Kiểm tra file là .dxf (DWG phải xuất DXF từ AutoCAD: SAVEAS → DXF) và không bị khoá."),
    "E-FILE-02": ("Không ghi được file kết quả.", "Đóng file Excel đang mở, kiểm tra ổ đĩa còn chỗ."),
    "E-RULE-01": ("Không thấy bộ quy tắc.", "Vào tab Kho, kiểm tra file .rules.json trong CAD-kho\\quy-tac hoặc tieu-chuan."),
    "E-AI-01": ("Chưa đăng nhập AI hoặc API key sai.", "Vào Cài đặt → Đăng nhập Claude, hoặc dán lại API key."),
    "E-AI-02": ("AI đang quá tải hoặc hết hạn mức.", "Thử lại sau vài phút."),
    "E-AI-03": ("Dịch vụ AI báo lỗi.", "Thử lại; vẫn lỗi thì tạo file báo lỗi gửi hỗ trợ."),
    "E-AI-04": ("Không kết nối được mạng tới AI.", "Kiểm tra Internet, proxy hoặc tường lửa công ty."),
    "E-AI-05": ("AI từ chối yêu cầu này.", "Đổi cách hỏi; không gửi dữ liệu nhạy cảm."),
    "E-CAD-01": ("Không nối được AutoCAD.", "Bấm ESC trong AutoCAD rồi thử lại; đóng hộp thoại đang mở."),
    "E-APP-99": ("Có lỗi không mong muốn.", "Bấm 'Tạo file báo lỗi' và gửi cho người hỗ trợ."),
}


KEEP_DAYS = 30


class DailyFileHandler(logging.FileHandler):
    """Ghi vào app-<ngày>.log; qua ngày thì tự mở file mới. Không đổi tên file cũ nên dễ gom theo ngày."""

    def __init__(self, log_dir: Path):
        self.log_dir = Path(log_dir)
        self._day = datetime.now().strftime("%Y-%m-%d")
        super().__init__(self._path_for(self._day), encoding="utf-8")
        self._cadtroly = True

    def _path_for(self, day: str) -> str:
        return str(self.log_dir / f"app-{day}.log")

    def emit(self, record):
        day = datetime.now().strftime("%Y-%m-%d")
        if day != self._day:
            self.acquire()
            try:
                self.close()
                self._day = day
                self.baseFilename = self._path_for(day)
                self.stream = self._open()
            finally:
                self.release()
        super().emit(record)


def today_log(kho: Path) -> Path:
    return kho / "log" / f"app-{datetime.now():%Y-%m-%d}.log"


def _prune(log_dir: Path, keep_days: int = KEEP_DAYS) -> int:
    from datetime import timedelta
    cutoff = (datetime.now() - timedelta(days=keep_days)).strftime("%Y-%m-%d")
    n = 0
    for f in log_dir.glob("*.log"):
        m = re.search(r"(\d{4}-\d{2}-\d{2})", f.name)
        if m and m.group(1) < cutoff:
            try:
                f.unlink()
                n += 1
            except OSError:
                pass
    return n


def setup_logging(kho: Path) -> Path:
    log_dir = kho / "log"
    log_dir.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    for h in list(root.handlers):
        if getattr(h, "_cadtroly", False):
            if Path(getattr(h, "log_dir", "")) == log_dir:
                return today_log(kho)
            root.removeHandler(h)   # kho khác (đổi kho / test): chuyển log sang kho mới
            h.close()
    h = DailyFileHandler(log_dir)
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    root.addHandler(h)
    root.setLevel(logging.INFO)
    for noisy in ("httpx", "httpx2", "httpcore", "uvicorn.access"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    def hook(exc_type, exc, tb):
        LOG.critical("Lỗi chưa bắt: %s", "".join(traceback.format_exception(exc_type, exc, tb)))
    sys.excepthook = hook

    def thook(args):
        LOG.critical("Lỗi trong thread %s: %s", args.thread.name if args.thread else "?",
                     "".join(traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback)))
    threading.excepthook = thook
    pruned = _prune(log_dir)
    LOG.info("=== khởi động · %s · Python %s · %s%s ===", datetime.now().isoformat(timespec="seconds"),
             platform.python_version(), platform.platform(), f" · xoá {pruned} log cũ" if pruned else "")
    return today_log(kho)


def friendly(code: str, detail: str = "") -> dict:
    msg, hint = ERRORS.get(code, ERRORS["E-APP-99"])
    return {"code": code, "message": msg, "hint": hint, "detail": detail[:300]}


def classify(exc: BaseException) -> str:
    """Đoán mã lỗi từ exception để UI hiện câu dễ hiểu."""
    s = f"{type(exc).__name__}: {exc}"
    if isinstance(exc, (FileNotFoundError, PermissionError)) or "Không đọc được" in s or "DXF" in s or "dxf" in s:
        return "E-FILE-01"
    if "quy tắc" in s or "ruleset" in s.lower():
        return "E-RULE-01"
    for code in ERRORS:
        if code in s:
            return code
    if isinstance(exc, (OSError,)):
        return "E-FILE-02"
    return "E-APP-99"


def recent_errors(kho: Path, n: int = 20, days: int = 7) -> list[dict]:
    """Lỗi/cảnh báo gần nhất, gom từ các file app-<ngày>.log của `days` ngày gần nhất."""
    files = sorted((kho / "log").glob("app-*.log"), reverse=True)[:days]
    out: list[dict] = []
    for path in files:
        block: list[str] = []
        day_out: list[dict] = []
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            is_head = len(line) > 24 and line[4] == "-" and line[10] == " " and any(
                f" {lv} " in line[:60] for lv in ("ERROR", "CRITICAL", "WARNING"))
            if is_head:
                if block:
                    day_out.append(_parse_block(block))
                block = [line]
            elif block and (line.startswith(" ") or line.startswith("Traceback") or line.startswith("  File")):
                block.append(line)
            elif block:
                day_out.append(_parse_block(block))
                block = []
        if block:
            day_out.append(_parse_block(block))
        out.extend(day_out[::-1])
        if len(out) >= n:
            break
    return out[:n]


def _parse_block(block: list[str]) -> dict:
    head = block[0]
    t = head[:19]
    level = "lỗi" if (" ERROR " in head or " CRITICAL " in head) else "cảnh báo"
    msg = head.split(": ", 1)[1] if ": " in head else head
    code = next((c for c in ERRORS if c in head), None)
    return {"t": t, "muc": level, "code": code, "message": friendly(code)["message"] if code else msg[:160],
            "detail": "\n".join(block)[-1500:]}


def make_report(kho: Path, cfg_path: Path | None = None, note: str = "") -> Path:
    out_dir = kho / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    zpath = out_dir / f"bao-loi-{stamp}.zip"
    info = {
        "thoi_gian": datetime.now().isoformat(timespec="seconds"),
        "ghi_chu": note,
        "he_dieu_hanh": platform.platform(),
        "python": platform.python_version(),
        "frozen": bool(getattr(sys, "frozen", False)),
        "exe": sys.executable,
        "kho": str(kho),
        "bien_moi_truong": {k: ("***" if "KEY" in k or "TOKEN" in k else v) for k, v in os.environ.items()
                            if k.startswith(("CADTROLY", "AUTOCAD_MCP", "TOOL_", "ANTHROPIC", "GEMINI", "OPENAI"))},
    }
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("thong-tin.json", json.dumps(info, ensure_ascii=False, indent=2))
        for f in sorted((kho / "log").glob("*")):
            if f.is_file() and f.stat().st_size < 20_000_000:
                z.write(f, f"log/{f.name}")
        cfg = cfg_path or (kho / "config.json")
        if cfg.exists():
            try:
                d = json.loads(cfg.read_text(encoding="utf-8"))
                z.writestr("config.json", json.dumps(d, ensure_ascii=False, indent=2))
            except Exception:
                pass
        # danh sách file trong kho (tên thôi, không nội dung bản vẽ)
        buf = io.StringIO()
        for f in sorted(kho.rglob("*")):
            if f.is_file() and "out" not in f.parts:
                buf.write(f"{f.relative_to(kho)}\t{f.stat().st_size}\n")
        z.writestr("kho-danh-sach.txt", buf.getvalue())
    LOG.info("Đã tạo file báo lỗi %s", zpath)
    return zpath


# ---------------------------------------------------------------- gửi về dev
def send_report(url: str, zip_path: Path, *, token: str = "", meta: dict | None = None, timeout: int = 30) -> dict:
    """POST gói báo lỗi lên máy chủ của dev (multipart). Không có thư viện ngoài: dùng urllib.

    Máy chủ nhận: tools/report_server.py (FastAPI) hoặc bất kỳ endpoint nào nhận multipart 'file' + 'meta'.
    Trả về {"ok": True, "id": ...} khi máy chủ nhận; lỗi thì {"ok": False, "error": ...} và KHÔNG ném exception.
    """
    import urllib.error
    import urllib.request
    import uuid

    boundary = "----cadtroly" + uuid.uuid4().hex
    meta_json = json.dumps(meta or {}, ensure_ascii=False)
    body = io.BytesIO()
    body.write(f"--{boundary}\r\nContent-Disposition: form-data; name=\"meta\"\r\n\r\n{meta_json}\r\n".encode("utf-8"))
    body.write(f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{zip_path.name}\"\r\n"
               f"Content-Type: application/zip\r\n\r\n".encode("utf-8"))
    body.write(zip_path.read_bytes())
    body.write(f"\r\n--{boundary}--\r\n".encode("utf-8"))
    req = urllib.request.Request(url, data=body.getvalue(), method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
            try:
                data = json.loads(raw)
            except Exception:
                data = {"raw": raw[:200]}
            LOG.info("Đã gửi báo lỗi tới %s: %s", url, data)
            return {"ok": True, **data}
    except urllib.error.HTTPError as exc:
        LOG.warning("Gửi báo lỗi thất bại HTTP %s", exc.code)
        return {"ok": False, "error": f"máy chủ trả {exc.code}"}
    except Exception as exc:
        LOG.warning("Gửi báo lỗi thất bại: %s", exc)
        return {"ok": False, "error": str(exc)[:200]}

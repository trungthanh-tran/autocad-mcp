"""Điểm vào cho bản đóng gói (exe): mở giao diện, không cần Python trên máy đối tác.

- Kho mặc định: %USERPROFILE%\\CAD-kho (Windows) hoặc ~/CAD-kho. Lần đầu chạy, chép kho mẫu đi kèm
  (quy tắc chuẩn công ty, bảng QCVN mẫu, skill) vào đó nếu còn trống.
- Nếu cạnh exe có thư mục `bin/` chứa ant.exe thì thêm vào PATH để nút Đăng nhập Claude dùng được.
- Tham số: --browser (mở trình duyệt thay vì cửa sổ), --port N, --kho <thư mục>.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


def _bundle_dir() -> Path:
    # PyInstaller: dữ liệu đi kèm nằm ở sys._MEIPASS (onefile) hoặc cạnh exe (onedir)
    base = getattr(sys, "_MEIPASS", None)
    return Path(base) if base else Path(__file__).resolve().parent.parent


def _exe_dir() -> Path:
    return Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent.parent


def seed_kho(kho: Path) -> int:
    """Chép kho mẫu vào kho người dùng, chỉ những file chưa có. Trả về số file đã chép."""
    src = _bundle_dir() / "kho-mac-dinh"
    if not src.exists():
        return 0
    n = 0
    for f in src.rglob("*"):
        if f.is_file():
            dst = kho / f.relative_to(src)
            if not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)
                n += 1
    return n


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="AI Trợ lý AutoCAD")
    ap.add_argument("--browser", action="store_true")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--kho")
    a = ap.parse_args(argv)
    if a.kho:
        os.environ["CADTROLY_KHO"] = a.kho
    # ant.exe đi kèm
    bin_dir = _exe_dir() / "bin"
    if bin_dir.exists():
        os.environ["PATH"] = str(bin_dir) + os.pathsep + os.environ.get("PATH", "")
    from cadtroly.config import Config
    cfg = Config.load()
    cfg.ensure_dirs()
    if not cfg.path.exists():
        cfg.save()
    seed_kho(cfg.kho)
    from cadtroly import errlog
    errlog.setup_logging(cfg.kho)
    _send_last_crash(cfg)
    crash_flag = cfg.kho / "log" / "crash.flag"
    try:
        from cadtroly.web.app import serve
        serve(port=a.port, window=not a.browser)
    except Exception:
        errlog.LOG.exception("Không khởi động được giao diện")
        crash_flag.write_text("1", encoding="utf-8")
        _msgbox("AI Trợ lý AutoCAD không khởi động được.\nLỗi đã được ghi lại và sẽ tự gửi cho người phát triển ở lần mở sau.\n"
                + str(errlog.today_log(cfg.kho)))
        return 1
    return 0


def _send_last_crash(cfg) -> None:
    """Lần mở trước bị crash → tự gom log gửi cho dev (nếu cấu hình cho phép), rồi xoá cờ."""
    from cadtroly import errlog
    flag = cfg.kho / "log" / "crash.flag"
    if not flag.exists():
        return
    try:
        if cfg.report.auto_on_crash and cfg.report.url:
            z = errlog.make_report(cfg.kho, cfg.path, "tự gửi sau crash")
            errlog.send_report(cfg.report.url, z, token=cfg.report.token,
                               meta={"don_vi": cfg.report.don_vi, "note": "auto crash", "version": cfg.version})
    finally:
        flag.unlink(missing_ok=True)


def _msgbox(text: str) -> None:
    try:
        if sys.platform == "win32":
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, text, "AI Trợ lý AutoCAD", 0x10)
        else:
            print(text, file=sys.stderr)
    except Exception:
        pass


if __name__ == "__main__":
    sys.exit(main())

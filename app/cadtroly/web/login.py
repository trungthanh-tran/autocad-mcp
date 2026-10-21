"""Đăng nhập Claude kiểu bấm nút → trình duyệt → callback, qua Anthropic CLI `ant auth login`.

Cơ chế: `ant` mở trình duyệt, nhận callback trên cổng cục bộ, đổi lấy token ngắn hạn và lưu profile
(%APPDATA%\\Anthropic trên Windows, ~/.config/anthropic trên Linux/macOS). SDK anthropic đọc profile
tự động khi KHÔNG đặt ANTHROPIC_API_KEY. Không có trình duyệt (máy chủ Linux) thì dùng chế độ
--no-browser: tool hiện link, người dùng mở trên máy khác, dán mã vào ô.

Đây là OAuth cho tổ chức API (tính tiền theo token), không phải gói Claude Pro/Max của claude.ai.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import threading


class Login:
    def __init__(self):
        self.proc: subprocess.Popen | None = None
        self.url: str | None = None
        self.log: list[str] = []
        self.mode: str | None = None

    @staticmethod
    def ant() -> str | None:
        return shutil.which("ant")

    def status(self) -> dict:
        a = self.ant()
        if not a:
            return {"installed": False, "logged_in": False,
                    "hint": "Chưa cài Anthropic CLI. Tải `ant` từ github.com/anthropics/anthropic-cli/releases "
                            "(Windows: giải nén ant.exe vào thư mục trong PATH; macOS: brew install anthropics/tap/ant).",
                    "url": self.url, "running": self.proc is not None and self.proc.poll() is None, "log": self.log[-5:]}
        try:
            env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
            r = subprocess.run([a, "auth", "status"], capture_output=True, text=True, timeout=15, env=env,
                               encoding="utf-8", errors="replace")
            out = (r.stdout + r.stderr).strip()
        except Exception as exc:
            out = f"lỗi: {exc}"
        logged = bool(out) and not re.search(r"not configured|run `ant auth login`|not logged|no credential|lỗi:", out, re.I)
        return {"installed": True, "logged_in": logged, "detail": out[:400], "url": self.url,
                "running": self.proc is not None and self.proc.poll() is None, "log": self.log[-5:],
                "api_key_set": bool(os.environ.get("ANTHROPIC_API_KEY"))}

    def start(self, no_browser: bool = False, profile: str | None = None) -> dict:
        a = self.ant()
        if not a:
            return self.status()
        if self.proc and self.proc.poll() is None:
            return {"ok": True, "already": True} | self.status()
        cmd = [a, "auth", "login"]
        if profile:
            cmd += ["--profile", profile]
        if no_browser:
            cmd.append("--no-browser")
        self.url, self.log, self.mode = None, [], "no-browser" if no_browser else "browser"
        env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
        self.proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     text=True, env=env, bufsize=1)

        def pump():
            for line in self.proc.stdout:  # type: ignore[union-attr]
                line = line.rstrip()
                self.log.append(line)
                m = re.search(r"https?://\S+", line)
                if m and self.url is None:
                    self.url = m.group()
        threading.Thread(target=pump, daemon=True).start()
        return {"ok": True, "mode": self.mode}

    def submit_code(self, code: str) -> dict:
        if not self.proc or self.proc.poll() is not None or not self.proc.stdin:
            return {"ok": False, "error": "Chưa bắt đầu đăng nhập hoặc tiến trình đã kết thúc."}
        self.proc.stdin.write(code.strip() + "\n")
        self.proc.stdin.flush()
        return {"ok": True}

    def logout(self) -> dict:
        a = self.ant()
        if not a:
            return {"ok": False, "error": "Chưa cài ant"}
        r = subprocess.run([a, "auth", "logout"], capture_output=True, text=True, timeout=15)
        self.url = None
        return {"ok": r.returncode == 0, "detail": (r.stdout + r.stderr).strip()[:200]}

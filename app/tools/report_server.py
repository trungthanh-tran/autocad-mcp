"""Máy chủ nhận báo lỗi từ người dùng (chạy ở phía dev).

    pip install fastapi uvicorn python-multipart
    CADTROLY_REPORT_TOKEN=bi-mat CADTROLY_REPORT_DIR=/var/cadtroly-reports python tools/report_server.py --port 8790

Nhận POST multipart {meta, file} tại /cadtroly/report, lưu vào <dir>/<YYYY-MM-DD>/RPT-<id>.zip + .json,
trả {"ok": true, "id": "RPT-..."}. Danh sách: GET /cadtroly/reports (cần token).
Đặt sau nginx (proxy_pass http://127.0.0.1:8790; client_max_body_size 50m;). Tuỳ chọn: báo Telegram khi có gói mới
(CADTROLY_TG_BOT, CADTROLY_TG_CHAT).
"""
from __future__ import annotations

import argparse
import json
import os
import secrets
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, File, Form, Header, HTTPException, UploadFile

MAX_BYTES = 50 * 1024 * 1024


def create_app(inbox: Path, token: str = "") -> FastAPI:
    app = FastAPI(title="cadtroly report inbox")
    inbox.mkdir(parents=True, exist_ok=True)

    def _auth(authorization: str | None):
        if token and authorization != f"Bearer {token}":
            raise HTTPException(401, "token sai")

    @app.post("/cadtroly/report")
    async def receive(file: UploadFile = File(...), meta: str = Form("{}"), authorization: str | None = Header(None)):
        _auth(authorization)
        data = await file.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise HTTPException(413, "gói quá lớn")
        rid = f"RPT-{datetime.now():%Y%m%d-%H%M%S}-{secrets.token_hex(2)}"
        day = inbox / f"{datetime.now():%Y-%m-%d}"
        day.mkdir(parents=True, exist_ok=True)
        (day / f"{rid}.zip").write_bytes(data)
        try:
            m = json.loads(meta)
        except Exception:
            m = {"raw": meta[:500]}
        m |= {"id": rid, "received": datetime.now().isoformat(timespec="seconds"), "size": len(data), "filename": file.filename}
        (day / f"{rid}.json").write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
        _notify(m)
        return {"ok": True, "id": rid}

    @app.get("/cadtroly/reports")
    def list_reports(authorization: str | None = Header(None), limit: int = 50):
        _auth(authorization)
        items = sorted(inbox.rglob("RPT-*.json"), reverse=True)[:limit]
        return {"reports": [json.loads(p.read_text(encoding="utf-8")) for p in items]}

    @app.get("/cadtroly/health")
    def health():
        return {"ok": True}

    return app


def _notify(m: dict) -> None:
    bot, chat = os.environ.get("CADTROLY_TG_BOT"), os.environ.get("CADTROLY_TG_CHAT")
    if not (bot and chat):
        return
    try:
        import urllib.parse
        import urllib.request
        text = f"[cadtroly] báo lỗi {m.get('id')} từ {m.get('don_vi') or '?'} v{m.get('version', '?')}: {m.get('note', '')}"
        urllib.request.urlopen(f"https://api.telegram.org/bot{bot}/sendMessage?" +
                               urllib.parse.urlencode({"chat_id": chat, "text": text}), timeout=10)
    except Exception:
        pass


if __name__ == "__main__":
    import uvicorn
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8790)
    ap.add_argument("--host", default="127.0.0.1")
    a = ap.parse_args()
    uvicorn.run(create_app(Path(os.environ.get("CADTROLY_REPORT_DIR", "cadtroly-reports")),
                           os.environ.get("CADTROLY_REPORT_TOKEN", "")), host=a.host, port=a.port)

"""Web UI cho người dùng cuối: FastAPI + palette HTML (static/index.html).

Chạy: cadtroly ui   → mở cửa sổ (pywebview nếu có) hoặc trình duyệt tại http://127.0.0.1:8765
API nhận đường dẫn file trên máy (cửa sổ pywebview có hộp thoại chọn file); trình duyệt thường thì
upload file vào kho/in/.
"""
import os
import shutil
import sys
import threading
import webbrowser
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel

from ..config import Config
from ..service import Service
from .chat import Chat
from .login import Login
from .. import errlog

STATIC = Path(__file__).parent / "static"


def create_app(cfg: Config | None = None) -> FastAPI:
    svc = Service(cfg)
    errlog.setup_logging(svc.cfg.kho)
    log = errlog.LOG
    chat = Chat(svc)
    login = Login()
    app = FastAPI(title="cadtroly")

    class PathBody(BaseModel):
        path: str

    @app.exception_handler(HTTPException)
    async def _http_exc(request: Request, exc: HTTPException):
        code = "E-RULE-01" if exc.status_code == 404 else ("E-FILE-01" if exc.status_code == 400 else "E-APP-99")
        (log.error if exc.status_code >= 500 else log.warning)("%s HTTP %s %s: %s", code, exc.status_code, request.url.path, exc.detail)
        return JSONResponse(status_code=exc.status_code, content={"detail": str(exc.detail), **errlog.friendly(code, str(exc.detail))})

    @app.exception_handler(Exception)
    async def _any_exc(request: Request, exc: Exception):
        code = errlog.classify(exc)
        log.exception("%s tại %s: %s", code, request.url.path, exc)
        return JSONResponse(status_code=500, content={"detail": str(exc), **errlog.friendly(code, str(exc))})

    @app.get("/api/errors")
    def errors():
        return {"errors": errlog.recent_errors(svc.cfg.kho), "log": str(errlog.today_log(svc.cfg.kho)),
                "report_url": svc.cfg.report.url, "don_vi": svc.cfg.report.don_vi}

    class Note(BaseModel):
        note: str = ""
        don_vi: str | None = None

    @app.post("/api/report")
    def report(n: Note):
        """Gom log → zip → gửi thẳng lên máy chủ dev. Gửi không được thì trả đường dẫn file để gửi tay."""
        if n.don_vi is not None:
            svc.cfg.report.don_vi = n.don_vi
            svc.cfg.save()
        z = errlog.make_report(svc.cfg.kho, svc.cfg.path, n.note)
        meta = {"don_vi": svc.cfg.report.don_vi, "note": n.note, "version": svc.cfg.version}
        sent = errlog.send_report(svc.cfg.report.url, z, token=svc.cfg.report.token, meta=meta) if svc.cfg.report.url else {"ok": False, "error": "chưa cấu hình report.url"}
        return {"ok": True, "sent": sent.get("ok", False), "id": sent.get("id"), "error": sent.get("error"),
                "file": str(z), "folder": str(z.parent)}

    @app.post("/api/open_folder")
    def open_folder(p: PathBody):
        import subprocess
        d = Path(p.path)
        d = d if d.is_dir() else d.parent
        try:
            if sys.platform == "win32":
                os.startfile(str(d))  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(d)])
            else:
                subprocess.Popen(["xdg-open", str(d)])
            return {"ok": True}
        except Exception as exc:
            log.warning("open_folder: %s", exc)
            return {"ok": False}
    app.state.svc = svc
    app.state.picked = None   # đường dẫn từ hộp thoại pywebview

    @app.get("/", response_class=HTMLResponse)
    def index():
        return (STATIC / "index.html").read_text(encoding="utf-8")

    @app.get("/api/status")
    def status():
        return svc.status() | {"recent": svc.recent(), "skills": svc.kho.skills(), "rulesets": svc.rulesets(),
                               "rules": svc.kho.rules.export()[-20:], "picked": app.state.picked}

    class P(BaseModel):
        path: str

    @app.post("/api/open")
    def open_(p: P):
        try:
            return svc.read(p.path, reload=True)
        except Exception as exc:
            log.warning("E-FILE-01 open %s: %s", p.path, exc)
            raise HTTPException(400, f"Không đọc được bản vẽ: {exc}")

    @app.post("/api/upload")
    async def upload(file: UploadFile = File(...)):
        d = svc.cfg.kho / "in"
        d.mkdir(parents=True, exist_ok=True)
        dst = d / Path(file.filename).name
        with dst.open("wb") as fh:
            shutil.copyfileobj(file.file, fh)
        return {"path": str(dst)} | svc.read(str(dst), reload=True)

    @app.post("/api/propose")
    def propose(p: P):
        return svc.propose(p.path)

    class D(BaseModel):
        path: str
        kind: str
        name: str
        cong_tac: str
        don_vi: str
        cach_tinh: str
        tham_so: dict | None = None
        save_rule: bool = True

    @app.post("/api/decide")
    def decide(d: D):
        try:
            return svc.decide(d.path, d.kind, d.name, d.cong_tac, d.don_vi, d.cach_tinh, d.tham_so, d.save_rule)
        except KeyError as exc:
            raise HTTPException(404, str(exc))

    @app.post("/api/accept_b")
    def accept_b(p: P):
        return svc.accept_all_b(p.path)

    class C(BaseModel):
        path: str
        height_m: float | None = None
        tru_lo_cua: float = 0.0

    @app.post("/api/compute")
    def compute(c: C):
        return svc.compute(c.path, c.height_m, c.tru_lo_cua)

    @app.post("/api/export")
    def export(c: C):
        return svc.export(c.path, height_m=c.height_m)

    class F(BaseModel):
        path: str
        height_m: float | None = None

    @app.post("/api/run_folder")
    def run_folder(f: F):
        return svc.run_folder(f.path, f.height_m)

    @app.get("/api/download")
    def download(path: str):
        p = Path(path)
        if not p.exists() or p.suffix.lower() != ".xlsx":
            raise HTTPException(404, "Không có file")
        return FileResponse(p, filename=p.name)

    class K(BaseModel):
        path: str
        ruleset: str
        include_unapproved: bool = False

    @app.post("/api/check")
    def check(k: K):
        try:
            return svc.check(k.path, k.ruleset, k.include_unapproved)
        except KeyError as exc:
            raise HTTPException(404, str(exc))

    class S(BaseModel):
        name: str
        enabled: bool

    @app.post("/api/skill")
    def skill(s: S):
        svc.kho.set_skill(s.name, s.enabled)
        return {"skills": svc.kho.skills()}

    class Cfg(BaseModel):
        provider: str | None = None
        api_key: str | None = None
        model_main: str | None = None

    @app.post("/api/config")
    def config(c: Cfg):
        if c.provider:
            svc.cfg.llm.provider = c.provider
        if c.model_main:
            svc.cfg.llm.model_main = c.model_main
        if c.api_key:
            # Lưu vào Windows Credential Manager nếu có keyring, không thì biến môi trường phiên này
            env = {"claude": "ANTHROPIC_API_KEY", "gemini": "GEMINI_API_KEY", "openai": "OPENAI_API_KEY"}.get(svc.cfg.llm.provider, "ANTHROPIC_API_KEY")
            os.environ[env] = c.api_key
            try:
                import keyring
                keyring.set_password("cadtroly", env, c.api_key)
            except Exception:
                pass
        svc.cfg.save()
        return {"ok": True, "llm": svc.cfg.llm.provider, "model": svc.cfg.llm.model_main}

    # ---- đăng nhập Claude kiểu bấm nút → trình duyệt → callback (Anthropic CLI) ----
    @app.get("/api/login/status")
    def login_status():
        return login.status()

    class L(BaseModel):
        no_browser: bool = False
        profile: str | None = None

    @app.post("/api/login/start")
    def login_start(l: L):
        r = login.start(l.no_browser, l.profile)
        if r.get("ok"):
            # khi dùng profile OAuth thì không để API key cũ đè lên (bẫy số 1 của SDK)
            os.environ.pop("ANTHROPIC_API_KEY", None)
            svc.cfg.llm.provider = "claude"
            svc.cfg.save()
        return r

    class Code(BaseModel):
        code: str

    @app.post("/api/login/code")
    def login_code(c: Code):
        return login.submit_code(c.code)

    @app.post("/api/login/logout")
    def login_logout():
        return login.logout()

    @app.get("/api/test_llm")
    def test_llm():
        from ..llm.client import LLM, LLMError
        try:
            out = LLM(svc.cfg.llm).ask("fast", "Trả lời đúng một từ.", "Nói 'ok'.", effort="low")
            return {"ok": True, "reply": out[:50]}
        except LLMError as exc:
            return {"ok": False, "error": str(exc)}
        except Exception as exc:
            return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}

    class M(BaseModel):
        text: str
        path: str | None = None

    @app.post("/api/chat")
    def chat_(m: M):
        return chat.send(m.text, m.path)

    @app.post("/api/chat/reset")
    def chat_reset():
        chat.reset()
        return {"ok": True}

    @app.get("/api/pick")
    def pick():
        """Hộp thoại chọn file: chỉ có khi chạy trong cửa sổ pywebview."""
        w = getattr(app.state, "window", None)
        if w is None:
            return {"path": None, "note": "Không có hộp thoại trong trình duyệt; dùng kéo thả/upload."}
        import webview
        r = w.create_file_dialog(webview.OPEN_DIALOG, file_types=("Bản vẽ (*.dxf;*.dwg)", "Tất cả (*.*)"))
        return {"path": r[0] if r else None}

    return app


def serve(host: str = "127.0.0.1", port: int = 8765, window: bool = True) -> None:
    import uvicorn
    app = create_app()
    try:
        import keyring
        for env in ("ANTHROPIC_API_KEY", "GEMINI_API_KEY", "OPENAI_API_KEY"):
            if not os.environ.get(env):
                v = keyring.get_password("cadtroly", env)
                if v and v.strip():
                    os.environ[env] = v.strip()
    except Exception:
        pass
    server = uvicorn.Server(uvicorn.Config(app, host=host, port=port, log_level="warning"))
    t = threading.Thread(target=server.run, daemon=True)
    t.start()
    url = f"http://{host}:{port}"
    if window:
        try:
            import webview
            w = webview.create_window("AI Trợ lý AutoCAD", url, width=1180, height=800, min_size=(900, 600))
            app.state.window = w
            webview.start()
            server.should_exit = True
            return
        except Exception as exc:  # thiếu pywebview / WebView2 / GTK: rơi về trình duyệt
            try:
                log_dir = Path(os.environ.get("CADTROLY_KHO", str(Path.home() / "CAD-kho"))) / "log"
                log_dir.mkdir(parents=True, exist_ok=True)
                (log_dir / "ui.log").write_text(f"webview fail: {exc}\n", encoding="utf-8")
            except Exception:
                pass
    webbrowser.open(url)
    t.join()

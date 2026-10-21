from pathlib import Path

from fastapi.testclient import TestClient


def test_web_flow(sample_dxf, kho_dir):
    from cadtroly.config import Config
    from cadtroly.web.app import create_app
    app = create_app(Config(kho=kho_dir))
    c = TestClient(app)
    assert c.get("/").status_code == 200 and "Bóc khối lượng" in c.get("/").text
    s = c.get("/api/status").json()
    assert s["kho"] == str(kho_dir) and any(r["id"] == "chuan-cong-ty" for r in s["rulesets"])
    P = str(sample_dxf)
    r = c.post("/api/open", json={"path": P}).json()
    assert r["entities"] == 49
    assert c.post("/api/open", json={"path": "khong-co.dxf"}).status_code == 400
    r = c.post("/api/propose", json={"path": P}).json()
    assert r["stats"]["A"] == 0 and len(r["groups"]) >= 6
    r = c.post("/api/decide", json={"path": P, "kind": "layer", "name": "TUONG220", "cong_tac": "Xây tường 220",
                                    "don_vi": "m3", "cach_tinh": "volume_by_height", "tham_so": {"day": 0.22}}).json()
    assert r["ok"] and r["group"]["tin_cay"] == "A"
    r = c.post("/api/accept_b", json={"path": P}).json()
    assert r["accepted"] >= 4 and r["stats"]["B"] == 0
    r = c.post("/api/compute", json={"path": P, "height_m": 3.6}).json()
    row = next(x for x in r["rows"] if x["cong_tac"] == "Xây tường 220")
    assert abs(row["khoi_luong"] - 40 * 3.6 * 0.22) < 0.01 and row["tin_cay"] == "A"
    r = c.post("/api/export", json={"path": P}).json()
    assert Path(r["excel"]).exists()
    d = c.get("/api/download", params={"path": r["excel"]})
    assert d.status_code == 200 and len(d.content) > 1000
    r = c.post("/api/check", json={"path": P, "ruleset": "chuan-cong-ty"}).json()
    assert r["summary"]["loi"] == 2
    assert c.post("/api/check", json={"path": P, "ruleset": "khong-co"}).status_code == 404
    # upload qua trình duyệt
    with open(sample_dxf, "rb") as fh:
        r = c.post("/api/upload", files={"file": ("tang-5.dxf", fh, "application/dxf")}).json()
    assert r["path"].endswith("tang-5.dxf") and r["entities"] == 49
    r = c.post("/api/run_folder", json={"path": str(kho_dir / "in")}).json()
    assert r["count"] == 1 and "excel" in r["results"][0]
    # cấu hình + chat khi tắt AI
    r = c.post("/api/config", json={"provider": "none"}).json()
    assert r["llm"] == "none"
    r = c.post("/api/chat", json={"text": "bóc khối lượng", "path": P}).json()
    assert "Claude" in r["reply"]
    assert c.get("/api/pick").json()["path"] is None
    s = c.get("/api/status").json()
    assert s["quy_tac"] >= 5 and len(s["recent"]) >= 1


def test_login_without_cli(kho_dir, monkeypatch):
    from cadtroly.config import Config
    from cadtroly.web.app import create_app
    from cadtroly.web import login as lg
    monkeypatch.setattr(lg.Login, "ant", staticmethod(lambda: None))
    c = TestClient(create_app(Config(kho=kho_dir)))
    s = c.get("/api/login/status").json()
    assert s["installed"] is False and "ant" in s["hint"]
    r = c.post("/api/login/start", json={"no_browser": True}).json()
    assert r["installed"] is False
    assert c.post("/api/login/code", json={"code": "x"}).json()["ok"] is False


def test_login_with_fake_cli(kho_dir, monkeypatch, tmp_path):
    """Giả lập `ant`: tiến trình login thật (in link, chờ mã trên stdin); `auth status` giả bằng hàm."""
    import os, subprocess, sys, time
    from cadtroly.config import Config
    from cadtroly.web.app import create_app
    from cadtroly.web import login as lg
    fake = tmp_path / "ant_login.py"
    flag = tmp_path / "ok.flag"
    fake.write_text("\n".join([
        "import sys, pathlib",
        f"flag = pathlib.Path({str(flag)!r})",
        "print('Open this URL: https://console.anthropic.com/oauth/authorize?x=1', flush=True)",
        "code = sys.stdin.readline().strip()",
        "if code == 'ABC': flag.write_text('1'); print('Logged in', flush=True)",
    ]) + "\n", encoding="utf-8")
    monkeypatch.setattr(lg.Login, "ant", staticmethod(lambda: sys.executable))
    orig = lg.subprocess.Popen
    monkeypatch.setattr(lg.subprocess, "Popen", lambda cmd, **kw: orig([cmd[0], str(fake)], **kw))

    def fake_run(cmd, **kw):
        out = "active profile: default (org acme)" if flag.exists() else "not logged in"
        return subprocess.CompletedProcess(cmd, 0, out, "")
    monkeypatch.setattr(lg.subprocess, "run", fake_run)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "stale-key")
    c = TestClient(create_app(Config(kho=kho_dir)))
    assert c.get("/api/login/status").json()["logged_in"] is False
    r = c.post("/api/login/start", json={"no_browser": True}).json()
    assert r["ok"] and r["mode"] == "no-browser"
    assert "ANTHROPIC_API_KEY" not in os.environ          # key cũ không được đè profile OAuth
    for _ in range(50):
        s = c.get("/api/login/status").json()
        if s["url"]:
            break
        time.sleep(0.1)
    assert s["url"].startswith("https://console.anthropic.com/oauth")
    assert c.post("/api/login/code", json={"code": "ABC"}).json()["ok"]
    for _ in range(50):
        s = c.get("/api/login/status").json()
        if s["logged_in"]:
            break
        time.sleep(0.1)
    assert s["logged_in"] is True, s


def test_errors_and_report(sample_dxf, kho_dir, monkeypatch):
    import zipfile
    from cadtroly import errlog
    from cadtroly.config import Config
    from cadtroly.web.app import create_app
    cfg = Config(kho=kho_dir)
    cfg.report.url = "http://127.0.0.1:9/khong-co"      # cổng 9: chắc chắn không nối được
    c = TestClient(create_app(cfg), raise_server_exceptions=False)
    r = c.post("/api/open", json={"path": "khong-co.dxf"})
    assert r.status_code == 400 and r.json()["code"] == "E-FILE-01" and "Không đọc được" in r.json()["message"]
    r = c.post("/api/check", json={"path": str(sample_dxf), "ruleset": "x"})
    assert r.status_code == 404 and r.json()["code"] == "E-RULE-01" and r.json()["hint"]
    errs = c.get("/api/errors").json()
    assert __import__("re").search(r"app-\d{4}-\d{2}-\d{2}\.log$", errs["log"]) and any(e["muc"] == "cảnh báo" for e in errs["errors"])
    # gửi thất bại → vẫn có file cục bộ
    r = c.post("/api/report", json={"note": "test", "don_vi": "Cty A"}).json()
    assert r["ok"] and r["sent"] is False and Path(r["file"]).exists()
    names = zipfile.ZipFile(r["file"]).namelist()
    assert "thong-tin.json" in names and any(n.startswith("log/") for n in names) and "config.json" in names
    # gửi thành công (giả lập máy chủ)
    monkeypatch.setattr(errlog, "send_report", lambda url, z, **kw: {"ok": True, "id": "RPT-1", "meta": kw.get("meta")})
    r = c.post("/api/report", json={"note": "lan 2"}).json()
    assert r["sent"] is True and r["id"] == "RPT-1"
    assert c.get("/api/errors").json()["don_vi"] == "Cty A"


def test_report_server_roundtrip(tmp_path):
    """Máy chủ nhận báo lỗi (tools/report_server.py) nhận được gói do errlog.send_report gửi."""
    import threading, zipfile, uvicorn, time, socket
    from cadtroly import errlog
    sys_path = str(Path(__file__).parent.parent / "tools")
    import sys
    sys.path.insert(0, sys_path)
    import report_server
    inbox = tmp_path / "inbox"
    app = report_server.create_app(inbox, token="abc")
    sock = socket.socket(); sock.bind(("127.0.0.1", 0)); port = sock.getsockname()[1]; sock.close()
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error"))
    th = threading.Thread(target=server.run, daemon=True); th.start()
    for _ in range(50):
        if server.started:
            break
        time.sleep(0.1)
    z = tmp_path / "bao-loi.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("thong-tin.json", "{}")
    bad = errlog.send_report(f"http://127.0.0.1:{port}/cadtroly/report", z, token="sai", meta={"don_vi": "X"})
    assert bad["ok"] is False
    ok = errlog.send_report(f"http://127.0.0.1:{port}/cadtroly/report", z, token="abc", meta={"don_vi": "X", "note": "n"})
    assert ok["ok"] and ok["id"].startswith("RPT-")
    saved = list(inbox.glob("*/*.zip")) + list(inbox.glob("*.zip"))
    assert saved and any(p.suffix == ".json" for p in inbox.rglob("*"))
    server.should_exit = True


def test_daily_log_rotation(tmp_path, monkeypatch):
    import logging
    from datetime import datetime, timedelta
    from cadtroly import errlog
    kho = tmp_path / "kho"; (kho / "log").mkdir(parents=True)
    old = kho / "log" / f"app-{(datetime.now() - timedelta(days=40)):%Y-%m-%d}.log"; old.write_text("cu", encoding="utf-8")
    keep = kho / "log" / f"app-{(datetime.now() - timedelta(days=3)):%Y-%m-%d}.log"; keep.write_text("giu", encoding="utf-8")
    p = errlog.setup_logging(kho)
    assert p.name == f"app-{datetime.now():%Y-%m-%d}.log" and p.exists()
    assert not old.exists() and keep.exists()          # xoá >30 ngày, giữ 3 ngày
    errlog.LOG.warning("E-AI-04 thử")
    assert "E-AI-04" in p.read_text(encoding="utf-8")
    # giả lập sang ngày mới: handler mở file mới
    h = next(x for x in logging.getLogger().handlers if getattr(x, "_cadtroly", False))
    h._day = "2000-01-01"
    errlog.LOG.warning("sau nửa đêm")
    assert "sau nửa đêm" in p.read_text(encoding="utf-8") and "sau nửa đêm" not in old.name
    errs = errlog.recent_errors(kho)
    assert errs[0]["message"].startswith("sau nửa đêm") and errs[1]["code"] == "E-AI-04"

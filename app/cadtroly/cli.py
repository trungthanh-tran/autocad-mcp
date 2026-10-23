"""CLI: cadtroly <lệnh>

  cadtroly init [--kho D:\\CAD-kho]         tạo kho + config
  cadtroly read  <dxf>                      tóm tắt bản vẽ
  cadtroly takeoff <dxf|thư mục> [--h 3.3] [--out x.xlsx]   bóc khối lượng ra Excel
  cadtroly check <dxf> <ruleset>            kiểm tra theo bộ quy tắc
  cadtroly sample [<out.dxf>]               sinh bản vẽ mẫu
  cadtroly mcp                              chạy MCP server (stdio)
  cadtroly update                           cập nhật code và package từ GitHub
  cadtroly connect [--client X] [--prompt]  in lệnh/cấu hình nối MCP cho client, hoặc prompt dán cho LLM
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from .config import Config
from .connect import CLIENTS, connect_text
from .kho.store import Kho


def _utf8():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def main(argv=None) -> int:
    _utf8()
    ap = argparse.ArgumentParser(prog="cadtroly")
    ap.add_argument("--kho", help="thư mục kho (mặc định CADTROLY_KHO hoặc ~/CAD-kho)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    p = sub.add_parser("read"); p.add_argument("path")
    p = sub.add_parser("takeoff"); p.add_argument("path"); p.add_argument("--h", type=float, dest="h"); p.add_argument("--out")
    p = sub.add_parser("check"); p.add_argument("path"); p.add_argument("ruleset")
    p = sub.add_parser("sample"); p.add_argument("out", nargs="?", default="samples/mat-bang-tang-3.dxf")
    sub.add_parser("mcp")
    sub.add_parser("update")
    p = sub.add_parser("connect")
    p.add_argument("--client", default="all", choices=CLIENTS)
    p.add_argument("--prompt", action="store_true", help="in một prompt hoàn chỉnh để dán cho LLM/agent nhờ tự cấu hình")
    a = ap.parse_args(argv)

    cfg = Config.load(Path(a.kho) if a.kho else None)
    if a.cmd == "init":
        cfg.save()
        print(f"Kho dữ liệu người dùng: {cfg.kho}\nConfig: {cfg.path}\nBộ tiêu chuẩn/quy tắc/skill mặc định nằm trong MCP.")
        return 0
    if a.cmd == "sample":
        from .samples import make_sample
        print(make_sample(a.out))
        return 0
    if a.cmd == "connect":
        print(connect_text(cfg, a.client, a.prompt))
        return 0
    if a.cmd == "mcp":
        from .mcp.bootstrap import ensure_runtime_dependencies
        ensure_runtime_dependencies()
        from .mcp.server import main as mcp_main
        mcp_main()
        return 0
    if a.cmd == "update":
        root = Path(__file__).resolve().parents[1]
        status = subprocess.run(
            ["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True, check=True
        ).stdout.strip()
        if status:
            print("Không thể update: thư mục code đang có thay đổi local chưa commit.", file=sys.stderr)
            print(status, file=sys.stderr)
            return 2
        subprocess.run(["git", "pull", "--ff-only", "origin", "main"], cwd=root, check=True)
        lock = root / "requirements-mcp.lock"
        command = [sys.executable, "-m", "pip", "install"]
        if lock.is_file():
            command += ["-r", str(lock)]
        command += ["-e", str(root)]
        subprocess.run(command, check=True)
        from version import __version__
        print(f"Đã update cadtroly {__version__}")
        return 0

    from .reader import read_dxf
    kho = Kho(cfg)
    if a.cmd == "read":
        d = read_dxf(a.path)
        print(json.dumps(d.summary(), ensure_ascii=False, indent=2))
        return 0
    if a.cmd == "takeoff":
        from .takeoff.calc import compute, stats
        from .takeoff.excel import export_excel
        from .takeoff.mapper import propose_mapping
        p = Path(a.path)
        files = sorted(p.glob("*.dxf")) if p.is_dir() else [p]
        for f in files:
            d = read_dxf(f)
            groups = propose_mapping(d, kho.rules)
            rows = compute(d, groups, height_m=a.h)
            out = Path(a.out) if (a.out and not p.is_dir()) else cfg.kho / "out" / (f.stem + ".xlsx")
            export_excel(d, groups, rows, out, meta={"stats": stats(groups)})
            s = stats(groups)
            print(f"{f.name}: A {s['A']}% B {s['B']}% C {s['C']}% → {out}")
            for r in rows:
                print(f"  [{r.tin_cay}] {r.cong_tac}: {r.khoi_luong} {r.don_vi}  ({r.nguon})")
        return 0
    if a.cmd == "check":
        from .check.engine import check_drawing, load_ruleset, summarize
        rp = Path(a.ruleset)
        if not rp.exists():
            for c in (cfg.kho / "tieu-chuan" / f"{a.ruleset}.rules.json", cfg.kho / "quy-tac" / f"{a.ruleset}.rules.json"):
                if c.exists():
                    rp = c
        rs = load_ruleset(rp)
        fs = check_drawing(read_dxf(a.path), rs)
        print(json.dumps(summarize(fs), ensure_ascii=False))
        for f in fs:
            print(f"  [{f.muc}] {f.rule_id} {f.mo_ta} — {f.dieu}" + (" (tự sửa được)" if f.tu_sua_duoc else ""))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())

# PyInstaller spec: python -m PyInstaller build/cadtroly.spec --noconfirm
# Ra dist/AI-Tro-ly-AutoCAD/ (onedir: khởi động nhanh, dễ kèm bin/ant.exe và kho-mac-dinh/)
import sys
from pathlib import Path

ROOT = Path(SPECPATH).parent
block_cipher = None

datas = [
    (str(ROOT / "cadtroly" / "web" / "static"), "cadtroly/web/static"),
    (str(ROOT / "samples" / "kho"), "kho-mac-dinh"),
]

hidden = [
    "uvicorn.logging", "uvicorn.loops.auto", "uvicorn.protocols.http.auto", "uvicorn.protocols.websockets.auto",
    "uvicorn.lifespan.on", "anyio._backends._asyncio", "multipart", "python_multipart",
    "openpyxl", "ezdxf", "anthropic", "httpx", "keyring.backends.Windows", "keyring.backends.SecretService",
    "webview.platforms.edgechromium", "webview.platforms.winforms", "webview.platforms.gtk", "webview.platforms.qt",
    "cadtroly.web.app", "cadtroly.web.chat", "cadtroly.web.login", "cadtroly.service", "cadtroly.llm.client",
]

a = Analysis(
    [str(ROOT / "cadtroly" / "launcher.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hidden,
    hookspath=[],
    runtime_hooks=[],
    # UI không cần MCP/FastMCP, engineering upstream, matplotlib: loại để exe gọn
    excludes=["fastmcp", "server", "backends", "engineering", "discovery", "matplotlib", "PIL.ImageQt",
              "tkinter", "pytest", "IPython", "notebook"],
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name="AI-Tro-ly-AutoCAD",
    debug=False,
    console=False,            # không hiện cửa sổ đen; lỗi ghi vào kho/log
    icon=None,
)
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=False, name="AI-Tro-ly-AutoCAD")

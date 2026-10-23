"""cadtroly connect: in lệnh/cấu hình nối MCP vào client với đường dẫn thật của máy này.

Khỏi phải sửa tay đường dẫn python, thư mục code, kho, và gấp đôi dấu \\ trong JSON.
--prompt in một đoạn để dán cho LLM/agent nhờ nó tự cấu hình.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from .config import Config

CLIENTS = ("all", "vscode", "claude-code", "claude-desktop", "gemini", "json")
NL = chr(10)


def server_spec(cfg: Config) -> tuple[str, str, dict]:
    """(python, cwd, env) dùng chung cho mọi client."""
    py = sys.executable
    cwd = str(Path(__file__).resolve().parents[1])          # thư mục chứa pyproject.toml
    env = {"CADTROLY_KHO": str(cfg.kho), "DWG_MCP_ALLOWED_ROOTS": str(cfg.kho), "AUTOCAD_MCP_BACKEND": "auto",
           "TOOL_PROFILE": "full", "TOOL_PACKS": "all", "PYTHONIOENCODING": "utf-8"}
    return py, cwd, env


def connect_text(cfg: Config, client: str = "all", as_prompt: bool = False) -> str:
    py, cwd, env = server_spec(cfg)
    entry = {"command": py, "args": ["-m", "cadtroly.mcp"], "cwd": cwd, "env": env}
    generic = json.dumps({"mcpServers": {"cadtroly": entry}}, ensure_ascii=False, indent=2)
    vscode = json.dumps({"servers": {"cadtroly": {"type": "stdio", **entry}}}, ensure_ascii=False, indent=2)
    e = " ".join(f'-e {k}="{v}"' for k, v in env.items())
    blocks = {
        "vscode": ("VS Code: Ctrl+Shift+P → MCP: Open User Configuration, dán vào, lưu → MCP: List Servers → Start",
                   vscode),
        "claude-code": ("Claude Code (chạy trong terminal, tại thư mục code)",
                        f'claude mcp add cadtroly {e} -- "{py}" -m cadtroly.mcp'),
        "gemini": ("Gemini CLI (chạy trong terminal, tại thư mục code; lỗi cú pháp thì dùng khối JSON)",
                   f'gemini mcp add {e} cadtroly "{py}" -m cadtroly.mcp'),
        "claude-desktop": ("Claude Desktop: dán vào %APPDATA%/Claude/claude_desktop_config.json rồi khởi động lại",
                           generic),
        "json": ("JSON mcpServers (Gemini: ~/.gemini/settings.json, Cursor: ~/.cursor/mcp.json, client khác)",
                 generic),
    }
    keys = [k for k in blocks] if client == "all" else [client]
    text = (NL * 2).join(f"# {blocks[k][0]}{NL}{blocks[k][1]}" for k in keys)
    if not as_prompt:
        return text
    return ("Tôi muốn nối MCP server 'cadtroly' (điều khiển AutoCAD) vào công cụ AI tôi đang dùng. Server chạy qua "
            f'stdio bằng lệnh "{py}" -m cadtroly.mcp, thư mục làm việc {cwd}. Hãy đăng ký server này vào công cụ '
            "của bạn (tự sửa file cấu hình nếu bạn có quyền, không thì chỉ tôi từng bước), dùng đúng các giá trị "
            "dưới đây, rồi kiểm tra bằng cách gọi tool knowledge_status." + NL * 2 +
            "Biến môi trường: " + json.dumps(env, ensure_ascii=False) + NL * 2 +
            "Cấu hình tham khảo:" + NL + text)

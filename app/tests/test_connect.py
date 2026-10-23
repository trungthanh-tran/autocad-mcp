"""cadtroly connect: cấu hình in ra phải là JSON hợp lệ, đúng đường dẫn máy này."""
import json
import sys
from pathlib import Path

from cadtroly.cli import main
from cadtroly.config import Config
from cadtroly.connect import connect_text


def _json(block: str) -> dict:
    return json.loads(block.split("\n", 1)[1])


def test_blocks(tmp_path):
    cfg = Config(kho=tmp_path / "kho")
    vs = _json(connect_text(cfg, "vscode"))["servers"]["cadtroly"]
    assert vs["type"] == "stdio" and vs["command"] == sys.executable and vs["args"] == ["-m", "cadtroly.mcp"]
    assert vs["env"]["CADTROLY_KHO"] == str(tmp_path / "kho")
    js = _json(connect_text(cfg, "json"))["mcpServers"]["cadtroly"]
    assert (Path(js["cwd"]) / "pyproject.toml").is_file()
    assert "claude mcp add cadtroly" in connect_text(cfg, "claude-code")
    p = connect_text(cfg, "all", as_prompt=True)
    assert "knowledge_status" in p and "# VS Code" in p and "# Gemini CLI" in p


def test_cli(tmp_path, capsys):
    assert main(["--kho", str(tmp_path), "connect", "--client", "claude-desktop"]) == 0
    assert '"mcpServers"' in capsys.readouterr().out

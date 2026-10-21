"""MCP của cadtroly. Import lười: `from cadtroly.mcp.server import mcp` khi cần, để UI/exe không kéo FastMCP."""


def build_server():
    from .server import build_server as _b
    return _b()

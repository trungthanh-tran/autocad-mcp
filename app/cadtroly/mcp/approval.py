"""Duyệt thao tác phá huỷ trước khi chạy: xoá, ghi đè file, lệnh/LISP thô, purge, đóng bản vẽ…

Hai cách, chọn bằng CADTROLY_APPROVAL:
  auto  (mặc định) client hỗ trợ elicitation → server hỏi thẳng người dùng (hộp Đồng ý/Huỷ của client);
        client không hỗ trợ → cách token.
  token tool bị chặn, trả về preview + token dùng một lần (hết hạn sau 5 phút, gắn với đúng tool và
        tham số đã xem). LLM phải cho người dùng xem preview, người dùng đồng ý mới gọi
        approval_execute(token). Tham số chạy là bản server đã lưu, LLM không đổi được.
  off   tắt (chỉ dùng khi chạy script tự động có kiểm soát).

Bước duyệt là cơ chế trong server, không phải lời dặn trong prompt: tool bị chặn không chạy
cho tới khi có Đồng ý hoặc token hợp lệ. Mọi yêu cầu/đồng ý/từ chối ghi vào kho/log.
"""
from __future__ import annotations

import json
import os
import secrets
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import mcp.types as mt
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.tools.tool import ToolResult

TTL_S = 300
EXECUTE_TOOL = "approval_execute"


def _exists(p: Any) -> bool:
    try:
        return bool(p) and Path(str(p)).exists()
    except OSError:
        return False


def _always(reason: str) -> Callable[[dict], str | None]:
    return lambda a: reason


# tool -> hàm(args) trả lý do cần duyệt, hoặc None nếu lần gọi này an toàn
RULES: dict[str, Callable[[dict], str | None]] = {
    "entity_delete": _always("xoá đối tượng"),
    "entity_delete_many": lambda a: f"xoá {len(a.get('handles') or [])} đối tượng",
    "layer_delete": _always("xoá layer"),
    "block_explode": _always("phá block"),
    "construction_clear": _always("xoá đường dựng hình"),
    "layout_delete": _always("xoá layout"),
    "viewport_delete": _always("xoá viewport"),
    "layer_state_delete": _always("xoá layer state"),
    "drawing_purge": _always("purge đối tượng không dùng"),
    "system_run_command": _always("chạy lệnh AutoCAD thô"),
    "system_run_lisp": _always("chạy biểu thức LISP"),
    "drawing_close": lambda a: "đóng và ghi đè bản vẽ" if a.get("save", True) else "đóng, bỏ thay đổi chưa lưu",
    "document_close": lambda a: ("đóng, bỏ thay đổi chưa lưu" if a.get("discard")
                                 else "đóng và ghi đè bản vẽ" if a.get("save") else None),
    "xref_manage": lambda a: None if (a.get("action") or "list") == "list" else f"xref {a.get('action')}",
    "text_find_replace": lambda a: None if a.get("dry_run") else "thay text hàng loạt",
    "drawing_refine": lambda a: None if a.get("dry_run") else "tự sửa bản vẽ",
    "drawing_save": lambda a: ("ghi đè file đang mở" if not a.get("path")
                               else f"ghi đè {a['path']}" if _exists(a["path"]) else None),
    "drawing_save_as": lambda a: f"ghi đè {a.get('path')}" if _exists(a.get("path")) else None,
    "drawing_export_dwg": lambda a: f"ghi đè {a.get('path')}" if _exists(a.get("path")) else None,
    "drawing_export_dxf": lambda a: f"ghi đè {a.get('path')}" if _exists(a.get("path")) else None,
    "drawing_finalize": lambda a: f"ghi đè {a.get('save_path')}" if _exists(a.get("save_path")) else None,
}


def needs_approval(tool: str, args: dict) -> str | None:
    """Lý do cần duyệt, hoặc None. cad_batch cần duyệt khi có bước cần duyệt."""
    if tool == "cad_batch":
        if args.get("dry_run"):
            return None
        reasons = []
        for i, step in enumerate(args.get("steps") or []):
            if isinstance(step, dict):
                r = needs_approval(str(step.get("tool", "")), step.get("args") or {})
                if r:
                    reasons.append(f"bước {i}: {step.get('tool')} ({r})")
        return "; ".join(reasons) or None
    rule = RULES.get(tool)
    return rule(args) if rule else None


def mode() -> str:
    m = os.environ.get("CADTROLY_APPROVAL", "auto").strip().lower()
    return m if m in {"auto", "token", "off"} else "auto"


@dataclass
class Pending:
    tool: str
    arguments: dict
    reason: str
    expires: float
    created: float = field(default_factory=time.time)


def _summary(tool: str, args: dict, reason: str) -> str:
    shown = json.dumps(args, ensure_ascii=False, default=str)
    if len(shown) > 600:
        shown = shown[:600] + "…"
    return f"Cần đồng ý: {reason}.\nTool: {tool}\nTham số: {shown}"


def _client_elicits(ctx) -> bool:
    try:
        return ctx.session.client_params.capabilities.elicitation is not None
    except Exception:
        return False


def _log(ctx, action: str, **kw) -> None:
    try:
        ctx.lifespan_context["kho"].log("approval", action, **kw)
    except Exception:
        pass


def _error(text: str, payload: dict) -> ToolResult:
    return ToolResult(content=text, structured_content={"ok": False, **payload}, is_error=True)


class ApprovalMiddleware(Middleware):
    """Chặn tool phá huỷ cho tới khi người dùng đồng ý (elicitation) hoặc có token hợp lệ."""

    def __init__(self, ttl_s: int = TTL_S):
        self.ttl_s = ttl_s
        self.pending: dict[str, Pending] = {}

    def _gc(self) -> None:
        now = time.time()
        for k in [k for k, p in self.pending.items() if p.expires < now]:
            del self.pending[k]

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        name = context.message.name
        args = dict(context.message.arguments or {})
        ctx = context.fastmcp_context
        if name == EXECUTE_TOOL:
            return await self._execute(context, call_next, str(args.get("token", "")))
        if mode() == "off":
            return await call_next(context)
        reason = needs_approval(name, args)
        if not reason:
            return await call_next(context)

        if mode() == "auto" and _client_elicits(ctx):
            answer = await ctx.elicit(_summary(name, args, reason),
                                      {"dong_y": {"title": "Đồng ý thực hiện"}, "huy": {"title": "Huỷ"}})
            if getattr(answer, "action", None) == "accept" and getattr(answer, "data", None) == "dong_y":
                _log(ctx, "accept", tool=name, reason=reason)
                return await call_next(context)
            _log(ctx, "decline", tool=name, reason=reason)
            return _error(f"Người dùng không đồng ý {reason}; {name} chưa chạy.",
                          {"kind": "approval_declined", "tool": name, "reason": reason})

        self._gc()
        token = secrets.token_urlsafe(12)
        self.pending[token] = Pending(name, args, reason, time.time() + self.ttl_s)
        _log(ctx, "request", tool=name, reason=reason)
        return _error(
            f"{_summary(name, args, reason)}\n\n{name} CHƯA chạy. Cho người dùng xem nội dung trên; chỉ khi người "
            f"dùng đồng ý mới gọi {EXECUTE_TOOL}(token=\"{token}\"). Token dùng một lần, hết hạn sau "
            f"{self.ttl_s // 60} phút.",
            {"kind": "approval_required", "tool": name, "arguments": args, "reason": reason,
             "token": token, "expires_in_s": self.ttl_s},
        )

    async def _execute(self, context: MiddlewareContext, call_next, token: str):
        self._gc()
        p = self.pending.pop(token, None)
        if p is None:
            return _error("Token không hợp lệ, đã dùng hoặc đã hết hạn. Gọi lại tool để lấy token mới.",
                          {"kind": "approval_invalid"})
        _log(context.fastmcp_context, "execute", tool=p.tool, reason=p.reason)
        msg = mt.CallToolRequestParams(name=p.tool, arguments=p.arguments)
        return await call_next(context.copy(message=msg))

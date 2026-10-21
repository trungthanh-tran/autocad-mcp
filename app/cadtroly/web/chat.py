"""Chat với Claude ngay trong palette: Claude gọi các hàm của Service như tool (vòng lặp tool use thủ công).

Chỉ gửi số liệu đã lọc. Không gửi file bản vẽ. Nếu chưa đăng nhập/API key → trả thông báo rõ, không sập UI.
"""
from __future__ import annotations

import json
from typing import Any

from ..service import Service

SYSTEM = """Bạn là AI Trợ lý AutoCAD cho kỹ sư Việt Nam, trả lời ngắn, tiếng Việt.
Bạn có tool đọc bản vẽ, bóc khối lượng (propose → decide → compute → export) và kiểm tra theo bộ quy tắc.
Nguyên tắc: số liệu lấy từ tool, không bịa. Nhóm B/C phải hỏi người dùng trước khi decide, trừ khi họ đã nói rõ.
Khi người dùng nói "X là Y" (ví dụ "WD_2 là cửa sổ nhôm"), gọi decide với save_rule=true. Kết quả Excel: nêu đường dẫn."""


def _tools(svc: Service) -> tuple[list[dict], dict[str, Any]]:
    cur = {"path": None}

    def read(path: str):
        cur["path"] = path
        return svc.read(path)

    def propose(path: str | None = None):
        p = path or cur["path"]
        cur["path"] = p
        r = svc.propose(p)
        r["groups"] = [{k: v for k, v in g.items() if k != "handles"} for g in r["groups"]]
        return r

    def decide(kind: str, name: str, cong_tac: str, don_vi: str, cach_tinh: str, tham_so: dict | None = None,
               save_rule: bool = True, path: str | None = None):
        return svc.decide(path or cur["path"], kind, name, cong_tac, don_vi, cach_tinh, tham_so, save_rule)

    def compute(height_m: float | None = None, path: str | None = None):
        return svc.compute(path or cur["path"], height_m)

    def export(height_m: float | None = None, path: str | None = None):
        return svc.export(path or cur["path"], height_m=height_m)

    def rulesets():
        return svc.rulesets()

    def check(ruleset: str, path: str | None = None):
        r = svc.check(path or cur["path"], ruleset)
        for f in r["findings"]:
            f["handles"] = f["handles"][:5]
        return r

    specs = [
        {"name": "read", "description": "Đọc bản vẽ DXF: layer, block, số đối tượng, đơn vị.",
         "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
        {"name": "propose", "description": "Bước 2 bóc khối lượng: nhóm layer/block và đề xuất công tác, tin cậy A/B/C.",
         "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}}},
        {"name": "decide", "description": "Kỹ sư xác nhận ánh xạ một nhóm; save_rule=true lưu thành quy tắc đơn vị.",
         "input_schema": {"type": "object", "properties": {
             "kind": {"type": "string", "enum": ["layer", "block"]}, "name": {"type": "string"},
             "cong_tac": {"type": "string"}, "don_vi": {"type": "string"},
             "cach_tinh": {"type": "string", "enum": ["count", "length", "area", "volume_by_height", "area_by_height", "skip"]},
             "tham_so": {"type": "object"}, "save_rule": {"type": "boolean"}, "path": {"type": "string"}},
             "required": ["kind", "name", "cong_tac", "don_vi", "cach_tinh"]}},
        {"name": "compute", "description": "Tính khối lượng theo ánh xạ hiện tại. height_m = chiều cao tầng nếu bản vẽ không có text H=.",
         "input_schema": {"type": "object", "properties": {"height_m": {"type": "number"}, "path": {"type": "string"}}}},
        {"name": "export", "description": "Xuất Excel khối lượng có truy vết. Trả về đường dẫn file.",
         "input_schema": {"type": "object", "properties": {"height_m": {"type": "number"}, "path": {"type": "string"}}}},
        {"name": "rulesets", "description": "Liệt kê bộ quy tắc kiểm tra có trong kho.", "input_schema": {"type": "object", "properties": {}}},
        {"name": "check", "description": "Kiểm tra bản vẽ theo bộ quy tắc (id).",
         "input_schema": {"type": "object", "properties": {"ruleset": {"type": "string"}, "path": {"type": "string"}}, "required": ["ruleset"]}},
    ]
    fns = {"read": read, "propose": propose, "decide": decide, "compute": compute, "export": export,
           "rulesets": rulesets, "check": check}
    return specs, fns


class Chat:
    def __init__(self, svc: Service):
        self.svc = svc
        self.history: list[dict] = []
        self.specs, self.fns = _tools(svc)

    def reset(self):
        self.history = []

    def send(self, text: str, current_path: str | None = None) -> dict:
        cfg = self.svc.cfg.llm
        if cfg.provider != "claude":
            return {"reply": "Chat trong palette hiện chỉ hỗ trợ Claude. Chọn Claude ở Cài đặt.", "calls": []}
        try:
            import anthropic
        except ImportError:
            return {"reply": "Chưa cài SDK anthropic. Chạy: pip install anthropic", "calls": []}
        client = anthropic.Anthropic()
        if current_path:
            text = f"[Bản vẽ đang mở: {current_path}]\n{text}"
        self.history.append({"role": "user", "content": text})
        calls = []
        try:
            for _ in range(12):
                resp = client.messages.create(
                    model=cfg.model_main, max_tokens=4000, system=SYSTEM,
                    tools=self.specs, messages=self.history,
                )
                self.history.append({"role": "assistant", "content": resp.content})
                if resp.stop_reason == "refusal":
                    return {"reply": "Claude từ chối yêu cầu này (E-AI-05).", "calls": calls}
                if resp.stop_reason != "tool_use":
                    break
                results = []
                for b in resp.content:
                    if b.type != "tool_use":
                        continue
                    try:
                        out = self.fns[b.name](**b.input)
                        results.append({"type": "tool_result", "tool_use_id": b.id, "content": json.dumps(out, ensure_ascii=False, default=str)[:20000]})
                        calls.append({"tool": b.name, "args": b.input, "ok": True})
                    except Exception as exc:
                        results.append({"type": "tool_result", "tool_use_id": b.id, "content": str(exc), "is_error": True})
                        calls.append({"tool": b.name, "args": b.input, "ok": False, "error": str(exc)})
                self.history.append({"role": "user", "content": results})
            reply = "".join(b.text for b in resp.content if b.type == "text")
            return {"reply": reply or "(không có nội dung)", "calls": calls}
        except anthropic.AuthenticationError:
            self.history.pop()
            return {"reply": "Chưa đăng nhập Claude hoặc API key sai (E-AI-01). Vào Cài đặt → Nguồn AI.", "calls": calls}
        except anthropic.APIConnectionError:
            return {"reply": "Không kết nối được tới Claude (E-AI-04). Kiểm tra mạng.", "calls": calls}
        except anthropic.APIStatusError as exc:
            return {"reply": f"Claude báo lỗi {exc.status_code} (E-AI-03).", "calls": calls}

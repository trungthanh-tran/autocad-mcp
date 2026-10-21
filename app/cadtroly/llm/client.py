"""Gọi LLM: Claude (mặc định, SDK anthropic), Gemini và OpenAI-compatible (httpx) làm dự phòng.

Nguyên tắc dữ liệu: chỉ gửi số liệu đã lọc (tên layer/block, số lượng, text ngắn), không bao giờ
gửi file DWG. Tên dự án/chủ đầu tư được che nếu cfg.llm.mask_project_names.

Ba việc dùng LLM:
  suggest_mapping   gợi ý công tác cho nhóm B/C (JSON)       → model_fast
  extract_rules     bóc văn bản tiêu chuẩn thành bảng quy tắc → model_hard
  plan_edit         lập kế hoạch sửa vẽ (JSON) trước preview  → model_main
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass

from ..config import LLMConfig


class LLMError(RuntimeError):
    pass


@dataclass
class LLM:
    cfg: LLMConfig

    # ------------------------------------------------------------ transport
    def _claude(self, model: str, system: str, user: str, *, effort: str = "medium", max_tokens: int = 8000) -> str:
        try:
            import anthropic
        except ImportError as exc:
            raise LLMError("Chưa cài anthropic SDK: pip install cadtroly[llm]") from exc
        client = anthropic.Anthropic()   # ANTHROPIC_API_KEY hoặc profile `ant auth login`
        kwargs = dict(model=model, max_tokens=max_tokens, system=system,
                      messages=[{"role": "user", "content": user}])
        if effort:
            kwargs["output_config"] = {"effort": effort}
        try:
            with client.messages.stream(**kwargs) as s:
                msg = s.get_final_message()
        except anthropic.AuthenticationError as exc:
            raise LLMError("Claude: chưa đăng nhập hoặc API key sai (E-AI-01)") from exc
        except anthropic.RateLimitError as exc:
            raise LLMError("Claude: vượt hạn mức, thử lại sau (E-AI-02)") from exc
        except anthropic.APIStatusError as exc:
            raise LLMError(f"Claude: lỗi {exc.status_code} (E-AI-03)") from exc
        except anthropic.APIConnectionError as exc:
            raise LLMError("Claude: không kết nối được mạng (E-AI-04)") from exc
        if msg.stop_reason == "refusal":
            raise LLMError("Claude từ chối yêu cầu (E-AI-05)")
        return "".join(b.text for b in msg.content if b.type == "text")

    def _gemini(self, model: str, system: str, user: str, **_) -> str:
        import httpx
        key = os.environ.get("GEMINI_API_KEY")
        if not key:
            raise LLMError("Gemini: thiếu GEMINI_API_KEY (E-AI-01)")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        body = {"system_instruction": {"parts": [{"text": system}]},
                "contents": [{"role": "user", "parts": [{"text": user}]}]}
        r = httpx.post(url, params={"key": key}, json=body, timeout=120)
        if r.status_code != 200:
            raise LLMError(f"Gemini: lỗi {r.status_code} (E-AI-03)")
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]

    def _openai_compat(self, model: str, system: str, user: str, **_) -> str:
        import httpx
        base = os.environ.get("OPENAI_BASE_URL", "http://localhost:11434/v1")
        key = os.environ.get("OPENAI_API_KEY", "none")
        r = httpx.post(f"{base}/chat/completions", headers={"Authorization": f"Bearer {key}"},
                       json={"model": model, "messages": [{"role": "system", "content": system},
                                                          {"role": "user", "content": user}]}, timeout=180)
        if r.status_code != 200:
            raise LLMError(f"OpenAI-compatible: lỗi {r.status_code} (E-AI-03)")
        return r.json()["choices"][0]["message"]["content"]

    def ask(self, tier: str, system: str, user: str, *, effort: str = "medium") -> str:
        model = {"fast": self.cfg.model_fast, "main": self.cfg.model_main, "hard": self.cfg.model_hard}[tier]
        prov = self.cfg.provider
        fn = {"claude": self._claude, "gemini": self._gemini, "openai": self._openai_compat}.get(prov)
        if fn is None:
            raise LLMError(f"Nguồn AI '{prov}' chưa hỗ trợ hoặc đang tắt (none)")
        try:
            return fn(model, system, user, effort=effort)
        except LLMError:
            if self.cfg.fallback_provider and self.cfg.fallback_provider != prov:
                fb = {"claude": self._claude, "gemini": self._gemini, "openai": self._openai_compat}[self.cfg.fallback_provider]
                return fb(model if self.cfg.fallback_provider == "claude" else os.environ.get("FALLBACK_MODEL", "gemini-2.5-flash"),
                          system, user, effort=effort)
            raise

    # ------------------------------------------------------------- helpers
    @staticmethod
    def json_block(text: str):
        m = re.search(r"\{.*\}|\[.*\]", text, re.S)
        if not m:
            raise LLMError("LLM không trả JSON")
        return json.loads(m.group())

    def mask(self, text: str, names: list[str]) -> str:
        if not self.cfg.mask_project_names:
            return text
        for i, n in enumerate(n for n in names if n):
            text = text.replace(n, f"[DU-AN-{i+1}]")
        return text

    # --------------------------------------------------------- 3 tác vụ
    SYS_MAP = ("Bạn là QS xây dựng Việt Nam. Nhận danh sách layer/block trong bản vẽ AutoCAD (tên, số lượng, loại hình, "
               "mẫu text/attribute) và gợi ý công tác chuẩn. Trả về JSON: [{\"kind\",\"name\",\"cong_tac\",\"don_vi\","
               "\"cach_tinh\",\"tham_so\",\"do_tin\":0-1,\"ly_do\"}]. cach_tinh ∈ count|length|area|volume_by_height|"
               "area_by_height|skip. Không chắc thì do_tin thấp. Không bịa độ dày nếu tên không có số.")

    def suggest_mapping(self, groups: list[dict], hints: dict | None = None) -> list[dict]:
        payload = {"groups": groups, "hints": hints or {}}
        out = self.ask("fast", self.SYS_MAP, json.dumps(payload, ensure_ascii=False), effort="low")
        return self.json_block(out)

    SYS_RULES = ("Bạn bóc tiêu chuẩn kỹ thuật xây dựng Việt Nam thành bảng quy tắc máy kiểm tra được. Với mỗi yêu cầu có "
                 "con số hoặc điều kiện rõ, tạo một dòng: {\"id\",\"dieu\" (số điều khoản),\"mo_ta\",\"loai\",\"gia_tri\","
                 "\"don_vi\",\"doi_tuong\",\"muc\":\"loi|canh_bao|xac_nhan\",\"trich\" (câu gốc)}. Yêu cầu ghi 'theo điều kiện "
                 "thực tế'/'theo thiết kế' → muc=xac_nhan. loai gợi ý: min_value|max_value|required|spacing|required_text. "
                 "Trả JSON {\"rules\":[...]}. Không thêm điều không có trong văn bản.")

    def extract_rules(self, std_id: str, text: str) -> dict:
        out = self.ask("hard", self.SYS_RULES, f"Tiêu chuẩn: {std_id}\n\n{text[:120000]}", effort="high")
        data = self.json_block(out)
        for r in data.get("rules", []):
            r.setdefault("duyet", False)
        return data

    SYS_PLAN = ("Bạn là trợ lý vẽ AutoCAD. Nhận yêu cầu và danh sách đối tượng trong vùng đang xem (handle, loại, layer, "
                "toạ độ). Lập kế hoạch bằng số, KHÔNG tự bịa toạ độ ngoài vùng. Trả JSON {\"steps\":[{\"tool\",\"args\","
                "\"mo_ta\"}],\"canh_bao\":[...],\"can_hoi\":[...]}. tool là tên tool acad_* (entity_copy, entity_move, "
                "dimension_linear, block_insert, entity_set_properties, system_run_lisp...). Mọi bước phải trong vùng.")

    def plan_edit(self, request: str, view: dict, entities: list[dict], tools: list[str]) -> dict:
        payload = {"yeu_cau": request, "vung": view, "doi_tuong": entities[:300], "tool_co_san": tools}
        out = self.ask("main", self.SYS_PLAN, json.dumps(payload, ensure_ascii=False), effort="medium")
        return self.json_block(out)


def get_llm(cfg: LLMConfig) -> LLM:
    return LLM(cfg)

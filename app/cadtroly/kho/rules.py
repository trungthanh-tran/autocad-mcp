"""Quy tắc ánh xạ layer/block → công tác, lưu JSON trong kho/quy-tac/.

Không train. Kỹ sư sửa một lần, tool ghi thành rule, lần sau tự áp.
Thứ tự ưu tiên: rule của đơn vị (file users) > rule mặc định (bundled) > heuristic từ khoá.
"""
from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path


def norm(s: str) -> str:
    """Bỏ dấu, thường hoá, gộp ký tự phân cách để so khớp tên layer/block tiếng Việt."""
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("đ", "d").replace("Đ", "D").lower()
    return re.sub(r"[\s_\-\.]+", "", s)


@dataclass
class MappingRule:
    kind: str                     # layer | block
    pattern: str                  # tên chính xác (đã norm) hoặc regex nếu is_regex
    cong_tac: str                 # tên công tác chuẩn, ví dụ "Xây tường 220"
    don_vi: str                   # m, m2, m3, cái, bộ
    cach_tinh: str = "count"      # count | length | area | volume_by_height | area_by_height
    tham_so: dict = field(default_factory=dict)   # ví dụ {"day": 0.22, "cao": "H"} ("H" = lấy từ text H=)
    is_regex: bool = False
    ma_dinh_muc: str = ""         # mã hiệu định mức (TT 38/2026/TT-BXD), do kỹ sư gán; trống = chưa gán
    nguon: str = "don-vi"         # don-vi | mac-dinh | ai
    ghi_chu: str = ""
    dung: int = 0
    cap_nhat: str = ""

    def matches(self, name: str) -> bool:
        n = norm(name)
        if self.is_regex:
            return re.search(self.pattern, n) is not None
        return n == norm(self.pattern)


class RuleStore:
    FILE = "anh-xa.json"

    def __init__(self, dir_: Path, fallback_dir: Path | None = None):
        self.dir = Path(dir_)
        self.fallback_dir = Path(fallback_dir) if fallback_dir else None
        self.dir.mkdir(parents=True, exist_ok=True)
        self.rules: list[MappingRule] = []
        self.load()

    @property
    def path(self) -> Path:
        return self.dir / self.FILE

    def load(self) -> None:
        self.rules = []
        paths = [self.path]
        if self.fallback_dir:
            paths.append(self.fallback_dir / self.FILE)
        for path in paths:
            if path.exists():
                for d in json.loads(path.read_text(encoding="utf-8")):
                    self.rules.append(MappingRule(**d))

    def save(self) -> None:
        self.path.write_text(json.dumps([asdict(r) for r in self.rules], ensure_ascii=False, indent=2),
                             encoding="utf-8")

    def find(self, kind: str, name: str) -> MappingRule | None:
        # rule đơn vị trước, rồi mặc định; khớp chính xác trước regex
        cands = [r for r in self.rules if r.kind == kind and r.matches(name)]
        cands.sort(key=lambda r: (r.nguon != "don-vi", r.is_regex))
        return cands[0] if cands else None

    def upsert(self, rule: MappingRule) -> MappingRule:
        rule.cap_nhat = datetime.now().isoformat(timespec="seconds")
        for i, r in enumerate(self.rules):
            if r.kind == rule.kind and r.pattern == rule.pattern and r.nguon == rule.nguon:
                rule.dung = r.dung
                self.rules[i] = rule
                self.save()
                return rule
        self.rules.append(rule)
        self.save()
        return rule

    def bump(self, rule: MappingRule) -> None:
        rule.dung += 1
        self.save()

    def export(self) -> list[dict]:
        return [asdict(r) for r in self.rules if r.nguon == "don-vi"]

    def import_rules(self, data: list[dict]) -> int:
        n = 0
        for d in data:
            self.upsert(MappingRule(**d))
            n += 1
        return n


# Từ khoá heuristic: (regex trên tên đã norm) -> (công tác, đơn vị, cách tính, tham số, tin cậy B)
HEURISTICS: list[tuple[str, str, str, str, dict]] = [
    (r"tuong|wall|a-?wall", "Xây tường", "m3", "volume_by_height", {"day": None, "cao": "H"}),
    (r"cuaso|window|a-?glaz|^win|cs\d", "Cửa sổ", "bộ", "count", {}),
    (r"cuadi|cua|door|a-?door|^d\d", "Cửa đi", "bộ", "count", {}),
    (r"cot|col(umn)?|s-?cols", "Cột BTCT", "cái", "count", {}),
    (r"dam|beam|s-?beam", "Dầm BTCT", "m", "length", {}),
    (r"san|slab|floor|s-?slab", "Sàn BTCT", "m2", "area", {}),
    (r"mong|found|footing", "Móng", "m3", "volume_by_height", {}),
    (r"thang|stair", "Thang", "cái", "count", {}),
    (r"wc|vesinh|toilet|p-?fixt", "Thiết bị vệ sinh", "bộ", "count", {}),
    (r"den|light|e-?lite", "Đèn", "bộ", "count", {}),
    (r"ong|pipe|p-?pipe", "Ống", "m", "length", {}),
    (r"hatch|gach|lat|tile|fin", "Lát nền", "m2", "area", {}),
    (r"dim|kichthuoc|text|chu|note|ghichu|title|khung", "", "", "skip", {}),
]


def heuristic(kind: str, name: str) -> tuple[str, str, str, dict] | None:
    n = norm(name)
    # tách số độ dày trong tên: tuong220, wall-100
    m = re.search(r"(\d{2,3})", n)
    thick = int(m.group(1)) if m else None
    for rx, ct, dv, cach, ts in HEURISTICS:
        if re.search(rx, n):
            if cach == "skip":
                return ("", "", "skip", {})
            ts = dict(ts)
            if ct == "Xây tường" and thick:
                ct = f"Xây tường {thick}"
                ts["day"] = thick / 1000.0
            return (ct, dv, cach, ts)
    return None

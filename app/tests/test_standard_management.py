from pathlib import Path

import pytest

from cadtroly.config import Config
from cadtroly.kho.store import Kho


def _kho(tmp_path: Path) -> Kho:
    cfg = Config(kho=tmp_path / "kho")
    cfg.ensure_dirs()
    return Kho(cfg)


def _standard(standard_id: str = "vn-fire-demo") -> dict:
    return {
        "id": standard_id,
        "ten": "Demo fire standard",
        "nganh": "fire",
        "phien_ban": "2026.1",
        "nguon": "project",
        "hieu_luc": "2026-01-01",
        "rules": [{"id": "exit-clear", "severity": "warning"}],
    }


def test_standard_add_list_by_industry_and_delete(tmp_path: Path):
    kho = _kho(tmp_path)
    path = kho.standard_add(_standard())
    assert path.exists()
    assert kho.standard_list("fire")[0]["id"] == "vn-fire-demo"
    deleted = kho.standard_delete("vn-fire-demo")
    assert deleted == path and not path.exists()


def test_bundled_standard_cannot_be_deleted(tmp_path: Path):
    with pytest.raises(PermissionError):
        _kho(tmp_path).standard_delete("qcvn-18-2021")


def test_standard_requires_safe_id_and_rules(tmp_path: Path):
    kho = _kho(tmp_path)
    with pytest.raises(ValueError):
        kho.standard_add(_standard("../escape"))
    bad = _standard("safe-id")
    bad["rules"] = {}
    with pytest.raises(ValueError):
        kho.standard_add(bad)

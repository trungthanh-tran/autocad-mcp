from pathlib import Path

import pytest

from cadtroly.config import Config
from cadtroly.kho.store import Kho


def test_add_user_skill_is_safe_and_listed(tmp_path: Path):
    cfg = Config(kho=tmp_path / "kho")
    cfg.ensure_dirs()
    kho = Kho(cfg)
    path = kho.add_skill(
        "qa-mep",
        "---\nname: qa-mep\ndescription: QA MEP\nversion: 0.1\n---\n\n# QA MEP\n",
    )
    assert path == tmp_path / "kho" / "skill" / "qa-mep" / "SKILL.md"
    assert any(item["name"] == "qa-mep" and item["enabled"] for item in kho.skills())


@pytest.mark.parametrize("name", ["../escape", "A skill", "a_b", "x"])
def test_add_skill_rejects_unsafe_names(tmp_path: Path, name: str):
    cfg = Config(kho=tmp_path / "kho")
    cfg.ensure_dirs()
    with pytest.raises(ValueError):
        Kho(cfg).add_skill(name, "---\nname: x\n---\n")


def test_add_skill_does_not_overwrite_bundled_skill(tmp_path: Path):
    cfg = Config(kho=tmp_path / "kho")
    cfg.ensure_dirs()
    with pytest.raises(FileExistsError):
        Kho(cfg).add_skill("qa-ban-ve-toan-dien", "---\nname: x\n---\n")

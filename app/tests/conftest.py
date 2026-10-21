import os
import sys
from pathlib import Path

import pytest

sys.stdout.reconfigure(encoding="utf-8") if hasattr(sys.stdout, "reconfigure") else None
os.environ["AUTOCAD_MCP_BACKEND"] = "ezdxf"
os.environ["TOOL_PROFILE"] = "lean"


@pytest.fixture(scope="session")
def sample_dxf(tmp_path_factory) -> Path:
    from cadtroly.samples import make_sample
    return make_sample(tmp_path_factory.mktemp("dxf") / "mat-bang-tang-3.dxf")


@pytest.fixture
def kho_dir(tmp_path, monkeypatch) -> Path:
    k = tmp_path / "kho"
    monkeypatch.setenv("CADTROLY_KHO", str(k))
    from cadtroly.config import Config
    cfg = Config(kho=k)
    cfg.ensure_dirs()
    src = Path(__file__).parent.parent / "samples" / "kho" / "quy-tac" / "chuan-cong-ty.rules.json"
    (k / "quy-tac" / "chuan-cong-ty.rules.json").write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return k

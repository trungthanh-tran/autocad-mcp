from pathlib import Path


def test_dwg_mcp_allowed_roots_alias_supports_semicolon(monkeypatch, tmp_path):
    first = tmp_path / "one"
    second = tmp_path / "two"
    first.mkdir()
    second.mkdir()
    monkeypatch.delenv("ALLOWED_PATHS", raising=False)
    monkeypatch.setenv("DWG_MCP_ALLOWED_ROOTS", f"{first};{second}")

    from config import Settings

    settings = Settings()
    assert settings.allowed_paths == [Path(first).resolve(), Path(second).resolve()]


def test_primary_allowed_paths_override_compatibility_alias(monkeypatch, tmp_path):
    primary = tmp_path / "primary"
    fallback = tmp_path / "fallback"
    primary.mkdir()
    fallback.mkdir()
    monkeypatch.setenv("ALLOWED_PATHS", str(primary))
    monkeypatch.setenv("DWG_MCP_ALLOWED_ROOTS", str(fallback))

    from config import Settings

    settings = Settings()
    assert settings.allowed_paths == [Path(primary).resolve()]

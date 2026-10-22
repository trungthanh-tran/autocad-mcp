from types import SimpleNamespace


def test_bootstrap_can_be_disabled(monkeypatch):
    from cadtroly.mcp import bootstrap

    monkeypatch.setenv("CADTROLY_AUTO_INSTALL", "false")
    monkeypatch.setattr(
        bootstrap.subprocess,
        "run",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("pip must not run")),
    )
    result = bootstrap.ensure_runtime_dependencies()
    assert result == {"installed": False, "skipped": True, "missing": []}


def test_update_refuses_dirty_checkout(monkeypatch, capsys):
    from cadtroly import cli

    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        return SimpleNamespace(stdout=" M local.py\n")

    monkeypatch.setattr(cli.subprocess, "run", fake_run)
    assert cli.main(["update"]) == 2
    assert len(calls) == 1
    assert "chưa commit" in capsys.readouterr().err

"""`fleting --help` com categoria de init por banco e comandos da engine ativa."""
import sys

import pytest

from fleting.cli.engines import ENGINES, current_project_engine, engine_from_args


def _help(monkeypatch, capsys):
    from fleting.cli import cli
    from fleting.cli.console.console import console

    monkeypatch.setattr(console, "clear", lambda *a, **k: None)
    monkeypatch.setattr(console, "width", 200, raising=False)
    monkeypatch.setattr(sys, "argv", ["fleting", "--help"])
    cli.main()
    return capsys.readouterr().out


def test_engine_from_args():
    assert engine_from_args(["demo"]) == ("sqlite", ["demo"])
    assert engine_from_args(["demo", "--mysql"]) == ("mysql", ["demo"])
    assert engine_from_args(["--mysql", "demo"]) == ("mysql", ["demo"])


def test_engine_from_args_rejeita_duas_flags(monkeypatch):
    monkeypatch.setitem(ENGINES, "fake", ENGINES["mysql"].__class__(
        key="fake", label="Fake", icon="x", flag="--fake"))
    with pytest.raises(ValueError):
        engine_from_args(["demo", "--mysql", "--fake"])


def test_help_fora_de_projeto_mostra_init_e_todas_engines(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    out = _help(monkeypatch, capsys)
    assert "Init with Database" in out
    assert "fleting init <app_name> --mysql" in out
    assert "MySQL / MariaDB Commands" in out
    assert "SQLite Commands" in out
    # a categoria nova vem logo depois de Project Commands
    assert out.index("Project Commands") < out.index("Init with Database") < out.index("Create Commands")


def test_help_em_projeto_mysql_mostra_so_mysql(tmp_path, monkeypatch, capsys):
    from fleting.cli.commands.init import handle_init

    monkeypatch.chdir(tmp_path)
    handle_init(["demo", "--mysql"])
    monkeypatch.chdir(tmp_path / "demo" / "app")
    assert current_project_engine() == "mysql"

    out = _help(monkeypatch, capsys)
    assert "MySQL / MariaDB (this project)" in out
    assert 'fleting[mysql]' in out
    assert "SQLite Commands" not in out


def test_help_em_projeto_sqlite_mostra_so_sqlite(project, monkeypatch, capsys):
    out = _help(monkeypatch, capsys)
    assert "SQLite (this project)" in out
    assert "MySQL / MariaDB Commands" not in out
    assert "fleting[mysql]" not in out
    assert "fleting init <app_name> --mysql" in out  # categoria de init continua visível


def test_init_mysql_mostra_proximos_passos(tmp_path, monkeypatch, capsys):
    from fleting.cli.commands.init import handle_init

    monkeypatch.chdir(tmp_path)
    handle_init(["demo", "--mysql"])
    out = capsys.readouterr().out
    assert 'fleting[mysql]' in out and "FLETING_DB_PASSWORD" in out
    assert '"ENGINE": "mysql"' in (tmp_path / "demo/configs/database.py").read_text("utf-8")


def test_init_sqlite_sem_passos_mysql(tmp_path, monkeypatch, capsys):
    from fleting.cli.commands.init import handle_init

    monkeypatch.chdir(tmp_path)
    handle_init(["demo"])
    assert "fleting[mysql]" not in capsys.readouterr().out

"""Testes para docs/02-correcoes-seguranca-manutencao.md (S1 … S5, M-A … M-F)."""
import ast
import importlib
import re
import sqlite3
import sys
import tomllib

import pytest

from conftest import REPO, read


# ---------------------------------------------------------------- S1
def _run_seed(db_project):
    from fleting.cli.templates.database import db_seed

    db_seed(db_project)
    import core.database as cdb

    return cdb.get_connection().execute("SELECT username, password FROM users").fetchall()


def test_s1_seed_sem_variavel_nao_cria_admin(db_project, monkeypatch):
    monkeypatch.delenv("FLETING_ADMIN_PASSWORD", raising=False)
    assert _run_seed(db_project) == []


def test_s1_seed_com_variavel_grava_hash(db_project, monkeypatch):
    monkeypatch.setenv("FLETING_ADMIN_PASSWORD", "segredo")
    rows = _run_seed(db_project)
    assert len(rows) == 1
    user, pwd = rows[0][0], rows[0][1]
    assert user == "admin"
    assert pwd.startswith("pbkdf2_sha256$") and "segredo" not in pwd


def test_s1_seed_mysql_template():
    src = read("fleting/cli/templates/database_mysql.py")
    assert "VALUES ('admin', 'fleting')" not in src
    assert "INITIAL_SEED" in src  # usa o seed comum (defaults.py)
    assert "FLETING_ADMIN_PASSWORD" in read("fleting/cli/templates/defaults.py")


def test_s1_documentado():
    assert "FLETING_ADMIN_PASSWORD" in read("docs/pt/cli.md")


# ---------------------------------------------------------------- S2
@pytest.mark.parametrize(
    "chamada",
    [
        lambda M: M.where(**{"id=1 OR 1": 1}),
        lambda M: M.create(**{"username) VALUES ('x');--": "a"}),
    ],
)
def test_s2_identificador_invalido_lanca_value_error(db_project, chamada):
    from core.base_model import BaseModel

    class Users(BaseModel):
        table_name = "users"

    with pytest.raises(ValueError):
        chamada(Users)


def test_s2_tabela_invalida(db_project):
    from core.base_model import BaseModel

    class Evil(BaseModel):
        table_name = "users; DROP TABLE users"

    with pytest.raises(ValueError):
        Evil.all()


# ---------------------------------------------------------------- S3
def test_s3_pull_sqlite_get_columns_funciona():
    from fleting.cli.commands.pull_sqlite import get_columns, get_foreign_keys

    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT)")
    cur = conn.cursor()
    cols = get_columns(cur, "users")
    assert [c[1] for c in cols] == ["id", "username"]
    get_foreign_keys(cur, "users")  # não deve lançar


def test_s3_pull_sqlite_sem_interpolacao_de_tabela():
    src = read("fleting/cli/commands/pull_sqlite.py")
    assert not re.search(r"PRAGMA \w+\(\{", src), "ainda interpola nome de tabela em PRAGMA"


@pytest.mark.parametrize("arquivo", ["shell_sqlite.py", "shell_mysql.py"])
def test_s3_shell_valida_antes_de_consultar(arquivo):
    src = read(f"fleting/cli/commands/{arquivo}")
    assert "SELECT * FROM {table_name}" not in src
    assert "[A-Za-z_][A-Za-z0-9_]*" in src


def test_s3_pull_recusa_tabela_invalida(project, monkeypatch):
    from fleting.cli.commands import pull

    chamado = []
    monkeypatch.setattr(
        "fleting.cli.commands.pull_sqlite.handle_pull_sqlite",
        lambda *a, **k: chamado.append(a),
        raising=False,
    )
    try:
        pull.handle_pull(["pull", "x); DROP TABLE users;--"])
    except SystemExit:
        pass
    assert not chamado, "pull.py não valida o nome da tabela"


# ---------------------------------------------------------------- S4
def test_s4_config_mysql_le_env(project, monkeypatch):
    from fleting.cli.helpers.project import activate_project

    activate_project(project)
    monkeypatch.setenv("FLETING_DB_PASSWORD", "abc")
    monkeypatch.setenv("FLETING_DB_PORT", "3307")
    import configs.database as cfg

    importlib.reload(cfg)
    assert cfg.DATABASE["MYSQL"]["PASSWORD"] == "abc"
    assert cfg.DATABASE["MYSQL"]["PORT"] == 3307


def test_s4_engine_ainda_detectavel(project):
    from fleting.cli.commands.db import get_engine_from_config

    assert get_engine_from_config(project) == "sqlite"


# ---------------------------------------------------------------- S5
@pytest.mark.parametrize("lang", ["pt", "es", "en"])
def test_s5_aviso_de_execucao_de_codigo(lang):
    p = REPO / "docs" / lang / "cli.md"
    if not p.exists():
        pytest.skip(f"{p} não existe")
    txt = p.read_text("utf-8").lower()
    assert "migrations/" in txt and "seeds/" in txt and "routes.py" in txt
    assert any(w in txt for w in ("confiáveis", "confiables", "trusted"))


# ---------------------------------------------------------------- M-B
def test_mb_comando_desconhecido_sai_com_2(monkeypatch):
    from fleting.cli import cli

    monkeypatch.setattr(sys, "argv", ["fleting", "naoexiste"])
    with pytest.raises(SystemExit) as e:
        cli.main()
    assert e.value.code == 2


def test_mb_erro_sai_com_1_sem_traceback(monkeypatch, capsys):
    from fleting.cli import cli

    def boom(*a, **k):
        raise RuntimeError("falhou")

    monkeypatch.setattr(cli, "handle_info", boom)
    monkeypatch.delenv("FLETING_DEBUG", raising=False)
    monkeypatch.setattr(sys, "argv", ["fleting", "info"])
    with pytest.raises(SystemExit) as e:
        cli.main()
    assert e.value.code == 1
    out = capsys.readouterr()
    assert "Traceback" not in out.out + out.err


def test_mb_create_page_mensagem_de_erro():
    assert 'console.print("Error creating page: ", str(e)' not in read("fleting/cli/commands/create.py")


# ---------------------------------------------------------------- M-C
def test_mc_dependencias_nao_usadas():
    deps = tomllib.loads(read("pyproject.toml"))["project"]["dependencies"]
    codigo = "\n".join(p.read_text("utf-8") for p in (REPO / "fleting").rglob("*.py"))
    for dep in ("typer", "psutil"):
        if any(d.split("=")[0].split(">")[0].strip() == dep for d in deps):
            assert re.search(rf"\bimport {dep}\b|\bfrom {dep}\b", codigo), f"{dep} declarado mas não usado"


# ---------------------------------------------------------------- M-E
def test_me_workflows_atualizados():
    for wf in (REPO / ".github" / "workflows").glob("*.yml"):
        txt = wf.read_text("utf-8")
        assert "actions/checkout@v3" not in txt, wf.name
        assert "actions/setup-python@v4" not in txt, wf.name


# ---------------------------------------------------------------- M-F
def test_mf_register_route_aceita_espacos(project):
    from fleting.cli.commands.create import register_route

    routes = project / "configs/routes.py"
    routes.write_text(routes.read_text("utf-8").replace("ROUTES = [", "ROUTES  =  ["), "utf-8")
    register_route("extra")
    txt = routes.read_text("utf-8")
    assert '"/extra"' in txt
    ast.parse(txt)

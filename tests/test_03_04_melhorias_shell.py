"""Testes para docs/03-melhorias.md (M1, M4, M5, M6, M7) e para a parte de
docs/04-atualizacao-shell-mysql-mariadb.md que não precisa de servidor."""
import ast
import sys
import tomllib

import pytest

from conftest import REPO, read


# ================================================================ 03-M5 transações / conexão
def test_m5_transaction_faz_rollback(db_project):
    from core.database import transaction, get_connection

    with pytest.raises(RuntimeError):
        with transaction() as conn:
            conn.execute("INSERT INTO users (username, password) VALUES ('x', 'y')")
            raise RuntimeError("boom")

    assert get_connection().execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0


def test_m5_close_connection_reabre(db_project):
    import core.database as cdb

    c1 = cdb.get_connection()
    cdb.close_connection()
    assert cdb._connection is None
    c2 = cdb.get_connection()
    assert c2 is not c1


def test_m5_sqlite_multithread(db_project):
    import threading
    import core.database as cdb

    erros = []

    def worker():
        try:
            cdb.get_connection().execute("SELECT 1").fetchone()
        except Exception as e:  # noqa: BLE001
            erros.append(e)

    t = threading.Thread(target=worker)
    t.start()
    t.join()
    assert not erros


def test_m5_dict_cursor_nao_altera_conexao(db_project):
    """Cursor dict não pode quebrar quem usa a conexão com tuplas (core/migrations.py)."""
    import core.database as cdb
    from core.migrations import applied_migrations

    cdb.dict_cursor(cdb.get_connection())
    assert applied_migrations() == ["001_initial.py"]


def test_m5_main_fecha_conexao(project):
    main = (project / "main.py").read_text("utf-8")
    assert "close_connection" in main and "on_disconnect" in main


# ================================================================ 03-M6 doctor
def test_m6_doctor_projeto_ok(project):
    from fleting.cli.commands.doctor import run_checks

    res = run_checks(project)
    assert not [m for lvl, m in res if lvl == "error"], res


def test_m6_doctor_detecta_rota_quebrada_e_view_orfa(project):
    from fleting.cli.commands.create import handle_create
    from fleting.cli.commands.doctor import run_checks

    handle_create(["page", "orfa"])
    (project / "app/views/pages/orfa_view.py").unlink()
    (project / "app/views/pages/solta_view.py").write_text("x = 1\n", "utf-8")

    res = run_checks(project)
    msgs = " ".join(m for _, m in res)
    assert any(lvl == "error" and "orfa" in m for lvl, m in res)
    assert any(lvl == "warning" and "solta_view.py" in m for lvl, m in res), msgs


def test_m6_doctor_no_cli(monkeypatch, project):
    from fleting.cli import cli

    monkeypatch.setattr(sys, "argv", ["fleting", "doctor"])
    cli.main()  # projeto saudável → não sai com erro


# ================================================================ 03-M1 / M4 / M7
def test_m1_extras_dev():
    extras = tomllib.loads(read("pyproject.toml"))["project"]["optional-dependencies"]
    assert any(d.startswith("pytest") for d in extras["dev"])


def test_m4_workflow_de_testes():
    wf = read(".github/workflows/tests.yml")
    assert "pytest" in wf and "ruff check" in wf
    assert "pytest" in read(".github/workflows/publish.yml")


def test_m7_changelog():
    txt = read("CHANGELOG.md")
    versao = tomllib.loads(read("pyproject.toml"))["project"]["version"]
    assert f"[{versao}]" in txt


# ================================================================ 04-P1 extras
def test_p1_extras_mysql_mariadb():
    extras = tomllib.loads(read("pyproject.toml"))["project"]["optional-dependencies"]
    assert any("mysql-connector-python" in d for d in extras["mysql"])
    assert any(d.lower().startswith("pymysql") for d in extras["mariadb"])


# ================================================================ 04-P2 core/database.py
def test_p2_core_database_nao_importa_driver_no_topo(tmp_path):
    from fleting.cli.templates.index import init_project

    init_project(tmp_path, "X", engine="mysql")
    src = (tmp_path / "core/database.py").read_text("utf-8")
    tree = ast.parse(src)
    top_imports = [
        n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))
    ]
    nomes = {a.name for n in top_imports for a in n.names} | {
        getattr(n, "module", None) for n in top_imports
    }
    assert "mysql.connector" not in nomes and "pymysql" not in nomes
    assert "utf8mb4_general_ci" in src  # SH6 collation MariaDB
    assert '"pymysql"' in src


def test_p2_config_tem_driver_e_collation(project, monkeypatch):
    from fleting.cli.helpers.project import activate_project
    import importlib

    activate_project(project)
    monkeypatch.setenv("FLETING_DB_DRIVER", "pymysql")
    import configs.database as cfg

    importlib.reload(cfg)
    assert cfg.DATABASE["MYSQL"]["DRIVER"] == "pymysql"
    assert cfg.DATABASE["MYSQL"]["OPTIONS"]["collation"] == "utf8mb4_general_ci"


def test_p2_driver_ausente_mensagem_clara(project, monkeypatch):
    from fleting.cli.helpers.project import activate_project

    activate_project(project)
    import core.database as cdb

    monkeypatch.setitem(cdb.DATABASE, "ENGINE", "mysql")
    monkeypatch.setitem(cdb.DATABASE["MYSQL"], "DRIVER", "pymysql")
    monkeypatch.setitem(sys.modules, "pymysql", None)  # simula não instalado
    with pytest.raises(RuntimeError, match=r"fleting\[mariadb\]"):
        cdb.get_connection()


# ================================================================ 04-P3 migrations MySQL
def test_p3_migrations_mysql_sem_db_execute(tmp_path):
    from fleting.cli.templates.database_mysql import db_init, make_migration

    db_init(tmp_path, "mysql")
    make_migration(tmp_path, "exemplo")
    for f in [tmp_path / "core/migrations.py", *(tmp_path / "migrations").glob("0*.py"),
              tmp_path / "seeds/initial.py"]:
        src = f.read_text("utf-8")
        ast.parse(src)
        assert "db.execute(" not in src, f.name


def test_p3_check_dependency_respeita_driver(monkeypatch):
    from fleting.cli.templates.database_mysql import check_mysql_dependency

    monkeypatch.setitem(sys.modules, "pymysql", None)
    assert check_mysql_dependency("pymysql") is False


# ================================================================ 04-P4 troca de engine
def test_p4_db_init_troca_engine_com_backup(project):
    from fleting.cli.commands.db import handle_db, get_engine_from_config

    handle_db(["init"])  # sqlite
    assert (project / "core/migrations.py").exists()

    handle_db(["init", "--mysql"])
    assert get_engine_from_config(project) == "mysql"
    assert (project / "core/database.py.bak").exists()
    assert (project / "core/migrations.py.bak").exists()
    mig = (project / "core/migrations.py").read_text("utf-8")
    assert "AUTO_INCREMENT" in mig

    handle_db(["init", "--sqlite"])
    assert get_engine_from_config(project) == "sqlite"
    assert "AUTOINCREMENT" in (project / "core/migrations.py").read_text("utf-8")


def test_p4_troca_engine_regenera_seed_antigo(project):
    """Seed/migration de versões antigas (com db.execute) são trocados na mudança de engine."""
    from fleting.cli.commands.db import handle_db

    handle_db(["init"])
    seed = project / "seeds/initial.py"
    seed.write_text("def run(db):\n    db.execute('INSERT OR IGNORE INTO users VALUES (1)')\n", "utf-8")
    custom = project / "seeds/meu_seed.py"
    custom.write_text("def run(db):\n    pass\n", "utf-8")

    handle_db(["init", "--mysql"])
    assert "db.execute" not in seed.read_text("utf-8")
    assert (project / "seeds/initial.py.bak").exists()
    assert custom.read_text("utf-8") == "def run(db):\n    pass\n"  # seeds do usuário intactos


def test_p4_defaults_sao_agnosticos(db_project, monkeypatch):
    """Mesma migration/seed padrão em SQLite (MySQL coberto em test_04_mysql.py)."""
    from fleting.cli.templates.defaults import INITIAL_MIGRATION, INITIAL_SEED

    for src in (INITIAL_MIGRATION, INITIAL_SEED):
        ast.parse(src)
        assert "db.execute(" not in src


def test_p4_db_somente_flag_nao_quebra(project):
    from fleting.cli.commands.db import handle_db

    handle_db(["--mysql"])  # sem subcomando: só mostra o uso


# ================================================================ 04-P5 shells
def test_p5_shells_sem_efeito_colateral_no_import(monkeypatch):
    monkeypatch.delattr(sys, "ps1", raising=False)
    for mod in ("fleting.cli.commands.shell_sqlite", "fleting.cli.commands.shell_mysql"):
        sys.modules.pop(mod, None)
        __import__(mod)
    assert not hasattr(sys, "ps1")


@pytest.mark.parametrize("modulo", ["shell_sqlite", "shell_mysql"])
def test_p5_load_models_de_app_models(project, modulo):
    import importlib
    from fleting.cli.commands.create import handle_create

    handle_create(["model", "produto"])
    mod = importlib.import_module(f"fleting.cli.commands.{modulo}")
    loaded = mod.load_models(project)
    assert "ProdutoModel" in loaded


def test_p5_load_models_ignora_model_quebrado(project):
    from fleting.cli.commands.shell_mysql import load_models

    (project / "app/models/ruim_model.py").write_text("import nao_existe\n", "utf-8")
    load_models(project)  # não deve lançar


# ================================================================ 04-P6 pull MySQL
@pytest.mark.parametrize("tipo,esperado", [("uuid", "str"), ("inet6", "str"), ("int(11)", "int")])
def test_p6_map_type_mariadb(tipo, esperado):
    from fleting.cli.commands.pull_mysql import map_type

    assert map_type(tipo) == esperado


# ================================================================ 04-P7 help/docs
def test_p7_help_menciona_mysql():
    src = read("fleting/cli/cli.py")
    assert "SQLite only" not in src
    assert "MySQL/MariaDB" in src


@pytest.mark.parametrize("lang", ["pt", "es"])
def test_p7_docs_shell_mysql(lang):
    txt = read(f"docs/{lang}/cli.md")
    assert 'fleting[mysql]' in txt and 'fleting[mariadb]' in txt

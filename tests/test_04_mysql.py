"""Integração MySQL / MariaDB (docs/04, passo 8).

Só roda com FLETING_TEST_MYSQL=1 e um servidor acessível pelas variáveis
FLETING_DB_HOST/PORT/USER/PASSWORD/NAME/DRIVER. Exemplo local:

    docker run -d --name mysql-local   -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=fleting -p 3306:3306 mysql:8
    docker run -d --name mariadb-local -e MARIADB_ROOT_PASSWORD=root -e MARIADB_DATABASE=fleting -p 3307:3306 mariadb:11
"""
import os

import pytest

pytestmark = pytest.mark.skipif(not os.getenv("FLETING_TEST_MYSQL"), reason="MySQL not configured")


@pytest.fixture
def mysql_project(tmp_path, monkeypatch):
    from conftest import _purge_project_modules
    from fleting.cli.helpers.project import activate_project
    from fleting.cli.templates.index import init_project
    from fleting.cli.templates.database_mysql import db_init, db_migrate

    root = tmp_path / "shtest"
    root.mkdir()
    init_project(root, "ShTest", engine="mysql")
    _purge_project_modules()
    monkeypatch.chdir(root)
    activate_project(root)

    import core.database as cdb

    # banco limpo
    conn = cdb.get_connection()
    cur = conn.cursor()
    for t in ("users", "_fleting_migrations", "exemplo"):
        cur.execute(f"DROP TABLE IF EXISTS `{t}`")
    conn.commit()
    cur.close()

    db_init(root, "mysql")
    db_migrate(root)
    yield root
    cdb.close_connection()
    _purge_project_modules()


def _helpers():
    from configs.database import DATABASE
    from core.database import get_connection
    from fleting.cli.commands.shell_mysql import build_helpers

    return build_helpers(get_connection(), DATABASE["MYSQL"]["DRIVER"])


def test_migrate_status_rollback(mysql_project, capsys):
    from fleting.cli.templates.database_mysql import db_status, db_rollback, make_migration, db_migrate
    from core.migrations import applied_migrations

    assert applied_migrations() == ["001_initial.py"]

    make_migration(mysql_project, "exemplo")
    db_migrate(mysql_project)
    assert len(applied_migrations()) == 2
    assert "exemplo" in _helpers()["tables"]()

    db_rollback(mysql_project)
    assert applied_migrations() == ["001_initial.py"]
    assert "exemplo" not in _helpers()["tables"]()

    db_status(mysql_project)
    assert "001_initial.py" in capsys.readouterr().out


def test_seed_com_hash(mysql_project, monkeypatch):
    from fleting.cli.templates.database_mysql import db_seed

    monkeypatch.setenv("FLETING_ADMIN_PASSWORD", "segredo")
    db_seed(mysql_project)
    db_seed(mysql_project)  # idempotente
    rows = _helpers()["query"]("SELECT username, password FROM users")
    assert len(rows) == 1
    assert rows[0]["password"].startswith("pbkdf2_sha256$")


def test_orm_crud(mysql_project):
    from core.base_model import BaseModel

    class Users(BaseModel):
        table_name = "users"

    u = Users.create(username="ana", password="x")
    assert Users.find(u["id"])["username"] == "ana"
    assert Users.where(username="ana")[0]["id"] == u["id"]
    assert Users.count() == 1

    obj = Users()
    obj.username, obj.password = "bob", "1"
    obj.save()
    obj.password = "2"
    obj.save()
    assert Users.find(obj.id)["password"] == "2"
    obj.delete()
    assert Users.count() == 1

    with pytest.raises(ValueError):
        Users.where(**{"id=1 OR 1": 1})


def test_shell_helpers(mysql_project, capsys):
    h = _helpers()
    assert {"users", "_fleting_migrations"} <= set(h["tables"]())

    assert h["query"]("INSERT INTO users (username, password) VALUES (%s, %s)", ("z", "p")) == 1
    # sem "Unread result found" entre chamadas seguidas
    for _ in range(3):
        assert h["table_exists"]("users")
    assert h["query"]("SELECT COUNT(*) n FROM users")[0]["n"] == 1
    assert h["query"]("UPDATE users SET username=%s WHERE username=%s", ("adm", "z")) == 1

    h["describe"]("users")
    h["table"]("users", limit=5)
    h["table"]("x; DROP TABLE users")
    out = capsys.readouterr().out
    assert "Table not found" in out
    assert "users" in h["tables"]()


def test_pull_mysql_gera_model(mysql_project):
    from fleting.cli.commands.pull_mysql import handle_pull_mysql

    handle_pull_mysql(mysql_project, "users", force=True)
    assert (mysql_project / "app/models/users_model.py").exists()


def test_shell_load_models(mysql_project):
    from fleting.cli.commands.create import handle_create
    from fleting.cli.commands.shell_mysql import load_models

    handle_create(["model", "users"])
    assert "UsersModel" in load_models(mysql_project)

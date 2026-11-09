"""Testes para docs/01-bugs-funcionais.md (B1 … B12)."""
import ast
import re
import tomllib

import pytest

from conftest import REPO, read


# ---------------------------------------------------------------- B3
def test_b3_init_importa_os():
    import fleting.cli.commands.init as init_mod

    assert hasattr(init_mod, "os"), "init.py usa os.symlink mas não importa os"
    assert "import stat" not in read("fleting/cli/commands/init.py")


# ---------------------------------------------------------------- B8
def test_b8_db_sem_print_de_debug_nem_bloco_comentado():
    src = read("fleting/cli/commands/db.py")
    assert "print(engine)" not in src
    assert "# def find_project_root" not in src
    assert "# def activate_project" not in src


# ---------------------------------------------------------------- B11
def test_b11_versao_vem_do_metadata():
    import fleting

    pyproject = tomllib.loads(read("pyproject.toml"))
    esperado = pyproject["project"]["version"]
    assert fleting.__version__ in (esperado, "0.0.0-dev")
    assert fleting.__version__ != "0.1.0"


# ---------------------------------------------------------------- B4
def test_b4_create_page_snake_case_gera_classes_pascal(project):
    from fleting.cli.commands.create import handle_create

    handle_create(["page", "user_profile"])

    view = (project / "app/views/pages/user_profile_view.py").read_text("utf-8")
    ctrl = (project / "app/controllers/user_profile_controller.py").read_text("utf-8")
    model = (project / "app/models/user_profile_model.py").read_text("utf-8")
    routes = (project / "configs/routes.py").read_text("utf-8")

    assert "class UserProfileView" in view
    assert "import UserProfileController" in view
    assert "class UserProfileController" in ctrl
    assert "import UserProfileModel" in ctrl
    assert "class UserProfileModel" in model
    assert "user_profile_view.UserProfileView" in routes
    assert "User_profile" not in view + ctrl + model + routes

    for f in (view, ctrl, model, routes):
        ast.parse(f)


def test_b4_controller_e_model_gerados_importam(project):
    from fleting.cli.commands.create import handle_create

    handle_create(["page", "user_profile"])
    import importlib

    mod = importlib.import_module("app.controllers.user_profile_controller")
    assert mod.UserProfileController().get_title()


# ---------------------------------------------------------------- B5
@pytest.mark.parametrize("nome", ["my-page", "../x", "1abc", "class", "a b", "x/y"])
def test_b5_nome_invalido_recusado(project, nome):
    from fleting.cli.commands.create import handle_create

    antes = sorted(p.relative_to(project) for p in project.rglob("*"))
    handle_create(["page", nome])
    depois = sorted(p.relative_to(project) for p in project.rglob("*"))
    assert antes == depois


def test_b5_create_fora_de_projeto_nao_quebra(tmp_path, monkeypatch):
    from fleting.cli.commands.create import handle_create

    monkeypatch.chdir(tmp_path)
    handle_create(["page", "x"])  # não deve lançar exceção
    assert not any(tmp_path.iterdir())


# ---------------------------------------------------------------- B2
def test_b2_delete_page_a_partir_de_subpasta_remove_arquivos_e_rota(project, monkeypatch):
    from fleting.cli.commands.create import handle_create
    from fleting.cli.commands.delete import handle_delete

    handle_create(["page", "teste"])
    assert (project / "app/views/pages/teste_view.py").exists()

    monkeypatch.chdir(project / "app" / "controllers")
    handle_delete(["page", "teste"])

    assert not (project / "app/views/pages/teste_view.py").exists()
    assert not (project / "app/controllers/teste_controller.py").exists()
    assert not (project / "app/models/teste_model.py").exists()

    routes = (project / "configs/routes.py").read_text("utf-8")
    assert '"/teste"' not in routes
    ast.parse(routes)
    # rotas padrão continuam lá
    assert '"/settings"' in routes or '"/help"' in routes


def test_b2_delete_nao_usa_cwd_fixo():
    assert "Path.cwd()" not in read("fleting/cli/commands/delete.py")


# ---------------------------------------------------------------- B9
@pytest.mark.parametrize(
    "arquivo",
    [
        "fleting/cli/commands/list.py",
        "fleting/cli/commands/shell.py",
        "fleting/cli/commands/shell_sqlite.py",
        "fleting/cli/commands/db.py",
    ],
)
def test_b9_sem_copias_locais_do_helper_de_projeto(arquivo):
    tree = ast.parse(read(arquivo))
    funcs = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    dup = funcs & {"get_project_root", "find_project_root", "is_fleting_project", "activate_project"}
    assert not dup, f"{arquivo} redefine {dup}; use fleting.cli.helpers.project"


def test_b9_helper_usa_console():
    src = read("fleting/cli/helpers/project.py")
    assert "print(" not in src.replace("console.print(", "")


def test_b9_list_funciona_em_subpasta(project, monkeypatch):
    from fleting.cli.commands.list import handle_list

    monkeypatch.chdir(project / "app" / "views")
    handle_list(["pages"])  # não deve lançar


# ---------------------------------------------------------------- B1 / B10 (ORM SQLite)
def _users_model():
    from core.base_model import BaseModel

    class UsersModel(BaseModel):
        table_name = "users"

    return UsersModel


def test_b1_orm_crud_sqlite(db_project):
    Users = _users_model()

    criado = Users.create(username="ana", password="x")
    assert criado["username"] == "ana"
    assert Users.find(criado["id"])["username"] == "ana"
    assert Users.first()["username"] == "ana"

    rows = Users.where(username="ana")
    assert len(rows) == 1 and rows[0]["username"] == "ana"
    assert Users.exists(username="ana")
    assert Users.count() == 1
    assert len(Users.all()) == 1


def test_b1_orm_relacoes_importam_placeholder(db_project):
    from core.orm import ForeignKey, HasMany  # noqa: F401
    import core.orm

    assert hasattr(core.orm, "placeholder"), "core/orm.py usa placeholder() sem importar"


def test_b1_placeholder_por_engine(db_project, monkeypatch):
    import core.database as cdb

    assert cdb.placeholder() == "?"
    monkeypatch.setitem(cdb.DATABASE, "ENGINE", "mysql")
    assert cdb.placeholder() == "%s"


def test_b1_template_mysql_tem_helpers(tmp_path):
    from fleting.cli.templates.index import init_project

    init_project(tmp_path, "X", engine="mysql")
    src = (tmp_path / "core/database.py").read_text("utf-8")
    assert "def placeholder" in src and "def dict_cursor" in src
    ast.parse(src)


def test_b10_save_insere_e_atualiza(db_project):
    Users = _users_model()

    u = Users()
    u.username = "bob"
    u.password = "1"
    u.save()
    assert u.id

    u.password = "2"
    u.save()
    assert Users.find(u.id)["password"] == "2"
    assert Users.count() == 1

    u.delete()
    assert Users.count() == 0


# ---------------------------------------------------------------- B6
def test_b6_fleting_app_removido_ou_atualizado(project):
    main = (project / "main.py").read_text("utf-8")
    app = project / "core/app.py"
    if app.exists():
        src = app.read_text("utf-8")
        assert "text=" not in src, "core/app.py ainda usa API antiga do Flet (text=)"
    else:
        assert "FletingApp" not in main


# ---------------------------------------------------------------- B7
def test_b7_idioma_vem_do_appstate(project):
    main = (project / "main.py").read_text("utf-8")
    assert 'I18n.load("pt")' not in main
    assert "I18n.load(AppState.language)" in main


# ---------------------------------------------------------------- todos os templates gerados são Python válido
def test_templates_gerados_compilam(project):
    erros = []
    for f in project.rglob("*.py"):
        try:
            ast.parse(f.read_text("utf-8"))
        except SyntaxError as e:
            erros.append(f"{f.relative_to(project)}: {e}")
    assert not erros, "\n".join(erros)


# ---------------------------------------------------------------- B12
def test_b12_readme_badges():
    readme = read("README.md")
    assert "Python-3.11+" in readme
    assert re.search(r"Flet-1\.0\.5", readme)
    assert "Python-3.10" not in readme and "Flet-0.25" not in readme


@pytest.mark.parametrize("lang", ["pt", "es", "en"])
def test_b12_enviroment_docs(lang):
    p = REPO / "docs" / lang / "enviroment.md"
    if not p.exists():
        pytest.skip(f"{p} não existe")
    txt = p.read_text("utf-8")
    assert "3.10" not in txt and "0.25" not in txt

"""Fixtures compartilhadas.

Os testes cobrem os itens de docs/01-bugs-funcionais.md (B*) e
docs/02-correcoes-seguranca-manutencao.md (S*, M-*). Cada teste leva o código
do item no nome para facilitar acompanhar o checklist.
"""
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
PKG = REPO / "fleting"

# Módulos do projeto gerado (ficam em sys.path via activate_project)
_PROJECT_MODULES = ("core", "configs", "app", "migrations", "seeds", "runtime_imports")


def _purge_project_modules():
    for name in list(sys.modules):
        if name.split(".")[0] in _PROJECT_MODULES:
            del sys.modules[name]


@pytest.fixture
def project(tmp_path, monkeypatch):
    """Gera um projeto Fleting (SQLite) em tmp_path e entra nele."""
    from fleting.cli.templates.index import init_project

    root = tmp_path / "demo"
    root.mkdir()
    init_project(root, "Demo", engine="sqlite")

    _purge_project_modules()
    old_path = list(sys.path)
    monkeypatch.chdir(root)
    yield root
    _purge_project_modules()
    sys.path[:] = old_path


@pytest.fixture
def db_project(project, monkeypatch):
    """Projeto com `db init` + `db migrate` já executados."""
    from fleting.cli.helpers.project import activate_project
    from fleting.cli.templates.database import db_init, db_migrate

    activate_project(project)
    db_init(project, "sqlite")
    db_migrate(project)
    yield project
    try:
        import core.database as cdb

        if cdb._connection is not None:
            cdb._connection.close()
            cdb._connection = None
    except Exception:
        pass


def read(rel: str) -> str:
    return (REPO / rel).read_text(encoding="utf-8")

# fleting/cli/engines.py
"""Registro das engines de banco suportadas pela CLI.

Para adicionar uma engine nova (ex.: SQL Server), basta incluir uma entrada em
ENGINES: o `fleting --help`, o `fleting init <app> --<flag>` e a mensagem
pós-init passam a mostrá-la automaticamente.
"""
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Engine:
    key: str                      # valor de "ENGINE" em configs/database.py
    label: str                    # nome exibido
    icon: str
    flag: str | None              # flag do `fleting init` (None = padrão)
    commands: list[tuple[str, str]] = field(default_factory=list)


ENGINES: dict[str, Engine] = {
    "sqlite": Engine(
        key="sqlite",
        label="SQLite",
        icon="🪶",
        flag=None,
        commands=[
            ("fleting db init --sqlite", "Switch an existing project to SQLite"),
            ("fleting shell", "tables(), query(sql), table(\"t\"), models()"),
        ],
    ),
    "mysql": Engine(
        key="mysql",
        label="MySQL / MariaDB",
        icon="🐬",
        flag="--mysql",
        commands=[
            ('pip install "fleting[mysql]"', "Install MySQL driver (mysql-connector)"),
            ('pip install "fleting[mariadb]"', "Install MariaDB driver (DRIVER=pymysql)"),
            ("fleting db init --mysql", "Switch an existing project to MySQL"),
            ("FLETING_DB_HOST, _PORT, _USER", "Server settings (env vars)"),
            ("FLETING_DB_PASSWORD, _NAME", "Credentials and database (env vars)"),
            ("FLETING_DB_DRIVER=pymysql", "Use PyMySQL (recommended for MariaDB)"),
            ("fleting shell", "tables(), describe(t), table(t), query(sql)"),
        ],
    ),
    # "sqlserver": Engine(key="sqlserver", label="SQL Server", icon="🟥", flag="--sqlserver", commands=[...]),
}

DEFAULT_ENGINE = "sqlite"


def engine_from_args(args: list[str]) -> tuple[str, list[str]]:
    """Separa a flag de engine dos demais argumentos. Retorna (engine, args_restantes)."""
    flags = {e.flag: e.key for e in ENGINES.values() if e.flag}
    chosen = [flags[a] for a in args if a in flags]
    if len(chosen) > 1:
        raise ValueError(f"Choose only one database engine: {', '.join(flags)}")
    rest = [a for a in args if a not in flags]
    return (chosen[0] if chosen else DEFAULT_ENGINE), rest


def current_project_engine(start: Path | None = None) -> str | None:
    """Engine do projeto no diretório atual (ou None fora de um projeto). Não imprime nada."""
    from fleting.cli.helpers.project import find_project_root

    root = find_project_root(start)
    if not root or not (root / "configs" / "database.py").exists():
        return None
    import re

    m = re.search(r'"ENGINE":\s*"([^"]+)"', (root / "configs" / "database.py").read_text(encoding="utf-8"))
    return m.group(1).lower() if m and m.group(1).lower() in ENGINES else None

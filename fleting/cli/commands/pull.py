# fleting/cli/commands/pull.py
import re
import sys
from fleting.cli.helpers.project import get_project_root
from fleting.cli.console.console import console


def register_db_commands(subparsers):
    """Registra os comandos db"""
    db_parser = subparsers.add_parser("db")
    db_sub = db_parser.add_subparsers(dest="db_command")

    model_parser = db_sub.add_parser("model")
    model_sub = model_parser.add_subparsers(dest="model_command")

    pull_parser = model_sub.add_parser("pull")
    pull_parser.add_argument("--table", help="Pull apenas uma tabela")
    pull_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing models"
    )


def handle_pull(args: list[str]):
    """Ponto de entrada - detecta engine e redireciona"""
    if not args:
        console.print("[error]Error: No arguments provided.[/error]")
        sys.exit(1)
    
    action = args[0]
    rest = args[1:]
    table = None
    force = False
    
    for arg in rest:
        if arg == "--force":
            force = True
        else:
            table = arg
    
    if table is not None and not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", table):
        console.print(f"[error]Invalid table name: {table!r}[/error]")
        return

    if action != "pull":
        console.print(f"[error]Unknown model action: {action}[/error]\n"
            "[suggestion]Use: fleting db model pull[/suggestion]")
        return
    
    console.print(f"[info]Running model pull | table={table} | force={force}[/info]")
    
    project_root = get_project_root()
    if not project_root:
        console.print("[error]No Fleting projects found.[/error]")
        return
    
    # =========================
    # DETECTAR ENGINE
    # =========================
    from configs.database import DATABASE
    engine = DATABASE.get("ENGINE", "sqlite").lower()
    console.print(f"[info]📌 Engine detected: {engine}[/info]")
    
    # =========================
    # REDIRECIONAR PARA ENGINE ESPECÍFICA
    # =========================
    if engine == "sqlite":
        from fleting.cli.commands.pull_sqlite import handle_pull_sqlite
        handle_pull_sqlite(project_root, table, force)
    
    elif engine == "mysql":
        from fleting.cli.commands.pull_mysql import handle_pull_mysql
        handle_pull_mysql(project_root, table, force)
    
    else:
        console.print(
            f"[error]❌ Engine '{engine}' not supported by pull command.[/error]\n"
            "[suggestion]Supported engines: sqlite, mysql[/suggestion]"
        )
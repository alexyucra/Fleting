# fleting/cli/commands/shell.py
from fleting.cli.console.console import console
from fleting.cli.helpers.project import get_project_root

def handle_shell():
    """Ponto de entrada - detecta engine e redireciona"""
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
        from fleting.cli.commands.shell_sqlite import handle_shell_sqlite
        handle_shell_sqlite(project_root)

    elif engine == "mysql":
        from fleting.cli.commands.shell_mysql import handle_shell_mysql
        handle_shell_mysql(project_root)

    else:
        console.print(
            f"[error]❌ Engine '{engine}' not supported by shell.[/error]\n"
            "[suggestion]Supported engines: sqlite, mysql[/suggestion]"
        )
# fleting/cli/commands/shell.py
from pathlib import Path
from fleting.cli.console.console import console


def is_fleting_project(path: Path) -> bool:
    return (path / ".fleting").exists()


def find_project_root(start=None) -> Path | None:
    if start is None:
        start = Path.cwd()
    elif isinstance(start, str):
        start = Path(start)

    start = start.resolve()

    if is_fleting_project(start):
        return start

    for parent in start.parents:
        if is_fleting_project(parent):
            return parent

    return None


def activate_project(root):
    import sys

    if isinstance(root, str):
        root = Path(root)

    root = root.resolve()

    if str(root) not in sys.path:
        sys.path.insert(0, str(root))


def get_project_root():
    root = find_project_root()
    if not root:
        console.print("❌ This directory is not a Fleting project.", style="error")
        console.print("👉 Go to the project root or a parent directory.", style="suggestion")
        return

    activate_project(root)
    return root


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
import code
from pathlib import Path
from fleting.cli.console.console import console
import importlib
import inspect
import sys
from rich.table import Table

class FletingPrompt:
    def __init__(self):
        self.counter = 0

    def __str__(self):
        self.counter += 1
        YELLOW = "\033[33m"
        GREEN = "\033[32m"
        RESET = "\033[0m"

        return f"{YELLOW}[{self.counter}] Fleting{GREEN} ❯_ {RESET}"

sys.ps1 = FletingPrompt()

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
    from pathlib import Path
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

def find_database(project_root: Path) -> Path | None:
    data_dir = project_root / "data"

    if not data_dir.exists():
        return None

    db_files = list(data_dir.glob("*.db"))
    return db_files[0] if db_files else None

def load_models(project_root: Path):
    models_dir = project_root / "models"
    loaded = {}

    if not models_dir.exists():
        return loaded

    for file in models_dir.glob("*.py"):
        if file.name.startswith("_"):
            continue

        module_name = f"models.{file.stem}"
        module = importlib.import_module(module_name)

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module_name:
                loaded[name] = obj

    return loaded

def handle_shell_sqlite():
    
    project_root = get_project_root()

    if not project_root:
        console.print("[error]No Fleting projects found.[/error]")
        return
    
    db_path = find_database(project_root)
    if not db_path:
        console.print(
            "[error]❌ No local databases found.[/error]\n"
            "[suggestion]👉 Execute: fleting db init & fleting migrate [/suggestion]"
        )
        return
    
    # =========================
    # Database
    # =========================
    from configs.database import DATABASE
    engine = DATABASE.get("ENGINE", "sqlite").lower()
    conn = None
    cursor = None
    
    if engine == "sqlite":
        console.print("[success]🟢 SQLite detected[/success]")
        try:
            from core.database import get_connection
            import sqlite3

            conn = get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
        except Exception as e:
            console.print(f"[error]Error obtaining connection: {e}[/error]")
            return
    else:
        console.print(
            f"[error]❌ Engine '{engine}' not supported by the shell.[/error]"
        )
        return
    
    # =========================
    # Helpers
    # =========================
    def tables():
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )
        return [row["name"] for row in cursor.fetchall()]

    def query(sql: str):
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def table_exists(cursor, table_name: str) -> bool:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        return cursor.fetchone() is not None
    
    def table_view(table_name: str):
        if not table_exists(cursor, table_name):
            console.print("[error]Table not found[/error]")
            return
        import re
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", table_name):
            console.print("[error]Invalid table name[/error]")
            return
        
        cursor.execute(f'SELECT * FROM "{table_name}"') 
        rows = cursor.fetchall()

        if not rows:
            console.print("[warning]Table exists but has no records[/warning]")
            return

        table = Table(title=f"📊 {table_name}")

        for col in rows[0].keys():
            table.add_column(col, style="cyan", no_wrap=True)

        for row in rows:
            table.add_row(*[str(v) for v in row])

        console.print(table)
    
    # =========================
    # Load models (REAL ORM)
    # =========================
    all_models_map = load_models(project_root)

    def models():
        return list(all_models_map.keys())

    banner = f"""
[bold cyan]Fleting Console[/bold cyan]
Project: [green]{project_root.name}[/green]
Database: [yellow]{db_path.name}[/yellow]

Available helpers:
• db/conn → SQLite connection
• cursor → SQLite cursor
• tables() → list tables
• query(sql) → execute SELECT
• models() → list models
• <Model>.all() → list records
• table("table_name") → execute SELECT FROM

Use quit() or Ctrl-Z plus Return to exit
"""

    console.print(banner)

    context = {
        "project_root": project_root,
        "Path": Path,
         # DB
        "db": conn,
        "conn": conn,
        "cursor": cursor,

        # Helpers
        "models": models,
        "tables": tables,
        "query": query,
        "table": table_view,
    }

    context.update(all_models_map)

    try:
        code.interact(banner="", local=context)
    except SystemExit:
        console.print("\n[info]👋 Leaving the Fleting Shell[/info]")


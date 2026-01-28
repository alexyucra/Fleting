import code
from pathlib import Path
from fleting.cli.console.console import console
import importlib
import inspect
from rich.table import Table

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

def handle_shell():
    
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
        
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        if not rows:
            console.print("[warning]Empty or non-existent table[/warning]")
            return

        table = Table(title=f"📊 {table_name}")

        for col in rows[0].keys():
            table.add_column(col, style="cyan", no_wrap=True)

        for row in rows:
            table.add_row(*[str(v) for v in row])

        console.print(table)
    
    def attach_orm(model, cursor):
        # regra 1: precisa declarar table
        if not hasattr(model, "table"):
            return False

        table = getattr(model, "table")

        # regra 2: tabela precisa existir
        if not table_exists(cursor, table):
            return False

        @classmethod
        def all(cls):
            cursor.execute(f"SELECT * FROM {table}")
            return [dict(row) for row in cursor.fetchall()]

        @classmethod
        def find(cls, id):
            cursor.execute(
                f"SELECT * FROM {table} WHERE id = ?", (id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None

        @classmethod
        def where(cls, **filters):
            keys = filters.keys()
            values = tuple(filters.values())
            conditions = " AND ".join(f"{k}=?" for k in keys)

            sql = f"SELECT * FROM {table} WHERE {conditions}"
            cursor.execute(sql, values)
            return [dict(row) for row in cursor.fetchall()]

        model.all = all
        model.find = find
        model.where = where

        return True
    
    def models():
        return list(persistent_models_map.keys())
    
    all_models_map = load_models(project_root)
    persistent_models_map = {}

    for name, model in all_models_map.items():
        if attach_orm(model, cursor):
            persistent_models_map[name] = model

    banner = f"""
[bold cyan]Fleting Console[/bold cyan]
Project: [green]{project_root.name}[/green]
Bank: [yellow]{db_path.name}[/yellow]

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

    context.update(persistent_models_map)

    try:
        code.interact(banner="", local=context)
    except SystemExit:
        console.print("\n[info]👋 Leaving the Fleting Shell[/info]")


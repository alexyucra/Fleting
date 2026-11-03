# fleting/cli/commands/shell_mysql.py
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


def load_models(project_root: Path):
    """Carrega os modelos do projeto"""
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


def handle_shell_mysql(project_root: Path):
    """Executa o shell para MySQL"""
    console.print("[success]🟢 MySQL detected[/success]")

    try:
        from core.database import get_connection
        conn = get_connection()
        cursor = conn.cursor()
    except Exception as e:
        console.print(f"[error]Error obtaining connection: {e}[/error]")
        return

    # =========================
    # Helpers MySQL
    # =========================
    def tables():
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = DATABASE()
            AND table_type = 'BASE TABLE'
        """)
        return [row[0] for row in cursor.fetchall()]

    def query(sql: str):
        cursor.execute(sql)
        rows = cursor.fetchall()
        # Converter para lista de dicionários
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    def table_exists(table_name: str) -> bool:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = DATABASE()
            AND table_name = %s
        """, (table_name,))
        return cursor.fetchone() is not None

    def table_view(table_name: str):
        if not table_exists(table_name):
            console.print("[error]Table not found[/error]")
            return

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        if not rows:
            console.print("[warning]Table exists but has no records[/warning]")
            return

        # Obter nomes das colunas
        columns = [desc[0] for desc in cursor.description]

        table = Table(title=f"📊 {table_name}")

        for col in columns:
            table.add_column(col, style="cyan", no_wrap=True)

        for row in rows:
            table.add_row(*[str(v) for v in row])

        console.print(table)

    # =========================
    # Load models
    # =========================
    all_models_map = load_models(project_root)

    def models():
        return list(all_models_map.keys())

    # Obter nome do database
    try:
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()[0]
    except:
        db_name = "unknown"

    banner = f"""
[bold cyan]Fleting Console (MySQL)[/bold cyan]
Project: [green]{project_root.name}[/green]
Database: [yellow]{db_name}[/yellow]

Available helpers:
• db/conn → MySQL connection
• cursor → MySQL cursor
• tables() → list tables
• query(sql) → execute SELECT
• models() → list models
• <Model>.all() → list records
• table("table_name") → show table data

Use quit() or Ctrl-Z plus Return to exit
"""

    console.print(banner)

    context = {
        "project_root": project_root,
        "Path": Path,
        "db": conn,
        "conn": conn,
        "cursor": cursor,
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
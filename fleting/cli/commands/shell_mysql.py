# fleting/cli/commands/shell_mysql.py
import code
import importlib
import inspect
import re
import sys
from pathlib import Path

from rich.table import Table
from fleting.cli.console.console import console

_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
ROW_LIMIT = 200


class FletingPrompt:
    def __init__(self, label="MySQL"):
        self.counter = 0
        self.label = label

    def __str__(self):
        self.counter += 1
        return f"\033[33m[{self.counter}] Fleting/{self.label}\033[32m ❯_ \033[0m"


def load_models(project_root: Path) -> dict:
    """Carrega classes de app/models/*.py."""
    models_dir = project_root / "app" / "models"
    loaded = {}
    if not models_dir.exists():
        return loaded

    for file in sorted(models_dir.glob("*.py")):
        if file.name.startswith("_"):
            continue
        module_name = f"app.models.{file.stem}"
        try:
            module = importlib.import_module(module_name)
        except Exception as e:
            console.print(f"[warning]⚠️  Could not load {module_name}: {e}[/warning]")
            continue
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module_name:
                loaded[name] = obj
    return loaded


def build_helpers(conn, driver: str):
    """Funções do shell, separadas para poder testar sem console interativo."""

    def _cursor():
        if driver == "pymysql":
            return conn.cursor()
        return conn.cursor(buffered=True)  # evita "Unread result found"

    def _run(sql, params=None):
        cur = _cursor()
        try:
            cur.execute(sql, params or ())
            if cur.description:
                cols = [d[0] for d in cur.description]
                return cols, cur.fetchall()
            conn.commit()
            return None, cur.rowcount
        finally:
            cur.close()

    def tables():
        _, rows = _run("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = DATABASE() AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """)
        return [r[0] for r in rows]

    def table_exists(name: str) -> bool:
        _, rows = _run("""
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = DATABASE() AND table_name = %s
        """, (name,))
        return bool(rows)

    def query(sql: str, params=None):
        """SELECT → lista de dicts; INSERT/UPDATE/DELETE → nº de linhas (com commit)."""
        cols, result = _run(sql, params)
        if cols is None:
            console.print(f"[success]✔ {result} row(s) affected[/success]")
            return result
        return [dict(zip(cols, r)) for r in result]

    def _print_table(title, cols, rows):
        t = Table(title=title)
        for c in cols:
            t.add_column(str(c), style="cyan", no_wrap=True)
        for r in rows:
            t.add_row(*["NULL" if v is None else str(v) for v in r])
        console.print(t)

    def describe(name: str):
        if not _IDENT.fullmatch(name) or not table_exists(name):
            console.print("[error]Table not found[/error]")
            return
        cols, rows = _run(f"DESCRIBE `{name}`")
        _print_table(f"🧱 {name}", cols, rows)

    def table_view(name: str, limit: int = ROW_LIMIT):
        if not _IDENT.fullmatch(name) or not table_exists(name):
            console.print("[error]Table not found[/error]")
            return
        cols, rows = _run(f"SELECT * FROM `{name}` LIMIT %s", (int(limit),))
        if not rows:
            console.print("[warning]Table exists but has no records[/warning]")
            return
        _print_table(f"📊 {name} (max {limit})", cols, rows)

    return {
        "_run": _run,
        "tables": tables,
        "table_exists": table_exists,
        "query": query,
        "describe": describe,
        "table": table_view,
    }


def handle_shell_mysql(project_root: Path):
    from configs.database import DATABASE
    driver = DATABASE.get("MYSQL", {}).get("DRIVER", "mysql-connector")

    try:
        from core.database import get_connection
        conn = get_connection()
    except Exception as e:
        console.print(f"[error]Error obtaining connection: {e}[/error]")
        console.print('[suggestion]👉 pip install "fleting[mysql]"  (ou "fleting[mariadb]")[/suggestion]')
        return

    h = build_helpers(conn, driver)
    all_models_map = load_models(project_root)

    def models():
        return list(all_models_map.keys())

    try:
        _, r = h["_run"]("SELECT DATABASE(), VERSION()")
        db_name, version = r[0]
    except Exception:
        db_name, version = "unknown", "?"
    flavor = "MariaDB" if "mariadb" in str(version).lower() else "MySQL"

    console.print(f"""
[bold cyan]Fleting Console ({flavor} {version})[/bold cyan]
Project: [green]{project_root.name}[/green]   Database: [yellow]{db_name}[/yellow]   Driver: [dim]{driver}[/dim]

Helpers:
• tables()                 → list tables
• describe("t")            → table structure
• table("t", limit=200)    → show rows
• query(sql, params=None)  → SELECT → dicts | DML → commit + rowcount
• models() / <Model>.all() → ORM
• conn                     → raw connection

Use quit() or Ctrl-Z + Enter (Windows) / Ctrl-D (Unix) to exit
""")

    context = {
        "project_root": project_root, "Path": Path,
        "db": conn, "conn": conn,
        "tables": h["tables"], "describe": h["describe"], "table": h["table"],
        "query": h["query"], "models": models,
    }
    context.update(all_models_map)

    old_ps1 = getattr(sys, "ps1", None)
    sys.ps1 = FletingPrompt(flavor)
    try:
        code.interact(banner="", local=context, exitmsg="")
    except SystemExit:
        pass
    finally:
        if old_ps1 is not None:
            sys.ps1 = old_ps1
        else:
            try:
                del sys.ps1
            except AttributeError:
                pass
        try:
            from core.database import close_connection
            close_connection()
        except Exception:
            try:
                conn.close()
            except Exception:
                pass
        console.print("\n[info]👋 Leaving the Fleting Shell[/info]")

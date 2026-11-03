from pathlib import Path
import sys
from fleting.cli.helpers.project import get_project_root

from rich.console import Console

console = Console()

def find_database(project_root: Path) -> Path | None:
    data_dir = project_root / "data"

    if not data_dir.exists():
        return None

    db_files = list(data_dir.glob("*.db"))
    return db_files[0] if db_files else None

def get_tables(cursor):
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
    """)
    return [row[0] for row in cursor.fetchall()]

def get_columns(cursor, table):
    cursor.execute(f"PRAGMA table_info({table})")
    return cursor.fetchall()

def get_foreign_keys(cursor, table: str):
    cursor.execute(f"PRAGMA foreign_key_list({table})")
    return cursor.fetchall()

def map_sqlite_type(sqlite_type: str) -> str:
    """Mapea tipos de SQLite a tipos de Python."""
    stype = sqlite_type.upper()
    if "INT" in stype:
        return "int"
    if "CHAR" in stype or "TEXT" in stype:
        return "str"
    if "FLOAT" in stype or "REAL" in stype or "NUMERIC" in stype:
        return "float"
    if "BLOB" in stype:
        return "bytes"
    return "Any" 

def generate_model(table, columns, foreign_keys, all_tables) -> str:

    class_name = "".join(word.capitalize() for word in table.split('_'))

    lines = [
        "from dataclasses import dataclass",
        "from typing import Any, Optional, ClassVar",
        "from core.base_model import BaseModel",
        "from core.orm import ForeignKey, HasMany",
        "",
        "@dataclass",
        f"class {class_name}Model(BaseModel):",
        f'    table_name: str = "{table}"',
        ""
    ]

    if not columns:
        lines.append("    pass")
    else:
        lines.append("    # columns")
        for col in columns:
            # _, name, col_type, notnull, default, pk = col
            _, name, col_type, *_ = col
            py_type = map_sqlite_type(col_type)
            lines.append(f"    {name}: Optional[{py_type}] = None")
        
        # ForeignKey relations
        if foreign_keys:
            lines.append("")
            lines.append("    # relations (ForeignKey)")

            for fk in foreign_keys:
                ref_table = fk[2]
                local_col = fk[3]
                remote_col = fk[4]

                attr = ref_table.rstrip("s")
                # Relations fora do __init__
                lines.append(
                    f'    {attr} = ForeignKey('
                    f'"{ref_table}", local="{local_col}", remote="{remote_col}")'
                )
        
        # HasMany (inverse relation)
        for other_table, fks in all_tables.items():
            for fk in fks:
                if fk[2] == table:
                    attr = other_table
                    lines.append(
                        f'    {attr} = HasMany('
                        f'"{other_table}", foreign_key="{fk[3]}")'
                    )

    return "\n".join(lines)

def save_model(project_root, table, content, force):
    import pathlib
    root = pathlib.Path(project_root).resolve()
    models_dir = root / "app" / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    
    path = models_dir / f"{table}_model.py"
    class_name = "".join(word.capitalize() for word in table.split('_'))

    default_pattern = f"""@dataclass
class {class_name}Model(BaseModel):
    table_name: str = "{table}"
"""

    if path.exists():
        current_content = path.read_text(encoding="utf-8").strip()
        
        normalized_current = "\n".join([line.strip() for line in current_content.splitlines() if line.strip()])
        normalized_default = "\n".join([line.strip() for line in default_pattern.splitlines() if line.strip()])

        if normalized_current != normalized_default and current_content != "":
            console.print(
                f"[warning]⚠️  Model {table}.py already contains custom logic. Ignored.[/warning]"
            )
            return
        else:
            console.print(f"[info]i Updating base model for: {table}.py[/info]")

    path.write_text(content, encoding="utf-8")
    console.print(f"[success]✔ Model generated in: [bold]{path.absolute()}[/bold][/success]")

def register_db_commands(subparsers):
    db_parser = subparsers.add_parser("db")

    db_sub = db_parser.add_subparsers(dest="db_command")

    model_parser = db_sub.add_parser("model")
    model_sub = model_parser.add_subparsers(dest="model_command")

    pull_parser = model_sub.add_parser("pull")
    pull_parser.add_argument("--table", help="Pull apenas uma tabela")
    pull_parser.add_argument(
        "--force",
        action="store_true",
        help="Overscrew existing models"
    )

def handle_pull_sqlite(args: list[str]):
    if not args:
        print("Error: No se proporcionaron argumentos.")
        sys.exit(1)
    
    action = args[0]          # pull
    rest = args[1:]           # users, --force
    table = None
    force = False
    for arg in rest:
        if arg == "--force":
            force = True
        else:
            table = arg
    if action == "pull":
        console.print(f"[info]Running model pull | table={table} | force={force}[/info]")
        
        project_root = get_project_root()

        if not project_root:
            console.print("[error]No Fleting projects found.[/error]")
            return
        
        db_path = find_database(project_root)
        if not db_path:
            console.print(
                "[error]❌ No local databases found.[/error]\n"
                "[suggestion]👉 Execute: fleting db init & fleting db migrate [/suggestion]"
            )
            return
        
        from core.table_filters import should_generate_model
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
        
        console.print("[info]🔍 Starting the introspection of the SQLite bank[/info]")

        excluded = DATABASE.get("MODEL_PULL", {}).get("EXCLUDE_TABLES", [])
        
        tables = [table] if table else get_tables(cursor)

        foreign_key_map = {}

        for tbl in tables:
            foreign_key_map[tbl] = get_foreign_keys(cursor, tbl)

        for tbl in tables:
            if not should_generate_model(tbl, excluded):
                console.print(f"[yellow]⏭ Skipping table {tbl}[/yellow]")
                continue
                    
            columns = get_columns(cursor, tbl)
            foreign_keys = foreign_key_map.get(tbl, [])

            if not columns:
                continue

            code = generate_model(
                tbl,
                columns,
                foreign_keys,
                foreign_key_map
            )

            save_model(project_root, tbl, code, force)

        console.print("[success]🎉 Models with relationships generated successfully[/success]")

    else:
        console.print( f"[error]Unknown model action: {action}[/error]\n"
            "[suggestion]Use: fleting db model pull[/suggestion]"
        )


    
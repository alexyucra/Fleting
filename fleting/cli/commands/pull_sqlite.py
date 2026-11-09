from pathlib import Path

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
    cursor.execute("SELECT * FROM pragma_table_info(?)", (table,))
    return cursor.fetchall()

def get_foreign_keys(cursor, table: str):
    cursor.execute("SELECT * FROM pragma_foreign_key_list(?)", (table,))
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

def handle_pull_sqlite(project_root: Path, table: str | None = None, force: bool = False):
    db_path = find_database(project_root)
    if not db_path:
        console.print(
            "[red]❌ No local databases found.[/red]\n"
            "👉 Execute: fleting db init & fleting db migrate"
        )
        return

    from core.table_filters import should_generate_model
    from configs.database import DATABASE
    from core.database import get_connection
    import sqlite3

    try:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
    except Exception as e:
        console.print(f"[red]Error obtaining connection: {e}[/red]")
        return

    console.print("🔍 Starting the introspection of the SQLite database")

    excluded = DATABASE.get("MODEL_PULL", {}).get("EXCLUDE_TABLES", [])
    tables = [table] if table else get_tables(cursor)

    foreign_key_map = {tbl: get_foreign_keys(cursor, tbl) for tbl in tables}

    for tbl in tables:
        if not should_generate_model(tbl, excluded):
            console.print(f"[yellow]⏭ Skipping table {tbl}[/yellow]")
            continue

        columns = get_columns(cursor, tbl)
        if not columns:
            continue

        code = generate_model(tbl, columns, foreign_key_map.get(tbl, []), foreign_key_map)
        save_model(project_root, tbl, code, force)

    console.print("[green]🎉 Models with relationships generated successfully[/green]")

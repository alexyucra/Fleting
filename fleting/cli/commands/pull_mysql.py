# fleting/cli/commands/pull_mysql.py
from pathlib import Path
from fleting.cli.console.console import console


def get_tables(cursor):
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = DATABASE()
        AND table_type = 'BASE TABLE'
    """)
    return [row[0] for row in cursor.fetchall()]


def get_columns(cursor, table):
    cursor.execute("""
        SELECT 
            column_name,
            data_type,
            is_nullable,
            column_key,
            column_default,
            extra
        FROM information_schema.columns 
        WHERE table_schema = DATABASE()
        AND table_name = %s
        ORDER BY ordinal_position
    """, (table,))
    return cursor.fetchall()


def get_foreign_keys(cursor, table: str):
    cursor.execute("""
        SELECT 
            kcu.column_name,
            kcu.referenced_table_name,
            kcu.referenced_column_name,
            kcu.constraint_name
        FROM information_schema.key_column_usage kcu
        WHERE kcu.referenced_table_schema = DATABASE()
        AND kcu.table_schema = DATABASE()
        AND kcu.table_name = %s
        AND kcu.referenced_column_name IS NOT NULL
    """, (table,))
    return cursor.fetchall()


def map_type(mysql_type: str) -> str:
    """Mapeia tipos de MySQL para Python"""
    stype = mysql_type.upper()
    if "INT" in stype or "TINYINT" in stype or "SMALLINT" in stype or "MEDIUMINT" in stype or "BIGINT" in stype:
        return "int"
    if "VARCHAR" in stype or "CHAR" in stype or "TEXT" in stype or "ENUM" in stype or "SET" in stype:
        return "str"
    if "FLOAT" in stype or "DOUBLE" in stype or "DECIMAL" in stype or "NUMERIC" in stype:
        return "float"
    if "DATE" in stype or "TIME" in stype or "DATETIME" in stype or "TIMESTAMP" in stype:
        return "str"
    if "BLOB" in stype or "BINARY" in stype or "VARBINARY" in stype:
        return "bytes"
    if "JSON" in stype:
        return "dict"
    return "Any"


def generate_model(table, columns, foreign_keys, all_tables) -> str:
    """Gera modelo para MySQL"""
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
            name = col[0]
            col_type = col[1]
            py_type = map_type(col_type)
            lines.append(f"    {name}: Optional[{py_type}] = None")
        
        if foreign_keys:
            lines.append("")
            lines.append("    # relations (ForeignKey)")
            for fk in foreign_keys:
                local_col = fk[0]
                ref_table = fk[1]
                remote_col = fk[2]
                attr = ref_table.rstrip("s")
                lines.append(
                    f'    {attr} = ForeignKey('
                    f'"{ref_table}", local="{local_col}", remote="{remote_col}")'
                )
        
        for other_table, fks in all_tables.items():
            for fk in fks:
                if fk[1] == table:
                    attr = other_table
                    lines.append(
                        f'    {attr} = HasMany('
                        f'"{other_table}", foreign_key="{fk[0]}")'
                    )

    return "\n".join(lines)


def save_model(project_root, table, content, force):
    """Salva o modelo gerado"""
    import pathlib
    root = pathlib.Path(project_root).resolve()
    models_dir = root / "app" /"models"
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


def handle_pull_mysql(project_root: Path, table: str | None = None, force: bool = False):
    """Executa pull para MySQL"""
    from core.table_filters import should_generate_model
    from configs.database import DATABASE

    console.print("[success]🟢 MySQL detected[/success]")
    
    try:
        from core.database import get_connection
        conn = get_connection()
        cursor = conn.cursor()
    except Exception as e:
        console.print(f"[error]Error obtaining connection: {e}[/error]")
        return
    
    try:
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()[0]
        console.print(f"[info]📊 Database: {db_name}[/info]")
    except Exception as e:
        console.print(f"[error]Error connecting to database: {e}[/error]")
        return
    
    console.print("[info]🔍 Starting introspection of MySQL database[/info]")

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

        code = generate_model(tbl, columns, foreign_keys, foreign_key_map)
        save_model(project_root, tbl, code, force)

    console.print("[success]🎉 MySQL models generated successfully[/success]")
# fleting/cli/templates/database_mysql.py
import importlib.util
from pathlib import Path
from fleting.cli.console.console import console
import datetime

def check_mysql_dependency() -> bool:
    """Verifica se o mysql-connector-python está instalado"""
    try:
        import mysql.connector  # noqa: F401
        return True
    except ImportError:
        console.print("\n[bold red]❌ MySQL connector not installed[/bold red]")
        console.print("\n[yellow]To use MySQL with Fleting, you need to install:[/yellow]")
        console.print("[bold cyan]pip install mysql-connector-python[/bold cyan]\n")
        return False

def handle_mysql_error(e: Exception):
    """Trata erros de conexão MySQL de forma amigável"""
    error_msg = str(e)
    
    # Erro 2003 - Não consegue conectar ao servidor
    if "2003" in error_msg or "Can't connect" in error_msg:
        console.print("\n[bold red]❌ Could not connect to MySQL server[/bold red]")
        console.print("\n[yellow]Please check:[/yellow]")
        console.print("  1. [cyan]Is MySQL running?[/cyan]")
        console.print("     docker ps | findstr mysql")
        console.print("     docker start mysql-local")
        console.print("\n  2. [cyan]Is the port correct?[/cyan]")
        console.print("     docker port mysql-local")
        console.print("     Check PORT in configs/database.py")
        console.print("\n  3. [cyan]Are the credentials correct?[/cyan]")
        console.print("     Check USER, PASSWORD, NAME in configs/database.py")
        console.print("\n  4. [cyan]Is the database created?[/cyan]")
        console.print("     docker exec -it mysql-local mysql -uroot -p -e 'CREATE DATABASE IF NOT EXISTS fleting'")
        return True
    
    # Erro 1045 - Acesso negado (senha incorreta)
    elif "1045" in error_msg or "Access denied" in error_msg:
        console.print("\n[bold red]❌ Access denied to MySQL server[/bold red]")
        console.print("\n[yellow]Please check your credentials in configs/database.py:[/yellow]")
        console.print("  - USER")
        console.print("  - PASSWORD")
        console.print("\n[cyan]To reset MySQL password:[/cyan]")
        console.print("  docker exec -it mysql-local mysql -uroot -p")
        console.print("  ALTER USER 'root'@'%' IDENTIFIED BY 'new_password';")
        console.print("  FLUSH PRIVILEGES;")
        return True
    
    # Erro 1049 - Banco de dados não existe
    elif "1049" in error_msg or "Unknown database" in error_msg:
        console.print("\n[bold red]❌ Database does not exist[/bold red]")
        console.print("\n[yellow]Create the database:[/yellow]")
        console.print("[cyan]docker exec -it mysql-local mysql -uroot -p -e 'CREATE DATABASE IF NOT EXISTS fleting'[/cyan]")
        console.print("\n[dim]Or check NAME in configs/database.py[/dim]")
        return True
    
    # Erro 1044 - Sem permissão para acessar o banco
    elif "1044" in error_msg or "Access denied for user" in error_msg:
        console.print("\n[bold red]❌ User does not have permission to access the database[/bold red]")
        console.print("\n[yellow]Check:[/yellow]")
        console.print("  1. USER in configs/database.py")
        console.print("  2. Database name in configs/database.py")
        console.print("  3. User permissions in MySQL")
        return True
    
    # Outros erros
    else:
        console.print(f"\n[bold red]❌ MySQL Error: {error_msg}[/bold red]")
        console.print("\n[yellow]Please check your MySQL configuration in configs/database.py[/yellow]")
        return True

def db_init(project_root: Path, engine: str = "mysql"):
    """Initialize database structure with MySQL templates"""
    BASE = project_root

    # =========================
    # UTIL
    # =========================
    def create_file(path, content=""):
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(content, encoding="utf-8")

    # =========================
    # ESTRUTURA DE PASTAS
    # =========================
    folders = [
        "migrations",
        "seeds",
        # "data",  # MySQL não usa arquivo físico
    ]

    for folder in folders:
        (BASE / folder).mkdir(parents=True, exist_ok=True)

    init_file = BASE / "migrations" / "__init__.py"
    if not init_file.exists():
        init_file.write_text("", encoding="utf-8")

    create_file(BASE / "migrations/001_initial.py", """
# Migration MySQL
def up(db):
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE,
            password VARCHAR(255)
        )
    ''')
    db.commit()

def down(db):
    cursor = db.cursor()
    cursor.execute('''
        DROP TABLE IF EXISTS users
    ''')
    db.commit()
""")
    print(f"✅ migrations/001_initial.py successfully created")

    create_file(BASE / "seeds/initial.py", """
# Seed MySQL
def run(db):
    cursor = db.cursor()
    cursor.execute('''
        INSERT IGNORE INTO users (username, password)
        VALUES VALUES (%s, %s), ("admin", hash_password(raw)),
    ''')
    db.commit()
""")
    print(f"✅ seeds/initial.py successfully created")

    create_file(BASE / "core/migrations.py", """
# Core migrations MySQL
from pathlib import Path
from core.database import get_connection, placeholder, dict_cursor

MIGRATIONS_TABLE = "_fleting_migrations"

def ensure_migrations_table():
    db = get_connection()
    cur = db.cursor()
    try:
        cur.execute(f'''
            CREATE TABLE IF NOT EXISTS {MIGRATIONS_TABLE} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) UNIQUE
            )
        ''')
        db.commit()
    finally:
        cur.close()

def applied_migrations():
    db = get_connection()
    cur = dict_cursor(db)
    try:
        ensure_migrations_table()
        cur.execute(
            f"SELECT name FROM {MIGRATIONS_TABLE} ORDER BY id"
        )
        rows = cur.fetchall()
    finally:
        cur.close()
    return [r["name"] for r in rows]

def apply_migration(name, up):
    db = get_connection()
    up(db)
    cur = db.cursor()
    try:
        cur.execute(
            f"INSERT INTO {MIGRATIONS_TABLE} (name) VALUES ({placeholder()})",
            (name,),
        )
        db.commit()
    finally:
        cur.close()

def rollback_migration(name, down):
    db = get_connection()
    down(db)
    cur = db.cursor()
    try:
        cur.execute(
            f"DELETE FROM {MIGRATIONS_TABLE} WHERE name = {placeholder()}",
            (name,),
        )
        db.commit()
    finally:
        cur.close()

""")

    print("✅ Database structure initialized with MySQL")

def db_migrate(root: Path):
    if not check_mysql_dependency():
        return
    
    try:
        import mysql.connector
    except ImportError:
        from fleting.cli.console.console import console
        console.print("\n[bold red]❌ MySQL connector not installed[/bold red]")
        console.print("\n[yellow]To use MySQL with Fleting, you need to install:[/yellow]")
        console.print("[bold cyan]pip install mysql-connector-python[/bold cyan]\n")
        console.print("[dim]Or if you prefer: pip install pymysql (requires code changes)[/dim]")
        return

    try:
        from core.migrations import applied_migrations, apply_migration
    except ImportError as e:
        from fleting.cli.console.console import console
        console.print(f"[red]❌ Error importing migrations: {e}[/red]")
        console.print("[yellow]👉 Run `fleting db init` first to create migration structure.[/yellow]")
        return

    migrations_dir = root / "migrations"

    if not migrations_dir.exists():
        print("❌ Run `fleting db init` first.")
        return

    applied = applied_migrations()

    files = sorted(migrations_dir.glob("*.py"))
    files = [f for f in files if f.name != "__init__.py"]

    if not files:
        print("⚠️ No migrations found.")
        return

    for file in files:
        if file.name in applied:
            continue

        spec = importlib.util.spec_from_file_location(file.stem, file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        if not hasattr(mod, "up"):
            print(f"❌ Migration {file.name} missing up()")
            continue

        apply_migration(file.name, mod.up)
        print(f"✅ Applied migration {file.name}")

def db_seed(root: Path):
    seeds_dir = root / "seeds"

    if not seeds_dir.exists():
        print("❌ No seeds directory.")
        return

    from core.database import get_connection
    db = get_connection()

    for file in sorted(seeds_dir.glob("*.py")):
        spec = importlib.util.spec_from_file_location(file.stem, file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        if hasattr(mod, "run"):
            mod.run(db)
            print(f"🌱 Seed executed: {file.name}")

    db.commit()

def make_migration(root: Path, name: str):
    migrations_dir = root / "migrations"
    migrations_dir.mkdir(exist_ok=True)

    existing = sorted(migrations_dir.glob("*.py"))
    nums = [
        int(f.name.split("_")[0])
        for f in existing
        if f.name[0:3].isdigit()
    ]
    next_num = max(nums, default=0) + 1

    filename = f"{next_num:03d}_{name}.py"
    path = migrations_dir / filename

    template = f'''"""
Migration: {name}
Created at: {datetime.datetime.now().isoformat()}
"""

def up(db):
    db.execute(\'\'\'
        CREATE TABLE IF NOT EXISTS exemplo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255)
        )
    \'\'\')
    pass

def down(db):
    # db.execute('DROP TABLE IF EXISTS exemplo')
    pass
'''

    path.write_text(template, encoding="utf-8")
    print(f"✅ Migration created: {filename}")

def db_rollback(root):
    from core.migrations import applied_migrations, rollback_migration

    migrations_dir = root / "migrations"
    applied = applied_migrations()

    if not applied:
        print("⚠️ No migrations to rollback.")
        return

    last = applied[-1]
    file = migrations_dir / last

    if not file.exists():
        print(f"❌ Migration file not found: {last}")
        return

    spec = importlib.util.spec_from_file_location(file.stem, file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    if not hasattr(mod, "down"):
        print(f"❌ Migration {last} has no down()")
        return

    rollback_migration(last, mod.down)
    print(f"↩️ Rolled back migration {last}")

def db_status(root):
    from core.migrations import applied_migrations

    migrations_dir = root / "migrations"

    if not migrations_dir.exists():
        print("❌ No migrations directory. Run `fleting db init` first.")
        return

    applied = applied_migrations()
    files = sorted(
        f.name for f in migrations_dir.glob("*.py")
        if f.name != "__init__.py"
    )

    applied_set = set(applied)
    files_set = set(files)

    pending = sorted(files_set - applied_set)
    missing = sorted(applied_set - files_set)

    print("\n📦 Database status\n")

    if applied:
        print("Applied migrations:")
        for name in applied:
            print(f"  ✔ {name}")
    else:
        print("Applied migrations:")
        print("  (none)")

    print()

    if pending:
        print("Pending migrations:")
        for name in pending:
            print(f"  ⏳ {name}")
    else:
        print("Pending migrations:")
        print("  (none)")

    if missing:
        print("\n⚠️ Inconsistencies detected:")
        for name in missing:
            print(f"  ❌ Applied but file missing: {name}")

    if not pending and not missing:
        print("\n✅ Database is up to date.")
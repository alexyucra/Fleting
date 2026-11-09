import importlib.util
from pathlib import Path
import datetime
from fleting.cli.templates.defaults import INITIAL_MIGRATION, INITIAL_SEED

# def db_init(project_root: Path):
def db_init(project_root: Path, engine: str = "sqlite"):

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
        "data",
    ]

    for folder in folders:
        (BASE / folder).mkdir(parents=True, exist_ok=True)

    init_file = BASE / "migrations" / "__init__.py"
    if not init_file.exists():
        init_file.write_text("", encoding="utf-8")

    create_file(BASE / "migrations/001_initial.py", INITIAL_MIGRATION)
    print(f"✅ migrations/001_initial.py successfully created")
    
    create_file(BASE / "seeds/initial.py", INITIAL_SEED)
    print(f"✅ seeds/initial.py successfully created")

    create_file(BASE / "core/migrations.py", """
# Core migrations SQLite
from pathlib import Path
from core.database import get_connection

MIGRATIONS_TABLE = "_fleting_migrations"

def ensure_migrations_table():
    db = get_connection()
    db.execute(f'''
        CREATE TABLE IF NOT EXISTS {MIGRATIONS_TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')
    db.commit()

def applied_migrations():
    db = get_connection()
    ensure_migrations_table()
    rows = db.execute(
        f"SELECT name FROM {MIGRATIONS_TABLE} ORDER BY id"
    ).fetchall()
    return [r[0] for r in rows]

def apply_migration(name, up):
    db = get_connection()
    up(db)
    db.execute(
        f"INSERT INTO {MIGRATIONS_TABLE} (name) VALUES (?)",
        (name,)
    )
    db.commit()

def rollback_migration(name, down):
    db = get_connection()
    down(db)
    db.execute(
        f"DELETE FROM {MIGRATIONS_TABLE} WHERE name = ?",
        (name,)
    )
    db.commit()
""")
     
    print("✅ Database structure initialized")

def db_migrate(root: Path):
    from core.migrations import applied_migrations, apply_migration

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
    # write your SQL here
    pass

def down(db):
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

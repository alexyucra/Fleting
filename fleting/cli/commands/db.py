from pathlib import Path
# from fleting.cli.templates.database import db_init, db_migrate, db_seed, make_migration, db_rollback, db_status
from fleting.cli.commands.pull import handle_pull
from fleting.cli.console.console import console
from fleting.cli.helpers.project import get_project_root

def handle_db(args):
    if not args:
        console.print("Use: fleting db <init|migrate|seed|make|rollback|status>", style="suggestion")
        return

    root = get_project_root()
    if not root:
        return

    force_mysql = "--mysql" in args
    force_sqlite = "--sqlite" in args
    args = [a for a in args if a not in ("--mysql", "--sqlite")]
    if not args:
        console.print("Use: fleting db <init|migrate|seed|make|rollback|status>", style="suggestion")
        return
    cmd = args[0]

    engine = get_engine_from_config(root)
    if cmd == "init" and (force_mysql or force_sqlite):
        new_engine = "mysql" if force_mysql else "sqlite"
        if new_engine != engine:
            update_database_engine(root, new_engine)
            regenerate_core_database(root, new_engine)
            console.print(f"Engine switched: {engine} → {new_engine}", style="success")
        engine = new_engine

    if engine == "mysql":
        from fleting.cli.templates.database_mysql import db_init, db_migrate, db_seed, make_migration, db_rollback, db_status
    else:
        from fleting.cli.templates.database import db_init, db_migrate, db_seed, make_migration, db_rollback, db_status

    if cmd == "init":
        db_init(root, engine)

    elif cmd == "migrate":
        db_migrate(root)

    elif cmd == "seed":
        db_seed(root)
        
    elif cmd == "make":
        if len(args) < 2:
            console.print("Use: fleting db make <name>\n", style="suggestion")
            return
        make_migration(root, args[1])
    elif cmd == "rollback":
        db_rollback(root)
    elif cmd == "status":
        db_status(root)
    elif cmd == "model":
        handle_pull(args[1:])
    else:
        console.print(f"Unknown db command: {cmd}", style="warning")

def get_engine_from_config(project_root: Path) -> str:
    """Lê a engine do arquivo configs/database.py"""

    db_config_path = project_root / "configs" / "database.py"
    
    if not db_config_path.exists():
        console.print("❌ configs/database.py not found", style="error")
        console.print("👉 Run fleting init first", style="suggestion")
        return "sqlite"  # fallback
    
    try:
        # Ler o arquivo e extrair a engine
        content = db_config_path.read_text(encoding="utf-8")
        
        # Procurar por "ENGINE": "mysql" ou "ENGINE": "sqlite"
        import re
        match = re.search(r'"ENGINE":\s*"([^"]+)"', content)
        if match:
            engine = match.group(1).lower()
            if engine in ["sqlite", "mysql"]:
                return engine
        
        # Fallback para sqlite
        return "sqlite"
    except Exception as e:
        console.print(f"⚠️  Error reading config: {e}", style="warning")
        return "sqlite"

def update_database_engine(project_root: Path, engine: str) -> bool:
    """Atualiza a engine no arquivo configs/database.py"""
    db_config_path = project_root / "configs" / "database.py"
    
    if not db_config_path.exists():
        console.print("❌ configs/database.py not found", style="error")
        return False
    
    content = db_config_path.read_text(encoding="utf-8")
    
    import re
    pattern = r'("ENGINE":\s*")[^"]*(")'
    
    if re.search(pattern, content):
        new_content = re.sub(pattern, f'"ENGINE": "{engine}"', content)
        db_config_path.write_text(new_content, encoding="utf-8")
        return True
    else:
        console.print("⚠️  Could not find ENGINE setting in database.py", style="warning")
        return False


def regenerate_core_database(root: Path, engine: str):
    """Recria core/database.py e core/migrations.py para a engine escolhida (com backup .bak)."""
    for rel in ("core/database.py", "core/migrations.py"):
        f = root / rel
        if f.exists():
            bak = f.with_suffix(".py.bak")
            if bak.exists():
                bak.unlink()
            f.rename(bak)
            console.print(f"Backup: {rel} → {bak.name}", style="info")

    # migration/seed padrão de versões antigas eram específicos de uma engine
    from fleting.cli.templates.defaults import DEFAULT_FILES, ENGINE_AGNOSTIC_MARKER
    for rel in DEFAULT_FILES:
        f = root / rel
        if f.exists() and ENGINE_AGNOSTIC_MARKER not in f.read_text(encoding="utf-8"):
            bak = f.with_suffix(".py.bak")
            if bak.exists():
                bak.unlink()
            f.rename(bak)
            console.print(f"Backup: {rel} → {bak.name} (engine-specific; regenerated)", style="warning")

    from fleting.cli.templates.index import write_core_database
    write_core_database(root, engine, overwrite=True)

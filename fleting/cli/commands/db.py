from pathlib import Path
# from fleting.cli.templates.database import db_init, db_migrate, db_seed, make_migration, db_rollback, db_status
from fleting.cli.commands.pull import handle_pull
from fleting.cli.console.console import console
from fleting.cli.helpers.project import get_project_root

# def is_fleting_project(path: Path) -> bool:
#     return (path / ".fleting").exists()

# def find_project_root(start=None) -> Path | None:
#     if start is None:
#         start = Path.cwd()
#     elif isinstance(start, str):
#         start = Path(start)

#     start = start.resolve()

#     if is_fleting_project(start):
#         return start

#     for parent in start.parents:
#         if is_fleting_project(parent):
#             return parent

#     return None

# def activate_project(root):
#     from pathlib import Path
#     import sys

#     if isinstance(root, str):
#         root = Path(root)

#     root = root.resolve()

#     if str(root) not in sys.path:
#         sys.path.insert(0, str(root))

# def get_project_root():
#     root = find_project_root()
#     if not root:
#         console.print("❌ This directory is not a Fleting project.", style="error")
#         console.print("👉 Go to the project root or a parent directory.", style="suggestion")
#         return

#     activate_project(root)
#     return root

def handle_db(args):
    if not args:
        console.print("Use: fleting db <init|migrate|seed|make|rollback|status>", style="suggestion")
        return

    root = get_project_root()
    if not root:
        return

    cmd = args[0]
    # get init engine
    engine = get_engine_from_config(root)
    print(engine)
    if engine == "mysql":
        from fleting.cli.templates.database_mysql import db_init, db_migrate, db_seed, make_migration, db_rollback, db_status
    else:
        from fleting.cli.templates.database import db_init, db_migrate, db_seed, make_migration, db_rollback, db_status

    # send update engine
    force_mysql = "--mysql" in args
    force_sqlite = "--sqlite" in args
    clean_args = [arg for arg in args if arg not in ["--mysql", "--sqlite"]]


    if cmd == "init":
        if force_mysql:
            new_engine = "mysql"
            db_init(root, new_engine)
        elif force_sqlite:
            new_engine = "sqlite"
            db_init(root, new_engine)
        else:
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


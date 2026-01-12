from pathlib import Path
import importlib.util
from fleting.cli.templates.database import db_init, db_migrate, db_seed, make_migration, db_rollback, db_status
# from fleting.cli.helpers.project import get_project_root

def get_project_root() -> Path:
    return Path.cwd()

def is_fleting_project(path: Path):
    return (path / "main.py").exists()

def handle_db(args):
    if not args:
        print("Use: fleting db <init|migrate|seed>")
        return

    root = get_project_root()

    if not is_fleting_project(root):
        print("❌ Not a Fleting project.")
        return

    cmd = args[0]

    if cmd == "init":
        db_init(root)
    elif cmd == "migrate":
        db_migrate(root)
    elif cmd == "seed":
        db_seed(root)
    elif cmd == "make":
        if len(args) < 2:
            print("Use: fleting db make <name>\n")
            return
        make_migration(root, args[1])
    elif cmd == "rollback":
        db_rollback(root)
    elif cmd == "status":
        db_status(root)
    else:
        print(f"Unknown db command: {cmd}")



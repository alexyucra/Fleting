from pathlib import Path
from fleting.cli.templates.database import db_init, db_migrate, db_seed, make_migration, db_rollback, db_status
from .rich_console import console

def is_fleting_project(path: Path) -> bool:
    return (path / ".fleting").exists()

def find_project_root(start=None) -> Path | None:
    if start is None:
        start = Path.cwd()
    elif isinstance(start, str):
        start = Path(start)

    start = start.resolve()

    if is_fleting_project(start):
        return start

    for parent in start.parents:
        if is_fleting_project(parent):
            return parent

    return None

def activate_project(root):
    from pathlib import Path
    import sys

    if isinstance(root, str):
        root = Path(root)

    root = root.resolve()

    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

def get_project_root():
    root = find_project_root()
    if not root:
        console.print("❌ This directory is not a Fleting project.", style="error")
        console.print("👉 Go to the project root or a parent directory.", style="suggestion")
        return

    activate_project(root)
    return root

def handle_db(args):
    if not args:
        console.print("Use: fleting db <init|migrate|seed|make|rollback|status>", style="suggestion")
        return

    root = get_project_root()
    if not root:
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
            console.print("Use: fleting db make <name>\n", style="suggestion")
            return
        make_migration(root, args[1])
    elif cmd == "rollback":
        db_rollback(root)
    elif cmd == "status":
        db_status(root)
    else:
        console.print(f"Unknown db command: {cmd}", style="warning")



from pathlib import Path
import sys

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
        print("❌ This directory is not a Fleting project.")
        print("👉 Go to the project root or a parent directory.")
        return

    activate_project(root)
    return root
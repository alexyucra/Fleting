from pathlib import Path
from fleting.cli.templates.index import init_project

def handle_init(args=None):
    args = args or []
    cwd = Path.cwd()

    if not args:
        project_root = cwd
    else:
        name = args[0]
        project_root = cwd if name == "." else cwd / name
        project_root.mkdir(parents=True, exist_ok=True)

    init_project(project_root)
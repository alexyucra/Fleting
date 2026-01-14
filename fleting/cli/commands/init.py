from pathlib import Path
from fleting.cli.templates.index import init_project
from .rich_console import console

DEFAULT_PROJECT_NAME = "app"
DEFAULT_APP_NAME = "Fleting"

def handle_init(args=None):
    args = args or []
    cwd = Path.cwd()

    if not args:
        project_root = cwd / DEFAULT_PROJECT_NAME
        project_name = DEFAULT_APP_NAME
        project_root.mkdir(parents=True, exist_ok=True)

    elif args[0] == ".":
        project_root = cwd
        project_name = DEFAULT_APP_NAME

    else:
        project_root = cwd / args[0]
        project_name = args[0].replace("_", " ").title()
        project_root.mkdir(parents=True, exist_ok=True)

    init_project(project_root, project_name)
    console.print("✅ Project Fleting successfully initiated!", style="success")
from pathlib import Path
import re
from fleting.cli.console.console import console
from fleting.cli.helpers.project import get_project_root

def handle_delete(args):
    if len(args) < 2:
        console.print("Uso: fleting delete <controller|view|model|page> <nome>", style="suggestion")
        return

    root = get_project_root()
    if not root:
        return

    kind, name = args[0], args[1].lower()

    try:
        if kind == "view":
            delete_view(root, name)

        elif kind == "controller":
            delete_controller(root, name)

        elif kind == "model":
            delete_model(root, name)

        elif kind == "page":
            delete_page(root, name)

        else:
            console.print(f"Unsupported Type: {kind}", style="warning")

    except Exception:
        console.print(f"Error when deleting {kind} {name}", style="error")

# -----------------
# delete controller
# -----------------
def delete_controller(root: Path, name: str):
    path = root / "app/controllers" / f"{name}_controller.py"

    if not path.exists():
        console.print(f"Controller '{name}' does not exist.", style="warning")
        return

    path.unlink()
    console.print(f"Controller successfully removed: {name}", style="success")

# -----------------
# delete view
# -----------------
def delete_view(root: Path, name: str):
    path = root / "app/views" / "pages" / f"{name}_view.py"

    if not path.exists():
        console.print(f"View '{name}' does not exist.", style="warning")
        return

    path.unlink()
    console.print(f"View successfully removed: {name}", style="success")

# -----------------
# delete model
# -----------------
def delete_model(root: Path, name: str):
    path = root / "app/models" / f"{name}_model.py"

    if not path.exists():
        console.print(f"Model '{name}' does not exist.", style="warning")
        return

    path.unlink()
    console.print(f"Model successfully removed: {name}", style="success")

# -----------------
# unregister route
# -----------------
def unregister_route(root: Path, name: str):
    routes_file = root / "configs" / "routes.py"
    if not routes_file.exists():
        return
    content = routes_file.read_text(encoding="utf-8")
    pattern = re.compile(
        r'\n\s*\{\s*\n\s*"path":\s*"/' + re.escape(name) + r'".*?\},\n',
        re.DOTALL,
    )
    new_content, n = pattern.subn("\n", content, count=1)
    if n:
        routes_file.write_text(new_content, encoding="utf-8")
        console.print(f"Route '/{name}' removed", style="success")

# -----------------
# delete page
# -----------------
def delete_page(root: Path, name: str):
    delete_view(root, name)
    delete_controller(root, name)
    delete_model(root, name)
    unregister_route(root, name)

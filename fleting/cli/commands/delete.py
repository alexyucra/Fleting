from pathlib import Path
from .rich_console import console

BASE = Path.cwd()

def handle_delete(args):
    if len(args) < 2:
        console.print("Uso: fleting delete <controller|view|model|page> <nome>", style="suggestion")
        return

    kind, name = args[0], args[1].lower()

    try:
        if kind == "view":
            delete_view(name)

        elif kind == "controller":
            delete_controller(name)

        elif kind == "model":
            delete_model(name)

        elif kind == "page":
            delete_page(name)

        else:
            console.print(f"Unsupported Type: {kind}", style="warning")

    except Exception:
        console.print(f"Error when deleting {kind} {name}", style="error")

# -----------------
# delete controller
# -----------------
def delete_controller(name: str):
    path = BASE / "controllers" / f"{name}_controller.py"

    if not path.exists():
        console.print(f"Controller '{name}' does not exist.", style="warning")
        return

    path.unlink()
    console.print(f"Controller successfully removed: {name}", style="success")

# -----------------
# delete view
# -----------------
def delete_view(name: str):
    path = BASE / "views" / "pages" / f"{name}_view.py"

    if not path.exists():
        console.print(f"View '{name}' does not exist.", style="warning")
        return

    path.unlink()
    console.print(f"View successfully removed: {name}", style="success")

# -----------------
# delete model
# -----------------
def delete_model(name: str):
    path = BASE / "models" / f"{name}_model.py"

    if not path.exists():
        console.print(f"Model '{name}' does not exist.", style="warning")
        return

    path.unlink()
    console.print(f"Model successfully removed: {name}", style="success")

# -----------------
# delete page
# -----------------
def delete_page(name: str):
    delete_view(name)
    delete_controller(name)
    delete_model(name)

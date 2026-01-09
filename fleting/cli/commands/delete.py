from pathlib import Path

BASE = Path.cwd()

def handle_delete(args):
    if len(args) < 2:
        print("Uso: fleting delete <controller|view|model|page> <nome>")
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
            print(f"Unsupported Type: {kind}")

    except Exception:
        print(f"Error when deleting {kind} {name}")

# -----------------
# delete controller
# -----------------
def delete_controller(name: str):
    path = BASE / "controllers" / f"{name}_controller.py"

    if not path.exists():
        print(f"Controller '{name}' does not exist.")
        return

    path.unlink()
    print(f"Controller successfully removed: {name}")

# -----------------
# delete view
# -----------------
def delete_view(name: str):
    path = BASE / "views" / "pages" / f"{name}_view.py"

    if not path.exists():
        print(f"View '{name}' does not exist.")
        return

    path.unlink()
    print(f"View successfully removed: {name}")

# -----------------
# delete model
# -----------------
def delete_model(name: str):
    path = BASE / "models" / f"{name}_model.py"

    if not path.exists():
        print(f"Model '{name}' does not exist.")
        return

    path.unlink()
    print(f"Model successfully removed: {name}")

# -----------------
# delete page
# -----------------
def delete_page(name: str):
    delete_view(name)
    delete_controller(name)
    delete_model(name)

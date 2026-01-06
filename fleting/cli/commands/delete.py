from pathlib import Path

BASE = Path.cwd() / "fleting"

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
            print(f"Tipo não suportado: {kind}")

    except Exception:
        print(f"Erro ao deletar {kind} {name}")

# -----------------
# delete controller
# -----------------
def delete_controller(name: str):
    path = BASE / "controllers" / f"{name}_controller.py"

    if not path.exists():
        print(f"Controller '{name}' não existe")
        return

    path.unlink()
    print(f"Controller removido com sucesso: {name}")

# -----------------
# delete view
# -----------------
def delete_view(name: str):
    path = BASE / "views" / "pages" / f"{name}_view.py"

    if not path.exists():
        print(f"View '{name}' não existe")
        return

    path.unlink()
    print(f"View removida com sucesso: {name}")

# -----------------
# delete model
# -----------------
def delete_model(name: str):
    path = BASE / "models" / f"{name}_model.py"

    if not path.exists():
        print(f"Model '{name}' não existe")
        return

    path.unlink()
    print(f"Model removido com sucesso: {name}")

# -----------------
# delete page
# -----------------
def delete_page(name: str):
    delete_view(name)
    delete_controller(name)
    delete_model(name)

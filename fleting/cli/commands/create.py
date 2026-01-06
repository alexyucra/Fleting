from pathlib import Path

def get_project_root() -> Path:
    """
    Diretório onde o usuário executou o comando fleting
    """
    return Path.cwd()

def get_fleting_base() -> Path:
    """
    Pasta base do framework dentro do projeto
    """
    return get_project_root() / "fleting"

def handle_create(args):
    if len(args) < 2:
        print("Uso: fleting create <controller|view|model|page> <nome>")
        return

    kind, name = args[0], args[1]
    name = name.lower()

    try:
        if kind == "controller":
            create_controller(name)
        elif kind == "view":
            create_view(name)
        elif kind == "model":
            create_model(name)
        elif kind == "page":
            create_page(name)
        else:
            print(f"Tipo não suportado: {kind}")

    except Exception as e:
        print(f"Erro ao criar {kind} {name}: {e}")

# --------------
# create controller
# --------------
def to_pascal_case(text: str) -> str:
    return "".join(word.capitalize() for word in text.split("_"))

def create_controller(name: str):
    BASE = get_fleting_base()
    path = BASE / "controllers" / f"{name}_controller.py"

    if path.exists():
        print(f"Controller '{name}' já existe")
        return

    class_name = f"{to_pascal_case(name)}Controller"
    model_class = f"{to_pascal_case(name)}Model"

    content = f'''from models.{name}_model import {model_class}

class {class_name}:
    """
    Controller for {name} page
    """

    def __init__(self, model=None):
        self.model = model or {model_class}()

    def get_title(self):
        return "{to_pascal_case(name)}"
'''
    path.write_text(content, encoding="utf-8")
    print(f"Controller criado com sucesso: {name}")

# --------------
# create view
# --------------
def create_view(name: str):
    BASE = get_fleting_base()
    path = BASE / "views" / "pages" / f"{name}_view.py"

    if path.exists():
        print(f"View '{name}' já existe")
        return

    class_name = f"{name.capitalize()}View"

    content = f"""import flet as ft
from views.layouts.main_layout import MainLayout

class {class_name}:
    def __init__(self, page, router):
        self.page = page
        self.router = router

    def render(self):
        content = ft.Column(
            controls=[
                ft.Text("{name.capitalize()}", size=24),
            ],
            spacing=16,
        )

        return MainLayout(
            page=self.page,
            content=content,
            router=self.router,
        )
"""

    path.write_text(content, encoding="utf-8")
    print(f"View criada com sucesso: {name}")


# --------------
# create model
# --------------
def create_model(name: str):
    BASE = get_fleting_base()
    path = BASE / "models" / f"{name}_model.py"

    if path.exists():
        print(f"Model '{name}' já existe")
        return

    class_name = f"{name.capitalize()}Model"

    content = f"""class {class_name}:
    def __init__(self):
        pass
"""

    path.write_text(content, encoding="utf-8")
    print(f"Model criado com sucesso: {name}")

# --------------
# create page
# --------------
def create_page(name: str):
    print(f"Criando page completa: {name}")
    try:
        create_model(name)
        create_controller(name)
        create_page_view(name)
        register_route(name)
    except Exception as e:
        print("Erro ao crear page: ", str(e))

def register_route(name: str):
    BASE = get_fleting_base()
    routes_file = BASE / "configs" / "routes.py"

    if not routes_file.exists():
        print("❌ routes.py não encontrado")
        return

    route_block = f"""
    {{
        "path": "/{name}",
        "view": "views.pages.{name}_view.{name.capitalize()}View",
        "label": "{name.capitalize()}",
        "icon": ft.Icons.CHEVRON_RIGHT,
        "show_in_top": True,
        "show_in_bottom": False,
    }},
"""

    content = routes_file.read_text(encoding="utf-8")

    # evita duplicar
    if f'"path": "/{name}"' in content:
        print(f"⚠️ Rota '/{name}' já existe")
        return

    if "ROUTES = [" not in content:
        print("❌ Estrutura ROUTES não encontrada")
        return

    content = content.replace(
        "ROUTES = [",
        "ROUTES = [" + route_block,
        1,
    )

    routes_file.write_text(content, encoding="utf-8")
    print(f"✅ Rota '/{name}' registrada com sucesso")

def create_page_view(name: str):
    BASE = get_fleting_base()
    path = BASE / "views" / "pages" / f"{name}_view.py"

    if path.exists():
        print(f"View '{name}' já existe")
        return

    class_name = f"{name.capitalize()}View"
    controller_class = f"{name.capitalize()}Controller"
    model_class = f"{name.capitalize()}Model"

    content = f"""import flet as ft
from views.layouts.main_layout import MainLayout
from controllers.{name}_controller import {controller_class}
from models.{name}_model import {model_class}

class {class_name}:
    def __init__(self, page, router):
        self.page = page
        self.router = router

        self.model = {model_class}()
        self.controller = {controller_class}(self.model)

    def render(self):
        content = ft.Column(
            controls=[
                ft.Text(self.controller.get_title(), size=24),
            ],
            spacing=16,
        )

        return MainLayout(
            page=self.page,
            content=content,
            router=self.router,
        )
"""
    path.write_text(content, encoding="utf-8")
    print(f"Page criada com sucesso: {name}")

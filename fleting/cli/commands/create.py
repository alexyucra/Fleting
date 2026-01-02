from pathlib import Path
from fleting.core.logger import get_logger

logger = get_logger("CLI.Create")

BASE = Path.cwd()

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
            logger.warning(f"Tipo de criação não suportado: {kind}")
            print(f"Tipo não suportado: {kind}")

    except Exception:
        logger.exception(f"Erro ao criar {kind}: {name}")
        print(f"Erro ao criar {kind} {name}")

# --------------
# create controller
# --------------
def create_controller(name: str):
    path = BASE / "controllers" / f"{name}_controller.py"

    if path.exists():
        print(f"Controller '{name}' já existe")
        return

    class_name = f"{name.capitalize()}Controller"

    content = f"""class {class_name}:
    def __init__(self, model=None):
        self.model = model

    def get_title(self):
        return "{name.capitalize()}"
"""
    path.write_text(content, encoding="utf-8")
    logger.info(f"Controller criado: {path}")
    print(f"Controller criado com sucesso: {name}")


# --------------
# create view
# --------------
def create_view(name: str):
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
    logger.info(f"View criada: {path}")
    print(f"View criada com sucesso: {name}")


# --------------
# create model
# --------------
def create_model(name: str):
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
    logger.info(f"Model criado: {path}")
    print(f"Model criado com sucesso: {name}")

# --------------
# create page
# --------------
def create_page(name: str):
    logger.info(f"Criando page completa: {name}")

    create_model(name)
    create_controller(name)
    create_page_view(name)

def create_page_view(name: str):
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
    logger.info(f"Page criada: {path}")
    print(f"Page criada com sucesso: {name}")

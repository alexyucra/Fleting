import keyword
import re
from fleting.cli.console.console import console
from fleting.cli.helpers.project import get_project_root

def to_pascal_case(text: str) -> str:
    return "".join(word.capitalize() for word in text.split("_"))

def handle_create(args):
    
    root = get_project_root()
    if not root:
        return
 
    if len(args) < 2:
        console.print("Use: fleting create <controller|view|model|page> <nome>", style="suggestion")
        return

    kind, name = args[0], args[1].lower()

    if not re.fullmatch(r"[a-z][a-z0-9_]*", name) or keyword.iskeyword(name):
        console.print(
            f"Invalid name '{name}'. Use snake_case: letters, numbers and '_' (starting with a letter).",
            style="error",
        )
        return

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
            console.print(f"Unsupported Type: {kind}", style="warning")

    except Exception as e:
        console.print(f"Error creating {kind} {name}: {e}", style="error")

# --------------
# create controller
# --------------
def create_controller(name: str):
    BASE = get_project_root()
    path = BASE / "app/controllers" / f"{name}_controller.py"

    if path.exists():
        console.print(f"Controller '{name}' already exists.", style="warning")
        return

    class_name = f"{to_pascal_case(name)}Controller"
    model_class = f"{to_pascal_case(name)}Model"

    content = f'''from app.models.{name}_model import {model_class}

class {class_name}:
    """
    Controller for {name} page
    """

    def __init__(self, model=None):
        self.model = model or {model_class}

    def get_title(self):
        return "{to_pascal_case(name)}"
'''
    path.write_text(content, encoding="utf-8")
    console.print(f"Controller successfully created: {name}", style="success")

# --------------
# create view
# --------------
def create_view(name: str):
    BASE = get_project_root()
    path = BASE / "app" / "views" / "pages" / f"{name}_view.py"

    if path.exists():
        console.print(f"View '{name}' already exists.", style="warning")
        return

    class_name = f"{to_pascal_case(name)}View"

    content = f"""import flet as ft
from app.views.layouts.main_layout import MainLayout

class {class_name}:
    def __init__(self, page, router):
        self.page = page
        self.router = router

    def render(self):
        content = ft.Column(
            controls=[
                ft.Text("{name.replace("_", " ").title()}", size=24),
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
    console.print(f"View successfully created: {name}", style="success")


# --------------
# create model
# --------------
def create_model(name: str):
    BASE = get_project_root()
    path = BASE / "app/models" / f"{name}_model.py"

    if path.exists():
        console.print(f"Model '{name}' already exists.", style="warning")
        return

    class_name = f"{to_pascal_case(name)}Model"

    content = f"""from core.base_model import BaseModel

class {class_name}(BaseModel):
    table_name = "{name}"
"""

    path.write_text(content, encoding="utf-8")
    console.print(f"Model successfully created: {name}", style="success")

# --------------
# create page
# --------------
def create_page(name: str):
    console.print(f"Creating a complete page: {name}", style="info")
    try:
        create_model(name)
        create_controller(name)
        create_page_view(name)
        register_route(name)
    except Exception as e:
        console.print(f"Error creating page: {e}", style="error")

def register_route(name: str):
    BASE = get_project_root()
    routes_file = BASE / "configs" / "routes.py"

    if not routes_file.exists():
        console.print("❌ configs/routes.py not found", style="error")
        return

    route_block = f"""
    {{
        "path": "/{name}",
        "view": "app.views.pages.{name}_view.{to_pascal_case(name)}View",
        "label": "{name.replace("_", " ").title()}",
        "icon": ft.Icons.CHEVRON_RIGHT,
        "show_in_top": True,
        "show_in_bottom": False,
    }},
"""

    content = routes_file.read_text(encoding="utf-8")

    # evita duplicar
    if f'"path": "/{name}"' in content:
        console.print(f"⚠️ Route '/{name}' already exists.", style="warning")
        return

    content, n = re.subn(r"ROUTES\s*=\s*\[", lambda m: m.group(0) + route_block, content, count=1)
    if not n:
        console.print("❌ ROUTES structure not found", style="error")
        return

    if not re.search(r"^import flet as ft\b", content, re.M):
        content = "import flet as ft\n" + content

    routes_file.write_text(content, encoding="utf-8")
    console.print(f"✅ Route '/{name}' successfully registered", style="success")

def create_page_view(name: str):
    BASE = get_project_root()
    path = BASE / "app" / "views" / "pages" / f"{name}_view.py"

    if path.exists():
        console.print(f"View '{name}' already exists.", style="warning")
        return

    class_name = f"{to_pascal_case(name)}View"
    controller_class = f"{to_pascal_case(name)}Controller"

    content = f"""import flet as ft
from app.views.layouts.main_layout import MainLayout
from app.controllers.{name}_controller import {controller_class}

class {class_name}:
    def __init__(self, page, router):
        self.page = page
        self.router = router
        self.controller = {controller_class}()

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
    console.print(f"Page created successfully: {name}", style="success")

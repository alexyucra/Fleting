from pathlib import Path
import json

def init_project(base: Path | None = None):
    """
    Inicializa um projeto Fleting no diretório atual
    """

    BASE = Path("fleting")

    # =========================
    # UTIL
    # =========================
    def create_file(path, content=""):
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(content, encoding="utf-8")

    # =========================
    # ESTRUTURA DE PASTAS
    # =========================
    folders = [
        "core",
        "configs/languages",
        "controllers",
        "models",
        "views/layouts",
        "views/pages",
        "cli/commands",
        "cli/templates",
    ]

    for folder in folders:
        (BASE / folder).mkdir(parents=True, exist_ok=True)

    # =========================
    # ARQUIVOS CORE
    # =========================
    create_file(BASE / "core/state.py", """
class AppState:
    device = None  # mobile | tablet | desktop
    initial_device = "mobile"
    language = "pt"
    initialized = False
""")

    create_file(BASE / "core/responsive.py", """
def get_device_type(width):
    if width <= 600:
        return "mobile"
    elif width <= 1024:
        return "tablet"
    return "desktop"
""")

    create_file(BASE / "core/router.py", """
import flet as ft
from core.logger import get_logger

logger = get_logger("Router")
class Router:
    def __init__(self, page):
        self.page = page
        self.current_route = "/"

    def _load_routes(self):
        # Import tardio para evitar circular import
        from configs.routes import routes
        return routes

    def navigate(self, route):
        routes = self._load_routes()

        if route not in routes:
            logger.warning(f"Rota não encontrada: {route}")
            route = "/"

        logger.info(f"Navegando para: {route}")
        self.current_route = route
        self.page.controls.clear()

        try:
            view = routes[route](self.page, self)
            self.page.add(view)
        except Exception as e:
            logger.exception("Erro ao renderizar view")
            self.page.add(ft.Text("Erro interno da aplicação"))

        self.page.update()
""")

    create_file(BASE / "core/app.py", """
import flet as ft
from core.responsive import get_device_type
from core.state import AppState

class FletingApp:
    def __init__(self, page):
        self.page = page
        AppState.device = AppState.initial_device
        self.page.on_resize = self.on_resize

    def on_resize(self, e):
        real_device = get_device_type(self.page.width)

        # Evita sobrescrever no primeiro frame falso
        if not AppState.initialized:
            AppState.initialized = True

        AppState.device = real_device
        self.page.update()
""")

    create_file(BASE / "core/i18n.py", """
import json
from pathlib import Path
from core.state import AppState

class I18n:
    translations = {}

    @classmethod
    def load(cls, lang):
        path = Path("configs/languages") / f"{lang}.json"
        cls.translations = json.loads(path.read_text(encoding="utf-8"))
        AppState.language = lang

    @classmethod
    def t(cls, key):
        value = cls.translations
        for k in key.split("."):
            value = value.get(k)
            if value is None:
                return key
        return value
""")

    create_file(BASE / "core/logger.py", """
import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "fleting.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

def get_logger(name: str):
    return logging.getLogger(name)
""")

    create_file(BASE / "core/error_handler.py", """
import flet as ft
from core.logger import get_logger

logger = get_logger("ErrorHandler")

class GlobalErrorHandler:
    @staticmethod
    def handle(page: ft.Page, error: Exception):
        logger.exception("Erro global capturado")

        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Ocorreu um erro", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Algo deu errado. Tente novamente."),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                expand=True,
                alignment=ft.alignment.center,
            )
        )
        page.update()
""")

    # =========================
    # CONFIGS
    # =========================
    create_file(BASE / "configs/app_config.py", """
# configs/app_config.py
import flet as ft

class ScreenConfig:
    MOBILE = {
        "width": 390,
        "height": 758,
        "max_content_width": 390,
    }

    TABLET = {
        "width": 768,
        "height": 1024,
        "max_content_width": 768,
    }

    DESKTOP = {
        "width": 1280,
        "height": 800,
        "max_content_width": None,  # sem limite
    }

class AppConfig:
    APP_NAME = "Fleting"
    DEFAULT_SCREEN = ScreenConfig.MOBILE
    THEME_MODE = ft.ThemeMode.LIGHT
""")

    create_file(BASE / "configs/routes.py", """
import importlib

# Mapeamento rota -> módulo.classe
ROUTE_MAP = {
    "/": "views.pages.home_view.HomeView",
    # "/login": "views.pages.login_view.LoginView",
    # "/dashboard": "views.pages.dashboard_view.DashboardView",
}

def load_view(view_path: str):
    \"\"\"Carrega uma view dinamicamente\"\"\"
    module_name, class_name = view_path.rsplit(".", 1)
    
    try:
        module = importlib.import_module(module_name)
        view_class = getattr(module, class_name)
        return view_class
    except (ImportError, AttributeError) as e:
        print(f"Erro ao carregar view {view_path}: {e}")
        return None

def get_routes():
    routes = {}

    for route_path, view_path in ROUTE_MAP.items():
        def create_view_lambda(path=view_path):
            # 🚨 lambda aceita page e router
            return lambda page, router: load_view(path)(page, router).render()

        routes[route_path] = create_view_lambda()

    return routes

routes = get_routes()
""")

    # =========================
    # LANGUAGES
    # =========================
    pt = {
    "app": {
        "name": "Fleting"
    },
    "menu": {
        "home": "Inicio",
        "settings": "Configurações"
    },
    "home": {
        "title": "Bem-vindo ao Fleting"
    },
    "settings": {
        "title": "Configurações",
        "language": "Idioma"
    }
    }

    es = {
    "app": {
        "name": "Fleting"
    },
    "menu": {
        "home": "Inicio",
        "settings": "Configuración"
    },
    "home": {
        "title": "Bienvenido a Fleting"
    },
    "settings": {
        "title": "Configuración",
        "language": "Idioma"
    }
    }

    (BASE / "configs/languages/pt.json").write_text(json.dumps(pt, indent=2, ensure_ascii=False))
    (BASE / "configs/languages/es.json").write_text(json.dumps(es, indent=2, ensure_ascii=False))

    # =========================
    # LAYOUT
    # =========================
    create_file(BASE / "views/layouts/main_layout.py", """
import flet as ft
from core.state import AppState
from core.i18n import I18n

class MainLayout(ft.Column):
    def __init__(self, page, content, router):
        super().__init__(expand=True)
        self._page = page
        self.router = router
        self.content = content

        self._build()

    def _build(self):
        self.controls.clear()

        # TOP BAR
        self.controls.append(self._top_bar())

        # CONTENT
        self.controls.append(
            ft.Container(
                content=self.content,
                expand=True,
                padding=0,
            )
        )

        # BOTTOM BAR (mobile / tablet)
        if AppState.device != "desktop":
            self.controls.append(self._bottom_bar())

    # ---------- TOP BAR ----------
    def _top_bar(self):
        return ft.AppBar(
            title=ft.Text(I18n.t("app.name")),
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            content=ft.Text("Português"),
                            on_click=lambda e: self._change_language("pt"),
                        ),
                        ft.PopupMenuItem(
                            content=ft.Text("Español"),
                            on_click=lambda e: self._change_language("es"),
                        ),
                    ]
                )
            ],
        )

    # ---------- BOTTOM BAR ----------
    def _bottom_bar(self):
        return ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.HOME,
                    label=I18n.t("menu.home"),
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.SETTINGS,
                    label=I18n.t("menu.settings"),
                ),
            ],
            on_change=self._on_nav_change,
        )

    def _on_nav_change(self, e):
        if not self.router:
            return

        if e.control.selected_index == 0:
            self.router.navigate("/")
        elif e.control.selected_index == 1:
            self.router.navigate("/settings")

    # ---------- LANGUAGE ----------
    def _change_language(self, lang):
        I18n.load(lang)
        if self.router:
            self.router.navigate(self.router.current_route)
""")

    # =========================
    # VIEW HOME
    # =========================
    create_file(BASE / "views/pages/home_view.py", """
import flet as ft
from views.layouts.main_layout import MainLayout

class HomeView:
    def __init__(self, page, router):
        self.page = page
        self.router = router
    
    def render(self):
        # CONTEÚDO DA VIEW (puro)
        content = ft.Column(
            controls=[
                ft.Text("Home Page", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Bem-vindo ao Fleting Framework!"),
                ft.Button(
                    "Ir para Configurações",
                    on_click=lambda e: self.router.navigate("/settings"),
                ),
            ],
            spacing=20,
        )

        # LAYOUT ENVOLVE O CONTEÚDO
        return MainLayout(
            page=self.page,
            content=content,
            router=self.router,
        )
""")

    # =========================
    # APP ENTRY
    # =========================
    create_file(BASE / "app.py", """
import flet as ft
from configs.app_config import AppConfig
from core.logger import get_logger
from core.error_handler import GlobalErrorHandler

logger = get_logger("App")

def main(page: ft.Page):
    try:
        from core.app import FletingApp
        page.window.width = AppConfig.DEFAULT_SCREEN["width"]
        page.window.height = AppConfig.DEFAULT_SCREEN["height"]

        from core.i18n import I18n
        I18n.load("pt")

        from core.router import Router
        from configs.routes import routes

        router = Router(page)
        router.navigate("/")

        logger.info("Aplicação iniciada com sucesso")
        
    except Exception as e:
        GlobalErrorHandler.handle(page, e)

ft.run(main)

""")

    # =========================
    # CLI BÁSICO
    # =========================
    create_file(BASE / "cli/cli.py", """
import sys
from core.logger import get_logger
from cli.commands.create import handle_create
from cli.commands.delete import handle_delete

logger = get_logger("CLI")

def main():
    try:
        args = sys.argv[1:]

        if not args:
            print("Uso: fleting create <controller|view|model|page> <nome>")
            return

        command = args[0]

        if command == "create":
            handle_create(args[1:])
        elif command == "delete":
            handle_delete(args[1:])
        else:
            logger.warning(f"Comando desconhecido: {command}")
            print(f"Comando desconhecido: {command}")

    except Exception as e:
        logger.exception("Erro no CLI")
        print("Erro ao executar comando CLI")

if __name__ == "__main__":
    main()
""")

    create_file(BASE / "cli/commands/create.py", """
from pathlib import Path
from core.logger import get_logger

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

    content = f\"\"\"class {class_name}:
    def __init__(self, model=None):
        self.model = model

    def get_title(self):
        return "{name.capitalize()}"
\"\"\"
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

    content = f\"\"\"import flet as ft
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
\"\"\"

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

    content = f\"\"\"class {class_name}:
    def __init__(self):
        pass
\"\"\"

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

    content = f\"\"\"import flet as ft
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
\"\"\"
    path.write_text(content, encoding="utf-8")
    logger.info(f"Page criada: {path}")
    print(f"Page criada com sucesso: {name}")
""")

    create_file(BASE / "cli/commands/delete.py", """
from pathlib import Path
from core.logger import get_logger

logger = get_logger("CLI.Delete")

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
            print(f"Tipo não suportado: {kind}")

    except Exception:
        logger.exception(f"Erro ao deletar {kind}: {name}")
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
    logger.info(f"Controller removido: {path}")
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
    logger.info(f"View removida: {path}")
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
    logger.info(f"Model removido: {path}")
    print(f"Model removido com sucesso: {name}")

# -----------------
# delete page
# -----------------
def delete_page(name: str):
    delete_view(name)
    delete_controller(name)
    delete_model(name)
""")

    # =========================
    # CLI run
    # =========================
    create_file(BASE / "fleting.bat", """
@echo off
python -m cli.cli %*
""")

    print("✅ Framework Fleting criado com sucesso!")

if __name__ == "__main__":
    init_project()
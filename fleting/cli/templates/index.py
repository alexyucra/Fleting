from pathlib import Path
import json

def init_project(project_root: Path):
    """
    Inicializa um projeto Fleting no diretório atual
    """

    BASE = project_root / "fleting"

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
        "assets",
        "core",
        "configs/languages",
        "controllers",
        "models",
        "views/layouts",
        "views/pages",
        "data",
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
    current_route = "/"
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
        self.routes = self._load_routes()

    def _load_routes(self):
        from configs.routes import routes
        return routes

    def navigate(self, route):
        routes = self.routes

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
        I18n.load(AppState.language)
        self.page.appbar = self.build_topbar()
        self.router.navigate("/")
    
    def build_topbar(self):
        menu_items = []

        menu = I18n.translations.get("menu", {})

        for route, label in menu.items():
            menu_items.append(
                ft.TextButton(
                    text=label,
                    icon=ft.icons.CIRCLE,
                    on_click=lambda e, r=f"/{route}": self.router.navigate(r),
                )
            )

        return ft.AppBar(
            title=ft.Text(I18n.t("app.name")),
            actions=menu_items,
            center_title=False,
        )

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
        current_file = Path(__file__).resolve()
        base_path = current_file.parent.parent
        path = base_path / "configs" / "languages" / f"{lang}.json"
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

LOG_DIR = Path(__file__).resolve().parents[1] / "logs"
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
                        ft.Text("⚠️ Ocorreu um erro", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Algo deu errado. Tente novamente."),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                expand=True,
            )
        )
        page.update()
""")

    create_file(BASE / "core/database.py", """
import sqlite3
# import mysql.connector  # opcional
from configs.database import DATABASE
from pathlib import Path

_connection = None

def get_connection():
    global _connection

    if _connection:
        return _connection

    engine = DATABASE["ENGINE"]

    if engine == "sqlite":
        db_path = DATABASE["SQLITE"]["PATH"]
        db_path.parent.mkdir(parents=True, exist_ok=True)

        _connection = sqlite3.connect(db_path)
        return _connection

    # elif engine == "mysql":
    #     cfg = DATABASE["MYSQL"]
    #     _connection = mysql.connector.connect(
    #         host=cfg["HOST"],
    #         port=cfg["PORT"],
    #         user=cfg["USER"],
    #         password=cfg["PASSWORD"],
    #         database=cfg["DATABASE"],
    #     )
    #     return _connection

    raise ValueError(f"Database engine não suportado: {engine}")

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
import flet as ft
import importlib

ROUTES = [
    {
        "path": "/",
        "view": "views.pages.home_view.HomeView",
        "label": "menu.home",
        "icon": ft.Icons.HOME,
        "show_in_top": True,
        "show_in_bottom": True,
    },
    {
        "path": "/settings",
        "view": "views.pages.settings_view.SettingsView",
        "label": "Settings",
        "icon": ft.Icons.SETTINGS,
        "show_in_top": True,
        "show_in_bottom": False,
    },
    {
        "path": "/help",
        "view": "views.pages.help_view.HelpView",
        "label": "Help",
        "icon": ft.Icons.HELP,
        "show_in_top": True,
        "show_in_bottom": True,
    }
]

def load_view(view_path: str):
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

    for r in ROUTES:
        def create_view_lambda(path=r["view"]):
            return lambda page, router: load_view(path)(page, router).render()

        routes[r["path"]] = create_view_lambda()

    return routes

routes = get_routes()

""")

    # =========================
    # LANGUAGES
    # =========================
    {
    "app": {
        "name": "Fleting"
    },
    "menu": {
        "home": "Home",
        "settings": "Configs"
    },
    "home": {
        "title": "Wellcome to Fleting"
    },
    "settings": {
        "title": "Configs",
        "language": "Language"
    }
    }

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

    pt_file = f"{BASE}/configs/languages/pt.json"
    es_file = f"{BASE}/configs/languages/es.json"
    with open(pt_file, 'w', encoding='utf-8') as f:
        json.dump(pt, f, indent=2, ensure_ascii=False)
    
    with open(es_file, 'w', encoding='utf-8') as f:
        json.dump(es, f, indent=2, ensure_ascii=False)

    # =========================
    # LAYOUT
    # =========================
    create_file(BASE / "views/layouts/main_layout.py", """
import flet as ft
from core.state import AppState
from core.i18n import I18n
from configs.routes import ROUTES

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
        items = []

        for r in ROUTES:
            if not r.get("show_in_top"):
                continue

            items.append(
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            ft.Icon(r["icon"]),
                            ft.Text(
                                I18n.t(r["label"]) if "." in r["label"] else r["label"]
                            ),
                        ],
                        spacing=10,
                    ),
                    on_click=lambda e, p=r["path"]: self.router.navigate(p),
                )
            )

        return ft.AppBar(
            title=ft.Text(I18n.t("app.name")),
            actions=[
                ft.PopupMenuButton(
                    icon=ft.Icons.MENU,
                    items=items,
                )
            ],
        )

    # ---------- BOTTOM BAR ----------
    def _bottom_bar(self):
        destinations = []
        paths = []

        for r in ROUTES:
            if r.get("show_in_bottom"):
                destinations.append(
                    ft.NavigationBarDestination(
                        icon=r["icon"],
                        label=I18n.t(r["label"]),
                    )
                )
                paths.append(r["path"])

        def on_change(e):
            self.router.navigate(paths[e.control.selected_index])

        return ft.NavigationBar(
            destinations=destinations,
            selected_index=paths.index(AppState.current_route)
            if AppState.current_route in paths else 0,
            on_change=on_change,
        )
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
        content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=24,
            controls=[
                ft.Text(
                    "Fleting",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Text(
                    "Micro Framework MVC para Flet",
                    size=16,
                    color=ft.Colors.GREY_600,
                ),

                ft.Text(
                    "Construa aplicações modernas com arquitetura clara, "
                    "roteamento dinâmico e CLI produtivo.",
                    size=14,
                    text_align=ft.TextAlign.CENTER,
                    width=420,
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=16,
                    controls=[
                        ft.FilledButton(
                            "Configurações",
                            icon=ft.Icons.SETTINGS,
                            on_click=lambda e: self.router.navigate("/settings"),
                        ),
                        ft.OutlinedButton(
                            "Criar nova página",
                            icon=ft.Icons.ADD,
                        ),
                    ],
                ),
            ],
        )

        # LAYOUT
        return MainLayout(
            page=self.page,
            content=content,
            router=self.router,
        )
""")

    create_file(BASE / "views/pages/settings_view.py", """
import flet as ft
from core.state import AppState
from core.i18n import I18n
from views.layouts.main_layout import MainLayout
from controllers.settings_controller import SettingsController
from models.settings_model import SettingsModel

class SettingsView:
    def __init__(self, page, router):
        self.page = page
        self.router = router

        self.model = SettingsModel()
        self.controller = SettingsController(self.model)
    
    def _change_language(self, lang: str):
        I18n.load(lang)
        self.page.update()

    def render(self):
        content = ft.Column(
            spacing=24,
            controls=[
                ft.Text(
                    self.controller.get_title(),
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Text(
                    I18n.t("settings.language"),
                    size=16,
                    color=ft.Colors.GREY_600,
                ),

                ft.RadioGroup(
                    value=AppState.language,
                    on_change=lambda e: self._change_language(e.control.value),
                    content=ft.Column(
                        controls=[
                            ft.Radio(value="pt", label="Português 🇧🇷"),
                            ft.Radio(value="en", label="English 🇺🇸"),
                            ft.Radio(value="es", label="Español 🇪🇸"),
                        ]
                    ),
                ),
            ],
        )

        return MainLayout(
            page=self.page,
            content=content,
            router=self.router,
        )
""")

    create_file(BASE / "views/pages/help_view.py", """
import flet as ft
from views.layouts.main_layout import MainLayout
from controllers.help_controller import HelpController
from models.help_model import HelpModel
from flet import UrlLauncher

class HelpView:
    def __init__(self, page, router):
        self.page = page
        self.router = router

        self.model = HelpModel()
        self.controller = HelpController(self.model)
        self.url_launcher = UrlLauncher()
    
    async def open_docs(self, e):
        await self.url_launcher.launch_url("https://github.com/alexyucra/Fleting")

    async def open_issues(self, e):
        await self.url_launcher.launch_url("https://github.com/alexyucra/fleting/issues")

    async def open_support(self, e):
        await self.url_launcher.launch_url("https://alexyucra.github.io/#contato")

    def render(self):
        

        content = ft.Column(
            spacing=24,
            controls=[
                ft.Text(
                    self.controller.get_title(),
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Text(
                    "Precisa de ajuda com o Fleting?",
                    size=18,
                    weight=ft.FontWeight.W_500,
                ),

                ft.Text(
                    "Aqui você encontra links úteis para documentação, "
                    "suporte e contribuição com o projeto.",
                    color=ft.Colors.GREY_600,
                ),

                ft.Divider(),

                ft.Button(
                    "📘 Documentação Oficial",
                    icon=ft.Icons.MENU_BOOK,
                    on_click=self.open_docs,
                ),

                ft.Button(
                    "🐛 Reportar um problema",
                    icon=ft.Icons.BUG_REPORT,
                    on_click=self.open_issues,
                ),

                ft.Button(
                    "💬 Precisa de uma automação ou Sistema?",
                    icon=ft.Icons.BUG_REPORT,
                    on_click=self.open_support,
                ),
            ],
        )

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
    # BASIC CONTROLLERS
    # =========================
    create_file(BASE / "controllers/settings_controller.py", """
from models.settings_model import SettingsModel

class SettingsController:
    '''
    Controller for settings page
    '''

    def __init__(self, model=None):
        self.model = model or SettingsModel()

    def get_title(self):
        return "Settings"
""")

    create_file(BASE / "controllers/help_controller.py", """
from models.help_model import HelpModel

class HelpController:
    '''
    Controller for help page
    '''

    def __init__(self, model=None):
        self.model = model or HelpModel()

    def get_title(self):
        return "Help"
""")

    # =========================
    # BASIC models
    # =========================
    create_file(BASE / "models/help_model.py", """
class HelpModel:
    def __init__(self):
        pass
""")

    create_file(BASE / "models/settings_model.py", """
class SettingsModel:
    def __init__(self):
        pass
""")

if __name__ == "__main__":
    init_project()
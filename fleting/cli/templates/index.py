from pathlib import Path
import json
import base64

ICON = "iVBORw0KGgoAAAANSUhEUgAAAFEAAABRCAIAAAAl7d1hAAAHeUlEQVR4nOWbbWxT1xnH/+f4+DXvcWynGYYCI7AWbW03ddsnutG1yaq1g0QUsaxrV2nA6CZQAVWomqap9MNYQ1e0qa3UlXVtpaqrWol96MSoRD/QFcqGVtKlBAIxTTJIbJLYjm/s6/tMF4KIHb8d+9om9u+Tfc/znHv+Ouee+5znnMuICFUGR/XBUX1wVB8c1QdH9cFRffCi1BoPgVTcrDDj389alPp6wO3M9RBaOsHtqHzNAP13M2aG9V/cDuf3mLsLZicqXPPIq7j8zpybmNG8lnkehsWFStWMcD8N7Jx3K4Hme9ktP4ZoQAVqBlHfY4iNpygx1TJPN1oeBLegst5VDA3fSl0SD9HIQerfjCtHUWHvZ1b/jUzF0TEa2keDv0b0MionJqldrU9dmZn6hPq34vJfQRoqQTO3oWZVdjNtRh/qZ3dD8aECYk9Wd0eupuF+OrMd/r9jwcfbdXdKGGtRuniAfL3QZrCANdu/LB14Bj6ggd2YGcVC1cw4HCukvSLn9HE+9QkW6lrS0Z6PVzxM53+DwGEsRM2sZmWenqSR74WEoL1cmscHR/bt+eOxt4+QllvE6shXsw7RyKs0/DJA5Yy3j7z+/t6T/wGwJKZ1rW7v+MkDwm7N7EJ9jyAWKKiNzg7m3abHs2Xp55V3zD6fQ2be+/nZjbt63/rdG9FpJZOPzVtQAwH436eRgzAOLmW9aPWyptiNODFgNr00PNyze/+7f3hHU+OpfWyLC20joD/YY++hXHPY7VZb0pVxs+nA2XOPb9937O0j8+2ZteB+vgoNv4JAivpLoXlVW+pcx5CZP33s5J7tz/2v31dQP4tGPZ3CxLwCoosHEPw3Sp8zOP7eh08d/WcGA4tG3S73ozs3CdvV6U2doNM9OVXtvF/PnFnb9N9aBFeO0uhfoE4m2HA7a98P2yKUsp+X35UlzIhy9qZ/bMuu5wc//kz/LxqyLyoB5t3GvL+YFTybPOxg7b0wtyTYaRG68Cy0jLOm4Zqdi1sb1ezL3UHBtr556LVn/0xxDebmLNZNa+DsTHHd4mGLdyRfVHx08QWUOA5rY6ZczGKcHRy7tH1Hr38sS6JXz4Sno+5rsN+afPHKh4XMZzwPH5clSxwyl09N9NHvETudPNvfgHF9BSYZzNHwS4heQuk01zqk7CdUFt7fohyqTxNEcrCMMVaKORyIT5Pv+fzCUp6Hj7u5Tso+aOYgKO/WT7/YTLF58kid3fRIR+R86uuhTxH4B0qjuU6yn6fMsx0VPeEI7XVrgeTpgDJkhRQfpvvTFdLwn6BOlEKzwyGX/VD4jb6N+8yhZ9zxLxLfXmOHEDqdwlNTyLc/U1Y0HqTR10qiuU5O84wpYTxrE6bQb13quTn7GKTS4K8w/reEHdzpAT1PND2QpXb/YUQGpdojII/lWoCVVz9fg0I8/JyrZue4WHY946dF6YsXMfo6albqMczMSM7ZX6KRV9jyvcXVHIvGpOxpnmb9osLUM5Ybmq8RD2HqpHSD0k1yBo7tqBKVsjelSqpY14Rt94VgBKx1k5S9yOMearqlchp4kmQT2XsmrGvCMATHCji/X3TNwYmglL15ztKNN2iOzX6xyqDEPTMx7xN6JFdszZf9ieu7bDiur0lE+4xji583Grcj53oI9uWyTiKPG/lDcsPSHtfAYOsM2tZPzRvoBWDxyD7J+WseD0ek7O12XvvUmFhh6EYUM7ElT+q7n6XRfEGNQuT0CDHC/Y7aR3bZhGrwzhtreww1t+XnK2QdwoHgJZFTqnlZjHZ03Xv7d75O55+B3AyQjfq79Sc5X4Ssw8CJPsqWXm9UtU0rlq7f2s3NV5cTSTmtArG4riZPWOk0f3b6XIZSR5y63O6Ht3U7muasNwvcx5gLt7Jb90DILWYL1XzSN5oyeLNrWmd9Y8/P1jV6PQkFWhSxMRgC42zJznz2dwvRrIQifYgnjSuPqnV+qe2Hjz9Y72pM4RMdMeiIDGOLnkDDtwuvSEhZnzp8PHp9wWAi3Em885tfXbNhLRfps4JKxhxIzrDWH8F5nyFVCSlrVY0zUHuMrV3u/e76e5qX3JLdJ3PeJ0daOtG6EQbBZPcxIpMhe0Nt7vb6sZjAB7iZ9mKFrIOUYJ3IEArBvY61/dRAwcgvDpNAU6BcyN/d3c3aHoXRCBSV6QGQ3GL7OkzvXvc6w1uE4ms+k48XtzDvL9F0D4qDQDGhcNrUdFrMTrb06cIDjzL28+dy9jW3saV79G33YiKKWLfik4u0nR1s0ZbUu1OGIopYd/BfuVqaHPqM5exASRDFq5qCp3Kyq/mKnvGwtKJUiGJVTGrqLai5MAHPBubZKJu4vFk1h/uynPqwL2WLn0xxhmDhaqbJE2nLuA3u9cyzoQTTVUpEsSqeOp76ev3dzPvz5NNAlaBZGdI3FpOwtumvorq7UG5EUWqd/Djhr7lJ/1jS2VGuwZxEURpBkx/N/uJ2tDygP7omueMYC02zpmD6LLgVLT9gni6YCspRLpxvRIOn9KOtWY//VdZ3sTc1HNUHR/XBUX1wVB8c1QcvdwPKwP8BUqJxlM/rbX4AAAAASUVORK5CYII="

def init_project(project_root: Path, project_name: str = "Fleting"):
    """
    Initializes a Fleting project in the current directory.
    """

    BASE = project_root

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
    ]

    for folder in folders:
        (BASE / folder).mkdir(parents=True, exist_ok=True)
    
    

    # =========================
    # ICON FLETING
    # =========================
    try:
        with open(BASE / "assets/icon.png", "wb") as f:
            f.write(base64.b64decode(ICON))
    except Exception as e:
        print(f"❌ Error creating icon: {str(e)}")
        pass
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
            logger.warning(f"Route not found: {route}")
            route = "/"

        logger.info(f"Navigating to: {route}")
        self.current_route = route
        self.page.controls.clear()

        try:
            view = routes[route](self.page, self)
            self.page.add(view)
        except Exception as e:
            logger.exception("Error rendering view")
            self.page.add(ft.Text("Internal application error"))

        self.page.update()
""")

    create_file(BASE / "core/app.py", """
import flet as ft
from core.responsive import get_device_type
from core.state import AppState
from core.i18n import I18n

class FletingApp:
    def __init__(self, page):
        self.page = page
        AppState.device = AppState.initial_device
        self.page.on_resize = self.on_resize
        I18n.load(AppState.language)
        self.page.appbar = self.build_topbar()
        from core.router import Router
        self.router = Router(page)
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

        # Avoid overwriting on the first fake frame
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
import sys
import os
from pathlib import Path

APP_NAME = "fleting"

def is_frozen():
    return getattr(sys, "frozen", False)

def is_android():
    return sys.platform == "android"

def get_log_dir():
    # ANDROID (APK)
    if is_android():
        return Path(os.getcwd()) / "files" / "logs"

    # EXECUTABLE (PyInstaller)
    if is_frozen():
        base = Path(os.getenv("LOCALAPPDATA", Path.home()))
        return base / APP_NAME / "logs"

    # DESENVOLVIMENTO
    return Path.cwd() / "logs"

LOG_DIR = get_log_dir()
LOG_DIR.mkdir(parents=True, exist_ok=True)

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
        logger.exception("Global error caught")

        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("⚠️ An error occurred.", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Something went wrong. Please try again."),
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
# import mysql.connector  
from configs.database import DATABASE
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
_connection = None

def get_connection():
    global _connection

    if _connection is not None:
        return _connection

    engine = DATABASE.get("ENGINE", "sqlite").lower()

    if engine == "sqlite":
        _connection = _connect_sqlite()
    elif engine == "mysql":
        _connection = _connect_mysql()
    else:
        raise RuntimeError(f"Unsupported database engine: {engine}")

    return _connection

# =========================
# SQLITE
# =========================
def _connect_sqlite():
    cfg = DATABASE.get("SQLITE", {})
    path_cfg = cfg.get("PATH", "data/fleting.db")

    db_path = BASE_DIR / Path(path_cfg)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(db_path)

# =========================
# MYSQL
# =========================
def _connect_mysql():
    pass
    # try:
    #     import mysql.connector
    # except ImportError:
    #     raise RuntimeError(
    #         "MySQL support requires `mysql-connector-python` :"
    #         "pip install mysql-connector-python"
    #     )

    # cfg = DATABASE.get("MYSQL", {})

    # return mysql.connector.connect(
    #     host=cfg.get("HOST", "localhost"),
    #     port=cfg.get("PORT", 3306),
    #     user=cfg.get("USER"),
    #     password=cfg.get("PASSWORD"),
    #     database=cfg.get("NAME"),
    #     charset=cfg.get("OPTIONS", {}).get("charset", "utf8mb4"),
    # )

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
        "max_content_width": None,  # no limit
    }

class AppConfig:
    APP_NAME = "{project_name}"
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
        "label": "menu.settings",
        "icon": ft.Icons.SETTINGS,
        "show_in_top": True,
        "show_in_bottom": False,
    },
    {
        "path": "/help",
        "view": "views.pages.help_view.HelpView",
        "label": "menu.help",
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
    
    create_file(BASE / "configs/database.py", """
DATABASE = {
    "ENGINE": "sqlite",  # sqlite | mysql

    "SQLITE": {
        "PATH": "data/fleting.db"
    },

    "MYSQL": {
        "HOST": "localhost",
        "PORT": 3306,
        "USER": "root",
        "PASSWORD": "",
        "NAME": "fleting",
        "OPTIONS": {
            "charset": "utf8mb4"
        }
    }
}
""")

    # =========================
    # LANGUAGES
    # =========================
    en = {
    "app": {
        "name": project_name
    },
    "menu": {
        "home": "Home",
        "settings": "Configs",
        "help": "Help"
    },
    "home": {
        "title": f"Wellcome to {project_name}"
    },
    "settings": {
        "title": "Configs",
        "language": "Language"
    }
    }

    pt = {
    "app": {
        "name": project_name
    },
    "menu": {
        "home": "Inicio",
        "settings": "Configurações",
        "help": "Ajuda"
    },
    "home": {
        "title": f"Bem-vindo ao {project_name}"
    },
    "settings": {
        "title": "Configurações",
        "language": "Idioma"
    }
    }

    es = {
    "app": {
        "name": project_name
    },
    "menu": {
        "home": "Inicio",
        "settings": "Configuración",
        "help": "Ayuda"
    },
    "home": {
        "title": f"Bienvenido a {project_name}"
    },
    "settings": {
        "title": "Configuración",
        "language": "Idioma"
    }
    }

    pt_file = f"{BASE}/configs/languages/pt.json"
    es_file = f"{BASE}/configs/languages/es.json"
    us_file = f"{BASE}/configs/languages/en.json"
    with open(pt_file, 'w', encoding='utf-8') as f:
        json.dump(pt, f, indent=2, ensure_ascii=False)
    
    with open(es_file, 'w', encoding='utf-8') as f:
        json.dump(es, f, indent=2, ensure_ascii=False)

    with open(us_file, 'w', encoding='utf-8') as f:
        json.dump(en, f, indent=2, ensure_ascii=False)

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
                ft.Image(
                    src="icon.png",
                    width=96,
                    height=96,
                    fit="contain",
                ),
                ft.Text(
                    "Fleting Framework",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Micro Framework MVC for Flet",
                    size=16,
                    color=ft.Colors.GREY_600,
                ),
                ft.Text(
                    "Build modern applications with a clear architecture, "
                    "Dynamic routing and productive CLI.",
                    size=14,
                    text_align=ft.TextAlign.CENTER,
                    width=420,
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=16,
                    controls=[
                        ft.FilledButton(
                            "Settings",
                            icon=ft.Icons.SETTINGS,
                            on_click=lambda e: self.router.navigate("/settings"),
                        ),
                        ft.OutlinedButton(
                            "Create new page",
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

class SettingsView:
    def __init__(self, page, router):
        self.page = page
        self.router = router
        self.controller = SettingsController()
    
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
    (BASE / ".fleting").write_text("fleting-project", encoding="utf-8")

    create_file(BASE / "main.py", """
import flet as ft
from configs.app_config import AppConfig
from core.logger import get_logger
from core.error_handler import GlobalErrorHandler
import runtime_imports 

logger = get_logger("App")

def main(page: ft.Page):
    try:
        page.assets_dir = "assets"

        if page.platform in (ft.PagePlatform.WINDOWS, ft.PagePlatform.LINUX, ft.PagePlatform.MACOS):
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

ft.app(main)

""")
    create_file(BASE / "runtime_imports.py", """
from views.pages.home_view import HomeView
from views.pages.settings_view import SettingsView
from views.pages.help_view import HelpView
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
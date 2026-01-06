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
    /"/"/"Carrega uma view dinamicamente/"/"/"
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
    /"/"/"
    Controller for settings page
    /"/"/"

    def __init__(self, model=None):
        self.model = model or SettingsModel()

    def get_title(self):
        return "Settings"
""")

    create_file(BASE / "controllers/help_controller.py", """
from models.help_model import HelpModel

class HelpController:
    /"/"/"
    Controller for help page
    /"/"/"

    def __init__(self, model=None):
        self.model = model or HelpModel()

    def get_title(self):
        return "Help"
""")

    # =========================
    # BASIC models
    # =========================
    create_file(BASE / "model/help_model.py", """
class HelpModel:
    def __init__(self):
        pass
""")

    create_file(BASE / "model/settings_model.py", """
class SettingsModel:
    def __init__(self):
        pass
""")

    # =========================
    # CLI BÁSICO
    # =========================
    create_file(BASE / "cli/cli.py", """
import sys
from fleting.cli.commands.init import handle_init
from fleting.cli.commands.run import handle_run
from fleting.cli.commands.info import handle_info
from fleting.cli.commands.create import handle_create
from fleting.cli.commands.delete import handle_delete

def print_help():
    print(\"\"\"
Fleting CLI

Uso:
  fleting init
      Inicializa um novo projeto Fleting

  fleting create page <nome>
      Cria uma nova página (model + controller + view)

  fleting create view <nome>
  fleting create model <nome>
  fleting create controller <nome>

  fleting delete page <nome>
  fleting delete view <nome>
  fleting delete model <nome>
  fleting delete controller <nome>
\"\"\")

def main():
    
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print_help()
        return

    command = args[0]
    
    try:
        if command == "init":
            handle_init()
        elif command == "run":
            handle_run()
        elif command == "info":
            handle_info()
        elif command == "create":
            handle_create(args[1:])
        elif command == "delete":
            handle_delete(args[1:])
        else:
            print(f"Comando desconhecido: {command}")
            print_help()

    except Exception as e:
        print("Erro ao executar comando CLI:", str(e))

if __name__ == "__main__":
    main()
""")

    create_file(BASE / "cli/commands/info.py", """
import platform
import sys
from importlib import metadata

BANNER = r\"\"\"
 ______ _      _   _             
|  ____| |    | | (_)            
| |__  | | ___| |_ _ _ __   __ _ 
|  __| | |/ _ \ __| | '_ \ / _` |
| |    | |  __/ |_| | | | | (_| |
|_|    |_|\___|\__|_|_| |_|\__, |
                            __/ |
                           |___/
\"\"\"

def _get_version(pkg_name: str):
    try:
        return metadata.version(pkg_name)
    except metadata.PackageNotFoundError:
        return "não instalado"

def handle_info():
    python_version = sys.version.split()[0]
    system = f"{platform.system()} {platform.release()}"

    flet_version = _get_version("flet")
    fleting_version = _get_version("fleting")

    print(BANNER)
    print("🚀 Fleting Framework\n")

    print("📦 Ambiente\n")
    print(f"🧠 Python        : {python_version}")
    print(f"🖥️  Sistema      : {system}")
    print(f"🧩 Flet          : {flet_version}")
    print(f"🚀 Fleting       : {fleting_version}")

    print("\n📚 Bibliotecas instaladas:")
    for dist in sorted(metadata.distributions(), key=lambda d: d.metadata["Name"].lower()):
        name = dist.metadata["Name"]
        version = dist.version
        print(f"  - {name}=={version}")

    print("\n✅ Ambiente pronto para uso.\n")
""")

    create_file(BASE / "cli/commands/run.py", """
import subprocess
import sys
import shutil
from pathlib import Path

def handle_run():
    project_root = Path.cwd()
    app_path = project_root / "fleting" / "app.py"

    if not shutil.which("flet"):
        print("❌ Flet não está instalado no ambiente")
        print("👉 pip install flet")
        return

    if not app_path.exists():
        print("❌ fleting/app.py não encontrado.")
        print("👉 Execute 'fleting init' primeiro.")
        return

    print("🚀 Iniciando aplicação Fleting...\n")

    try:
        subprocess.run(
            ["flet", "run", str(app_path)],
            check=True
        )
    except subprocess.CalledProcessError:
        print("❌ Erro ao executar o app com Flet")
""")

    create_file(BASE / "cli/commands/create.py", """
from pathlib import Path

def get_project_root() -> Path:
    /"/"/"
    Diretório onde o usuário executou o comando fleting
    /"/"/"
    return Path.cwd()

def get_fleting_base() -> Path:
    /"/"/"
    Pasta base do framework dentro do projeto
    /"/"/"
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
    /"/"/"
    Controller for {name} page
    /"/"/"

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

    content = f/"/"/"import flet as ft
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
/"/"/"

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

    content = f/"/"/"class {class_name}:
    def __init__(self):
        pass
/"/"/"

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

    route_block = f/"/"/"
    {{
        "path": "/{name}",
        "view": "views.pages.{name}_view.{name.capitalize()}View",
        "label": "{name.capitalize()}",
        "icon": ft.Icons.CHEVRON_RIGHT,
        "show_in_top": True,
        "show_in_bottom": False,
    }},
/"/"/"

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

    content = f/"/"/"import flet as ft
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
/"/"/"
    path.write_text(content, encoding="utf-8")
    print(f"Page criada com sucesso: {name}")

""")

    create_file(BASE / "cli/commands/delete.py", """
from pathlib import Path
from core.logger import get_logger

logger = get_logger("CLI.Delete")

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
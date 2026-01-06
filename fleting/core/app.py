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

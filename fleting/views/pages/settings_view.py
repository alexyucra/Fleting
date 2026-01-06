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

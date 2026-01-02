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

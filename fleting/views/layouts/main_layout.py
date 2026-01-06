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

    # def _on_nav_change(self, e):
    #     if not self.router:
    #         return

    #     if e.control.selected_index == 0:
    #         self.router.navigate("/")
    #     elif e.control.selected_index == 1:
    #         self.router.navigate("/settings")

    # ---------- LANGUAGE ----------
    # def _change_language(self, lang):
    #     I18n.load(lang)
    #     if self.router:
    #         self.router.navigate(self.router.current_route)

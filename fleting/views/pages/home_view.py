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
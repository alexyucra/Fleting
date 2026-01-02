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
                alignment=ft.alignment.center,
            )
        )
        page.update()

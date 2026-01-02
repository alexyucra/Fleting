
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

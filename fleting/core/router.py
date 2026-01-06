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

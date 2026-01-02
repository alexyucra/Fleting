"""
Configuração de rotas com lazy loading para evitar circular imports
"""
import importlib

# Mapeamento rota -> módulo.classe
ROUTE_MAP = {
    "/": "views.pages.home_view.HomeView",
    # "/login": "views.pages.login_view.LoginView",
    # "/dashboard": "views.pages.dashboard_view.DashboardView",
}

def load_view(view_path: str):
    """Carrega uma view dinamicamente"""
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

    for route_path, view_path in ROUTE_MAP.items():
        def create_view_lambda(path=view_path):
            # 🚨 lambda aceita page e router
            return lambda page, router: load_view(path)(page, router).render()

        routes[route_path] = create_view_lambda()

    return routes

routes = get_routes()
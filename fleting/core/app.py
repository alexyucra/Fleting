import flet as ft
from core.responsive import get_device_type
from core.state import AppState

class FletingApp:
    def __init__(self, page):
        self.page = page
        AppState.device = AppState.initial_device
        self.page.on_resize = self.on_resize

    def on_resize(self, e):
        real_device = get_device_type(self.page.width)

        # Evita sobrescrever no primeiro frame falso
        if not AppState.initialized:
            AppState.initialized = True

        AppState.device = real_device
        self.page.update()

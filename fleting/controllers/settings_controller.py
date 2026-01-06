from models.settings_model import SettingsModel

class SettingsController:
    """
    Controller for settings page
    """

    def __init__(self, model=None):
        self.model = model or SettingsModel()

    def get_title(self):
        return "Settings"

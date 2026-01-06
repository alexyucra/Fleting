from models.help_model import HelpModel

class HelpController:
    """
    Controller for help page
    """

    def __init__(self, model=None):
        self.model = model or HelpModel()

    def get_title(self):
        return "Help"

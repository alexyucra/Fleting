
import json
from pathlib import Path
from core.state import AppState
from core.logger import get_logger
logger = get_logger("I18n")

class I18n:
    translations = {}

    @classmethod
    def load(cls, lang):
        current_file = Path(__file__).resolve()
        base_path = current_file.parent.parent
        path = base_path / "configs" / "languages" / f"{lang}.json"
        cls.translations = json.loads(path.read_text(encoding="utf-8"))
        logger.info(f"Idioma carregado: {lang}")
        AppState.language = lang

    @classmethod
    def t(cls, key):
        value = cls.translations
        for k in key.split("."):
            value = value.get(k)
            if value is None:
                return key
        return value

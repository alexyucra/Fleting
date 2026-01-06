"""
Configuração de persistência do Fleting
"""

from pathlib import Path

BASE_DIR = Path.cwd()

# =========================
# DATABASE CONFIG
# =========================

DATABASE = {
    # 🔹 sqlite | mysql
    "ENGINE": "sqlite",

    # =====================
    # SQLITE (default)
    # =====================
    "SQLITE": {
        "PATH": BASE_DIR / "data" / "app.db",
    },

    # =====================
    # MYSQL (opcional)
    # =====================
    # "MYSQL": {
    #     "HOST": "localhost",
    #     "PORT": 3306,
    #     "USER": "root",
    #     "PASSWORD": "password",
    #     "DATABASE": "fleting",
    # },
}
# fleting/cli/templates/defaults.py
"""Migration e seed iniciais. Funcionam em SQLite e MySQL/MariaDB."""

INITIAL_MIGRATION = """# Migration inicial (SQLite e MySQL/MariaDB)
from core.database import is_mysql


def up(db):
    pk = "INT AUTO_INCREMENT PRIMARY KEY" if is_mysql() else "INTEGER PRIMARY KEY AUTOINCREMENT"
    cur = db.cursor()
    cur.execute(f\'\'\'
        CREATE TABLE IF NOT EXISTS users (
            id {pk},
            username VARCHAR(255) UNIQUE,
            password VARCHAR(255)
        )
    \'\'\')
    cur.close()


def down(db):
    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.close()
"""

INITIAL_SEED = """# Seed inicial (SQLite e MySQL/MariaDB)
import hashlib
import os
import secrets

from core.database import is_mysql, placeholder


def hash_password(raw: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", raw.encode(), salt.encode(), 200_000).hex()
    return f"pbkdf2_sha256$200000${salt}${digest}"


def run(db):
    raw = os.environ.get("FLETING_ADMIN_PASSWORD")
    if not raw:
        print("⚠️  FLETING_ADMIN_PASSWORD not set; admin user not created.")
        return
    verb = "INSERT IGNORE" if is_mysql() else "INSERT OR IGNORE"
    p = placeholder()
    cur = db.cursor()
    cur.execute(
        f"{verb} INTO users (username, password) VALUES ({p}, {p})",
        ("admin", hash_password(raw)),
    )
    cur.close()
"""

# arquivos padrão que dependem da engine (usados na troca de engine)
ENGINE_AGNOSTIC_MARKER = "from core.database import is_mysql"
DEFAULT_FILES = {
    "migrations/001_initial.py": INITIAL_MIGRATION,
    "seeds/initial.py": INITIAL_SEED,
}

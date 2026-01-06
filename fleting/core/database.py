import sqlite3
# import mysql.connector  # opcional
from configs.database import DATABASE
from pathlib import Path

_connection = None


def get_connection():
    global _connection

    if _connection:
        return _connection

    engine = DATABASE["ENGINE"]

    if engine == "sqlite":
        db_path = DATABASE["SQLITE"]["PATH"]
        db_path.parent.mkdir(parents=True, exist_ok=True)

        _connection = sqlite3.connect(db_path)
        return _connection

    # elif engine == "mysql":
    #     cfg = DATABASE["MYSQL"]
    #     _connection = mysql.connector.connect(
    #         host=cfg["HOST"],
    #         port=cfg["PORT"],
    #         user=cfg["USER"],
    #         password=cfg["PASSWORD"],
    #         database=cfg["DATABASE"],
    #     )
    #     return _connection

    raise ValueError(f"Database engine não suportado: {engine}")

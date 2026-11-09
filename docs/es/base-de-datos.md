# 🗄️ Bases de datos

Fleting soporta **SQLite** (por defecto) y **MySQL / MariaDB**. El mismo código de models, migraciones y seeds funciona en ambos motores; solo cambia la configuración.

| Motor | Estado | Driver | Instalación | Uso recomendado |
|---|---|---|---|---|
| SQLite | ✅ Estable | `sqlite3` (incluido) | — | Desarrollo, apps embebidas/móviles |
| MySQL 8 | ✅ Estable | `mysql-connector-python` | `pip install "fleting[mysql]"` | Producción, apps web |
| MariaDB 10.6+ / 11 | ✅ Estable | `PyMySQL` (recomendado) o `mysql-connector-python` | `pip install "fleting[mariadb]"` | Producción |
| SQL Server | 🔄 Próximamente | — | — | Integraciones corporativas |

---

## Elegir el motor

=== "Proyecto nuevo"

    ```bash
    fleting init miapp            # SQLite
    fleting init miapp --mysql    # MySQL / MariaDB
    ```

=== "Proyecto existente"

    ```bash
    fleting db init --mysql       # cambia a MySQL / MariaDB
    fleting db init --sqlite      # vuelve a SQLite
    ```

    Al cambiar de motor, Fleting:

    - modifica `"ENGINE"` en `configs/database.py`;
    - guarda `core/database.py` y `core/migrations.py` como `*.py.bak` y genera las versiones del nuevo motor;
    - regenera `migrations/001_initial.py` y `seeds/initial.py` **solo** si son los archivos por defecto de versiones antiguas (también con respaldo `.bak`). Sus demás archivos no se modifican.

Dentro de un proyecto, `fleting --help` muestra los comandos del motor en uso.

---

## Configuración (`configs/database.py`)

```python
import os
# ENGINE: "sqlite" | "mysql"
DATABASE = {
    "ENGINE": "sqlite",

    "SQLITE": {
        "PATH": "data/fleting.db"
    },

    "MYSQL": {
        "DRIVER": os.environ.get("FLETING_DB_DRIVER", "mysql-connector"),  # o "pymysql" (MariaDB)
        "HOST": os.environ.get("FLETING_DB_HOST", "localhost"),
        "PORT": int(os.environ.get("FLETING_DB_PORT", "3306")),
        "USER": os.environ.get("FLETING_DB_USER", "root"),
        "PASSWORD": os.environ.get("FLETING_DB_PASSWORD", ""),
        "NAME": os.environ.get("FLETING_DB_NAME", "fleting"),
        "OPTIONS": {
            "charset": "utf8mb4",
            "collation": "utf8mb4_general_ci"
        }
    }
}
```

!!! warning "No guarde contraseñas en el código"
    Use las variables de entorno de abajo. Mantenga la línea `"ENGINE": "..."` como texto literal: la CLI la lee para detectar el motor.

### Variables de entorno

| Variable | Por defecto | Uso |
|---|---|---|
| `FLETING_DB_HOST` | `localhost` | Servidor MySQL/MariaDB |
| `FLETING_DB_PORT` | `3306` | Puerto |
| `FLETING_DB_USER` | `root` | Usuario |
| `FLETING_DB_PASSWORD` | *(vacío)* | Contraseña |
| `FLETING_DB_NAME` | `fleting` | Nombre de la base |
| `FLETING_DB_DRIVER` | `mysql-connector` | `mysql-connector` o `pymysql` |
| `FLETING_ADMIN_PASSWORD` | — | Contraseña del usuario `admin` creado por `fleting db seed` |

=== "PowerShell"

    ```powershell
    $env:FLETING_DB_PASSWORD = "micontraseña"
    $env:FLETING_DB_DRIVER = "pymysql"
    ```

=== "CMD"

    ```bat
    set FLETING_DB_PASSWORD=micontraseña
    set FLETING_DB_DRIVER=pymysql
    ```

=== "Linux / macOS"

    ```bash
    export FLETING_DB_PASSWORD=micontraseña
    export FLETING_DB_DRIVER=pymysql
    ```

---

## MySQL y MariaDB con Docker

```bash
# MySQL 8
docker run -d --name fleting-mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=fleting -p 3306:3306 mysql:8

# MariaDB 11
docker run -d --name fleting-mariadb -e MARIADB_ROOT_PASSWORD=root -e MARIADB_DATABASE=fleting -p 3307:3306 mariadb:11
```

!!! tip "MariaDB"
    `mysql-connector-python` 8.0.30+ envía la collation `utf8mb4_0900_ai_ci`, que no existe en MariaDB. Fleting ya usa `utf8mb4_general_ci` por defecto, pero el driver recomendado para MariaDB es **PyMySQL** (`FLETING_DB_DRIVER=pymysql`).

---

## Migraciones y seeds

| Comando | Qué hace |
|---|---|
| `fleting db init` | Crea `migrations/`, `seeds/`, `data/` y `core/migrations.py` |
| `fleting db migrate` | Aplica las migraciones pendientes (registradas en `_fleting_migrations`) |
| `fleting db make <nombre>` | Crea `migrations/00N_<nombre>.py` |
| `fleting db rollback` | Revierte la última migración (`down`) |
| `fleting db status` | Lista migraciones aplicadas y pendientes |
| `fleting db seed` | Ejecuta `run(db)` de cada archivo en `seeds/` |

Una migración recibe la conexión en `up(db)` / `down(db)`. Use **cursor**, que funciona en todos los motores:

```python
from core.database import is_mysql

def up(db):
    pk = "INT AUTO_INCREMENT PRIMARY KEY" if is_mysql() else "INTEGER PRIMARY KEY AUTOINCREMENT"
    cur = db.cursor()
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS productos (
            id {pk},
            nombre VARCHAR(255),
            precio DECIMAL(10, 2)
        )
    """)
    cur.close()

def down(db):
    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS productos")
    cur.close()
```

### Usuario admin del seed

`seeds/initial.py` solo crea el usuario `admin` si `FLETING_ADMIN_PASSWORD` está definida. La contraseña se guarda con hash **PBKDF2-SHA256** (`pbkdf2_sha256$200000$<salt>$<hash>`), nunca en texto plano. Ejecutar el seed otra vez no duplica el usuario.

!!! danger "Código del proyecto"
    `db migrate`, `db seed` y `list routes` importan y ejecutan archivos Python del proyecto (`migrations/`, `seeds/`, `configs/routes.py`). Ejecútelos solo en proyectos confiables.

---

## ORM

```python
from core.base_model import BaseModel

class ProductosModel(BaseModel):
    table_name = "productos"
```

| Método | Retorno |
|---|---|
| `Model.all()` | lista de dicts |
| `Model.first()` | dict o `None` |
| `Model.find(id)` | dict o `None` |
| `Model.where(campo=valor, ...)` | lista de dicts |
| `Model.count()` / `Model.exists(**filtros)` | `int` / `bool` |
| `Model.create(**datos)` | dict creado |
| `obj.save()` | inserta (sin `id`) o actualiza (con `id`) |
| `obj.delete()` | elimina por `id` |
| `Model.with_("relacion").all()` | carga `ForeignKey` / `HasMany` |

Los nombres de tabla y columna se validan (`[A-Za-z_][A-Za-z0-9_]*`); los valores siempre van como parámetros. Algo como `Model.where(**{"id=1 OR 1": 1})` lanza `ValueError`.

### Transacciones y conexión

```python
from core.database import transaction, close_connection

with transaction() as conn:          # commit al final, rollback si hay error
    cur = conn.cursor()
    cur.execute("UPDATE productos SET precio = precio * 1.1")

close_connection()                   # la app ya lo llama al cerrar
```

### Generar models desde la base

```bash
fleting db model pull                  # todas las tablas
fleting db model pull productos        # una tabla
fleting db model pull productos --force
```

---

## Consola (`fleting shell`)

| Helper | SQLite | MySQL / MariaDB |
|---|---|---|
| `tables()` | ✅ | ✅ |
| `query(sql)` | SELECT → dicts | SELECT → dicts; INSERT/UPDATE/DELETE → commit + nº de filas |
| `table("t")` | ✅ | ✅ (`limit=200`) |
| `describe("t")` | — | ✅ |
| `models()` / `<Model>.all()` | ✅ | ✅ |
| `conn` / `db` | conexión | conexión |

```text
>>> tables()
['_fleting_migrations', 'users']
>>> query("UPDATE users SET username=%s WHERE id=%s", ("adm", 1))
✔ 1 row(s) affected
```

---

## Diagnóstico

`fleting doctor` revisa el motor configurado, si el driver MySQL está instalado y si el seed aún usa la contraseña por defecto antigua.

## Problemas comunes

| Error | Causa / solución |
|---|---|
| `MySQL support requires: pip install "fleting[mysql]"` | Instale el driver (o `fleting[mariadb]` con `DRIVER=pymysql`) |
| `Unknown collation: utf8mb4_0900_ai_ci` | MariaDB + connector antiguo: use `FLETING_DB_DRIVER=pymysql` |
| `Access denied for user` | Revise `FLETING_DB_USER` / `FLETING_DB_PASSWORD` |
| `Unknown database` | Cree la base (`CREATE DATABASE fleting`) o ajuste `FLETING_DB_NAME` |
| `Can't connect to MySQL server` | Servidor detenido o puerto incorrecto (`FLETING_DB_PORT`) |
| `'Connection' object has no attribute 'execute'` | Migración/seed antiguo con `db.execute`: use `db.cursor().execute(...)` |

# 🗄️ Databases

Fleting supports **SQLite** (default) and **MySQL / MariaDB**. The same models, migrations and seeds work on both engines; only the configuration changes.

| Engine | Status | Driver | Install | Best for |
|---|---|---|---|---|
| SQLite | ✅ Stable | `sqlite3` (built in) | — | Development, embedded/mobile apps |
| MySQL 8 | ✅ Stable | `mysql-connector-python` | `pip install "fleting[mysql]"` | Production, web apps |
| MariaDB 10.6+ / 11 | ✅ Stable | `PyMySQL` (recommended) or `mysql-connector-python` | `pip install "fleting[mariadb]"` | Production |
| SQL Server | 🔄 Coming soon | — | — | Enterprise integrations |

---

## Choosing the engine

=== "New project"

    ```bash
    fleting init myapp            # SQLite
    fleting init myapp --mysql    # MySQL / MariaDB
    ```

=== "Existing project"

    ```bash
    fleting db init --mysql       # switch to MySQL / MariaDB
    fleting db init --sqlite      # back to SQLite
    ```

    When switching, Fleting:

    - updates `"ENGINE"` in `configs/database.py`;
    - saves `core/database.py` and `core/migrations.py` as `*.py.bak` and generates the new engine's versions;
    - regenerates `migrations/001_initial.py` and `seeds/initial.py` **only** if they are the default files from older versions (also backed up as `.bak`). Your other files are left untouched.

Inside a project, `fleting --help` shows the commands for the engine in use.

---

## Configuration (`configs/database.py`)

```python
import os
# ENGINE: "sqlite" | "mysql"
DATABASE = {
    "ENGINE": "sqlite",

    "SQLITE": {
        "PATH": "data/fleting.db"
    },

    "MYSQL": {
        "DRIVER": os.environ.get("FLETING_DB_DRIVER", "mysql-connector"),  # or "pymysql" (MariaDB)
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

!!! warning "Keep passwords out of the code"
    Use the environment variables below. Keep the `"ENGINE": "..."` line as a literal string: the CLI reads it to detect the engine.

### Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `FLETING_DB_HOST` | `localhost` | MySQL/MariaDB server |
| `FLETING_DB_PORT` | `3306` | Port |
| `FLETING_DB_USER` | `root` | User |
| `FLETING_DB_PASSWORD` | *(empty)* | Password |
| `FLETING_DB_NAME` | `fleting` | Database name |
| `FLETING_DB_DRIVER` | `mysql-connector` | `mysql-connector` or `pymysql` |
| `FLETING_ADMIN_PASSWORD` | — | Password for the `admin` user created by `fleting db seed` |

=== "PowerShell"

    ```powershell
    $env:FLETING_DB_PASSWORD = "mypassword"
    $env:FLETING_DB_DRIVER = "pymysql"
    ```

=== "CMD"

    ```bat
    set FLETING_DB_PASSWORD=mypassword
    set FLETING_DB_DRIVER=pymysql
    ```

=== "Linux / macOS"

    ```bash
    export FLETING_DB_PASSWORD=mypassword
    export FLETING_DB_DRIVER=pymysql
    ```

---

## MySQL and MariaDB with Docker

```bash
# MySQL 8
docker run -d --name fleting-mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=fleting -p 3306:3306 mysql:8

# MariaDB 11
docker run -d --name fleting-mariadb -e MARIADB_ROOT_PASSWORD=root -e MARIADB_DATABASE=fleting -p 3307:3306 mariadb:11
```

```bash
docker ps                                   # is it running?
docker logs fleting-mysql
docker exec -it fleting-mysql mysql -uroot -proot
docker rm -f fleting-mysql                  # stop and remove
```

!!! tip "MariaDB"
    `mysql-connector-python` 8.0.30+ sends the `utf8mb4_0900_ai_ci` collation, which MariaDB does not have. Fleting already defaults to `utf8mb4_general_ci`, but the recommended MariaDB driver is **PyMySQL** (`FLETING_DB_DRIVER=pymysql`).

---

## Migrations and seeds

| Command | What it does |
|---|---|
| `fleting db init` | Creates `migrations/`, `seeds/`, `data/` and `core/migrations.py` |
| `fleting db migrate` | Applies pending migrations (tracked in `_fleting_migrations`) |
| `fleting db make <name>` | Creates `migrations/00N_<name>.py` |
| `fleting db rollback` | Reverts the last migration (`down`) |
| `fleting db status` | Lists applied and pending migrations |
| `fleting db seed` | Runs `run(db)` from every file in `seeds/` |

A migration receives the connection in `up(db)` / `down(db)`. Use a **cursor**, which works on every engine:

```python
from core.database import is_mysql

def up(db):
    pk = "INT AUTO_INCREMENT PRIMARY KEY" if is_mysql() else "INTEGER PRIMARY KEY AUTOINCREMENT"
    cur = db.cursor()
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS products (
            id {pk},
            name VARCHAR(255),
            price DECIMAL(10, 2)
        )
    """)
    cur.close()

def down(db):
    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS products")
    cur.close()
```

### Seed admin user

`seeds/initial.py` only creates the `admin` user if `FLETING_ADMIN_PASSWORD` is set. The password is stored as a **PBKDF2-SHA256** hash (`pbkdf2_sha256$200000$<salt>$<hash>`), never in plain text. Running the seed again does not duplicate the user.

!!! danger "Project code"
    `db migrate`, `db seed` and `list routes` import and run Python files from the project (`migrations/`, `seeds/`, `configs/routes.py`). Only run them on projects you trust.

---

## ORM

```python
from core.base_model import BaseModel

class ProductsModel(BaseModel):
    table_name = "products"
```

| Method | Returns |
|---|---|
| `Model.all()` | list of dicts |
| `Model.first()` | dict or `None` |
| `Model.find(id)` | dict or `None` |
| `Model.where(field=value, ...)` | list of dicts |
| `Model.count()` / `Model.exists(**filters)` | `int` / `bool` |
| `Model.create(**data)` | created dict |
| `obj.save()` | inserts (no `id`) or updates (with `id`) |
| `obj.delete()` | deletes by `id` |
| `Model.with_("relation").all()` | loads `ForeignKey` / `HasMany` |

Table and column names are validated (`[A-Za-z_][A-Za-z0-9_]*`); values are always passed as parameters. Something like `Model.where(**{"id=1 OR 1": 1})` raises `ValueError`.

### Transactions and connection

```python
from core.database import transaction, close_connection

with transaction() as conn:          # commit at the end, rollback on error
    cur = conn.cursor()
    cur.execute("UPDATE products SET price = price * 1.1")

close_connection()                   # the app already calls this on exit
```

### Generate models from the database

```bash
fleting db model pull                 # every table
fleting db model pull products        # one table
fleting db model pull products --force
```

---

## Console (`fleting shell`)

| Helper | SQLite | MySQL / MariaDB |
|---|---|---|
| `tables()` | ✅ | ✅ |
| `query(sql)` | SELECT → dicts | SELECT → dicts; INSERT/UPDATE/DELETE → commit + row count |
| `table("t")` | ✅ | ✅ (`limit=200`) |
| `describe("t")` | — | ✅ |
| `models()` / `<Model>.all()` | ✅ | ✅ |
| `conn` / `db` | connection | connection |

```text
>>> tables()
['_fleting_migrations', 'users']
>>> query("UPDATE users SET username=%s WHERE id=%s", ("adm", 1))
✔ 1 row(s) affected
```

---

## Diagnostics

`fleting doctor` checks the configured engine, whether the MySQL driver is installed and whether the seed still uses the old default password.

## Troubleshooting

| Error | Cause / fix |
|---|---|
| `MySQL support requires: pip install "fleting[mysql]"` | Install the driver (or `fleting[mariadb]` with `DRIVER=pymysql`) |
| `Unknown collation: utf8mb4_0900_ai_ci` | MariaDB + old connector: use `FLETING_DB_DRIVER=pymysql` |
| `Access denied for user` | Check `FLETING_DB_USER` / `FLETING_DB_PASSWORD` |
| `Unknown database` | Create it (`CREATE DATABASE fleting`) or set `FLETING_DB_NAME` |
| `Can't connect to MySQL server` | Server stopped or wrong port (`FLETING_DB_PORT`) |
| `'Connection' object has no attribute 'execute'` | Old migration/seed using `db.execute`: use `db.cursor().execute(...)` |

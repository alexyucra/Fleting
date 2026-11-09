# 🧭 Step-by-step examples

Complete walkthroughs using the CLI. Each example starts from scratch.

> In every example, first activate your virtual environment and install: `pip install fleting`.

---

## 1. First app (SQLite)

```bash
fleting init shop
cd shop
fleting run
```

Result: an app with **Home**, **Settings** and **Help** pages, responsive layout and i18n (pt, en, es).

Check the structure:

```bash
fleting doctor
```
```text
  ✔ .fleting found
  ✔ main.py found
  ✔ 3 route(s) checked
  ✔ Database engine: sqlite

0 error(s), 0 warning(s)
```

---

## 2. Create a full page

```bash
fleting create page products
```

Generates:

| File | Class |
|---|---|
| `app/models/products_model.py` | `ProductsModel` |
| `app/controllers/products_controller.py` | `ProductsController` |
| `app/views/pages/products_view.py` | `ProductsView` |
| `configs/routes.py` | `/products` route in the menu |

Multi-word names use *snake_case*: `fleting create page user_profile` → `UserProfileView`, `UserProfileController`, `UserProfileModel`.

```bash
fleting list pages      # model / controller / view of each page
fleting list routes     # registered routes
fleting run             # the page shows up in the menu
```

!!! note "Valid names"
    Lowercase letters, digits and `_`, starting with a letter. `my-page`, `1abc` and reserved words (`class`) are rejected.

---

## 3. Create standalone components

```bash
fleting create model customer
fleting create controller customer
fleting create view customer
```

A view created this way gets **no** route. `fleting doctor` warns:

```text
  ⚠️  View customer_view.py has no route in configs/routes.py
```

---

## 4. Delete a page

```bash
fleting delete page products
```

Removes the model, controller, view **and** the `/products` route. Works from any subfolder of the project (for example, inside `app/views`).

```bash
fleting delete view customer       # only the view
```

---

## 5. SQLite: table, data and queries

```bash
fleting db init
fleting db make products
```

Edit `migrations/002_products.py`:

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

Apply it and create the admin user:

=== "PowerShell"

    ```powershell
    fleting db migrate
    $env:FLETING_ADMIN_PASSWORD = "StrongPass123"
    fleting db seed
    fleting db status
    ```

=== "Linux / macOS"

    ```bash
    fleting db migrate
    FLETING_ADMIN_PASSWORD=StrongPass123 fleting db seed
    fleting db status
    ```

Generate the model from the table and use the ORM:

```bash
fleting db model pull products
fleting shell
```
```text
>>> tables()
['_fleting_migrations', 'sqlite_sequence', 'users', 'products']
>>> ProductsModel.create(name="Pen", price=2.5)
{'id': 1, 'name': 'Pen', 'price': 2.5}
>>> ProductsModel.where(name="Pen")
[{'id': 1, 'name': 'Pen', 'price': 2.5}]
>>> table("products")
>>> quit()
```

Undo the last migration:

```bash
fleting db rollback
```

---

## 6. Use the ORM in a controller

```python
# app/controllers/products_controller.py
from app.models.products_model import ProductsModel

class ProductsController:
    def list(self):
        return ProductsModel.all()

    def add(self, name: str, price: float):
        return ProductsModel.create(name=name, price=price)
```

```python
# app/views/pages/products_view.py (inside render)
items = [ft.Text(f"{p['name']} — $ {p['price']}") for p in self.controller.list()]
content = ft.Column(controls=items, spacing=8)
```

---

## 7. MySQL project

```bash
docker run -d --name fleting-mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=fleting -p 3306:3306 mysql:8
pip install "fleting[mysql]"

fleting init shop --mysql
cd shop
```

Configure the connection:

=== "PowerShell"

    ```powershell
    $env:FLETING_DB_PASSWORD = "root"
    $env:FLETING_ADMIN_PASSWORD = "StrongPass123"
    ```

=== "Linux / macOS"

    ```bash
    export FLETING_DB_PASSWORD=root
    export FLETING_ADMIN_PASSWORD=StrongPass123
    ```

```bash
fleting db init
fleting db migrate
fleting db seed
fleting doctor
fleting shell
```
```text
Fleting Console (MySQL 8.4.x)
>>> describe("users")
>>> query("SELECT COUNT(*) n FROM users")
[{'n': 1}]
```

---

## 8. MariaDB project

```bash
docker run -d --name fleting-mariadb -e MARIADB_ROOT_PASSWORD=root -e MARIADB_DATABASE=fleting -p 3307:3306 mariadb:11
pip install "fleting[mariadb]"

fleting init shop --mysql
cd shop
```

=== "PowerShell"

    ```powershell
    $env:FLETING_DB_DRIVER = "pymysql"
    $env:FLETING_DB_PORT = "3307"
    $env:FLETING_DB_PASSWORD = "root"
    ```

=== "Linux / macOS"

    ```bash
    export FLETING_DB_DRIVER=pymysql FLETING_DB_PORT=3307 FLETING_DB_PASSWORD=root
    ```

```bash
fleting db init && fleting db migrate
fleting shell          # the banner shows "Fleting Console (MariaDB 11.x)"
```

---

## 9. Move an existing SQLite project to MySQL

```bash
cd shop
pip install "fleting[mysql]"
fleting db init --mysql
```
```text
Backup: core/database.py → database.py.bak
Backup: core/migrations.py → migrations.py.bak
Engine switched: sqlite → mysql
```

Then, with the `FLETING_DB_*` variables set:

```bash
fleting db migrate
fleting db seed
```

!!! warning "Data"
    Switching engines does **not copy data** from SQLite to MySQL; it only reconfigures the project and re-applies the migrations on the new database. Your own migrations that use SQLite-only syntax need adjusting (see example 5).

To go back: `fleting db init --sqlite`.

---

## 10. Diagnostics and debugging

```bash
fleting doctor               # structure, routes, driver, seed
fleting info                 # versions and environment
```

CLI errors show only the message. To see the full traceback:

=== "PowerShell"

    ```powershell
    $env:FLETING_DEBUG = "1"; fleting db migrate
    ```

=== "Linux / macOS"

    ```bash
    FLETING_DEBUG=1 fleting db migrate
    ```

Exit codes: `0` success, `1` error (including `doctor` with errors), `2` unknown command.

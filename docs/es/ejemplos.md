# 🧭 Ejemplos paso a paso

Recorridos completos con la CLI. Cada ejemplo empieza desde cero.

> En todos los ejemplos, active antes el entorno virtual ([Entorno](enviroment.md)) e instale: `pip install fleting`.

---

## 1. Primera app (SQLite)

```bash
fleting init tienda
cd tienda
fleting run
```

Resultado: app con páginas **Home**, **Settings** y **Help**, layout responsive e i18n (pt, en, es).

Para revisar la estructura:

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

## 2. Crear una página completa

```bash
fleting create page productos
```

Genera:

| Archivo | Clase |
|---|---|
| `app/models/productos_model.py` | `ProductosModel` |
| `app/controllers/productos_controller.py` | `ProductosController` |
| `app/views/pages/productos_view.py` | `ProductosView` |
| `configs/routes.py` | ruta `/productos` en el menú |

Los nombres con varias palabras usan *snake_case*: `fleting create page user_profile` → `UserProfileView`, `UserProfileController`, `UserProfileModel`.

```bash
fleting list pages      # model / controller / view de cada página
fleting list routes     # rutas registradas
fleting run             # la página aparece en el menú
```

!!! note "Nombres válidos"
    Minúsculas, números y `_`, empezando por letra. `mi-pagina`, `1abc` y palabras reservadas (`class`) se rechazan.

---

## 3. Crear componentes sueltos

```bash
fleting create model cliente
fleting create controller cliente
fleting create view cliente
```

Una view creada así **no** recibe ruta. `fleting doctor` avisa:

```text
  ⚠️  View cliente_view.py has no route in configs/routes.py
```

---

## 4. Eliminar una página

```bash
fleting delete page productos
```

Elimina model, controller, view **y** la ruta `/productos`. Funciona desde cualquier subcarpeta del proyecto (por ejemplo, dentro de `app/views`).

```bash
fleting delete view cliente        # solo la view
```

---

## 5. SQLite: tabla, datos y consultas

```bash
fleting db init
fleting db make productos
```

Edite `migrations/002_productos.py`:

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

Aplique y cree el admin:

=== "PowerShell"

    ```powershell
    fleting db migrate
    $env:FLETING_ADMIN_PASSWORD = "ClaveFuerte123"
    fleting db seed
    fleting db status
    ```

=== "Linux / macOS"

    ```bash
    fleting db migrate
    FLETING_ADMIN_PASSWORD=ClaveFuerte123 fleting db seed
    fleting db status
    ```

Genere el model desde la tabla y use el ORM:

```bash
fleting db model pull productos
fleting shell
```
```text
>>> tables()
['_fleting_migrations', 'sqlite_sequence', 'users', 'productos']
>>> ProductosModel.create(nombre="Lápiz", precio=2.5)
{'id': 1, 'nombre': 'Lápiz', 'precio': 2.5}
>>> ProductosModel.where(nombre="Lápiz")
[{'id': 1, 'nombre': 'Lápiz', 'precio': 2.5}]
>>> table("productos")
>>> quit()
```

Revertir la última migración:

```bash
fleting db rollback
```

---

## 6. Usar el ORM en el controller

```python
# app/controllers/productos_controller.py
from app.models.productos_model import ProductosModel

class ProductosController:
    def listar(self):
        return ProductosModel.all()

    def registrar(self, nombre: str, precio: float):
        return ProductosModel.create(nombre=nombre, precio=precio)
```

```python
# app/views/pages/productos_view.py (fragmento de render)
items = [ft.Text(f"{p['nombre']} — $ {p['precio']}") for p in self.controller.listar()]
content = ft.Column(controls=items, spacing=8)
```

---

## 7. Proyecto con MySQL

```bash
docker run -d --name fleting-mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=fleting -p 3306:3306 mysql:8
pip install "fleting[mysql]"

fleting init tienda --mysql
cd tienda
```

Configure la conexión:

=== "PowerShell"

    ```powershell
    $env:FLETING_DB_PASSWORD = "root"
    $env:FLETING_ADMIN_PASSWORD = "ClaveFuerte123"
    ```

=== "Linux / macOS"

    ```bash
    export FLETING_DB_PASSWORD=root
    export FLETING_ADMIN_PASSWORD=ClaveFuerte123
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

## 8. Proyecto con MariaDB

```bash
docker run -d --name fleting-mariadb -e MARIADB_ROOT_PASSWORD=root -e MARIADB_DATABASE=fleting -p 3307:3306 mariadb:11
pip install "fleting[mariadb]"

fleting init tienda --mysql
cd tienda
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
fleting shell          # el banner muestra "Fleting Console (MariaDB 11.x)"
```

---

## 9. Migrar un proyecto SQLite existente a MySQL

```bash
cd tienda
pip install "fleting[mysql]"
fleting db init --mysql
```
```text
Backup: core/database.py → database.py.bak
Backup: core/migrations.py → migrations.py.bak
Engine switched: sqlite → mysql
```

Luego, con las variables `FLETING_DB_*` definidas:

```bash
fleting db migrate
fleting db seed
```

!!! warning "Datos"
    El cambio de motor **no copia datos** de SQLite a MySQL; solo reconfigura el proyecto y vuelve a aplicar las migraciones en la base nueva. Sus migraciones con sintaxis exclusiva de SQLite deben ajustarse (vea el ejemplo 5).

Para volver: `fleting db init --sqlite`.

---

## 10. Diagnóstico y depuración

```bash
fleting doctor               # estructura, rutas, driver, seed
fleting info                 # versiones y entorno
```

Los errores de la CLI muestran solo el mensaje. Para ver el traceback completo:

=== "PowerShell"

    ```powershell
    $env:FLETING_DEBUG = "1"; fleting db migrate
    ```

=== "Linux / macOS"

    ```bash
    FLETING_DEBUG=1 fleting db migrate
    ```

Códigos de salida: `0` éxito, `1` error (incluido `doctor` con errores), `2` comando desconocido.

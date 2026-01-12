# 🛠️ CLI.md — Guía de Comandos CLI

## 🛠️ Fleting CLI

El CLI de Fleting automatiza la creación y eliminación de archivos siguiendo el estándar del framework.

---

## 📦 Inicialización del Proyecto

Para crear la estructura inicial de un nuevo proyecto Fleting, ejecuta:

```bash 
fleting init <nombre_proyecto>
cd <nombre_proyecto>
fleting run
```

### 📌 Comportamento:

Cria automaticamente a pasta <nombre_proyecto>/

Estrutura compatível com Flet Build (APK / Web / Desktop)

Nome padrão do projeto: Fleting

Estrutura gerada:

```bash
<nombre_proyecto>/
 ├─ assets/
 ├─ configs/
 ├─ controllers/
 ├─ core/
 ├─ models/
 ├─ views/
 └─ main.py
```

Salida esperada:

```shell
✅ ¡Framework Fleting creado con éxito!
```

Este comando crea automáticamente la estructura básica de carpetas y archivos necesarios para iniciar una app Fleting.

## 🖥️ Comando de Ayuda

Para ver todos los comandos disponibles en la CLI:

> fleting -h

o

> fleting --help

Salida:
```shell
🚀 Fleting CLI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Uso:
  fleting <comando> [opciones]


📖 Comandos Disponibles
┌──────────────────────────────────────┬────────────────────────────────────────────────────────┐
│ Comando                              │ Descripción                                            │
├──────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ fleting init <nombre_app>            │ Inicializa un nuevo proyecto Fleting                   │
│ fleting info                         │ Muestra información de versión y del sistema           │
│ fleting run                          │ Ejecuta la aplicación                                  │
│ fleting create page <nombre>         │ Crea una página (model + controller + view)            │
│ fleting create view <nombre>         │ Crea una nueva vista                                   │
│ fleting create model <nombre>        │ Crea un nuevo modelo                                   │
│ fleting create controller <nombre>   │ Crea un nuevo controller                               │
|--------------------------------------|--------------------------------------------------------|
│ fleting delete page <nombre>         │ Elimina una página existente                           │
│ fleting delete view <nombre>         │ Elimina una vista                                      │
│ fleting delete model <nombre>        │ Elimina un modelo                                      │
│ fleting delete controller <nombre>   │ Elimina un controller                                  │
|--------------------------------------|--------------------------------------------------------|
│ fleting list pages                   │ Lista todas las páginas                                │
│ fleting list controllers             │ Lista todos los controllers                            │
│ fleting list views                   │ Lista todas las vistas                                 │
│ fleting list models                  │ Lista todos los models                                 │
│ fleting list routes                  │ Lista todos las rutas                                  │
|--------------------------------------|--------------------------------------------------------|
│ fleting db init                      │ Inicializa la estructura de la base de datos           │
│ fleting db migrate                   │ Ejecuta las migraciones de la base de datos            │
│ fleting db seed                      │ Inserta datos iniciales en la base de datos            │
│ fleting db make <nombre>             │ Crea una nueva migración                               │
│ fleting db rollback                  │ Revierte la última migración aplicada                  │
│ fleting db status                    │ Muestra el estado actual de las migraciones            │
└──────────────────────────────────────┴────────────────────────────────────────────────────────┘
```

## ℹ️ Información del Entorno

El comando info muestra información detallada del entorno, versiones y dependencias instaladas.

> fleting info

Ejemplo de salida:

```shell
 ______ _      _   _
|  ____| |    | | (_)
| |__  | | ___| |_ _ _ __   __ _
|  __| | |/ _ \ __| | '_ \ / _` |
| |    | |  __/ |_| | | | | (_| |
|_|    |_|\___|\__|_|_| |_|\__, |
                            __/ |
                           |___/

🚀 Fleting Framework

📦 Entorno

🧠 Python        : 3.11.0
🖥️  Sistema      : Windows 10
🧩 Flet          : 0.80.0
🚀 Fleting       : 1.0.12

📚 Bibliotecas instaladas:
  - anyio==4.12.0
  - certifi==2025.11.12
  - flet==0.80.0
  - flet-desktop==0.80.0
  - fleting==1.0.12
  - h11==0.16.0
  - httpcore==1.0.9
  - httpx==0.28.1
  - idna==3.11
  - msgpack==1.1.2
  - oauthlib==3.3.1
  - pip==25.3
  - repath==0.9.0
  - six==1.17.0
  - typing_extensions==4.15.0

✅ Entorno listo para usar.
```

## ▶️ Ejecutando el Proyecto

Después de inicializar el proyecto, ejecuta la app con:

```bash 
fleting run
# o
flet run fleting/main.py
# o, alternativamente:

python fleting/main.py
```

    💡 Recomendado: usar `fleting run` para una mejor integración con el runtime de Flet.

## ✅ Flujo Básico de Uso

```shell
pip install flet
pip install fleting

fleting init app
cd app
app> fleting run

# para desarrollo
app> fleting create page home
app> flet run main.py
app> python main.py
```

## ▶️ Ejecutando el CLI para desarrollo

### Windows

```bash
fleting create view home
# o
python -m cli.cli create view home
```

## 📦 Comandos Disponibles

### 🔹 create  
Crea archivos estandarizados.

> fleting create <tipo> <nombre>

### 🔹 delete  
Elimina archivos existentes.

> fleting delete <tipo> <nombre>

## 🧩 Tipos Soportados

| Tipo | Descripción |
|------|-------------|
| controller | Crea un controller |
| view | Crea una view simple |
| model | Crea un model |
| page | Crea view + controller + model |

### ✨ Ejemplos

#### Crear una View

```bash
fleting create view home
```

Crea:

views/pages/home_view.py

#### Crear un Controller

```bash
fleting create controller user
```

Crea:

controllers/user_controller.py

#### Crear un Model

```bash
fleting create model product
```

Crea:

models/product_model.py

### Crear una Page Completa

```bash
fleting create page dashboard
```

Crea automáticamente:

- models/dashboard_model.py
- controllers/dashboard_controller.py
- views/pages/dashboard_view.py
- registra una ruta en configs/routes.py

Todo ya conectado (MVC).

## 🗑️ Eliminación de Archivos

### Eliminar View
```bash
fleting delete view home
```

### Eliminar Controller
```bash
fleting delete controller user
```

### Eliminar Model
```bash
fleting delete model product
```

### Eliminar Page Completa
```bash
fleting delete page dashboard
```

Elimina:
- view
- controller
- model

### ⚠️ Observaciones Importantes

- El CLI no elimina rutas automáticamente
- No sobrescribe archivos existentes
- Todos los comandos generan logs en `logs/fleting.log`

---

# 🗄️ Gestión de Base de Datos — Fleting CLI

El Fleting Framework incluye un sistema de gestión de base de datos simple, seguro y orientado a **migraciones**, inspirado en frameworks modernos como Django y Alembic.

Esta sección describe en detalle todos los comandos disponibles bajo `fleting db`.

---

## 📌 `fleting db init`

### Descripción
Inicializa la **estructura básica del sistema de base de datos** del proyecto.

Este comando:
- Crea las carpetas necesarias para trabajar con base de datos
- Prepara el proyecto para recibir migraciones y seeds
- **No crea tablas ni datos**
- **No ejecuta migraciones**

### Qué crea

```text
app/
├── migrations/
│   ├── __init__.py
│   └── 001_initial.py
├── seeds/
│   └── initial.py
└── data/
```

Ejemplo de uso:

```bash
fleting db init
```
Salida esperada


> ✅ Database structure initialized

## 📌 fleting db migrate

Descripción: 
Ejecuta todas las migraciones pendientes del proyecto.

Este comando:

- Crea el archivo de base de datos (SQLite) si no existe
- Ejecuta las funciones up(db) de las migraciones no aplicadas
- Registra cada migración aplicada en la tabla _fleting_migrations
- Nunca ejecuta una migración dos veces

Reglas importantes:

- Solo se ejecutan migraciones no aplicadas
- El orden de ejecución es numérico (001, 002, 003, ...)
- Si una migración falla, el proceso se detiene

Ejemplo de uso
```bash
fleting db migrate
```
Salida esperada

> ✅ Applied migration 001_initial.py

## 📌 fleting db seed

**Descripción**
Inserta datos iniciales o de prueba en la base de datos.

Este comando:

- Ejecuta todos los archivos dentro de app/seeds
- Busca la función run(db) en cada seed
- Es ideal para crear usuarios iniciales, datos demo, etc.

### ⚠️ Advertencia

        ⚠️ Este comando puede ejecutarse más de una vez, por lo que los seeds deben ser idempotentes (usar INSERT OR IGNORE, por ejemplo).

Ejemplo de uso
```bash
fleting db seed
```
Salida esperada
> 🌱 Seed executed: initial.py

## 📌 fleting db make <nombre>

**Descripción**
Crea una nueva migración de base de datos.

Este comando:

- Genera automáticamente el siguiente número de migración
- Crea un archivo con funciones up(db) y down(db)
- No ejecuta la migración automáticamente

Convención de nombres

```text
001_initial.py
002_create_users_table.py
003_add_email_to_users.py
```
Ejemplo de uso

```bash
fleting db make add_email_to_users
```
Archivo generado

```python
def up(db):
    db.execute("""
        ALTER TABLE users ADD COLUMN email TEXT;
    """)

def down(db):
    # Código para revertir el cambio
    pass
```
## 📌 fleting db rollback

**Descripción**
Revierte la última migración aplicada.

Este comando:

- Identifica la última migración registrada
- Ejecuta su función down(db)
- Elimina la migración del registro _fleting_migrations

### ⚠️ Limitación de SQLite

        SQLite no soporta todas las operaciones de rollback (por ejemplo, DROP COLUMN), por lo que la implementación de down() debe ser cuidadosa.

Ejemplo de uso
```bash
fleting db rollback
```
Salida esperada

> ↩️ Rolled back migration 002_add_email_to_users.py

## 📌 fleting db status
**Descripción**
Muestra el estado actual de las migraciones del proyecto.

Este comando:

- Lista migraciones aplicadas
- Lista migraciones pendientes
- Detecta inconsistencias (migraciones aplicadas sin archivo)

Ejemplo de uso

```bash
fleting db status
```
Salida de ejemplo:

```text
📦 Database status

Applied migrations:
  ✔ 001_initial.py

Pending migrations:
  ⏳ 002_add_email_to_users.py
```
Base de datos actualizada

> ✅ Database is up to date.

## 🧠 Buenas prácticas

- Nunca edites una migración ya aplicada
- Crea siempre una nueva migración para cambios de schema
- Implementa down() siempre que sea posible
- Usa SQL explícito para mayor control
- Versiona las migraciones junto al código

## 🚀 Flujo recomendado
```bash
fleting db init
fleting db make create_users_table
fleting db migrate
fleting db seed
```

Este flujo garantiza un entorno de base de datos consistente, reproducible y seguro.

---

# 🎯 Filosofía del CLI

Convención > Configuración

- Cero preguntas interactivas
- Predecible
- Seguro (no sobrescribe código)

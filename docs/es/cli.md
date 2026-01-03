# 🛠️ CLI.md — Guía de Comandos CLI

## 🛠️ Fleting CLI

El CLI de Fleting automatiza la creación y eliminación de archivos siguiendo el estándar del framework.

---

## 📦 Inicialización del Proyecto

Para crear la estructura inicial de un nuevo proyecto Fleting, ejecuta:

> fleting init

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
Fleting CLI

Uso:
  fleting init
      Inicializa un nuevo proyecto Fleting

  fleting create page <nombre>
      Crea una nueva página (model + controller + view)

  fleting create view <nombre>
  fleting create model <nombre>
  fleting create controller <nombre>

  fleting delete page <nombre>
  fleting delete view <nombre>
  fleting delete model <nombre>
  fleting delete controller <nombre>
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

> fleting run

o

> flet run fleting/app.py

o, alternativamente:

> python fleting/app.py

💡 Recomendado: usar `flet run` para una mejor integración con el runtime de Flet.

## ✅ Flujo Básico de Uso

```shell
pip install flet
pip install fleting

fleting init
fleting run

# para desarrollo
fleting create page home
flet run fleting/app.py
```

## ▶️ Ejecutando el CLI para desarrollo

### Windows

> fleting create view home

o

> python -m cli.cli create view home

## 📦 Comandos Disponibles

🔹 create  
Crea archivos estandarizados.

> fleting create <tipo> <nombre>

🔹 delete  
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

> fleting create view home

Crea:

views/pages/home_view.py

#### Crear un Controller

> fleting create controller user

Crea:

controllers/user_controller.py

#### Crear un Model

> fleting create model product

Crea:

models/product_model.py

#### Crear una Page Completa

> fleting create page dashboard

Crea automáticamente:

- models/dashboard_model.py
- controllers/dashboard_controller.py
- views/pages/dashboard_view.py

Todo ya conectado (MVC).

## 🗑️ Eliminación de Archivos

### Eliminar View
> fleting delete view home

### Eliminar Controller
> fleting delete controller user

### Eliminar Model
> fleting delete model product

### Eliminar Page Completa
> fleting delete page dashboard

Elimina:
- view
- controller
- model

⚠️ Observaciones Importantes

- El CLI no elimina rutas automáticamente
- No sobrescribe archivos existentes
- Todos los comandos generan logs en `logs/fleting.log`

## 🎯 Filosofía del CLI

Convención > Configuración

- Cero preguntas interactivas
- Predecible
- Seguro (no sobrescribe código)

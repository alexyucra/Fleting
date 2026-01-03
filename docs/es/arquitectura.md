# Arquitectura

## 🧱 Estructura de Carpetas

```text
fleting/
│
├── core/               # Infraestructura del framework
│   ├── app.py
│   ├── router.py
│   ├── responsive.py
│   ├── state.py
│   ├── i18n.py
│   ├── logger.py
│   └── error_handler.py
│
├── configs/            # Configuraciones globales
│   ├── app_config.py
│   ├── routes.py
│   └── languages/
│       ├── pt.json
│       └── es.json
│
├── views/
│   ├── layouts/        # Layouts reutilizables
│   └── pages/          # Views de páginas
│
├── controllers/        # Controllers
├── models/             # Models
│
├── cli/                # CLI del framework
│   ├── cli.py
│   ├── commands/
│   └── templates/
│
├── app.py              # Punto de entrada de la aplicación
└── fleting.bat         # Runner del CLI (Windows)
```

## 🧭 Arquitectura de Views

En Fleting, las Views no conocen el layout de la aplicación.

```text
View (contenido puro)
   ↓
Layout (AppBar, NavigationBar, etc.)
   ↓
Page (Flet)
```

Ejemplo simplificado:

```py
class HomeView:
    def render(self):
        content = ft.Text("Home")
        return MainLayout(page, content, router)
```

## 🌍 Internacionalización (i18n)

Archivos JSON en `configs/languages`.

Acceso mediante `I18n.t("clave.subclave")`.

```py
from core.i18n import I18n

I18n.load("pt")
I18n.t("home.title")
```

## 📱 Responsividad

El estado global de la aplicación mantiene el tipo de dispositivo actual:

```py
from core.state import AppState

AppState.device  # mobile | tablet | desktop
```

Se actualiza automáticamente al redimensionar la ventana.

## 🚦 Enrutamiento

Las rutas se definen en `configs/routes.py` con lazy loading:

```py
ROUTE_MAP = {
    "/": "views.pages.home_view.HomeView",
}
```

Cada view recibe:

- page
- router

Y retorna un control Flet.

## 🧰 Logs y Errores

- Logs automáticos en `logs/fleting.log`
- Captura global de errores con pantalla amigable
- Stacktrace registrado automáticamente

## 🚀 Objetivo del Framework

Fleting no intenta ser todo.

Existe para:

- acelerar proyectos con Flet
- mantener el código limpio
- servir como base sólida para aplicaciones reales

Simple, extensible y directo al punto.

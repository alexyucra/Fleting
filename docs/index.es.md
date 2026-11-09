# 🚀 Framework Fleting para Flet (Python)

<p align="center">
<img src="img/fleting_logo.png" width="120"/>
</p>

<p align="center">
<strong>Crea aplicaciones multiplataforma con Python, Flet y MVC: más rápido que nunca.</strong>
</p>

<p align="center">
<a href="#">
<img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
</a>
<a href="#">
<img src="https://img.shields.io/badge/Flet-0.25+-green.svg" alt="Flet">
</a>
<a href="#">
<img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</a>
<a href="#">
<img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome">
</a>
</p>

---
<p align="center">
<a href="index.md">🇺🇸 English</a> | 
<a href="index.pt.md">🇧🇷 Português</a> | 
<a href="index.es.md">🇪🇸 Español</a>
</p>

---

## ¿Qué es Fleting?

**Fleting** es un micro-framework ligero y con un enfoque definido (*opinionated*), construido sobre [Flet](https://flet.dev/). Aporta la potencia de la **arquitectura MVC**, una **organización limpia del código** y un **desarrollo rápido** a los desarrolladores de Python que crean aplicaciones multiplataforma.

Ya sea que estés creando una aplicación móvil, una herramienta de escritorio o un panel de control optimizado para tabletas, Fleting te ofrece la estructura y las herramientas necesarias para lanzar tus proyectos más rápido. ### ✨ Características destacadas

- **⚡️ Arquitectura MVC** — Clara separación de responsabilidades
- **📱 Enfoque Mobile-First** — Se adapta automáticamente a móviles, tabletas y escritorio
- **🌍 i18n integrado** — Soporte multilingüe listo para usar
- **🛠️ CLI productiva** — Genera páginas, modelos, controladores y más
- **🗄️ Soporte para múltiples bases de datos** — SQLite, MySQL y MariaDB (próximamente PostgreSQL y SQL Server)
- **🎨 Layouts desacoplados** — Componentes de interfaz reutilizables y adaptables (responsive)
- **🚦 Enrutamiento sencillo** — Definición de rutas limpia y declarativa
- **🧪 ORM integrado** — Capa de modelos ligera con gestión de relaciones

---

## 🎯 ¿Para quién es Fleting?

| 👨‍💻 **Desarrolladores independientes** | 🏢 **Equipos** | 📚 **Estudiantes** |
|-----------------------------------------|--------------|-----------------|
| Crea aplicaciones rápidamente sin complicaciones excesivas | Estructura de proyecto estandarizada | Aprende MVC en Python |
| Un solo framework para móvil y escritorio | Fácil incorporación de nuevos miembros | Practica arquitectura del mundo real | ---

## 🚀 Inicio rápido

Pon en marcha tu primera aplicación Fleting en menos de **3 minutos**:

### 1. Crea un entorno virtual aislado

**Elige tu herramienta preferida:**

<details>
<summary><strong>📦 Usando uv (Recomendado)</strong></summary>

```bash
# Instala uv si no lo tienes
pip install uv

# Crea un nuevo proyecto con uv
uv init myapp
cd myapp

# Crea y activa el entorno virtual
uv venv

# Activar en Linux/macOS
source .venv/bin/activate

# Activar en Windows (PowerShell)
.venv\Scripts\activate

# Instala las dependencias
uv pip install flet fleting
```

</details><details> <summary><strong>🐍 Usando venv (Estándar)</strong></summary>

```bash
# Crea el entorno virtual
python -m venv venv

# Activar en Linux/macOS
source venv/bin/activate

# Activar en Windows (PowerShell)
venv\Scripts\activate

# Activar en Windows (CMD)
venv\Scripts\activate.bat

# Instala las dependencias
pip install flet fleting

```

</details><details> <summary><strong>📋 Usando Poetry</strong></summary>

```bash
# Instala Poetry
pip install poetry

# Crea un nuevo proyecto
poetry new myapp
cd myapp

# Añade dependencias
poetry add flet fleting

# Activa el entorno
poetry shell
```
</details>

### 2. Crea un nuevo proyecto

```bash
pip install flet fleting
fleting init myapp
cd myapp
```

### 3. Ejecuta tu aplicación

```bash
fleting run
```

¡Listo! 🎉 Ya tienes una aplicación multiplataforma funcional con:

✅ Soporte multi-idioma (inglés, portugués, español)

✅ Diseño responsivo (móvil, tableta, escritorio)

✅ Arquitectura MVC

✅ Base de datos SQLite lista

---
## 🧪 ¿Prefieres MySQL o MariaDB?

```bash
pip install "fleting[mysql]"      # MySQL
pip install "fleting[mariadb]"    # MariaDB (PyMySQL)
fleting init myapp --mysql
```

- [Guía de bases de datos](./es/base-de-datos.md): configuración, variables de entorno, Docker, migraciones, ORM, shell
- [Ejemplos paso a paso](./es/ejemplos.md): todos los comandos de la CLI en la práctica

## 🛠️ Comandos de la CLI de Fleting

### 📦 Comandos del proyecto

| Comando | Descripción | |---------|-------------|
| `fleting init <app_name>` | Inicializar un nuevo proyecto Fleting |
| `fleting init <app_name> --mysql` | Inicializar un nuevo proyecto Fleting con MySQL / MariaDB |
| `fleting info` | Mostrar información de la versión y del sistema |
| `fleting run` | Ejecutar la aplicación |
| `fleting doctor` | Revisar problemas comunes del proyecto |

---

### ➕ Comandos de creación

| Comando | Descripción |
|---------|-------------|
| `fleting create page <name>` | Crear una página (modelo + controlador + vista) |
| `fleting create view <name>` | Crear una nueva vista |
| `fleting create model <name>` | Crear un nuevo modelo |
| `fleting create controller <name>` | Crear un nuevo controlador |

---

### 🗑️ Comandos de eliminación

| Comando | Descripción |
|---------|-------------|
| `fleting delete page <name>` | Eliminar una página existente |
| `fleting delete view <name>` | Eliminar una vista |
| `fleting delete model <name>` | Eliminar un modelo |
| `fleting delete controller <name>` | Eliminar un controlador |

---

### 📋 Comandos de listado

| Comando | Descripción |
|---------|-------------|
| `fleting list pages` | Listar todas las páginas |
| `fleting list controllers` | Listar todos los controladores |
| `fleting list views` | Listar todas las vistas |
| `fleting list models` | Listar todos los modelos |
| `fleting list routes` | Listar todas las rutas |

---

### 🗄️ Comandos de base de datos

| Comando | Descripción |
|---------|-------------|
| `fleting db init` | Inicializar la base de datos (SQLite por defecto) |
| `fleting db init --mysql` | Cambia el proyecto a MySQL / MariaDB (con respaldo `.bak`) |
| `fleting db init --sqlite` | Vuelve el proyecto a SQLite |
| `fleting db migrate` | Ejecutar migraciones de base de datos |
| `fleting db seed` | Poblar la base de datos con datos iniciales |
| `fleting db make <name>` | Crear una nueva migración |
| `fleting db rollback` | Revertir la última migración |
| `fleting db status` | Mostrar el estado actual de las migraciones |

---

### 🗄️ Comandos de base de datos / modelos

| Comando | Descripción |
|---------|-------------|
| `fleting db model pull` | Generar modelos a partir del esquema de la base de datos |
| `fleting db model pull <table>` | Generar modelo para una tabla específica |
| `fleting db model pull <table> --force` | Sobrescribir archivos de modelo existentes |

---

### 🧩 Comandos de consola

| Comando | Descripción |
|---------|-------------|
| `fleting shell` | Abrir consola interactiva de base de datos (SQLite, MySQL / MariaDB) |

---

## 📊 Resumen de categorías de comandos

| Categoría | Comandos |
|----------|----------|
| **Proyecto** | `init`, `info`, `run`, `doctor` |
| **Crear** | `create page`, `create view`, `create model`, `create controller` |
| **Eliminar** | `delete page`, `delete view`, `delete model`, `delete controller` |
| **Listar** | `list pages`, `list controllers`, `list views`, `list models`, `list routes` |
| **Base de datos** | `db init`, `db migrate`, `db seed`, `db make`, `db rollback`, `db status` |
| **Modelos** | `db model pull` |
| **Consola** | `shell` |

---
## 📱 Diseñado para el mundo real

Enfoque *Mobile-First* (prioridad móvil) desde el diseño
Fleting detecta automáticamente el tipo de dispositivo y adapta los diseños en consecuencia:

```py
from core.state import AppState

if AppState.device == "mobile":
# Mostrar interfaz optimizada para móviles
elif AppState.device == "tablet":
# Mostrar interfaz optimizada para tablets
else:
# Mostrar interfaz optimizada para escritorio
```

### Internacionalización integrada

Admite múltiples idiomas mediante archivos JSON sencillos:

```json
{
"app": {
"name": "MyApp"
},
"home": {
"title": "Welcome to MyApp"
}
}
```

```py
from core.i18n import I18n

# Mostrar texto traducido
I18n.t("home.title")  # "Welcome to MyApp" en inglés
I18n.t("home.title")  # "Bem-vindo ao MyApp" en portugués
I18n.t("home.title")  # "Bienvenido a MyApp" en español
```

### Compatibilidad con bases de datos

|Motor	|Estado	|Caso de uso|
|-------|-------|--------|
|SQLite	    |✅ Estable	|Desarrollo, aplicaciones embebidas|
|MySQL	    |✅ Estable	|Producción, aplicaciones web|
|MariaDB	|✅ Estable	|Producción (driver PyMySQL recomendado)|
|PostgreSQL	|🔄 Próximamente	|Aplicaciones empresariales|
|SQL Server	|🔄 Próximamente	|Integraciones empresariales| ## 📊 Estructura del proyecto
Fleting genera una estructura de proyecto limpia y organizada:

```shell
myapp/
├── app/
│   ├── controllers/   # Lógica de negocio
│   ├── models/        # Capa de datos
│   └── views/         # Componentes de la interfaz de usuario (UI)
│       ├── layouts/   # Diseños reutilizables
│       └── pages/     # Vistas de página
├── configs/           # Archivos de configuración
│   ├── app_config.py
│   ├── routes.py
│   └── languages/     # Traducciones i18n
├── core/              # Núcleo del framework
│   ├── app.py
│   ├── router.py
│   ├── database.py
│   ├── i18n.py
│   └── migrations.py
├── migrations/        # Migraciones de base de datos
├── seeds/             # Datos iniciales (seed data)
└── main.py            # Punto de entrada de la aplicación
```

## 📚 Recursos de aprendizaje

|Recurso	|Descripción| Enlace |
|---------|-----------|------|
|📖 [Documentación de Fleting](https://alexyucra.github.io/Fleting/)	|Documentación completa del framework| |
|🎓 [Curso de Fleting](https://github.com/alexyucra/fleting-curso)	|Curso en video paso a paso| |
|🐍 [Documentación de Flet](https://github.com/alexyucra/flet-docs)	|Framework Flet subyacente| |
|🤖 [FLAI – Framework de IA local para Fleting](https://github.com/alexyucra/flai)	|IA local para aplicaciones Fleting| | ## 🎯 Filosofía
Fleting se construyó sobre principios claros:

### 1️⃣ Simplicidad ante todo
- Sin abstracciones innecesarias
- Código explícito y legible
- Arquitectura predecible

### 2️⃣ Separación de responsabilidades
- Vista → UI pura (Flet)
- Diseño (Layout) → Estructura visual reutilizable
- Controlador → Lógica de negocio
- Modelo → Capa de datos
- Enrutador → Navegación
- Núcleo (Core) → Infraestructura del framework

### 3️⃣ Enfoque "Mobile-First" (prioridad móvil)
- Detección automática del dispositivo
- Adaptación dinámica del diseño
- Componentes optimizados para pantallas táctiles

### 4️⃣ Internacionalización nativa
- Traducciones sencillas en JSON
- Cambio de idioma en tiempo real
- Accesible desde cualquier parte de la aplicación

### 5️⃣ CLI de primer nivel
- Generación de código estandarizada
- Reducción de código repetitivo (*boilerplate*)
- Convención sobre configuración

## 🤝 Contribuciones
¡Agradecemos las contribuciones! Ya sea mediante:

- 🐛 Reporte de errores — Abre un *issue*

- 💡 Ideas para nuevas funciones — Inicia una discusión

- 📝 Documentación — Mejora nuestra documentación

- 🔧 Código — Envía un *pull request*

- [Para quienes deseen contribuir a Fleting en GitHub.](CONTRIBUTING.md)

Consulta nuestra Guía de contribución para empezar.

## 📄 Licencia
Licencia MIT: úsala libremente en proyectos personales y comerciales.

## 💬 Obtén ayuda
- 📖 Lee la documentación
- 🐛 Reporta problemas
- 💬 Contacta al autor

<p align="center"> <strong>⭐️ Danos una estrella en GitHub: ¡nos ayuda mucho!</strong> </p><p align="center"> <a href="https://github.com/alexyucra/Fleting"> <img src="https://img.shields.io/github/stars/alexyucra/Fleting?style=social" alt="Estrellas en GitHub"> </a> </p> ```

___
# Framework Fleting

<p align="center">
<img src="img/fleting.gif" width="260" />
</p>
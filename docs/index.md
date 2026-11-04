# 🚀 Fleting Framework for Flet Python

<p align="center">
  <img src="img/fleting_logo.png" width="120"/>
</p>

<p align="center">
  <strong>Build cross-platform applications with Python, Flet, and MVC — faster than ever.</strong>
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

## What is Fleting?

**Fleting** is a lightweight, opinionated micro-framework built on top of [Flet](https://flet.dev/). It brings the power of **MVC architecture**, **clean code organization**, and **rapid development** to Python developers building cross-platform applications.

Whether you're creating a mobile app, a desktop tool, or a tablet-friendly dashboard — Fleting gives you the structure and tools to ship faster.

### ✨ Key Highlights

- **⚡️ MVC Architecture** — Clear separation of concerns
- **📱 Mobile-First** — Automatically adapts to mobile, tablet, and desktop
- **🌍 Built-in i18n** — Multi-language support out of the box
- **🛠️ Productive CLI** — Generate pages, models, controllers, and more
- **🗄️ Multi-Database Support** — SQLite and MySQL (PostgreSQL & SQL Server coming soon)
- **🎨 Decoupled Layouts** — Reusable, responsive UI components
- **🚦 Simple Routing** — Clean, declarative route definitions
- **🧪 Built-in ORM** — Lightweight model layer with relationships

---

## 🎯 Who is Fleting for?

| 👨‍💻 **Solo Developers** | 🏢 **Teams** | 📚 **Students** |
|-------------------------|--------------|-----------------|
| Build apps fast without over-engineering | Standardized project structure | Learn MVC in Python |
| One framework for mobile + desktop | Easy onboarding for new members | Practice real-world architecture |

---


## ⚠️ Important change to the Fleting foundation

Version **Fleting 1.2.3** was originally built upon **Flet 0.8.x**.

As of this update, the project now uses **Flet 1.0.5** as its foundation. In other words:

- **Before:** Fleting 1.2.3 + Flet 0.8.x
- **Now:** Fleting 1.2.3 + Flet 1.0.5

This update incorporates the stability, performance, and API improvements found in Flet 1.0, but it also **introduces breaking changes** compared to Flet 0.8.x. If you have existing code written for the older Flet API, please review the points below before migrating:

- Services are now asynchronous and independent of the `page` object (e.g., `await ft.SharedPreferences()` instead of `page.client_storage`).
- Most explicit calls to `page.update()` are no longer required.
- `UserControl` has been removed; custom components now inherit directly from controls (e.g., `ft.Row`, etc.).
- Some controls have been renamed (e.g., `ElevatedButton` → `Button`).

Please refer to the official Flet migration guide for further details.

---

## 🚀 Quick Start

Get your first Fleting app running in under **3 minutes**:

### 1. Create an isolated virtual environment

**Choose your preferred tool:**

<details>
<summary><strong>📦 Using uv (Recommended)</strong></summary>

```bash
# Install uv if you don't have it
pip install uv

# Create a new project with uv
uv init myapp
cd myapp

# Create and activate virtual environment
uv venv

# Activate on Linux/macOS
source .venv/bin/activate

# Activate on Windows (PowerShell)
.venv\Scripts\activate

# Install dependencies
uv pip install flet fleting
```

</details><details> <summary><strong>🐍 Using venv (Standard)</strong></summary>

```bash
# Create virtual environment
python -m venv venv

# Activate on Linux/macOS
source venv/bin/activate

# Activate on Windows (PowerShell)
venv\Scripts\activate

# Activate on Windows (CMD)
venv\Scripts\activate.bat

# Install dependencies
pip install flet fleting

```

</details><details> <summary><strong>📋 Using Poetry</strong></summary>

```bash
# Install Poetry
pip install poetry

# Create new project
poetry new myapp
cd myapp

# Add dependencies
poetry add flet fleting

# Activate environment
poetry shell
```
</details>

### 2. Create a new project

```bash
pip install flet fleting
fleting init myapp
cd myapp
```

### 3. Run your app

```bash
fleting run
```

That's it! 🎉 You now have a working cross-platform application with:

✅ Multi-language support (English, Portuguese, Spanish)

✅ Responsive layout (mobile, tablet, desktop)

✅ MVC architecture

✅ SQLite database ready

---
## 🧪 Want MySQL instead?

```bash
fleting init myapp --mysql
```
[data base setup in docker](./en/database.md)

## 🛠️ Fleting CLI Commands

### 📦 Project Commands

| Command | Description |
|---------|-------------|
| `fleting init <app_name>` | Initialize a new Fleting project |
| `fleting init <app_name> --mysql` | Initialize a new Fleting project with MySQL |
| `fleting info` | Show version and system information |
| `fleting run` | Run the application |

---

### ➕ Create Commands

| Command | Description |
|---------|-------------|
| `fleting create page <name>` | Create a page (model + controller + view) |
| `fleting create view <name>` | Create a new view |
| `fleting create model <name>` | Create a new model |
| `fleting create controller <name>` | Create a new controller |

---

### 🗑️ Delete Commands

| Command | Description |
|---------|-------------|
| `fleting delete page <name>` | Delete an existing page |
| `fleting delete view <name>` | Delete a view |
| `fleting delete model <name>` | Delete a model |
| `fleting delete controller <name>` | Delete a controller |

---

### 📋 List Commands

| Command | Description |
|---------|-------------|
| `fleting list pages` | List all pages |
| `fleting list controllers` | List all controllers |
| `fleting list views` | List all views |
| `fleting list models` | List all models |
| `fleting list routes` | List all routes |

---

### 🗄️ Database Commands

| Command | Description |
|---------|-------------|
| `fleting db init` | Initialize the database (SQLite by default) |
| `fleting db init --mysql` | Initialize the database with MySQL |
| `fleting db migrate` | Run database migrations |
| `fleting db seed` | Seed the database with initial data |
| `fleting db make <name>` | Create a new migration |
| `fleting db rollback` | Rollback the last migration |
| `fleting db status` | Show current database migration status |

---

### 🗄️ Database / Models Commands

| Command | Description |
|---------|-------------|
| `fleting db model pull` | Generate models from the database schema |
| `fleting db model pull <table>` | Generate model for a specific table |
| `fleting db model pull <table> --force` | Overwrite existing model files |

---

### 🧩 Console Commands

| Command | Description |
|---------|-------------|
| `fleting shell` | Open interactive database shell

---

## 📊 Command Categories Summary

| Category | Commands |
|----------|----------|
| **Project** | `init`, `info`, `run` |
| **Create** | `create page`, `create view`, `create model`, `create controller` |
| **Delete** | `delete page`, `delete view`, `delete model`, `delete controller` |
| **List** | `list pages`, `list controllers`, `list views`, `list models`, `list routes` |
| **Database** | `db init`, `db migrate`, `db seed`, `db make`, `db rollback`, `db status` |
| **Models** | `db model pull` |
| **Console** | `shell` |

---
## 📱 Built for the Real World

Mobile-First by Design
Fleting automatically detects the device type and adapts layouts accordingly:

```py
from core.state import AppState

if AppState.device == "mobile":
    # Show mobile-optimized UI
elif AppState.device == "tablet":
    # Show tablet-optimized UI
else:
    # Show desktop-optimized UI
```

### Built-in Internationalization

Support multiple languages with simple JSON files:

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

# Display translated text
I18n.t("home.title")  # "Welcome to MyApp" in English
I18n.t("home.title")  # "Bem-vindo ao MyApp" in Portuguese
I18n.t("home.title")  # "Bienvenido a MyApp" in Spanish
```

### Database Support

|Engine	|Status	|Use Case|
|-------|-------|--------|
|SQLite	    |✅ Stable	|Development, embedded apps|
|MySQL	    |✅ Stable	|Production, web applications|
|PostgreSQL	|🔄 Coming Soon	|Enterprise applications|
|SQL Server	|🔄 Coming Soon	|Enterprise integrations|

## 📊 Project Structure
Fleting generates a clean, organized project structure:

```shell
myapp/
├── app/
│   ├── controllers/   # Business logic
│   ├── models/        # Data layer
│   └── views/         # UI components
│       ├── layouts/   # Reusable layouts
│       └── pages/     # Page views
├── configs/           # Configuration files
│   ├── app_config.py
│   ├── routes.py
│   └── languages/     # i18n translations
├── core/              # Framework core
│   ├── app.py
│   ├── router.py
│   ├── database.py
│   ├── i18n.py
│   └── migrations.py
├── migrations/        # Database migrations
├── seeds/             # Seed data
└── main.py            # Application entry point
```

## 📚 Learning Resources

|Resource	|Description| Link |
|---------|-----------|------|
|📖 [Fleting Documentation](https://alexyucra.github.io/Fleting/)	|Complete framework documentation| |
|🎓 [Fleting Course](https://github.com/alexyucra/fleting-curso)	|Step-by-step video course| |
|🐍 [Flet Documentation](https://github.com/alexyucra/flet-docs)	|Underlying Flet framework| |
|🤖 [FLAI – Local AI Framework for Fleting](https://github.com/alexyucra/flai)	|Local AI for Fleting apps| |

## 🎯 Philosophy
Fleting was built on clear principles:

### 1️⃣ Simplicity Above All
- No unnecessary abstractions
- Explicit, readable code
- Predictable architecture

### 2️⃣ Separation of Responsibilities
- View → Pure UI (Flet)
- Layout → Reusable visual structure
- Controller → Business logic
- Model → Data layer
- Router → Navigation
- Core → Framework infrastructure

### 3️⃣ Mobile-First
- Automatic device detection
- Dynamic layout adaptation
- Touch-friendly components

### 4️⃣ Native Internationalization
- Simple JSON translations
- Real-time language switching
- Accessible anywhere in the app

### 5️⃣ CLI as a First-Class Citizen
- Standardized code generation
- Reduced boilerplate
- Convention over Configuration

## 🤝 Contributing
We welcome contributions! Whether it's:

- 🐛 Bug reports — Open an issue

- 💡 Feature ideas — Start a discussion

- 📝 Documentation — Improve our docs

- 🔧 Code — Submit a pull request
- [For those who want to contribute to Fleting on GitHub.](CONTRIBUTING.md)

Check out our Contributing Guide to get started.

## 📄 License
MIT License — Use it freely in personal and commercial projects.

## 💬 Get Help
- 📖 Read the Docs
- 🐛 Report Issues
- 💬 Contact the Author

<p align="center"> <strong>⭐️ Star us on GitHub — it helps!</strong> </p><p align="center"> <a href="https://github.com/alexyucra/Fleting"> <img src="https://img.shields.io/github/stars/alexyucra/Fleting?style=social" alt="GitHub stars"> </a> </p> ```

___
# Fleting Framework

<p align="center">
  <img src="img/fleting.gif" width="260" />
</p>

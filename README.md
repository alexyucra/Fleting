<p align="center">
  <a href="#">
    <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Flet-1.0.5+-green.svg" alt="Flet">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome">
  </a>
</p>

<p align="center">
| <a href="https://alexyucra.github.io/Fleting/">🇺🇸 English</a> |
  <a href="https://alexyucra.github.io/Fleting/pt/cli/">🇧🇷 Português</a> |
  <a href="https://alexyucra.github.io/Fleting/es/cli/">🇪🇸 Español</a> |
</p>

---
<p align="center">
  <img src="docs/img/fleting_logo.png" width="100"/>
</p>

# 🚀 Fleting Framework for Flet Python

Fleting is an opinionated micro-framework built on top of Flet, focused on:

- Simplicity
- Clear organization
- Productivity
- Cross-platform applications (mobile, tablet, and desktop)

It features an architecture inspired by MVC, with a **decoupled layout**, **simple routing**, **i18n**, **automatic responsiveness**, a **CLI for code generation** and a small **ORM with migrations** for SQLite, MySQL and MariaDB.

<p align="center">
  <img src="docs/img/fleting.gif" width="260" />
</p>

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

## ✨ What's new in 1.3.0

- **MySQL & MariaDB** support end to end: `fleting init <app> --mysql`, migrations, seeds, ORM, `db model pull` and an interactive `fleting shell`.
- Switch an existing project between engines with `fleting db init --mysql` / `--sqlite` (with `.bak` backups).
- New `fleting doctor` command to check a project for common problems.
- `fleting --help` shows a **"Init with Database"** section and the commands for the engine of the current project.
- Security: no default `admin/fleting` credential (set `FLETING_ADMIN_PASSWORD`), database credentials from environment variables, SQL identifier validation.
- Many fixes in `create`, `delete`, the ORM and the CLI. See the [CHANGELOG](CHANGELOG.md).

## 🚀 Quick Start

### 1. Create an isolated virtual environment

- [Recommended: environment with poetry](docs/pt/enviroment.md)

### 2. Install and create a project

```shell
pip install fleting

fleting init myapp
cd myapp
fleting run
```

### 3. Add a page

```shell
fleting create page products     # model + controller + view + route
fleting run
```

## 🗄️ Databases

| Engine | Install | Create a project |
|---|---|---|
| SQLite (default) | — | `fleting init myapp` |
| MySQL 8 | `pip install "fleting[mysql]"` | `fleting init myapp --mysql` |
| MariaDB 10.6+ / 11 | `pip install "fleting[mariadb]"` | `fleting init myapp --mysql` + `FLETING_DB_DRIVER=pymysql` |

MySQL/MariaDB credentials are read from environment variables (`FLETING_DB_HOST`, `FLETING_DB_PORT`, `FLETING_DB_USER`, `FLETING_DB_PASSWORD`, `FLETING_DB_NAME`, `FLETING_DB_DRIVER`).

```shell
fleting db init            # migrations/, seeds/, data/
fleting db migrate         # apply migrations
fleting db seed            # creates "admin" only if FLETING_ADMIN_PASSWORD is set
fleting shell              # tables(), query(sql), table("t"), describe("t"), models()
```

Full guide: [English](docs/en/database.md) · [Português](docs/pt/banco-de-dados.md) · [Español](docs/es/base-de-datos.md)

## 🛠️ CLI

| Category | Commands |
|---|---|
| **Project** | `init <app>`, `info`, `run`, `doctor` |
| **Init with database** | `init <app> --mysql` |
| **Create** | `create page\|view\|model\|controller <name>` |
| **Delete** | `delete page\|view\|model\|controller <name>` |
| **List** | `list pages\|controllers\|views\|models\|routes` |
| **Database** | `db init [--mysql\|--sqlite]`, `db migrate`, `db seed`, `db make <name>`, `db rollback`, `db status` |
| **Models** | `db model pull [<table>] [--force]` |
| **Console** | `shell` |

Run `fleting --help` for the full list. Step-by-step examples for every command: [English](docs/en/examples.md) · [Português](docs/pt/exemplos.md) · [Español](docs/es/ejemplos.md)

## 🧪 Development

```shell
pip install -e ".[dev]"
pytest -q
ruff check fleting
```

MySQL/MariaDB integration tests run with `FLETING_TEST_MYSQL=1` and the `FLETING_DB_*` variables pointing to a server (see `tests/test_04_mysql.py`).

## 📚 Documentation

Complete documentation is available at:

👉 [Full documentation](https://alexyucra.github.io/Fleting/)

---

## 🎯 Philosophy

O Fleting foi criado com alguns princípios claros:

### 1️⃣ Simplicity above all
- No unnecessary abstractions
- Explicit and easy-to-understand code
- Predictable architecture

### 2️⃣ Separation of responsibilities
- **View** → Pure UI (Flet)
- **Layout** → Reusable visual structure
- **Controller** → Business rules
- **Model** → Data
- **Router** → Navegação
- **Core** → Framework infrastructure

### 3️⃣ Mobile-first
- The global application state automatically identifies:
  - `mobile`
  - `tablet`
  - `desktop`
- Layouts can dynamically react to device type

### 4️⃣ Native internationalization
- Simple JSON-based translation system
- Real-time language switching
- Translations accessible anywhere in the app

### 5️⃣ CLI as a first-class citizen
- Standardized file creation and removal
- Reduced boilerplate
- Convention > Configuration

---

## 📄 License

MIT

## How to contribute
- [For those who want to contribute to Fleting on GitHub.](CONTRIBUTING.md)

<p align="center">
| <a href="https://alexyucra.github.io/Fleting/">🇺🇸 English</a> |
  <a href="https://alexyucra.github.io/Fleting/pt/cli/">🇧🇷 Português</a> |
  <a href="https://alexyucra.github.io/Fleting/es/cli/">🇪🇸 Español</a> |
</p>
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

<p align="center">
| <a href="https://alexyucra.github.io/Fleting/">🇺🇸 English</a> |
  <a href="https://alexyucra.github.io/Fleting/pt/cli/">🇧🇷 Português</a> |
  <a href="https://alexyucra.github.io/Fleting/es/cli/">🇪🇸 Español</a> |
</p>

---
<p align="center">
  <img src="../img/fleting_logo.png" width="100"/>
</p>

# 🚀 Fleting Framework for Flet Python

Fleting is an opinionated micro-framework built on top of Flet, focused on:

- Simplicity
- Clear organization
- Productivity
- Cross-platform applications (mobile, tablet, and desktop)

It features an architecture inspired by MVC, with a **decoupled layout**, **simple routing**, **i18n**, **automatic responsiveness**, and a **CLI for code generation**.

It brings an MVC-inspired architecture with **decoupled layout**, **simple routing**, **i18n**, **automatic responsiveness**, and a **CLI for code generation**.

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

## 🚀 Quick Start

### 1. Create an isolated virtual environment

- [Recommended: environment with poetry](docs/pt/enviroment.md)


## 🛠️ CLI

```shell
pip install flet
pip install fleting

fleting init
fleting run

# for development
fleting create page home
flet run fleting/app.py
```

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
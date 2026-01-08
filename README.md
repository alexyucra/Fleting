<p align="center">
| <a href="README.md">🇺🇸 English</a> |
  <a href="docs/readme-pt.md">🇧🇷 Português</a> |
  <a href="docs/readme-es.md">🇪🇸 Español</a> |
</p>

---

#  ![](./docs/img/fleting%20logo.png) Fleting Framework

Fleting is an opinionated micro-framework built on top of Flet, focused on:

- Simplicity
- Clear organization
- Productivity
- Cross-platform applications (mobile, tablet, and desktop)

Ele traz uma arquitetura inspirada em MVC, com **layout desacoplado**, **roteamento simples**, **i18n**, **responsividade automática** e um **CLI para geração de código**.

It brings an MVC-inspired architecture with **decoupled layout**, **simple routing**, **i18n**, **automatic responsiveness**, and a **CLI for code generation**.

<p align="center">
  <img src="docs/img/fleting.gif" width="260" />
</p>

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

👉 [Full documentation](docs/pt/index.md)

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
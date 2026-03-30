# Fleting Framework

<p align="center">
  <img src="img/fleting_logo.png" width="100"/>
</p>

Fleting es un micro-framework opinativo construido sobre **Flet**, enfocado en:

- simplicidad

- organización clara

- productividad

- aplicaciones multiplataforma (móvil, tablet y escritorio)

Aporta una arquitectura inspirada en MVC, con **layout desacoplado**, **enrutamiento simple**, **i18n**, **responsividad automática** y un **CLI para generación de código**.

<p align="center">
  <img src="img/fleting.gif" width="260" />
</p>

## 🚀 Inicio rápido

### 1. Crea un entorno virtual aislado

- [Recomendado: entorno con poetry](es/enviroment.md)

## 🛠️ CLI

```shell
pip install flet
pip install fleting

fleting init
fleting run

# para desarrollo
fleting create page home
flet run fleting/app.py
```

## 📚 Documentación

La documentación completa está disponible en:

👉 [documentación completa](es/index.md)

## 🎯 Filosofía

Fleting fue creado con algunos principios claros:

### 1️⃣ Simplicidad por encima de todo

- Nada de abstracciones innecesarias
- Código explícito y fácil de entender
- Arquitectura predecible

### 2️⃣ Separación de responsabilidades

- **View** → UI pura (Flet)
- **Layout** → Estructura visual reutilizable
- **Controller** → Reglas de negocio
- **Model** → Datos
- **Router** → Navegación
- **Core** → Infraestructura del framework

### 3️⃣ Mobile-first

El estado global de la aplicación identifica automáticamente:

- mobile
- tablet
- desktop

Los layouts pueden reaccionar dinámicamente al tipo de dispositivo

### 4️⃣ Internacionalización nativa

- Sistema de traducción simple basado en JSON
- Cambio de idioma en tiempo real
- Traducciones accesibles en cualquier parte de la app

### 5️⃣ CLI como ciudadano de primera clase

- Creación y eliminación de archivos estandarizados
- Reducción de boilerplate
- Convención > Configuración

## 📄 Licencia

[MIT](/LICENSE)

## Cómo contribuir

👉  [Para quienes quieran contribuir con Fleting en GitHub.](CONTRIBUTING.md)
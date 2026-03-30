# ✅ Fleting – Checklist de Mejoras

## 🟢 BASE (ya implementado)
- [x] Arquitectura MVC organizada
- [x] Router con *lazy loading* (sin imports circulares)
- [x] Layout global (TopBar + BottomBar)
- [x] Responsividad (mobile / tablet / desktop)
- [x] Estado global (`AppState`)
- [x] i18n con JSON (PT / ES)
- [x] CLI básico (`create controller`)
- [x] Compatible con Flet ≥ 0.70 (sin APIs deprecated)

---

## 🔵 RESPONSIVIDAD & UI
- [ ] Limitar el ancho del contenido en *desktop* (`max_content_width`)
- [ ] Crear `ResponsiveContainer` reutilizable
- [ ] Sidebar automática para *desktop* (reemplazar BottomBar)
- [ ] Breakpoints configurables vía `AppConfig`
- [ ] Detección de orientación (portrait / landscape)
- [ ] Sistema de espaciado estándar (design system)

---

## 🟣 LAYOUT & NAVEGACIÓN
- [ ] Crear `BaseView` abstracta
- [ ] Estandarizar el título de la página por *view*
- [ ] Resaltar la ruta activa en el menú
- [ ] Soporte para rutas con parámetros (`/user/:id`)
- [ ] Historial de navegación (back)
- [ ] Transiciones entre pantallas (animaciones)

---

## 🟠 INTERNACIONALIZACIÓN (i18n)
- [ ] Fallback automático al idioma por defecto
- [ ] Detección del idioma del sistema
- [ ] Persistencia del idioma (local storage)
- [ ] CLI para generar archivos de idioma
- [ ] Validación de claves faltantes
- [ ] Namespace por módulo (`home.title`, `auth.login`)

---

## 🔴 ESTADO & CONFIGURACIÓN
- [ ] Persistencia de estado (local storage)
- [ ] Tema claro / oscuro
- [ ] Observadores de estado (reactividad)
- [ ] Configuración por entorno (dev / prod)
- [ ] Middleware global (ej: auth guard)

---

## 🟡 CLI (Developer Experience)
- [x] fleting create controller
- [x] fleting create view
- [x] fleting create model
- [x] fleting create page
- [x] Logging en el CLI
- [x] Manejo de errores en el CLI
- [x] delete controller
- [x] delete view
- [x] delete model
- [x] delete page
- [ ] Templates personalizables
- [ ] Validación de nombres
- [ ] `fleting run`
- [ ] `fleting build`

---

## 🟤 CALIDAD & MANTENIMIENTO
- [ ] Tipado con `typing`
- [ ] Tests unitarios (router, i18n)
- [ ] Linter (ruff / flake8)
- [ ] Formateo automático (black)
- [x] Logging estructurado
- [x] Manejo global de errores

---

## ⚫ DOCUMENTACIÓN
- [x] README con la filosofía del framework
- [x] Guía de comandos CLI
- [x] Diagrama de la arquitectura
- [x] Guía de creación de *views*
- [x] Ejemplos completos
- [x] Checklist de mejoras
- [ ] Guía de responsividad
- [ ] Guía de i18n

---

## 🚀 FUTURO (nivel framework real)
- [ ] Sistema de plugins
- [ ] Inyección de dependencias
- [ ] Módulo de autenticación (login / guards)
- [ ] Store central (tipo Redux)
- [ ] Hot reload de views
- [ ] Exportar como paquete pip

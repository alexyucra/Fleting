# Arquitetura

## 🧱 Estrutura de Pastas

```text
fleting/
│
├── core/               # Infraestrutura do framework
│   ├── app.py
│   ├── router.py
│   ├── responsive.py
│   ├── state.py
│   ├── i18n.py
│   ├── logger.py
│   └── error_handler.py
│
├── configs/            # Configurações globais
│   ├── app_config.py
│   ├── routes.py
│   └── languages/
│       ├── pt.json
│       └── es.json
│
├── views/
│   ├── layouts/        # Layouts reutilizáveis
│   └── pages/          # Views de páginas
│
├── controllers/        # Controllers
├── models/             # Models
│
├── cli/                # CLI do framework
│   ├── cli.py
│   ├── commands/
│   └── templates/
│
├── app.py              # Entry point da aplicação
└── runtime_imports.py  # importação de views para build (Windows)

```

## 🧭 Arquitetura de Views

No Fleting, Views não conhecem o layout da aplicação.

```text
View (conteúdo puro)
   ↓
Layout (AppBar, NavigationBar, etc)
   ↓
Page (Flet)

```

Exemplo simplificado:

```py
class HomeView:
    def render(self):
        content = ft.Text("Home")
        return MainLayout(page, content, router)

```

## 🌍 Internacionalização (i18n)

Arquivos JSON em configs/languages

Acesso via I18n.t("chave.subchave")

```py
from core.i18n import I18n

I18n.load("pt")
I18n.t("home.title")
```

## 📱 Responsividade

O estado global da aplicação mantém o tipo de dispositivo atual:

```py
from core.state import AppState

AppState.device  # mobile | tablet | desktop
```

Atualizado automaticamente ao redimensionar a janela.

## 🚦 Roteamento

Rotas são definidas em configs/routes.py com lazy loading:

```py
ROUTE_MAP = {
    "/": "views.pages.home_view.HomeView",
}
```

Cada view recebe:

- page
- router

E retorna um controle Flet.

## 🧰 Logs e Erros

- Logs automáticos em logs/fleting.log
- Captura global de erros com tela amigável
- Stacktrace registrado automaticamente

## 🚀 Objetivo do Framework

Fleting não tenta ser tudo.

Ele existe para:

- acelerar projetos Flet
- manter código limpo
- servir como base sólida para apps reais

Simples, extensível e direto ao ponto.

---




# ✅ Fleting – Checklist de Melhorias

## 🟢 BASE (já implementado)
- [x] Arquitetura MVC organizada
- [x] Router com lazy loading (sem circular imports)
- [x] Layout global (TopBar + BottomBar)
- [x] Responsividade (mobile / tablet / desktop)
- [x] Estado global (`AppState`)
- [x] i18n com JSON (PT / ES)
- [x] CLI básico (`create controller`)
- [x] Compatível com Flet ≥ 0.70 (sem APIs deprecated)

---

## 🔵 RESPONSIVIDADE & UI
- [ ] Limitar largura do conteúdo no desktop (`max_content_width`)
- [ ] Criar `ResponsiveContainer` reutilizável
- [ ] Sidebar automática para desktop (substituir BottomBar)
- [ ] Breakpoints configuráveis via `AppConfig`
- [ ] Detecção de orientação (portrait / landscape)
- [ ] Sistema de espaçamento padrão (design system)

---

## 🟣 LAYOUT & NAVEGAÇÃO
- [ ] Criar `BaseView` abstrata
- [ ] Padronizar título da página por view
- [ ] Highlight da rota ativa no menu
- [ ] Suporte a rotas com parâmetros (`/user/:id`)
- [ ] Histórico de navegação (back)
- [ ] Transições entre telas (animações)

---

## 🟠 INTERNACIONALIZAÇÃO (i18n)
- [ ] Fallback automático para idioma padrão
- [ ] Detecção de idioma do sistema
- [ ] Persistência do idioma (local storage)
- [ ] CLI para gerar arquivos de idioma
- [ ] Validação de chaves ausentes
- [ ] Namespace por módulo (`home.title`, `auth.login`)

---

## 🔴 ESTADO & CONFIGURAÇÃO
- [ ] Persistência de estado (local storage)
- [ ] Tema claro / escuro
- [ ] Observadores de estado (reactividade)
- [ ] Configuração por ambiente (dev / prod)
- [ ] Middleware global (ex: auth guard)

---

## 🟡 CLI (Developer Experience)
- [x] fleting create controller
- [x] fleting create view
- [x] fleting create model
- [x] fleting create page
- [x] Logging no CLI
- [x] Tratamento de erros no CLI
- [x] delete controller
- [x] delete view
- [x] delete model
- [x] delete page
- [ ] Templates customizáveis
- [ ] Validação de nomes
- [ ] `fleting run`
- [ ] `fleting build`

---

## 🟤 QUALIDADE & MANUTENÇÃO
- [ ] Tipagem com `typing`
- [ ] Testes unitários (router, i18n)
- [ ] Linter (ruff / flake8)
- [ ] Formatação automática (black)
- [X] Logging estruturado
- [x] Tratamento global de erros

---

## ⚫ DOCUMENTAÇÃO
- [X] README com filosofia do framework
- [X] Guia de comandos CLI
- [X] Diagrama da arquitetura
- [X] Guia de criação de views
- [X] Exemplos completos
- [X] Checklist de melhorias
- [ ] Guia de responsividade
- [ ] Guia de i18n


---

## 🚀 FUTURO (nível framework real)
- [ ] Sistema de plugins
- [ ] Injeção de dependências
- [ ] Auth module (login / guards)
- [ ] Store central (Redux-like)
- [ ] Hot reload de views
- [ ] Export como package pip

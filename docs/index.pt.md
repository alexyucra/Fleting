# 🚀 Framework Fleting para Flet Python

<p align="center">
<img src="img/fleting_logo.png" width="120"/>
</p>

<p align="center">
<strong>Crie aplicativos multiplataforma com Python, Flet e MVC — mais rápido do que nunca.</strong>
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

## O que é o Fleting?

O **Fleting** é um micro-framework leve e com uma abordagem opinativa, construído sobre o [Flet](https://flet.dev/). Ele traz o poder da **arquitetura MVC**, da **organização de código limpo** e do **desenvolvimento rápido** para desenvolvedores Python que criam aplicativos multiplataforma.

Seja criando um aplicativo móvel, uma ferramenta para desktop ou um painel otimizado para tablets, o Fleting oferece a estrutura e as ferramentas necessárias para você entregar seus projetos mais rapidamente. ### ✨ Principais Destaques

- **⚡️ Arquitetura MVC** — Separação clara de responsabilidades
- **📱 Mobile-First** — Adapta-se automaticamente a dispositivos móveis, tablets e desktops
- **🌍 i18n Integrado** — Suporte nativo a múltiplos idiomas
- **🛠️ CLI Produtiva** — Gere páginas, modelos, controladores e muito mais
- **🗄️ Suporte a Múltiplos Bancos de Dados** — SQLite e MySQL (PostgreSQL e SQL Server em breve)
- **🎨 Layouts Desacoplados** — Componentes de interface (UI) reutilizáveis ​​e responsivos
- **🚦 Roteamento Simples** — Definições de rotas limpas e declarativas
- **🧪 ORM Integrado** — Camada de modelo leve com suporte a relacionamentos

---

## 🎯 Para quem é o Fleting?

| 👨‍💻 **Desenvolvedores Solo** | 🏢 **Equipes** | 📚 **Estudantes** |
|-------------------------|--------------|-----------------|
| Crie apps rapidamente sem complexidade excessiva | Estrutura de projeto padronizada | Aprenda MVC em Python |
| Um único framework para mobile e desktop | Integração fácil de novos membros | Pratique arquitetura do mundo real | ---

## 🚀 Início Rápido

Coloque seu primeiro aplicativo Fleting para rodar em menos de **3 minutos**:

### 1. Crie um ambiente virtual isolado

**Escolha sua ferramenta preferida:**

<details>
<summary><strong>📦 Usando uv (Recomendado)</strong></summary>

```bash
# Instale o uv se ainda não o tiver
pip install uv

# Crie um novo projeto com uv
uv init myapp
cd myapp

# Crie e ative o ambiente virtual
uv venv

# Ative no Linux/macOS
source .venv/bin/activate

# Ative no Windows (PowerShell)
.venv\Scripts\activate

# Instale as dependências
uv pip install flet fleting
```

</details><details> <summary><strong>🐍 Usando venv (Padrão)</strong></summary>

```bash
# Crie o ambiente virtual
python -m venv venv

# Ative no Linux/macOS
source venv/bin/activate

# Ative no Windows (PowerShell)
venv\Scripts\activate

# Ative no Windows (CMD)
venv\Scripts\activate.bat

# Instale as dependências
pip install flet fleting

```

</details><details> <summary><strong>📋 Usando Poetry</strong></summary>

```bash
# Instale o Poetry
pip install poetry

# Crie um novo projeto
poetry new myapp
cd myapp

# Adicione as dependências
poetry add flet fleting

# Ative o ambiente
poetry shell
```
</details>

### 2. Crie um novo projeto

```bash
pip install flet fleting
fleting init myapp
cd myapp
```

### 3. Execute seu aplicativo

```bash
fleting run
```

Pronto! 🎉 Agora você tem um aplicativo multiplataforma funcional com:

✅ Suporte a múltiplos idiomas (Inglês, Português, Espanhol)

✅ Layout responsivo (mobile, tablet, desktop)

✅ Arquitetura MVC

✅ Banco de dados SQLite pronto para uso

---
## 🧪 Prefere usar MySQL?

```bash
fleting init myapp --mysql
```
[configuração do banco de dados no docker](./en/database.md)

## 🛠️ Comandos da CLI do Fleting

### 📦 Comandos de Projeto

| Comando | Descrição |
|---------|-------------|
| `fleting init <app_name>` | Inicializa um novo projeto Fleting |
| `fleting init <app_name> --mysql` | Inicializa um novo projeto Fleting com MySQL |
| `fleting info` | Exibe informações de versão e do sistema |
| `fleting run` | Executa a aplicação |

---

### ➕ Comandos de Criação

| Comando | Descrição |
|---------|-------------|
| `fleting create page <name>` | Cria uma página (model + controller + view) |
| `fleting create view <name>` | Cria uma nova view |
| `fleting create model <name>` | Cria um novo model |
| `fleting create controller <name>` | Cria um novo controller |

---

### 🗑️ Comandos de Exclusão

| Comando | Descrição |
|---------|-------------|
| `fleting delete page <name>` | Exclui uma página existente |
| `fleting delete view <name>` | Exclui uma view |
| `fleting delete model <name>` | Exclui um model |
| `fleting delete controller <name>` | Exclui um controller |

---

### 📋 Comandos de Listagem

| Comando | Descrição |
|---------|-------------|
| `fleting list pages` | Lista todas as páginas |
| `fleting list controllers` | Lista todos os controladores |
| `fleting list views` | Lista todas as views |
| `fleting list models` | Lista todos os modelos |
| `fleting list routes` | Lista todas as rotas |

---

### 🗄️ Comandos de Banco de Dados

| Comando | Descrição |
|---------|-------------|
| `fleting db init` | Inicializa o banco de dados (SQLite por padrão) |
| `fleting db init --mysql` | Inicializa o banco de dados com MySQL |
| `fleting db migrate` | Executa as migrações do banco de dados |
| `fleting db seed` | Popula o banco de dados com dados iniciais |
| `fleting db make <name>` | Cria uma nova migração |
| `fleting db rollback` | Reverte a última migração |
| `fleting db status` | Mostra o status atual das migrações do banco de dados |

---

### 🗄️ Comandos de Banco de Dados / Modelos

| Comando | Descrição |
|---------|-------------|
| `fleting db model pull` | Gera modelos a partir do esquema do banco de dados |
| `fleting db model pull <table>` | Gera modelo para uma tabela específica |
| `fleting db model pull <table> --force` | Sobrescreve arquivos de modelo existentes |

---

### 🧩 Comandos de Console

| Comando | Descrição |
|---------|-------------|
| `fleting shell` | Abre o shell interativo do banco de dados (apenas SQLite) |

---

## 📊 Resumo das Categorias de Comandos

| Categoria | Comandos |
|----------|----------|
| **Projeto** | `init`, `info`, `run` |
| **Criação** | `create page`, `create view`, `create model`, `create controller` |
| **Exclusão** | `delete page`, `delete view`, `delete model`, `delete controller` |
| **Listagem** | `list pages`, `list controllers`, `list views`, `list models`, `list routes` |
| **Banco de Dados** | `db init`, `db migrate`, `db seed`, `db make`, `db rollback`, `db status` |
| **Models** | `db model pull` |
| **Console** | `shell` |

---

## 📱 Criado para o Mundo Real

Design "Mobile-First" (Focado em Dispositivos Móveis)
O Fleting detecta automaticamente o tipo de dispositivo e adapta os layouts de acordo:

```py
from core.state import AppState

if AppState.device == "mobile":
# Exibir interface otimizada para dispositivos móveis
elif AppState.device == "tablet":
# Exibir interface otimizada para tablets
else:
# Exibir interface otimizada para desktop
```

### Internacionalização Integrada

Suporte a múltiplos idiomas com arquivos JSON simples:

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

# Exibir texto traduzido
I18n.t("home.title")  # "Welcome to MyApp" em inglês
I18n.t("home.title")  # "Bem-vindo ao MyApp" em português
I18n.t("home.title")  # "Bienvenido a MyApp" em espanhol
```

### Suporte a Banco de Dados

|Motor	|Status	|Caso de Uso|
|-------|-------|--------|
|SQLite	    |✅ Estável	|Desenvolvimento, aplicações embarcadas|
|MySQL	    |✅ Estável	|Produção, aplicações web|
|PostgreSQL	|🔄 Em breve	|Aplicações corporativas|
|SQL Server	|🔄 Em breve	|Integrações corporativas| 

## 📊 Estrutura do Projeto
O Fleting gera uma estrutura de projeto limpa e organizada:

```shell
myapp/
├── app/
│   ├── controllers/   # Lógica de negócios
│   ├── models/        # Camada de dados
│   └── views/         # Componentes de UI
│       ├── layouts/   # Layouts reutilizáveis
│       └── pages/     # Visualizações de página
├── configs/           # Arquivos de configuração
│   ├── app_config.py
│   ├── routes.py
│   └── languages/     # Traduções i18n
├── core/              # Núcleo do framework
│   ├── app.py
│   ├── router.py
│   ├── database.py
│   ├── i18n.py
│   └── migrations.py
├── migrations/        # Migrações de banco de dados
├── seeds/             # Dados iniciais (seed data)
└── main.py            # Ponto de entrada da aplicação
```

## 📚 Recursos de Aprendizado

|Recurso	|Descrição| Link |
|---------|-----------|------|
|📖 [Documentação do Fleting](https://alexyucra.github.io/Fleting/)	|Documentação completa do framework| |
|🎓 [Curso de Fleting](https://github.com/alexyucra/fleting-curso)	|Curso em vídeo passo a passo| |
|🐍 [Documentação do Flet](https://github.com/alexyucra/flet-docs)	|Framework Flet subjacente| |
|🤖 [FLAI – Framework de IA Local para Fleting](https://github.com/alexyucra/flai)	|IA local para aplicações Fleting| | 

## 🎯 Filosofia
O Fleting foi construído com base em princípios claros:

### 1️⃣ Simplicidade Acima de Tudo
- Sem abstrações desnecessárias
- Código explícito e legível
- Arquitetura previsível

### 2️⃣ Separação de Responsabilidades
- View → UI pura (Flet)
- Layout → Estrutura visual reutilizável
- Controller → Lógica de negócios
- Model → Camada de dados
- Router → Navegação
- Core → Infraestrutura do framework

### 3️⃣ Mobile-First
- Detecção automática de dispositivo
- Adaptação dinâmica de layout
- Componentes otimizados para toque

### 4️⃣ Internacionalização Nativa
- Traduções simples em JSON
- Troca de idioma em tempo real
- Acessível em qualquer parte do aplicativo

### 5️⃣ CLI como Recurso de Primeira Classe
- Geração de código padronizada
- Redução de código repetitivo (*boilerplate*)
- Convenção sobre Configuração

## 🤝 Contribuição
Aceitamos contribuições! Seja através de:

- 🐛 Relatos de bugs — Abra uma *issue*

- 💡 Ideias de funcionalidades — Inicie uma discussão

- 📝 Documentação — Melhore nossa documentação

- 🔧 Código — Envie um *pull request*

- [Para quem deseja contribuir com o Fleting no GitHub.](CONTRIBUTING.md)

Consulte nosso Guia de Contribuição para começar.

## 📄 Licença
Licença MIT — Use livremente em projetos pessoais e comerciais.

## 💬 Obtenha Ajuda
- 📖 Leia a documentação
- 🐛 Relate problemas
- 💬 Entre em contato com o autor

<p align="center"> <strong>⭐️ Dê uma estrela no GitHub — isso ajuda!</strong> </p><p align="center"> <a href="https://github.com/alexyucra/Fleting"> <img src="https://img.shields.io/github/stars/alexyucra/Fleting?style=social" alt="Estrelas no GitHub"> </a> </p> ```

___
# Framework Fleting

<p align="center">
<img src="img/fleting.gif" width="260" />
</p>
# 🛠️ CLI.md — Guia de Comandos CLI

## 🛠️ Fleting CLI

O CLI do Fleting automatiza a criação e remoção de arquivos seguindo o padrão do framework.

---

## ▶️ Executando o CLI

### Windows


> fleting create view home

ou

> python -m cli.cli create view home

## 📦 Comandos Disponíveis
🔹 create

Cria arquivos padronizados.

> fleting create <tipo> <nome>

🔹 delete

Remove arquivos existentes.

> fleting delete <tipo> <nome>

## 🧩 Tipos Suportados

|Tipo   |	Descrição |
|-------|-------------|
|controller	|Cria um controller|
|view	|Cria uma view simples|
|model	|Cria um model|
|page	|Cria view + controller + model|

### ✨ Exemplos

#### Criar uma View

> fleting create view home


Cria:

views/pages/home_view.py

#### Criar um Controller

> fleting create controller user

Cria:

controllers/user_controller.py

#### Criar um Model

> fleting create model product

Cria:

models/product_model.py

#### Criar uma Page Completa

> fleting create page dashboard

Cria automaticamente:

- models/dashboard_model.py
- controllers/dashboard_controller.py
- views/pages/dashboard_view.py


Tudo já conectado (MVC).

## 🗑️ Remoção de Arquivos

### Remover View

> fleting delete view home

### Remover Controller

> fleting delete controller user

### Remover Model

> fleting delete model product

### Remover Page Completa

> fleting delete page dashboard

Remove:

- view
- controller
- model

        ⚠️ Observações Importantes

        O CLI não remove rotas automaticamente
        Não sobrescreve arquivos existentes
        Todos os comandos geram logs em logs/fleting.log

## 🎯 Filosofia do CLI

Convenção > Configuração

- Zero perguntas interativas
- Previsível
- Seguro (não sobrescreve código)

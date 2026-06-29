# 🛠️ CLI.md — Guia de Comandos CLI

## 🛠️ Fleting CLI

O CLI do Fleting automatiza a criação e remoção de arquivos seguindo o padrão do framework.

---

## Amviente virtual recomendado

> uv venv

> .\venv\script\Activate

## 📦 Inicialização do Projeto

> pip install fleting

Para criar a estrutura inicial de um novo projeto Fleting, execute:

```bash 
fleting init <nome_projeto>
cd <nome_projeto>
fleting run
```

### 📌 Comportamento:

Cria automaticamente a pasta <nome_projeto>/

Estrutura compatível com Flet Build (APK / Web / Desktop)

Nome padrão do projeto: Fleting

Estrutura gerada:

```bash
<nome_projeto>/
 ├─ app/
 |   ├─ models/
 |   ├─ views/
 |   ├─ controllers/
 ├─ assets/
 ├─ configs/
 ├─ core/
 └─ main.py
```

Saída esperada:

> ✅ Framework Fleting criado com sucesso!


Esse comando cria automaticamente a estrutura básica de pastas e arquivos necessários para iniciar um app Fleting.

## 🖥️ Comando de Ajuda

Para visualizar todos os comandos disponíveis na CLI:

> fleting -h

ou

> fleting --help

saida:

```shell
🚀 Fleting CLI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Uso:
  fleting <comando> [opções]


📖 Comandos Disponíveis
┌──────────────────────────────────────┬────────────────────────────────────────────────────────┐
│ Comando                              │ Descrição                                              │
├──────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ fleting init  <app_name>             │ Inicializa um novo projeto Fleting                     │
│ fleting info                         │ Exibe informações de versão e do sistema               │
│ fleting run                          │ Executa a aplicação                                    │
|--------------------------------------|--------------------------------------------------------|
│ fleting create page <nome>           │ Cria uma página (model + controller + view)            │
│ fleting create view <nome>           │ Cria uma nova view                                     │
│ fleting create model <nome>          │ Cria um novo model                                     │
│ fleting create controller <nome>     │ Cria um novo controller                                │
|--------------------------------------|--------------------------------------------------------|
│ fleting delete page <nome>           │ Remove uma página existente                            │
│ fleting delete view <nome>           │ Remove uma view                                        │
│ fleting delete model <nome>          │ Remove um model                                        │
│ fleting delete controller <nome>     │ Remove um controller                                   │
|--------------------------------------|--------------------------------------------------------|
│ fleting list pages                   │ Lista todas as páginas                                 │
│ fleting list controllers             │ Lista todos os controllers                             │
│ fleting list views                   │ Lista todas as views                                   │
│ fleting list models                  │ Lista todos os models                                  │
│ fleting list routes                  │ Lista todas as rotas                                   │
|--------------------------------------|--------------------------------------------------------|
│ fleting db init                      │ Inicializa a estrutura do banco de dados               │
│ fleting db migrate                   │ Executa as migrations do banco de dados                │
│ fleting db seed                      │ Popula o banco de dados com dados iniciais             │
│ fleting db make <nome>               │ Cria uma nova migration                                │
│ fleting db rollback                  │ Reverte a última migration aplicada                    │
│ fleting db status                    │ Exibe o status atual das migrations do banco de dados  │
└──────────────────────────────────────┴────────────────────────────────────────────────────────┘
```

## ℹ️ Informações do Ambiente

O comando info exibe informações detalhadas do ambiente, versões e dependências instaladas.

> fleting info

Exemplo de saída:

```shell
 ______ _      _   _
|  ____| |    | | (_)
| |__  | | ___| |_ _ _ __   __ _
|  __| | |/ _ \ __| | '_ \ / _` |
| |    | |  __/ |_| | | | | (_| |
|_|    |_|\___|\__|_|_| |_|\__, |
                            __/ |
                           |___/

🚀 Fleting Framework

📦 Ambiente

🧠 Python        : 3.11.0
🖥️  Sistema      : Windows 10
🧩 Flet          : 0.80.0
🚀 Fleting       : 1.0.12

📚 Bibliotecas instaladas:
  - anyio==4.12.0
  - certifi==2025.11.12
  - flet==0.80.0
  - flet-desktop==0.80.0
  - fleting==1.0.12
  - h11==0.16.0
  - httpcore==1.0.9
  - httpx==0.28.1
  - idna==3.11
  - msgpack==1.1.2
  - oauthlib==3.3.1
  - pip==25.3
  - repath==0.9.0
  - six==1.17.0
  - typing_extensions==4.15.0

✅ Ambiente pronto para uso.
```

## ▶️ Executando o Projeto

Após inicializar o projeto, execute o app com:

```bash 
fleting run
# ou
bash flet run fleting/main.py

# ou, alternativamente:
python fleting/main.py
```

        💡 Recomendado: usar `fleting run` para melhor integração com o runtime do Flet.


## ✅ Fluxo Básico de Uso

```shell
pip install flet
pip install fleting

fleting init app
cd app
app> fleting run

# para desenvolvimento
app> fleting create page home
app> flet run main.py
app> python main.py
```

## ▶️ Executando  o CLI para desenvolvimento

### Windows

```bash
fleting create view home
# ou
python -m cli.cli create view home
```

## 📦 Comandos Disponíveis

### 🔹 create

Cria arquivos padronizados.

> fleting create <tipo> <nome>

### 🔹 delete

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

```bash 
fleting create view home
```

Cria:

views/pages/home_view.py

#### Criar um Controller

```bash
fleting create controller user
```

Cria:

controllers/user_controller.py

#### Criar um Model

```bash 
fleting create model product
```

Cria:

models/product_model.py

### Criar uma Page Completa

```bash
fleting create page dashboard
```

Cria automaticamente:

- models/dashboard_model.py
- controllers/dashboard_controller.py
- views/pages/dashboard_view.py
- adiciona una rota en configs/routes.py

Tudo já conectado (MVC).

## 🗑️ Remoção de Arquivos

### Remover View

```bash
fleting delete view home
```

### Remover Controller

```bash
fleting delete controller user
```

### Remover Model

```bash
fleting delete model product
```

### Remover Page Completa

```bash
fleting delete page dashboard
```

Remove:

- view
- controller
- model

### ⚠️ Observações Importantes

- O CLI não remove rotas automaticamente
- Não sobrescreve arquivos existentes
- Todos os comandos geram logs em logs/fleting.log

# 🗄️ Gerenciamento de Banco de Dados — Fleting CLI

O Fleting Framework inclui um sistema de gerenciamento de banco de dados simples, seguro e orientado a migrações, inspirado em frameworks modernos como Django e Alembic.

Esta seção descreve em detalhes todos os comandos disponíveis em `fleting db`.

---

## 📌 `fleting db init`

### Descrição
Inicializa a estrutura básica do sistema de banco de dados do projeto.

Este comando:
- Cria as pastas necessárias para trabalhar com o banco de dados
- Prepara o projeto para receber migrações e seeds
- **Não cria tabelas ou dados**
- **Não executa migrações**

### O que ele cria

```text
app/
├── migrations/
│ ├── __init__.py
│ └── 001_initial.py
├── seeds/
│ └── initial.py
└── data/
```

Exemplo de uso:

```bash
fleting db init
```
Saída esperada

> ✅ Estrutura do banco de dados inicializada

## 📌 fleting db migrate

Descrição: Executa todas as migrações pendentes do projeto.

Este comando:

- Cria o arquivo de banco de dados (SQLite) se ele não existir
- Executa as funções `up(db)` para migrações não aplicadas
- Registra cada migração aplicada na tabela `_fleting_migrations`
- Nunca executa uma migração duas vezes

Regras importantes:

- Somente migrações não aplicadas são executadas
- A ordem de execução é numérica (001, 002, 003, ...)
- Se uma migração falhar, o processo é interrompido

Exemplo de uso:
```bash
fleting db migrate
```
Saída esperada:

> ✅ Migração aplicada 001_initial.py

## 📌 fleting db seed

**Descrição**
Insere dados iniciais ou de teste no banco de dados.

Este comando:

- Executa todos os arquivos dentro de app/seeds
- Busca pela função `run(db)` em cada seed
- Ideal para criar usuários iniciais, dados de demonstração, etc.

### ⚠️ Aviso

⚠️ Este comando pode ser executado mais de uma vez, portanto, as seeds devem ser idempotentes (use INSERT ou IGNORE, por exemplo).

Exemplo de uso
```bash
fleting db seed
```
Saída esperada
> 🌱 Seed executada: initial.py

## 📌 fleting db make <nome>

**Descrição**
Cria uma nova migração de banco de dados.

Este comando:

- Gera automaticamente o próximo número de migração
- Cria um arquivo com as funções `up(db)` e `down(db)`
- Não executa a migração automaticamente

Convenção de nomenclatura

```texto
001_initial.py
002_create_users_table.py
003_add_email_to_users.py
```
Exemplo de uso

```bash
fleting db make add_email_to_users
```
Arquivo gerado

```python
def up(db):
db.execute("""
ALTER TABLE users ADD COLUMN email TEXT;

""")

def down(db):
# Código para reverter a alteração
pass
```
## 📌 fleting db rollback

**Descrição**
Reverte a última migração aplicada.

Este comando:

- Identifica a última migração registrada
- Executa sua função `down(db)`
- Remove a migração do log `_fleting_migrations`

### ⚠️ Limitação do SQLite

O SQLite não suporta todas as operações de rollback (por exemplo, `DROP COLUMN`), portanto, a implementação de `down()` deve ser feita com cuidado.

Exemplo de uso
```bash
fleting db rollback
```
Saída esperada

> ↩️ Migração 002_add_email_to_users.py revertida

## 📌 fleting db status
**Descrição**
Exibe o status atual das migrações do projeto.

Este comando:

- Lista as migrações aplicadas
- Lista as migrações pendentes
- Detecta inconsistências (migrações aplicadas sem um arquivo)

Exemplo de uso

```bash
fleting db status
```
Exemplo de saída:

```text
📦 Status do banco de dados

Migrações aplicadas:
✔ 001_initial.py

Migrações pendentes:

⏳ 002_add_email_to_users.py
```
Banco de dados atualizado

> ✅ Banco de dados atualizado.

## 🧠 Melhores Práticas

- Nunca edite uma migração existente
- Sempre crie uma nova migração para alterações de esquema
- Implemente `down()` sempre que possível
- Use SQL explícito para maior controle
- Versionar as migrações juntamente com o código

## 🚀 Fluxo Recomendado
```bash
fleting db init
fleting db make create_users_table
fleting db migrate
fleting db seed
```

Este fluxo garante um ambiente de banco de dados consistente, reproduzível e seguro.

---

# 🎯 Filosofia do CLI

Convenção > Configuração

- Zero perguntas interativas
- Previsível
- Seguro (não sobrescreve código)

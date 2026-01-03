# 🛠️ CLI.md — Guia de Comandos CLI

## 🛠️ Fleting CLI

O CLI do Fleting automatiza a criação e remoção de arquivos seguindo o padrão do framework.

---

## 📦 Inicialização do Projeto

Para criar a estrutura inicial de um novo projeto Fleting, execute:

> fleting init

Saída esperada:

```shell
✅ Framework Fleting criado com sucesso!
```

Esse comando cria automaticamente a estrutura básica de pastas e arquivos necessários para iniciar um app Fleting.

## 🖥️ Comando de Ajuda

Para visualizar todos os comandos disponíveis na CLI:

> fleting -h

ou

> fleting --help

saida:
```shell
Fleting CLI

Uso:
  fleting init
      Inicializa um novo projeto Fleting

  fleting create page <nome>
      Cria uma nova página (model + controller + view)

  fleting create view <nome>
  fleting create model <nome>
  fleting create controller <nome>

  fleting delete page <nome>
  fleting delete view <nome>
  fleting delete model <nome>
  fleting delete controller <nome>
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

> fletting run

ou

> flet run fleting/app.py

ou, alternativamente:

python fleting/app.py

        💡 Recomendado: usar `flet run` para melhor integração com o runtime do Flet.


## ✅ Fluxo Básico de Uso

```shell
pip install flet
pip install fleting

fleting init
fleting run

# para desenvolvimento
fleting create page home
flet run fleting/app.py
```

## ▶️ Executando  o CLI para desenvolvimento

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

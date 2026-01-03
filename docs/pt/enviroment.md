# Guia Rápido: Criando um Projeto Python com pyenv e Poetry

Este guia mostra passo a passo como criar um projeto Python do zero usando `pyenv` para gerenciar versões do Python e `poetry` para gerenciar dependências e ambientes virtuais.

---

## 1. Pré-requisitos

Antes de começar, instale as ferramentas necessárias:

- **pipx** (para instalar ferramentas Python globalmente)
- **pyenv** (para gerenciar versões do Python)
- **poetry** (para gerenciar projetos e dependências Python)

```bash
# Instalar pipx (se ainda não tiver)
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Instalar pyenv (veja instruções oficiais: https://github.com/pyenv/pyenv)
# Exemplo no Linux/macOS:
curl https://pyenv.run | bash

# Instalar poetry (recomendado via pipx)
pipx install poetry
```

## 2. Criar um novo projeto com Poetry

Use o comando abaixo para criar a estrutura inicial do projeto:

```shell
poetry new meu-projeto
cd meu-projeto
```

Isso criará a pasta meu-projeto/ com a estrutura básica:

```shell
meu-projeto/
```

## 3. Escolher a versão do Python com pyenv
Instale a versão desejada do Python (exemplo: 3.11.0) e defina localmente para este projeto:

```bash
pyenv install 3.11.0      # Instala a versão 3.11.0
pyenv local 3.11.0        # Define a versão local para este projeto
```

Isso criará um arquivo .python-version na pasta do projeto, indicando a versão escolhida.

## 4. Inicializar o Poetry no projeto

Caso queira configurar manualmente o pyproject.toml, rode:

```bash
poetry init
```

Isso permite definir informações do projeto e dependências.

```
meu-projeto/
├── .python-version   # Versão do Python definida pelo pyenv
├── pyproject.toml    # Configurações do projeto e dependências
```

## 5. Ativar o ambiente virtual do Poetry

Para ativar o ambiente virtual isolado criado pelo Poetry:

```bash
poetry env activate
# Creating virtualenv ...
```

O Poetry cria automaticamente um ambiente virtual isolado para o projeto.
Dependendo do seu sistema operacional, ele gera um script de ativação dentro da pasta de cache do Poetry.

Para usar o ambiente virtual, você deve executar o script indicado pelo Poetry.
No Windows, geralmente será algo como:

> & <path_do_virtualenv>\Scripts\activate.ps1


No Linux/macOS, será algo como:

> source <path_do_virtualenv>/bin/activate


        Observação: Depois de ativar o ambiente, todos os pacotes que você instalar usando poetry add serão isolados neste projeto, sem afetar outros projetos ou a instalação global do Python.

você debe ver algo asim:

> (meu-projeto-py3.11) PS C:\Users\...\meu-projeto>

Agora você está pronto para começar a desenvolver seu projeto Python de forma organizada e isolada.
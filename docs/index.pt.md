# Fleting Framework

<p align="center">
  <img src="img/fleting_logo.png" width="100"/>
</p>

Fleting é um micro-framework opinativo construído sobre **Flet**, focado em:
- simplicidade
- organização clara
- produtividade
- aplicações multiplataforma (mobile, tablet e desktop)

Ele traz uma arquitetura inspirada em MVC, com **layout desacoplado**, **roteamento simples**, **i18n**, **responsividade automática** e um **CLI para geração de código**.

<p align="center">
  <img src="img/fleting.gif" width="260" />
</p>

## 🚀 Quick Start

### 1. crie um ambiente virtual isolado

- [Recomendado: env com poetry](pt/enviroment.md)


## 🛠️ CLI

```shell
pip install flet
pip install fleting

fleting init
fleting run

# para desenvolvimento
fleting create page home
flet run fleting/app.py
```

## 📚 Documentação - Fleting Docs

A documentação completa está disponível em:

👉 [Fleting Documentação](https://alexyucra.github.io/Fleting/)

👉 [Flet Documentação](https://github.com/alexyucra/flet-docs)

👉 [Fleting Curso Completo](https://github.com/alexyucra/fleting-curso)

👉 [FLAI – Local AI Framework para Fleting](https://github.com/alexyucra/flai)

---

## 🎯 Filosofia

O Fleting foi criado com alguns princípios claros:

### 1️⃣ Simplicidade acima de tudo
- Nada de abstrações desnecessárias
- Código explícito e fácil de entender
- Arquitetura previsível

### 2️⃣ Separação de responsabilidades
- **View** → UI pura (Flet)
- **Layout** → Estrutura visual reutilizável
- **Controller** → Regras de negócio
- **Model** → Dados
- **Router** → Navegação
- **Core** → Infraestrutura do framework

### 3️⃣ Mobile-first
- O estado global da aplicação identifica automaticamente:
  - `mobile`
  - `tablet`
  - `desktop`
- Layouts podem reagir dinamicamente ao tipo de dispositivo

### 4️⃣ Internacionalização nativa
- Sistema de tradução simples baseado em JSON
- Mudança de idioma em tempo real
- Traduções acessíveis em qualquer parte da app

### 5️⃣ CLI como cidadão de primeira classe
- Criação e remoção de arquivos padronizados
- Redução de boilerplate
- Convenção > Configuração

---

## 📄 Licença

MIT

## Como contribuir
- [Para quem quiser contribuir com o Fleting no GitHub.](CONTRIBUTING.md)
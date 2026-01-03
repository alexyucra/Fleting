# 🤝 Contribuindo com o Fleting

Obrigado por seu interesse em contribuir com o **Fleting**! 🚀

Toda ajuda é bem-vinda: código, documentação, testes, exemplos, sugestões ou correções.

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

* **Python 3.10+**
* **Git**
* **Poetry** (recomendado)
* Conta no **GitHub**

---

## 🍴 1. Faça um Fork do repositório

1. Acesse o repositório oficial do Fleting no GitHub
2. Clique em **Fork** (canto superior direito)
3. Isso criará uma cópia do projeto na sua conta

---

## 💻 2. Clone o seu fork localmente

```bash
git clone https://github.com/seu-usuario/fleting.git
cd fleting
```

---

## 🌱 3. Crie uma branch para sua contribuição

Nunca trabalhe diretamente na branch `main`.

```bash
git checkout -b feature/minha-melhoria
```

Sugestões de nomes:

* `feature/novo-comando`
* `fix/bug-cli-run`
* `docs/melhorar-readme`

---

## 📦 4. Instale as dependências

Usando **Poetry**:

```bash
poetry install
poetry shell
```

Ou usando **pip** (alternativo):

```bash
pip install -e .
```

---

## 🛠️ 5. Faça suas alterações

Estrutura principal do projeto:

* `fleting/cli/` → comandos da CLI
* `fleting/cli/templates/` → templates e scaffold
* `fleting/core/` → núcleo do framework
* `README.md` → documentação

### Boas práticas

* Utilize imports absolutos (`from fleting...`)
* Mantenha o código simples e legível
* Evite quebrar comandos existentes
* Escreva mensagens de log claras

---

## 🧪 6. Teste localmente

Antes de enviar sua contribuição, teste os comandos principais:

```bash
fleting info
fleting init
fleting create page home
fleting run
```

---

## 💾 7. Commit das alterações

```bash
git add .
git commit -m "feat: adiciona comando fleting info"
```

Padrão recomendado de commits:

* `feat:` nova funcionalidade
* `fix:` correção de bug
* `docs:` documentação
* `refactor:` refatoração de código

---

## 📤 8. Envie sua branch para o GitHub

```bash
git push origin feature/minha-melhoria
```

---

## 🔁 9. Abra um Pull Request (PR)

1. Vá até o repositório original do Fleting
2. Clique em **Compare & Pull Request**
3. Descreva claramente:

   * O que foi feito
   * Por que foi feito
   * Como testar

---

## ✅ 10. Revisão e Merge

* Seu PR será revisado
* Ajustes podem ser solicitados
* Após aprovação, ele será integrado ao projeto 🎉

---

## 📜 Código de Conduta

* Seja respeitoso
* Ajude outros contribuidores
* Feedback construtivo é sempre bem-vindo

---

## 💙 Obrigado por contribuir!

Sua contribuição ajuda o **Fleting** a crescer e evoluir para toda a comunidade.

🚀 **Vamos construir juntos!**

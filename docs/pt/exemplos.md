# 🧭 Exemplos passo a passo

Roteiros completos usando a CLI. Cada exemplo começa do zero.

> Em todos os exemplos, ative antes o ambiente virtual ([Ambiente](enviroment.md)) e instale: `pip install fleting`.

---

## 1. Primeiro app (SQLite)

```bash
fleting init loja
cd loja
fleting run
```

Resultado: app com páginas **Home**, **Settings** e **Help**, layout responsivo e i18n (pt, en, es).

Para conferir a estrutura:

```bash
fleting doctor
```
```text
  ✔ .fleting found
  ✔ main.py found
  ✔ 3 route(s) checked
  ✔ Database engine: sqlite

0 error(s), 0 warning(s)
```

---

## 2. Criar uma página completa

```bash
fleting create page produtos
```

Isso gera:

| Arquivo | Classe |
|---|---|
| `app/models/produtos_model.py` | `ProdutosModel` |
| `app/controllers/produtos_controller.py` | `ProdutosController` |
| `app/views/pages/produtos_view.py` | `ProdutosView` |
| `configs/routes.py` | rota `/produtos` no menu |

Nomes com várias palavras usam *snake_case*: `fleting create page user_profile` → `UserProfileView`, `UserProfileController`, `UserProfileModel`.

```bash
fleting list pages      # model / controller / view de cada página
fleting list routes     # rotas registradas
fleting run             # a página aparece no menu
```

!!! note "Nomes válidos"
    Letras minúsculas, números e `_`, começando por letra. `minha-pagina`, `1abc` e palavras reservadas (`class`) são recusados.

---

## 3. Criar componentes avulsos

```bash
fleting create model cliente
fleting create controller cliente
fleting create view cliente
```

Uma view criada assim **não** ganha rota. O `fleting doctor` avisa:

```text
  ⚠️  View cliente_view.py has no route in configs/routes.py
```

---

## 4. Remover uma página

```bash
fleting delete page produtos
```

Remove model, controller, view **e** a rota `/produtos`. Funciona de qualquer subpasta do projeto (por exemplo, dentro de `app/views`).

```bash
fleting delete view cliente        # só a view
```

---

## 5. Banco SQLite: tabela, dados e consultas

```bash
fleting db init
fleting db make produtos
```

Edite `migrations/002_produtos.py`:

```python
from core.database import is_mysql

def up(db):
    pk = "INT AUTO_INCREMENT PRIMARY KEY" if is_mysql() else "INTEGER PRIMARY KEY AUTOINCREMENT"
    cur = db.cursor()
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS produtos (
            id {pk},
            nome VARCHAR(255),
            preco DECIMAL(10, 2)
        )
    """)
    cur.close()

def down(db):
    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS produtos")
    cur.close()
```

Aplique e crie o admin:

=== "PowerShell"

    ```powershell
    fleting db migrate
    $env:FLETING_ADMIN_PASSWORD = "SenhaForte123"
    fleting db seed
    fleting db status
    ```

=== "Linux / macOS"

    ```bash
    fleting db migrate
    FLETING_ADMIN_PASSWORD=SenhaForte123 fleting db seed
    fleting db status
    ```

Gere o model a partir da tabela e use o ORM:

```bash
fleting db model pull produtos
fleting shell
```
```text
>>> tables()
['_fleting_migrations', 'sqlite_sequence', 'users', 'produtos']
>>> ProdutosModel.create(nome="Caneta", preco=2.5)
{'id': 1, 'nome': 'Caneta', 'preco': 2.5}
>>> ProdutosModel.where(nome="Caneta")
[{'id': 1, 'nome': 'Caneta', 'preco': 2.5}]
>>> table("produtos")
>>> quit()
```

Desfazer a última migration:

```bash
fleting db rollback
```

---

## 6. Usar o ORM no controller

```python
# app/controllers/produtos_controller.py
from app.models.produtos_model import ProdutosModel

class ProdutosController:
    def listar(self):
        return ProdutosModel.all()

    def cadastrar(self, nome: str, preco: float):
        return ProdutosModel.create(nome=nome, preco=preco)
```

```python
# app/views/pages/produtos_view.py (trecho de render)
itens = [ft.Text(f"{p['nome']} — R$ {p['preco']}") for p in self.controller.listar()]
content = ft.Column(controls=itens, spacing=8)
```

---

## 7. Projeto com MySQL

```bash
docker run -d --name fleting-mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=fleting -p 3306:3306 mysql:8
pip install "fleting[mysql]"

fleting init loja --mysql
cd loja
```

Configure a conexão:

=== "PowerShell"

    ```powershell
    $env:FLETING_DB_PASSWORD = "root"
    $env:FLETING_ADMIN_PASSWORD = "SenhaForte123"
    ```

=== "Linux / macOS"

    ```bash
    export FLETING_DB_PASSWORD=root
    export FLETING_ADMIN_PASSWORD=SenhaForte123
    ```

```bash
fleting db init
fleting db migrate
fleting db seed
fleting doctor
fleting shell
```
```text
Fleting Console (MySQL 8.4.x)
>>> describe("users")
>>> query("SELECT COUNT(*) n FROM users")
[{'n': 1}]
```

---

## 8. Projeto com MariaDB

```bash
docker run -d --name fleting-mariadb -e MARIADB_ROOT_PASSWORD=root -e MARIADB_DATABASE=fleting -p 3307:3306 mariadb:11
pip install "fleting[mariadb]"

fleting init loja --mysql
cd loja
```

=== "PowerShell"

    ```powershell
    $env:FLETING_DB_DRIVER = "pymysql"
    $env:FLETING_DB_PORT = "3307"
    $env:FLETING_DB_PASSWORD = "root"
    ```

=== "Linux / macOS"

    ```bash
    export FLETING_DB_DRIVER=pymysql FLETING_DB_PORT=3307 FLETING_DB_PASSWORD=root
    ```

```bash
fleting db init && fleting db migrate
fleting shell          # o banner mostra "Fleting Console (MariaDB 11.x)"
```

---

## 9. Migrar um projeto SQLite existente para MySQL

```bash
cd loja
pip install "fleting[mysql]"
fleting db init --mysql
```
```text
Backup: core/database.py → database.py.bak
Backup: core/migrations.py → migrations.py.bak
Engine switched: sqlite → mysql
```

Depois, com as variáveis `FLETING_DB_*` definidas:

```bash
fleting db migrate
fleting db seed
```

!!! warning "Dados"
    A troca de engine **não copia dados** do SQLite para o MySQL; ela só reconfigura o projeto e reaplica as migrations no banco novo. Migrations suas que usem sintaxe só do SQLite precisam ser ajustadas (veja o exemplo 5).

Para voltar: `fleting db init --sqlite`.

---

## 10. Diagnóstico e depuração

```bash
fleting doctor               # estrutura, rotas, driver, seed
fleting info                 # versões e ambiente
```

Erros da CLI mostram só a mensagem. Para ver o traceback completo:

=== "PowerShell"

    ```powershell
    $env:FLETING_DEBUG = "1"; fleting db migrate
    ```

=== "Linux / macOS"

    ```bash
    FLETING_DEBUG=1 fleting db migrate
    ```

Códigos de saída: `0` sucesso, `1` erro (inclusive `doctor` com erros), `2` comando desconhecido.

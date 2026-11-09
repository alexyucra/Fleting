# 🗄️ Bancos de dados

O Fleting suporta **SQLite** (padrão) e **MySQL / MariaDB**. O mesmo código de models, migrations e seeds funciona nas duas engines; o que muda é só a configuração.

| Engine | Status | Driver | Instalação | Uso indicado |
|---|---|---|---|---|
| SQLite | ✅ Estável | `sqlite3` (embutido) | — | Desenvolvimento, apps embarcados/mobile |
| MySQL 8 | ✅ Estável | `mysql-connector-python` | `pip install "fleting[mysql]"` | Produção, apps web |
| MariaDB 10.6+ / 11 | ✅ Estável | `PyMySQL` (recomendado) ou `mysql-connector-python` | `pip install "fleting[mariadb]"` | Produção |
| SQL Server | 🔄 Em breve | — | — | Integrações corporativas |

---

## Escolhendo a engine

=== "Projeto novo"

    ```bash
    fleting init meuapp            # SQLite
    fleting init meuapp --mysql    # MySQL / MariaDB
    ```

=== "Projeto existente"

    ```bash
    fleting db init --mysql        # troca para MySQL / MariaDB
    fleting db init --sqlite       # volta para SQLite
    ```

    Na troca, o Fleting:

    - altera `"ENGINE"` em `configs/database.py`;
    - salva `core/database.py` e `core/migrations.py` como `*.py.bak` e gera as versões da nova engine;
    - regenera `migrations/001_initial.py` e `seeds/initial.py` **somente** se forem os arquivos padrão de versões antigas (também com backup `.bak`). Seus outros arquivos não são tocados.

Dentro de um projeto, `fleting --help` mostra os comandos da engine em uso.

---

## Configuração (`configs/database.py`)

```python
import os
# ENGINE: "sqlite" | "mysql"
DATABASE = {
    "ENGINE": "sqlite",

    "SQLITE": {
        "PATH": "data/fleting.db"
    },

    "MYSQL": {
        "DRIVER": os.environ.get("FLETING_DB_DRIVER", "mysql-connector"),  # ou "pymysql" (MariaDB)
        "HOST": os.environ.get("FLETING_DB_HOST", "localhost"),
        "PORT": int(os.environ.get("FLETING_DB_PORT", "3306")),
        "USER": os.environ.get("FLETING_DB_USER", "root"),
        "PASSWORD": os.environ.get("FLETING_DB_PASSWORD", ""),
        "NAME": os.environ.get("FLETING_DB_NAME", "fleting"),
        "OPTIONS": {
            "charset": "utf8mb4",
            "collation": "utf8mb4_general_ci"
        }
    }
}
```

!!! warning "Não grave senhas no código"
    Use as variáveis de ambiente abaixo. Mantenha a linha `"ENGINE": "..."` como texto literal: a CLI a lê para descobrir a engine.

### Variáveis de ambiente

| Variável | Padrão | Uso |
|---|---|---|
| `FLETING_DB_HOST` | `localhost` | Servidor MySQL/MariaDB |
| `FLETING_DB_PORT` | `3306` | Porta |
| `FLETING_DB_USER` | `root` | Usuário |
| `FLETING_DB_PASSWORD` | *(vazio)* | Senha |
| `FLETING_DB_NAME` | `fleting` | Nome do banco |
| `FLETING_DB_DRIVER` | `mysql-connector` | `mysql-connector` ou `pymysql` |
| `FLETING_ADMIN_PASSWORD` | — | Senha do usuário `admin` criado por `fleting db seed` |

=== "PowerShell"

    ```powershell
    $env:FLETING_DB_PASSWORD = "minhasenha"
    $env:FLETING_DB_DRIVER = "pymysql"
    ```

=== "CMD"

    ```bat
    set FLETING_DB_PASSWORD=minhasenha
    set FLETING_DB_DRIVER=pymysql
    ```

=== "Linux / macOS"

    ```bash
    export FLETING_DB_PASSWORD=minhasenha
    export FLETING_DB_DRIVER=pymysql
    ```

---

## MySQL e MariaDB com Docker

```bash
# MySQL 8
docker run -d --name fleting-mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=fleting -p 3306:3306 mysql:8

# MariaDB 11
docker run -d --name fleting-mariadb -e MARIADB_ROOT_PASSWORD=root -e MARIADB_DATABASE=fleting -p 3307:3306 mariadb:11
```

!!! tip "MariaDB"
    O `mysql-connector-python` 8.0.30+ envia a collation `utf8mb4_0900_ai_ci`, que não existe no MariaDB. O Fleting já usa `utf8mb4_general_ci` por padrão, mas o driver recomendado para MariaDB é o **PyMySQL** (`FLETING_DB_DRIVER=pymysql`).

---

## Migrations e seeds

| Comando | O que faz |
|---|---|
| `fleting db init` | Cria `migrations/`, `seeds/`, `data/` e `core/migrations.py` |
| `fleting db migrate` | Aplica as migrations pendentes (registradas em `_fleting_migrations`) |
| `fleting db make <nome>` | Cria `migrations/00N_<nome>.py` |
| `fleting db rollback` | Desfaz a última migration (`down`) |
| `fleting db status` | Lista migrations aplicadas e pendentes |
| `fleting db seed` | Executa `run(db)` de cada arquivo em `seeds/` |

Uma migration recebe a conexão em `up(db)` / `down(db)`. Use **cursor**, que funciona em todas as engines:

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

### Usuário admin do seed

`seeds/initial.py` só cria o usuário `admin` se `FLETING_ADMIN_PASSWORD` estiver definida. A senha é gravada com hash **PBKDF2-SHA256** (`pbkdf2_sha256$200000$<salt>$<hash>`), nunca em texto puro. Rodar o seed de novo não duplica o usuário.

!!! danger "Código do projeto"
    `db migrate`, `db seed` e `list routes` importam e executam arquivos Python do projeto (`migrations/`, `seeds/`, `configs/routes.py`). Só rode em projetos confiáveis.

---

## ORM

```python
from core.base_model import BaseModel

class ProdutosModel(BaseModel):
    table_name = "produtos"
```

| Método | Retorno |
|---|---|
| `Model.all()` | lista de dicts |
| `Model.first()` | dict ou `None` |
| `Model.find(id)` | dict ou `None` |
| `Model.where(campo=valor, ...)` | lista de dicts |
| `Model.count()` / `Model.exists(**filtros)` | `int` / `bool` |
| `Model.create(**dados)` | dict criado |
| `obj.save()` | insere (sem `id`) ou atualiza (com `id`) |
| `obj.delete()` | remove pelo `id` |
| `Model.with_("relacao").all()` | carrega `ForeignKey` / `HasMany` |

Nomes de tabela e colunas são validados (`[A-Za-z_][A-Za-z0-9_]*`); valores sempre vão como parâmetros. Algo como `Model.where(**{"id=1 OR 1": 1})` gera `ValueError`.

### Transações e conexão

```python
from core.database import transaction, close_connection

with transaction() as conn:          # commit no fim, rollback em caso de erro
    cur = conn.cursor()
    cur.execute("UPDATE produtos SET preco = preco * 1.1")

close_connection()                   # o app já chama isso ao fechar
```

### Gerar models a partir do banco

```bash
fleting db model pull                 # todas as tabelas
fleting db model pull produtos        # uma tabela
fleting db model pull produtos --force
```

---

## Console (`fleting shell`)

| Helper | SQLite | MySQL / MariaDB |
|---|---|---|
| `tables()` | ✅ | ✅ |
| `query(sql)` | SELECT → dicts | SELECT → dicts; INSERT/UPDATE/DELETE → commit + nº de linhas |
| `table("t")` | ✅ | ✅ (`limit=200`) |
| `describe("t")` | — | ✅ |
| `models()` / `<Model>.all()` | ✅ | ✅ |
| `conn` / `db` | conexão | conexão |

```text
>>> tables()
['_fleting_migrations', 'users']
>>> query("UPDATE users SET username=%s WHERE id=%s", ("adm", 1))
✔ 1 row(s) affected
```

---

## Diagnóstico

`fleting doctor` confere a engine configurada, se o driver MySQL está instalado e se o seed ainda usa a senha padrão antiga.

## Problemas comuns

| Erro | Causa / solução |
|---|---|
| `MySQL support requires: pip install "fleting[mysql]"` | Instale o driver (ou `fleting[mariadb]` com `DRIVER=pymysql`) |
| `Unknown collation: utf8mb4_0900_ai_ci` | MariaDB + connector antigo: use `FLETING_DB_DRIVER=pymysql` |
| `Access denied for user` | Confira `FLETING_DB_USER` / `FLETING_DB_PASSWORD` |
| `Unknown database` | Crie o banco (`CREATE DATABASE fleting`) ou ajuste `FLETING_DB_NAME` |
| `Can't connect to MySQL server` | Servidor parado ou porta errada (`FLETING_DB_PORT`) |
| `'Connection' object has no attribute 'execute'` | Migration/seed antigo usando `db.execute`: troque por `db.cursor().execute(...)` |

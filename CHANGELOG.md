# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e [SemVer](https://semver.org/lang/pt-BR/).

## [1.3.0] - 2026-11-09

### Added
- `fleting shell` com suporte a **MySQL e MariaDB**: `tables()`, `describe()`, `table(name, limit)`, `query(sql, params)` (DML com commit) e carregamento dos models de `app/models`.
- Extras de instalação: `pip install "fleting[mysql]"` e `pip install "fleting[mariadb]"` (PyMySQL).
- `configs/database.py`: chaves `DRIVER` (`mysql-connector` | `pymysql`) e `OPTIONS.collation` (padrão `utf8mb4_general_ci`, compatível com MariaDB).
- `fleting doctor`: verifica estrutura do projeto, rotas sem view, views sem rota, driver MySQL e seed com senha padrão.
- `core/database.py`: `transaction()`, `close_connection()` e conexão SQLite segura entre threads. O app fecha a conexão ao encerrar.
- `fleting db init --mysql|--sqlite` troca a engine de um projeto existente, com backup `.bak` de `core/database.py` e `core/migrations.py`.
- Suíte de testes (pytest) e workflow de CI com SQLite, MySQL 8 e MariaDB 11.

### Changed
- `configs/database.py` lê credenciais MySQL de `FLETING_DB_HOST`, `FLETING_DB_PORT`, `FLETING_DB_USER`, `FLETING_DB_PASSWORD`, `FLETING_DB_NAME` e `FLETING_DB_DRIVER`.
- `fleting db seed` só cria o usuário `admin` se `FLETING_ADMIN_PASSWORD` estiver definida; a senha é gravada com hash PBKDF2-SHA256.
- A CLI sai com código `1` em erro (traceback só com `FLETING_DEBUG=1`) e `2` em comando desconhecido.
- `__version__` passa a vir do metadata do pacote.
- Removidas as dependências não usadas `typer` e `psutil`.
- GitHub Actions: `checkout@v4`, `setup-python@v5`; o publish roda os testes antes do build.

### Fixed
- ORM: funciona com MySQL (placeholders `%s` e cursor dict), import circular entre `core/base_model.py` e `core/orm.py`, e `save()` (insere e atualiza corretamente).
- `fleting create` com nomes snake_case (`user_profile` → `UserProfileView/Controller/Model`), validação de nomes e verificação de projeto.
- `fleting delete page` funciona a partir de subpastas e remove a rota de `configs/routes.py`.
- `register_route` aceita variações de espaço em `ROUTES = [`.
- `fleting init` no Linux/macOS (`NameError: os` ao criar symlink).
- `fleting db model pull` e `fleting shell` no SQLite (assinatura incorreta das funções; `PRAGMA` inválido).
- Migrations, rollback, status e seed no MySQL (`connection.execute` não existe no mysql-connector).
- `main.py` usa o idioma de `AppState.language`.

### Security
- ORM, `shell` e `db model pull` validam identificadores SQL (tabelas/colunas), evitando injeção via nomes.
- Fim da credencial padrão `admin/fleting` no seed.

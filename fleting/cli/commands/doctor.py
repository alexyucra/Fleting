# fleting/cli/commands/doctor.py
"""`fleting doctor`: diagnóstico do projeto. Não altera nenhum arquivo."""
import ast
import importlib
import importlib.util
from pathlib import Path

from fleting.cli.console.console import console
from fleting.cli.helpers.project import get_project_root


def _routes_from_file(routes_file: Path) -> list[dict]:
    """Extrai path/view de ROUTES sem executar o arquivo."""
    tree = ast.parse(routes_file.read_text(encoding="utf-8"))
    routes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "ROUTES" for t in node.targets
        ) and isinstance(node.value, ast.List):
            for item in node.value.elts:
                if not isinstance(item, ast.Dict):
                    continue
                entry = {}
                for k, v in zip(item.keys, item.values):
                    if isinstance(k, ast.Constant) and isinstance(v, ast.Constant):
                        entry[k.value] = v.value
                routes.append(entry)
    return routes


def run_checks(root: Path) -> list[tuple[str, str]]:
    """Retorna lista de (nível, mensagem). nível ∈ {"ok", "warning", "error"}."""
    results: list[tuple[str, str]] = []

    def ok(msg):
        results.append(("ok", msg))

    def warn(msg):
        results.append(("warning", msg))

    def err(msg):
        results.append(("error", msg))

    # 1. estrutura
    for rel in (".fleting", "main.py", "configs/routes.py", "configs/database.py"):
        (ok if (root / rel).exists() else err)(f"{rel} {'found' if (root / rel).exists() else 'missing'}")

    # 2/3. rotas x views
    routes_file = root / "configs" / "routes.py"
    if routes_file.exists():
        try:
            routes = _routes_from_file(routes_file)
        except SyntaxError as e:
            err(f"configs/routes.py has a syntax error: {e}")
            routes = []

        routed_modules = set()
        for r in routes:
            view = r.get("view", "")
            module_path = view.rsplit(".", 1)[0] if "." in view else ""
            routed_modules.add(module_path)
            file = root / (module_path.replace(".", "/") + ".py")
            if not file.exists():
                err(f"Route {r.get('path')!r} points to missing view {view!r}")
        if routes:
            ok(f"{len(routes)} route(s) checked")

        pages = root / "app" / "views" / "pages"
        if pages.exists():
            for f in sorted(pages.glob("*_view.py")):
                mod = f"app.views.pages.{f.stem}"
                if mod not in routed_modules:
                    warn(f"View {f.name} has no route in configs/routes.py")

    # 5. driver MySQL
    db_cfg = root / "configs" / "database.py"
    if db_cfg.exists():
        from fleting.cli.commands.db import get_engine_from_config

        engine = get_engine_from_config(root)
        ok(f"Database engine: {engine}")
        if engine == "mysql":
            text = db_cfg.read_text(encoding="utf-8")
            driver_mod = "pymysql" if '"pymysql"' in text and "DRIVER" in text else "mysql.connector"
            try:
                found = importlib.util.find_spec(driver_mod) is not None
            except ModuleNotFoundError:
                found = False
            if found:
                ok(f"MySQL driver installed ({driver_mod})")
            else:
                extra = "mariadb" if driver_mod == "pymysql" else "mysql"
                err(f'MySQL driver {driver_mod} not installed: pip install "fleting[{extra}]"')

    # 6. seed com senha padrão
    seeds = root / "seeds"
    if seeds.exists():
        for f in seeds.glob("*.py"):
            txt = f.read_text(encoding="utf-8")
            if "'fleting'" in txt or '"fleting")' in txt:
                warn(f"seeds/{f.name} seems to contain the default password 'fleting' (see FLETING_ADMIN_PASSWORD)")

    # core/ antigo (ORM sem _ident / sem placeholder)
    base_model = root / "core" / "base_model.py"
    if base_model.exists() and "_ident" not in base_model.read_text(encoding="utf-8"):
        warn("core/base_model.py is from an older Fleting version (no SQL identifier validation)")

    return results


def handle_doctor(args=None):
    root = get_project_root()
    if not root:
        return

    console.print(f"🩺 Fleting doctor — {root}", style="info")
    results = run_checks(root)
    icons = {"ok": "✔", "warning": "⚠️ ", "error": "❌"}
    styles = {"ok": "success", "warning": "warning", "error": "error"}
    for level, msg in results:
        console.print(f"  {icons[level]} {msg}", style=styles[level])

    errors = sum(1 for lvl, _ in results if lvl == "error")
    warnings = sum(1 for lvl, _ in results if lvl == "warning")
    console.print(f"\n{errors} error(s), {warnings} warning(s)", style="error" if errors else "success")
    return errors

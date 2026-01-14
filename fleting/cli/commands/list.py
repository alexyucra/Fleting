from pathlib import Path
import importlib.util
import sys
from .rich_console import console

# ----------------------
# Utils
# ----------------------
def get_project_root() -> Path:
    return Path.cwd()

def is_fleting_project(path: Path) -> bool:
    return (path / "main.py").exists() and (path / "configs").exists()

def print_table(headers, rows):
    col_sizes = [len(h) for h in headers]

    for row in rows:
        for i, cell in enumerate(row):
            col_sizes[i] = max(col_sizes[i], len(str(cell)))

    def fmt(row):
        return " | ".join(str(cell).ljust(col_sizes[i]) for i, cell in enumerate(row))

    console.print(fmt(headers))
    console.print("-+-".join("-" * s for s in col_sizes))

    for row in rows:
        console.print(fmt(row))

# ----------------------
# Handlers
# ----------------------
def handle_list(args):
    root = get_project_root()

    if not is_fleting_project(root):
        console.print("❌ This directory is not a Fleting project.", style="error")
        return

    if not args:
        console.print("Use: fleting list <pages|controllers|views|models|routes>", style="suggestion")
        return

    kind = args[0]

    if kind == "controllers":
        list_simple(root / "controllers", "_controller.py", "Controller")
    elif kind == "views":
        list_simple(root / "views" / "pages", "_view.py", "View")
    elif kind == "models":
        list_simple(root / "models", "_model.py", "Model")
    elif kind == "routes":
        list_routes(root)
    elif kind == "pages":
        list_pages(root)
    else:
        console.print(f"Unknown list type: {kind}", style="warning")

# ----------------------
# Simple lists
# ----------------------
def list_simple(path: Path, suffix: str, label: str):
    rows = []

    if not path.exists():
        console.print(f"No {label.lower()}s found.", style="warning")
        return

    for file in sorted(path.glob(f"*{suffix}")):
        name = file.stem.replace(suffix.replace(".py", ""), "")
        rows.append([name, file.name])

    print_table([label, "File"], rows)

# ----------------------
# Pages (MVC + route)
# ----------------------
def list_pages(root: Path):
    rows = []

    models = {f.stem.replace("_model", "") for f in (root / "models").glob("*_model.py")}
    controllers = {f.stem.replace("_controller", "") for f in (root / "controllers").glob("*_controller.py")}
    views = {f.stem.replace("_view", "") for f in (root / "views" / "pages").glob("*_view.py")}

    routes = load_routes(root)

    all_pages = sorted(models | controllers | views | routes.keys())

    for name in all_pages:
        rows.append([
            name,
            "✔" if name in models else "—",
            "✔" if name in controllers else "—",
            "✔" if name in views else "—",
            f"/{name}" if name in routes else "—",
        ])

    print_table(
        ["Page", "Model", "Controller", "View", "Route"],
        rows
    )

# ----------------------
# Routes
# ----------------------
def list_routes(root: Path):
    routes = load_routes(root)

    rows = []
    for path, view in routes.items():
        rows.append([path, view])

    print_table(["Route", "View"], rows)

def load_routes(root: Path):
    routes_file = root / "configs" / "routes.py"

    spec = importlib.util.spec_from_file_location("routes", routes_file)
    routes_module = importlib.util.module_from_spec(spec)
    sys.modules["routes"] = routes_module
    spec.loader.exec_module(routes_module)

    return {r["path"].replace("/", ""): r["view"] for r in routes_module.ROUTES}
from pathlib import Path
import importlib.util
import sys
from typing import Dict, List, Set
from fleting.cli.console import (
    console, 
    print_simple_table,     
    print_pages_table,       
    print_routes_table,      
    create_table
)

# ----------------------
# Utils
# ----------------------
def get_project_root() -> Path:
    return Path.cwd()

def is_fleting_project(path: Path) -> bool:
    return (path / "main.py").exists() and (path / "configs").exists()

def print_table_2(headers, rows):
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

def print_table(headers: List[str], rows: List[List[str]], title: str = ""):
    """Función de compatibilidad para reemplazar la antigua print_table"""
    table = create_table(title, [(h, "bold cyan", 20) for h in headers])
    
    for row in rows:
        styled_row = []
        for i, cell in enumerate(row):
            if headers[i].lower() in ["model", "controller", "view"]:
                if cell == "✔":
                    styled_cell = "[green]✔[/green]"
                else:
                    styled_cell = "[dim red]—[/dim red]"
            elif headers[i].lower() == "route":
                styled_cell = f"[yellow]{cell}[/yellow]"
            else:
                styled_cell = f"[cyan]{cell}[/cyan]"
            styled_row.append(styled_cell)
        
        table.add_row(*styled_row)
    
    console.print()
    console.print(table)
# ----------------------
# Handlers
# ----------------------
def handle_list(args):
    root = get_project_root()

    if not is_fleting_project(root):
        console.print("❌ This directory is not a Fleting project.", style="error")
        return

    if not args:
        console.print("[bold yellow]Usage:[/bold yellow] fleting list <pages|controllers|views|models|routes>")
        console.print("\n[yellow]Available options:[/yellow]")
        options_table = console.create_table(columns=[("Option", "bold green", 15), ("Description", "cyan", 40)])
        options_table.add_row("pages", "List all pages with MVC components")
        options_table.add_row("controllers", "List all controllers")
        options_table.add_row("views", "List all views")
        options_table.add_row("models", "List all models")
        options_table.add_row("routes", "List all routes")
        console.print(options_table)
        return
        # console.print("Use: fleting list <pages|controllers|views|models|routes>", style="suggestion")
        # return

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
        console.print(f"[dim]Available options: pages, controllers, views, models, routes[/dim]")

# ----------------------
# Simple lists
# ----------------------
def list_simple(path: Path, suffix: str, title: str):
    rows = []

    if not path.exists():
        console.print(f"No {title.lower()} found.", style="warning")
        return

    for file in sorted(path.glob(f"*{suffix}")):
        name = file.stem.replace(suffix.replace(".py", ""), "")
        file_size = file.stat().st_size
        rows.append([name, file.name, f"{file_size:,} bytes"])

    print_simple_table(
        headers=[
            ("Name", "bold green", 20),
            ("File", "cyan", 25),
            ("Size", "dim", 15)
        ],
        rows=rows,
        title=title
    )

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

    if not routes:
        console.print("No routes found.", style="warning")
        return

    rows = []
    for path, view in sorted(routes.items()):
        # Extraer nombre del controlador de la view string
        view_name = view.split('.')[-1] if '.' in view else view
        rows.append([f"/{path}", view_name])

    print_routes_table(
        headers=[
            ("Route", "bold green", 25),
            ("View", "cyan", 30)
        ],
        rows=rows
    )

def load_routes(root: Path) -> Dict[str, str]:
    """charge route from routes.py"""
    routes_file = root / "configs" / "routes.py"
    
    if not routes_file.exists():
        return {}

    try:
        spec = importlib.util.spec_from_file_location("routes", routes_file)
        routes_module = importlib.util.module_from_spec(spec)
        sys.modules["routes"] = routes_module
        spec.loader.exec_module(routes_module)
        
        routes_dict = {}
        for r in routes_module.ROUTES:
            path = r["path"].replace("/", "")
            routes_dict[path] = r["view"]
        return routes_dict
    except Exception as e:
        console.print(f"Could not load routes: {e}", style="warning")
        return {}
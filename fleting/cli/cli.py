import sys
from fleting.cli.commands.init import handle_init
from fleting.cli.commands.run import handle_run
from fleting.cli.commands.info import handle_info
from fleting.cli.commands.create import handle_create
from fleting.cli.commands.delete import handle_delete
from fleting.cli.commands.list import handle_list
from fleting.cli.commands.db import handle_db
from fleting.cli.commands.shell import handle_shell
from fleting.cli.commands.pull import handle_pull
from fleting.cli.commands.doctor import handle_doctor

from fleting.cli.console.console import console
from fleting.cli.console import Table, Panel, box
import os
import traceback
from rich.markup import escape

def print_help():
    console.clear()
    
    # Título principal
    console.print()
    console.rule("[bold cyan]🚀 Fleting CLI[/bold cyan]", style="cyan")
    console.print()
    
    # Panel de uso
    console.print(Panel.fit(
        "[bold green]fleting <command> [options][/bold green]",
        title="[yellow]📌 Usage[/yellow]",
        border_style="yellow",
        padding=(1, 2)
    ))
    console.print()
    
    table = Table(
        show_header=True,
        header_style="bold magenta",
        box=box.ROUNDED,
        border_style="blue",
        padding=(0, 1)
    )
    
    table.add_column("Command", style="bold green", width=36)
    table.add_column("Description", style="cyan", width=44)
    
    from fleting.cli.engines import ENGINES, current_project_engine

    active_engine = current_project_engine()

    # Comandos organizados por categorías
    categories = {
        "💼 Project Commands": [
            ("fleting init <app_name>", "Initialize a new Fleting project (SQLite)"),
            ("fleting info", "Show version and system information"),
            ("fleting run", "Run the application"),
            ("fleting doctor", "Check the project for common problems"),
        ],
        "➕ Create Commands": [
            ("fleting create page <name>", "Create a page (model + controller + view)"),
            ("fleting create view <name>", "Create a new view"),
            ("fleting create model <name>", "Create a new model"),
            ("fleting create controller <name>", "Create a new controller"),
        ],
        "🗑️  Delete Commands": [
            ("fleting delete page <name>", "Delete an existing page"),
            ("fleting delete view <name>", "Delete a view"),
            ("fleting delete model <name>", "Delete a model"),
            ("fleting delete controller <name>", "Delete a controller"),
        ],
        "📋 List Commands": [
            ("fleting list pages", "List all pages"),
            ("fleting list controllers", "List all controllers"),
            ("fleting list views", "List all views"),
            ("fleting list models", "List all models"),
            ("fleting list routes", "List all routes"),
        ],
        "🗄️  Database Commands": [
            ("fleting db init", "Initialize the database"),
            ("fleting db migrate", "Run database migrations"),
            ("fleting db seed", "Seed the database with initial data"),
            ("fleting db make <name>", "Create a new migration"),
            ("fleting db rollback", "Rollback the last migration"),
            ("fleting db status", "Show current database migration status"),
        ],
        "🗄️  Database / Models": [
            ("fleting db model pull", "Generate models from the database schema"),
            ("fleting db model pull <table>", "Generate model for a specific table"),
            ("fleting db model pull <table> --force", "Overwrite existing model files"),
        ],
        "🧩  Console Command": [
            ("fleting shell", "Open interactive database shell (SQLite, MySQL/MariaDB)"),
        ],
    }

    # Inicialização com banco de dados (gerado a partir do registro de engines)
    items = list(categories.items())
    items.insert(1, ("🛢️  Init with Database", [
        (f"fleting init <app_name> {e.flag}", f"New project using {e.label}")
        for e in ENGINES.values() if e.flag
    ]))
    categories = dict(items)

    # Comandos específicos da engine: dentro de um projeto mostra só a engine ativa;
    # fora de um projeto mostra todas
    shown = [ENGINES[active_engine]] if active_engine else list(ENGINES.values())
    for e in shown:
        title = f"{e.icon} {e.label} (this project)" if active_engine else f"{e.icon} {e.label} Commands"
        categories[title] = [(escape(cmd), escape(desc)) for cmd, desc in e.commands]

    for category, commands in categories.items():
        # Añadir separador para categorías
        if list(categories.keys()).index(category) > 0:
            table.add_row("─" * 36, "─" * 44, style="dim")
        
        # Añadir título de categoría
        table.add_row(
            f"[bold yellow]{category}[/bold yellow]",
            "",
            style="yellow"
        )
        
        # Añadir comandos de la categoría
        for cmd, desc in commands:
            table.add_row(f"  {cmd}", desc)
    
    console.print(table)
    console.print()

def main():
    
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print_help()
        return

    command = args[0]
    
    try:
        if command == "init":
            handle_init(args[1:])
        elif command == "run":
            handle_run()
        elif command == "info":
            handle_info()
        elif command == "create":
            handle_create(args[1:])
        elif command == "delete":
            handle_delete(args[1:])
        elif command == "list":
            handle_list(args[1:])
        elif command == "db":
            handle_db(args[1:])
        elif command == "shell":
            handle_shell()
        elif command == "pull":
            handle_pull(args[1:])
        elif command == "doctor":
            if handle_doctor(args[1:]):
                sys.exit(1)
        else:
            console.print(f"Unknown command: {command}", style="error")
            console.print("Use: fleting --help", style="suggestion")
            sys.exit(2)

    except Exception as e:
        console.print(f"Error: {e}", style="error")
        if os.environ.get("FLETING_DEBUG") == "1":
            traceback.print_exc()
        else:
            console.print("Set FLETING_DEBUG=1 to see the full traceback.", style="suggestion")
        sys.exit(1)

if __name__ == "__main__":
    main()

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

from fleting.cli.console.console import console
from fleting.cli.console import Table, Panel, Text, box, Rule
import traceback

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
    
    # Comandos organizados por categorías
    categories = {
        "💼 Project Commands": [
            ("fleting init <app_name>", "Initialize a new Fleting project"),
            ("fleting info", "Show version and system information"),
            ("fleting run", "Run the application"),
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
            ("fleting shell", "Open interactive database shell (SQLite only)"),
        ],
    }
    
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
        else:
            print(f"Unknown command: {command}")
            print_help()

    except Exception as e:
        print("Error executing CLI command:", str(e))
        traceback.print_exc() 

if __name__ == "__main__":
    main()

import sys
from fleting.cli.commands.init import handle_init
from fleting.cli.commands.run import handle_run
from fleting.cli.commands.info import handle_info
from fleting.cli.commands.create import handle_create
from fleting.cli.commands.delete import handle_delete
from fleting.cli.commands.list import handle_list
from fleting.cli.commands.db import handle_db

def print_help():
    # ANSI Colors
    RESET = "\033[0m"
    BOLD = "\033[1m"

    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"
    GRAY = "\033[90m"

    # Header
    print(f"""
{CYAN}{BOLD}🚀 Fleting CLI{RESET}
{GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

{YELLOW}📌 Usage:{RESET}
  {GREEN}fleting <command> [options]{RESET}
""")
    
    # Table header
    print(
        f"\n{MAGENTA}{BOLD}📖 Available Commands{RESET}\n"
        f"{BLUE}┌──────────────────────────────────────┬──────────────────────────────────────────────┐{RESET}\n"
        f"{BLUE}│ {BOLD}Command{RESET}{BLUE}                              │ {BOLD}Description{RESET}{BLUE}                                  │{RESET}\n"
        f"{BLUE}├──────────────────────────────────────┼──────────────────────────────────────────────┤{RESET}"
    )
    
    rows = [
        ("fleting init <app_name>", "Initialize a new Fleting project"),
        ("fleting info", "Show version and system information"),
        ("fleting run", "Run the application"),

        ("fleting create page <name>", "Create a page (model + controller + view)"),
        ("fleting create view <name>", "Create a new view"),
        ("fleting create model <name>", "Create a new model"),
        ("fleting create controller <name>", "Create a new controller"),

        ("fleting delete page <name>", "Delete an existing page"),
        ("fleting delete view <name>", "Delete a view"),
        ("fleting delete model <name>", "Delete a model"),
        ("fleting delete controller <name>", "Delete a controller"),

        ("fleting list pages", "List all pages"),
        ("fleting list controllers", "List all controllers"),
        ("fleting list views", "List all views"),
        ("fleting list models", "List all models"),
        ("fleting list routes", "List all routes"),

        ("fleting db init", "Initialize the database"),
        ("fleting db migrate", "Run database migrations"),
        ("fleting db seed", "Seed the database with initial data"),
        ("fleting db make <name>", "Create a new migration"),
        ("fleting db rollback", "Rollback the last migration"),
        ("fleting db status", "Show current database migration status"),
    ]

    for cmd, desc in rows:
        print(
            f"{BLUE}│ {GREEN}{BOLD}{cmd:<36}{RESET}{BLUE} │ {CYAN}{desc:<44}{BLUE} │{RESET}"
        )

    print(
        f"{BLUE}└──────────────────────────────────────┴──────────────────────────────────────────────┘{RESET}\n\n"
        f"{GRAY}✨ Tip: use {GREEN}fleting <command> -h{GRAY} for command-specific help.{RESET}"
    )

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
        else:
            print(f"Unknown command: {command}")
            print_help()

    except Exception as e:
         print("Error executing CLI command:", str(e))

if __name__ == "__main__":
    main()

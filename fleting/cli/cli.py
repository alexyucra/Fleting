import sys
from fleting.cli.commands.init import handle_init
from fleting.cli.commands.run import handle_run
from fleting.cli.commands.info import handle_info
from fleting.cli.commands.create import handle_create
from fleting.cli.commands.delete import handle_delete
from fleting.cli.commands.list import handle_list

def print_help():
    print("""
Fleting CLI

Usages:

    fleting init
            Initializes a new Fleting project
          
    fleting info 
            Version and library information
          
    fleting run 
            Runs the app

    fleting create page <name> 
          Creates a new page (model + controller + view)
    
    fleting create view <name>
    fleting create model <name>
    fleting create controller <name>

    fleting delete page <name>
    fleting delete view <name>
    fleting delete model <name>
    fleting delete controller <name>
""")

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
        else:
            print(f"Unknown command: {command}")
            print_help()

    except Exception as e:
         print("Error executing CLI command:", str(e))

if __name__ == "__main__":
    main()

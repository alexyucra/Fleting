import sys
from fleting.cli.commands.init import handle_init
from fleting.cli.commands.run import handle_run
from fleting.cli.commands.info import handle_info
from fleting.cli.commands.create import handle_create
from fleting.cli.commands.delete import handle_delete

def print_help():
    print("""
Fleting CLI

Uso:
  fleting init
      Inicializa um novo projeto Fleting

  fleting create page <nome>
      Cria uma nova página (model + controller + view)

  fleting create view <nome>
  fleting create model <nome>
  fleting create controller <nome>

  fleting delete page <nome>
  fleting delete view <nome>
  fleting delete model <nome>
  fleting delete controller <nome>
""")

def main():
    
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print_help()
        return

    command = args[0]
    
    try:
        if command == "init":
            handle_init()
        elif command == "run":
            handle_run()
        elif command == "info":
            handle_info()
        elif command == "create":
            handle_create(args[1:])
        elif command == "delete":
            handle_delete(args[1:])
        else:
            print(f"Comando desconhecido: {command}")
            print_help()

    except Exception as e:
        print("Erro ao executar comando CLI: {e}")

if __name__ == "__main__":
    main()

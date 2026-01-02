import sys

from fleting.cli.commands.create import handle_create
from fleting.cli.commands.delete import handle_delete

def main():
    try:
        args = sys.argv[1:]

        if not args:
            print("Uso: fleting create <controller|view|model|page> <nome>")
            return

        command = args[0]

        if command == "create":
            handle_create(args[1:])
        elif command == "delete":
            handle_delete(args[1:])
        else:
            print(f"Comando desconhecido: {command}")

    except Exception as e:
        print("Erro ao executar comando CLI")

if __name__ == "__main__":
    main()

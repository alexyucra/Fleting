import sys
from fleting.core.logger import get_logger
from fleting.cli.commands.create import handle_create
from fleting.cli.commands.delete import handle_delete

logger = get_logger("CLI")

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
            logger.warning(f"Comando desconhecido: {command}")
            print(f"Comando desconhecido: {command}")

    except Exception as e:
        logger.exception("Erro no CLI")
        print("Erro ao executar comando CLI")

if __name__ == "__main__":
    main()

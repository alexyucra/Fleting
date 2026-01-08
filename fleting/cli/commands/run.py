import subprocess
import sys
import shutil
from pathlib import Path

def handle_run():
    project_root = Path.cwd()
    app_path = project_root / "app.py"

    if not app_path.exists():
        print("❌ app.py não encontrado.")
        print("👉 Execute este comando dentro de um projeto Fleting.")
        return

    if not shutil.which("flet"):
        print("❌ Flet não está instalado no ambiente")
        print("👉 pip install flet")
        return

    print("🚀 Iniciando aplicação Fleting...\n")

    try:
        subprocess.run(
            ["flet", "run", str(app_path)],
            check=True
        )
    except subprocess.CalledProcessError:
        print("❌ Erro ao executar o app com Flet")

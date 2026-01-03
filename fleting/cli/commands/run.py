import subprocess
import sys
import shutil
from pathlib import Path

def handle_run():
    project_root = Path.cwd()
    app_path = project_root / "fleting" / "app.py"

    if not shutil.which("flet"):
        print("❌ Flet não está instalado no ambiente")
        print("👉 pip install flet")
        return

    if not app_path.exists():
        print("❌ fleting/app.py não encontrado.")
        print("👉 Execute 'fleting init' primeiro.")
        return

    print("🚀 Iniciando aplicação Fleting...\n")

    try:
        subprocess.run(
            ["flet", "run", str(app_path)],
            check=True
        )
    except subprocess.CalledProcessError:
        print("❌ Erro ao executar o app com Flet")

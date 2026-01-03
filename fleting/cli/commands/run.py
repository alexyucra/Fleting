import subprocess
import sys
from pathlib import Path

def handle_run():
    app_path = Path.cwd() / "fleting" / "app.py"

    if not shutil.which("flet"):
        print("❌ Flet não está instalado")
        print("👉 pip install flet")
        return

    if not app_path.exists():
        print("❌ app.py não encontrado. Execute 'fleting init' primeiro.")
        return

    print("🚀 Iniciando aplicação Fleting...\n")
    subprocess.run([sys.executable, str(app_path)])

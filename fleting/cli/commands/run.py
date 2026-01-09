import subprocess
import sys
import shutil
from pathlib import Path
from rich_console import console

def handle_run():
    project_root = Path.cwd()
    app_path = project_root / "app.py"

    if not app_path.exists():
        console.print("❌ app.py não encontrado.", style="error")
        console.print("👉 Execute este comando dentro de um projeto Fleting.", style="suggestion")
        return

    if not shutil.which("flet"):
        console.print("❌ Flet não está instalado no ambiente", style="error")
        console.print("👉 pip install flet", style="suggestion")
        return

    console.print("🚀 Iniciando aplicação Fleting...\n", style="info")

    try:
        subprocess.run(
            ["flet", "run", str(app_path)],
            check=True
        )
    except subprocess.CalledProcessError:
        console.print("❌ Erro ao executar o app com Flet", style="error")
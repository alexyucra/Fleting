import subprocess
import sys
import shutil
from pathlib import Path

def handle_run():
    project_root = Path.cwd()
    app_path = project_root / "main.py"

    if not app_path.exists():
        print("❌ main.py not found.")
        print("👉 Execute this command within a Fleting project.")
        return

    if not shutil.which("flet"):
        print("❌ Flet is not installed in the environment.")
        print("👉 pip install flet")
        return

    print("🚀 Starting Fleting application..\n")

    try:
        subprocess.run(
            ["flet", "run", str(app_path)],
            check=True
        )
    except subprocess.CalledProcessError:
        print("❌ Error running the app with Flat")

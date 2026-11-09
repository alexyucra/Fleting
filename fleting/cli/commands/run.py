import subprocess
import shutil
from pathlib import Path
from fleting.cli.console.console import console

def handle_run():
    project_root = Path.cwd()
    app_path = project_root / "main.py"

    if not app_path.exists():
        console.print("❌ main.py not found.", style="error")
        console.print("👉 Execute this command within a Fleting project.", style="suggestion")
        return

    if not shutil.which("flet"):
        console.print("❌ Flet is not installed in the environment.", style="error")
        console.print("👉 pip install flet", style="suggestion")
        return

    console.print("🚀 Starting Fleting application..\n", style="info")

    try:
        subprocess.run(
            ["flet", "run", str(app_path)],
            check=True
        )
    except subprocess.CalledProcessError:
        console.print("❌ Error running the app with Flet", style="error")

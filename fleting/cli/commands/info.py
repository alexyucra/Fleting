import platform
import sys
from importlib import metadata
from fleting.cli.console.console import console

BANNER = r"""
 ______ _      _   _             
|  ____| |    | | (_)            
| |__  | | ___| |_ _ _ __   __ _ 
|  __| | |/ _ \ __| | '_ \ / _` |
| |    | |  __/ |_| | | | | (_| |
|_|    |_|\___|\__|_|_| |_|\__, |
                            __/ |
                           |___/
"""

def _get_version(pkg_name: str):
    try:
        return metadata.version(pkg_name)
    except metadata.PackageNotFoundError:
        return "not installed"

def handle_info():
    python_version = sys.version.split()[0]
    system = f"{platform.system()} {platform.release()}"

    flet_version = _get_version("flet")
    fleting_version = _get_version("fleting")

    console.print(BANNER)
    console.print("🚀 Fleting Framework\n", style="header")
    console.print("\n📚 Installed libraries:", style="subtitle")
    for dist in sorted(metadata.distributions(), key=lambda d: d.metadata["Name"].lower()):
        name = dist.metadata["Name"]
        version = dist.version
        console.print(f"  - {name}=={version}", style="muted")

    
    console.print("📦 Environment\n", style="subtitle")
    console.print(f"🧠 Python        : {python_version}", style="label")
    console.print(f"🖥️  System      : {system}", style="label")
    console.print(f"🧩 Flet          : {flet_version}", style="label")
    console.print(f"🚀 Fleting       : {fleting_version}", style="label")

    console.print("\n✅ Ready-to-use environment.\n", style="success")

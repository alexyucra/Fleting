import platform
import sys
from importlib import metadata
from rich_console import console

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
        return "não instalado"

def handle_info():
    python_version = sys.version.split()[0]
    system = f"{platform.system()} {platform.release()}"

    flet_version = _get_version("flet")
    fleting_version = _get_version("fleting")

    print(BANNER)
    console.print("🚀 Fleting Framework\n", style="title")

    console.print("📦 Ambiente\n", style="subtitle")
    console.print(f"🧠 Python        : {python_version}", style="label")
    console.print(f"🖥️  Sistema      : {system}", style="label")
    console.print(f"🧩 Flet          : {flet_version}", style="label")
    console.print(f"🚀 Fleting       : {fleting_version}", style="label")

    console.print("\n📚 Bibliotecas instaladas:", style="title")
    for dist in sorted(metadata.distributions(), key=lambda d: d.metadata["Name"].lower()):
        name = dist.metadata["Name"]
        version = dist.version
        console.print(f"  - {name}=={version}", style="info")

    console.print("\n✅ Ambiente pronto para uso.\n", style="success")
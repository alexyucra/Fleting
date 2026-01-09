import platform
import sys
from importlib import metadata

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

    print(BANNER)
    print("🚀 Fleting Framework\n")

    print("📦 Environment\n")
    print(f"🧠 Python        : {python_version}")
    print(f"🖥️  Sistem      : {system}")
    print(f"🧩 Flet          : {flet_version}")
    print(f"🚀 Fleting       : {fleting_version}")

    print("\n📚 Installed libraries:")
    for dist in sorted(metadata.distributions(), key=lambda d: d.metadata["Name"].lower()):
        name = dist.metadata["Name"]
        version = dist.version
        print(f"  - {name}=={version}")

    print("\n✅ Ready-to-use environment.\n")

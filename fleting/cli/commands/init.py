from pathlib import Path
import shutil
import stat
import sys
from fleting.cli.templates.index import init_project
from fleting.cli.console.console import console

DEFAULT_PROJECT_NAME = "app"
DEFAULT_APP_NAME = "fleting"
CLI_NAME = "fleting" 

def _create_launcher(project_root: Path, cli_name: str = CLI_NAME):
    """Creates a launcher/shortcut for the Fleting executable"""
    BASE = project_root
    bin_dir = BASE / "bin"
    
    bin_dir.mkdir(parents=True, exist_ok=True)
    
    fleting_exe = None
    
    if sys.platform == "win32":
        # For Windows
        possible_names = ["fleting.exe", "fleting"]
    else:
        # For Unix-like (Linux, macOS)
        possible_names = ["fleting"]
    
    for name in possible_names:
        found = shutil.which(name)
        if found:
            fleting_exe = Path(found)
            break
    
    if not fleting_exe:
        console.print("Fleting not found in system", style="error")
        console.print("Project will be created without local launcher", style="warning")
        return False
    
    if sys.platform == "win32":
        # Windows: create .bat file named "fleting.bat"
        launcher_path = bin_dir / f"{cli_name}.bat"
        launcher_content = f'@"{fleting_exe}" %*'
        launcher_path.write_text(launcher_content, encoding='utf-8')
        
        # Optional: also create .ps1 for PowerShell
        ps_launcher = bin_dir / f"{cli_name}.ps1"
        ps_content = f'& "{fleting_exe}" @args'
        ps_launcher.write_text(ps_content, encoding='utf-8')
        
    else:
        # Unix-like: create shell script named "fleting"
        launcher_path = bin_dir / cli_name
        launcher_content = f"""#!/usr/bin/env bash
exec "{fleting_exe}" "$@"
"""
        launcher_path.write_text(launcher_content)
        
        try:
            launcher_path.chmod(launcher_path.stat().st_mode | 0o111)  # +x for all
        except:
            console.print(f"Could not make {launcher_path} executable", style="warning")
    
    return True

def _create_symlink(project_root: Path, cli_name: str = CLI_NAME):
    """Alternative: creates a direct symlink (Unix only)"""
    BASE = project_root
    bin_dir = BASE / "bin"
    
    bin_dir.mkdir(parents=True, exist_ok=True)
    
    fleting_exe = shutil.which(cli_name)
    if not fleting_exe:
        return False
    
    launcher_path = bin_dir / cli_name
    
    try:
        if sys.platform != "win32":
            # Unix: create symlink
            if launcher_path.exists():
                launcher_path.unlink()
            os.symlink(fleting_exe, launcher_path)
            return True
    except Exception as e:
        console.print(f"Error creating symlink: {e}", style="error")
    
    return False

def _bin(project_root: Path, cli_name: str = CLI_NAME):
    """Creates local binary/launcher - simplified version"""
    BASE = project_root
    bin_dir = BASE / "bin"
    
    bin_dir.mkdir(parents=True, exist_ok=True)
    
    if sys.platform != "win32":
        if _create_symlink(project_root, cli_name):
            console.print("Project created with local Fleting (symlink)", style="info")
            return
    
    if _create_launcher(project_root, cli_name):
        console.print("Project created with local Fleting (symlink)", style="info")
    # else:
    #     console.print("[warning]Project created without local Fleting access[/warning]")
    #     console.print("[info]Install Fleting globally or use full path[/info]")

def handle_init(args=None):
    args = args or []
    cwd = Path.cwd()

    if not args:
        project_root = cwd / DEFAULT_PROJECT_NAME
        project_name = DEFAULT_APP_NAME
        project_root.mkdir(parents=True, exist_ok=True)

    elif args[0] == ".":
        project_root = cwd
        project_name = DEFAULT_APP_NAME

    else:
        project_root = cwd / args[0]
        project_name = args[0].replace("_", " ").title()
        project_root.mkdir(parents=True, exist_ok=True)

    try:
        init_project(project_root, project_name)
        
        # Always use "fleting" as the CLI name for consistency
        _bin(project_root, CLI_NAME)
        
        console.print("✅ Project Fleting successfully initiated!", style="success")
        
         # Give instructions if Fleting wasn't found
        if not shutil.which("fleting"):
            console.print("\nNote: Fleting was not found in global PATH", style="info")
            console.print("To use the 'fleting' command locally, you need to:", style="info")
            console.print("  1. Install Fleting globally: pip install fleting", style="info")
            console.print("  2. Or use the full path to the executable", style="info")
        
        # Show usage instructions
        console.print("\nUsage:", style="info")
        console.print(f"  cd {project_root.name}")
        console.print("  bin\\fleting <command> # Access database shell (Windows)", style="suggestion")
        console.print("  bin/fleting <command>  # Access database shell (Unix)", style="suggestion")
            
    except Exception as e:
        console.print(f"Error creating project: {e}", style="error")
        raise
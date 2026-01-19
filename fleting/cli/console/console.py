# cli/console/console.py
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich import box
from rich.rule import Rule
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.tree import Tree
from fleting.cli.console.themes import THEMES

console = Console(theme=THEMES)

def create_table(title: str = "", columns: list = None, min_width: int = 30) -> Table:
    """Create a table with Fleting stile"""
    table = Table(
        show_header=True,
        header_style="bold cyan",
        box=box.ROUNDED,
        border_style="blue",
        padding=(0, 1),
        min_width=min_width,
        expand=True
    )
    
    if title:
        table.title = f"[bold yellow]{title}[/bold yellow]"
    
    if columns:
        for col in columns:
            if isinstance(col, tuple):
                table.add_column(col[0], style=col[1], width=col[2] if len(col) > 2 else None)
            else:
                table.add_column(col, style="cyan")
    
    return table

def print_simple_table(headers: list, rows: list, title: str = ""):
    """Print a simple table with styled rows"""
    table = create_table(title, headers)
    
    for row in rows:
        styled_row = []
        for cell in row:
            cell_str = str(cell)
            # Apply styles based on content
            if cell_str in ["✔", "✅", "✓"]:
                styled_cell = "[green]✔[/green]"
            elif cell_str in ["—", "✗", "❌"]:
                styled_cell = "[dim]—[/dim]"
            elif "bytes" in cell_str.lower():
                styled_cell = f"[dim]{cell_str}[/dim]"
            else:
                styled_cell = f"[cyan]{cell_str}[/cyan]"
            styled_row.append(styled_cell)
        
        table.add_row(*styled_row)
    
    console.print()
    console.print(table)
    console.print()
    
def print_pages_table(headers: list, rows: list):
    """print page tables with specific colors"""
    table = create_table("📄 Pages Overview", headers, min_width=50)
    
    for row in rows:
        styled_row = []
        for i, cell in enumerate(row):
            if i == 0:  # page name
                styled_cell = f"[bold cyan]{cell}[/bold cyan]"
            elif cell == "✔":
                styled_cell = "[green]✔[/green]"
            elif cell == "—":
                styled_cell = "[dim red]—[/dim red]"
            else:
                styled_cell = f"[yellow]{cell}[/yellow]"
            styled_row.append(styled_cell)
        
        table.add_row(*styled_row)
    
    console.print()
    console.print(table)
    console.print(f"[dim]Legend: [green]✔[/green] = Present | [dim red]—[/dim red] = Missing[/dim]")
    console.print()

def print_routes_table(headers: list, rows: list):
    """Print routes table with especial style"""
    table = create_table("🛣️ Routes", headers, min_width=40)
    
    for row in rows:
        styled_row = []
        styled_row.append(f"[bold green]{row[0]}[/bold green]")  # Route
        styled_row.append(f"[cyan]{row[1]}[/cyan]")  # View
        table.add_row(*styled_row)
    
    console.print()
    console.print(table)

__all__ = [
    'console',
    'Console',
    'Table',
    'Panel',
    'Columns',
    'Text',
    'box',
    'Rule',
    'Syntax',
    'Markdown',
    'Progress',
    'SpinnerColumn',
    'TextColumn',
    'Prompt',
    'Confirm',
    'Tree',
    'create_table',
    'print_simple_table',
    'print_pages_table',
    'print_routes_table',
]


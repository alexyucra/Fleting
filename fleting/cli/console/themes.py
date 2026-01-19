from rich.theme import Theme

THEMES = Theme({
    # Main states - matching current CLI emoji style
    "success": "green1 bold",
    "error": "red1 bold", 
    "warning": "yellow1 bold",
    "info": "cyan bold",
    
    # Soft variants
    "success.dim": "green3",
    "error.dim": "red3", 
    "warning.dim": "yellow3",
    "info.dim": "cyan3",
    
    # UX / hints
    "suggestion": "magenta italic",
    "hint": "bright_black italic",
    "muted": "bright_black",
    
    # Structure
    "title": "bold white underline",
    "subtitle": "bold white",
    "label": "bold blue",
    "value": "white",
    
    # Debug / dev stuff
    "debug": "dim cyan",
    "trace": "dim bright_black",
    
    # Fancy extras
    "highlight": "black on yellow",
    "important": "bold white on red",
    
    # CLI specific themes
    "command": "bold green",
    "description": "white",
    "header": "bold cyan",
    "table.border": "blue",
    "table.header": "bold blue"
})

from rich.console import Console
from rich.panel import Panel

console = Console()


def print_panel(title: str, message: str, color: str = "red"):
    panel = Panel(
        message,
        title=title,
        border_style=color,
    )
    console.print(panel)

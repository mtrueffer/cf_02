import asyncio
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text
from shutil import get_terminal_size

class Battlefield:
    def __init__(self, game):
        self.game = game
        self.console = Console()
        self.layout = self._create_layout()
        self.console_lines = []

    def _create_layout(self):
        layout = Layout(name="root")

        layout.split(
            Layout(name="upper", ratio=3),
            Layout(name="console", ratio=1)
        )

        layout["upper"].split_row(
            Layout(name="battlefield",ratio=3),
            Layout(name="info", ratio=1)
        )

        return layout

    def render_battlefield(self):
        width, height = self.game.xylim
        grid = [[" " for _ in range(width)] for _ in range(height)]

        # Buildings
        for b in self.game.objects["Buildings"]:
            bx, by = map(int, b.position)
            bw, bh = b.size
            for y in range(by, by+bh):
                for x in range(bx, bx+bw):
                    if 0 <= x < width and 0 <= y < height:
                        grid[y][x] = "█"

        # Units
        for u in self.game.objects["Units"]:
            x,y = map(int, u.position)
            if 0 <= x < width and 0 <= y < height:
                team_colour = "[red]" if u.team == 1 else "[blue]"
                grid[y][x] = f"{team_colour}U[/]"

        battlefield_str = "\n".join("".join(row) for row in grid)
        return Panel(battlefield_str, title="Battlefield",
            border_style="green")

    def render_info(self):
        table = Table(title="Game Info")
        table.add_column("Stat", justify="right",
            style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        table.add_row("Tick", str(self.game.tick))
        table.add_row("Total Units", str(len(self.game.objects["Units"])))
        table.add_row("Total Buildings", str(len(self.game.objects["Buildings"])))

        return Panel(table, border_style="yellow")

    def render_console_panel(self):
        terminal_height = get_terminal_size((80, 24)).lines
        console_height = int(terminal_height * 0.25) - 4

        console_text = "\n".join(self.console_lines[-console_height:])
        return Panel(console_text, title="Command Console", border_style="magenta")

    def update_layout(self):
        self.layout["battlefield"].update(self.render_battlefield())
        self.layout["info"].update(self.render_info())
        self.layout["console"].update(self.render_console_panel())
        return self.layout

    def add_console_message(self, text):
        self.console_lines.append(text)

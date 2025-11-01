from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Input, Header, Footer
from textual.reactive import reactive
from textual import events
import asyncio, time, wcwidth

class Battlefield(App):

    CSS_PATH = "battlefield.css"
    BINDINGS = [("q", "quit", "Quit")]

    tick = reactive(0)
    runtime = reactive(0.0)
    command_history = reactive(list, always_update=True)
    current_input = reactive("")
    objects = reactive(dict)

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.start_time = time.time()
        self.command_history = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            with Vertical(id='left'):
                yield Static("",id="stats")
            with Vertical(id='main'):
                yield Static("", id="battlefield")
                yield Static("", id="console")
                yield Input(placeholder="Type command...", id="input")
        yield Footer()

    async def on_mount(self):
        self.set_interval(self.game.tick_time, self.update_game)

    def update_game(self):
        self.game.update()
        self.tick += 1
        self.runtime = time.time() - self.start_time
        self.refresh_ui()

    def _battlefield(self):
        width,height = self.game.xylim
        grid = [[" " for _ in range(width)] for _ in range(height)]

        for x in range(width):
            grid[0][x] = "\u2501"
            grid[height - 1][x] = "\u2501"

        for y in range(height):
            grid[y][0] = "\u2503"
            grid[y][width - 1] = "\u2503"

        grid[0][0] = "\u250F"
        grid[0][width - 1] = "\u2513"
        grid[height - 1][0] = "\u2517"
        grid[height - 1][width - 1] = "\u251B"

        for unit in self.game.objects.get("Units", []):
            x,y = map(int, unit.position)
            x = max(0, min(width - 1, x))
            y = max(0, min(height - 1, y))
            symbol = self.decode_unicode(unit.symbol) if hasattr(unit, "symbol") else "?"
            grid[y][x] = symbol

        for building in self.game.objects.get("Buildings", []):
            x,y = map(int, building.position)
            symbol = self.decode_unicode(building.symbol) if hasattr(building, "symbol") else "#"
            grid[y][x] = symbol

        return "\n".join("".join(self.fix_width(cell) for cell in row) for row in grid)

    def refresh_ui(self):
        if not self.is_running:
            return

        battlefield = self._battlefield()

        self.query_one("#battlefield", Static).update(battlefield)

        stats = (
            f"[bold green]Tick:[/bold green] {self.tick}\n"
            f"[bold green]Runtime:[/bold green] {self.runtime:,.1f}s\n"
            f"[bold green]Units:[/bold green] {len(self.game.objects.get('Units', []))}\n"
            f"[bold green]Buildings:[/bold green] {len(self.game.objects.get('Buildings', []))}\n"
        )
        self.query_one("#stats", Static).update(stats)

        console_text = "\n".join(self.command_history[-6:]) or "[dim]No commands...[/dim]"
        self.query_one("#console", Static).update(console_text)

    async def on_input_submitted(self, event: Input.Submitted):
        cmd = event.value.strip()
        event.input.value = ""
        if not cmd:
            return
        if cmd.lower() in {"quit", "exit"}:
            await self.action_quit()
            return
        self.command_history.append(f"> {cmd}")
        await self.game.command_handler.handle(cmd)
        self.refresh_ui()

    async def on_key(self, event: events.Key):
        if event.key == "escape":
            await self.action_quit()

    def log_command(self, msg: str):
        print(f"[LOG] {msg}")
        self.command_history.append(msg)
        self.call_after_refresh(self.refresh_ui)

    def decode_unicode(self, s: str) -> str:
        try:
            return s.encode("utf-8").decode("unicode_escape")
        except Exception:
            return s

    def fix_width(self,ch, width=2):
        w = wcwidth.wcwidth(ch)
        if w < width:
            return ch + " " * (width - w)
        elif w > width:
            return ch[:width]
        return ch

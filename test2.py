import asyncio
from prompt_toolkit import PromptSession
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live

console = Console()

class DemoGame:
    def __init__(self):
        self.tick = 0
        self.running = True
        self.layout = self._make_layout()
        self.console_lines = []

    def _make_layout(self):
        layout = Layout()
        layout.split(
            Layout(name="upper", ratio=3),
            Layout(name="console", ratio=1)
        )
        return layout

    def render(self):
        battlefield = Panel(f"TICK: {self.tick}", title="Battlefield", border_style="green")
        log_panel = Panel("\n".join(self.console_lines[-8:]), title="Console", border_style="magenta")
        self.layout["upper"].update(battlefield)
        self.layout["console"].update(log_panel)

    async def run(self):
        session = PromptSession("> ")

        async def input_loop():
            while self.running:
                try:
                    cmd = await session.prompt_async()
                except (EOFError, KeyboardInterrupt):
                    self.running = False
                    break
                if not cmd:
                    continue
                if cmd.lower() in {"quit", "exit"}:
                    self.running = False
                    break
                self.console_lines.append(f"You typed: {cmd}")

        async def game_loop():
            while self.running:
                self.tick += 1
                self.render()
                await asyncio.sleep(0.5)

        with Live(self.layout, refresh_per_second=5, console=console, screen=False):
            await asyncio.gather(game_loop(), input_loop())


if __name__ == "__main__":
    asyncio.run(DemoGame().run())

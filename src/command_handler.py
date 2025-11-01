class CommandHandler:
    def __init__(self, game):
        self.game = game

    async def handle(self, cmd: str):
        parts = cmd.split()
        if not parts:
            return
        action = parts[0].lower()

        if action == "some" and len(parts) > 1:
            self.game.battlefield.log_command(f"Doing something")
        else:
            self.game.battlefield.log_command(f"[red]Unknown command:[/red] {cmd}")


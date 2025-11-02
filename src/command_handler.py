class CommandHandler:
    def __init__(self, game):
        self.game = game

    async def handle(self, cmd: str):
        parts = cmd.split()
        if not parts:
            return
        action = parts[0].lower()

        if action == "build":
            await self.handle_build(parts)
        else:
            self.game.battlefield.log_command(f"[red]Unknown command:[/red] {cmd}")

    async def handle_build(self, parts):
        if len(parts) != 4:
            self.game.battlefield.log_command("[red]Usage: build <building_name> <team> <x,y>[/red]")
            return

        _, name, team_str, pos_str = parts

        try:
            team = int(team_str)
        except ValueError:
            self.game.battlefield.log_command(f"[red]Invalid team number:[/red] {team_str}")
            return

        if team not in range(1, self.game.teams):
            self.game.battlefield.log_command(f"[red]Team {team} does not exist.[/red]")
            return

        try:
            x_str, y_str = pos_str.split(",")
            x,y = int(x_str), int(y_str)
        except ValueError:
            self.game.battlefield.log_command(f"[red]Invalid position format:[/red] {pos_str}")
            return

        width, height = self.game.xylim
        if not (1 < x < width - 2 and 1 < y < height -2):
            self.game.battlefield.log_command(f"[red]Position out of bounds:[/red] ({x},{y})")
            return

        valid_buildings = list(self.game.building_stats[self.game.team_factions[team-1]].keys())

        if name not in valid_buildings:
            self.game.battlefield.log_command(f"{valid_buildings}")
            #self.game.battlefield.log_command(f"[red]{name}[/red] is not a valid building for [yellow]{self.game.team_factions[team-1]}[/yellow].")
            return

        self.game.objects = self.game.building_spawner.spawn(
            self.game.objects,
            team=team-1,
            name=name,
            x=x,
            y=y)


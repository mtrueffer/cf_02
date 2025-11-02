import asyncio
from src.battlefield import Battlefield

class IOManager:
    def __init__(self, game):
        self.game = game
        self.output = None

    async def run(self):
        app = Battlefield(self.game)
        self.game.battlefield = app
        self.game.building_spawner.startup(self.game.objects)
        await app.run_async()

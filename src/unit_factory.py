from .unit import Unit
from .utils import load_unit_stats

class UnitFactory:
    def __init__(self, game, team):
        self.game = game
        self.team = team

        self.unit_stats = game.unit_stats

    def create(self, faction, name, position):
        return Unit(
            game=self.game,
            team=self.team,
            faction=faction,
            unit_stats=self.game.unit_stats[faction],
            name=name,
            position=position)

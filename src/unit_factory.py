from .unit import Unit
from .utils import load_unit_stats

class UnitFactory:
    def __init__(self, game, team):
        self.game = game
        self.team = team

        self.unit_stats = game.unit_stats

    def create(self, faction, name):
        return Unit(self.game, self.team,
            self.game.unit_stats[faction], name)

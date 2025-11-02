from .game_object import Unit, Building, Castle
from .utils import load_unit_stats, load_building_stats
from .registry import get_class

class Factory:
    def __init__(self, game, team):
        self.game = game
        self.team = team
        self.stats = None

    def create(self, faction, name, position, type):
        class_name = get_class(type)
        return class_name(
            game=self.game,
            team=self.team,
            faction=faction,
            stats=self.stats[faction],
            name=name,
            position=position
        )

class BuildingFactory(Factory):
    def __init__(self, game, team):
        super().__init__(game, team)
        self.stats = game.building_stats

class UnitFactory(Factory):
    def __init__(self, game, team):
        super().__init__(game, team)
        self.stats = game.unit_stats

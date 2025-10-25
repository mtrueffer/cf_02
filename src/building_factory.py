from .building import Building

class BuildingFactory:
    def __init__(self, game, team):
        self.game = game
        self.team = team

        self.building_stats = game.building_stats

    def create(self, faction, name, position):
        return Building(
            game=self.game,
            team=self.team,
            faction=faction,
            building_stats=self.game.building_stats[faction],
            name=name,
            position=position)

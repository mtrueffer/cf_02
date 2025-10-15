from .building import Building

class BuildingFactory:
    def __init__(self, game, team):
        self.game = game
        self.team = team

        self.building_stats = game.building_stats

    def create(self, faction, name):
        return Building(self.game, self.team,
            self.game.building_stats[faction], name)

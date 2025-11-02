from .factory import BuildingFactory, UnitFactory
from .game_object import Castle

class FactionFactory():
    def __init__(self, game, team, name):
        self.game = game
        self.team = team
        self.name = name

    def create(self, object_type, position):
        factory_type = self.game.factories[object_type]
        factory = factory_type(self.game, self.team)
        return factory.create("Standard", self.name, position, "Castle")

class HumanFactory(FactionFactory):
    def __init__(self, game, team, name):
        super().__init__(game, team, name)

    def create(self, object_type, position):
        factory_type = self.game.factories[object_type]
        factory = factory_type(self.game, self.team)
        return factory.create("Human", self.name, position, object_type)




from .unit_factory import UnitFactory

class FactionFactory():
    def __init__(self, game, team, name):
        self.game = game
        self.team = team
        self.name = name

    def create(self, object_type):
        pass

class HumanFactory(FactionFactory):
    def __init__(self, game, team, name):
        super().__init__(game, team, name)

    def create(self, object_type):
        return self.game.factories[object_type].create("Human")




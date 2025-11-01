
import time

class Spawner:
    def __init__(self, game):
        self.game = game
        self.t0 = time.time()

    def update(self, objects):
	    pass

    def add(self, faction_factory="Human", team=None,
            object_type="Unit", name=None, position=(1,1)):
        factory_class = self.game.faction_factories[faction_factory]
        factory = factory_class(self.game, team, name)
        return factory.create(object_type, position)

class BuildingSpawner(Spawner):
    def __init__(self, game):
        super().__init__(game)

    def update(self, objects):
        objects_upd = objects
        if self.game.tick == 10:
            for team in range(self.game.teams):
                if team == 0:
                    xy = (1,8)
                else:
                    xy = (self.game.xylim[0]-1,2)
                objects_upd["Buildings"].append(self.add(
                    faction_factory=self.game.team_factions[team],
                    team=team,
                    object_type="Building",
                    name="Farm",
                    position=xy))
        return objects_upd

    def startup(self, objects):
        objects_upd = objects
        for team in range(self.game.teams):
            if team == 0:
                xy = (2,5)
            else:
                xy = (self.game.xylim[0]-2,5)
            objects_upd["Buildings"].append(self.add(
                faction_factory="Standard",
                team=team,
                object_type="Building",
                name="Castle",
                position = xy))
        return objects_upd

class UnitSpawner(Spawner):
    def __init__(self, game, spawner, spawn_position, spawn_interval=4):
        super().__init__(game)
        self.spawner = spawner
        self.spawn_position = spawn_position
        self.spawn_interval = spawn_interval

    def update(self, objects):
        objects_upd = objects

        if time.time() - self.t0 >= self.spawn_interval:
            objects_upd["Units"].append(self.add(
                faction_factory=self.spawner.faction,
                team=self.spawner.team,
                object_type="Unit",
                name=self.spawner.unit_name,
                position=self.spawn_position))
            self.t0 = time.time()
        return objects_upd

        



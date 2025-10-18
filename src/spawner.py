import time

class Spawner:
    def __init__(self, game):
        self.game = game
        self.t0 = time.time() 

    def update(self, objects):
	    pass

    def add(self, faction_factory="Human", team=None,
            object_type="Unit", name=None):
        factory_class = self.game.faction_factories[faction_factory]
        factory = factory_class(self.game, team, name)
        return factory.create(object_type)

class BuildingSpawner(Spawner):
    def __init__(self, game):
        super().__init__(game)

    def update(self, objects):
        pass

    def startup(self, objects):
        objects_upd = objects
        for team in self.teams:
            objects_upd["Buildings"].append(self.add("Standard",
                team, "Building", "Castle"))
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
            objects_upd["Units"].append(self.add("Human",
                team=1, object_type="Unit", name="Footman"))
            objects_upd["Units"].append(self.add("Human",
                team=2, object_type="Unit", name="Knight"))
            self.t0 = time.time()
        return objects_upd

        



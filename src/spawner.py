import time

class Spawner:
    def __init__(self, game):
        self.game = game
        self.t0 = time.time() 

    def update(self, objects, tick):
        objects_upd = objects

        # Add logic for when the spawner should trigger
        if time.time() - self.t0 >= 4: 
            objects_upd["Units"].append(self.add(self.game.faction_factories["Human"],
                team=1, object_type="Unit"))
            objects_upd["Units"].append(self.add(self.game.faction_factories["Human"],
                team=2, object_type="Unit"))
            self.t0 = time.time()
        return objects_upd

    def add(self, faction_factory="Human", team=None, object_type="Unit"):
        return faction_factory.create(object_type)

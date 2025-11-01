import time, math, random

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

        castle_positions = self.generate_edge_far_positions(
            *self.game.xylim, n_castles=self.game.teams)

        for team in range(self.game.teams):
            objects_upd["Buildings"].append(
                self.add(
                    faction_factory="Standard",
                    team=team,
                    object_type="Building",
                    name="Castle",
                    position=castle_positions[team]
                )
            )

        return objects_upd

    def distance(self, a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def generate_edge_far_positions(self, width, height, n_castles, edge_band=3):
        candidates = []
        for x in range(width):
            for y in range(height):
                if (x < edge_band or x >= width - edge_band or 
                        y < edge_band or y >= height - edge_band):
                    candidates.append((x, y))

        if not candidates:
            raise ValueError("Edge band too thick for battlefield size")

        positions = [random.choice(candidates)]

        for _ in range(1, n_castles):
            best_spot, best_min_dist= None, -1
            for c in candidates:
                min_d = min(self.distance(c, p) for p in positions)
                if min_d > best_min_dist:
                    best_min_dist = min_d
                    best_spot = c
            positions.append(best_spot)
            candidates.remove(best_spot)

        return positions

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


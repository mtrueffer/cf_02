from .utils import distance
from .spawner import UnitSpawner

class Building:
    def __init__(self, game, team, faction, building_stats, name, position):
        self.game = game
        self.team = team
        self.faction = faction
        self.name = name
        self.building_stats = building_stats[name]
        self.type = self.building_stats["type"]
        self.id = len(game.objects["Buildings"]) + 1

        self.position = position
        self.cell_index = None

        self.unit_spawner = None
        if self.type == "spawner":
            self.unit_spawner = UnitSpawner(self.game, self, self.position,
                self.building_stats["spawn_rate"])


        self.health = self.building_stats["health"]
        self.vision = 5

        self.target = None

        self.game.logger.log(
            message=f"{self.name} {self.id} of the {self.team} team was built in at position ({self.position})!"
        )

    def update(self):
        if self.type == "spawner":
            self.unit_spawner.update()

    def can_see(self, other):
        dist = distance(self.position, other.position)
        if dist > self.vision:
            return False
        return True

    def is_alive(self):
        return self.health > 0

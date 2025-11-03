from .utils import distance
from .spawner import UnitSpawner
from .utils import norm_dist, distance, dot_prod, have_same_sign
from .registry import register_class
import math, colorsys

@register_class
class GameObject:
    def __init__(self, game, team, faction, stats, name, position):
        self.game = game
        self.team = team
        self.faction = faction
        self.stats = stats[name]
        self.name = name
        self.position = position

        self.cell_index = None

        self.symbol = self.stats["symbol"]
        self.health = self.stats["health"]
        self.is_dead = False
        self.vision = 5

        self.target = None
        self.attackedby = []

    @property
    def color(self):
        hue = (self.team % self.game.teams) / self.game.teams
        r, g, b = colorsys.hsv_to_rgb(hue, 0.85, 1.0)
        return f"rgb({int(r*255)},{int(g*255)},{int(b*255)})"

    def colored_symbol(self):
        return f"[{self.color}]{self.symbol}[/{self.color}]"

    def is_alive(self):
        return self.health > 0

    def can_see(self, object):
        pass

    def update(self):
        pass

    def find_target(self, object_type):
        visible_objects = [
            o for o in self.game.objects[object_type]
            if o.team != self.team and self.can_see(o)]
        if not visible_objects:
            return None
        visible_objects.sort(key=lambda o: distance(self.position, o.position))
        return visible_objects[0]

@register_class
class Building(GameObject):
    def __init__(self, game, team, faction, stats, name, position):
        super().__init__(game, team, faction, stats, name, position)

        self.type = self.stats["type"]
        self.id = len(game.objects["Buildings"]) + 1

        self.level = 1
        self.unit_spawner = None
        self.unit_name = self.stats["unit"][self.level-1]
        if self.type == "spawner":
            self.unit_spawner = UnitSpawner(self.game, self, self.position,
                self.stats["spawn_rate"])

        self.size = (1,1)

    def update(self):
        if self.type == "spawner":
           self.game.objects = self.unit_spawner.update(self.game.objects)

    def can_see(self, other):
        dist = distance(self.position, other.position)
        if dist > self.vision:
            return False
        return True

    def upgrade(self):
        if self.levels < self.stats["levels"]:
            self.level += 1
            self.unit_name = self.stats["unit"][self.level]

@register_class
class Castle(Building):
    def __init__(self, game, team, faction, stats, name, position):
        super().__init__(game, team, faction, stats, name, position)

@register_class
class Unit(GameObject):
    def __init__(self, game, team, faction, stats, name, position):
        super().__init__(game, team, faction, stats, name, position)

        self.id = len(game.objects["Units"]) + 1

        self.direction = self.point_at()
        self.speed_vect = self.velocity()

    def update(self):
        if not self.target:
            self.target = self.find_target("Units")
            if not self.target:
                self.target = self.find_target("Buildings")
        if self.target:
            self.direction = self.point_at(*self.target.position)
            self.speed_vect = self.velocity()
            if distance(self.position, self.target.position) <= self.stats["range"]:
                self.attack()
            else:
                self.position = self.move()
        else:
            self.direction = self.point_at()
            self.speed_vect = self.velocity()
            self.position = self.move()

    def attack(self):
        damage = self.stats.get("damage", 1)
        self.target.health -= damage

        if self.target.health <= 0:
            self.target.health = 0
            self.target.is_dead = True

    def move(self):
        return self.position[0]+self.speed_vect[0], self.position[1]+self.speed_vect[1]

    def point_at(self, x=None, y=None):
        if x == None:
            if self.team == 0:
                x,y = self.game.objects["Buildings"][1].position
            else:
                x,y = self.game.objects["Buildings"][0].position
        return norm_dist(tuple(self.position),(x, y))

    def velocity(self):
        return [axis * self.stats["speed"] for axis in self.direction]

    def can_see(self, other):
        dist = distance(self.position, other.position)
        if dist > self.vision:
            return False
        dot = dot_prod(norm_dist(self.position, other.position), self.direction)
        return dot >= 0

from .utils import norm_dist, distance, dot_prod, have_same_sign

import math

class Unit:
    def __init__(self, game, team, unit_stats, name):
        self.game = game
        self.team = team
        self.name = name
        self.unit_stats = unit_stats[name]
        self.id = len(game.objects["Units"]) + 1

        self.position = [0 if self.team==1 else self.game.xylim[0],
            self.game.xylim[1] / 2]
        self.direction = self.point_at()
        self.velocity = self.velocity()

        self.cell_index = None

        self.health = self.unit_stats["health"]
        self.vision = 5

        self.target = None

        self.attackedby = None

        self.game.logger.log(
            message=f"{self.name} {self.id} of the {self.team} team spawned in at position ({self.position})!"
        )

    def move(self):
        if 0 < self.position + self.speed * self.direction < self.game.length:
            self.position += self.speed * self.direction
        else:
            self.direction *= -1

    def point_at(self, x=None, y=None):
        if x == None:
            x=self.game.xylim[0] if self.team==1 else 0
            y=self.game.xylim[1] / 2
        return norm_dist(tuple(self.position),(x, y))

    def velocity(self):
        return [axis * self.unit_stats["speed"] for axis in self.direction]

    def can_see(self, other):
        dist = distance(self.position, other.position)
        if dist > self.vision:
            return False
        dot = dot_prod(norm_dist(self.position, other.position), self.direction)
        return dot >= 0

    def is_alive(self):
        return self.health > 0

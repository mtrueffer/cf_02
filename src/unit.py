from .utils import norm_dist, distance, dot_prod, have_same_sign

import math

class Unit:
    def __init__(self, game, team, unit_stats, name):
        self.game = game
        self.team = team
        self.name = name
        self.unit_stats = unit_stats[name]
        self.id = len(game.objects["Units"]) + 1

        self.position = [self.game.xylim[0] * team==2,
            self.game.xylim[1] / 2]
        self.direction = self.point_at()
        self.velocity = self.velocity()

        self.cell_index = None

        self.vision = 5

        self.target = None

        self.attackedby = None

        self.game.logger.log(
            self.team,
            f"{self.name} {self.id} of the {self.team} team spawned in!",
            self.game.tick
        )

    def move(self):
        if 0 < self.position + self.speed * self.direction < self.game.length:
            self.position += self.speed * self.direction
            self.game.logger.log(
                self.faction,
                f"{self.name} moves to {self.position} in bin {self.bin_index}",
                self.game.tick
            )
        else:
            self.direction *= -1
            self.game.logger.log(
                self.faction,
                f"{self.name} turns around!",
                self.game.tick
            )

    def point_at(self, x=None, y=None):
        if x == None:
            x=self.game.xylim[0]*(self.team==1)
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

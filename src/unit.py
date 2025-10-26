from .utils import norm_dist, distance, dot_prod, have_same_sign

import math

class Unit:
    def __init__(self, game, team, faction, unit_stats, name, position):
        self.game = game
        self.team = team
        self.name = name
        self.unit_stats = unit_stats[name]
        self.id = len(game.objects["Units"]) + 1

        self.position = position
        self.direction = self.point_at()
        self.speed_vect = self.velocity()

        self.cell_index = None

        self.health = self.unit_stats["health"]
        self.vision = 5

        self.target = None

        self.attackedby = None

        self.game.logger.log(
            message=f"{self.name} {self.id} of the {self.team} team spawned in at position ({self.position})!"
        )

    def update(self):
        #If moving:
        self.direction = self.point_at()
        self.speed_vect = self.velocity()
        self.position = self.move()
        
        self.game.logger.log(
            message=f"{self.name} {self.id} on the {self.team} team moved to {tuple(round(axis,2) for axis in self.position)}",
            )

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
        return [axis * self.unit_stats["speed"] for axis in self.direction]

    def can_see(self, other):
        dist = distance(self.position, other.position)
        if dist > self.vision:
            return False
        dot = dot_prod(norm_dist(self.position, other.position), self.direction)
        return dot >= 0

    def is_alive(self):
        return self.health > 0

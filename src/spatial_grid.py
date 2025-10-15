from .utils import have_same_sign, distance
class SpatialGrid:
    def __init__(self, cell_size=3, logger=None, tick=0):
        self.cell_size = cell_size
        self.logger = logger
        self.tick = tick

        self.cells = {}

    def get_cell_index(self, position):
        x, y = position
        return int(x // self.cell_size), int(y // self.cell_size)

    def add(self, unit):
        idxy = self.get_cell_index(unit.position)
        if idxy not in self.grid:
            self.grid[idxy] = []
        self.grid[idxy].append(unit)
        unit.cell_index = idxy

    def remove(self, unit):
        self.bins[unit.cell_index].remove(unit)

    def move(self, unit):
        new_idxy = self.get_cell_index(unit.position)
        if new_idxy != unit.cell_index:
            self.remove(unit)
            self.add(unit)

    def nearby(self, unit):
        cx, cy = self.get_cell_index(unit.position)
        nearby = []

        cell_radius = int(unit.vision // self.cell_size)

        for dx in range(-cell_radius, cell_radius+1):
            for dy in range(-cell_radius, cell_radius+1):
                cell = (cx+dy, cy+dy)
                if cell in self.cells:
                    for other in self.cells[cell]:
                        dist = distance(tuple(unit.position),tuple(other.position))
                        if dist <= radius:
                            nearby.append(other)
        return nearby

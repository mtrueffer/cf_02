import time

# Includes
from .utils import load_unit_stats
from .spawner import Spawner
from .logger import Logger
from .spatial_grid import SpatialGrid
from .faction_factory import FactionFactory, HumanFactory
from .unit_factory import UnitFactory

class Game:
    def __init__(self, xylim=(20,10), ticks=20, tick_time=1,
            console_level="info", stats_file="src/unit_stats.csv"):

        # Game Parameters
        self.xylim = xylim
        self.tick_time = tick_time
        self.ticks = ticks
        self.tick = 0
        self.stats_file = stats_file

        # Data Files
        self.unit_stats = load_unit_stats(stats_file)

        # Systems
        self.logger = Logger(console_level=console_level)
        self.grid = SpatialGrid(self, self.tick)

        # Factories
        self.factories = {
            "Unit": UnitFactory(self, team=None)
        }
        self.faction_factories = {
            "Human": HumanFactory(self.factories, team=None, name=None)
        }
        
        # Spawners
        self.spawner = Spawner(self)

        # Objects
        self.objects = {
            "Units": [],
            "Buildings": [],
            "Projectiles": []
        }

    #----------
    # Main Game Loop
    #---------
    def run(self):
        for _ in range(self.ticks):
            self.update()
            time.sleep(self.tick_time)

    #---------
    # Game Updates
    #---------
    def update(self):
        self.tick += 1

        # Update Objects
        self.objects = self.spawner.update(self.objects, self.tick)

        for unit in self.objects["Units"]:
            if unit.is_alive():
                nearby_objects = {"Units": [], "Buildings": []}
                nearby_objects = self.grid.nearby(unit,
                        vision_range=unit.vision_range)
                # Unit Decision Tree
                # 1. Has target unit and still targetable?
                    # if in attack range, attack
                    # else if can move to attack range
                        #, move to target if able
                    # else drop target
                # 2. Is being attacked?
                    # is attacker targetable? add to unit.target
                # 3. Nearby units
                    # if targetable, target
                # 4. Has target building and still targetable?
                    # if in attack range, attack
                    # else if can move to attack range
                        # Move to attack range
                    # else drop target
                # 5. Nearby buildings
                    # if targetable, target
                # 6. If not on center of lane
                    # Move to center of lane
                # 7. Move down lane towards enemy side

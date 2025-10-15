import time

# Includes
from .utils import load_unit_stats
from .spawner import Spawner
from .logger import Logger
from .spatial_grid import SpatialGrid
from .faction_factory import FactionFactory, HumanFactory
from .unit_factory import UnitFactory

class Game:
    def __init__(self, xylim=(20,10), ticks=20, tick_time=1, teams=2
            console_level="info", unit_stats_file="src/unit_stats.csv"
            building_stats_file="src/building_stats.csv"):

        # Game Parameters
        self.xylim = xylim
        self.tick_time = tick_time
        self.ticks = ticks
        self.tick = 0
        self.teams = 2
        self.unit_stats_file = unit_stats_file
        self.building_stats_file = building_stats_file

        # Data Files
        self.unit_stats = load_unit_stats(self.unit_stats_file)
        self.building_stats = load_building_stats(self.building_stats_file)

        # Systems
        self.logger = Logger(console_level=console_level)
        self.grid = SpatialGrid(tick=self.tick)

        # Factories
        self.factories = {
            "Unit": UnitFactory
            "Building": BuildingFactory
        }
        self.faction_factories = {
            "Standard": FactionFactory
            "Human": HumanFactory
        }

        # Objects
        self.objects = {
            "Units": [],
            "Buildings": [],
            "Projectiles": []
        }

        # Spawners
        self.building_spawner = BuildingSpawner(self)
        self.building_spawner.startup(self.objects)

    def __str__(self):
        total_units = len(self.objects["Units"])
        total_buildings = len(self.objects["Buildings"])
        total_projectiles = len(self.objects["Projectiles"])

        team_counts = {}
        for unit in self.objects["Units"]:
            team_counts[unit.team] = team_counts.get(unit.team, 0) + 1
        team_summary = ", ".join(
            f"Team {team}: {count}" for team, count in team_counts.items()
        ) if team_counts else "No active units"

        return (
            f"[Tick {self.tick}/{self.ticks}] "
            f"Units: {total_units}, Buildings: {total_buildings}, Projectiles: {total_projectiles} | "
            f"{team_summary}"
        )

    #----------
    # Main Game Loop
    #---------
    def run(self):
        for _ in range(self.ticks):
            self.logger.log(message=self)
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
                nearby_objects = self.grid.nearby(unit)
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

import time

# Includes
from .utils import load_unit_stats, load_building_stats
from .spawner import Spawner, UnitSpawner, BuildingSpawner
from .logger import Logger
from .spatial_grid import SpatialGrid
from .faction_factory import FactionFactory, HumanFactory
from .unit_factory import UnitFactory
from .building_factory import BuildingFactory
from .battlefield import Battlefield
from .command_handler import CommandHandler
from .io_manager import IOManager
import asyncio

class Game:
    def __init__(self, xylim=(30,20), ticks=100, tick_time=1, teams=2,
            console_level="system", unit_stats_file="src/unit_stats.csv",
            building_stats_file="src/building_stats.csv"):

        # Game Parameters
        self.xylim = xylim
        self.tick_time = tick_time
        self.ticks = ticks
        self.tick = 0
        self.teams = teams
        self.unit_stats_file = unit_stats_file
        self.building_stats_file = building_stats_file
        self.battlefield = None
        self.command_handler = CommandHandler(self)
        self.io = IOManager(self)
        self.running = True
        self.paused = False

        # Data Files
        self.unit_stats = load_unit_stats(self.unit_stats_file)
        self.building_stats = load_building_stats(self.building_stats_file)

        # Systems
        self.logger = Logger(console_level=console_level)
        self.grid = SpatialGrid(tick=self.tick)

        # Factories
        self.factories = {
            "Unit": UnitFactory,
            "Building": BuildingFactory
        }
        self.faction_factories = {
            "Standard": FactionFactory,
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

        # Team Assignments
        self.team_factions = []
        for team in range(self.teams):
            self.team_factions.append("Human")

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
    async def run(self):
        await self.io.run()

    #---------
    # Game Updates
    #---------
    def update(self):
        self.tick += 1

        # Update Objects
        self.objects = self.building_spawner.update(self.objects)

        for building in self.objects["Buildings"]:
            building.update()

        for unit in self.objects["Units"]:
            if unit.is_alive():
                nearby_objects = {"Units": [], "Buildings": []}
                nearby_objects = self.grid.nearby(unit)
                unit.update()
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


from colorama import Fore, Style, init
from datetime import datetime
import os

init(autoreset=True)

class Logger:
    LEVELS = ["debug", "info", "combat", "system"]

    def __init__(self, enable_timestamp=True, enable_color=True,
            log_dir="logs", console_level="info"):
        self.enable_timestamp = enable_timestamp
        self.enable_color = enable_color
        self.console_level = console_level.lower()
        self.log_dir = log_dir

        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(
            self.log_dir,
            f"battle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )

        self.faction_colors = {
            "red": Fore.RED,
            "blue": Fore.CYAN,
            "green": Fore.GREEN,
            "yellow": Fore.YELLOW,
            "neutral": Fore.MAGENTA,
            "none": Fore.WHITE,
        }

        self.level_colors = {
            "debug": Fore.WHITE,
            "info": Fore.GREEN,
            "combat": Fore.YELLOW,
            "system": Fore.MAGENTA,
        }

    def log(self, faction="none", message="", tick=None, level="info"):
        level = level.lower()
        if level not in self.LEVELS:
            level = "info"

        timestamp = ""
        if self.enable_timestamp:
            if tick is not None:
                timestamp = f"[T{tick:03d}] "
            else:
                timestamp = f"[{datetime.now().strftime('%H:%M:%S')}] "

        #Build text
        log_elem = []
        log_elem.append(f"{timestamp}")
        log_elem.append(f"[{level.upper():7}]")
        log_elem.append(f"{message}")

        #Out to file
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(" ".join(log_elem) + "\n")
        except Exception as e:
            print(f"Logger Error: Unable to write to file ({e})")

        #Out to console
        if self.LEVELS.index(level) >= self.LEVELS.index(self.console_level):
            faction_color = self.faction_colors.get(faction.lower(), Fore.WHITE) if self.enable_color else ""
            level_color = self.level_colors.get(level.lower(), Fore.WHITE) if self.enable_color else ""
            reset = Style.RESET_ALL if self.enable_color else ""
            print(f"{log_elem[0]} {level_color}{log_elem[1]} {faction_color}{log_elem[2]}{reset}")



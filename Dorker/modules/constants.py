import random
import os
from colorama import Fore, Style

COLORS = {
    "RED": Fore.RED,
    "GREEN": Fore.GREEN,
    "MAGENTA": Fore.MAGENTA,
    "CYAN": Fore.CYAN,
    "MIXED": Fore.RED + Fore.BLUE,
    "BLUE": Fore.BLUE,
    "YELLOW": Fore.YELLOW,
    "WHITE": Fore.WHITE,
    "RESET": Style.RESET_ALL,
}

BANNER = """
    ___           __          
   / _ \___  ____/ /_____ ____
  / // / _ \/ __/  '_/ -_) __/
 /____/\___/_/ /_/\_\\__/_/        by D.Sanjai Kumar && r648r
"""

RANDOM_COLOR = random.choice(list(COLORS.values()))
RESULTS_PER_PAGE = 10
TOTAL_RESULTS = 100
CONFIG_FILE_DEFAULT_PATH = ".dorkrc.yaml"
LOGGIN_DEFAULT_PATH=os.path.join("logs", "dorker.log")
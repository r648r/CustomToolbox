# modules/constants.py

import random
import os
from colorama import Fore, Style


#  ___   ____  ____   __    _     _    _____      _       __    _     _     ____ 
# | | \ | |_  | |_   / /\  | | | | |    | |      \ \  /  / /\  | |   | | | | |_  
# |_|_/ |_|__ |_|   /_/--\ \_\_/ |_|__  |_|       \_\/  /_/--\ |_|__ \_\_/ |_|__ 
# 
####################################
# Test and add support with arguments + config file
RESULTS_PER_PAGE = 10
TOTAL_RESULTS = 100
####################################
OUTPUT_DIRECTORY_DEFAULT_PATH = "output"
CONFIG_FILE_DEFAULT_PATH = ".dorkrc.yaml"
LOG_DEFAULT_PATH=os.path.join("logs", "dorker.log")
#   _____     __           
#  / ___/__  / /__  _______
# / /__/ _ \/ / _ \/ __(_-<
# \___/\___/_/\___/_/ /___/
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
RANDOM_COLOR = random.choice(list(COLORS.values()))
BANNER=r"""
    ___           __          
   / _ \___  ____/ /_____ ____
  / // / _ \/ __/  '_/ -_) __/
 /____/\___/_/ /_/\_\\__/_/        by D.Sanjai Kumar && r648r
"""
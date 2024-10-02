#!/usr/bin/python3
import argparse
import logging
import os

# Import directory 'modules'
from modules.constants import COLORS, RANDOM_COLOR, CONFIG_FILE_DEFAULT_PATH, LOGGIN_DEFAULT_PATH, BANNER
from modules.config_loader import load_config, get_config_values
from modules.utils import validate_arguments
from modules.dorking import handle_dorking
 
# Send much love to D.Sanjai Kumar : https://github.com/RevoltSecurities/GoogleDorker/blob/main/dorker/dorker.py

def main():
    # Parse args 
    parser = argparse.ArgumentParser(description=f"{COLORS['CYAN']}A Powerful Tool for Google Dorking{COLORS['RESET']}")
    parser.add_argument("-q", "--query", help=f"[{COLORS['GREEN']}ALERT{COLORS['RESET']}]: Google dorking query for your target. Example: `-q inurl:test | inurl:env | inurl:dev | inurl:staging`", type=str)
    parser.add_argument("-d", "--domain", help=f"[{COLORS['GREEN']}ALERT{COLORS['RESET']}]: Target name for Google dorking. Example: `-d example.com`", type=str)
    parser.add_argument("-o", "--output", help=f"[{COLORS['GREEN']}ALERT{COLORS['RESET']}]: File name to save the dorking results. Example: `-o results.txt`", type=str)
    args = parser.parse_args()
    validate_arguments(args)

    # Start search
    logging.info(f"{RANDOM_COLOR}{BANNER}{COLORS['RESET']}")
    config_data = load_config(CONFIG_FILE_DEFAULT_PATH)
    output_file = args.output if args.output else get_config_values(config_data, 'output_file', "dorker_results.txt")
    handle_dorking(config_data, args.domain, output_file, query=args.query)
    logging.info(f"[{RANDOM_COLOR} Finish {COLORS['RESET']}]")

if __name__ == "__main__":
    from modules.constants import COLORS
    logging.basicConfig(
        format=f"[{COLORS['BLUE']}%(levelname)s{COLORS['RESET']}] [{COLORS['MAGENTA']}%(asctime)s{COLORS['RESET']}] %(message)s",
        datefmt="%H:%M:%S",
        encoding='utf-8',
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f"{LOGGIN_DEFAULT_PATH}", mode='a')
        ]
    )
    
main()
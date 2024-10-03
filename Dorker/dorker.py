# dorker.py

import logging

# Import local
from modules.constants import (
    COLORS, RANDOM_COLOR, CONFIG_FILE_DEFAULT_PATH,
    LOG_DEFAULT_PATH, BANNER, OUTPUT_DIRECTORY_DEFAULT_PATH
)
from modules.config_loader import load_config, get_config_values
from modules.dorking import handle_dorking
from modules.arguments import parse_arguments

def main():
    args = parse_arguments()
    # -c défini > default vars in constants.py
    if args.config:
        config_file = args.config
    else:
        config_file = CONFIG_FILE_DEFAULT_PATH
    config_data = load_config(config_file)

    # -o défini > config file value > default vars in constants.py
    if args.output:
        output_dir = args.output
    else:
        output_dir = get_config_values(config_data, 'output_directory', default=OUTPUT_DIRECTORY_DEFAULT_PATH)

    logging.info(f"{RANDOM_COLOR}{BANNER}{COLORS['RESET']}")
    handle_dorking(config_data, args.domain, output_dir, query=args.query)
    logging.info(f"[{RANDOM_COLOR} Finish {COLORS['RESET']}]")

if __name__ == "__main__":
    from modules.constants import COLORS
    logging.basicConfig(
        format=f"[{COLORS['BLUE']}%(levelname)s{COLORS['RESET']}] "
               f"[{COLORS['MAGENTA']}%(asctime)s{COLORS['RESET']}] %(message)s",
        datefmt="%H:%M:%S",
        encoding='utf-8',
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f"{LOG_DEFAULT_PATH}", mode='a')
        ]
    )

    main()

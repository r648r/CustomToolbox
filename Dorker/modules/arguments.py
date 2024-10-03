# modules/arguments.py

import argparse
from .constants import COLORS


def validate_arguments(args, parser):
    """Valide les arguments de la ligne de commande."""
    if not args.query and not args.domain:
        parser.error("At least one of --query or --domain must be specified.")

def parse_arguments():
    """Analyse les arguments de la ligne de commande et les retourne."""
    parser = argparse.ArgumentParser(
        description=f"{COLORS['CYAN']}A Powerful Tool for Google Dorking{COLORS['RESET']}"
    )
    parser.add_argument(
        "-q", "--query",
        help=f"[{COLORS['GREEN']}ALERT{COLORS['RESET']}]: Google dorking query for your target. Example: `dorker.py -q 'inurl:test | inurl:env' -d 'example.com'`",
        type=str
    )
    parser.add_argument(
        "-d", "--domain",
        help=f"[{COLORS['GREEN']}ALERT{COLORS['RESET']}]: Target domain for Google dorking. Example: `dorker.py -d 'example.com'`",
        type=str
    )
    parser.add_argument(
        "-o", "--output",
        help=f"[{COLORS['GREEN']}ALERT{COLORS['RESET']}]: Directory to save the dorking results. Example: `dorker.py -d 'example.com' -o ./results`",
        type=str
    )
    parser.add_argument(
        "-c", "--config",
        help=f"[{COLORS['GREEN']}ALERT{COLORS['RESET']}]: Path to the configuration file. Example: `dorker.py -c 'config.yaml'`",
        type=str
    )
    args = parser.parse_args()
    validate_arguments(args, parser)
    return args

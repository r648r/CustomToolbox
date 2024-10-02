#!/usr/bin/python3
import argparse
import yaml
import time
import random
import logging
from googleapiclient.discovery import build
import os
from colorama import Fore, Style

#        __           __                  ___ 
#   ____/ /___  _____/ /_____  ______   _|__ \
#  / __  / __ \/ ___/ //_/ _ \/ ___/ | / /_/ /
# / /_/ / /_/ / /  / ,< /  __/ /   | |/ / __/ 
# \__,_/\____/_/  /_/|_|\___/_/    |___/____/ 
#
# Fork by D.Sanjai Kumar https://github.com/RevoltSecurities/GoogleDorker/blob/main/dorker/dorker.py

###########################################
# Constants for colors and configurations #
###########################################
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
RESULTS_PER_PAGE = 10
TOTAL_RESULTS = 100

# Logging configuration
logging.basicConfig(
    format=f"[{COLORS['BLUE']}%(levelname)s{COLORS['RESET']}] [{COLORS['MAGENTA']}%(asctime)s{COLORS['RESET']}] %(message)s",
    datefmt="%H:%M:%S",
    encoding='utf-8',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("google_dorker.log", mode='a')
    ]
)

# ConfigLoader functions
def load_config(config_file="google_dorker.yaml"):
    """Load the configuration from the YAML file."""
    if not os.path.isfile(config_file):
        logging.error(f"Configuration file {config_file} not found.")
        exit()
    try:
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as yaml_err:
        logging.error(f"YAML Parsing Error - {yaml_err}")
        exit()

def get_config_values(config_data, key, default=None, error_message=None):
    """Retrieve a value from the configuration data."""
    value = config_data.get(key, default)
    if value is None and error_message:
        logging.error(error_message)
        exit()
    return value

# Google Dorker functions
def query_google(search_query, google_api_keys, google_cse_ids, results_per_page, total_results, output):
    """Query Google Custom Search Engine using the provided search_query. Fork by D.Sanjai Kumar"""
    try:
        # Randomly select API key and CSE ID
        google_api = random.choice(google_api_keys)
        google_cse_id = random.choice(google_cse_ids)

        service = build('customsearch', 'v1', developerKey=google_api)
        results = []

        start_index = 1
        while start_index < total_results:
            try:
                response = service.cse().list(
                    q=search_query,
                    cx=google_cse_id,
                    num=results_per_page,
                    start=start_index
                ).execute()

                for item in response.get('items', []):
                    title = item['title']
                    link = item['link']
                    results.append(f"[{search_query}] [{link}] [{title}]")

                start_index += results_per_page

            except Exception as e:
                logging.error(f"Failed to execute search query '{search_query}' - {e}")
                break

        # Display and save results
        if results:
            for url in results:
                logging.info(f"[{COLORS['GREEN']}FOUND{COLORS['RESET']}] {url}")
                write_result(output, url)
            logging.info(f"Total URLs found for '{search_query}': {len(results)}")
        else:
            logging.warning(f"{COLORS['RED']}No found{COLORS['RESET']} {search_query}")

    except Exception as e:
        logging.error(f"Unexpected error in query_google - {e}")

def write_result(output_file, url):
    """Write a result to the output file."""
    output_dir = os.path.dirname(output_file)

    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_file, "a") as file:
        file.write(f"dork - {url}\n")

def validate_arguments(args):
    """Validate script arguments."""
    if not args.query and not args.domain:
        logging.error("Either a query or domain must be provided.")
        exit()
    if args.output and not args.output.endswith(".txt"):
        logging.error("Output file must be a .txt file.")
        exit()

def charger_mots(wordlist_path):
    """Load words from a wordlist file and return a set of unique words."""
    if not os.path.isfile(wordlist_path):
        logging.warning(f"Wordlist file {wordlist_path} not found.")
        return set()

    try:
        with open(wordlist_path, 'r', encoding='utf-8') as wl_file:
            return set(ligne.strip() for ligne in wl_file if ligne.strip())
    except Exception as e:
        logging.error(f"Error reading wordlist file {wordlist_path} : {e}")
        return set()

def handle_dorking(config_data, domain, output_file, query=None):
    """Handle the dorking process with the given query or domain."""
    wordlists = get_config_values(config_data, 'wordlists', [], "No wordlists specified in configuration.")
    google_api_keys = get_config_values(config_data, 'Google-API', [], "No Google API keys specified in configuration.")
    google_cse_ids = get_config_values(config_data, 'Google-CSE-ID', [], "No Google CSE IDs specified in configuration.")

    # If a direct query is provided, use it
    if query:
        search_query = f"{query} site:{domain}" if domain else query
        query_google(search_query, google_api_keys, google_cse_ids, RESULTS_PER_PAGE, TOTAL_RESULTS, output_file)
    else:
        # Iterate over each wordlist
        for wordlist_path in wordlists:
            mots = charger_mots(wordlist_path)
            if not mots:
                continue  # Skip to next wordlist if none are loaded
            for mot in mots:
                search_query = f"{mot} site:{domain}" if domain else mot
                query_google(search_query, google_api_keys, google_cse_ids, RESULTS_PER_PAGE, TOTAL_RESULTS, output_file)

def main():
    parser = argparse.ArgumentParser(description=f"{COLORS['CYAN']}A Powerful Tool for Google Dorking{COLORS['RESET']}")
    parser.add_argument("-q", "--query", help=f"[{COLORS['GREEN']}ALERT{COLORS['RESET']}]: Google dorking query for your target. Exemple : `-q inurl:test | inurl:env | inurl:dev | inurl:staging`", type=str)
    parser.add_argument("-d", "--domain", help=f"[{COLORS['GREEN']}ALERT{COLORS['RESET']}]: Target name for Google dorking. Exemple : `-d exemple.com`", type=str)
    parser.add_argument("-o", "--output", help=f"[{COLORS['GREEN']}ALERT{COLORS['RESET']}]: File name to save the dorking results Exemple : `-o `", type=str)
    args = parser.parse_args()

    validate_arguments(args)

    logging.info(f"{RANDOM_COLOR}Starting Google Dorker...{COLORS['RESET']}")

    # Load configuration
    config_data = load_config()

    # Determine the output file
    output_file = args.output if args.output else get_config_values(config_data, 'output_file', "dorker_results.txt")

    # Handle the dorking process
    handle_dorking(config_data, args.domain, output_file, query=args.query)

if __name__ == "__main__":
    main()

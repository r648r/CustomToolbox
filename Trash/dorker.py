#!/usr/bin/python3
import httpx
import argparse
import yaml
import time
import random
import logging
from googleapiclient.discovery import build
import os
from colorama import Fore, Style

#    ___           __          
#   / _ \___  ____/ /_____ ____
#  / // / _ \/ __/  '_/ -_) __/
# /____/\___/_/ /_/\_\\__/_/   
# 
# Fork by D.Sanjai Kumar https://github.com/RevoltSecurities/GoogleDorker/blob/main/dorker/dorker.py

# Constants for colors and configurations

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

logging.basicConfig(
    format=f"[{COLORS['BLUE']}%(levelname)s{COLORS['RESET']}] [{COLORS['MAGENTA']}%(asctime)s{COLORS['RESET']}] %(message)s",
    datefmt="%H:%M:%S",  # Only show the hour, minute, and second
    level=logging.INFO,  # Adjust the log level here (e.g., DEBUG, INFO, WARNING)
    handlers=[
        logging.StreamHandler(),  # Output logs to console
        logging.FileHandler("google_dorker.log", mode='a')  # Save logs to a file
    ]
)

class ConfigLoader:
    def __init__(self, config_file="google_dorker.yaml"):
        self.config_file = config_file
        self.config_data = self.load_config()

    def load_config(self):
        """Load the configuration from the YAML file."""
        if not os.path.isfile(self.config_file):
            logging.error(f"Configuration file {self.config_file} not found.")
            exit()
        try:
            with open(self.config_file, 'r') as file:
                data = yaml.safe_load(file)
                return data
        except yaml.YAMLError as yaml_err:
            logging.error(f"YAML Parsing Error - {yaml_err}")
            exit()

    def get_wordlists(self):
        """Get the list of wordlist paths from the configuration."""
        wordlists = self.config_data.get('wordlists', [])
        if not wordlists:
            logging.error("No wordlists specified in the configuration file.")
            exit()
        return wordlists

    def get_output_file(self):
        """Get the output file path from the configuration."""
        output_file = self.config_data.get('output_file', None)
        if not output_file:
            logging.warning("No output file specified in configuration. Using default output.")
            output_file = "dorker_results.txt"
        return output_file

    def get_google_api_keys(self):
        """Get Google API keys from the configuration."""
        google_api_keys = self.config_data.get('Google-API', [])
        if not google_api_keys:
            logging.error("No Google API keys specified in the configuration file.")
            exit()
        return google_api_keys

    def get_google_cse_ids(self):
        """Get Google CSE IDs from the configuration."""
        google_cse_ids = self.config_data.get('Google-CSE-ID', [])
        if not google_cse_ids:
            logging.error("No Google CSE IDs specified in the configuration file.")
            exit()
        return google_cse_ids

class GoogleDorker:
    def __init__(self, domain, output, google_api_keys, google_cse_ids):
        self.domain = domain
        self.output = output
        self.google_api_keys = google_api_keys
        self.google_cse_ids = google_cse_ids
        self.results_per_page = 10
        self.total_results = 100

    def query_google(self, search_query):
        """Query Google Custom Search Engine using the provided search_query."""
        try:
            # Randomly select API key and CSE ID
            google_api = random.choice(self.google_api_keys)
            google_cse_id = random.choice(self.google_cse_ids)

            service = build('customsearch', 'v1', developerKey=google_api)
            results = []

            start_index = 1
            while start_index < self.total_results:
                try:
                    response = service.cse().list(
                        q=search_query,
                        cx=google_cse_id,
                        num=self.results_per_page,
                        start=start_index
                    ).execute()

                    for item in response.get('items', []):
                        title = item['title']
                        link = item['link']
                        results.append(f"[{search_query}] [{link}] [{title}]")

                    start_index += self.results_per_page
                    # Sleep to prevent rate limiting
                    #time.sleep(random.uniform(1, 2))

                except Exception as e:
                    logging.error(f"Failed to execute search query '{search_query}' - {e}")
                    break

            # Display and save results
            if results:
                for url in results:
                    logging.info(f"[{COLORS['GREEN']}FOUND{COLORS['RESET']}] {url}")
                    self.write_result(url)
                logging.info(f"Total URLs found for '{search_query}': {len(results)}")
            else:
                logging.warning(f"{COLORS['RED']}No found{COLORS['RESET']} {search_query}")

        except Exception as e:
            logging.error(f"Unexpected error in query_google - {e}")

    def write_result(self, url):
        """Write a result to the output file."""
        output_dir = os.path.dirname(self.output)

        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(self.output, "a") as file:
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
    """Charge les mots d'un fichier wordlist et renvoie un ensemble de mots uniques."""
    if not os.path.isfile(wordlist_path):
        logging.warning(f"Le fichier wordlist {wordlist_path} est introuvable.")
        return set()

    try:
        with open(wordlist_path, 'r', encoding='utf-8') as wl_file:
            mots = set(ligne.strip() for ligne in wl_file if ligne.strip())
        return mots
    except Exception as e:
        logging.error(f"Erreur lors de la lecture du fichier {wordlist_path} : {e}")
        return set()

def main():
    parser = argparse.ArgumentParser(description=f"{COLORS['CYAN']}A Powerful Tool for Google Dorking{COLORS['RESET']}")
    parser.add_argument("-q", "--query", help=f"[{COLORS['GREEN']}ALERT{COLORS['RESET']}]: Google dorking query for your target", type=str)
    parser.add_argument("-d", "--domain", help=f"[{COLORS['GREEN']}ALERT{COLORS['RESET']}]: Target name for Google dorking", type=str)
    parser.add_argument("-o", "--output", help=f"[{COLORS['GREEN']}ALERT{COLORS['RESET']}]: File name to save the dorking results", type=str)
    args = parser.parse_args()

    validate_arguments(args)

    logging.info(f"{RANDOM_COLOR}Starting Google Dorker...{COLORS['RESET']}")

    # Load configuration using ConfigLoader
    config_loader = ConfigLoader()
    wordlists = config_loader.get_wordlists()
    output_file = args.output if args.output else config_loader.get_output_file()
    google_api_keys = config_loader.get_google_api_keys()
    google_cse_ids = config_loader.get_google_cse_ids()

    # Initialize GoogleDorker with configuration data
    dorker = GoogleDorker(
        domain=args.domain,
        output=output_file,
        google_api_keys=google_api_keys,
        google_cse_ids=google_cse_ids
    )

    # If a direct query is provided, use it
    if args.query:
        search_query = f"{args.query} site:{args.domain} " if args.domain else args.query
        dorker.query_google(search_query)
    else:
        # Iterate over each wordlist
        for wordlist_path in wordlists:
            mots = charger_mots(wordlist_path)
            if not mots:
                continue  # Passe au wordlist suivant si aucun mot n'est chargé
            for mot in mots:
                search_query = f"{mot} site:{args.domain}" if args.domain else mot
                dorker.query_google(search_query)

if __name__ == "__main__":
    main()

# modules/dorking.py

from icecream import ic

# Import local
from .config_loader import get_config_values
from .google_dorker import query_google
from .utils import charger_mots
from .constants import RESULTS_PER_PAGE, TOTAL_RESULTS

def handle_dorking(config_data, domain, output_file, query=None):
    """Handle the dorking process with the given query or domain."""
    wordlists = get_config_values(config_data, 'wordlists', [], "No wordlists specified in configuration.")
    google_api_keys = get_config_values(config_data, 'Google-API', [], "No Google API keys specified in configuration.")
    google_cse_ids = get_config_values(config_data, 'Google-CSE-ID', [], "No Google CSE IDs specified in configuration.")

    # If a direct query is provided, use it
    if query:
        search_query = f"{query} site:{domain}" if domain else query
        google_api_keys, google_cse_ids = query_google(search_query, google_api_keys, google_cse_ids, RESULTS_PER_PAGE, TOTAL_RESULTS, output_file)
    else:
        # Iterate over each wordlist
        for wordlist_path in wordlists:
            mots = charger_mots(wordlist_path)
            if not mots:
                continue  # Skip to next wordlist if none are loaded
            for mot in mots:
                search_query = f"{mot} site:{domain}" if domain else mot
                google_api_keys, google_cse_ids = query_google(search_query, google_api_keys, google_cse_ids, RESULTS_PER_PAGE, TOTAL_RESULTS, output_file)

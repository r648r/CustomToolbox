# modules/google_dorker.py

import logging
import random
import sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from icecream import ic

# Import local
from .constants import COLORS
from .utils import write_result
from .exceptions import NoValidAPIKeyException
from .exceptions import NoValidCSEIDException
    

def build_google_service(api_keys):
    """
    Construit le service Google Custom Search API en utilisant une clé API aléatoire.
    Retourne l'objet service et la clé API utilisée.
    """
    while api_keys:
        api_key = random.choice(api_keys)
        try:
            service = build('customsearch', 'v1', developerKey=api_key, cache_discovery=False)
            return service
        except HttpError as e:
            logging.error(f"Clé API invalide ou quota dépassé pour '{api_key}' - {e}")
            api_keys.remove(api_key)

    raise NoValidAPIKeyException("Aucune clé API Google valide disponible.")

def execute_search(service, cse_ids, search_query, results_per_page, total_results):
    """
    Exécute la requête de recherche en utilisant le service fourni et un ID CSE aléatoire.
    Retourne les résultats bruts de la recherche.
    """
    results = []
    start_index = 1
    while start_index < total_results:
        if not cse_ids:
            raise NoValidCSEIDException("Aucun ID CSE Google valide disponible.")
        cse_id = random.choice(cse_ids)
        try:
            response = service.cse().list(
                q=search_query,
                cx=cse_id,
                num=results_per_page,
                start=start_index
            ).execute()
            results.extend(response.get('items', []))
            start_index += results_per_page
        except HttpError as e:
            status_code = e.resp.status
            if status_code == 429:
                logging.warning(f"RateLimitExceeded : ID CSE '{cse_id}' - HttpError {status_code}")
            else:
                logging.warning(f"Search failed with this CSE ID : '{cse_id}' - HttpError {status_code} - {e}")
            cse_ids.remove(cse_id)
            ic(type(cse_ids), cse_ids)
        except Exception as e:
            logging.error(f"Big problem bro - {e}")
            break
    return results



def process_results(items):
    """
    Traite et formate les résultats de la recherche.
    Retourne une liste de tuples contenant le titre et le lien.
    """
    results = []
    for item in items:
        title = item.get('title', 'Pas de titre')
        link = item.get('link', 'Pas de lien')
        results.append((title, link))
    return results

def save_and_log_results(results, output_file, search_query):
    if results:
        for title, link in results:
            formatted_result = f"[{search_query}] [{link}] [{title}]"
            logging.info(f"[{COLORS['GREEN']}FIND{COLORS['RESET']}] {formatted_result}")
            write_result(output_file, search_query, link)
        logging.info(f"Total des URL trouvées pour '{search_query}': {len(results)}")
    else:
        logging.info(f"[{COLORS['RED']}Aucun résultat trouvé pour{COLORS['RESET']}] {search_query}")

def query_google(search_query, google_api_keys, google_cse_ids, results_per_page, total_results, output_file):
    try:
        service = build_google_service(google_api_keys)
        raw_results = execute_search(service, google_cse_ids, search_query, results_per_page, total_results)
        processed_results = process_results(raw_results)
        save_and_log_results(processed_results, output_file, search_query)
        return google_api_keys, google_cse_ids
    except NoValidAPIKeyException as e:
        logging.error(f"{e}")
        sys.exit(1)
    except NoValidCSEIDException as e:
        logging.error(f"{e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Échec de la fonction query_google pour '{search_query}' - {e}")
        return google_api_keys, google_cse_ids

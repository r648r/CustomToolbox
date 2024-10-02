import os
import logging

def write_result(output_file, search_query, url):
    """Write a result to the output file."""
    try:
        output_dir = os.path.dirname(output_file)
        # Create the output directory if it doesn't exist
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            logging.info(f"Created output directory: {output_dir}")

        with open(output_file, "a", encoding='utf-8') as file:
            file.write(f"[{search_query}] {url}\n")
            logging.debug(f"Wrote result to {output_file}: [{search_query}] {url}")
    except Exception as e:
        logging.error(f"Failed to write result to {output_file} - {e}")


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
            return set(line.strip() for line in wl_file if line.strip())
        
    except Exception as e:
        logging.error(f"Error reading wordlist file {wordlist_path} : {e}")
        return set()

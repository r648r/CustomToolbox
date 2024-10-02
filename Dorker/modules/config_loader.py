import os
import yaml
import logging

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

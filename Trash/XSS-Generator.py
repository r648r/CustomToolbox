#!/usr/bin/env python3
import argparse
import urllib.parse
import sys

def unescape_js(encoded_str):
    """
    Décoder une chaîne encodée de manière similaire à JavaScript's unescape.
    Remplace les séquences %xx par les caractères correspondants.
    """
    return urllib.parse.unquote(encoded_str)

def main():
    parser = argparse.ArgumentParser(
        description="Décoder une chaîne encodée de manière similaire à JavaScript's unescape."
    )
    parser.add_argument(
        "encoded_string",
        type=str,
        nargs='?',
        help="La chaîne encodée à décoder. Si non fourni, la lecture se fait depuis l'entrée standard."
    )
    
    args = parser.parse_args()

    if args.encoded_string:
        decoded = unescape_js(args.encoded_string)
        print(decoded)
    else:
        # Lecture depuis l'entrée standard
        print("Entrez la chaîne encodée à décoder (Ctrl+D pour terminer) :")
        input_str = sys.stdin.read()
        decoded = unescape_js(input_str.strip())
        print(decoded)

if __name__ == "__main__":
    main()

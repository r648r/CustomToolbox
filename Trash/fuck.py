# Impossible de faire plus de 2 requetes d'affilé sans le taper une exeption pour me dire que je suis rate limite. Mais je pense que c'est la meilleurs solutions car les requêtes google CSE coûtent 5 $pour 1 000 requêtes, jusqu'à un maximum de 10 000 requêtes par jour.
# 
# Mais pour l'implémenté il faudrait que je fasse du proxy rotation, avec un bail service en ligne pas trop chère
# 
# ```python
# j = search("test", num_results=100, lang="en", proxy="http://API:@proxy.host.com:8080/", ssl_verify=False)
# ```
# 
# Pour de belle liste de dorks j'avais vus ca : <https://github.com/nawaraskc217/google_dorks>


import argparse
from googlesearch import search
import urllib.parse
from icecream import ic


def main():
    parser = argparse.ArgumentParser(description="Zouloute des query google")
    parser.add_argument('-w', '--wordlist', required=True, help='Path to worlist')
    parser.add_argument('-d', '--domaine', required=True, help='Domaine name')
    args = parser.parse_args()
    
    with open(args.wordlist, 'r') as f:
        dorks = [line.strip() for line in f if line.strip()]
    
    for dork in dorks:
        query = f"{dork} site:{args.domaine}"
        print(f"https://www.google.com/search?client=firefox-b-d&q={urllib.parse.quote(query)}")
        print(f"==============================================================================")
        search_results = search(query, num_results=10, advanced=True)
        for result in search_results:
            ic(result)

if __name__ == "__main__":
    main()

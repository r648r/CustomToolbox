# Configure logging

## To do

### Output

- [ ] Crée le repertoire .\result si il n'existe pas
- [ ] Crée un fichier en output soit dans le reperoire ./result de cette forme : <nom_de_la_wordlist (sans le '.txt')>.domain.txt
- [ ] Faire l'output dans un fichier parsable en bash facilement
- [ ] Trouver pourquoi le programme tourne autant quand les clef sont dead
- [ ] Constante.py Test and add support with arguments + config file

### Features

- [ ] Faire un fuzzer de clef CSE pour généré des clef
- [ ] Géré les dork avec des "" et non site:
- [ ] Implémenté le listing sur une wrodlist de domaine
- [ ] Trouver solution pour automatisation a grande echelle
- [ ] Statistique sur les dork qui marche le mieux
- [ ] Faire un arg qui verifie si les dork d'une worldlist sont KO meme sans site
- [ ] Implémenté une enum de domaine via un arg et une wordlist deja la
- [ ] Asynchore / multhreding

### Super chiant

- [ ] meilleurs pratique python : <https://github.com/Utkarsh731/python-coding-best-pracitces>
- [ ] cache_discovery=False  Comprendre c'est quoi cette merde : cache_discovery=False
- [ ] Faire des commentaires plsu claire en anaglais
- [ ] Supprim tout les fr dans le code et varaible
- [ ] # Mettre ces 2 la ici et comprendre leur imapct : RESULTS_PER_PAGE = 10
- [ ] TOTAL_RESULTS = 100
- [ ] Faire du trie dans mes imports
- [ ] Faire un tour de tout les loggins les mettre en anglais + definir le niveau plus finnement
- [ ] Faire plus de clef de CSE Google
- [ ] Add small sleep
- [ ] Faire un vrai README.MD
- [ ] Regarder des hearder de la requests
- [X] Raise les exeption lier aux clef d'api dead
- [X] Ajouter des Wordlists dans fichier de conf
      - [X] Modifier le nom du fichier de conf rc
      - [X] Faire une classe gestion de worlist
- [ ] Intégreé a exegol !!

## Tips

Selectionner depuis les log les url valide.

 ```bash
 cat /mnt/c/Users/r.lechappe/Documents/Personnel/g-dork-search-engine/Dorker/google_dorker.log | grep 'FOUND' | sed -n 's/.*\[\(http[^ ]*\)\].*/\1/p'
 ```

 ```bash
 pip install colorama icecream PyYAML google-api-python-client oauth2client
 ```

```bash
pip freeze > requirements.txt 
```

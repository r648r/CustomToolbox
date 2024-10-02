# Configure logging

## To do

### Output

- [ ] Faire en sorte que le nom du fichier du dossier soit le domaine de l'entreprise
- [ ] Faire en sorte que dans le reperoire resulat choisit dans le rc ai pour nom // que la wordlist
- [ ] Faire l'output dans un fichier parsable en bash facilement
- [ ] Trouver pourquoi le programme tourne autant quand les clef sont dead

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

- [ ] meilleurs pratique python : https://github.com/Utkarsh731/python-coding-best-pracitces
- [ ] cache_discovery=False  Comprendre c'est quoi cette merde : cache_discovery=False 
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

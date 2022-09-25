# Problème 1 : Affichage d'images bitmap

## Résumé du travail à réaliser

Le travail demandé consiste à réaliser un programme Python en ligne de commande 
qui affiche une image au format PPM dont le chemin est passé en paramètre au 
programme.

## Description du format PPM

Le format d'images PPM permet de stocker une image non compressée, en écrivant
directement dans un fichier la liste des pixels qu'elle contient avec leurs
couleurs. Une couleur est décrite au moyen de trois coordonnées indiquant les
quantités de rouge, vert et bleu qui la composent. On appelle RGB (*red, green,
blue*) ce système de coordonnées.

Un fichier PPM est constitué d'une en-tête suivie de la liste des pixels de
l'image. L'en-tête comporte quatre valeurs, séparées par des espaces ou des
sauts de lignes :

-   La version, sur deux caractères. Il existe principalement deux versions, P3
    et P6 — on utilisera ici la version P3 ;
-   La largeur de l'image, en nombre de pixels, écrite en texte brut (par
    exemple la chaîne `"1024"` pour la valeur 1024) ;
-   La hauteur de l'image, en pixels, écrite en texte brut ;
-   La valeur maximale de chaque coordonnée de couleur, écrite en texte brut,
    par exemple 255.

Dans l'en-tête, le caractère dièse (`'#'`) est utilisé pour les commentaires.
Tous les caractères situés entre le dièse et le prochain saut de ligne doivent
être ignorés.
Immédiatement après l'en-tête vient la liste de pixels, énumérés depuis le
premier en haut à gauche de l'image jusqu'à celui en bas à droite, en
parcourant l'image ligne par ligne.
Dans la version P3, les valeurs des couleurs pour chaque pixel sont écrites en
texte brut, les valeurs séparées par des espaces ou des sauts de lignes (la
version P6 utilise un codage un peu plus compliqué).  
Voici un exemple d'image PPM en version P3:

```
P3
# exemple d'image
4 4 # carré de 4 sur 4 pixels
20 # la valeur maximale d'une couleur est 20
20  0  0    0  0  0    0  0  0   20 13  0
 0  0  0    0 20 10    0  0  0    0  0  0
 0  0  0    0  0  0    0 20 10    0  0  0
 0 20  0    0  0  0    0  0  0    0  0  0
```

La quatrième ligne de l'exemple ci-dessus (20) indique la valeur maximale
d'intensité pour chaque canal de couleur (rouge, vert ou bleu) d'un pixel. Dans
cet exemple cela signifie donc que chaque composante de couleur est exprimée
par un nombre entre 0 (correspondant à 0% d'intensité de la couleur concernée)
et 20 (correspondant à 100% d'intensité)

Dans l'exemple, le pixel en haut à gauche de l'image est codé par les trois
valeurs `20  0  0`. Ces valeurs indiquent une intensité de rouge de 20/20 =
100%, et une intensité de vert et de bleu de 0/20 = 0%. Ce pixel est donc
rouge pur. On note cette couleur RGB par le triplet 
(20/20, 0/20, 0/20) = (100%, 0%, 0%). 

De même, la couleur du pixel en bas à gauche est codée par `0 20  0`; en RGB,
cela donne donc (0,1,0), c'est-à-dire du vert pur. Enfin, la couleur du pixel
en haut à droite est (20/20, 13/20, 0) = (1, 0.65, 0), mélange de rouge et de
vert qui produit une couleur orange.

Vous trouverez plus de détails sur le [système
RGB](https://fr.wikipedia.org/wiki/Rouge_vert_bleu) et sur le [format
PPM](https://fr.wikipedia.org/wiki/Portable_pixmap) sur Wikipedia.

## Travail demandé

Comme dans la plupart des travaux qui vous seront proposés au cours de ce
module, nous séparons une partie obligatoire, qu'il est indispensable de
terminer entièrement pour obtenir une bonne appréciation, et une partie
optionnelle vous permettant de creuser davantage les aspects qui vous
intéressent.

### Partie obligatoire

Écrire un programme recevant comme argument le nom d'un fichier PPM au format
P3 et affichant l'image qu'il contient à l'aide de `fltk`. 

Note : pour cet exercice, on affichera l'image "à la main", sans utiliser la
fonction `image` de `fltk` ou une autre bibliothèque de gestion d'images.

### Améliorations possibles

Si vous avez **entièrement terminé la partie obligatoire**, vous êtes libre de
réaliser toute amélioration qui vous intéresse, ou même de simplement vous
documenter et rassembler des informations pertinentes sur le sujet (que vous
pourrez présenter sous la forme d'un bref rapport, par exemple dans un fichier
`rapport.txt`).

Voici quelques idées d'approfondissements possibles :

- Étudier d'autres formats d'images bitmap (PGM, PBM, PPM P6, BMP, etc.) afin
  de déterminer comment les afficher.
- Réaliser quelques filtres (noir et blanc, séparation des canaux, luminosité,
  inverse, bruit, flou, rotation ou symétrie...) que votre afficheur pourra
  appliquer aux images chargées sur simple pression d'une touche du clavier ou
  d'un bouton sur l'interface.
- Permettre l'édition d'images à la main par clic sur les pixels (par exemple :
  édition d'icônes, d'emoji...)
- Implémenter une fonctionnalité de sauvegarde des images.
- Ajouter des paramètres optionnels en ligne de commande (niveau de zoom,
  rotation ou symétrie, format...).

Cette liste n'est évidemment pas exhaustive.

## Conseils

Pour réaliser cet exercice, vous devez connaître (ou réviser) :
- la notion de script et le passage de [paramètres en ligne de
  commande](https://docs.python.org/fr/3/tutorial/stdlib.html#command-line-arguments) ;
- la [documentation du module `fltk`](https://antoinemeyer.frama.io/fltk/) ;
- l'accès aux
  [fichiers](https://docs.python.org/fr/3/tutorial/inputoutput.html#reading-and-writing-files) ;
- la manipulation de [chaînes de
  caractères](https://docs.python.org/fr/3/tutorial/introduction.html#strings)
  (en particulier la fonction
  [`split`](https://docs.python.org/fr/3/library/stdtypes.html#str.split)) ;
- la manipulation de
  [listes](https://docs.python.org/fr/3/tutorial/introduction.html#lists) en
  Python.

Il est recommandé de structurer le plus proprement possible votre code à l'aide
de fonctions, et de respecter les bonnes pratiques de présentation du code
expliquées par exemple
[ici](https://python.sdv.univ-paris-diderot.fr/15_bonnes_pratiques/). Un outil
d'analyse de code comme [Pylava](https://pylavadocs.readthedocs.io/en/latest/)
peut être très utile pour cela.

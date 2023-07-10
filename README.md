Créons ensemble un programme Python et Numpy qui permet de générer du texte qui ressemble à du français. Pour ça, je vais m'appuyer sur le concept de Chaînes de Markov.

On commence par charger un texte qui nous servira de base de données. Ici on va utiliser [Le rouge et le noir](https://archive.org/stream/lerougeetlenoir0000sten/lerougeetlenoir0000sten_djvu.txt) de Stendhal, qui est disponible en téléchargement gratuit. Après avoir téléchargé le contenu du livre en `txt`, on peut le charger dans notre programme Python, et commencer par supprimer tous les retours à la ligne et caractères spéciaux, ainsi que de mettre toutes les lettres en minuscules :

```Python
# Chargement du fichier texte de référence
with open(my_dir + "Le rouge et le noir.txt", "r", encoding='utf-8') as f:
    text = f.read().replace("\n", " ").lower()
    for c in '-;:!?"()*—£':
        text = text.replace(c, ' ')
        text = text.replace("  ", " ")
```

Pour savoir quelle taille va faire notre matrice finale, on peut compter le nombre $n$ de caractères différents présents dans ce texte. On peut alors définir une matrice de dimension $n^3$ dans laquelle on va compter le nombre d'occurrences d'une lettre en fonction des deux lettres qui la précèdent. 

```Python
# Comptage du nombre de caractères différents
chars = set(text)
n_char = len(chars)
occurences_matrix = np.zeros((n_char, n_char, n_char))
```

Pour pouvoir compter ces occurrences, il nous faut un moyen de lier chaque caractère à un indice de $1$ à $n$. On va simplement utiliser un dictionnaire :

```Python
# Création d'un dictionnaire pour associer chaque caractère à un nombre
char_to_int = dict((c, i) for i, c in enumerate(chars))
```

On peut enfin commencer à compter les caractères. On crée deux variables `prev_char` et `prev2_char` qui vont stocker pendant la boucle les deux caractères précédents. On initialise ces deux variables avec des espaces.

```Python
# Comptage des occurences de chaque lettre en fonction des deux précédentes
prev_char, prev2_char = ' ', ' '
for char in text:
   occurences_matrix[char_to_int[prev2_char],
                     char_to_int[prev_char],
                     char_to_int[char]] += 1
   prev2_char = prev_char
   prev_char = char
```

Il faut maintenant diviser chaque ligne de la matrice de sorte à obtenir des fréquences, pour deux lettres précédentes données.

```Python
# Normalisation des occurences
for i in range(n_char):
      for j in range(n_char):
         if np.sum(occurences_matrix[i, j, :]) > 0:
               occurences_matrix[i, j, :] /= np.sum(occurences_matrix[i, j, :])
```

Il ne nous reste plus qu'à paramétrer notre programme en entrant les deux premières lettres du texte à générer et sa longueur.

```Python
# Nombre de caractères à générer et caractères de départ
n_char_to_generate = 100
prev_char, prev2_char = 'l', 'e'
generated = prev2_char + prev_char
```

On peut alors commencer à générer du texte en utilisant la matrice de fréquences créée comme probabilité d'apparition d'une lettre après deux autres :

```Python
# Génération de texte
for i in range(n_char_to_generate):
   probs = occurrences[char_int[prev2_char],
                        char_int[prev_char]]
   next_char = np.random.choice(int_char,
                                 p=probs)
   generated += next_char
   prev2_char = prev_char
   prev_char = next_char
```

Enfin, on rajoute un point final, et on parcourt le texte une dernière fois pour remettre des majuscules en début de phrase, avant de pouvoir finalement affiché notre texte généré.

```Python
# Rétablissement des majuscules après les caractères '. '
generated_text += '. '
for i in range(len(generated_text)):
   if generated_text[i-2:i] == '. ':
      generated_text = generated_text[:i] + generated_text[i].upper() + generated_text[i+1:]

print(generated_text)
```

Voici le texte ainsi généré. On peut y lire des mots de la langue française comme `plan` ou `celle`, et des mots qu'on aurait presque envie d'ajouter au dictionnaire, comme `magrelle` ou le verbe  `chalonner`.

```
El, de, endent lettes plan pos d’eng. Dit chalonnait avai dis une que feredit a lus les, mandrenteme cyraigureux je le en orts a crour due rode voup dir une. Quest cevecomment ambierachasprit de voir de d’unes le sine dont grange. Se si 400 rec moyes l’helle m. Aurde magrelle jultree, moitu si jule sait ant. Son vez peresec amont ses a hons vole, ii insant connesest lle, je uncier. Ost lest be laite. De fetaiten donnee coute nouvrie l’au vatier. Cit unee la frahil le maires moleur, re. Et fel nee maimir la. Sertes combe des, marde celle le. Siondees cous les il de moi sangagie m m unee queforee vide amointrent, con ent, mans pente de l’ait arle faccas l’ord. Mortue lardisachemoilicne prons lieransez moit pas des actemen de cour un leille, s’il nier nais de remblen res la apperres nors son a sie prieller. La sond trocussaint egauten, de cup il, abonge, ever. La prens a vingts des et l mal n’exteme de de hes le mardu beaut chaus tiqu’au bont den. Chevortur a tont bor<pours, julie jule sign.
```

Bien sûr, il est assez facile de se rendre compte que ce texte n'est pas français. Pourquoi ne pas aller plus loin avec des matrices d'occurrences de dimension $4$ voire $5$ ? 


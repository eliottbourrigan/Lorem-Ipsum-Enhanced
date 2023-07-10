import numpy as np
my_dir = "C:/Users/ebour/Documents/Obsidian Vault/Projets/Informatique/Lorem Ipsum Enhanced/"

# Chargement du fichier texte de référence
with open(my_dir + "Le rouge et le noir.txt", "r", encoding='utf-8') as f:
    text = f.read().replace("\n", " ").lower()
    for c in '-;:!?"()*—£%':
        text = text.replace(c, ' ')
        text = text.replace("  ", " ")

# Comptage du nombre de caractères différents
chars = set(text)
n_char = len(chars)
occurrences = np.zeros((n_char, n_char, n_char))

# Création d'un dictionnaire pour associer chaque caractère à un nombre et vice-versa
char_int = dict((c, i) for i, c in enumerate(chars))
int_char = [c for c in chars]

# Comptage des occurences de chaque lettre en fonction des deux précédentes
prev_char, prev2_char = ' ', ' '
for char in text:
   occurrences[char_int[prev2_char],
                     char_int[prev_char],
                     char_int[char]] += 1
   prev2_char = prev_char
   prev_char = char
   
# Normalisation des occurences
for i in range(n_char):
      for j in range(n_char):
         if np.sum(occurrences[i, j, :]) > 0:
               occurrences[i, j, :] /= np.sum(occurrences[i, j, :])

# Nombre de caractères à générer et caractères de départ
n_char_to_generate = 1000
prev_char, prev2_char = 'l', 'e'
generated = prev2_char + prev_char

# Génération de texte
for i in range(n_char_to_generate):
   probs = occurrences[char_int[prev2_char],
                        char_int[prev_char]]
   next_char = np.random.choice(int_char,
                                 p=probs)
   generated += next_char
   prev2_char = prev_char
   prev_char = next_char

# Rétablissement des majuscules après les caractères '. '
generated = generated[0].upper() + generated[1:] + '.'
for i in range(len(generated)):
   if generated[i-2:i] == '. ':
      generated = generated[:i] + generated[i].upper() + generated[i+1:]

print(generated)




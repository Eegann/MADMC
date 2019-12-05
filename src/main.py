import math
import random
import copy
import time

import file_parsing
import local_search
import incremental_elicitation

##### Paramètres du programme #####

# n objets, entre 1 et 200
n = 10
k = math.floor(n/2)
# p critères, entre 1 et 6
p = 2

####################################

# récupération des valeurs du fichier texte
data = file_parsing.get_data(n,p)

print("Recherche locale:\n\n")
time1 = time.time()

[allx,ally] = local_search.neighbor_local_search(n,k,p,data)

time2 = time.time()

ally_for_file = copy.deepcopy(ally)
print("Données utilisées: ",data)
print("Vecteurs d'affectation solutions: ",allx)
print("Valeurs des évaluations: ",ally)

# on crée un vecteur de poids aléatoire simulant les préférences du décideur
w=[random.uniform(0,1) for i in range(p)]

# on le normalise pour que la somme du vecteur fasse 1
w=[w[i]/sum(w) for i in range(p)]

print("\n\nElicitation incrémentale:\nNombre de solutions potentielles:",len(ally),"\n\n")
time3 = time.time()

[opt,opt_value, nb_q] = incremental_elicitation.mmr_incremental_elicitaiton(allx, ally, w)

time4 = time.time()
print("Solution optimale: ",opt)
print("Valeur de la solution: ",opt_value)
print("Poids du décideur: ",w)
print("Nombre de questions: ",nb_q)

file_parsing.write_res(ally_for_file, n, p, nb_q, time2-time1, time4-time3)
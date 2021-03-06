import math
import random
import copy
import time

import file_parsing
import local_search
import incremental_elicitation
import nd_tree
import interactive_local_search

import multiprocessing

def compare_to_file(n,p,k):
    pareto = file_parsing.get_pareto(n,p)
    pareto_opt=pareto[0]
    pareto_opt_value=0
    for i in range(p):
        pareto_opt_value+=pareto_opt[i]*w[i]
    for par in pareto:
        pareto_value=0
        for i in range(p):
            pareto_value += par[i] * w[i]
        if pareto_value>pareto_opt_value:
            pareto_opt=par
            pareto_opt_value=pareto_value
    return pareto_opt


def procedure1_PLS(n,p,k,w):
    print("procedure1_PLS  n={} p={}".format(n,p))
    data = file_parsing.get_data(n,p) # n: nb de objets; p: nb de criteres

    # print("Recherche locale:\n\n")
    time1 = time.time()

    [allx, ally] = local_search.neighbor_local_search(n, k, p, data)
    time2 = time.time()
    ally_for_file = copy.deepcopy(ally)

    #print("Données utilisées: ", data)
    #print("Vecteurs d'affectation solutions: ", allx)
    #print("Valeurs des évaluations: ", ally)

    # print("\n\nElicitation incrémentale:\nNombre de solutions potentielles:", len(ally), "\n\n")
    time3 = time.time()

    evidence = [];
    [opt, opt_value, nb_q, _, _] = incremental_elicitation.mmr_incremental_elicitaiton(allx, ally, w, evidence)

    time4 = time.time()
    # print("Solution optimale: ", opt)
    # print("Valeur de la solution: ", opt_value)
    # print("Poids du décideur: ", w)
    # print("Nombre de questions: ", nb_q)

    real_opt=compare_to_file(n, p, k)

    file_parsing.write_res_proc1_PLS(opt_value, real_opt, n, p, w, nb_q, time2 - time1, time4 - time3)
    
    
def procedure1_nd_tree(n,p,k,w):

    print("procedure1_ND_tree  n={} p={}".format(n,p))
    data = file_parsing.get_data(n, p)

    # print("Recherche locale:\n\n")
    time1 = time.time()

    [allx, ally] = nd_tree.nd_tree(n, k, p, data)
    time2 = time.time()
    ally_for_file = copy.deepcopy(ally)

    # print("Données utilisées: ", data)
    # print("Vecteurs d'affectation solutions: ", allx)
    # print("Valeurs des évaluations: ", ally)

    # print("\n\nElicitation incrémentale:\nNombre de solutions potentielles:", len(ally), "\n\n")
    time3 = time.time()

    [opt, opt_value, nb_q, _, _] = incremental_elicitation.mmr_incremental_elicitaiton(allx, ally, w, [])

    time4 = time.time()
    # print("Solution optimale: ", opt)
    # print("Valeur de la solution: ", opt_value)
    # print("Poids du décideur: ", w)
    # print("Nombre de questions: ", nb_q)

    real_opt = compare_to_file(n, p, k)

    file_parsing.write_res_proc1_nd_tree(opt_value, real_opt, n, p, w, nb_q, time2 - time1, time4 - time3)

def procedure2_interactive_local_search(n,p,k,w):
    print("procedure2_ILS  n={} p={}".format(n,p))
    data = file_parsing.get_data(n,p) # n: nb de objets; p: nb de criteres

    # print("Recherche locale + Elicitation incrementale:\n\n")

    time1 = time.time()

    opt, opt_value, nb_q = interactive_local_search.interactive_local_search(n, k, p, data,w)

    time2 = time.time()
    #print("Solution optimale: ", opt)
    # print("Valeur de la solution: ", opt_value)
    # print("Poids du décideur: ", w)
    # print("Nombre de questions: ", nb_q)

    real_opt = compare_to_file(n, p, k)

    file_parsing.write_res_proc2_ILS(opt_value, real_opt, n, p, w, nb_q, time2 - time1)

####################################

if __name__ == "__main__":

    for z in range(14):
        # n objets, entre 1 et 200
        parametres = [[10,2],[10,3],[10,4],[10,5],#[10,6], # 0 ... 4
                      [20,2],[20,3],#[20,4],[20,5],[20,6],  #  5 ...9
                      [30,2]]#,[30,3],[30,4],[30,5],        #  10 .. 13
        #[40,2],[40,3],[40,4],               # 14.. 16
        #[50,2],[50,3],                      # 17 , 18
        #[60,2],[60,3],                      # 19, 20
        #[80,2],                              # 21
        #[100,2],                             # 22
        #[200,2]]                             # 23


        for n,p in parametres:
            # on crée un vecteur de poids aléatoire simulant les préférences du décideur
            w = [random.uniform(0, 1) for i in range(p)]

            # on le normalise pour que la somme du vecteur fasse 1
            w = [w[i] / sum(w) for i in range(p)]
            procedure1_PLS(n,p,math.floor(n/2),w,)

        for n,p in parametres:
            # on crée un vecteur de poids aléatoire simulant les préférences du décideur
            w = [random.uniform(0, 1) for i in range(p)]

            # on le normalise pour que la somme du vecteur fasse 1
            w = [w[i] / sum(w) for i in range(p)]
            procedure1_nd_tree(n, p, math.floor(n / 2), w,)

        for n,p in parametres:
            # on crée un vecteur de poids aléatoire simulant les préférences du décideur
            w = [random.uniform(0, 1) for i in range(p)]

            # on le normalise pour que la somme du vecteur fasse 1
            w = [w[i] / sum(w) for i in range(p)]
            procedure2_interactive_local_search(n, p, math.floor(n / 2), w,)


import csv
import random
import networkx as nx
import matplotlib.pyplot as plt

#NIVEAU_CONFIANCE : Pour un niveau de confiance de 95 %
#PROPORTION_INTERET : Estimation conservatrice de 0,5 (car on ne sait pas si deux streamers ont publics similaires)
#TAILLE_ECHANTILLON : Formule de Cochran
NOMBRE_STREAMERS = 100
SEUIL_ARETE = 10000
NIVEAU_CONFIANCE = 1.96
MARGE_ERREUR = 0.01
PROPORTION_INTERET = 0.5
TAILLE_ECHANTILLON = round(((NIVEAU_CONFIANCE ** 2) * PROPORTION_INTERET * (1 - PROPORTION_INTERET))/(MARGE_ERREUR ** 2))

def affiche_matrice(matrice):
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            print("    {}    ".format(matrice[i][j]), end='|')
        print()

#Dans la diagonale, 2 informations sur le streamer (dans cet ordre) : login et nombre de followers
def init_matrice():
    with open('CSV_Streamers.csv', mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        matrice = []
        
        for i in range(NOMBRE_STREAMERS):
            ligne = []
            for j in range(i+1):
                if(i == j):
                    infos_streamer = next(reader)
                    ligne.append([infos_streamer['Channel'], int(infos_streamer['Followers'])])
                else:
                    ligne.append(0)
            matrice.append(ligne)        
    
    #Initialisation des followers en communs entre deux streamers
    for i in range(1, len(matrice)):
        for j in range(i):
            matrice[i][j] = estimation_followers_commun(matrice[i][i][1], matrice[j][j][1])

    return matrice

#Utilisation d'un échantillonnage aléatoire simple pour avoir estimation du nombre de followers communs à 2 streamers
def estimation_followers_commun(nb_a, nb_b):
    #Création échantillons à partir de sélection aléatoire de TAILLE_ECHANTILLON chiffres parmi une liste de taille nb_a/nb_b
    echantillon_a = random.sample(range(nb_a), TAILLE_ECHANTILLON)
    echantillon_b = random.sample(range(nb_b), TAILLE_ECHANTILLON)

    nb_followers_en_commun = len(set(echantillon_a).intersection(set(echantillon_b)))

    #Calcul de l'estimation en utilisant un facteur de correction
    #estimation = round(followers_en_commun * (nb_a / len(echantillon_a)) * (nb_b / len(echantillon_b)))
    estimation = round((((nb_followers_en_commun / TAILLE_ECHANTILLON) * nb_a) + ((nb_followers_en_commun / TAILLE_ECHANTILLON) * nb_b))/2 )

    return estimation

################################
#Fonctions de création du graphe
def charger_graphe(matrice):
    G = nx.Graph()
    
    #Initialisation des sommets et création d'un tableau pour stocker leur taille
    tailles = []
    for i in range(len(matrice)):
        G.add_node(matrice[i][i][0])
        tailles.append(matrice[i][i][1]/50000)

    #Initialisation des arêtes
    for i in range(1, len(matrice)):
        for j in range(i):
            if(matrice[i][j] > SEUIL_ARETE):
                G.add_edge(matrice[i][i][0],matrice[j][j][0], width=100)
    
    return [G, tailles]

def generation_couleur_aleatoire(G):
    color_map = []
    for node in G:
        if random.randint(0,1) == 0:
            color_map.append('blue')
        else: 
            color_map.append('green')
    return color_map

matrice = init_matrice()
#affiche_matrice(matrice)

tab_aux = charger_graphe(matrice)
G = tab_aux[0]
tailles = tab_aux[1]
color_map = generation_couleur_aleatoire(G)          

nx.draw(G, with_labels=True, font_size=5, font_color='white', node_size=tailles, node_color=color_map, edge_color='red' ,width=0.1)
plt.rcParams['savefig.facecolor'] = '#000000' # Set background color to black
plt.savefig('Graphes.png', dpi=300)
plt.show()

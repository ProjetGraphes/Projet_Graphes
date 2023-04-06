import csv
import random
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk



#NIVEAU_CONFIANCE : Pour un niveau de confiance de 95 %
#PROPORTION_INTERET : Estimation conservatrice de 0,5 (car on ne sait pas si deux streamers ont publics similaires)
#TAILLE_ECHANTILLON : Formule de Cochran
NOMBRE_STREAMERS = 10
SEUIL_ARETE = 7000
AJUSTE_TAILLE_SOMMET = 50000

NIVEAU_CONFIANCE = 1.96
MARGE_ERREUR = 0.01
PROPORTION_INTERET = 0.5
TAILLE_ECHANTILLON = round(((NIVEAU_CONFIANCE ** 2) * PROPORTION_INTERET * (1 - PROPORTION_INTERET))/(MARGE_ERREUR ** 2))

############################FONCTIONS DE CREATION D'UNE MATRICE (NON UTILISEES)############################
def afficher_matrice(matrice):
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            print("    {}    ".format(matrice[i][j]), end='|')
        print()

def initialiser_matrice():
    with open('CSV_Streamers.csv', mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        matrice = []
        
        for i in range(NOMBRE_STREAMERS):
            ligne = [None] * (i+1)
            for j in reversed(range(i+1)):
                if(i == j):
                    #Stockage de 2 informations sur le streamer (dans cet ordre) : login et nombre de followers
                    infos_streamer = next(reader)
                    ligne[j] = [infos_streamer['Channel'], int(infos_streamer['Followers'])]
                else:
                    #Initialisation des followers en communs entre deux streamers
                    ligne[j] = estimer_followers_communs(ligne[i][1], matrice[j][j][1])
            matrice.append(ligne)

    return matrice

############################FONCTIONS DE CREATION DU GRAPHE############################
def charger_graphe():
    with open('CSV_Streamers.csv', mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        G = nx.Graph()
        
        #Initialisation des sommets et arêtes + création d'un tableau pour stocker la taille des sommets
        tailles_sommets = []
        #Initialisation des sommets et de leur taille
        for ligne in range(NOMBRE_STREAMERS):
            infos_streamer = next(reader)

            G.add_node(infos_streamer['Channel'])
            tailles_sommets.append(round(int(infos_streamer['Followers'])/AJUSTE_TAILLE_SOMMET))

            #Initialisation des arêtes
            i_tailles = 0
            for sommet in G.nodes():
                if(sommet != infos_streamer['Channel']):
                    poids = estimer_followers_communs(int(infos_streamer['Followers']), tailles_sommets[i_tailles] * AJUSTE_TAILLE_SOMMET)
                    if(poids > SEUIL_ARETE):
                        G.add_edge(infos_streamer['Channel'], sommet, weight=poids)
                    i_tailles += 1
        
    return {'G': G, 'tailles_sommets': tailles_sommets}

#Utilisation d'un échantillonnage aléatoire simple pour avoir estimation du nombre de followers communs à 2 streamers
def estimer_followers_communs(nb_a, nb_b):
    #Création échantillons à partir de sélection aléatoire de TAILLE_ECHANTILLON chiffres parmi une liste de taille nb_a/nb_b
    echantillon_a = random.sample(range(nb_a), TAILLE_ECHANTILLON)
    echantillon_b = random.sample(range(nb_b), TAILLE_ECHANTILLON)

    nb_followers_en_commun = len(set(echantillon_a).intersection(set(echantillon_b)))

    #Calcul de l'estimation
    estimation = round(nb_followers_en_commun * nb_a / TAILLE_ECHANTILLON)

    return estimation

def detecter_communautes(G):
    communautes = nx.community.louvain_communities(G)
    
    #Création du tableau de couleurs selon la communauté
    couleurs = plt.cm.Set1(range(len(communautes)))
    couleurs_sommets = []
    for sommet in G.nodes():
        for cle, communaute in enumerate(communautes):
            if sommet in communaute:
                couleurs_sommets.append(couleurs[cle])
                break

    return couleurs_sommets



def display_node_info(node):
    neighbors = list(G.neighbors(node))
    print("------------------")
    print(f"NOM DU STREAMER: {node}")
    print(f"NOMBRE DE VOISIN: {len(neighbors)}")
    print("LISTE DE VOISIN: ", neighbors)
    print("------------------")


def on_node_click(event):
    if (event.button == 3 or event.button == 1):
        x, y = event.xdata, event.ydata
        node = None
        min_dist = float("inf")
        for n in G.nodes:
            dist = (pos[n][0] - x)**2 + (pos[n][1] - y)**2
            if dist < min_dist:
                node = n
                min_dist = dist
        display_node_info(node)

tab_aux = charger_graphe()
G = tab_aux['G']
tailles_sommets = tab_aux['tailles_sommets']
couleurs_sommets = detecter_communautes(G)

pos = nx.spring_layout(G)
nx.draw(G, with_labels=True, pos=pos, font_size=5, font_color='white', node_color=couleurs_sommets, node_size=tailles_sommets, edge_color='red', width=0.1)
nx.set_node_attributes(G, pos, 'pos')

plt.rcParams['savefig.facecolor'] = '#000000'
plt.savefig('Graphe.png', dpi=300)
plt.gcf().canvas.mpl_connect('button_press_event', on_node_click)
plt.show()


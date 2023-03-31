import csv

import networkx as nx

import matplotlib.pyplot as plt
import community
from matplotlib import cm

NOMBRE_STREAMERS = 1000

def onClick(event):
    (x, y) = (event.xdata, event.ydata)
    for i in G.nodes():
        node = pos[i]
        distance = pow(x - node[0], 2) + pow(y - node[1], 2)
        if distance < 0.0001:
            print("Le streamer choisi:")
            print(i)
            print("a pour voisins:")
            neighbor = list(G.neighbors(i))
            print(neighbor)

def on_press(event):
    global n1
    global n2
    if event.key == 'e':
        (x, y) = (event.xdata, event.ydata)
        for i in G.nodes():
            node = pos[i]
            distance = pow(x - node[0], 2) + pow(y - node[1], 2)
            if distance < 0.0001:
                n1 = i
                print("Le 1er streamer choisi est:")
                print(n1)
    if event.key == 'm':
        (x, y) = (event.xdata, event.ydata)
        for i in G.nodes():
            node = pos[i]
            distance = pow(x - node[0], 2) + pow(y - node[1], 2)
            if distance < 0.0001:
                n2 = i
                print("Le 2nd streamer choisi est:")
                print(n2)
    if event.key == 'x':
        if (n1 != 0 and n2 != 0):
            paths = list(nx.shortest_simple_paths(G, n1, n2))
            print("le chemin entre ces deux aliments est :")
            print(paths[0])           

with open('CSV_Streamers_BRUT.csv', mode='r', encoding='utf-8') as csv_file:
    data = list(csv.reader(csv_file, delimiter=','))

    fig, ax = plt.subplots()
    fig.canvas.mpl_connect('button_press_event', onClick)
    fig.canvas.mpl_connect('key_press_event', on_press)
    
    G = nx.Graph()
    compteur = 1
    liste=[]
    while compteur < NOMBRE_STREAMERS:

        if compteur != NOMBRE_STREAMERS - 1:
            i = compteur + 1
            while i < NOMBRE_STREAMERS:
                #liste.append(comapredeuxligne(compteur, i))
                i += 1
        compteur += 1
        print(compteur)
    

    pos = nx.fruchterman_reingold_layout(G)
    nx.draw_spring(G, with_labels=True)
    nx.draw_networkx_edges(G, pos, alpha=0.4)

    plt.show()
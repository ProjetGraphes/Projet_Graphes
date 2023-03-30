import csv
from dotenv import load_dotenv
import os
import requests
import mysql.connector

NOMBRE_STREAMERS = 993
LIEN_STREAMERS = 1000

load_dotenv()
headers = {
    'Client-ID': os.getenv('CLIENT_ID'),
    'Authorization': 'Bearer ' + os.getenv('CLIENT_SECRET')
}

mydb = mysql.connector.connect(
  host=os.getenv('DB_HOST'),
  user=os.getenv('DB_USER'),
  password=os.getenv('DB_PASSWORD'),
  database=os.getenv('DB_NAME')
)

def affiche_matrice(matrice):
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            print("    {}    ".format(matrice[i][j]), end='|')
        print()

#Dans la diagonale, 3 informations sur le streamer (dans cet ordre) : ID, login et nombre de followers
def init_matrice():
    with open('CSV_Streamers.csv', mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        matrice = []
        
        for i in range(3):
            ligne = []
            for j in range(i+1):
                if(i == j):
                    infos_streamer = next(reader)
                    ligne.append([int(infos_streamer['ID']), infos_streamer['Channel'], int(infos_streamer['Followers'])])
                else:
                    ligne.append(0)
            matrice.append(ligne)
    return matrice


def lien_streamer(id_a, id_b):
    nb_followers_commun = 0
    


    return nb_followers_commun

'''matrice = init_matrice()
affiche_matrice(matrice)'''
data_json = requests.get("https://api.twitch.tv/helix/users/follows?to_id=55828551", headers=headers)
data_dict = data_json.json()


print(data_dict)
'''tab1 = [1, 2, 3, 4, 5]
tab2 = [3, 4, 5, 6, 7]

print(set(tab1))'''
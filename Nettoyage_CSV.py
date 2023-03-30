from urllib.parse import quote
import requests
import csv
from dotenv import load_dotenv
import os

LIMITE_URL = 100
NOMBRE_STREAMERS = 1000

load_dotenv()
headers = {
    'Client-ID': os.getenv('CLIENT_ID'),
    'Authorization': 'Bearer ' + os.getenv('CLIENT_SECRET')
}

with open('CSV_Streamers_BRUT.csv', mode='r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file, delimiter=',')
    cpt_nombre_streamers = 0
    cpt_id = 0
    nouveau_csv = {}
    
    #Remplissage du tableau temporaire
    for ligne in reader:
        nouveau_csv[int(ligne['Ranking'])-1] = {'Channel': ligne['Channel'], 'Followers': ligne['Followers']}
        
    while cpt_nombre_streamers < NOMBRE_STREAMERS :
        string_url = ""
        cpt_limite_url = 0
        cpt_ajout_id = 0

        #Parcours de 100 streamers pour récupérer leur ID via l'API (appel limité à 100 streamers)
        while cpt_limite_url < LIMITE_URL:
            login = nouveau_csv[cpt_nombre_streamers]['Channel']

            if(cpt_limite_url != 0):
                string_url += "&"
            
            #Sélection du login entre parenthèses
            if('(' in login and ')' in login):
                login = login[login.find("(") + 1 : login.find(")")]
                nouveau_csv[cpt_nombre_streamers]['Channel'] = login

            #Ajout d'un nouveau login
            string_url += "login=" + quote(login)

            cpt_limite_url = cpt_limite_url + 1
            cpt_nombre_streamers = cpt_nombre_streamers + 1
        
        #Appel à l'API pour récupérer l'ID de 100 streamers
        data_json = requests.get('https://api.twitch.tv/helix/users?' + string_url, headers=headers)
        data_dict = data_json.json()
        
        #Ajout des IDs et modification de leur login (si besoin) pour les 100 streamers dans le nouveau CSV
        while cpt_ajout_id < LIMITE_URL:
            for sous_tab in data_dict['data']:
                if nouveau_csv[cpt_id]['Channel'].lower() == sous_tab['login']:
                    nouveau_csv[cpt_id]['ID'] = sous_tab['id']
                    nouveau_csv[cpt_id]['Channel'] = sous_tab['login']
                    break
            cpt_id = cpt_id + 1
            cpt_ajout_id = cpt_ajout_id + 1

#Suppression des streamers à supprimer (pas de retour d'ID car leur compte n'est plus disponible)
for i in range(len(nouveau_csv)):
    if(len(nouveau_csv[i]) != 3):
        nouveau_csv.pop(i)

with open('CSV_Streamers_2.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Channel', 'Followers', 'ID']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for i in nouveau_csv:
        writer.writerow(nouveau_csv[i])
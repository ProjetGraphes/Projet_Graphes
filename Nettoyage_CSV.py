import csv

with open('CSV_Streamers_BRUT.csv', mode='r', encoding='utf-8') as csv_file:
    with open('CSV_Streamers.csv', mode='w', newline='', encoding='utf-8') as new_csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        
        fieldnames = ['Channel', 'Followers']
        writer = csv.DictWriter(new_csv_file, fieldnames=fieldnames)

        writer.writeheader()
        #Remplissage du nouveau CSV avec le login (en lettres latines) et le nombre de followers des streamers
        for ligne in reader:
            chaine = ligne['Channel']
            if('(' in chaine and ')' in chaine):
                chaine = chaine[chaine.find("(") + 1 : chaine.find(")")]
            writer.writerow({'Channel': chaine.lower(), 'Followers': ligne['Followers']})

import mysql.connector
import csv
import sys
from dotenv import load_dotenv
import os

mydb = mysql.connector.connect(
  host=os.getenv('DB_HOST'),
  user=os.getenv('DB_USER'),
  password=os.getenv('DB_PASSWORD'),
  database=os.getenv('DB_NAME')
)
cursor = db.cursor()
headers = next(csv_file)

print("Importation en cours...")
with open('CSV_Streamers') as csv_file:
    csvfile = csv.reader(csv_file, delimiter=",")
    all_value = []
    for row in csvfile:
        value = (row[0], row[2])
        all_value.append(value)
        cursor.execute("INSERT INTO streamers (streamers_login, streamers_twitch_id) VALUES (%s, %s)", all_value )

db.commit()
cursor.close()
print ("Importation fini :)")

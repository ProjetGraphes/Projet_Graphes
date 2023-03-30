import mysql.connector
import csv
import sys
from dotenv import load_dotenv
import os

db = mysql.connector.connect(
  host=os.getenv('DB_HOST'),
  user=os.getenv('DB_USER'),
  password=os.getenv('DB_PASSWORD'),
  database=os.getenv('DB_NAME')
)
cursor = db.cursor()
csv_data = csv.reader(open('CSV_Streamers'))
headers = next(csv_data)

print("Importation en cours...")
for row in csv_data:
    print(row)
    cursor.execute("INSERT INTO streamers (streamers_login, streamers_twitch_id) VALUES (%s, %s)", row )

db.commit()
cursor.close()
print ("Importation fini :)")


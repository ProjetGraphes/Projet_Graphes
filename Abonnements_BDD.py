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


from dotenv import load_dotenv
import os

NOMBRE_STREAMERS = 993

load_dotenv()
headers = {
    'Client-ID': os.getenv('CLIENT_ID'),
    'Authorization': 'Bearer ' + os.getenv('CLIENT_SECRET')
}



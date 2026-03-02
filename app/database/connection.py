from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv
import certifi

load_dotenv()

db_a_client = MongoClient(getenv("FA_MONGO_URI"), tls=True, tlsCAFile=certifi.where())

db_a = db_a_client["innovatearena"]

user_coll = db_a["User"]
event_coll = db_a["Event"]
payments_coll = db_a["Payments"]

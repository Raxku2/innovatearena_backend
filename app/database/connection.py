from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv


load_dotenv()


db_a_client = MongoClient(getenv("FA_MONGO_URI"))

db_a = db_a_client["innovatearena"]

user_coll = db_a["User"]
event_coll = db_a["Event"]
payments_coll = db_a["Payments"]


def pingMongoDB_1():
    try:
        db_a_client.admin.command("ping")
        print("✅ MongoDB connection successful!")
        return True
    except Exception as err:
        print("❌ MongoDB connection failed.")
        print(err)
        return False

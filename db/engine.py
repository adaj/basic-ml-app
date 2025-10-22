import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

def get_mongo_collection(collection_name: str):
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    return db[collection_name]

# Wrap db functions in this module to separate the database logic from the business logic
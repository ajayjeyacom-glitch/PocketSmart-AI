# backend/database.py - MongoDB Connection
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["pocketsmart_db"]

def get_user_collection():
    return db["users"]

def get_history_collection():
    return db["recommendation_history"]

def get_db():
    return db

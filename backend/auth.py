# backend/auth.py - Member 4 - MongoDB + JWT + History
import os
import jwt
import bcrypt
from datetime import datetime, timedelta
from backend.database import get_user_collection, get_history_collection

SECRET_KEY = os.getenv("JWT_SECRET", "pocketsmart_secret_key")
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_jwt(user_id: str) -> str:
    payload = {"user_id": str(user_id), "exp": datetime.utcnow() + timedelta(days=7)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except:
        return None

def register_user(email, password):
    users = get_user_collection()
    if users.find_one({"email": email}):
        return None
    hashed = hash_password(password)
    result = users.insert_one({"email": email, "password": hashed, "created_at": datetime.utcnow()})
    return create_jwt(result.inserted_id)

def login_user(email, password):
    users = get_user_collection()
    user = users.find_one({"email": email})
    if user and verify_password(password, user["password"]):
        return create_jwt(user["_id"])
    return None

def save_recommendation_history(user_id, product, recommendation):
    history = get_history_collection()
    history.insert_one({
        "user_id": str(user_id),
        "product": product,
        "recommendation": recommendation,
        "timestamp": datetime.utcnow()
    })

def get_user_history(user_id):
    history = get_history_collection()
    return list(history.find({"user_id": str(user_id)}).sort("timestamp", -1))

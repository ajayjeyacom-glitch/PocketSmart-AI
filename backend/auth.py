# Member 4 - Auth & Database Module
# PocketSmart-AI - Authentication System

import sqlite3
import hashlib
from datetime import datetime

class AuthManager:
    def __init__(self, db_path="pocketsmart.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Database table create pannum"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Budget table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                category TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully!")

    def hash_password(self, password):
        """Password ah secure ah maathum"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, email, password):
        """Puthu user register pannum"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            password_hash = self.hash_password(password)
            
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            conn.commit()
            conn.close()
            return True, "User registered successfully!"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def login_user(self, username, password):
        """User login check pannum"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        password_hash = self.hash_password(password)
        
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password_hash=?",
            (username, password_hash)
        )
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return True, "Login successful!"
        else:
            return False, "Invalid credentials!"

# Test code
if __name__ == "__main__":
    auth = AuthManager()
    print("Auth Module Ready - Member 4 Work Completed")

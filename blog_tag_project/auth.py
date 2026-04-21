import sqlite3
import hashlib
import time

DB_NAME = "app.db"

# -------------------------
# DB CONNECTION
# -------------------------
def get_connection():
    conn = sqlite3.connect(DB_NAME, timeout=10, check_same_thread=False)
    return conn

# -------------------------
# PASSWORD HASHING
# -------------------------
def hash_password(password, salt="blog_ai_salt"):
    return hashlib.sha256((password + salt).encode()).hexdigest()

# -------------------------
# VALIDATION
# -------------------------
def validate_user(username, password):
    if not username or not password:
        return False
    if len(username) < 3:
        return False
    if len(password) < 4:
        return False
    return True

# -------------------------
# CREATE USER
# -------------------------
def create_user(username, password):
    if not validate_user(username, password):
        return False

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check duplicate username
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        if cursor.fetchone():
            conn.close()
            return False

        # Insert new user
        cursor.execute(
            "INSERT INTO users(username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print("Signup error:", e)
        return False

# -------------------------
# LOGIN USER
# -------------------------
def login_user(username, password):
    if not validate_user(username, password):
        return None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check login credentials
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, hash_password(password))
        )

        user = cursor.fetchone()

        # Update last login only if user exists
        if user:
            try:
                cursor.execute(
                    "UPDATE users SET last_login=CURRENT_TIMESTAMP WHERE username=?",
                    (username,)
                )
                conn.commit()
            except:
                pass  # Ignore if last_login column does not exist

        conn.close()
        return user

    except Exception as e:
        print("Login error:", e)
        return None


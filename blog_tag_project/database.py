import sqlite3

DB_NAME = "app.db"

# -------------------------
# DB CONNECTION HELPER
# -------------------------
def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

# -------------------------
# INIT DATABASE
# -------------------------
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE (FIXED WITH last_login)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP
    )
    """)

    # Add last_login column if old table already exists
    try:
        cursor.execute("""
        ALTER TABLE users ADD COLUMN last_login TIMESTAMP
        """)
    except:
        pass

    # HISTORY TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        content TEXT,
        tags TEXT,
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # INDEX for faster history lookup
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_history_username
    ON history(username)
    """)

    conn.commit()
    conn.close()




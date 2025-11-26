import sqlite3
import os

# ---- DATABASE LOCATION (Railway compatible) ----
DB_PATH = "/workspace/database.db"   # persistent
# DB_PATH = "/tmp/database.db"       # non-persistent (optional)

# Ensure directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Connect to database
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# ---- CREATE TABLE IF NOT EXISTS ----
cursor.execute("""
CREATE TABLE IF NOT EXISTS guilds (
    guild_id INTEGER PRIMARY KEY,
    prefix TEXT DEFAULT '!'
)
""")
conn.commit()

# ---- FUNCTIONS ----

def get_guild(guild_id: int):
    cursor.execute("SELECT * FROM guilds WHERE guild_id = ?", (guild_id,))
    return cursor.fetchone()


def set_prefix(guild_id: int, prefix: str):
    cursor.execute("""
        INSERT INTO guilds (guild_id, prefix)
        VALUES (?, ?)
        ON CONFLICT(guild_id) DO UPDATE SET prefix = excluded.prefix
    """, (guild_id, prefix))
    conn.commit()


def get_or_create_guild(guild_id: int):
    guild = get_guild(guild_id)
    if guild is None:
        cursor.execute("INSERT INTO guilds (guild_id, prefix) VALUES (?, '!')", (guild_id,))
        conn.commit()
        return get_guild(guild_id)
    return guild

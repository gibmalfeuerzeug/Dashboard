import os

DB = "/workspace/database.db"
conn = sqlite3.connect(DB)

def load_db():
    if not DB_FILE.exists():
        save_db({"users": [], "settings": {}})
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Beispiele
def add_user(user):
    db = load_db()
    db["users"].append(user)
    save_db(db)

def get_users():
    db = load_db()
    return db["users"]

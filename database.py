import sqlite3


DB = "database.sqlite"


# Initialisierung
conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS guilds (id TEXT PRIMARY KEY, prefix TEXT)")
conn.commit()
conn.close()


# Guild holen oder erstellen
def get_or_create_guild(gid):
conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("SELECT id, prefix FROM guilds WHERE id=?", (gid,))
row = cur.fetchone()


if not row:
cur.execute("INSERT INTO guilds (id, prefix) VALUES (?, '!')", (gid,))
conn.commit()
row = (gid, '!')


conn.close()
return {'id': row[0], 'prefix': row[1]}


# Prefix setzen
def set_prefix(gid, prefix):
conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("UPDATE guilds SET prefix=? WHERE id=?", (prefix, gid))
conn.commit()
conn.close()


# Prefix holen
def get_prefix_for_guild(gid):
conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("SELECT prefix FROM guilds WHERE id=?", (gid,))
row = cur.fetchone()
conn.close()
return row[0] if row else '!'

# app/db.py
import json
import sqlite3
from config import DB_BACKEND, DB_URL

# Only SQLite is implemented for now
conn = None
if DB_BACKEND == "sqlite":
    import os
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/intel.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ip_cache (
            ip TEXT PRIMARY KEY,
            fingerprint TEXT,
            data TEXT,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

async def cache_result(ip, fingerprint, data):
    if DB_BACKEND != "sqlite" or not conn:
        return
    try:
        conn.execute(
            "REPLACE INTO ip_cache (ip, fingerprint, data) VALUES (?, ?, ?)",
            (ip, fingerprint, json.dumps(data))
        )
        conn.commit()
    except Exception as e:
        print(f"[!] Cache error: {e}")

async def get_cached(ip):
    if DB_BACKEND != "sqlite" or not conn:
        return None
    try:
        cur = conn.execute("SELECT data FROM ip_cache WHERE ip = ?", (ip,))
        row = cur.fetchone()
        return json.loads(row[0]) if row else None
    except:
        return None

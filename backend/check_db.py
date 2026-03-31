import sqlite3
import os

db_paths = [
    r'C:\Users\Make\Desktop\shamgp\backend\shop_db.db',
    r'.\shop_db.db',
    r'..\shop_db.db',
    r'C:\Users\Make\Desktop\shamgp\shop_db.db',
]

for path in db_paths:
    if os.path.exists(path):
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        print(f"Path: {path}")
        print(f"Tables ({len(tables)}): {tables[:5]}...")
        if 'users' in tables:
            cur.execute("SELECT username FROM users LIMIT 3")
            print("Sample users:", [r[0] for r in cur.fetchall()])
        conn.close()
    else:
        print(f"NOT FOUND: {path}")

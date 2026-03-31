import sqlite3
conn = sqlite3.connect('shop_db.db')
cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
conn.close()
print('Total tables:', len(tables))
for t in tables:
    print(' ', t)

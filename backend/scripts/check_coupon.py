import sqlite3
conn = sqlite3.connect('shop_db.db')
cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='coupons'")
print('coupons table:', 'exists' if cur.fetchone() else 'MISSING')
conn.close()

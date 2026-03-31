import sqlite3
conn = sqlite3.connect(r'C:\Users\Make\Desktop\shamgp\backend\shop_db.db')
cur = conn.cursor()
cur.execute("SELECT id, username, password, status, is_deleted FROM users WHERE username='testuser1'")
print("testuser1:", cur.fetchall())
conn.close()

import sqlite3
conn = sqlite3.connect(r'C:\Users\Make\Desktop\shamgp\backend\shop_db.db')
cur = conn.cursor()

# Check all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print("Tables:", tables)

# Check if role_menu table exists
print("\n--- role_menu ---")
try:
    cur.execute("SELECT * FROM role_menu LIMIT 3")
    print([dict(zip([d[0] for d in cur.description], r)) for r in cur.fetchall()])
except Exception as e:
    print("Error:", e)

# Check if role_permission table exists
print("\n--- role_permission ---")
try:
    cur.execute("SELECT * FROM role_permission LIMIT 3")
    print([dict(zip([d[0] for d in cur.description], r)) for r in cur.fetchall()])
except Exception as e:
    print("Error:", e)

# Check user_role
print("\n--- user_role ---")
try:
    cur.execute("SELECT * FROM user_role LIMIT 5")
    print([dict(zip([d[0] for d in cur.description], r)) for r in cur.fetchall()])
except Exception as e:
    print("Error:", e)

# Check users
print("\n--- users ---")
cur.execute("SELECT id, username, email, status FROM users LIMIT 5")
for r in cur.fetchall():
    print(r)

conn.close()

import sqlite3
conn = sqlite3.connect(r'C:\Users\Make\Desktop\shamgp\backend\shop_db.db')
cur = conn.cursor()

# Check roles for testuser1 (id=4)
cur.execute("SELECT * FROM user_role WHERE user_id=4")
print("user_role for user 4:", cur.fetchall())

# Check role details
cur.execute("SELECT * FROM role")
print("\nAll roles:")
for r in cur.fetchall():
    print(r)

# Check what the issue might be - does role 1 exist?
cur.execute("SELECT * FROM role WHERE id=1")
print("\nRole 1:", cur.fetchone())

# Check if there are any role records with no corresponding menus
cur.execute("SELECT r.id, r.name, COUNT(m.menu_id) as menu_count FROM role r LEFT JOIN role_menu m ON r.id = m.role_id GROUP BY r.id")
print("\nRole menu counts:")
for r in cur.fetchall():
    print(r)

conn.close()

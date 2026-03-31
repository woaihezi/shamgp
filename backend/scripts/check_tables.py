import sqlite3
conn = sqlite3.connect('shop_db.db')
cur = conn.cursor()

# 检查所有关联表
tables = ['user_role', 'user_role_association', 'role_permission']
for t in tables:
    try:
        cur.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{t}'")
        row = cur.fetchone()
        print(f'{t}: {row}')
    except Exception as e:
        print(f'{t} error: {e}')

conn.close()

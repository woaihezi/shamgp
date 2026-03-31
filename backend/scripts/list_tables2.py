import sqlite3, sys
conn = sqlite3.connect('shop_db.db')
cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
conn.close()
with open('tables_list.txt', 'w', encoding='utf-8') as f:
    f.write(f'Total tables: {len(tables)}\n')
    for t in tables:
        f.write(f'  {t}\n')
print('Done')

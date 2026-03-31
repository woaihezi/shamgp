import sqlite3, sys
conn = sqlite3.connect('shop_db.db')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print('Tables:', tables)
checks = {
    'shipping_rules': 'SELECT COUNT(*) FROM shipping_rules',
    'coupons': 'SELECT COUNT(*) FROM coupons',
    'favorites': 'SELECT COUNT(*) FROM favorites',
    'browse_histories': 'SELECT COUNT(*) FROM browse_histories',
    'order_status_logs': 'SELECT COUNT(*) FROM order_status_logs',
    'products': 'SELECT COUNT(*) FROM product_spus',
    'skus': 'SELECT COUNT(*) FROM product_skus',
}
for name, sql in checks.items():
    try:
        cur.execute(sql)
        print(f'{name}: {cur.fetchone()[0]}')
    except Exception as e:
        print(f'{name}: ERROR - {e}')
conn.close()

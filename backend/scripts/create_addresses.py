import sqlite3

conn = sqlite3.connect('shop_db.db')
conn.execute("""
CREATE TABLE IF NOT EXISTS addresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    consignee_name VARCHAR(50) NOT NULL,
    consignee_phone VARCHAR(20) NOT NULL,
    province VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    district VARCHAR(50) NOT NULL,
    detail_address VARCHAR(200) NOT NULL,
    zip_code VARCHAR(10),
    is_default BOOLEAN NOT NULL DEFAULT 0,
    is_deleted BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")
conn.commit()
print("addresses table created")

# Verify
cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='addresses'")
print("Table exists:", cur.fetchone() is not None)
conn.close()

import sqlite3

conn = sqlite3.connect("users.db", timeout=10)
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
)
''')

conn.commit()
conn.close()

print("DB created successfully 👍")
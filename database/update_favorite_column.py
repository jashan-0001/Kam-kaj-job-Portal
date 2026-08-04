import sqlite3
from config import DATABASE_PATH

conn = sqlite3.connect(DATABASE_PATH)

cursor = conn.cursor()

try:

    cursor.execute("""
        ALTER TABLE applications
        ADD COLUMN is_favorite INTEGER DEFAULT 0
    """)

    print("Favorite column added.")

except sqlite3.OperationalError:

    print("Column already exists.")

conn.commit()
conn.close()
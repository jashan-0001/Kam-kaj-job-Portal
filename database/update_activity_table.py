import sqlite3

from config import DATABASE_PATH

conn = sqlite3.connect(DATABASE_PATH)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS recruiter_activity (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    employer_id INTEGER NOT NULL,

    activity TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()

conn.close()

print("Recruiter Activity table created successfully.")
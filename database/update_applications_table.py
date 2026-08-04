import sqlite3
from config import DATABASE_PATH

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

columns = [

    ("ats_score", "INTEGER"),

    ("match_percentage", "REAL"),

    ("matched_skills", "TEXT"),

    ("missing_skills", "TEXT"),

    ("recommendation", "TEXT")

]

for column_name, column_type in columns:

    try:

        cursor.execute(
            f"""
            ALTER TABLE applications
            ADD COLUMN {column_name} {column_type}
            """
        )

        print(f"Added: {column_name}")

    except sqlite3.OperationalError:

        print(f"Already exists: {column_name}")

conn.commit()
conn.close()

print("\nDatabase Updated Successfully.")
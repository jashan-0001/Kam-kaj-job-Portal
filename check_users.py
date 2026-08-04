from database.database import fetch_all

users = fetch_all("""
SELECT id, full_name, email, role
FROM users
""")

for user in users:
    print(user)
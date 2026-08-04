import bcrypt

from database.database import execute_query

EMAIL = "admin@jobportal.com"
NEW_PASSWORD = "Admin@123"

hashed_password = bcrypt.hashpw(
    NEW_PASSWORD.encode("utf-8"),
    bcrypt.gensalt()
).decode("utf-8")

success = execute_query(
    """
    UPDATE users
    SET password = ?
    WHERE email = ?
    """,
    (
        hashed_password,
        EMAIL
    )
)

if success:
    print("✅ Password reset successful.")
    print("Email:", EMAIL)
    print("Password:", NEW_PASSWORD)
else:
    print("❌ Password reset failed.")
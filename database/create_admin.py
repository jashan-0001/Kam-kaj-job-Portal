import bcrypt
from database.database import fetch_one, execute_query

ADMIN_NAME = "Administrator"
ADMIN_EMAIL = "admin@jobportal.com"
ADMIN_PASSWORD = "Admin@123"
ADMIN_PHONE = "9999999999"


def create_admin():
    existing = fetch_one(
        "SELECT id FROM users WHERE email = ?",
        (ADMIN_EMAIL,)
    )

    if existing:
        return

    hashed_password = bcrypt.hashpw(
        ADMIN_PASSWORD.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    execute_query(
        """
        INSERT INTO users
        (
            full_name,
            email,
            password,
            role,
            phone,
            is_active
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            ADMIN_NAME,
            ADMIN_EMAIL,
            hashed_password,
            "Admin",
            ADMIN_PHONE,
            1
        )
    )

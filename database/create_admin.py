import bcrypt

from database.database import (
    fetch_one,
    execute_query
)


# =====================================================
# DEFAULT ADMIN
# =====================================================

ADMIN_NAME = "Administrator"

ADMIN_EMAIL = "admin@jobportal.com"

ADMIN_PASSWORD = "Admin@123"

ADMIN_PHONE = "9999999999"


# =====================================================
# HASH PASSWORD
# =====================================================

hashed_password = bcrypt.hashpw(
    ADMIN_PASSWORD.encode("utf-8"),
    bcrypt.gensalt()
).decode("utf-8")


# =====================================================
# CHECK EXISTING ADMIN
# =====================================================

def create_admin():
    existing = fetch_one(
        """
        SELECT id
        FROM users
        WHERE email = ?
        """,
        (ADMIN_EMAIL,)
    )

    if existing:
        return

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

    print("Admin account created successfully.")

    print("-----------------------------------")
    print(f"Email    : {ADMIN_EMAIL}")
    print(f"Password : {ADMIN_PASSWORD}")
    print("-----------------------------------")

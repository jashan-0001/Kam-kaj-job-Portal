import bcrypt

from database.database import (
    fetch_one,
    execute_query
)

from utils.logger import logger


# =====================================================
# DEFAULT ADMIN DETAILS
# =====================================================

ADMIN_NAME = "System Administrator"

ADMIN_EMAIL = "admin@portal.com"

ADMIN_PASSWORD = "Admin@123"

ADMIN_PHONE = "9999999999"

ADMIN_ROLE = "Admin"


# =====================================================
# CREATE DEFAULT ADMIN
# =====================================================

def create_default_admin():

    try:

        logger.info(
            "Checking for default admin account."
        )

        existing = fetch_one(
            """
            SELECT id
            FROM users
            WHERE email = ?
            """,
            (ADMIN_EMAIL,)
        )

        if existing:

            logger.info(
                "Default admin already exists."
            )

            print("✅ Default admin already exists.")

            return

        hashed_password = bcrypt.hashpw(
            ADMIN_PASSWORD.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        success = execute_query(
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
                ADMIN_ROLE,
                ADMIN_PHONE,
                1
            )
        )

        if success:

            logger.info(
                "Default admin account created successfully."
            )

            print("\n===================================")
            print(" Admin account created successfully")
            print("===================================")
            print(f"Email    : {ADMIN_EMAIL}")
            print(f"Password : {ADMIN_PASSWORD}")
            print("===================================\n")

        else:

            logger.error(
                "Failed to create default admin."
            )

            print("❌ Failed to create admin account.")

    except Exception:

        logger.exception(
            "Error while creating default admin."
        )

        print("❌ Unexpected error while creating admin.")


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    create_default_admin()

import bcrypt

from database.database import (
    fetch_one,
    execute_query
)

from utils.logger import logger


# ============================================================
# ADMIN CONFIGURATION
# ============================================================

ADMIN_NAME = "Administrator"

ADMIN_EMAIL = "admin@jobportal.com"

ADMIN_PASSWORD = "Admin@123"

ADMIN_PHONE = "9999999999"


# ============================================================
# CREATE ADMIN
# ============================================================

def create_admin():
    """
    Create the default administrator account
    if it does not already exist.
    """

    try:

        # ----------------------------------------------------
        # CHECK WHETHER ADMIN ALREADY EXISTS
        # ----------------------------------------------------

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
                "Administrator account already exists."
            )

            return True


        # ----------------------------------------------------
        # HASH ADMIN PASSWORD
        # ----------------------------------------------------

        hashed_password = bcrypt.hashpw(
            ADMIN_PASSWORD.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")


        # ----------------------------------------------------
        # INSERT ADMIN
        # ----------------------------------------------------

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
                "Admin",
                ADMIN_PHONE,
                1
            )
        )


        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        if success:

            logger.info(
                "Administrator account created successfully."
            )

            return True


        logger.error(
            "Failed to create administrator account."
        )

        return False


    except Exception:

        logger.exception(
            "create_admin() failed."
        )

        return False

from database.database import (
    execute_query,
    fetch_one
)

from services.auth import hash_password

from constants import ROLE_ADMIN

from utils.logger import logger


# ============================================================
# DEFAULT ADMIN CONFIGURATION
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
        # Check whether admin already exists
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
        # Hash administrator password
        # ----------------------------------------------------

        hashed_password = hash_password(
            ADMIN_PASSWORD
        )

        # ----------------------------------------------------
        # Insert administrator
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
                ROLE_ADMIN,
                ADMIN_PHONE,
                1
            )
        )

        # ----------------------------------------------------
        # Result
        # ----------------------------------------------------

        if success:

            logger.info(
                "Default administrator account created successfully."
            )

            return True

        logger.error(
            "Failed to create default administrator account."
        )

        return False

    except Exception:

        logger.exception(
            "Administrator creation failed."
        )

        return False

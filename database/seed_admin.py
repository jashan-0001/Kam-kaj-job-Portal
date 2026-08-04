import bcrypt

from database.database import execute_query, fetch_one


ADMIN_NAME = "Administrator"
ADMIN_EMAIL = "admin@kamkaj.com"
ADMIN_PASSWORD = "Admin@123"
ADMIN_PHONE = "9999999999"


def create_admin():

    existing = fetch_one(
        "SELECT id FROM users WHERE email = ?",
        (ADMIN_EMAIL,)
    )

    if existing:
        print("Admin already exists.")
        return

    hashed_password = bcrypt.hashpw(
        ADMIN_PASSWORD.encode(),
        bcrypt.gensalt()
    ).decode()

    success = execute_query(
        """
        INSERT INTO users
        (
            full_name,
            email,
            password,
            role,
            phone
        )
        VALUES
        (
            ?, ?, ?, ?, ?
        )
        """,
        (
            ADMIN_NAME,
            ADMIN_EMAIL,
            hashed_password,
            "Admin",
            ADMIN_PHONE
        )
    )

    if success:
        print("Admin created successfully.")
        print(f"Email    : {ADMIN_EMAIL}")
        print(f"Password : {ADMIN_PASSWORD}")
    else:
        print("Failed to create admin.")


if __name__ == "__main__":
    create_admin()

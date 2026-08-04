import bcrypt

from database.database import execute_query, fetch_one

from utils.logger import logger


# =====================================================
# PASSWORD FUNCTIONS
# =====================================================
# =====================================================

def hash_password(password):
    """Hash a plain text password using bcrypt."""
    try:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    except Exception:
        logger.exception("Password hashing failed.")
        raise


def verify_password(password, hashed_password):
    """Verify a password against its bcrypt hash."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        logger.exception("Password verification failed.")
        return False


# =====================================================
# REGISTER USER
# =====================================================
# =====================================================

def register_user(full_name, email, password, role, phone):
    """Register a new user."""
    try:
        full_name = full_name.strip()
        email = email.strip().lower()
        phone = phone.strip()

        logger.info("New user registration requested.")

        existing_user = fetch_one(
            """
            SELECT id
            FROM users
            WHERE email = ?
            """,
            (email,),
        )

        if existing_user:
            logger.warning("Registration blocked. Email already exists.")
            return False, "Email already registered.", None

        allowed_roles = ("Admin", "Employer", "Candidate")

        if role not in allowed_roles:
            logger.warning(f"Invalid role received: {role}")
            return False, "Invalid role selected.", None

        hashed_password = hash_password(password)

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
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                full_name,
                email,
                hashed_password,
                role,
                phone,
            ),
        )

        if success:
            user = fetch_one(
                """
                SELECT id
                FROM users
                WHERE email = ?
                """,
                (email,),
            )

            logger.info("User registered successfully.")
            return True, "Registration Successful.", user["id"]

        logger.error("Registration failed.")
        return False, "Registration Failed.", None

    except Exception:
        logger.exception("Registration service failed.")
        return False, "Registration Failed.", None


# =====================================================
# LOGIN USER
# =====================================================
# =====================================================

def login_user(email, password):
    """Authenticate user."""
    try:
        email = email.strip().lower()

        logger.info("Login attempt received.")

        user = fetch_one(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,),
        )

        # -----------------------------------------
        # Invalid User
        # -----------------------------------------
        if user is None:
            logger.warning("Login failed.")
            return False, "Invalid email or password.", None

        # -----------------------------------------
        # Disabled Account
        # -----------------------------------------
        if not user["is_active"]:
            logger.warning("Disabled account login attempt.")
            return (
                False,
                "Your account has been disabled. Please contact the administrator.",
                None,
            )

        # -----------------------------------------
        # Password Verification
        # -----------------------------------------
        if not verify_password(password, user["password"]):
            logger.warning("Login failed.")
            return False, "Invalid email or password.", None

        logger.info(f"User logged in successfully. User ID={user['id']}")
        return True, "Login Successful.", user

    except Exception:
        logger.exception("Login service failed.")
        return False, "Login Failed.", None


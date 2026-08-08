import bcrypt

from database.database import (
    execute_query,
    fetch_one
)

from utils.logger import logger


# =====================================================
# PASSWORD FUNCTIONS
# =====================================================

def hash_password(password):
    """
    Hash a plain text password using bcrypt.
    """

    try:

        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    except Exception:

        logger.exception(
            "Password hashing failed."
        )

        raise


def verify_password(password, hashed_password):
    """
    Verify a plain text password against
    a bcrypt password hash.
    """

    try:

        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )

    except Exception:

        logger.exception(
            "Password verification failed."
        )

        return False


# =====================================================
# REGISTER USER
# =====================================================

def register_user(
    full_name,
    email,
    password,
    role,
    phone
):
    """
    Register a new user.
    """

    try:

        # ---------------------------------------------
        # Clean input
        # ---------------------------------------------

        full_name = full_name.strip()
        email = email.strip().lower()
        phone = phone.strip()

        logger.info(
            "New user registration requested."
        )

        # ---------------------------------------------
        # Check existing email
        # ---------------------------------------------

        existing_user = fetch_one(
            """
            SELECT id
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        if existing_user:

            logger.warning(
                "Registration blocked. Email already exists."
            )

            return (
                False,
                "Email already registered.",
                None
            )

        # ---------------------------------------------
        # Validate role
        # ---------------------------------------------

        allowed_roles = (
            "Admin",
            "Employer",
            "Candidate"
        )

        if role not in allowed_roles:

            logger.warning(
                f"Invalid role received: {role}"
            )

            return (
                False,
                "Invalid role selected.",
                None
            )

        # ---------------------------------------------
        # Hash password
        # ---------------------------------------------

        hashed_password = hash_password(
            password
        )

        # ---------------------------------------------
        # Insert user
        # ---------------------------------------------

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
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                full_name,
                email,
                hashed_password,
                role,
                phone,
                1
            )
        )

        if not success:

            logger.error(
                "Registration failed."
            )

            return (
                False,
                "Registration Failed.",
                None
            )

        # ---------------------------------------------
        # Get newly created user
        # ---------------------------------------------

        user = fetch_one(
            """
            SELECT id
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        if user is None:

            logger.error(
                "User created but could not be retrieved."
            )

            return (
                False,
                "Registration Failed.",
                None
            )

        logger.info(
            f"User registered successfully. "
            f"User ID={user['id']}"
        )

        return (
            True,
            "Registration Successful.",
            user["id"]
        )

    except Exception:

        logger.exception(
            "Registration service failed."
        )

        return (
            False,
            "Registration Failed.",
            None
        )


# =====================================================
# LOGIN USER
# =====================================================

def login_user(
    email,
    password
):
    """
    Authenticate a user.
    """

    try:

        # ---------------------------------------------
        # Clean email
        # ---------------------------------------------

        email = email.strip().lower()

        logger.info(
            "Login attempt received."
        )

        # ---------------------------------------------
        # Find user
        # ---------------------------------------------

        user = fetch_one(
            """
            SELECT
                id,
                full_name,
                email,
                password,
                role,
                phone,
                created_at,
                is_active
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        # ---------------------------------------------
        # Invalid user
        # ---------------------------------------------

        if user is None:

            logger.warning(
                "Login failed. Invalid email."
            )

            return (
                False,
                "Invalid email or password.",
                None
            )

        # ---------------------------------------------
        # Disabled account
        # ---------------------------------------------

        if not user["is_active"]:

            logger.warning(
                f"Disabled account login attempt. "
                f"User ID={user['id']}"
            )

            return (
                False,
                "Your account has been disabled. "
                "Please contact the administrator.",
                None
            )

        # ---------------------------------------------
        # Password verification
        # ---------------------------------------------

        if not verify_password(
            password,
            user["password"]
        ):

            logger.warning(
                f"Login failed. "
                f"Invalid password for User ID={user['id']}"
            )

            return (
                False,
                "Invalid email or password.",
                None
            )

        # ---------------------------------------------
        # Successful login
        # ---------------------------------------------

        logger.info(
            f"User logged in successfully. "
            f"User ID={user['id']}"
        )

        return (
            True,
            "Login Successful.",
            user
        )

    except Exception:

        logger.exception(
            "Login service failed."
        )

        return (
            False,
            "Login Failed.",
            None
        ) 

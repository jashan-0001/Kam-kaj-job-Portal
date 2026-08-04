import re


def validate_name(name):
    """
    Validate full name.
    """
    name = name.strip()

    if len(name) < 3:
        return False, "Name must be at least 3 characters."

    if not all(ch.isalpha() or ch.isspace() for ch in name):
        return False, "Name should contain only letters and spaces."

    return True, ""


def validate_email(email):
    """
    Validate email format.
    """
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    if re.match(pattern, email):
        return True, ""

    return False, "Enter a valid email address."


def validate_phone(phone):
    """
    Validate Indian phone number.
    """
    if not phone.isdigit():
        return False, "Phone number must contain only digits."

    if len(phone) != 10:
        return False, "Phone number must be exactly 10 digits."

    if phone[0] not in "6789":
        return False, "Phone number should start with 6, 7, 8 or 9."

    return True, ""


def validate_password(password):
    """
    Validate password strength.
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain one uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain one lowercase letter."

    if not re.search(r"\d", password):
        return False, "Password must contain one number."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain one special character."

    return True, ""
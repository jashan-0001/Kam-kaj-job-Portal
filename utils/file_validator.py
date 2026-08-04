from pathlib import Path

from config import (
    ALLOWED_RESUME_EXTENSIONS,
    MAX_RESUME_SIZE
)


# =====================================================
# FILE EXTENSION
# =====================================================

def is_allowed_extension(filename):
    """
    Check whether the uploaded file has
    an allowed extension.
    """

    extension = Path(filename).suffix.lower().replace(".", "")

    return extension in ALLOWED_RESUME_EXTENSIONS


# =====================================================
# FILE SIZE
# =====================================================

def is_valid_file_size(uploaded_file):
    """
    Check whether the uploaded file
    is within the allowed size.
    """

    return uploaded_file.size <= MAX_RESUME_SIZE


# =====================================================
# VALIDATE RESUME
# =====================================================

def validate_resume(uploaded_file):
    """
    Validate uploaded resume.

    Returns:
        (True, "") if valid
        (False, error_message) otherwise
    """

    if uploaded_file is None:

        return (
            False,
            "Please upload a resume."
        )

    if not is_allowed_extension(
        uploaded_file.name
    ):

        return (
            False,
            "Only PDF resumes are allowed."
        )

    if not is_valid_file_size(
        uploaded_file
    ):

        return (
            False,
            "Resume size must not exceed 5 MB."
        )

    return (
        True,
        ""
    )
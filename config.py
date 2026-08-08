import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

# =====================================================
# BASE DIRECTORY
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


# =====================================================
# APPLICATION
# =====================================================

APP_NAME = "AI Job Portal"

DEBUG_MODE = True


# =====================================================
# DATABASE - OLD SQLITE PATH
# =====================================================

# Kept only for compatibility with any old code.
# The application now uses Supabase PostgreSQL.

DATABASE_DIR = Path("/tmp")

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATABASE_PATH = DATABASE_DIR / "jobportal.db"


# =====================================================
# POSTGRESQL / SUPABASE
# =====================================================

SUPABASE_DATABASE_URL = st.secrets.get(
    "SUPABASE_DATABASE_URL",
    os.getenv("SUPABASE_DATABASE_URL")
)

# =====================================================
# UPLOAD DIRECTORIES
# =====================================================

UPLOAD_DIR = BASE_DIR / "uploads"

RESUME_DIR = UPLOAD_DIR / "resumes"

LOGO_DIR = UPLOAD_DIR / "company_logos"

REPORT_DIR = UPLOAD_DIR / "reports"

EXPORT_DIR = UPLOAD_DIR / "exports"


# =====================================================
# CREATE DIRECTORIES
# =====================================================

for folder in [
    UPLOAD_DIR,
    RESUME_DIR,
    LOGO_DIR,
    REPORT_DIR,
    EXPORT_DIR
]:

    folder.mkdir(
        parents=True,
        exist_ok=True
    )


# =====================================================
# FILE UPLOAD SETTINGS
# =====================================================

ALLOWED_RESUME_EXTENSIONS = {
    "pdf"
}

MAX_RESUME_SIZE = 5 * 1024 * 1024


# =====================================================
# LOGGING
# =====================================================

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =====================================================
# GEMINI
# =====================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

try:

    import streamlit as st

    if "GEMINI_API_KEY" in st.secrets:

        GEMINI_API_KEY = st.secrets[
            "GEMINI_API_KEY"
        ]

except Exception:
    pass


# =====================================================
# EMAIL
# =====================================================

EMAIL_ADDRESS = os.getenv(
    "EMAIL_ADDRESS"
)

EMAIL_PASSWORD = os.getenv(
    "EMAIL_PASSWORD"
)

try:

    import streamlit as st

    if "EMAIL_ADDRESS" in st.secrets:

        EMAIL_ADDRESS = st.secrets[
            "EMAIL_ADDRESS"
        ]

    if "EMAIL_PASSWORD" in st.secrets:

        EMAIL_PASSWORD = st.secrets[
            "EMAIL_PASSWORD"
        ]

except Exception:
    pass

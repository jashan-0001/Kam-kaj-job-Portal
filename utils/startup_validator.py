import os
from pathlib import Path

import streamlit as st

from utils.logger import logger


def get_config_value(key: str):
    """
    Get configuration value from:
    1. Streamlit secrets
    2. Environment variables
    """

    # Streamlit Cloud / production
    try:
        if key in st.secrets:
            value = st.secrets[key]

            if value:
                return value

    except Exception:
        pass

    # Local .env / environment
    return os.getenv(key)


# ============================================================
# STARTUP VALIDATION
# ============================================================

def validate_startup():
    """
    Validate application configuration before startup.
    """

    required_config = [
        "SUPABASE_DATABASE_URL",
        "EMAIL_ADDRESS",
        "EMAIL_PASSWORD",
        "GEMINI_API_KEY",
    ]

    missing = []

    for key in required_config:

        value = get_config_value(key)

        if not value:
            missing.append(key)

    # --------------------------------------------------------
    # Missing configuration
    # --------------------------------------------------------

    if missing:

        logger.error(
            f"Missing configuration: {', '.join(missing)}"
        )

        raise RuntimeError(
            "Missing required configuration: "
            + ", ".join(missing)
        )

    # --------------------------------------------------------
    # Required folders
    # --------------------------------------------------------

    folders = [
        "uploads",
        "logs",
    ]

    for folder in folders:

        Path(folder).mkdir(
            parents=True,
            exist_ok=True
        )

    # --------------------------------------------------------
    # Validation successful
    # --------------------------------------------------------

    logger.info(
        "Startup validation completed successfully."
    )

import os
from pathlib import Path

from utils.logger import logger


def validate_startup():
    """
    Validate application configuration before startup.
    """

    required_env = [
        "EMAIL_ADDRESS",
        "EMAIL_PASSWORD",
        "GEMINI_API_KEY"
    ]

    missing = []

    for key in required_env:

        if not os.getenv(key):
            missing.append(key)

    if missing:

        logger.error(
            f"Missing environment variables: {', '.join(missing)}"
        )

        raise RuntimeError(
            f"Missing environment variables: {', '.join(missing)}"
        )

    folders = [
        "uploads",
        "logs"
    ]

    for folder in folders:

        Path(folder).mkdir(
            parents=True,
            exist_ok=True
        )

    logger.info(
        "Startup validation completed successfully."
    )
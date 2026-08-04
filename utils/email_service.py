import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import (
    EMAIL_ADDRESS,
    EMAIL_PASSWORD
)

from utils.logger import logger


# =====================================================
# SEND EMAIL
# =====================================================

def send_email(
    recipient,
    subject,
    body
):
    """
    Send an HTML email using Gmail SMTP.
    Returns True if successful, otherwise False.
    """

    try:

        logger.info(
            f"Sending email to {recipient}"
        )

        message = MIMEMultipart()

        message["From"] = EMAIL_ADDRESS
        message["To"] = recipient
        message["Subject"] = subject

        message.attach(
            MIMEText(body, "html")
        )

        with smtplib.SMTP(
            "smtp.gmail.com",
            587,
            timeout=30
        ) as server:

            server.starttls()

            server.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            server.send_message(message)

        logger.info(
            f"Email sent successfully to {recipient}"
        )

        return True

    except Exception:

        logger.exception(
            f"Failed to send email to {recipient}"
        )

        return False
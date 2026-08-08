from constants import (
    APPLICATION_SHORTLISTED,
    APPLICATION_INTERVIEW,
    APPLICATION_REJECTED,
)

from utils.email_service import send_email
from utils.logger import logger

from templates.shortlisted import shortlisted_template
from templates.interview import interview_template
from templates.rejected import rejected_template


# ============================================================
# SEND STATUS EMAIL
# ============================================================

def send_status_email(application, status):
    """
    Send an email to the candidate based on application status.

    Supported statuses:
        - Shortlisted
        - Interview Scheduled
        - Rejected

    Pending status does not send an email.
    """

    try:

        if not application:
            logger.error(
                "Cannot send status email: application data is missing."
            )
            return False

        candidate_name = application.get("full_name")
        recipient = application.get("email")
        job_title = application.get("title")

        if not recipient:
            logger.error(
                "Cannot send status email: candidate email is missing."
            )
            return False

        if not candidate_name:
            logger.error(
                "Cannot send status email: candidate name is missing."
            )
            return False

        if not job_title:
            logger.error(
                "Cannot send status email: job title is missing."
            )
            return False

        logger.info(
            f"Preparing {status} email for {recipient}"
        )

        # ====================================================
        # SHORTLISTED
        # ====================================================

        if status == APPLICATION_SHORTLISTED:

            subject = (
                f"Congratulations! Shortlisted for {job_title}"
            )

            body = shortlisted_template(
                candidate_name,
                job_title
            )

        # ====================================================
        # INTERVIEW
        # ====================================================

        elif status == APPLICATION_INTERVIEW:

            subject = (
                f"Interview Invitation - {job_title}"
            )

            body = interview_template(
                candidate_name,
                job_title
            )

        # ====================================================
        # REJECTED
        # ====================================================

        elif status == APPLICATION_REJECTED:

            subject = (
                f"Application Update - {job_title}"
            )

            body = rejected_template(
                candidate_name,
                job_title
            )

        # ====================================================
        # OTHER STATUS
        # ====================================================

        else:

            logger.info(
                f"No email required for application status: {status}"
            )

            return False

        # ====================================================
        # SEND EMAIL
        # ====================================================

        success = send_email(
            recipient=recipient,
            subject=subject,
            body=body
        )

        if success:

            logger.info(
                f"{status} email sent successfully "
                f"to {recipient}"
            )

        else:

            logger.error(
                f"Failed to send {status} email "
                f"to {recipient}"
            )

        return success

    except Exception:

        logger.exception(
            "Email notification service failed."
        )

        return False

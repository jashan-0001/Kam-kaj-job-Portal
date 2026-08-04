from utils.email_service import send_email
from utils.logger import logger

from templates.shortlisted import shortlisted_template
from templates.interview import interview_template
from templates.rejected import rejected_template


# =====================================================
# SEND STATUS EMAIL
# =====================================================

def send_status_email(
    application,
    status
):
    """
    Send an email based on application status.
    """

    try:

        candidate_name = application["full_name"]

        recipient = application["email"]

        job_title = application["title"]

        logger.info(
            f"Preparing {status} email for {recipient}"
        )

        if status == "Shortlisted":

            subject = (
                f"Congratulations! Shortlisted for {job_title}"
            )

            body = shortlisted_template(
                candidate_name,
                job_title
            )

        elif status == "Interview Scheduled":

            subject = (
                f"Interview Invitation - {job_title}"
            )

            body = interview_template(
                candidate_name,
                job_title
            )

        elif status == "Rejected":

            subject = (
                f"Application Update - {job_title}"
            )

            body = rejected_template(
                candidate_name,
                job_title
            )

        else:

            logger.warning(
                f"Unknown application status: {status}"
            )

            return False

        success = send_email(
            recipient=recipient,
            subject=subject,
            body=body
        )

        if success:

            logger.info(
                f"{status} email sent successfully to {recipient}"
            )

        else:

            logger.error(
                f"Failed to send {status} email to {recipient}"
            )

        return success

    except Exception:

        logger.exception(
            f"Email notification service failed for {application.get('email', 'Unknown User')}"
        )

        return False
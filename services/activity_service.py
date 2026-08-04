from database.database import (
    execute_query,
    fetch_all
)

from utils.logger import logger


# =====================================================
# ADD RECRUITER ACTIVITY
# =====================================================

def add_activity(
    employer_id,
    activity
):
    """
    Save recruiter activity.
    """

    try:

        query = """
        INSERT INTO recruiter_activity
        (
            employer_id,
            activity
        )
        VALUES (?, ?)
        """

        success = execute_query(
            query,
            (
                employer_id,
                activity
            )
        )

        if success:

            logger.info(
                f"Activity added for Employer ID {employer_id}"
            )

        else:

            logger.error(
                f"Failed to add activity for Employer ID {employer_id}"
            )

        return success

    except Exception:

        logger.exception(
            f"Activity service failed while adding activity for Employer ID {employer_id}"
        )

        return False


# =====================================================
# GET RECENT ACTIVITIES
# =====================================================

def get_recent_activity(
    employer_id
):
    """
    Return latest recruiter activities.
    """

    try:

        query = """
        SELECT *

        FROM recruiter_activity

        WHERE employer_id = ?

        ORDER BY created_at DESC

        LIMIT 15
        """

        activities = fetch_all(
            query,
            (employer_id,)
        )

        logger.info(
            f"Fetched {len(activities)} activities for Employer ID {employer_id}"
        )

        return activities

    except Exception:

        logger.exception(
            f"Failed to fetch recruiter activities for Employer ID {employer_id}"
        )

        return []
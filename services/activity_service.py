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

    Returns:
        bool: True if activity was saved successfully.
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
                f"Activity added successfully "
                f"for Employer ID={employer_id}"
            )

        else:

            logger.error(
                f"Failed to add activity "
                f"for Employer ID={employer_id}"
            )

        return success

    except Exception:

        logger.exception(
            f"Activity service failed while adding "
            f"activity for Employer ID={employer_id}"
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

    Returns:
        list[dict]
    """

    try:

        query = """
        SELECT
            id,
            employer_id,
            activity,
            created_at

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
            f"Fetched {len(activities)} activities "
            f"for Employer ID={employer_id}"
        )

        return activities

    except Exception:

        logger.exception(
            f"Failed to fetch recruiter activities "
            f"for Employer ID={employer_id}"
        )

        return []


# =====================================================
# GET ACTIVITY COUNT
# =====================================================

def get_activity_count(
    employer_id
):
    """
    Return total recruiter activities
    for an employer.
    """

    try:

        from database.database import fetch_one

        query = """
        SELECT
            COUNT(*) AS total

        FROM recruiter_activity

        WHERE employer_id = ?
        """

        row = fetch_one(
            query,
            (employer_id,)
        )

        return (
            row["total"]
            if row
            else 0
        )

    except Exception:

        logger.exception(
            f"Failed to calculate activity count "
            f"for Employer ID={employer_id}"
        )

        return 0

import streamlit as st

from database.database import (
    execute_query,
    fetch_all
)

from utils.logger import logger
from utils.cache_manager import clear_cache


# =====================================================
# CREATE NOTIFICATION
# =====================================================

def create_notification(
    user_id,
    title,
    message,
    notification_type="info"
):
    """
    Create a notification for a user.

    Returns:
        bool: True if notification was created successfully.
    """

    try:

        query = """
        INSERT INTO notifications
        (
            user_id,
            title,
            message,
            type,
            is_read
        )
        VALUES (?, ?, ?, ?, ?)
        """

        success = execute_query(
            query,
            (
                user_id,
                title,
                message,
                notification_type,
                0
            )
        )

        if success:

            clear_cache()

            logger.info(
                f"Notification created successfully "
                f"for User ID={user_id}"
            )

        else:

            logger.error(
                f"Failed to create notification "
                f"for User ID={user_id}"
            )

        return success

    except Exception:

        logger.exception(
            f"Notification service failed "
            f"for User ID={user_id}"
        )

        return False


# =====================================================
# GET USER NOTIFICATIONS
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_notifications(
    user_id
):
    """
    Return all notifications for a user.
    """

    try:

        query = """
        SELECT

            id,
            user_id,
            title,
            message,
            type,
            is_read,
            created_at

        FROM notifications

        WHERE user_id = ?

        ORDER BY created_at DESC
        """

        notifications = fetch_all(
            query,
            (user_id,)
        )

        logger.info(
            f"Fetched {len(notifications)} notifications "
            f"for User ID={user_id}"
        )

        return notifications

    except Exception:

        logger.exception(
            f"Failed to fetch notifications "
            f"for User ID={user_id}"
        )

        return []


# =====================================================
# GET UNREAD NOTIFICATION COUNT
# =====================================================

@st.cache_data(
    ttl=30,
    show_spinner=False
)
def get_unread_notification_count(
    user_id
):
    """
    Return number of unread notifications
    for a user.
    """

    try:

        query = """
        SELECT
            COUNT(*) AS total

        FROM notifications

        WHERE user_id = ?

        AND is_read = 0
        """

        from database.database import fetch_one

        row = fetch_one(
            query,
            (user_id,)
        )

        return (
            row["total"]
            if row
            else 0
        )

    except Exception:

        logger.exception(
            f"Failed to calculate unread "
            f"notifications for User ID={user_id}"
        )

        return 0


# =====================================================
# MARK SINGLE NOTIFICATION AS READ
# =====================================================

def mark_as_read(
    notification_id
):
    """
    Mark one notification as read.
    """

    try:

        query = """
        UPDATE notifications

        SET is_read = 1

        WHERE id = ?
        """

        success = execute_query(
            query,
            (notification_id,)
        )

        if success:

            clear_cache()

            logger.info(
                f"Notification {notification_id} "
                f"marked as read."
            )

        else:

            logger.error(
                f"Failed to mark notification "
                f"{notification_id} as read."
            )

        return success

    except Exception:

        logger.exception(
            f"Failed while marking notification "
            f"{notification_id} as read."
        )

        return False


# =====================================================
# MARK ALL NOTIFICATIONS AS READ
# =====================================================

def mark_all_read(
    user_id
):
    """
    Mark all notifications for a user as read.
    """

    try:

        query = """
        UPDATE notifications

        SET is_read = 1

        WHERE user_id = ?

        AND is_read = 0
        """

        success = execute_query(
            query,
            (user_id,)
        )

        if success:

            clear_cache()

            logger.info(
                f"All notifications marked as read "
                f"for User ID={user_id}"
            )

        else:

            logger.error(
                f"Failed to mark notifications as read "
                f"for User ID={user_id}"
            )

        return success

    except Exception:

        logger.exception(
            f"Failed while marking all notifications "
            f"for User ID={user_id}"
        )

        return False


# =====================================================
# DELETE NOTIFICATION
# =====================================================

def delete_notification(
    notification_id
):
    """
    Delete a notification.
    """

    try:

        query = """
        DELETE FROM notifications

        WHERE id = ?
        """

        success = execute_query(
            query,
            (notification_id,)
        )

        if success:

            clear_cache()

            logger.info(
                f"Notification {notification_id} deleted."
            )

        else:

            logger.error(
                f"Failed to delete notification "
                f"{notification_id}."
            )

        return success

    except Exception:

        logger.exception(
            f"Failed while deleting notification "
            f"{notification_id}"
        )

        return False

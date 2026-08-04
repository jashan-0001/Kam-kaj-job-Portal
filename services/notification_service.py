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
    """

    try:

        query = """
        INSERT INTO notifications
        (
            user_id,
            title,
            message,
            type
        )
        VALUES (?, ?, ?, ?)
        """

        success = execute_query(
            query,
            (
                user_id,
                title,
                message,
                notification_type
            )
        )

        if success:

            clear_cache()

            logger.info(
                f"Notification created for User ID {user_id}"
            )

        else:

            logger.error(
                f"Failed to create notification for User ID {user_id}"
            )

        return success

    except Exception:

        logger.exception(
            f"Notification service failed for User ID {user_id}"
        )

        return False


# =====================================================
# GET USER NOTIFICATIONS
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_notifications(user_id):
    """
    Return all notifications for a user.
    """

    try:

        query = """
        SELECT *

        FROM notifications

        WHERE user_id = ?

        ORDER BY created_at DESC
        """

        notifications = fetch_all(
            query,
            (user_id,)
        )

        logger.info(
            f"Fetched {len(notifications)} notifications for User ID {user_id}"
        )

        return notifications

    except Exception:

        logger.exception(
            f"Failed to fetch notifications for User ID {user_id}"
        )

        return []


# =====================================================
# MARK SINGLE NOTIFICATION AS READ
# =====================================================

def mark_as_read(notification_id):
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
                f"Notification {notification_id} marked as read."
            )

        else:

            logger.error(
                f"Failed to mark notification {notification_id} as read."
            )

        return success

    except Exception:

        logger.exception(
            f"Failed while marking notification {notification_id} as read."
        )

        return False


# =====================================================
# MARK ALL NOTIFICATIONS AS READ
# =====================================================

def mark_all_read(user_id):
    """
    Mark all notifications for a user as read.
    """

    try:

        query = """
        UPDATE notifications

        SET is_read = 1

        WHERE user_id = ?
        """

        success = execute_query(
            query,
            (user_id,)
        )

        if success:

            clear_cache()

            logger.info(
                f"All notifications marked as read for User ID {user_id}"
            )

        else:

            logger.error(
                f"Failed to mark notifications as read for User ID {user_id}"
            )

        return success

    except Exception:

        logger.exception(
            f"Failed while marking all notifications for User ID {user_id}"
        )

        return False


# =====================================================
# DELETE NOTIFICATION
# =====================================================

def delete_notification(notification_id):
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
                f"Failed to delete notification {notification_id}."
            )

        return success

    except Exception:

        logger.exception(
            f"Failed while deleting notification {notification_id}"
        )

        return False
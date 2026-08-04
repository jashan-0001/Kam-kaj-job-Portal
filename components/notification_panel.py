import streamlit as st

from services.notification_service import (
    get_notifications,
    mark_as_read,
    delete_notification
)


def show_notification_panel(user_id):
    """
    Display candidate notifications.
    """

    notifications = get_notifications(user_id)

    unread = sum(
        1
        for notification in notifications
        if notification["is_read"] == 0
    )

    st.subheader(
        f"🔔 Notifications ({unread} unread)"
    )

    if not notifications:
        st.info("No notifications available.")
        return

    for notification in notifications:

        with st.container():

            if notification["type"] == "success":

                st.success(
                    f"**{notification['title']}**\n\n"
                    f"{notification['message']}"
                )

            elif notification["type"] == "error":

                st.error(
                    f"**{notification['title']}**\n\n"
                    f"{notification['message']}"
                )

            elif notification["type"] == "warning":

                st.warning(
                    f"**{notification['title']}**\n\n"
                    f"{notification['message']}"
                )

            else:

                st.info(
                    f"**{notification['title']}**\n\n"
                    f"{notification['message']}"
                )

            st.caption(notification["created_at"])

            col1, col2 = st.columns(2)

            with col1:

                if (
                    notification["is_read"] == 0
                    and st.button(
                        "✅ Mark Read",
                        key=f"read_{notification['id']}"
                    )
                ):

                    mark_as_read(
                        notification["id"]
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{notification['id']}"
                ):

                    delete_notification(
                        notification["id"]
                    )

                    st.rerun()

            st.divider()
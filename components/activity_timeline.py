import streamlit as st

from services.activity_service import (
    get_recent_activity
)


def show_activity_timeline(
    employer_id
):

    activities = get_recent_activity(
        employer_id
    )

    st.subheader("📋 Recent Activity")

    if not activities:

        st.info(
            "No recent activity."
        )

        return

    for item in activities:

        st.markdown(
            f"""
### {item['activity']}

🕒 {item['created_at']}
"""
        )

        st.divider()
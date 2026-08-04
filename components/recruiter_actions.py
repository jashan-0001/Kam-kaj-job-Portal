import streamlit as st

from services.application_services import (
    update_application_status
)


def show_recruiter_actions(application):

    st.subheader(
        "📋 Recruiter Actions"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "🟢 Shortlist",
            key=f"shortlist_{application['id']}"
        ):

            update_application_status(
                application["id"],
                "Shortlisted"
            )

            st.rerun()

    with col2:

        if st.button(
            "📅 Interview",
            key=f"interview_{application['id']}"
        ):

            update_application_status(
                application["id"],
                "Interview Scheduled"
            )

            st.rerun()

    with col3:

        if st.button(
            "❌ Reject",
            key=f"reject_{application['id']}"
        ):

            update_application_status(
                application["id"],
                "Rejected"
            )

            st.rerun()
import streamlit as st

from services.application_services import (
    get_candidate_applications
)

from components.ai_report import (
    show_ai_report
)


def show_candidate_ai_dashboard(candidate_id):

    applications = get_candidate_applications(
        candidate_id
    )

    if not applications:

        st.info(
            "You haven't applied for any jobs yet."
        )
        return

    st.header("📊 My AI Resume Reports")

    for application in applications:

        with st.expander(
            f"{application['title']} | {application['company']}"
        ):
            show_ai_report(application)
import streamlit as st

from services.application_services import (
    get_my_applications
)


def show_candidate_dashboard_cards(user_id):

    applications = get_my_applications(user_id)

    total = len(applications)

    shortlisted = len(
        [
            app
            for app in applications
            if app["status"] == "Shortlisted"
        ]
    )

    hired = len(
        [
            app
            for app in applications
            if app["status"] == "Hired"
        ]
    )

    pending = len(
        [
            app
            for app in applications
            if app["status"] == "Pending"
        ]
    )

    st.subheader("📊 Dashboard")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "📄 Applications",
            total
        )

    with col2:

        st.metric(
            "⭐ Shortlisted",
            shortlisted
        )

    col3, col4 = st.columns(2)

    with col3:

        st.metric(
            "🟢 Pending",
            pending
        )

    with col4:

        st.metric(
            "🎉 Hired",
            hired
        )
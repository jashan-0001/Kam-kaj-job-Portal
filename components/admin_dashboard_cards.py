import streamlit as st

from services.admin_service import (
    get_admin_statistics
)


def show_admin_dashboard_cards():

    stats = get_admin_statistics()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "👥 Total Users",
            stats["users"]
        )

    with col2:
        st.metric(
            "🧑 Candidates",
            stats["candidates"]
        )

    with col3:
        st.metric(
            "🏢 Employers",
            stats["employers"]
        )

    col4, col5 = st.columns(2)

    with col4:
        st.metric(
            "💼 Jobs",
            stats["jobs"]
        )

    with col5:
        st.metric(
            "📄 Applications",
            stats["applications"]
        )
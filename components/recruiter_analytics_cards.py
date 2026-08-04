import streamlit as st

from services.analytics_service import (
    get_recruiter_statistics
)


def show_recruiter_analytics_cards(employer_id):
    """
    Display recruiter analytics cards.
    """

    stats = get_recruiter_statistics(employer_id)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📌 Total Jobs",
            stats["total_jobs"]
        )

    with col2:
        st.metric(
            "📄 Applications",
            stats["total_applications"]
        )

    with col3:
        st.metric(
            "📊 Average ATS",
            stats["average_ats"]
        )

    with col4:
        st.metric(
            "🏆 Best ATS",
            stats["best_ats"]
        )
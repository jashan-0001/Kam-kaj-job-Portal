import streamlit as st

from services.job_service import (
    total_jobs,
    total_open_jobs,
    total_closed_jobs
)

from services.application_services import (
    total_applications
)


def show_dashboard_cards(user_id):

    try:
        jobs = total_jobs(user_id)
        st.write("✅ total_jobs OK:", jobs)
    except Exception as e:
        st.error(f"total_jobs failed: {e}")
        return

    try:
        open_jobs = total_open_jobs(user_id)
        st.write("✅ total_open_jobs OK:", open_jobs)
    except Exception as e:
        st.error(f"total_open_jobs failed: {e}")
        return

    try:
        closed_jobs = total_closed_jobs(user_id)
        st.write("✅ total_closed_jobs OK:", closed_jobs)
    except Exception as e:
        st.error(f"total_closed_jobs failed: {e}")
        return

    try:
        applications = total_applications(user_id)
        st.write("✅ total_applications OK:", applications)
    except Exception as e:
        st.error(f"total_applications failed: {e}")
        return

    st.subheader("📊 Dashboard Statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("💼 Jobs Posted", jobs)

    with col2:
        st.metric("📄 Applications", applications)

    col3, col4 = st.columns(2)

    with col3:
        st.metric("🟢 Open Jobs", open_jobs)

    with col4:
        st.metric("🔴 Closed Jobs", closed_jobs)
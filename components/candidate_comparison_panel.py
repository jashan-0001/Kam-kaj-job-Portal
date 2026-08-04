import streamlit as st

from services.application_services import (
    get_applications_by_job
)

from components.candidate_comparison import (
    show_candidate_comparison
)


def show_candidate_comparison_panel(job_id):
    """
    Display a candidate comparison panel for one job.
    """

    applications = get_applications_by_job(job_id)

    if len(applications) < 2:
        st.info("At least two applications are required to compare candidates.")
        return

    st.subheader("⚖️ Compare Candidates")

    application_map = {
        f"{app['full_name']} ({app['ats_score']}/100)": app
        for app in applications
    }

    options = list(application_map.keys())

    col1, col2 = st.columns(2)

    with col1:
        candidate_a = st.selectbox(
            "Candidate A",
            options,
            key=f"candidate_a_{job_id}"
        )

    with col2:
        candidate_b = st.selectbox(
            "Candidate B",
            options,
            index=1,
            key=f"candidate_b_{job_id}"
        )

    if candidate_a == candidate_b:
        st.warning("Please select two different candidates.")
        return

    if st.button(
        "🔍 Compare Candidates",
        key=f"compare_{job_id}",
        use_container_width=True
    ):
        show_candidate_comparison(
            application_map[candidate_a],
            application_map[candidate_b]
        )
import streamlit as st

from constants import ROLE_EMPLOYER

from components.dashboard_cards import show_dashboard_cards
from components.recruiter_analytics_cards import (
    show_recruiter_analytics_cards
)
from components.recruiter_charts import (
    show_ats_chart,
    show_recommendation_chart,
    show_job_chart
)
from components.post_job_form import (
    show_post_job_form
)
from components.job_management import (
    show_job_management
)
from components.employer_applications import (
    show_employer_applications
)
from components.application_management import (
    show_application_management
)
from components.activity_timeline import (
    show_activity_timeline
)

from services.job_service import (
    get_jobs_by_employer
)

from utils.logger import logger


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Employer Dashboard",
    page_icon="🏢",
    layout="wide"
)


# ==========================================================
# DASHBOARD
# ==========================================================

try:

    # ==========================================================
    # AUTHENTICATION
    # ==========================================================

    if not st.session_state.get("logged_in"):
        st.switch_page("app.py")

    if st.session_state.get("role") != ROLE_EMPLOYER:

        logger.warning(
            "Unauthorized access attempt to Employer Dashboard."
        )

        st.error("Access Denied")

        st.stop()

    # ==========================================================
    # SESSION VARIABLES
    # ==========================================================

    user_id = st.session_state["user_id"]

    user_name = st.session_state["name"]

    logger.info(
        f"Employer Dashboard opened by {user_name} (ID={user_id})"
    )

    # ==========================================================
    # HEADER
    # ==========================================================

    st.title("🏢 Employer Dashboard")

    st.success(
        f"Welcome, {user_name}"
    )

    # ==========================================================
    # DASHBOARD
    # ==========================================================

    with st.expander(
        "📊 Dashboard Statistics",
        expanded=True
    ):

        show_dashboard_cards(user_id)

    # ==========================================================
    # ANALYTICS
    # ==========================================================

    with st.expander(
        "📈 Recruiter Analytics",
        expanded=False
    ):

        show_recruiter_analytics_cards(user_id)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            show_ats_chart(user_id)

        with col2:
            show_recommendation_chart(user_id)

        st.divider()

        show_job_chart(user_id)

    # ==========================================================
    # POST JOB
    # ==========================================================

    with st.expander(
        "➕ Post New Job",
        expanded=False
    ):

        show_post_job_form(user_id)

    # ==========================================================
    # MY JOBS
    # ==========================================================

    with st.expander(
        "📋 My Posted Jobs",
        expanded=False
    ):

        jobs = get_jobs_by_employer(user_id)

        if not jobs:

            st.info(
                "You haven't posted any jobs yet."
            )

        else:

            for job in jobs:

                with st.expander(
                    f"{job['title']} | {job['company']}"
                ):

                    st.write(
                        f"📍 {job['location']}"
                    )

                    st.write(
                        f"💰 {job['salary']}"
                    )

                    st.write(
                        f"💼 {job['experience']}"
                    )

                    st.write(
                        f"🛠 {job['skills']}"
                    )

                    if st.button(
                        "View Applications",
                        key=f"job_{job['id']}"
                    ):

                        st.session_state["selected_job"] = job["id"]

    # ==========================================================
    # APPLICATIONS
    # ==========================================================

    if "selected_job" in st.session_state:

        with st.expander(
            "📥 Applications",
            expanded=True
        ):

            show_employer_applications(
                st.session_state["selected_job"]
            )

    # ==========================================================
    # JOB MANAGEMENT
    # ==========================================================

    with st.expander(
        "⚙ Job Management",
        expanded=False
    ):

        show_job_management(user_id)

    # ==========================================================
    # APPLICATION MANAGEMENT
    # ==========================================================

    with st.expander(
        "📑 Application Management",
        expanded=False
    ):

        show_application_management(user_id)

    # ==========================================================
    # ACTIVITY
    # ==========================================================

    with st.expander(
        "📝 Recent Recruiter Activity",
        expanded=False
    ):

        show_activity_timeline(user_id)

    # ==========================================================
    # LOGOUT
    # ==========================================================

    if st.button(
        "Logout",
        use_container_width=True
    ):

        logger.info(
            f"Employer {user_name} (ID={user_id}) logged out."
        )

        st.session_state.clear()

        st.switch_page("app.py")


# ==========================================================
# ERROR HANDLING
# ==========================================================
except Exception:

    logger.exception(
        "Employer Dashboard crashed."
    )

    st.error(
        "Something went wrong while loading the dashboard. Please refresh the page and try again."
    )

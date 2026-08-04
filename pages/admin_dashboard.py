import streamlit as st
import pandas as pd

from services.admin_service import (
    get_admin_statistics,
    get_all_users,
    get_all_jobs,
    get_all_applications,
    delete_user,
    delete_job,
    delete_application_admin,
    toggle_user_status
)

from utils.logger import logger


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🛡️",
    layout="wide"
)


# =====================================================
# AUTHENTICATION
# =====================================================

if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

if st.session_state.get("role") != "Admin":

    st.error("Access Denied")

    st.stop()


logger.info("Admin Dashboard opened.")


# =====================================================
# HEADER
# =====================================================

st.title("🛡️ Admin Dashboard")

st.divider()


# =====================================================
# DASHBOARD CARDS
# =====================================================

stats = get_admin_statistics()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Users",
    stats["users"]
)

col2.metric(
    "Candidates",
    stats["candidates"]
)

col3.metric(
    "Employers",
    stats["employers"]
)

col4.metric(
    "Jobs",
    stats["jobs"]
)

col5.metric(
    "Applications",
    stats["applications"]
)


# =====================================================
# USER MANAGEMENT
# =====================================================

with st.expander(
    "👥 User Management",
    expanded=True
):

    users = get_all_users()

    if users:

        df = pd.DataFrame(users)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        selected_user = st.selectbox(
            "Select User",
            df["id"]
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Enable / Disable User",
                use_container_width=True
            ):

                if toggle_user_status(selected_user):

                    st.success("User updated.")

                    st.rerun()

        with col2:

            if st.button(
                "Delete User",
                use_container_width=True
            ):

                if delete_user(selected_user):

                    st.success("User deleted.")

                    st.rerun()

    else:

        st.info("No users found.")


# =====================================================
# JOB MANAGEMENT
# =====================================================

with st.expander(
    "💼 Job Management"
):

    jobs = get_all_jobs()

    if jobs:

        df = pd.DataFrame(jobs)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        selected_job = st.selectbox(
            "Select Job",
            df["id"],
            key="admin_job"
        )

        if st.button(
            "Delete Job",
            use_container_width=True
        ):

            if delete_job(selected_job):

                st.success(
                    "Job deleted."
                )

                st.rerun()

    else:

        st.info("No jobs found.")


# =====================================================
# APPLICATION MANAGEMENT
# =====================================================

with st.expander(
    "📄 Application Management"
):

    applications = get_all_applications()

    if applications:

        df = pd.DataFrame(applications)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        selected_application = st.selectbox(
            "Select Application",
            df["id"],
            key="admin_application"
        )

        if st.button(
            "Delete Application",
            use_container_width=True
        ):

            if delete_application_admin(
                selected_application
            ):

                st.success(
                    "Application deleted."
                )

                st.rerun()

    else:

        st.info("No applications found.")


# =====================================================
# LOGOUT
# =====================================================

st.divider()

if st.button(
    "Logout",
    use_container_width=True
):

    logger.info(
        "Admin logged out."
    )

    st.session_state.clear()

    st.switch_page("app.py")
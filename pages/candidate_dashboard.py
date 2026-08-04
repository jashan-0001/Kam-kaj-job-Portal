import streamlit as st

from constants import ROLE_CANDIDATE

from components.browse_jobs import (
    show_browse_jobs
)

from components.candidate_ai_dashboard import (
    show_candidate_ai_dashboard
)

from components.notification_panel import (
    show_notification_panel
)

from utils.logger import logger


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Candidate Dashboard",
    page_icon="👨‍💻",
    layout="wide"
)


# =====================================================
# DASHBOARD
# =====================================================

try:

    # =====================================================
    # AUTHENTICATION
    # =====================================================

    if not st.session_state.get("logged_in"):
        st.switch_page("app.py")

    if st.session_state.get("role") != ROLE_CANDIDATE:

        logger.warning(
            "Unauthorized access attempt to Candidate Dashboard."
        )

        st.error("Access Denied")

        st.stop()

    # =====================================================
    # SESSION VARIABLES
    # =====================================================

    user_id = st.session_state["user_id"]

    user_name = st.session_state["name"]

    logger.info(
        f"Candidate Dashboard opened by {user_name} (ID={user_id})"
    )


    # =====================================================
    # HEADER
    # =====================================================

    st.title("👨‍💻 Candidate Dashboard")

    st.success(
        f"Welcome, {user_name}"
    )


    # =====================================================
    # NOTIFICATIONS
    # =====================================================

    with st.expander(
        "🔔 Notifications",
        expanded=False
    ):

        show_notification_panel(user_id)


    # =====================================================
    # BROWSE JOBS
    # =====================================================

    with st.expander(
        "💼 Browse Jobs",
        expanded=True
    ):

        show_browse_jobs()


    # =====================================================
    # AI DASHBOARD
    # =====================================================

    with st.expander(
        "🤖 AI Resume Dashboard",
        expanded=False
    ):

        show_candidate_ai_dashboard(user_id)


    # =====================================================
    # LOGOUT
    # =====================================================

    if st.button(
        "Logout",
        use_container_width=True
    ):

        logger.info(
            f"Candidate {user_name} (ID={user_id}) logged out."
        )

        st.session_state.clear()

        st.switch_page("app.py")


# =====================================================
# ERROR HANDLING
# =====================================================

except Exception:

    logger.exception(
        "Candidate Dashboard crashed."
    )

    st.error(
        "Something went wrong while loading your dashboard. Please refresh the page and try again."
    )
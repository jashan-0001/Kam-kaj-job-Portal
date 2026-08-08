import streamlit as st

from utils.startup_validator import validate_startup
from utils.error_handler import handle_exception

from database.init_db import create_tables
from database.create_admin import create_admin


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Job Portal",
    page_icon="💼",
    layout="wide"
)


# ============================================================
# START APPLICATION
# ============================================================

try:

    # ========================================================
    # VALIDATE APPLICATION CONFIGURATION
    # ========================================================

    validate_startup()

    # ========================================================
    # DATABASE INITIALIZATION
    # ========================================================

    create_tables()

    # ========================================================
    # CREATE DEFAULT ADMIN
    # ========================================================

    create_admin()

    # ========================================================
    # USER NOT LOGGED IN
    # ========================================================

    if not st.session_state.get(
        "logged_in",
        False
    ):

        st.title(
            "💼 Kam - Kaj Job Portal"
        )

        st.write(
            "Welcome to Kam - Kaj Job Portal"
        )

        st.divider()

        col1, col2 = st.columns(2)

        # ----------------------------------------------------
        # LOGIN
        # ----------------------------------------------------

        with col1:

            if st.button(
                "🔑 Login",
                use_container_width=True
            ):

                st.switch_page(
                    "pages/login.py"
                )

        # ----------------------------------------------------
        # REGISTER
        # ----------------------------------------------------

        with col2:

            if st.button(
                "📝 Register",
                use_container_width=True
            ):

                st.switch_page(
                    "pages/register.py"
                )

    # ========================================================
    # LOGGED IN
    # ========================================================

    else:

        role = st.session_state.get(
            "role"
        )

        # ----------------------------------------------------
        # CANDIDATE
        # ----------------------------------------------------

        if role == "Candidate":

            st.switch_page(
                "pages/candidate_dashboard.py"
            )

        # ----------------------------------------------------
        # EMPLOYER
        # ----------------------------------------------------

        elif role == "Employer":

            st.switch_page(
                "pages/employer_dashboard.py"
            )

        # ----------------------------------------------------
        # ADMIN
        # ----------------------------------------------------

        elif role == "Admin":

            st.switch_page(
                "pages/admin_dashboard.py"
            )

        # ----------------------------------------------------
        # INVALID ROLE
        # ----------------------------------------------------

        else:

            st.error(
                "Invalid user role."
            )

            # Clear invalid login state
            st.session_state.clear()

            st.rerun()


# ============================================================
# GLOBAL ERROR HANDLING
# ============================================================

except Exception as e:

    handle_exception(e)

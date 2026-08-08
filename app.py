import streamlit as st
from dotenv import load_dotenv

from config import BASE_DIR

from utils.startup_validator import validate_startup
from utils.error_handler import handle_exception

from database.init_db import create_tables
from database.create_admin import create_admin


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv(BASE_DIR / ".env")


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

    # --------------------------------------------------------
    # 1. Validate configuration
    # --------------------------------------------------------

    validate_startup()

    # --------------------------------------------------------
    # 2. Initialize Supabase PostgreSQL database
    # --------------------------------------------------------

    create_tables()

    # --------------------------------------------------------
    # 3. Create default administrator
    # --------------------------------------------------------

    create_admin()

    # --------------------------------------------------------
    # 4. User not logged in
    # --------------------------------------------------------

    if not st.session_state.get("logged_in", False):

        st.title("💼 Kam - Kaj Job Portal")

        st.write(
            "Welcome to Kam - Kaj Job Portal"
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "🔑 Login",
                use_container_width=True
            ):

                st.switch_page(
                    "pages/login.py"
                )

        with col2:

            if st.button(
                "📝 Register",
                use_container_width=True
            ):

                st.switch_page(
                    "pages/register.py"
                )

    # --------------------------------------------------------
    # 5. Logged in
    # --------------------------------------------------------

    else:

        role = st.session_state.get("role")

        if role == "Candidate":

            st.switch_page(
                "pages/candidate_dashboard.py"
            )

        elif role == "Employer":

            st.switch_page(
                "pages/employer_dashboard.py"
            )

        elif role == "Admin":

            # Change this path if your admin page
            # has a different filename.
            st.switch_page(
                "pages/admin_dashboard.py"
            )

        else:

            st.error(
                "Invalid user role."
            )

except Exception as e:

    handle_exception(e)

import streamlit as st
from dotenv import load_dotenv

from utils.startup_validator import validate_startup
from utils.error_handler import handle_exception

# =====================================================
# LOAD ENVIRONMENT
# =====================================================

load_dotenv()

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Job Portal",
    page_icon="💼",
    layout="wide"
)

# =====================================================
# START APPLICATION
# =====================================================

try:

    # Validate application configuration
    validate_startup()

    # -----------------------------------------------
    # User not logged in
    # -----------------------------------------------

    if "logged_in" not in st.session_state:

        st.title("💼 Kam - Kaj Job Portal")

        st.write(
            "Welcome to kam - kaj Job Portal"
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

    # -----------------------------------------------
    # Logged in
    # -----------------------------------------------

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

        else:

            st.error(
                "Invalid user role."
            )

except Exception as e:

    import traceback

    st.error(str(e))

    st.code(traceback.format_exc())

    raise

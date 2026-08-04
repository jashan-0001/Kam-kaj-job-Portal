import streamlit as st

from utils.auth import login_user
from utils.logger import logger

from services.audit_service import log_activity


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Login",
    page_icon="🔑",
    layout="centered"
)


# =====================================================
# PAGE
# =====================================================

st.title("🔑 Login")


# =====================================================
# INPUTS
# =====================================================

email = st.text_input(
    "Email"
).strip().lower()


password = st.text_input(
    "Password",
    type="password"
)


# =====================================================
# LOGIN
# =====================================================

if st.button(
    "Login",
    use_container_width=True
):

    # -----------------------------
    # Validation
    # -----------------------------

    if not email:

        st.warning(
            "Please enter your email."
        )

        st.stop()


    if not password:

        st.warning(
            "Please enter your password."
        )

        st.stop()


    try:

        logger.info(
            "Login button clicked."
        )


        with st.spinner(
            "Signing in..."
        ):


            success, message, user = login_user(
                email,
                password
            )



        # =====================================================
        # LOGIN SUCCESS
        # =====================================================

        if success:


            # -----------------------------
            # Store Session
            # -----------------------------

            st.session_state["logged_in"] = True

            st.session_state["user_id"] = user["id"]

            st.session_state["name"] = user["full_name"]

            st.session_state["email"] = user["email"]

            st.session_state["role"] = user["role"]



            logger.info(
                f"User logged in successfully. User ID={user['id']}"
            )


            # ===============================
            # AUDIT LOG
            # ===============================

            log_activity(
                user_id=user["id"],
                action="LOGIN_SUCCESS",
                description="User logged in successfully"
            )


            st.success(
                message
            )



            # -----------------------------
            # Redirect
            # -----------------------------
            if user["role"] == "Admin":
                logger.info(
                    f"Admin logged in. User ID={user['id']}"
                )
                st.switch_page(
                    "pages/admin_dashboard.py"
                )
            elif user["role"] == "Employer":
                logger.info(
                    f"Employer logged in. User ID={user['id']}"
                )
                st.switch_page(
                    "pages/employer_dashboard.py"
                )
            elif user["role"] == "Candidate":
                logger.info(
                    f"Candidate logged in. User ID={user['id']}"
                )
                st.switch_page(
                    "pages/candidate_dashboard.py"
                )
            else:
                logger.error(
                    f"Unknown role: {user['role']}"
                )
                st.error(
                    "Invalid user role."
                )

        # =====================================================
        # LOGIN FAILED
        # =====================================================

        else:
            logger.warning(
                f"Login failed for email: {email}"
            )

            # ===============================
            # AUDIT LOG
            # ===============================
            log_activity(
                user_id=None,
                action="LOGIN_FAILED",
                description=f"Failed login attempt for {email}"
            )

            st.error(
                message
            )

    except Exception as e:
        logger.exception(
            "Unexpected error during login."
        )

        st.error(
            "Something went wrong. Please try again."
        )



# =====================================================
# BACK BUTTON
# =====================================================

st.divider()


if st.button(
    "⬅ Back to Home",
    use_container_width=True
):


    logger.info(
        "Returned to Home Page."
    )


    st.switch_page(
        "app.py"
    )
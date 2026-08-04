import streamlit as st

from utils.auth import register_user
from utils.logger import logger

from services.audit_service import log_activity

from utils.validation import (
    validate_name,
    validate_email,
    validate_phone,
    validate_password
)


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Register",
    page_icon="📝",
    layout="centered"
)


# =====================================================
# HEADER
# =====================================================

st.title("📝 Create Account")

st.write(
    "Register as Candidate or Employer"
)

st.divider()


# =====================================================
# INPUT FIELDS
# =====================================================

full_name = st.text_input(
    "Full Name"
).strip()


email = st.text_input(
    "Email"
).strip().lower()


phone = st.text_input(
    "Phone Number"
).strip()


password = st.text_input(
    "Password",
    type="password"
)


confirm_password = st.text_input(
    "Confirm Password",
    type="password"
)


role = st.selectbox(
    "Select Role",
    (
        "Candidate",
        "Employer"
    )
)


# =====================================================
# REGISTER
# =====================================================

if st.button(
    "Register",
    use_container_width=True
):

    try:

        logger.info(
            "Registration button clicked."
        )


        # -------------------------------------
        # Validation
        # -------------------------------------

        valid, message = validate_name(
            full_name
        )

        if not valid:
            st.error(message)
            st.stop()


        valid, message = validate_email(
            email
        )

        if not valid:
            st.error(message)
            st.stop()


        valid, message = validate_phone(
            phone
        )

        if not valid:
            st.error(message)
            st.stop()


        valid, message = validate_password(
            password
        )

        if not valid:
            st.error(message)
            st.stop()


        if password != confirm_password:

            st.error(
                "Passwords do not match."
            )

            st.stop()



        # -------------------------------------
        # Create Account
        # -------------------------------------

        with st.spinner(
            "Creating your account..."
        ):


            success, message, user_id = register_user(
                full_name,
                email,
                password,
                role,
                phone
            )


        # -------------------------------------
        # SUCCESS
        # -------------------------------------

        if success:


            logger.info(
                f"User registered successfully. ID: {user_id}"
            )


            # ===============================
            # AUDIT LOG
            # ===============================

            log_activity(
                user_id=user_id,
                action="REGISTER",
                description=f"New {role} account created"
            )


            st.success(
                message
            )


            st.info(
                "You can now login."
            )



        # -------------------------------------
        # FAILED REGISTRATION
        # -------------------------------------

        else:


            logger.warning(
                "Registration failed."
            )


            st.error(
                message
            )



    except Exception as e:


        logger.exception(
            "Unexpected registration error."
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
        "Returned to Home page."
    )


    st.switch_page(
        "app.py"
    )
import streamlit as st


def show_status_badge(status):
    """
    Display a colored badge for application status.
    """

    if status == "Pending":

        st.warning("🟡 Pending")

    elif status == "Shortlisted":

        st.success("🟢 Shortlisted")

    elif status == "Interview Scheduled":

        st.info("🔵 Interview Scheduled")

    elif status == "Rejected":

        st.error("🔴 Rejected")

    else:

        st.write(status)
import streamlit as st
import pandas as pd

from services.admin_service import (
    get_all_applications,
    delete_application_admin
)


def show_admin_application_management():

    st.header("📄 Application Management")

    applications = get_all_applications()

    if not applications:
        st.info("No applications found.")
        return

    # ----------------------------------
    # Search
    # ----------------------------------

    search = st.text_input(
        "Search Candidate"
    )

    # ----------------------------------
    # Status Filter
    # ----------------------------------

    status_filter = st.selectbox(
        "Application Status",
        [
            "All",
            "Pending",
            "Shortlisted",
            "Interview Scheduled",
            "Rejected"
        ]
    )

    filtered = []

    for app in applications:

        if search:

            keyword = search.lower()

            if (
                keyword not in app["full_name"].lower()
                and
                keyword not in app["email"].lower()
            ):
                continue

        if status_filter != "All":

            if app["status"] != status_filter:
                continue

        filtered.append(app)

    if not filtered:

        st.info("No matching applications.")
        return

    # ----------------------------------
    # Table
    # ----------------------------------

    rows = []

    for app in filtered:

        rows.append(
            {
                "ID": app["id"],
                "Candidate": app["full_name"],
                "Email": app["email"],
                "Job": app["title"],
                "ATS": app["ats_score"],
                "Match %": app["match_percentage"],
                "Status": app["status"]
            }
        )

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    selected = st.selectbox(
        "Select Application",
        df["ID"]
    )

    if st.button(
        "🗑 Delete Application",
        use_container_width=True
    ):

        delete_application_admin(selected)

        st.success(
            "Application deleted successfully."
        )

        st.rerun()
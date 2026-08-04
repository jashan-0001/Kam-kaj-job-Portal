import streamlit as st
import pandas as pd

from services.admin_service import (
    get_all_jobs,
    delete_job
)


def show_admin_job_management():

    st.header("💼 Job Management")

    jobs = get_all_jobs()

    if not jobs:
        st.info("No jobs found.")
        return

    # ----------------------------------
    # Search
    # ----------------------------------

    search = st.text_input(
        "Search Job"
    )

    filtered = []

    for job in jobs:

        if search:

            keyword = search.lower()

            if (
                keyword not in job["title"].lower()
                and
                keyword not in job["company"].lower()
                and
                keyword not in job["employer"].lower()
            ):
                continue

        filtered.append(job)

    if not filtered:

        st.info("No matching jobs.")
        return

    # ----------------------------------
    # Table
    # ----------------------------------

    table = []

    for job in filtered:

        table.append(
            {
                "ID": job["id"],
                "Title": job["title"],
                "Company": job["company"],
                "Employer": job["employer"],
                "Location": job["location"],
                "Posted": job["created_at"]
            }
        )

    df = pd.DataFrame(table)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    selected = st.selectbox(
        "Select Job",
        df["ID"]
    )

    if st.button(
        "🗑 Delete Job",
        use_container_width=True
    ):

        delete_job(selected)

        st.success(
            "Job deleted successfully."
        )

        st.rerun()
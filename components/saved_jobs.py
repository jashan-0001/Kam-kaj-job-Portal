import streamlit as st

from services.saved_job_service import (
    get_saved_jobs,
    unsave_job
)


def show_saved_jobs(user_id):

    st.header("❤️ Saved Jobs")

    jobs = get_saved_jobs(user_id)

    if not jobs:
        st.info("You haven't saved any jobs yet.")
        return

    search = st.text_input(
        "🔍 Search Saved Jobs"
    ).strip().lower()

    filtered = []

    for job in jobs:

        title = job["title"].lower()
        company = job["company"].lower()

        if (
            search in title
            or
            search in company
        ):
            filtered.append(job)

    st.write(f"### {len(filtered)} Saved Job(s)")

    for job in filtered:

        with st.container(border=True):

            st.subheader(job["title"])

            st.write(f"🏢 {job['company']}")

            st.write(f"📍 {job['location']}")

            st.write(f"💰 {job['salary']}")

            st.write(f"💼 {job['experience']}")

            st.write("### Skills")

            st.info(job["skills"])

            st.write("### Description")

            st.write(job["description"])

            if st.button(
                "❌ Remove",
                key=f"remove_{job['id']}"
            ):

                unsave_job(
                    user_id,
                    job["id"]
                )

                st.success(
                    "Removed from Saved Jobs."
                )

                st.rerun()
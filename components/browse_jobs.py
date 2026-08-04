import streamlit as st

from components.job_card import show_job_card
from services.job_service import get_open_jobs

def show_browse_jobs():
    st.header("💼 Browse Available Jobs")

    jobs = get_open_jobs()

    if not jobs:
        st.info("No jobs available.")
        return

    st.subheader("🔍 Find Your Dream Job")

    col1, col2 = st.columns(2)

    with col1:
        search = st.text_input(
            "Job Title / Company",
            placeholder="Python Developer, Google..."
        ).strip().lower()

    with col2:
        locations = sorted(
            {job["location"] for job in jobs if job["location"]}
        )
        location_filter = st.selectbox(
            "Location",
            ["All Locations"] + locations
        )

    col3, col4 = st.columns(2)

    with col3:
        experiences = sorted(
            {job["experience"] for job in jobs if job["experience"]}
        )
        experience_filter = st.selectbox(
            "Experience",
            ["All Experience"] + experiences
        )

    with col4:
        salary_search = st.text_input(
            "Salary Contains",
            placeholder="600000"
        ).strip()

    filtered_jobs = []

    for job in jobs:
        title = job["title"].lower()
        company = job["company"].lower()

        title_match = search in title or search in company
        location_match = (
            location_filter == "All Locations"
            or job["location"] == location_filter
        )
        experience_match = (
            experience_filter == "All Experience"
            or job["experience"] == experience_filter
        )
        salary_match = (
            salary_search == ""
            or salary_search.lower() in job["salary"].lower()
        )

        if title_match and location_match and experience_match and salary_match:
            filtered_jobs.append(job)

    st.write(f"### {len(filtered_jobs)} Job(s) Found")

    if not filtered_jobs:
        st.warning("No matching jobs found.")
        return

    candidate_id = st.session_state.get("user_id")

    if candidate_id is None:
        st.error("Please log in to apply for jobs.")
        return

    for job in filtered_jobs:
        show_job_card(job, candidate_id)
import streamlit as st

from components.job_card import show_job_card
from services.job_service import get_open_jobs


# ============================================================
# BROWSE JOBS
# ============================================================

def show_browse_jobs():
    """
    Display all currently open jobs and provide
    search/filter functionality for candidates.
    """

    st.header("💼 Browse Available Jobs")

    # ========================================================
    # GET OPEN JOBS
    # ========================================================

    jobs = get_open_jobs()

    if not jobs:

        st.info(
            "No jobs available."
        )

        return

    # ========================================================
    # SEARCH & FILTER
    # ========================================================

    st.subheader(
        "🔍 Find Your Dream Job"
    )

    col1, col2 = st.columns(2)

    # ========================================================
    # JOB TITLE / COMPANY SEARCH
    # ========================================================

    with col1:

        search = st.text_input(
            "Job Title / Company",
            placeholder="Python Developer, Google..."
        ).strip().lower()

    # ========================================================
    # LOCATION FILTER
    # ========================================================

    with col2:

        locations = sorted(
            {
                str(job.get("location", "")).strip()
                for job in jobs
                if job.get("location")
            }
        )

        location_filter = st.selectbox(
            "Location",
            ["All Locations"] + locations
        )

    # ========================================================
    # EXPERIENCE FILTER
    # ========================================================

    col3, col4 = st.columns(2)

    with col3:

        experiences = sorted(
            {
                str(job.get("experience", "")).strip()
                for job in jobs
                if job.get("experience")
            }
        )

        experience_filter = st.selectbox(
            "Experience",
            ["All Experience"] + experiences
        )

    # ========================================================
    # SALARY SEARCH
    # ========================================================

    with col4:

        salary_search = st.text_input(
            "Salary Contains",
            placeholder="600000"
        ).strip().lower()

    # ========================================================
    # FILTER JOBS
    # ========================================================

    filtered_jobs = []

    for job in jobs:

        title = str(
            job.get("title", "")
        ).lower()

        company = str(
            job.get("company", "")
        ).lower()

        location = str(
            job.get("location", "")
        )

        experience = str(
            job.get("experience", "")
        )

        salary = str(
            job.get("salary", "")
        ).lower()

        # ----------------------------------------------------
        # Search
        # ----------------------------------------------------

        title_match = (
            not search
            or search in title
            or search in company
        )

        # ----------------------------------------------------
        # Location
        # ----------------------------------------------------

        location_match = (
            location_filter == "All Locations"
            or location == location_filter
        )

        # ----------------------------------------------------
        # Experience
        # ----------------------------------------------------

        experience_match = (
            experience_filter == "All Experience"
            or experience == experience_filter
        )

        # ----------------------------------------------------
        # Salary
        # ----------------------------------------------------

        salary_match = (
            not salary_search
            or salary_search in salary
        )

        # ----------------------------------------------------
        # FINAL FILTER
        # ----------------------------------------------------

        if (
            title_match
            and location_match
            and experience_match
            and salary_match
        ):

            filtered_jobs.append(job)

    # ========================================================
    # RESULTS COUNT
    # ========================================================

    st.write(
        f"### {len(filtered_jobs)} Job(s) Found"
    )

    if not filtered_jobs:

        st.warning(
            "No matching jobs found."
        )

        return

    # ========================================================
    # CANDIDATE LOGIN CHECK
    # ========================================================

    candidate_id = st.session_state.get(
        "user_id"
    )

    if candidate_id is None:

        st.error(
            "Please log in to apply for jobs."
        )

        return

    # ========================================================
    # DISPLAY JOB CARDS
    # ========================================================

    for job in filtered_jobs:

        show_job_card(
            job,
            candidate_id
        )

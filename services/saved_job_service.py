import streamlit as st

from database.database import (
    execute_query,
    fetch_all,
    fetch_one
)

from utils.cache_manager import clear_cache


# =====================================================
# SAVE JOB
# =====================================================

def save_job(
    candidate_id,
    job_id
):
    """
    Save a job for a candidate.

    Returns:
        bool: True if the job was saved successfully.
    """

    try:

        # -------------------------------------------------
        # Check whether job is already saved
        # -------------------------------------------------

        existing = fetch_one(
            """
            SELECT id

            FROM saved_jobs

            WHERE candidate_id = ?
            AND job_id = ?

            LIMIT 1
            """,
            (
                candidate_id,
                job_id
            )
        )

        if existing:

            return True

        # -------------------------------------------------
        # Verify that the job exists
        # -------------------------------------------------

        job = fetch_one(
            """
            SELECT id

            FROM jobs

            WHERE id = ?
            """,
            (job_id,)
        )

        if not job:

            return False

        # -------------------------------------------------
        # Save job
        # -------------------------------------------------

        query = """
        INSERT INTO saved_jobs
        (
            candidate_id,
            job_id
        )
        VALUES (?, ?)
        """

        success = execute_query(
            query,
            (
                candidate_id,
                job_id
            )
        )

        if success:

            clear_cache()

        return success

    except Exception:

        return False


# =====================================================
# UNSAVE JOB
# =====================================================

def unsave_job(
    candidate_id,
    job_id
):
    """
    Remove a saved job for a candidate.

    Returns:
        bool
    """

    try:

        query = """
        DELETE FROM saved_jobs

        WHERE candidate_id = ?
        AND job_id = ?
        """

        success = execute_query(
            query,
            (
                candidate_id,
                job_id
            )
        )

        if success:

            clear_cache()

        return success

    except Exception:

        return False


# =====================================================
# CHECK SAVED
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def is_saved(
    candidate_id,
    job_id
):
    """
    Check whether a job is already saved.

    Returns:
        dict | None
    """

    try:

        query = """
        SELECT
            id

        FROM saved_jobs

        WHERE candidate_id = ?
        AND job_id = ?

        LIMIT 1
        """

        return fetch_one(
            query,
            (
                candidate_id,
                job_id
            )
        )

    except Exception:

        return None


# =====================================================
# GET SAVED JOBS
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_saved_jobs(
    candidate_id
):
    """
    Return all saved jobs for a candidate.
    """

    try:

        query = """
        SELECT

            jobs.id,
            jobs.title,
            jobs.company,
            jobs.location,
            jobs.experience,
            jobs.salary,
            jobs.skills,
            jobs.description,
            jobs.status,
            jobs.created_at,

            saved_jobs.saved_at

        FROM saved_jobs

        INNER JOIN jobs
            ON jobs.id = saved_jobs.job_id

        WHERE saved_jobs.candidate_id = ?

        ORDER BY saved_jobs.saved_at DESC
        """

        return fetch_all(
            query,
            (candidate_id,)
        )

    except Exception:

        return []


# =====================================================
# COUNT SAVED JOBS
# =====================================================

@st.cache_data(
    ttl=30,
    show_spinner=False
)
def count_saved_jobs(
    candidate_id
):
    """
    Return total number of saved jobs
    for a candidate.
    """

    try:

        from database.database import fetch_one

        query = """
        SELECT
            COUNT(*) AS total

        FROM saved_jobs

        WHERE candidate_id = ?
        """

        row = fetch_one(
            query,
            (candidate_id,)
        )

        return (
            row["total"]
            if row
            else 0
        )

    except Exception:

        return 0

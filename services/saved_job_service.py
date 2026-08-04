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

def save_job(candidate_id, job_id):
    """
    Save a job for a candidate.
    """

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


# =====================================================
# UNSAVE JOB
# =====================================================

def unsave_job(candidate_id, job_id):
    """
    Remove a saved job.
    """

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


# =====================================================
# CHECK SAVED
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def is_saved(candidate_id, job_id):
    """
    Check whether a job is already saved.
    """

    query = """
    SELECT id

    FROM saved_jobs

    WHERE candidate_id = ?
      AND job_id = ?
    """

    return fetch_one(
        query,
        (
            candidate_id,
            job_id
        )
    )


# =====================================================
# GET SAVED JOBS
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_saved_jobs(candidate_id):
    """
    Return all saved jobs for a candidate.
    """

    query = """
    SELECT

        jobs.id,
        jobs.title,
        jobs.company,
        jobs.location,
        jobs.experience,
        jobs.salary,
        jobs.skills,
        jobs.status,
        jobs.created_at

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
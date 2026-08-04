import streamlit as st

from database.database import (
    execute_query,
    fetch_all,
    fetch_one
)
from utils.logger import logger
from typing import List, Dict
from utils.cache_manager import clear_cache
# =====================================================
# ADD JOB
# =====================================================

def add_job(
    title,
    company,
    location,
    experience,
    salary,
    skills,
    description,
    posted_by
):
    """
    Add a new job.
    """

    try:

        query = """
        INSERT INTO jobs
        (
            title,
            company,
            location,
            experience,
            salary,
            skills,
            description,
            posted_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        success = execute_query(
            query,
            (
                title,
                company,
                location,
                experience,
                salary,
                skills,
                description,
                posted_by
            )
        )

        if success:

            clear_cache()

            logger.info(
                f"Job created successfully by Employer ID={posted_by}"
            )

        return success

    except Exception:

        logger.exception(
            "Failed to add job."
        )

        return False

# =====================================================
# GET ALL JOBS
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_all_jobs() -> List[Dict]:

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
        jobs.posted_by,
        users.full_name AS employer_name

    FROM jobs

    INNER JOIN users
        ON jobs.posted_by = users.id

    WHERE jobs.status='Open'

    ORDER BY jobs.created_at DESC
    """

    return fetch_all(query)


# =====================================================
# GET JOBS BY EMPLOYER
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_jobs_by_employer(user_id)-> List[Dict]:

    query = """
    SELECT
        id,
        title,
        company,
        location,
        experience,
        salary,
        skills,
        description,
        status,
        created_at

    FROM jobs

    WHERE posted_by=?

    ORDER BY created_at DESC
    """

    return fetch_all(
        query,
        (user_id,)
    )


# =====================================================
# GET JOB
# =====================================================

@st.cache_data(
    ttl=300,
    show_spinner=False
)
def get_job_by_id(job_id) -> Dict | None:

    query = """
    SELECT
        id,
        title,
        company,
        location,
        experience,
        salary,
        skills,
        description,
        status,
        posted_by,
        created_at

    FROM jobs

    WHERE id=?
    """

    return fetch_one(
        query,
        (job_id,)
    )


# =====================================================
# UPDATE JOB
# =====================================================

def update_job(
    job_id,
    title,
    company,
    location,
    experience,
    salary,
    skills,
    description
):
    """
    Update an existing job.
    """

    try:

        query = """
        UPDATE jobs
        SET
            title=?,
            company=?,
            location=?,
            experience=?,
            salary=?,
            skills=?,
            description=?
        WHERE id=?
        """

        success = execute_query(
            query,
            (
                title,
                company,
                location,
                experience,
                salary,
                skills,
                description,
                job_id
            )
        )

        if success:

            clear_cache()

            logger.info(
                f"Job updated successfully. Job ID={job_id}"
            )

        return success

    except Exception:

        logger.exception(
            f"Failed to update Job ID={job_id}"
        )

        return False

# =====================================================
# DELETE JOB
# =====================================================

def delete_job(job_id):
    """
    Delete a job.
    """

    try:

        success = execute_query(
            "DELETE FROM jobs WHERE id=?",
            (job_id,)
        )

        if success:

            clear_cache()

            logger.info(
                f"Job deleted successfully. Job ID={job_id}"
            )

        return success

    except Exception:

        logger.exception(
            f"Failed to delete Job ID={job_id}"
        )

        return False

# =====================================================
# CLOSE JOB
# =====================================================

def close_job(job_id):
    """
    Mark a job as Closed.
    """

    try:

        success = execute_query(
            """
            UPDATE jobs
            SET status='Closed'
            WHERE id=?
            """,
            (job_id,)
        )

        if success:

            clear_cache()

            logger.info(
                f"Job closed successfully. Job ID={job_id}"
            )

        return success

    except Exception:

        logger.exception(
            f"Failed to close Job ID={job_id}"
        )

        return False


# =====================================================
# REOPEN JOB
# =====================================================

def reopen_job(job_id):
    """
    Reopen a previously closed job.
    """

    try:

        success = execute_query(
            """
            UPDATE jobs
            SET status='Open'
            WHERE id=?
            """,
            (job_id,)
        )

        if success:

            clear_cache()

            logger.info(
                f"Job reopened successfully. Job ID={job_id}"
            )

        return success

    except Exception:

        logger.exception(
            f"Failed to reopen Job ID={job_id}"
        )

        return False


# =====================================================
# TOTAL JOBS
# =====================================================

@st.cache_data(
    ttl=30,
    show_spinner=False
)
def total_jobs(user_id):

    row = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM jobs
        WHERE posted_by=?
        """,
        (user_id,)
    )

    return row["total"] if row else 0


# =====================================================
# TOTAL OPEN JOBS
# =====================================================

@st.cache_data(
    ttl=30,
    show_spinner=False
)
def total_open_jobs(user_id):

    row = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM jobs
        WHERE posted_by=?
        AND status='Open'
        """,
        (user_id,)
    )

    return row["total"] if row else 0


# =====================================================
# TOTAL CLOSED JOBS
# =====================================================

@st.cache_data(
    ttl=30,
    show_spinner=False
)
def total_closed_jobs(user_id):

    row = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM jobs
        WHERE posted_by=?
        AND status='Closed'
        """,
        (user_id,)
    )

    return row["total"] if row else 0


# =====================================================
# GET OPEN JOBS
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_open_jobs() -> List[Dict]:

    query = """
    SELECT
        id,
        title,
        company,
        location,
        experience,
        salary,
        skills,
        description,
        status

    FROM jobs

    WHERE status='Open'

    ORDER BY created_at DESC
    """

    return fetch_all(query)


# =====================================================
# JOB SKILLS
# =====================================================

@st.cache_data(
    ttl=300,
    show_spinner=False
)
def get_job_skills(job_id)-> List[str]:

    row = fetch_one(
        """
        SELECT skills
        FROM jobs
        WHERE id=?
        """,
        (job_id,)
    )

    if not row:
        return []

    return [
        skill.strip()
        for skill in row["skills"].split(",")
        if skill.strip()
    ]
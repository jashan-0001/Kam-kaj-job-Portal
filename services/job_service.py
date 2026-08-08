import streamlit as st

from database.database import (
    execute_query,
    fetch_all,
    fetch_one
)

from utils.logger import logger
from utils.cache_manager import clear_cache

from typing import List, Dict


# ============================================================
# ADD JOB
# ============================================================

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
    Add a new job for an employer.
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
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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


# ============================================================
# GET ALL OPEN JOBS
# ============================================================

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

    WHERE jobs.status = 'Open'

    ORDER BY jobs.created_at DESC
    """

    return fetch_all(query)


# ============================================================
# GET JOBS BY EMPLOYER
# ============================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_jobs_by_employer(user_id) -> List[Dict]:

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

    WHERE posted_by = %s

    ORDER BY created_at DESC
    """

    return fetch_all(
        query,
        (user_id,)
    )


# ============================================================
# GET JOB
# ============================================================

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

    WHERE id = %s
    """

    return fetch_one(
        query,
        (job_id,)
    )


# ============================================================
# CHECK JOB OWNERSHIP
# ============================================================

def is_job_owner(
    job_id,
    employer_id
):
    """
    Verify that a job belongs to the specified employer.
    """

    row = fetch_one(
        """
        SELECT id
        FROM jobs
        WHERE id = %s
        AND posted_by = %s
        """,
        (
            job_id,
            employer_id
        )
    )

    return row is not None


# ============================================================
# UPDATE JOB
# ============================================================

def update_job(
    job_id,
    title,
    company,
    location,
    experience,
    salary,
    skills,
    description,
    employer_id=None
):
    """
    Update a job.

    If employer_id is provided, ownership is verified.
    """

    try:

        if employer_id is not None:

            if not is_job_owner(
                job_id,
                employer_id
            ):

                logger.warning(
                    f"Unauthorized job update attempt. "
                    f"Job ID={job_id}, Employer ID={employer_id}"
                )

                return False


        query = """
        UPDATE jobs

        SET
            title = %s,
            company = %s,
            location = %s,
            experience = %s,
            salary = %s,
            skills = %s,
            description = %s

        WHERE id = %s
        """

        params = (
            title,
            company,
            location,
            experience,
            salary,
            skills,
            description,
            job_id
        )

        success = execute_query(
            query,
            params
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


# ============================================================
# DELETE JOB
# ============================================================

def delete_job(
    job_id,
    employer_id=None
):
    """
    Delete a job.

    Ownership is checked when employer_id is supplied.

    IMPORTANT:
    Because the database currently uses ON DELETE CASCADE,
    deleting a job can also delete its applications.
    """

    try:

        if employer_id is not None:

            if not is_job_owner(
                job_id,
                employer_id
            ):

                logger.warning(
                    f"Unauthorized job deletion attempt. "
                    f"Job ID={job_id}, Employer ID={employer_id}"
                )

                return False


        # ----------------------------------------------------
        # Check for existing applications
        # ----------------------------------------------------

        application_row = fetch_one(
            """
            SELECT COUNT(*) AS total
            FROM applications
            WHERE job_id = %s
            """,
            (job_id,)
        )

        application_count = (
            application_row["total"]
            if application_row
            else 0
        )


        # ----------------------------------------------------
        # Prevent destructive deletion
        # ----------------------------------------------------

        if application_count > 0:

            logger.warning(
                f"Job deletion blocked because applications exist. "
                f"Job ID={job_id}, Applications={application_count}"
            )

            return False


        # ----------------------------------------------------
        # Delete job
        # ----------------------------------------------------

        success = execute_query(
            """
            DELETE FROM jobs
            WHERE id = %s
            """,
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


# ============================================================
# CLOSE JOB
# ============================================================

def close_job(
    job_id,
    employer_id=None
):
    """
    Mark a job as Closed.
    """

    try:

        if employer_id is not None:

            if not is_job_owner(
                job_id,
                employer_id
            ):

                logger.warning(
                    f"Unauthorized job close attempt. "
                    f"Job ID={job_id}, Employer ID={employer_id}"
                )

                return False


        success = execute_query(
            """
            UPDATE jobs

            SET status = 'Closed'

            WHERE id = %s
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


# ============================================================
# REOPEN JOB
# ============================================================

def reopen_job(
    job_id,
    employer_id=None
):
    """
    Reopen a previously closed job.
    """

    try:

        if employer_id is not None:

            if not is_job_owner(
                job_id,
                employer_id
            ):

                logger.warning(
                    f"Unauthorized job reopen attempt. "
                    f"Job ID={job_id}, Employer ID={employer_id}"
                )

                return False


        success = execute_query(
            """
            UPDATE jobs

            SET status = 'Open'

            WHERE id = %s
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


# ============================================================
# TOTAL JOBS
# ============================================================

@st.cache_data(
    ttl=30,
    show_spinner=False
)
def total_jobs(user_id):

    row = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM jobs
        WHERE posted_by = %s
        """,
        (user_id,)
    )

    return row["total"] if row else 0


# ============================================================
# TOTAL OPEN JOBS
# ============================================================

@st.cache_data(
    ttl=30,
    show_spinner=False
)
def total_open_jobs(user_id):

    row = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM jobs
        WHERE posted_by = %s
        AND status = 'Open'
        """,
        (user_id,)
    )

    return row["total"] if row else 0


# ============================================================
# TOTAL CLOSED JOBS
# ============================================================

@st.cache_data(
    ttl=30,
    show_spinner=False
)
def total_closed_jobs(user_id):

    row = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM jobs
        WHERE posted_by = %s
        AND status = 'Closed'
        """,
        (user_id,)
    )

    return row["total"] if row else 0


# ============================================================
# GET OPEN JOBS
# ============================================================

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

    WHERE status = 'Open'

    ORDER BY created_at DESC
    """

    return fetch_all(query)


# ============================================================
# JOB SKILLS
# ============================================================

@st.cache_data(
    ttl=300,
    show_spinner=False
)
def get_job_skills(job_id) -> List[str]:

    row = fetch_one(
        """
        SELECT skills
        FROM jobs
        WHERE id = %s
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

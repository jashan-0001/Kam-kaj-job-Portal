import streamlit as st

from database.database import (
    fetch_one,
    fetch_all
)
from utils.logger import logger


# =====================================================
# CACHE
# =====================================================

def clear_analytics_cache():
    """
    Clear analytics cache.
    """
    st.cache_data.clear()


# =====================================================
# RECRUITER STATISTICS
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_recruiter_statistics(employer_id):
    """
    Return recruiter dashboard statistics.
    """

    try:

        row = fetch_one(
            """
            SELECT COUNT(*) AS total_jobs
            FROM jobs
            WHERE posted_by = ?
            """,
            (employer_id,)
        )

        total_jobs = row["total_jobs"] if row else 0

        row = fetch_one(
            """
            SELECT COUNT(*) AS total_applications

            FROM applications

            INNER JOIN jobs
            ON jobs.id = applications.job_id

            WHERE jobs.posted_by = ?
            """,
            (employer_id,)
        )

        total_applications = row["total_applications"] if row else 0

        row = fetch_one(
            """
            SELECT AVG(applications.ats_score) AS average_ats

            FROM applications

            INNER JOIN jobs
            ON jobs.id = applications.job_id

            WHERE jobs.posted_by = ?
            """,
            (employer_id,)
        )

        average_ats = (
            row["average_ats"]
            if row and row["average_ats"] is not None
            else 0
        )

        row = fetch_one(
            """
            SELECT MAX(applications.ats_score) AS best_ats

            FROM applications

            INNER JOIN jobs
            ON jobs.id = applications.job_id

            WHERE jobs.posted_by = ?
            """,
            (employer_id,)
        )

        best_ats = (
            row["best_ats"]
            if row and row["best_ats"] is not None
            else 0
        )

        return {
            "total_jobs": total_jobs,
            "total_applications": total_applications,
            "average_ats": round(average_ats, 2),
            "best_ats": best_ats
        }

    except Exception:

        logger.exception(
            "Failed to load recruiter statistics."
        )

        return {
            "total_jobs": 0,
            "total_applications": 0,
            "average_ats": 0,
            "best_ats": 0
        }

# =====================================================
# ATS SCORES
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_ats_scores(employer_id):
    """
    Return ATS scores.
    """

    try:

        query = """
        SELECT applications.ats_score

        FROM applications

        INNER JOIN jobs
        ON jobs.id = applications.job_id

        WHERE jobs.posted_by = ?
        """

        rows = fetch_all(
            query,
            (employer_id,)
        )

        return [
            row["ats_score"]
            for row in rows
            if row["ats_score"] is not None
        ]

    except Exception:

        logger.exception(
            "Failed to load ATS scores."
        )

        return []

# =====================================================
# RECOMMENDATION DISTRIBUTION
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_recommendation_distribution(employer_id):
    """
    Return recommendation distribution.
    """

    try:

        query = """
        SELECT

            applications.recommendation,

            COUNT(*) AS total

        FROM applications

        INNER JOIN jobs
        ON jobs.id = applications.job_id

        WHERE jobs.posted_by = ?

        GROUP BY applications.recommendation
        """

        return fetch_all(
            query,
            (employer_id,)
        )

    except Exception:

        logger.exception(
            "Failed to load recommendation distribution."
        )

        return []

# =====================================================
# APPLICATIONS PER JOB
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_applications_per_job(employer_id):
    """
    Return applications per job.
    """

    try:

        query = """
        SELECT

            jobs.title,

            COUNT(applications.id) AS total

        FROM jobs

        LEFT JOIN applications
        ON jobs.id = applications.job_id

        WHERE jobs.posted_by = ?

        GROUP BY jobs.id

        ORDER BY total DESC
        """

        return fetch_all(
            query,
            (employer_id,)
        )

    except Exception:

        logger.exception(
            "Failed to load applications per job."
        )

        return []
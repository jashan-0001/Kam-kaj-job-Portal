import uuid

import streamlit as st

from config import RESUME_DIR

from database.database import execute_query, fetch_all, fetch_one

from constants import APPLICATION_PENDING

from ai.resume_analyzer import analyze_resume
from ai.screening_engine import screen_resume

from services.job_service import get_job_skills

from utils.cache_manager import clear_cache
from utils.logger import logger
from services.audit_service import log_activity


# =====================================================
# CONFIGURATION
# =====================================================
UPLOAD_FOLDER = RESUME_DIR
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


# =====================================================
# SAVE RESUME
# =====================================================

def save_resume(uploaded_file):
    """Save uploaded resume with a unique filename."""

    try:
        if uploaded_file is None:
            return None

        extension = uploaded_file.name.split(".")[-1]
        filename = f"{uuid.uuid4().hex}.{extension}"
        file_path = UPLOAD_FOLDER / filename

        with open(file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        logger.info(f"Resume saved: {filename}")
        return str(file_path)

    except Exception:
        logger.exception("Unable to save resume.")
        return None


# =====================================================
# CHECK DUPLICATE APPLICATION
# =====================================================

def already_applied(job_id, user_id):
    """Check whether candidate has already applied."""

    try:
        query = """
        SELECT id
        FROM applications
        WHERE job_id = ?
        AND user_id = ?
        """

        return fetch_one(query, (job_id, user_id))

    except Exception:
        logger.exception("Failed to check duplicate application.")
        return None


# =====================================================
# APPLY FOR JOB
# =====================================================

def apply_job(job_id, candidate_id, resume_path):
    """Apply for a job using AI screening."""

    try:
        resume = analyze_resume(resume_path)

        if resume is None:
            logger.error("Resume analysis failed.")
            return False

        candidate_skills = resume["skills"]
        job_skills = get_job_skills(job_id)
        screening = screen_resume(candidate_skills, job_skills)

        query = """
        INSERT INTO applications
        (
            job_id,
            user_id,
            resume_path,
            ats_score,
            match_percentage,
            matched_skills,
            missing_skills,
            recommendation,
            status
        )
        VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        params = (
            job_id,
            candidate_id,
            resume_path,
            screening["ats_score"],
            screening["match_percentage"],
            ", ".join(screening["matched_skills"]),
            ", ".join(screening["missing_skills"]),
            screening["recommendation"],
            APPLICATION_PENDING,
        )

        success = execute_query(query, params)

        if success:
            clear_cache()

            log_activity(
                user_id=candidate_id,
                action="RESUME_UPLOAD",
                description="Candidate uploaded resume",
            )

            log_activity(
                user_id=candidate_id,
                action="JOB_APPLY",
                description=f"Applied for job ID {job_id}",
            )

            logger.info(f"Audit logs created for Candidate {candidate_id}")

        return success

    except Exception:
        logger.exception("Job application failed.")
        return False


# =====================================================
# CANDIDATE APPLICATIONS
# =====================================================
@st.cache_data(ttl=60, show_spinner=False)
def get_my_applications(user_id):
    query = """
SELECT
    a.id,
    j.title,
    j.company,
    j.location,
    a.match_percentage,
    a.status,
    a.applied_at

FROM applications a

JOIN jobs j
ON a.job_id = j.id

WHERE a.user_id = ?

ORDER BY a.applied_at DESC
"""

    return fetch_all(query, (user_id,))


# =====================================================
# EMPLOYER APPLICATIONS
# =====================================================
@st.cache_data(ttl=60, show_spinner=False)
def get_applications_by_employer(employer_id):
    query = """
SELECT
    a.id,
    a.user_id,
    a.ats_score,
    a.match_percentage,
    a.status,
    a.applied_at,
    a.resume_path,
    a.recommendation,
    a.matched_skills,
    a.missing_skills,

    u.id AS candidate_id,
    u.full_name,
    u.email,

    j.id AS job_id,
    j.title,
    j.company,
    j.posted_by AS employer_id

FROM jobs j

JOIN applications a
ON a.job_id = j.id

JOIN users u
ON a.user_id = u.id

WHERE j.posted_by = ?

ORDER BY a.applied_at DESC
"""

    return fetch_all(query, (employer_id,))


# =====================================================
# UPDATE APPLICATION STATUS
# =====================================================

def update_application_status(application_id, status, user_id=None):
    try:
        query = """
        UPDATE applications
        SET status = ?
        WHERE id = ?
        """

        result = execute_query(query, (status, application_id))

        if result:
            clear_cache()

            log_activity(
                user_id=user_id,
                action="APPLICATION_STATUS_UPDATE",
                description=(
                    f"Application {application_id} "
                    f"status changed to {status}"
                ),
            )

            logger.info(f"Application {application_id} updated to {status}")

        return result

    except Exception:
        logger.exception("Unable to update application.")
        return False


# =====================================================
# TOTAL APPLICATIONS
# =====================================================
@st.cache_data(ttl=30, show_spinner=False)
def total_applications(employer_id):
    """Return total applications received by employer."""

    try:
        query = """
        SELECT COUNT(*) AS total

        FROM jobs j

        JOIN applications a
        ON j.id = a.job_id

        WHERE j.posted_by = ?
        """

        row = fetch_one(query, (employer_id,))
        return row["total"] if row else 0

    except Exception:
        logger.exception("Unable to calculate total applications.")
        return 0


# =====================================================
# DELETE APPLICATION
# =====================================================

def delete_application(application_id):
    try:
        query = """
        DELETE FROM applications
        WHERE id = ?
        """

        logger.info(f"Application deleted: {application_id}")
        success = execute_query(query, (application_id,))

        if success:
            clear_cache()

        return success

    except Exception:
        logger.exception("Unable to delete application.")
        return False


# =====================================================
# APPLICATIONS BY JOB
# =====================================================
@st.cache_data(ttl=60, show_spinner=False)
def get_applications_by_job(job_id):
    """Return applications for a specific job."""

    try:
        query = """
        SELECT
            a.*,
            u.full_name,
            u.email,
            j.title,
            j.company,
            j.posted_by AS employer_id

        FROM applications a

        JOIN users u
        ON a.user_id = u.id

        JOIN jobs j
        ON a.job_id = j.id

        WHERE a.job_id = ?

        ORDER BY a.ats_score DESC
        """

        return fetch_all(query, (job_id,))

    except Exception:
        logger.exception("Unable to fetch job applications.")
        return []


# =====================================================
# CANDIDATE APPLICATIONS
# =====================================================
@st.cache_data(ttl=60, show_spinner=False)
def get_candidate_applications(candidate_id):
    """Return all applications of one candidate."""

    try:
        query = """
        SELECT
            a.*,
            j.title,
            j.company,
            j.location

        FROM applications a

        JOIN jobs j
        ON a.job_id = j.id

        WHERE a.user_id = ?

        ORDER BY a.applied_at DESC
        """

        return fetch_all(query, (candidate_id,))

    except Exception:
        logger.exception("Unable to fetch candidate applications.")
        return []


# =====================================================
# GET APPLICATION BY ID
# =====================================================
@st.cache_data(ttl=300, show_spinner=False)
def get_application_by_id(application_id):
    """Return a single application."""

    try:
        query = """
        SELECT
            a.*,
            u.id AS candidate_id,
            u.full_name,
            u.email,
            j.id AS job_id,
            j.title,
            j.company,
            j.posted_by AS employer_id

        FROM applications a

        JOIN users u
        ON a.user_id = u.id

        JOIN jobs j
        ON a.job_id = j.id

        WHERE a.id = ?
        """

        return fetch_one(query, (application_id,))

    except Exception:
        logger.exception("Unable to fetch application.")
        return None


def toggle_favorite(application_id):
    """Toggle favourite status."""

    try:
        query = """
        UPDATE applications
        SET is_favorite =
            CASE
                WHEN is_favorite = 1 THEN 0
                ELSE 1
            END
        WHERE id = ?
        """

        success = execute_query(query, (application_id,))

        if success:
            clear_cache()
            logger.info(f"Application {application_id} favorite toggled.")

        return success

    except Exception:
        logger.exception("Unable to toggle favorite.")
        return False

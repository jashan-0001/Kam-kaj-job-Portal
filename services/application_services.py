import uuid

import streamlit as st

from config import RESUME_DIR

from database.database import (
    execute_query,
    fetch_all,
    fetch_one
)

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

UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# =====================================================
# SAVE RESUME
# =====================================================

def save_resume(uploaded_file):
    """
    Save uploaded resume with a unique filename.

    Returns:
        str | None: Saved file path or None if failed.
    """

    try:

        if uploaded_file is None:
            return None

        # -------------------------------------------------
        # Get extension safely
        # -------------------------------------------------

        original_name = uploaded_file.name

        extension = original_name.rsplit(
            ".",
            1
        )[-1].lower()

        filename = (
            f"{uuid.uuid4().hex}.{extension}"
        )

        file_path = (
            UPLOAD_FOLDER / filename
        )

        # -------------------------------------------------
        # Save file
        # -------------------------------------------------

        with open(
            file_path,
            "wb"
        ) as file:

            file.write(
                uploaded_file.getbuffer()
            )

        logger.info(
            f"Resume saved successfully: {filename}"
        )

        return str(file_path)

    except Exception:

        logger.exception(
            "Unable to save resume."
        )

        return None


# =====================================================
# CHECK DUPLICATE APPLICATION
# =====================================================

def already_applied(
    job_id,
    user_id
):
    """
    Check whether a candidate has already
    applied for a particular job.

    Returns:
        dict | None
    """

    try:

        query = """
        SELECT
            id,
            job_id,
            user_id,
            status,
            applied_at

        FROM applications

        WHERE job_id = ?
        AND user_id = ?

        LIMIT 1
        """

        return fetch_one(
            query,
            (
                job_id,
                user_id
            )
        )

    except Exception:

        logger.exception(
            "Failed to check duplicate application."
        )

        return None


# =====================================================
# APPLY FOR JOB
# =====================================================

def apply_job(
    job_id,
    candidate_id,
    resume_path
):
    """
    Apply for a job using AI resume screening.

    Returns:
        bool
    """

    try:

        # -------------------------------------------------
        # Validate job
        # -------------------------------------------------

        job = fetch_one(
            """
            SELECT
                id,
                title,
                status,
                posted_by

            FROM jobs

            WHERE id = ?
            """,
            (job_id,)
        )

        if not job:

            logger.warning(
                f"Application rejected. Job ID={job_id} not found."
            )

            return False

        # -------------------------------------------------
        # Check job status
        # -------------------------------------------------

        if job["status"] != "Open":

            logger.warning(
                f"Application rejected. Job ID={job_id} is closed."
            )

            return False

        # -------------------------------------------------
        # Check duplicate application
        # -------------------------------------------------

        existing_application = already_applied(
            job_id,
            candidate_id
        )

        if existing_application:

            logger.warning(
                f"Duplicate application blocked. "
                f"Candidate ID={candidate_id}, "
                f"Job ID={job_id}"
            )

            return False

        # -------------------------------------------------
        # Analyze resume
        # -------------------------------------------------

        resume = analyze_resume(
            resume_path
        )

        if resume is None:

            logger.error(
                "Resume analysis failed."
            )

            return False

        # -------------------------------------------------
        # Extract candidate skills
        # -------------------------------------------------

        candidate_skills = resume.get(
            "skills",
            []
        )

        # -------------------------------------------------
        # Get required job skills
        # -------------------------------------------------

        job_skills = get_job_skills(
            job_id
        )

        # -------------------------------------------------
        # AI Screening
        # -------------------------------------------------

        screening = screen_resume(
            candidate_skills,
            job_skills
        )

        if not screening:

            logger.error(
                "Resume screening failed."
            )

            return False

        # -------------------------------------------------
        # Safely extract screening results
        # -------------------------------------------------

        ats_score = screening.get(
            "ats_score",
            0
        )

        match_percentage = screening.get(
            "match_percentage",
            0
        )

        matched_skills = screening.get(
            "matched_skills",
            []
        )

        missing_skills = screening.get(
            "missing_skills",
            []
        )

        recommendation = screening.get(
            "recommendation",
            ""
        )

        # -------------------------------------------------
        # Insert application
        # -------------------------------------------------

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
        (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        )
        """

        params = (
            job_id,
            candidate_id,
            resume_path,
            ats_score,
            match_percentage,
            ", ".join(
                str(skill)
                for skill in matched_skills
            ),
            ", ".join(
                str(skill)
                for skill in missing_skills
            ),
            recommendation,
            APPLICATION_PENDING
        )

        success = execute_query(
            query,
            params
        )

        if not success:

            logger.error(
                "Application database insertion failed."
            )

            return False

        # -------------------------------------------------
        # Clear application cache
        # -------------------------------------------------

        clear_cache()

        # -------------------------------------------------
        # Audit: Resume Upload
        # -------------------------------------------------

        log_activity(
            user_id=candidate_id,
            action="RESUME_UPLOAD",
            description=(
                "Candidate uploaded resume."
            )
        )

        # -------------------------------------------------
        # Audit: Job Application
        # -------------------------------------------------

        log_activity(
            user_id=candidate_id,
            action="JOB_APPLY",
            description=(
                f"Applied for job ID {job_id}."
            )
        )

        logger.info(
            f"Application submitted successfully. "
            f"Candidate ID={candidate_id}, "
            f"Job ID={job_id}"
        )

        return True

    except Exception:

        logger.exception(
            "Job application failed."
        )

        return False


# =====================================================
# CANDIDATE APPLICATIONS
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_my_applications(
    user_id
):
    """
    Return applications submitted by a candidate.
    """

    query = """
    SELECT

        a.id,
        a.job_id,
        a.user_id,
        j.title,
        j.company,
        j.location,
        a.match_percentage,
        a.ats_score,
        a.status,
        a.applied_at,
        a.recommendation

    FROM applications a

    JOIN jobs j
        ON a.job_id = j.id

    WHERE a.user_id = ?

    ORDER BY a.applied_at DESC
    """

    return fetch_all(
        query,
        (user_id,)
    )


# =====================================================
# EMPLOYER APPLICATIONS
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_applications_by_employer(
    employer_id
):
    """
    Return all applications received
    by an employer.
    """

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

    return fetch_all(
        query,
        (employer_id,)
    )


# =====================================================
# UPDATE APPLICATION STATUS
# =====================================================

def update_application_status(
    application_id,
    status,
    user_id=None
):
    """
    Update application status.

    If user_id is provided, it is used to ensure
    that the employer can only update applications
    belonging to their own jobs.
    """

    try:

        # -------------------------------------------------
        # Secure employer ownership check
        # -------------------------------------------------

        if user_id is not None:

            application = fetch_one(
                """
                SELECT
                    a.id

                FROM applications a

                JOIN jobs j
                    ON a.job_id = j.id

                WHERE a.id = ?
                AND j.posted_by = ?
                """,
                (
                    application_id,
                    user_id
                )
            )

            if not application:

                logger.warning(
                    f"Unauthorized application status update. "
                    f"Application ID={application_id}, "
                    f"User ID={user_id}"
                )

                return False

        # -------------------------------------------------
        # Update status
        # -------------------------------------------------

        query = """
        UPDATE applications

        SET status = ?

        WHERE id = ?
        """

        result = execute_query(
            query,
            (
                status,
                application_id
            )
        )

        if not result:

            return False

        clear_cache()

        # -------------------------------------------------
        # Audit activity
        # -------------------------------------------------

        if user_id is not None:

            log_activity(
                user_id=user_id,
                action="APPLICATION_STATUS_UPDATE",
                description=(
                    f"Application {application_id} "
                    f"status changed to {status}."
                )
            )

        logger.info(
            f"Application {application_id} "
            f"updated to {status}."
        )

        return True

    except Exception:

        logger.exception(
            "Unable to update application."
        )

        return False


# =====================================================
# TOTAL APPLICATIONS
# =====================================================

@st.cache_data(
    ttl=30,
    show_spinner=False
)
def total_applications(
    employer_id
):
    """
    Return total applications received
    by an employer.
    """

    try:

        query = """
        SELECT
            COUNT(*) AS total

        FROM jobs j

        JOIN applications a
            ON j.id = a.job_id

        WHERE j.posted_by = ?
        """

        row = fetch_one(
            query,
            (employer_id,)
        )

        return (
            row["total"]
            if row
            else 0
        )

    except Exception:

        logger.exception(
            "Unable to calculate total applications."
        )

        return 0


# =====================================================
# DELETE APPLICATION
# =====================================================

def delete_application(
    application_id
):
    """
    Delete an application.
    """

    try:

        success = execute_query(
            """
            DELETE FROM applications
            WHERE id = ?
            """,
            (application_id,)
        )

        if success:

            clear_cache()

            logger.info(
                f"Application deleted: {application_id}"
            )

        return success

    except Exception:

        logger.exception(
            "Unable to delete application."
        )

        return False


# =====================================================
# APPLICATIONS BY JOB
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_applications_by_job(
    job_id
):
    """
    Return applications for a specific job.
    """

    try:

        query = """
        SELECT

            a.*,

            u.id AS candidate_id,
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

        return fetch_all(
            query,
            (job_id,)
        )

    except Exception:

        logger.exception(
            "Unable to fetch job applications."
        )

        return []


# =====================================================
# CANDIDATE APPLICATIONS
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_candidate_applications(
    candidate_id
):
    """
    Return all applications submitted
    by one candidate.
    """

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

        return fetch_all(
            query,
            (candidate_id,)
        )

    except Exception:

        logger.exception(
            "Unable to fetch candidate applications."
        )

        return []


# =====================================================
# GET APPLICATION BY ID
# =====================================================

@st.cache_data(
    ttl=300,
    show_spinner=False
)
def get_application_by_id(
    application_id
):
    """
    Return a single application with
    candidate and employer information.
    """

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

        return fetch_one(
            query,
            (application_id,)
        )

    except Exception:

        logger.exception(
            "Unable to fetch application."
        )

        return None


# =====================================================
# TOGGLE FAVORITE
# =====================================================

def toggle_favorite(
    application_id
):
    """
    Toggle favourite status of an application.
    """

    try:

        query = """
        UPDATE applications

        SET is_favorite =
            CASE
                WHEN is_favorite = 1
                THEN 0
                ELSE 1
            END

        WHERE id = ?
        """

        success = execute_query(
            query,
            (application_id,)
        )

        if success:

            clear_cache()

            logger.info(
                f"Application {application_id} "
                f"favorite toggled."
            )

        return success

    except Exception:

        logger.exception(
            "Unable to toggle favorite."
        )

        return False

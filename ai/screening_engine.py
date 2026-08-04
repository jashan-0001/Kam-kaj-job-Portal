import streamlit as st

from ai.ats_score import (
    calculate_skill_match,
    calculate_ats_score
)

from utils.logger import logger


# =====================================================
# CACHE MANAGEMENT
# =====================================================

def clear_screening_cache():
    """
    Clear cached AI screening results.
    """

    st.cache_data.clear()


# =====================================================
# AI RESUME SCREENING
# =====================================================

@st.cache_data(
    ttl=600,
    show_spinner=False
)
def screen_resume(
    candidate_skills,
    job_skills
):
    """
    Perform AI Resume Screening.

    Returns:
        matched_skills
        missing_skills
        match_percentage
        ats_score
        recommendation
        stars
    """

    try:

        logger.info(
            "Starting AI resume screening."
        )

        # ---------------------------------------------
        # Normalize Skills
        # ---------------------------------------------

        candidate_skills = sorted({

            skill.strip().lower()

            for skill in candidate_skills

            if skill and skill.strip()

        })

        job_skills = sorted({

            skill.strip().lower()

            for skill in job_skills

            if skill and skill.strip()

        })

        # ---------------------------------------------
        # Skill Matching
        # ---------------------------------------------

        match = calculate_skill_match(
            candidate_skills,
            job_skills
        )

        # ---------------------------------------------
        # ATS Score
        # ---------------------------------------------

        ats = calculate_ats_score(
            match["match_percentage"]
        )

        result = {

            "matched_skills":
                match["matched_skills"],

            "missing_skills":
                match["missing_skills"],

            "match_percentage":
                match["match_percentage"],

            "ats_score":
                ats["ats_score"],

            "recommendation":
                ats["recommendation"],

            "stars":
                ats["stars"]

        }

        logger.info(
            f"AI screening completed successfully. ATS Score: {result['ats_score']}"
        )

        return result

    except Exception:

        logger.exception(
            "AI resume screening failed."
        )

        return {

            "matched_skills": [],

            "missing_skills": [],

            "match_percentage": 0,

            "ats_score": 0,

            "recommendation":
                "Unable to analyze the resume.",

            "stars":
                "☆☆☆☆☆"

        }
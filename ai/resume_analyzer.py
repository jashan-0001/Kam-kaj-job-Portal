import streamlit as st

from ai.resume_parser import extract_resume_text
from ai.skill_extractor import extract_resume_details
from ai.education_extractor import extract_education
from ai.experience_extractor import (
    extract_experience,
    extract_years_of_experience
)

from utils.logger import logger


# =====================================================
# CACHE MANAGEMENT
# =====================================================

def clear_resume_analysis_cache():
    """
    Clear cached resume analysis results.
    """

    st.cache_data.clear()


# =====================================================
# ANALYZE RESUME
# =====================================================

@st.cache_data(
    ttl=600,
    show_spinner=False
)
def analyze_resume(pdf_path):
    """
    Analyze a resume and return structured information.
    """

    try:

        logger.info(
            f"Starting resume analysis: {pdf_path}"
        )

        # ---------------------------------------------
        # Validate Input
        # ---------------------------------------------

        if not pdf_path:

            logger.warning(
                "Resume path is empty."
            )

            return None

        # ---------------------------------------------
        # Extract Resume Text
        # ---------------------------------------------

        text = extract_resume_text(pdf_path)

        if not text:

            logger.warning(
                f"No readable text found in resume: {pdf_path}"
            )

            return None

        # ---------------------------------------------
        # Extract Candidate Information
        # ---------------------------------------------

        basic = extract_resume_details(text) or {}

        education = extract_education(text) or []

        experience = extract_experience(text) or []

        years = extract_years_of_experience(text)

        if years is None:
            years = 0

        result = {

            "name":
                basic.get("name", ""),

            "email":
                basic.get("email", ""),

            "phone":
                basic.get("phone", ""),

            "skills":
                basic.get("skills", []),

            "education":
                education,

            "experience":
                experience,

            "years_of_experience":
                years,

            "raw_text":
                text

        }

        logger.info(
            f"Resume analysis completed successfully: {pdf_path}"
        )

        return result

    except Exception:

        logger.exception(
            f"Resume analysis failed: {pdf_path}"
        )

        return None
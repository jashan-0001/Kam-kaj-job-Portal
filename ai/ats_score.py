import streamlit as st


# =====================================================
# CACHE MANAGEMENT
# =====================================================

def clear_ats_cache():
    """
    Clear cached ATS calculation results.
    """

    st.cache_data.clear()


# =====================================================
# SKILL MATCH
# =====================================================

@st.cache_data(
    ttl=600,
    show_spinner=False
)
def calculate_skill_match(
    candidate_skills,
    job_skills
):
    """
    Compare candidate skills with required job skills.
    """

    candidate = {

        skill.strip().lower()

        for skill in candidate_skills

        if skill and skill.strip()

    }

    required = {

        skill.strip().lower()

        for skill in job_skills

        if skill and skill.strip()

    }

    matched = sorted(
        candidate & required
    )

    missing = sorted(
        required - candidate
    )

    if not required:

        percentage = 0

    else:

        percentage = round(

            (len(matched) / len(required)) * 100,

            2

        )

    return {

        "matched_skills":
            matched,

        "missing_skills":
            missing,

        "match_percentage":
            percentage

    }


# =====================================================
# ATS SCORE
# =====================================================

@st.cache_data(
    ttl=600,
    show_spinner=False
)
def calculate_ats_score(match_percentage):
    """
    Calculate ATS Score, Recommendation and Rating.
    """

    score = round(match_percentage)

    if score >= 90:

        recommendation = "Excellent Candidate"

        stars = "★★★★★"

    elif score >= 75:

        recommendation = "Very Good Candidate"

        stars = "★★★★☆"

    elif score >= 60:

        recommendation = "Good Candidate"

        stars = "★★★☆☆"

    elif score >= 40:

        recommendation = "Average Candidate"

        stars = "★★☆☆☆"

    else:

        recommendation = "Needs Improvement"

        stars = "★☆☆☆☆"

    return {

        "ats_score":
            score,

        "recommendation":
            recommendation,

        "stars":
            stars

    }
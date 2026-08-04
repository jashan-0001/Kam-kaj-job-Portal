import re

import streamlit as st


# =====================================================
# EXPERIENCE KEYWORDS
# =====================================================

EXPERIENCE_KEYWORDS = [
    "experience",
    "worked",
    "employment",
    "intern",
    "internship",
    "developer",
    "engineer",
    "analyst",
    "consultant",
    "manager",
    "executive",
    "associate",
    "software",
    "project"
]


# =====================================================
# REGEX PATTERN
# =====================================================

YEARS_PATTERN = re.compile(
    r"(\d+)\+?\s*(?:years?|yrs?)",
    re.IGNORECASE
)


# =====================================================
# CACHE MANAGEMENT
# =====================================================

def clear_experience_cache():
    """
    Clear cached experience extraction results.
    """

    st.cache_data.clear()


# =====================================================
# EXPERIENCE EXTRACTOR
# =====================================================

@st.cache_data(
    ttl=600,
    show_spinner=False
)
def extract_experience(text):
    """
    Extract work experience details from resume text.
    """

    experience = []

    seen = set()

    for line in text.splitlines():

        cleaned = line.strip()

        if not cleaned:
            continue

        lower = cleaned.lower()

        for keyword in EXPERIENCE_KEYWORDS:

            if keyword in lower:

                if cleaned not in seen:

                    experience.append(cleaned)

                    seen.add(cleaned)

                break

    return experience


# =====================================================
# YEARS OF EXPERIENCE
# =====================================================

@st.cache_data(
    ttl=600,
    show_spinner=False
)
def extract_years_of_experience(text):
    """
    Estimate years of experience from resume.
    """

    matches = YEARS_PATTERN.findall(text)

    if not matches:
        return 0

    return max(
        int(year)
        for year in matches
    )
import streamlit as st


# =====================================================
# EDUCATION KEYWORDS
# =====================================================

EDUCATION_KEYWORDS = [
    "b.tech",
    "btech",
    "b.e",
    "be",
    "bca",
    "b.sc",
    "bsc",
    "b.com",
    "bcom",
    "m.tech",
    "mtech",
    "mca",
    "mba",
    "m.sc",
    "msc",
    "phd",
    "diploma",
    "engineering",
    "computer science",
    "information technology",
    "12th",
    "10th",
    "higher secondary",
    "secondary"
]


# =====================================================
# CACHE MANAGEMENT
# =====================================================

def clear_education_cache():
    """
    Clear cached education extraction results.
    """

    st.cache_data.clear()


# =====================================================
# EDUCATION EXTRACTOR
# =====================================================

@st.cache_data(
    ttl=600,
    show_spinner=False
)
def extract_education(text):
    """
    Extract education details from resume text.
    """

    education = []

    seen = set()

    for line in text.splitlines():

        cleaned = line.strip()

        if not cleaned:
            continue

        lower = cleaned.lower()

        for keyword in EDUCATION_KEYWORDS:

            if keyword in lower:

                if cleaned not in seen:

                    education.append(cleaned)

                    seen.add(cleaned)

                break

    return education
import re

import streamlit as st


# =====================================================
# COMMON SKILLS DATABASE
# =====================================================

COMMON_SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "C#",
    "JavaScript",
    "TypeScript",
    "HTML",
    "CSS",
    "SQL",
    "SQLite",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Oracle",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Machine Learning",
    "Deep Learning",
    "Data Analysis",
    "Data Science",
    "Streamlit",
    "Flask",
    "Django",
    "FastAPI",
    "Git",
    "GitHub",
    "Docker",
    "Linux",
    "Excel",
    "Power BI",
    "Tableau"
]


# =====================================================
# CACHE MANAGEMENT
# =====================================================

def clear_skill_cache():
    """
    Clear cached skill extraction results.
    """

    st.cache_data.clear()


# =====================================================
# SKILL EXTRACTION
# =====================================================

@st.cache_data(
    ttl=600,
    show_spinner=False
)
def extract_resume_details(text):
    """
    Extract candidate details from resume text.

    Returns:
        name
        email
        phone
        skills
    """

    data = {

        "name": "",

        "email": "",

        "phone": "",

        "skills": []

    }

    # ---------------------------------------------
    # Name
    # ---------------------------------------------

    lines = [

        line.strip()

        for line in text.splitlines()

        if line.strip()

    ]

    if lines:

        data["name"] = lines[0]

    # ---------------------------------------------
    # Email
    # ---------------------------------------------

    email = re.search(

        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

        text

    )

    if email:

        data["email"] = email.group()

    # ---------------------------------------------
    # Phone
    # ---------------------------------------------

    phone = re.search(

        r"(\+91[- ]?)?[6-9]\d{9}",

        text

    )

    if phone:

        data["phone"] = phone.group()

    # ---------------------------------------------
    # Skills
    # ---------------------------------------------

    lower_text = text.lower()

    found_skills = {

        skill

        for skill in COMMON_SKILLS

        if skill.lower() in lower_text

    }

    data["skills"] = sorted(found_skills)

    return data
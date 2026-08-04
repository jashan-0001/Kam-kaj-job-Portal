import streamlit as st

from ai.skill_gap import generate_dynamic_feedback


def show_ai_report(application):

    st.subheader("🤖 AI Resume Analysis")

    ats_score = application["ats_score"] or 0

    matched = []

    if application["matched_skills"]:
        matched = [
            skill.strip()
            for skill in application["matched_skills"].split(",")
            if skill.strip()
        ]

    missing = []

    if application["missing_skills"]:
        missing = [
            skill.strip()
            for skill in application["missing_skills"].split(",")
            if skill.strip()
        ]

    feedback = generate_dynamic_feedback(
        ats_score,
        matched,
        missing,
        application["title"]
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "ATS Score",
            f"{ats_score}/100"
        )

    with col2:
        st.metric(
            "Recommendation",
            application["recommendation"]
        )

    st.divider()

    st.write("### AI Suggestions")

    for line in feedback:
        st.write(line)
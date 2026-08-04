SKILL_RESOURCES = {

    "python": [
        "Practice Python daily",
        "Build 2-3 Python projects"
    ],

    "sql": [
        "Learn SQL JOINs",
        "Practice SQL queries"
    ],

    "streamlit": [
        "Build Streamlit dashboards",
        "Deploy Streamlit applications"
    ],

    "docker": [
        "Learn Docker fundamentals",
        "Containerize a Python project"
    ],

    "aws": [
        "Learn AWS EC2",
        "Deploy a project on AWS"
    ],

    "git": [
        "Practice Git branching",
        "Push projects to GitHub"
    ],

    "machine learning": [
        "Study Scikit-learn",
        "Build ML prediction projects"
    ]
}


def generate_skill_gap_report(matched_skills, missing_skills):
    """
    Generate AI Skill Gap Analysis.
    """

    report = {

        "strengths": matched_skills,

        "missing_skills": missing_skills,

        "recommendations": []

    }

    for skill in missing_skills:

        key = skill.lower()

        if key in SKILL_RESOURCES:

            report["recommendations"].extend(
                SKILL_RESOURCES[key]
            )

        else:

            report["recommendations"].append(
                f"Learn {skill}"
            )

    return report
def generate_dynamic_feedback(
    ats_score,
    matched_skills,
    missing_skills,
    job_title
):
    """
    Generate job-specific AI recommendations.
    """

    feedback = []

    feedback.append(
        f"You are currently a {ats_score}% match for the '{job_title}' position."
    )

    if matched_skills:

        feedback.append(
            "Your strongest matching skills are:"
        )

        for skill in matched_skills:

            feedback.append(
                f"✓ {skill}"
            )

    if missing_skills:

        feedback.append(
            "To improve your chances:"
        )

        for skill in missing_skills:

            feedback.append(
                f"• Learn {skill} because it is required for this role."
            )

        feedback.append(
            "Build at least one project using these skills."
        )

        feedback.append(
            "Update your resume after gaining experience."
        )

    else:

        feedback.append(
            "Excellent! You already match all required skills."
        )

    estimated_score = min(
        100,
        ats_score + len(missing_skills) * 10
    )

    feedback.append(
        f"Estimated ATS after improvement: {estimated_score}%"
    )

    return feedback
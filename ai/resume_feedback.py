from typing import Dict


def generate_resume_feedback(screening: Dict) -> Dict:
    """
    Generate simple AI feedback from screening results.
    """

    matched = screening.get("matched_skills", [])
    missing = screening.get("missing_skills", [])
    ats = screening.get("ats_score", 0)

    strengths = []

    if matched:
        strengths.append(
            f"Matched skills: {', '.join(matched)}"
        )

    if ats >= 80:
        strengths.append(
            "Excellent ATS compatibility."
        )
    elif ats >= 60:
        strengths.append(
            "Good ATS compatibility."
        )
    else:
        strengths.append(
            "Resume needs improvement."
        )

    suggestions = []

    if missing:
        suggestions.append(
            f"Learn or highlight: {', '.join(missing)}"
        )

    suggestions.append(
        "Use measurable achievements."
    )

    suggestions.append(
        "Keep the resume ATS friendly."
    )

    return {

        "strengths": strengths,

        "missing_skills": missing,

        "suggestions": suggestions,

        "recommendation": screening["recommendation"]

    }
def calculate_confidence(
    ats_score,
    matched_skills,
    missing_skills,
    match_percentage
):
    """
    Calculate AI confidence score.
    """

    ats_score = ats_score or 0
    match_percentage = match_percentage or 0

    matched_count = len(matched_skills)
    missing_count = len(missing_skills)

    confidence = (
        ats_score * 0.45
        + match_percentage * 0.35
        + matched_count * 3
        - missing_count * 4
    )

    confidence = max(0, min(100, round(confidence)))

    return confidence


def generate_interview_recommendation(
    ats_score,
    matched_skills,
    missing_skills,
    match_percentage
):
    """
    Generate AI interview recommendation.
    """

    confidence = calculate_confidence(
        ats_score,
        matched_skills,
        missing_skills,
        match_percentage
    )

    if confidence >= 90:

        status = "Highly Recommended"
        emoji = "🟢"
        action = "Invite for Technical Interview"

    elif confidence >= 70:

        status = "Consider"
        emoji = "🟡"
        action = "Schedule HR Screening"

    else:

        status = "Not Recommended"
        emoji = "🔴"
        action = "Keep in Talent Pool"

    return {
        "status": status,
        "emoji": emoji,
        "confidence": confidence,
        "reason": (
            f"ATS Score: {ats_score}, "
            f"Matched Skills: {len(matched_skills)}, "
            f"Missing Skills: {len(missing_skills)}."
        ),
        "action": action
    }
def compare_candidates(candidate1, candidate2):
    """
    Compare two candidates based on ATS score.
    """

    score1 = candidate1["ats_score"] or 0
    score2 = candidate2["ats_score"] or 0

    if score1 > score2:
        winner = candidate1["full_name"]

    elif score2 > score1:
        winner = candidate2["full_name"]

    else:
        winner = "Tie"

    return {
        "candidate1": candidate1,
        "candidate2": candidate2,
        "winner": winner
    }
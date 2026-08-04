def rank_candidate(applications):
    """
    Rank candidates by ATS score.
    """

    ranked = sorted(
        applications,
        key=lambda x: x["ats_score"] or 0,
        reverse=True
    )

    for index, application in enumerate(ranked, start=1):

        application["rank"] = index

        if index == 1:
            application["badge"] = "🥇"
        elif index == 2:
            application["badge"] = "🥈"
        elif index == 3:
            application["badge"] = "🥉"
        else:
            application["badge"] = f"{index}."

    return ranked
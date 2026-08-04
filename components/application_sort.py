def sort_applications(
    applications,
    sort_by
):

    if sort_by == "ATS Score":

        applications.sort(
            key=lambda x: x["ats_score"] or 0,
            reverse=True
        )

    elif sort_by == "Match %":

        applications.sort(
            key=lambda x: x["match_percentage"] or 0,
            reverse=True
        )

    else:

        applications.sort(
            key=lambda x: x["applied_at"],
            reverse=True
        )

    return applications
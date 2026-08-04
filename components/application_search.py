def filter_applications(
    applications,
    search,
    status
):

    filtered = []

    for app in applications:

        if search:

            if search not in app["full_name"].lower():

                continue

        if status != "All":

            if app["status"] != status:

                continue

        filtered.append(app)

    return filtered
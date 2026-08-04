import streamlit as st
import pandas as pd

from constants import (
    APPLICATION_PENDING,
    APPLICATION_SHORTLISTED,
    APPLICATION_INTERVIEW,
    APPLICATION_REJECTED,
    NOTIFICATION_SUCCESS,
    NOTIFICATION_INFO,
    NOTIFICATION_ERROR
)

from services.application_services import (
    get_applications_by_employer,
    update_application_status,
    get_application_by_id
)

from services.notification_service import (
    create_notification
)

from services.email_notification_service import (
    send_status_email
)

from services.activity_service import (
    add_activity
)
from io import BytesIO

def export_to_excel(df):
    """
    Convert DataFrame to Excel.
    """

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Applications"
        )

    return output.getvalue()

def show_application_management(employer_id):

    st.subheader("📄 Job Applications")

    applications = get_applications_by_employer(
        employer_id
    )

    if not applications:
        st.info("No applications received yet.")
        return

    # --------------------------------------------------
    # Search & Filters
    # --------------------------------------------------

    st.subheader("🔍 Search & Filter")

    search = st.text_input(
        "Search Candidate"
    )

    status_filter = st.selectbox(
        "Application Status",
        [
            "All",
            APPLICATION_PENDING,
            APPLICATION_SHORTLISTED,
            APPLICATION_INTERVIEW,
            APPLICATION_REJECTED
        ]
    )

    ats_filter = st.slider(
        "Minimum ATS Score",
        0,
        100,
        0
    )

    sort_by = st.selectbox(
        "Sort By",
        [
            "Highest ATS",
            "Lowest ATS",
            "Highest Match %",
            "Newest Application",
            "Oldest Application"
        ]
    )

    # --------------------------------------------------
    # Filtering
    # --------------------------------------------------

    filtered = []

    for app in applications:

        if search:

            keyword = search.lower()

            if (
                keyword not in app["full_name"].lower()
                and keyword not in app["email"].lower()
            ):
                continue

        if (
            status_filter != "All"
            and app["status"] != status_filter
        ):
            continue

        if app["ats_score"] < ats_filter:
            continue

        filtered.append(app)

    if not filtered:
        st.info("No candidates match your search.")
        return

    # --------------------------------------------------
    # Sorting
    # --------------------------------------------------

    if sort_by == "Highest ATS":

        filtered.sort(
            key=lambda x: x["ats_score"],
            reverse=True
        )

    elif sort_by == "Lowest ATS":

        filtered.sort(
            key=lambda x: x["ats_score"]
        )

    elif sort_by == "Highest Match %":

        filtered.sort(
            key=lambda x: x["match_percentage"],
            reverse=True
        )

    elif sort_by == "Newest Application":

        filtered.sort(
            key=lambda x: x["applied_at"],
            reverse=True
        )

    elif sort_by == "Oldest Application":

        filtered.sort(
            key=lambda x: x["applied_at"]
        )

    # --------------------------------------------------
    # Data Table
    # --------------------------------------------------

    df = pd.DataFrame(
        [
            {
                "Application ID": app["id"],
                "Candidate": app["full_name"],
                "Email": app["email"],
                "Job": app["title"],
                "ATS Score": app["ats_score"],
                "Match %": app["match_percentage"],
                "Status": app["status"]
            }
            for app in filtered
        ]
    )

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )

    st.divider()

    excel = export_to_excel(df)

    st.download_button(
        "📥 Export to Excel",
        data=excel,
        file_name="applications.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

    # --------------------------------------------------
    # Update Status
    # --------------------------------------------------

    selected = st.selectbox(
        "Select Application",
        df["Application ID"]
    )

    status = st.selectbox(
        "Change Status",
        [
            APPLICATION_PENDING,
            APPLICATION_SHORTLISTED,
            APPLICATION_INTERVIEW,
            APPLICATION_REJECTED
        ]
    )

    if st.button(
        "Update Status",
        use_container_width=True
    ):

        application = get_application_by_id(selected)

        if application is None:
            st.error("Application not found.")
            return

        success = update_application_status(
            selected,
            status
        )

        if not success:
            st.error("Database Error.")
            return

        # --------------------------------------------------
        # Shortlisted
        # --------------------------------------------------

        if status == APPLICATION_SHORTLISTED:

            add_activity(
                application["employer_id"],
                f"🟢 {application['full_name']} was shortlisted for {application['title']}."
            )

            create_notification(
                user_id=application["user_id"],
                title="🎉 Application Shortlisted",
                message=f"Congratulations! You have been shortlisted for {application['title']}.",
                notification_type=NOTIFICATION_SUCCESS
            )

        # --------------------------------------------------
        # Interview
        # --------------------------------------------------

        elif status == APPLICATION_INTERVIEW:

            add_activity(
                application["employer_id"],
                f"📅 Interview scheduled with {application['full_name']} for {application['title']}."
            )

            create_notification(
                user_id=application["user_id"],
                title="📅 Interview Scheduled",
                message=f"Your interview has been scheduled for {application['title']}.",
                notification_type=NOTIFICATION_INFO
            )

        # --------------------------------------------------
        # Rejected
        # --------------------------------------------------

        elif status == APPLICATION_REJECTED:

            add_activity(
                application["employer_id"],
                f"❌ {application['full_name']} was rejected for {application['title']}."
            )

            create_notification(
                user_id=application["user_id"],
                title="❌ Application Update",
                message=f"Your application for {application['title']} was not selected.",
                notification_type=NOTIFICATION_ERROR
            )

        # --------------------------------------------------
        # Pending
        # --------------------------------------------------

        else:

            add_activity(
                application["employer_id"],
                f"Application status changed to {APPLICATION_PENDING}."
            )

            create_notification(
                user_id=application["user_id"],
                title="📄 Application Updated",
                message=f"Your application status has been updated to {APPLICATION_PENDING}.",
                notification_type=NOTIFICATION_INFO
            )

        # --------------------------------------------------
        # Send Email
        # --------------------------------------------------

        send_status_email(
            application,
            status
        )

        st.success(
            "Application Updated Successfully."
        )

        st.rerun()
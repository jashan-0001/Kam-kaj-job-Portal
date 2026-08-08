import streamlit as st
import pandas as pd
from io import BytesIO

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


# =====================================================
# EXPORT TO EXCEL
# =====================================================

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


# =====================================================
# APPLICATION MANAGEMENT
# =====================================================

def show_application_management(
    employer_id
):
    """
    Display and manage applications received
    by an employer.
    """

    st.subheader(
        "📄 Job Applications"
    )

    applications = get_applications_by_employer(
        employer_id
    )

    if not applications:

        st.info(
            "No applications received yet."
        )

        return

    # =================================================
    # SEARCH & FILTERS
    # =================================================

    st.subheader(
        "🔍 Search & Filter"
    )

    col1, col2 = st.columns(2)

    with col1:

        search = st.text_input(
            "Search Candidate",
            placeholder="Name or email..."
        ).strip().lower()

    with col2:

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

    col3, col4 = st.columns(2)

    with col3:

        ats_filter = st.slider(
            "Minimum ATS Score",
            min_value=0,
            max_value=100,
            value=0
        )

    with col4:

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

    # =================================================
    # FILTER APPLICATIONS
    # =================================================

    filtered = []

    for application in applications:

        full_name = str(
            application.get(
                "full_name",
                ""
            )
        ).lower()

        email = str(
            application.get(
                "email",
                ""
            )
        ).lower()

        status = application.get(
            "status"
        )

        ats_score = float(
            application.get(
                "ats_score",
                0
            ) or 0
        )

        # ---------------------------------------------
        # Search
        # ---------------------------------------------

        if search:

            if (
                search not in full_name
                and search not in email
            ):

                continue

        # ---------------------------------------------
        # Status
        # ---------------------------------------------

        if (
            status_filter != "All"
            and status != status_filter
        ):

            continue

        # ---------------------------------------------
        # ATS
        # ---------------------------------------------

        if ats_score < ats_filter:

            continue

        filtered.append(
            application
        )

    if not filtered:

        st.info(
            "No candidates match your search."
        )

        return

    # =================================================
    # SORTING
    # =================================================

    if sort_by == "Highest ATS":

        filtered.sort(
            key=lambda x: float(
                x.get("ats_score", 0) or 0
            ),
            reverse=True
        )

    elif sort_by == "Lowest ATS":

        filtered.sort(
            key=lambda x: float(
                x.get("ats_score", 0) or 0
            )
        )

    elif sort_by == "Highest Match %":

        filtered.sort(
            key=lambda x: float(
                x.get(
                    "match_percentage",
                    0
                ) or 0
            ),
            reverse=True
        )

    elif sort_by == "Newest Application":

        filtered.sort(
            key=lambda x: (
                x.get("applied_at")
                or ""
            ),
            reverse=True
        )

    elif sort_by == "Oldest Application":

        filtered.sort(
            key=lambda x: (
                x.get("applied_at")
                or ""
            )
        )

    # =================================================
    # DATA TABLE
    # =================================================

    df = pd.DataFrame(
        [
            {
                "Application ID": application["id"],
                "Candidate": application["full_name"],
                "Email": application["email"],
                "Job": application["title"],
                "ATS Score": application["ats_score"],
                "Match %": application["match_percentage"],
                "Status": application["status"]
            }

            for application in filtered
        ]
    )

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )

    # =================================================
    # EXPORT
    # =================================================

    st.divider()

    excel = export_to_excel(
        df
    )

    st.download_button(
        "📥 Export to Excel",
        data=excel,
        file_name="applications.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        use_container_width=True
    )

    # =================================================
    # UPDATE APPLICATION STATUS
    # =================================================

    st.divider()

    st.subheader(
        "🔄 Update Application Status"
    )

    application_ids = [
        application["id"]
        for application in filtered
    ]

    selected_application_id = st.selectbox(
        "Select Application",
        options=application_ids,
        key="application_status_selection",
        format_func=lambda application_id: next(
            (
                f"{application['full_name']} — "
                f"{application['title']} "
                f"(ID: {application_id})"
                for application in filtered
                if application["id"] == application_id
            ),
            str(application_id)
        )
    )

    status = st.selectbox(
        "Change Status",
        [
            APPLICATION_PENDING,
            APPLICATION_SHORTLISTED,
            APPLICATION_INTERVIEW,
            APPLICATION_REJECTED
        ],
        key="application_status"
    )

    if st.button(
        "Update Status",
        use_container_width=True,
        type="primary"
    ):

        # ---------------------------------------------
        # Get application
        # ---------------------------------------------

        application = get_application_by_id(
            selected_application_id
        )

        if application is None:

            st.error(
                "Application not found."
            )

            return

        # ---------------------------------------------
        # Verify employer ownership
        # ---------------------------------------------

        if application.get(
            "employer_id"
        ) != employer_id:

            st.error(
                "You are not authorized to update "
                "this application."
            )

            return

        # ---------------------------------------------
        # Update database
        # ---------------------------------------------

        success = update_application_status(
            selected_application_id,
            status,
            employer_id
        )

        if not success:

            st.error(
                "Database Error or unauthorized request."
            )

            return

        # =================================================
        # SHORTLISTED
        # =================================================

        if status == APPLICATION_SHORTLISTED:

            add_activity(
                employer_id,
                (
                    f"🟢 {application['full_name']} "
                    f"was shortlisted for "
                    f"{application['title']}."
                )
            )

            create_notification(
                user_id=application["user_id"],
                title="🎉 Application Shortlisted",
                message=(
                    f"Congratulations! You have been "
                    f"shortlisted for "
                    f"{application['title']}."
                ),
                notification_type=NOTIFICATION_SUCCESS
            )

        # =================================================
        # INTERVIEW
        # =================================================

        elif status == APPLICATION_INTERVIEW:

            add_activity(
                employer_id,
                (
                    f"📅 Interview scheduled with "
                    f"{application['full_name']} "
                    f"for {application['title']}."
                )
            )

            create_notification(
                user_id=application["user_id"],
                title="📅 Interview Scheduled",
                message=(
                    f"Your interview has been scheduled "
                    f"for {application['title']}."
                ),
                notification_type=NOTIFICATION_INFO
            )

        # =================================================
        # REJECTED
        # =================================================

        elif status == APPLICATION_REJECTED:

            add_activity(
                employer_id,
                (
                    f"❌ {application['full_name']} "
                    f"was rejected for "
                    f"{application['title']}."
                )
            )

            create_notification(
                user_id=application["user_id"],
                title="❌ Application Update",
                message=(
                    f"Your application for "
                    f"{application['title']} "
                    f"was not selected."
                ),
                notification_type=NOTIFICATION_ERROR
            )

        # =================================================
        # PENDING
        # =================================================

        else:

            add_activity(
                employer_id,
                (
                    f"Application status changed "
                    f"to {APPLICATION_PENDING} "
                    f"for {application['full_name']}."
                )
            )

            create_notification(
                user_id=application["user_id"],
                title="📄 Application Updated",
                message=(
                    f"Your application status has been "
                    f"updated to {APPLICATION_PENDING}."
                ),
                notification_type=NOTIFICATION_INFO
            )

        # =================================================
        # SEND EMAIL
        # =================================================

        email_success = send_status_email(
            application,
            status
        )

        if not email_success:

            st.warning(
                "Application status was updated, "
                "but the email notification could not "
                "be sent."
            )

        else:

            st.success(
                "Application status updated and "
                "candidate notified successfully."
            )

        st.rerun()


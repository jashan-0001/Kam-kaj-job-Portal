import streamlit as st
import pandas as pd

from constants import (
    JOB_OPEN,
    JOB_CLOSED
)

from services.job_service import (
    get_jobs_by_employer,
    get_job_by_id,
    update_job,
    delete_job,
    close_job,
    reopen_job
)

from services.audit_service import log_activity
from utils.logger import logger


# ============================================================
# JOB MANAGEMENT
# ============================================================

def show_job_management(user_id):
    """
    Display and manage jobs posted by the current employer.
    """

    st.subheader("📋 My Posted Jobs")

    try:

        # ====================================================
        # GET EMPLOYER JOBS
        # ====================================================

        jobs = get_jobs_by_employer(user_id)

        if not jobs:

            st.info(
                "No jobs have been posted yet."
            )

            return

        # ====================================================
        # SEARCH
        # ====================================================

        search = st.text_input(
            "🔍 Search Job",
            placeholder="Search by title or company..."
        ).strip().lower()

        filtered_jobs = []

        for job in jobs:

            title = str(
                job.get("title", "")
            ).lower()

            company = str(
                job.get("company", "")
            ).lower()

            if (
                not search
                or search in title
                or search in company
            ):
                filtered_jobs.append(job)

        if not filtered_jobs:

            st.warning(
                "No matching jobs found."
            )

            return

        # ====================================================
        # DATA TABLE
        # ====================================================

        table = [
            {
                "ID": job["id"],
                "Title": job["title"],
                "Company": job["company"],
                "Location": job["location"],
                "Experience": job["experience"],
                "Salary": job["salary"],
                "Status": job["status"]
            }
            for job in filtered_jobs
        ]

        df = pd.DataFrame(table)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # ====================================================
        # SELECT JOB
        # ====================================================

        job_options = df["ID"].tolist()

        def job_label(job_id):

            for job in filtered_jobs:

                if job["id"] == job_id:

                    return (
                        f"{job['title']} "
                        f"({job['company']})"
                    )

            return str(job_id)

        # ====================================================
        # EDIT JOB
        # ====================================================

        st.subheader("✏️ Edit Job")

        selected_job_id = st.selectbox(
            "Select Job to Edit",
            options=job_options,
            key="edit_job",
            format_func=job_label
        )

        job = get_job_by_id(
            selected_job_id
        )

        if job:

            with st.form(
                "edit_job_form"
            ):

                title = st.text_input(
                    "Job Title",
                    value=job["title"]
                )

                company = st.text_input(
                    "Company",
                    value=job["company"]
                )

                location = st.text_input(
                    "Location",
                    value=job["location"]
                )

                experience_options = [
                    "Fresher",
                    "0-1 Years",
                    "1-3 Years",
                    "3-5 Years",
                    "5+ Years"
                ]

                current_experience = job.get(
                    "experience",
                    "Fresher"
                )

                experience_index = (
                    experience_options.index(
                        current_experience
                    )
                    if current_experience
                    in experience_options
                    else 0
                )

                experience = st.selectbox(
                    "Experience",
                    experience_options,
                    index=experience_index
                )

                salary = st.text_input(
                    "Salary",
                    value=job["salary"]
                )

                skills = st.text_area(
                    "Skills",
                    value=job["skills"],
                    height=120
                )

                description = st.text_area(
                    "Description",
                    value=job["description"],
                    height=220
                )

                update = st.form_submit_button(
                    "💾 Update Job",
                    use_container_width=True
                )

            if update:

                success = update_job(
                    selected_job_id,
                    title.strip(),
                    company.strip(),
                    location.strip(),
                    experience,
                    salary.strip(),
                    skills.strip(),
                    description.strip()
                )

                if success:

                    log_activity(
                        user_id=user_id,
                        action="JOB_UPDATE",
                        description=(
                            f"Updated job: "
                            f"{title.strip()}"
                        )
                    )

                    st.success(
                        "Job updated successfully."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Unable to update job."
                    )

        # ====================================================
        # JOB STATUS MANAGEMENT
        # ====================================================

        st.divider()

        st.subheader("🔒 Job Status")

        status_job_id = st.selectbox(
            "Select Job",
            options=job_options,
            key="status_job",
            format_func=job_label
        )

        selected_job = get_job_by_id(
            status_job_id
        )

        if selected_job:

            current_status = selected_job.get(
                "status",
                JOB_OPEN
            )

            st.write(
                f"**Current Status:** {current_status}"
            )

            col1, col2 = st.columns(2)

            # =================================================
            # CLOSE JOB
            # =================================================

            with col1:

                if (
                    current_status == JOB_OPEN
                    and st.button(
                        "🔒 Close Job",
                        use_container_width=True
                    )
                ):

                    success = close_job(
                        status_job_id
                    )

                    if success:

                        log_activity(
                            user_id=user_id,
                            action="JOB_CLOSE",
                            description=(
                                f"Closed job: "
                                f"{selected_job['title']}"
                            )
                        )

                        st.success(
                            "Job closed successfully."
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Unable to close job."
                        )

            # =================================================
            # REOPEN JOB
            # =================================================

            with col2:

                if (
                    current_status == JOB_CLOSED
                    and st.button(
                        "🔓 Reopen Job",
                        use_container_width=True
                    )
                ):

                    success = reopen_job(
                        status_job_id
                    )

                    if success:

                        log_activity(
                            user_id=user_id,
                            action="JOB_REOPEN",
                            description=(
                                f"Reopened job: "
                                f"{selected_job['title']}"
                            )
                        )

                        st.success(
                            "Job reopened successfully."
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Unable to reopen job."
                        )

            # =================================================
            # DELETE JOB
            # =================================================

            st.divider()

            st.subheader("🗑️ Delete Job")

            delete_job_id = st.selectbox(
                "Select Job to Delete",
                options=job_options,
                key="delete_job",
                format_func=job_label
            )

            delete_confirmation = st.checkbox(
                "I understand that deleting this job "
                "may also delete its related applications."
            )

            if st.button(
                "🗑️ Delete Selected Job",
                type="primary",
                use_container_width=True
            ):

                if not delete_confirmation:

                    st.warning(
                        "Please confirm that you want "
                        "to delete this job."
                    )

                    return

                try:

                    selected_job_details = get_job_by_id(
                        delete_job_id
                    )

                    success = delete_job(
                        delete_job_id
                    )

                    if success:

                        logger.info(
                            f"Job ID={delete_job_id} "
                            f"deleted by Employer ID={user_id}"
                        )

                        job_title = (
                            selected_job_details["title"]
                            if selected_job_details
                            else f"Job ID {delete_job_id}"
                        )

                        log_activity(
                            user_id=user_id,
                            action="JOB_DELETE",
                            description=(
                                f"Deleted job: "
                                f"{job_title}"
                            )
                        )

                        st.success(
                            "Job deleted successfully."
                        )

                        st.rerun()

                    else:

                        logger.warning(
                            f"Failed deleting "
                            f"Job ID={delete_job_id}"
                        )

                        st.error(
                            "Unable to delete the job."
                        )

                except Exception:

                    logger.exception(
                        "Unexpected error while deleting job."
                    )

                    st.error(
                        "Something went wrong while deleting job."
                    )

    except Exception:

        logger.exception(
            "Unexpected error loading job management."
        )

        st.error(
            "Unable to load job management."
        )

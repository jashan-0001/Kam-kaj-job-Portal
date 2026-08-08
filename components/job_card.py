import streamlit as st

from constants import JOB_OPEN

from services.saved_job_service import (
    save_job,
    unsave_job,
    is_saved
)

from services.application_services import (
    save_resume,
    already_applied,
    apply_job
)

from utils.file_validator import (
    validate_resume
)


# ============================================================
# JOB CARD
# ============================================================

def show_job_card(job, user_id):
    """
    Display a professional job card with:

    - Job information
    - Save / Unsave functionality
    - Resume upload
    - Duplicate application checking
    - AI-powered application screening
    """

    if not job:
        return

    job_id = job.get("id")

    if job_id is None:
        st.error(
            "Invalid job information."
        )
        return

    with st.container(border=True):

        # ====================================================
        # JOB TITLE
        # ====================================================

        st.subheader(
            f"💼 {job.get('title', 'Untitled Job')}"
        )

        # ====================================================
        # COMPANY
        # ====================================================

        st.markdown(
            f"**🏢 Company:** "
            f"{job.get('company', 'Unknown Company')}"
        )

        col1, col2 = st.columns(2)

        # ====================================================
        # JOB DETAILS
        # ====================================================

        with col1:

            st.write(
                f"📍 Location: "
                f"{job.get('location', 'Not specified')}"
            )

            st.write(
                f"💼 Experience: "
                f"{job.get('experience', 'Not specified')}"
            )

        with col2:

            st.write(
                f"💰 Salary: "
                f"{job.get('salary', 'Not specified')}"
            )

            status = job.get(
                "status",
                JOB_OPEN
            )

            if status == JOB_OPEN:

                st.success(
                    "🟢 Open"
                )

            else:

                st.error(
                    "🔴 Closed"
                )

        # ====================================================
        # REQUIRED SKILLS
        # ====================================================

        st.markdown(
            "### 🛠 Required Skills"
        )

        st.info(
            job.get(
                "skills",
                "No specific skills listed."
            )
        )

        # ====================================================
        # JOB DESCRIPTION
        # ====================================================

        st.markdown(
            "### 📄 Job Description"
        )

        st.write(
            job.get(
                "description",
                "No description available."
            )
        )

        st.divider()

        # ====================================================
        # SAVE / UNSAVE JOB
        # ====================================================

        saved = is_saved(
            user_id,
            job_id
        )

        if saved:

            if st.button(
                "💔 Remove from Saved Jobs",
                key=f"unsave_{job_id}",
                use_container_width=True
            ):

                success = unsave_job(
                    user_id,
                    job_id
                )

                if success:

                    st.success(
                        "Removed from Saved Jobs."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Unable to remove saved job."
                    )

        else:

            if st.button(
                "❤️ Save Job",
                key=f"save_{job_id}",
                use_container_width=True
            ):

                success = save_job(
                    user_id,
                    job_id
                )

                if success:

                    st.success(
                        "Job Saved."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Unable to save job."
                    )

        # ====================================================
        # ONLY OPEN JOBS CAN ACCEPT APPLICATIONS
        # ====================================================

        if status != JOB_OPEN:

            st.warning(
                "This job is currently closed "
                "and is not accepting applications."
            )

            return

        # ====================================================
        # CHECK DUPLICATE APPLICATION
        # ====================================================

        existing_application = already_applied(
            job_id,
            user_id
        )

        if existing_application:

            st.success(
                "✅ Already Applied"
            )

            return

        # ====================================================
        # RESUME UPLOAD
        # ====================================================

        resume = st.file_uploader(
            "Upload Resume (PDF only)",
            type=["pdf"],
            key=f"resume_{job_id}"
        )

        # ====================================================
        # APPLY NOW
        # ====================================================

        if st.button(
            "🚀 Apply Now",
            key=f"apply_{job_id}",
            use_container_width=True
        ):

            # ------------------------------------------------
            # Validate Resume
            # ------------------------------------------------

            is_valid, error = validate_resume(
                resume
            )

            if not is_valid:

                st.error(
                    error
                )

                return

            # ------------------------------------------------
            # Save Resume
            # ------------------------------------------------

            resume_path = save_resume(
                resume
            )

            if resume_path is None:

                st.error(
                    "Unable to save resume."
                )

                return

            # ------------------------------------------------
            # Submit Application
            # ------------------------------------------------

            success = apply_job(
                job_id,
                user_id,
                resume_path
            )

            if success:

                st.success(
                    "Application submitted successfully."
                )

                st.balloons()

                st.rerun()

            else:

                st.error(
                    "Unable to submit application."
                )

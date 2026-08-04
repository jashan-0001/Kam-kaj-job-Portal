import streamlit as st

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


def show_job_card(job, user_id):
    """
    Display a professional job card with
    resume upload and apply functionality.
    """

    with st.container(border=True):

        st.subheader(f"💼 {job['title']}")

        st.markdown(f"**🏢 Company:** {job['company']}")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"📍 Location: {job['location']}")
            st.write(f"💼 Experience: {job['experience']}")

        with col2:
            st.write(f"💰 Salary: {job['salary']}")

            status = job["status"] if "status" in job.keys() else "Open"

            if status == "Open":
                st.success("🟢 Open")
            else:
                st.error("🔴 Closed")

        st.markdown("### 🛠 Required Skills")
        st.info(job["skills"])

        st.markdown("### 📄 Job Description")
        st.write(job["description"])

        st.divider()

        # ============================================
        # Save / Unsave Job
        # ============================================

        saved = is_saved(user_id, job["id"])

        if saved:

            if st.button(
                "💔 Remove from Saved Jobs",
                key=f"unsave_{job['id']}"
            ):

                unsave_job(
                    user_id,
                    job["id"]
                )

                st.success("Removed from Saved Jobs.")

                st.rerun()

        else:

            if st.button(
                "❤️ Save Job",
                key=f"save_{job['id']}"
            ):

                save_job(
                    user_id,
                    job["id"]
                )

                st.success("Job Saved.")

                st.rerun()

        # ============================================
        # Resume Upload
        # ============================================

        resume = st.file_uploader(
            "Upload Resume (PDF only)",
            type=["pdf"],
            key=f"resume_{job['id']}"
        )

        # ============================================
        # Duplicate Check
        # ============================================

        if already_applied(
            job["id"],
            user_id
        ):

            st.success("✅ Already Applied")

            return

        # ============================================
        # Apply
        # ============================================

        if st.button(
            "🚀 Apply Now",
            key=f"apply_{job['id']}",
            use_container_width=True
        ):

            is_valid, error = validate_resume(
                resume
            )

            if not is_valid:

                st.error(error)

                return

            resume_path = save_resume(
                resume
            )

            if resume_path is None:

                st.error(
                    "Unable to save resume."
                )

                return

            success = apply_job(
                job["id"],
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
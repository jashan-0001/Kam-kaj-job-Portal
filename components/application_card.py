import os
import streamlit as st

from ai.interview_recommendation import (
    generate_interview_recommendation
)

from services.application_services import (
    update_application_status
)

from services.email_notification_service import (
    send_status_email
)

from services.notification_service import (
    create_notification
)

from services.activity_service import (
    add_activity
)
from constants import (
    APPLICATION_PENDING,
    APPLICATION_SHORTLISTED,
    APPLICATION_INTERVIEW,
    APPLICATION_REJECTED,
    NOTIFICATION_SUCCESS,
    NOTIFICATION_INFO,
    NOTIFICATION_ERROR
)
def show_application_card(application):
    """
    Display one application card.
    """

    ats = application["ats_score"] or 0

    matched_skills = [
        s.strip()
        for s in (application["matched_skills"] or "").split(",")
        if s.strip()
    ]

    missing_skills = [
        s.strip()
        for s in (application["missing_skills"] or "").split(",")
        if s.strip()
    ]

    match_percentage = application["match_percentage"] or 0

    interview_ai = generate_interview_recommendation(
        ats_score=ats,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        match_percentage=match_percentage
    )

    # ==========================================================
    # Candidate Rank
    # ==========================================================

    st.markdown(
        f"## {application['badge']} Rank #{application['rank']}"
    )

    if ats >= 90:
        st.success("🥇 TOP CANDIDATE")
    elif ats >= 75:
        st.info("🥈 STRONG CANDIDATE")
    elif ats >= 60:
        st.warning("🥉 GOOD CANDIDATE")
    else:
        st.error("⚠ Needs Improvement")

    st.subheader(application["full_name"])
    st.caption(application["email"])

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        st.metric("🎯 ATS Score", f"{ats}/100")

    with c2:
        st.metric("📊 Match %", f"{match_percentage}%")

    st.success(
        f"🤖 AI Resume Recommendation\n\n"
        f"{application['recommendation']}"
    )

    # ==========================================================
    # Interview Recommendation
    # ==========================================================

    st.divider()

    st.subheader("🤖 AI Interview Recommendation")

    if interview_ai["status"] == "Highly Recommended":
        st.success(
            f"{interview_ai['emoji']} {interview_ai['status']}"
        )
    elif interview_ai["status"] == "Consider":
        st.warning(
            f"{interview_ai['emoji']} {interview_ai['status']}"
        )
    else:
        st.error(
            f"{interview_ai['emoji']} {interview_ai['status']}"
        )

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Confidence",
            f"{interview_ai['confidence']}%"
        )

    with c2:
        st.metric(
            "Match %",
            f"{match_percentage}%"
        )

    st.info(f"**Reason:** {interview_ai['reason']}")
    st.success(f"**Recommended Action:** {interview_ai['action']}")

    st.divider()

    # ==========================================================
    # Skills
    # ==========================================================

    st.write("### ✅ Matched Skills")

    if matched_skills:

        cols = st.columns(3)

        for i, skill in enumerate(matched_skills):
            cols[i % 3].success(skill)

    else:
        st.info("No matched skills found.")

    st.divider()

    st.write("### ❌ Missing Skills")

    if missing_skills:

        cols = st.columns(3)

        for i, skill in enumerate(missing_skills):
            cols[i % 3].error(skill)

    else:
        st.success("Perfect Skill Match 🎉")

    st.divider()

    # ==========================================================
    # Resume
    # ==========================================================

    resume_path = application["resume_path"]

    if resume_path and os.path.exists(resume_path):

        with open(resume_path, "rb") as pdf:

            st.download_button(
                "📄 Download Resume",
                pdf,
                os.path.basename(resume_path),
                mime="application/pdf",
                key=f"resume_{application['id']}",
                use_container_width=True
            )

    else:
        st.warning("Resume not found.")

    # ==========================================================
    # Status
    # ==========================================================

    st.divider()

    st.write("### 📌 Application Status")

    status = application["status"]

    if status == APPLICATION_PENDING:
        st.warning(status)

    elif status == APPLICATION_SHORTLISTED:
        st.success(status)

    elif status == APPLICATION_INTERVIEW:
        st.info(status)

    elif status == APPLICATION_REJECTED:
        st.error(status)

    st.divider()

    # ==========================================================
    # Recruiter Actions
    # ==========================================================

    st.subheader("📋 Recruiter Actions")

    c1, c2, c3 = st.columns(3)

    # ==========================================================
    # SHORTLIST
    # ==========================================================

    with c1:

        if st.button(
            "🟢 Shortlist",
            key=f"short_{application['id']}",
            use_container_width=True
        ):

            if update_application_status(
                application["id"],
                APPLICATION_SHORTLISTED
            ):

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

                send_status_email(
                    application,
                    "Shortlisted"
             )

            st.success("Candidate shortlisted successfully.")

    st.rerun()
    # ==========================================================
    # INTERVIEW
    # ==========================================================

    with c2:

        if st.button(
            "📅 Interview",
            key=f"interview_{application['id']}",
            use_container_width=True
        ):

            if update_application_status(
                application["id"],
                APPLICATION_INTERVIEW
            ):

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

                send_status_email(
                    application,
                    "Interview Scheduled"
                )

                st.success("Interview scheduled successfully.")

                st.rerun()

            else:
                st.error("Unable to update application.")

    # ==========================================================
    # REJECT
    # ==========================================================

    with c3:

        if st.button(
            "❌ Reject",
            key=f"reject_{application['id']}",
            use_container_width=True
        ):

            if update_application_status(
                application["id"],
                APPLICATION_REJECTED
            ):

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

                send_status_email(
                    application,
                    "Rejected"
                )

                st.success("Candidate rejected successfully.")

                st.rerun()

            else:
                st.error("Unable to update application.")

    st.caption(
        f"Applied On: {application['applied_at']}"
    )
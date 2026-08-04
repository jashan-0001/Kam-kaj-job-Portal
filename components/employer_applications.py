import streamlit as st


from services.application_services import (
    get_applications_by_job
)


from services.audit_service import (
    log_activity
)


from utils.logger import logger


from components.application_card import (
    show_application_card
)


from ai.candidate_ranking import (
    rank_candidate
)


from components.candidate_comparison_panel import (
    show_candidate_comparison_panel
)



def show_employer_applications(
    job_id,
    user_id=None
):
    """
    Display all applications for a selected job.
    """


    try:


        applications = get_applications_by_job(
            job_id
        )


        if not applications:

            st.info(
                "No applications received yet."
            )

            return



        # -----------------------------------------
        # Rank Candidates
        # -----------------------------------------

        applications = rank_candidate(
            applications
        )


        applications = sorted(

            applications,

            key=lambda x: x["ats_score"] or 0,

            reverse=True

        )



        # -----------------------------------------
        # Dashboard Summary
        # -----------------------------------------

        st.subheader(
            f"📥 Applications ({len(applications)})"
        )


        avg_score = round(

            sum(
                app["ats_score"] or 0
                for app in applications
            )
            /
            len(applications),

            2

        )



        col1, col2, col3 = st.columns(
            3
        )


        col1.metric(

            "Applications",

            len(applications)

        )


        col2.metric(

            "Average ATS",

            avg_score

        )


        col3.metric(

            "Best ATS",

            applications[0]["ats_score"] or 0

        )


        st.divider()



        # -----------------------------------------
        # Search Candidate
        # -----------------------------------------

        search = st.text_input(

            "🔍 Search Candidate",

            key=f"search_{job_id}"

        ).strip().lower()



        filtered = []



        for application in applications:


            name = (

                application["full_name"]
                or ""

            ).lower()



            if search:


                if search not in name:

                    continue



            filtered.append(
                application
            )



        if not filtered:


            st.warning(
                "No candidate found."
            )

            return



        # -----------------------------------------
        # Candidate Cards
        # -----------------------------------------

        for application in filtered:


            with st.container():


                show_application_card(
                    application
                )


                st.divider()



        # -----------------------------------------
        # AI Comparison Panel
        # -----------------------------------------

        show_candidate_comparison_panel(
            job_id
        )



    except Exception:


        logger.exception(

            "Unexpected error loading employer applications."

        )


        st.error(

            "Unable to load applications."

        )
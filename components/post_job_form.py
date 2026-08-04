import streamlit as st

from services.job_service import add_job
from services.audit_service import log_activity
from utils.logger import logger



def show_post_job_form(user_id):
    """
    Display the Job Posting Form
    """


    st.subheader(
        "📢 Post New Job"
    )


    with st.form(
        "post_job_form",
        clear_on_submit=True
    ):


        title = st.text_input(
            "Job Title *",
            placeholder="Python Developer"
        )


        company = st.text_input(
            "Company Name *",
            placeholder="Google"
        )


        location = st.text_input(
            "Location *",
            placeholder="Bangalore"
        )


        experience = st.selectbox(
            "Experience Required *",
            [
                "Fresher",
                "0-1 Years",
                "1-3 Years",
                "3-5 Years",
                "5+ Years"
            ]
        )


        salary = st.text_input(
            "Salary",
            placeholder="₹6,00,000 - ₹10,00,000"
        )


        skills = st.text_area(
            "Required Skills *",
            height=120,
            placeholder="Python, SQL, Streamlit, Pandas, Machine Learning"
        )


        description = st.text_area(
            "Job Description *",
            height=220,
            placeholder="Write complete job description..."
        )


        submitted = st.form_submit_button(
            "📢 Post Job",
            use_container_width=True
        )



    if submitted:


        try:


            logger.info(
                f"Employer {user_id} attempted to post a job."
            )


            # -----------------------------
            # Validation
            # -----------------------------

            if not title.strip():

                st.error(
                    "Please enter Job Title."
                )

                return



            if not company.strip():

                st.error(
                    "Please enter Company Name."
                )

                return



            if not location.strip():

                st.error(
                    "Please enter Location."
                )

                return



            if not skills.strip():

                st.error(
                    "Please enter Required Skills."
                )

                return



            if not description.strip():

                st.error(
                    "Please enter Job Description."
                )

                return



            # -----------------------------
            # Create Job
            # -----------------------------

            success = add_job(

                title.strip(),

                company.strip(),

                location.strip(),

                experience,

                salary.strip(),

                skills.strip(),

                description.strip(),

                user_id

            )



            # -----------------------------
            # SUCCESS
            # -----------------------------

            if success:


                logger.info(
                    f"Job posted successfully by Employer ID={user_id}"
                )



                # =============================
                # AUDIT LOG
                # =============================

                log_activity(

                    user_id=user_id,

                    action="JOB_POST",

                    description=(
                        f"Employer posted job: {title.strip()}"
                    )

                )



                st.success(
                    "✅ Job posted successfully."
                )


                st.balloons()


                st.rerun()



            # -----------------------------
            # FAILED
            # -----------------------------

            else:


                logger.warning(
                    f"Job posting failed by Employer ID={user_id}"
                )


                st.error(
                    "Unable to post job."
                )



        except Exception as e:


            logger.exception(
                "Unexpected error while posting job."
            )


            st.error(
                "Something went wrong while posting job."
            )
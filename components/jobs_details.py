import streamlit as st


def show_job_details(job):

    if not job:
        st.warning("No job selected.")
        return

    st.divider()

    st.header("📄 Job Details")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"### {job['title']}")
        st.write(f"🏢 **Company:** {job['company']}")
        st.write(f"📍 **Location:** {job['location']}")
        st.write(f"💰 **Salary:** {job['salary']}")

    with col2:
        st.write(f"💼 **Experience:** {job['experience']}")
        st.write(f"🛠 **Skills:** {job['skills']}")

    st.divider()

    st.subheader("Job Description")

    st.write(job["description"])

    st.divider()

    if st.button(
        "Apply for this Job",
        use_container_width=True
    ):
        st.info(
            "Apply Job feature will be implemented in Lesson 8."
        )
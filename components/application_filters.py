import streamlit as st


def show_application_filters():

    st.subheader("🔍 Recruiter Filters")

    col1, col2, col3 = st.columns(3)

    with col1:

        search = st.text_input(
            "Search Candidate"
        ).strip().lower()

    with col2:

        status = st.selectbox(
            "Status",
            [
                "All",
                "Pending",
                "Shortlisted",
                "Interview Scheduled",
                "Rejected"
            ]
        )

    with col3:

        sort = st.selectbox(
            "Sort By",
            [
                "ATS Score",
                "Match %",
                "Newest"
            ]
        )

    return search, status, sort
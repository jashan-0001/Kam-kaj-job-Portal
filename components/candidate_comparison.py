import streamlit as st

from ai.candidate_comparison import compare_candidates


def show_candidate_comparison(candidate1, candidate2):

    result = compare_candidates(
        candidate1,
        candidate2
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            result["candidate1"]["full_name"]
        )

        st.metric(
            "ATS Score",
            result["candidate1"]["ats_score"]
        )

        st.metric(
            "Match %",
            result["candidate1"]["match_percentage"]
        )

        st.success(
            result["candidate1"]["recommendation"]
        )

    with col2:

        st.subheader(
            result["candidate2"]["full_name"]
        )

        st.metric(
            "ATS Score",
            result["candidate2"]["ats_score"]
        )

        st.metric(
            "Match %",
            result["candidate2"]["match_percentage"]
        )

        st.success(
            result["candidate2"]["recommendation"]
        )

    st.divider()

    if result["winner"] == "Tie":

        st.info("🤝 Both candidates have equal ATS scores.")

    else:

        st.success(
            f"🏆 Recommended Candidate: {result['winner']}"
        )
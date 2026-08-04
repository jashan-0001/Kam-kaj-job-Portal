import streamlit as st


def show_ats_metrics(
    ats_score,
    match_percentage
):

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🎯 ATS Score",
            f"{ats_score}/100"
        )

    with col2:

        st.metric(
            "📊 Match %",
            f"{match_percentage}%"
        )
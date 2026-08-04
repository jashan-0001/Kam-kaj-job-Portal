import streamlit as st


def show_ai_interview_card(result, match_percentage):

    st.subheader(
        "🤖 AI Interview Recommendation"
    )

    status = result["status"]

    if status == "Highly Recommended":

        st.success(
            f"{result['emoji']} {status}"
        )

    elif status == "Consider":

        st.warning(
            f"{result['emoji']} {status}"
        )

    else:

        st.error(
            f"{result['emoji']} {status}"
        )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Confidence",
            f"{result['confidence']}%"
        )

    with col2:

        st.metric(
            "Match %",
            f"{match_percentage}%"
        )

    st.info(
        f"Reason: {result['reason']}"
    )

    st.success(
        f"Action: {result['action']}"
    )
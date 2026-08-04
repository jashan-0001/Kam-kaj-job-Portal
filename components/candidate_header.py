import streamlit as st

from components.favorite_button import (
    show_favorite_button
)


def show_candidate_header(application):
    """
    Display candidate header.
    """

    col1, col2 = st.columns([8, 1])

    with col1:

        st.subheader(
            application["full_name"]
        )

        st.caption(
            application["email"]
        )

    with col2:

        if "is_favorite" in application.keys():
            show_favorite_button(application)
import streamlit as st

from services.application_services import (
    toggle_favorite
)


def show_favorite_button(application):
    """
    Display favorite toggle button.
    """

    favorite = application["is_favorite"]

    icon = "⭐" if favorite else "☆"

    if st.button(
        icon,
        key=f"fav_{application['id']}"
    ):

        toggle_favorite(
            application["id"]
        )

        st.rerun()
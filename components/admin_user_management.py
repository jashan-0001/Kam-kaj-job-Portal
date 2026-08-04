import streamlit as st
import pandas as pd

from services.admin_service import (
    get_all_users,
    delete_user,
    toggle_user_status
)


def show_admin_user_management():

    st.header("👥 User Management")

    users = get_all_users()

    if not users:
        st.info("No users found.")
        return

    # -------------------------
    # Search
    # -------------------------

    search = st.text_input(
        "Search User"
    )

    # -------------------------
    # Role Filter
    # -------------------------

    role = st.selectbox(
        "Filter Role",
        [
            "All",
            "Candidate",
            "Employer",
            "Admin"
        ]
    )

    filtered = []

    for user in users:

        if search:

            keyword = search.lower()

            if (
                keyword not in user["full_name"].lower()
                and
                keyword not in user["email"].lower()
            ):
                continue

        if role != "All":

            if user["role"] != role:
                continue

        filtered.append(user)

    if not filtered:

        st.info("No matching users found.")
        return

    # -------------------------
    # Table
    # -------------------------

    table = []

    for user in filtered:

        table.append(
            {
                "ID": user["id"],
                "Name": user["full_name"],
                "Email": user["email"],
                "Role": user["role"],
                "Status": (
                    "🟢 Active"
                    if user["is_active"]
                    else "🔴 Disabled"
                ),
                "Joined": user["created_at"]
            }
        )

    df = pd.DataFrame(table)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # -------------------------
    # User Actions
    # -------------------------

    selected = st.selectbox(
        "Select User",
        df["ID"]
    )

    selected_user = None

    for user in filtered:

        if user["id"] == selected:

            selected_user = user

            break

    col1, col2 = st.columns(2)

    # -------------------------
    # Activate / Deactivate
    # -------------------------

    with col1:

        button_text = (
            "Deactivate User"
            if selected_user["is_active"]
            else "Activate User"
        )

        if st.button(
            button_text,
            use_container_width=True
        ):

            toggle_user_status(selected)

            st.success(
                "User status updated."
            )

            st.rerun()

    # -------------------------
    # Delete User
    # -------------------------

    with col2:

        if st.button(
            "Delete User",
            use_container_width=True
        ):

            delete_user(selected)

            st.success(
                "User deleted."
            )

            st.rerun()
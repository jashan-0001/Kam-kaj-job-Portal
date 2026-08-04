import pandas as pd
import streamlit as st

from services.audit_service import (
    get_recent_activities,
    total_activities,
    successful_login_count,
    failed_login_count
)

from utils.logger import logger


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Admin Audit Dashboard",
    page_icon="🛡️",
    layout="wide"
)


# =====================================================
# ACCESS CONTROL
# =====================================================

if (
    not st.session_state.get("logged_in")
    or
    st.session_state.get("role") != "Admin"
):

    st.error(
        "⛔ Access denied."
    )

    st.stop()


# =====================================================
# PAGE HEADER
# =====================================================

st.title("🛡️ Admin Audit Dashboard")

st.caption(
    "Monitor user activities, login events, and security logs."
)

st.divider()


try:

    # =====================================================
    # DASHBOARD METRICS
    # =====================================================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Activities",
        total_activities()
    )

    col2.metric(
        "Successful Logins",
        successful_login_count()
    )

    col3.metric(
        "Failed Logins",
        failed_login_count()
    )

    st.divider()

    # =====================================================
    # REFRESH BUTTON
    # =====================================================

    refresh_col1, refresh_col2 = st.columns([1, 5])

    with refresh_col1:

        if st.button(
            "🔄 Refresh",
            use_container_width=True
        ):

            st.cache_data.clear()

            st.rerun()

    # =====================================================
    # LOAD DATA
    # =====================================================

    activities = get_recent_activities()

    if not activities:

        st.info(
            "No audit logs found."
        )

        st.stop()

    df = pd.DataFrame(
        activities
    )

    # =====================================================
    # SEARCH & FILTER
    # =====================================================

    search_col, filter_col = st.columns(
        [3, 1]
    )

    with search_col:

        search = st.text_input(
            "🔍 Search",
            placeholder="Search by user, email, action or description..."
        ).strip().lower()

    with filter_col:

        actions = sorted(
            df["action"].dropna().unique()
        )

        selected_action = st.selectbox(
            "Action",
            ["All"] + list(actions)
        )

    # =====================================================
    # APPLY SEARCH
    # =====================================================

    if search:

        df = df[
            df.astype(str)
              .apply(
                  lambda col: col.str.lower()
              )
              .apply(
                  lambda col: col.str.contains(
                      search,
                      na=False
                  )
              )
              .any(axis=1)
        ]

    # =====================================================
    # APPLY FILTER
    # =====================================================

    if selected_action != "All":

        df = df[
            df["action"] == selected_action
        ]

    # =====================================================
    # COLUMN ORDER
    # =====================================================

    columns = [

        "created_at",

        "full_name",

        "email",

        "role",

        "action",

        "description",

        "ip_address"

    ]

    df = df[
        [
            column
            for column in columns
            if column in df.columns
        ]
    ]

    # =====================================================
    # TOTAL RECORDS
    # =====================================================

    st.caption(
        f"Showing {len(df)} audit record(s)."
    )

    # =====================================================
    # DATA TABLE
    # =====================================================

    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True

    )

except Exception:

    logger.exception(
        "Unable to load Admin Audit Dashboard."
    )

    st.error(
        "Something went wrong while loading the audit dashboard."
    )
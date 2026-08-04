import streamlit as st
import pandas as pd

from services.admin_service import (
    get_role_statistics,
    get_application_statistics,
    get_company_job_statistics
)


def show_admin_analytics():

    st.header("📊 Platform Analytics")

    # --------------------------------------------------
    # Users by Role
    # --------------------------------------------------

    role_data = get_role_statistics()

    if role_data:

        st.subheader("👥 Users by Role")

        df = pd.DataFrame(role_data)

        st.bar_chart(
            df.set_index("role")["total"]
        )

    st.divider()

    # --------------------------------------------------
    # Applications by Status
    # --------------------------------------------------

    app_data = get_application_statistics()

    if app_data:

        st.subheader("📄 Applications by Status")

        df = pd.DataFrame(app_data)

        st.bar_chart(
            df.set_index("status")["total"]
        )

    st.divider()

    # --------------------------------------------------
    # Jobs by Company
    # --------------------------------------------------

    company_data = get_company_job_statistics()

    if company_data:

        st.subheader("💼 Jobs by Company")

        df = pd.DataFrame(company_data)

        st.bar_chart(
            df.set_index("company")["total"]
        )
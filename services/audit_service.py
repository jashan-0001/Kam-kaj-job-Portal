from datetime import datetime

import streamlit as st

from database.database import (
    get_connection,
    fetch_all,
    fetch_one
)


# =====================================================
# ENSURE TABLE COLUMNS
# =====================================================

def ensure_audit_logs_columns(cursor):
    """
    Ensure required audit_logs columns exist
    in PostgreSQL/Supabase.
    """

    cursor.execute("""
        ALTER TABLE audit_logs
        ADD COLUMN IF NOT EXISTS description TEXT
    """)

    cursor.execute("""
        ALTER TABLE audit_logs
        ADD COLUMN IF NOT EXISTS ip_address TEXT
    """)


# =====================================================
# LOG USER ACTIVITY
# =====================================================
def log_activity(
    user_id,
    action,
    description=None,
    ip_address=None
):
    """
    Store activity in audit_logs.
    """

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        # -------------------------------------------------
        # Ensure required columns exist
        # -------------------------------------------------

        ensure_audit_logs_columns(cursor)

        # -------------------------------------------------
        # Insert activity
        # -------------------------------------------------

        cursor.execute(
            """
            INSERT INTO audit_logs
            (
                user_id,
                action,
                description,
                ip_address,
                created_at
            )
            VALUES
            (%s, %s, %s, %s, %s)
            """,
            (
                user_id,
                action,
                description,
                ip_address,
                datetime.now()
            )
        )

        conn.commit()

    except Exception:

        if conn:

            try:
                conn.rollback()

            except Exception:
                pass

        raise

    finally:

        if conn:

            try:
                conn.close()

            except Exception:
                pass


# =====================================================
# RECENT ACTIVITIES
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_recent_activities(limit=100):
    """
    Return recent audit activities.
    """

    query = """
    SELECT

        a.id,
        a.user_id,
        a.action,
        a.description,
        a.ip_address,
        a.created_at,

        u.full_name,
        u.email,
        u.role

    FROM audit_logs a

    LEFT JOIN users u
    ON a.user_id = u.id

    ORDER BY a.created_at DESC

    LIMIT ?
    """

    return fetch_all(
        query,
        (limit,)
    )


# =====================================================
# TOTAL ACTIVITIES
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def total_activities():

    row = fetch_one(
        """
        SELECT
            COUNT(*) AS total
        FROM audit_logs
        """
    )

    return row["total"] if row else 0


# =====================================================
# SUCCESSFUL LOGINS
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def successful_login_count():

    row = fetch_one(
        """
        SELECT
            COUNT(*) AS total
        FROM audit_logs
        WHERE action = 'LOGIN_SUCCESS'
        """
    )

    return row["total"] if row else 0


# =====================================================
# FAILED LOGINS
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def failed_login_count():

    row = fetch_one(
        """
        SELECT
            COUNT(*) AS total
        FROM audit_logs
        WHERE action = 'LOGIN_FAILED'
        """
    )

    return row["total"] if row else 0


# =====================================================
# ACTIVITIES BY ACTION
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_activities_by_action(action):
    """
    Return all audit records
    for one action.
    """

    query = """
    SELECT *

    FROM audit_logs

    WHERE action = ?

    ORDER BY created_at DESC
    """

    return fetch_all(
        query,
        (action,)
    )


# =====================================================
# USER ACTIVITY
# =====================================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_user_activity(user_id):
    """
    Return activity history
    of one user.
    """

    query = """
    SELECT *

    FROM audit_logs

    WHERE user_id = ?

    ORDER BY created_at DESC
    """

    return fetch_all(
        query,
        (user_id,)
    )

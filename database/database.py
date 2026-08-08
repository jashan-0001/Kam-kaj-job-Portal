import os
import sys

from contextlib import contextmanager
from typing import Any, Dict, List, Optional

import psycopg
from psycopg.rows import dict_row

# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from config import SUPABASE_DATABASE_URL
from utils.logger import logger


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Create a PostgreSQL connection to Supabase.
    """

    if not SUPABASE_DATABASE_URL:
        raise RuntimeError(
            "SUPABASE_DATABASE_URL is not configured."
        )

    try:

        conn = psycopg.connect(
            SUPABASE_DATABASE_URL,
            connect_timeout=10,
            row_factory=dict_row
        )

        return conn

    except Exception:

        logger.exception(
            "Unable to connect to Supabase PostgreSQL."
        )

        raise


# ============================================================
# CONNECTION CONTEXT MANAGER
# ============================================================

@contextmanager
def get_cursor():
    """
    Provide a managed PostgreSQL connection and cursor.

    The connection is automatically closed after use.
    """

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        yield conn, cursor

    except Exception:

        if conn:

            try:
                conn.rollback()

            except Exception:
                pass

        raise

    finally:

        if cursor:

            try:
                cursor.close()

            except Exception:
                pass

        if conn:

            try:
                conn.close()

            except Exception:
                pass


# ============================================================
# SQL PLACEHOLDER CONVERSION
# ============================================================

def convert_query(query: str) -> str:
    """
    Convert SQLite-style ? placeholders to PostgreSQL %s.

    Example:

        SELECT *
        FROM users
        WHERE email = ?

    becomes:

        SELECT *
        FROM users
        WHERE email = %s
    """

    if not query:
        return query

    return query.replace("?", "%s")


# ============================================================
# EXECUTE INSERT / UPDATE / DELETE
# ============================================================

def execute_query(
    query: str,
    params: tuple = ()
) -> bool:
    """
    Execute INSERT, UPDATE or DELETE query.

    Returns:
        True  -> successful transaction
        False -> failed transaction
    """

    conn = None

    try:

        with get_cursor() as (conn, cursor):

            postgres_query = convert_query(query)

            cursor.execute(
                postgres_query,
                params
            )

            conn.commit()

            return True

    except Exception as e:

        if conn:

            try:
                conn.rollback()

            except Exception:
                pass

        logger.exception(
            "execute_query failed."
            f"\nSQL: {query}"
            f"\nError: {e}"
        )

        return False


# ============================================================
# EXECUTE QUERY AND RETURN INSERTED ROW
# ============================================================

def execute_returning(
    query: str,
    params: tuple = ()
) -> Optional[Dict[str, Any]]:
    """
    Execute an INSERT/UPDATE query containing
    RETURNING and return the resulting row.

    Example:

        INSERT INTO users (...)
        VALUES (...)
        RETURNING id
    """

    conn = None

    try:

        with get_cursor() as (conn, cursor):

            postgres_query = convert_query(query)

            cursor.execute(
                postgres_query,
                params
            )

            row = cursor.fetchone()

            conn.commit()

            if row:
                return dict(row)

            return None

    except Exception as e:

        if conn:

            try:
                conn.rollback()

            except Exception:
                pass

        logger.exception(
            "execute_returning failed."
            f"\nSQL: {query}"
            f"\nError: {e}"
        )

        return None


# ============================================================
# FETCH ONE
# ============================================================

def fetch_one(
    query: str,
    params: tuple = ()
) -> Optional[Dict[str, Any]]:
    """
    Execute SELECT query and return one row.

    Returns a normal Python dictionary.
    """

    try:

        with get_cursor() as (_, cursor):

            postgres_query = convert_query(query)

            cursor.execute(
                postgres_query,
                params
            )

            row = cursor.fetchone()

            if row:
                return dict(row)

            return None

    except Exception as e:

        logger.exception(
            "fetch_one failed."
            f"\nSQL: {query}"
            f"\nError: {e}"
        )

        return None


# ============================================================
# FETCH ALL
# ============================================================

def fetch_all(
    query: str,
    params: tuple = ()
) -> List[Dict[str, Any]]:
    """
    Execute SELECT query and return all rows.

    Returns a list of normal Python dictionaries.
    """

    try:

        with get_cursor() as (_, cursor):

            postgres_query = convert_query(query)

            cursor.execute(
                postgres_query,
                params
            )

            rows = cursor.fetchall()

            return [
                dict(row)
                for row in rows
            ]

    except Exception as e:

        logger.exception(
            "fetch_all failed."
            f"\nSQL: {query}"
            f"\nError: {e}"
        )

        return []


# ============================================================
# EXECUTE MANY
# ============================================================

def execute_many(
    query: str,
    params_list: list
) -> bool:
    """
    Execute the same INSERT/UPDATE/DELETE query
    for multiple parameter sets.
    """

    conn = None

    try:

        with get_cursor() as (conn, cursor):

            postgres_query = convert_query(query)

            cursor.executemany(
                postgres_query,
                params_list
            )

            conn.commit()

            return True

    except Exception as e:

        if conn:

            try:
                conn.rollback()

            except Exception:
                pass

        logger.exception(
            "execute_many failed."
            f"\nSQL: {query}"
            f"\nError: {e}"
        )

        return False

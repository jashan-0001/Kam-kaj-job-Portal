import os
import sys
import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, List, Optional

# =====================================================
# PROJECT ROOT
# =====================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config import DATABASE_PATH
from utils.logger import logger


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_connection() -> sqlite3.Connection:
    """
    Create and configure a production SQLite connection.
    """

    conn = sqlite3.connect(
        DATABASE_PATH,
        timeout=30,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    # -------------------------------------------------
    # SQLite Production Optimizations
    # -------------------------------------------------

    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.execute("PRAGMA temp_store=MEMORY;")
    conn.execute("PRAGMA cache_size=-64000;")      # ~64 MB cache
    conn.execute("PRAGMA busy_timeout=30000;")

    return conn


# =====================================================
# CONNECTION CONTEXT MANAGER
# =====================================================

@contextmanager
def get_cursor():
    """
    Provide a managed database cursor.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:

        yield conn, cursor

    finally:

        try:
            cursor.close()
        except Exception:
            pass

        conn.close()


# =====================================================
# EXECUTE INSERT / UPDATE / DELETE
# =====================================================

def execute_query(
    query: str,
    params: tuple = ()
) -> bool:

    conn = None

    try:

        with get_cursor() as (conn, cursor):

            cursor.execute(
                query,
                params
            )

            conn.commit()

            return True

    except Exception:

        if conn:
            conn.rollback()

        logger.exception(
            f"execute_query failed.\nSQL: {query}"
        )

        return False


# =====================================================
# FETCH ONE
# =====================================================

def fetch_one(
    query: str,
    params: tuple = ()
) -> Optional[Dict[str, Any]]:

    try:

        with get_cursor() as (_, cursor):

            cursor.execute(
                query,
                params
            )

            row = cursor.fetchone()

            if row:

                return dict(row)

            return None

    except Exception:

        logger.exception(
            f"fetch_one failed.\nSQL: {query}"
        )

        return None


# =====================================================
# FETCH ALL
# =====================================================

def fetch_all(
    query: str,
    params: tuple = ()
) -> List[Dict[str, Any]]:

    try:

        with get_cursor() as (_, cursor):

            cursor.execute(
                query,
                params
            )

            rows = cursor.fetchall()

            return [
                dict(row)
                for row in rows
            ]

    except Exception:

        logger.exception(
            f"fetch_all failed.\nSQL: {query}"
        )

        return []


# =====================================================
# EXECUTE MANY
# =====================================================

def execute_many(
    query: str,
    params_list: list
) -> bool:

    conn = None

    try:

        with get_cursor() as (conn, cursor):

            cursor.executemany(
                query,
                params_list
            )

            conn.commit()

            return True

    except Exception:

        if conn:
            conn.rollback()

        logger.exception(
            f"execute_many failed.\nSQL: {query}"
        )

        return False
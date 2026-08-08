import os
import sys

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

from database.database import get_connection
from utils.logger import logger


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

def create_tables():
    """
    Create all PostgreSQL/Supabase database tables and indexes.
    """

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        # ============================================================
        # USERS TABLE
        # ============================================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id SERIAL PRIMARY KEY,

            full_name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            role TEXT NOT NULL
                CHECK(role IN ('Admin', 'Employer', 'Candidate')),

            phone TEXT,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            is_active INTEGER DEFAULT 1
        )
        """)

        # ============================================================
        # JOBS TABLE
        # ============================================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (

            id SERIAL PRIMARY KEY,

            title TEXT NOT NULL,

            company TEXT NOT NULL,

            location TEXT NOT NULL,

            experience TEXT NOT NULL,

            salary TEXT NOT NULL,

            skills TEXT NOT NULL,

            description TEXT NOT NULL,

            posted_by INTEGER NOT NULL,

            status TEXT DEFAULT 'Open',

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(posted_by)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """)

        # ============================================================
        # APPLICATIONS TABLE
        # ============================================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (

            id SERIAL PRIMARY KEY,

            job_id INTEGER NOT NULL,

            user_id INTEGER NOT NULL,

            resume_path TEXT NOT NULL,

            ats_score DOUBLE PRECISION DEFAULT 0,

            match_percentage DOUBLE PRECISION DEFAULT 0,

            matched_skills TEXT,

            missing_skills TEXT,

            recommendation TEXT,

            status TEXT DEFAULT 'Pending',

            is_favorite INTEGER DEFAULT 0,

            applied_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(job_id, user_id),

            FOREIGN KEY(job_id)
                REFERENCES jobs(id)
                ON DELETE CASCADE,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """)

        # ============================================================
        # SAVED JOBS TABLE
        # ============================================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_jobs (

            id SERIAL PRIMARY KEY,

            candidate_id INTEGER NOT NULL,

            job_id INTEGER NOT NULL,

            saved_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(candidate_id, job_id),

            FOREIGN KEY(candidate_id)
                REFERENCES users(id)
                ON DELETE CASCADE,

            FOREIGN KEY(job_id)
                REFERENCES jobs(id)
                ON DELETE CASCADE
        )
        """)

        # ============================================================
        # NOTIFICATIONS TABLE
        # ============================================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (

            id SERIAL PRIMARY KEY,

            user_id INTEGER NOT NULL,

            title TEXT NOT NULL,

            message TEXT NOT NULL,

            type TEXT NOT NULL,

            is_read INTEGER DEFAULT 0,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """)

        # ============================================================
        # RECRUITER ACTIVITY TABLE
        # ============================================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recruiter_activity (

            id SERIAL PRIMARY KEY,

            employer_id INTEGER NOT NULL,

            activity TEXT NOT NULL,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(employer_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """)

        # ============================================================
        # AUDIT LOG TABLE
        # ============================================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (

            id SERIAL PRIMARY KEY,

            user_id INTEGER,

            user_role TEXT,

            action TEXT NOT NULL,

            details TEXT,

            description TEXT,

            ip_address TEXT,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE SET NULL
        )
        """)

        # ============================================================
        # INDEXES
        # ============================================================

        indexes = [

            """
            CREATE INDEX IF NOT EXISTS
            idx_users_email
            ON users(email)
            """,

            """
            CREATE INDEX IF NOT EXISTS
            idx_users_role
            ON users(role)
            """,

            """
            CREATE INDEX IF NOT EXISTS
            idx_jobs_posted_by
            ON jobs(posted_by)
            """,

            """
            CREATE INDEX IF NOT EXISTS
            idx_jobs_status
            ON jobs(status)
            """,

            """
            CREATE INDEX IF NOT EXISTS
            idx_jobs_created_at
            ON jobs(created_at)
            """,

            """
            CREATE INDEX IF NOT EXISTS
            idx_applications_job
            ON applications(job_id)
            """,

            """
            CREATE INDEX IF NOT EXISTS
            idx_applications_user
            ON applications(user_id)
            """,

            """
            CREATE INDEX IF NOT EXISTS
            idx_applications_status
            ON applications(status)
            """,

            """
            CREATE INDEX IF NOT EXISTS
            idx_notifications_user
            ON notifications(user_id)
            """,

            """
            CREATE INDEX IF NOT EXISTS
            idx_activity_employer
            ON recruiter_activity(employer_id)
            """,

            """
            CREATE INDEX IF NOT EXISTS
            idx_audit_logs_user
            ON audit_logs(user_id)
            """,

            """
            CREATE INDEX IF NOT EXISTS
            idx_audit_logs_action
            ON audit_logs(action)
            """,

            """
            CREATE INDEX IF NOT EXISTS
            idx_audit_logs_created_at
            ON audit_logs(created_at)
            """
        ]

        for query in indexes:

            cursor.execute(query)

        # ============================================================
        # COMMIT
        # ============================================================

        conn.commit()

        logger.info(
            "Supabase PostgreSQL database initialized successfully."
        )

        print("=" * 60)
        print("Supabase PostgreSQL Database Initialized Successfully")
        print("=" * 60)

    except Exception:

        if conn:

            try:
                conn.rollback()

            except Exception:
                pass

        logger.exception(
            "Supabase PostgreSQL database initialization failed."
        )

        raise

    finally:

        if conn:

            try:
                conn.close()

            except Exception:
                pass

            logger.info(
                "Database connection closed."
            )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    create_tables()
```

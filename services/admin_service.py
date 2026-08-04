from database.database import (
    fetch_all,
    fetch_one,
    execute_query
)

# =====================================================
# ADMIN DASHBOARD STATISTICS
# =====================================================

def get_admin_statistics():
    """
    Return platform statistics.
    """

    stats = {}

    row = fetch_one(
        "SELECT COUNT(*) AS total FROM users"
    )
    stats["users"] = row["total"] if row else 0

    row = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM users
        WHERE role='Candidate'
        """
    )
    stats["candidates"] = row["total"] if row else 0

    row = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM users
        WHERE role='Employer'
        """
    )
    stats["employers"] = row["total"] if row else 0

    row = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM jobs
        """
    )
    stats["jobs"] = row["total"] if row else 0

    row = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM applications
        """
    )
    stats["applications"] = row["total"] if row else 0

    return stats


# =====================================================
# GET ALL USERS
# =====================================================

def get_all_users():

    query = """
    SELECT
        id,
        full_name,
        email,
        role,
        is_active,
        created_at
    FROM users
    ORDER BY created_at DESC
    """

    return fetch_all(query)


# =====================================================
# DELETE USER
# =====================================================

def delete_user(user_id):

    query = """
    DELETE FROM users
    WHERE id = ?
    """

    return execute_query(
        query,
        (user_id,)
    )


# =====================================================
# TOGGLE USER STATUS
# =====================================================

def toggle_user_status(user_id):

    query = """
    UPDATE users
    SET is_active =
        CASE
            WHEN is_active = 1 THEN 0
            ELSE 1
        END
    WHERE id = ?
    """

    return execute_query(
        query,
        (user_id,)
    )


# =====================================================
# GET ALL JOBS
# =====================================================

def get_all_jobs():

    query = """
    SELECT

        jobs.id,
        jobs.title,
        jobs.company,
        jobs.location,
        jobs.status,
        jobs.created_at,

        users.full_name AS employer

    FROM jobs

    JOIN users
        ON jobs.posted_by = users.id

    ORDER BY jobs.created_at DESC
    """

    return fetch_all(query)


# =====================================================
# DELETE JOB
# =====================================================

def delete_job(job_id):

    query = """
    DELETE FROM jobs
    WHERE id = ?
    """

    return execute_query(
        query,
        (job_id,)
    )


# =====================================================
# GET ALL APPLICATIONS
# =====================================================

def get_all_applications():

    query = """
    SELECT

        applications.id,
        applications.ats_score,
        applications.match_percentage,
        applications.status,
        applications.applied_at,

        users.full_name,
        users.email,

        jobs.title

    FROM applications

    JOIN users
        ON applications.user_id = users.id

    JOIN jobs
        ON applications.job_id = jobs.id

    ORDER BY applications.applied_at DESC
    """

    return fetch_all(query)


# =====================================================
# DELETE APPLICATION
# =====================================================

def delete_application_admin(application_id):

    query = """
    DELETE FROM applications
    WHERE id = ?
    """

    return execute_query(
        query,
        (application_id,)
    )


# =====================================================
# USERS BY ROLE
# =====================================================

def get_role_statistics():

    query = """
    SELECT

        role,
        COUNT(*) AS total

    FROM users

    GROUP BY role

    ORDER BY total DESC
    """

    return fetch_all(query)


# =====================================================
# APPLICATION STATUS
# =====================================================

def get_application_statistics():

    query = """
    SELECT

        status,
        COUNT(*) AS total

    FROM applications

    GROUP BY status

    ORDER BY total DESC
    """

    return fetch_all(query)


# =====================================================
# JOBS BY COMPANY
# =====================================================

def get_company_job_statistics():

    query = """
    SELECT

        company,
        COUNT(*) AS total

    FROM jobs

    GROUP BY company

    ORDER BY total DESC
    """

    return fetch_all(query)
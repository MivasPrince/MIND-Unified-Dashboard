from core.db import run_query


# ----------------- BASIC LOADERS -----------------

def load_attempts(start_date=None, end_date=None):
    """Load attempts with optional date filtering."""
    sql = """
        SELECT *
        FROM attempts
        WHERE timestamp BETWEEN :start AND :end
        ORDER BY timestamp;
    """
    return run_query(sql, {
        "start": f"{start_date} 00:00:00",
        "end": f"{end_date} 23:59:59"
    })


def load_attempts_for_student(student_id, start_date=None, end_date=None):
    sql = """
        SELECT *
        FROM attempts
        WHERE student_id = :sid
        AND timestamp BETWEEN :start AND :end
        ORDER BY timestamp;
    """
    return run_query(sql, {
        "sid": student_id,
        "start": f"{start_date} 00:00:00",
        "end": f"{end_date} 23:59:59"
    })


def load_latest_attempts_per_case(student_id):
    """
    Latest attempt (highest attempt_number) per case for a given student.
    """
    sql = """
        SELECT DISTINCT ON (case_id)
            case_id, attempt_number, score, duration_seconds,
            ces_value, timestamp, state
        FROM attempts
        WHERE student_id = :sid
        ORDER BY case_id, attempt_number DESC;
    """
    return run_query(sql, {"sid": student_id})


# ----------------- AGGREGATIONS -----------------

def load_case_averages():
    """
    Average score & time per case across all students.
    """
    sql = """
        SELECT 
            case_id,
            AVG(score)::numeric(10,2) AS avg_score,
            AVG(duration_seconds)::numeric(10,2) AS avg_time,
            AVG(ces_value)::numeric(10,2) AS avg_ces
        FROM attempts
        GROUP BY case_id
        ORDER BY case_id;
    """
    return run_query(sql)


def load_first_vs_second_attempt_improvements():
    """
    Improvement from attempt 1 to attempt 2 across cases.
    """
    sql = """
        SELECT 
            case_id,
            AVG(CASE WHEN attempt_number = 1 THEN score END) AS avg_first,
            AVG(CASE WHEN attempt_number = 2 THEN score END) AS avg_second,
            AVG(
                CASE WHEN attempt_number = 2 THEN score END -
                (SELECT score FROM attempts a2 
                 WHERE a2.case_id = attempts.case_id
                 AND a2.attempt_number = 1
                 LIMIT 1)
            ) AS avg_improvement
        FROM attempts
        GROUP BY case_id;
    """
    return run_query(sql)


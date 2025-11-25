from core.db import run_query


# ----------------- BASIC ENGAGEMENT LOADERS -----------------

def load_engagement_logs(start_date=None, end_date=None):
    sql = """
        SELECT *
        FROM engagement_logs
        WHERE timestamp BETWEEN :start AND :end
        ORDER BY timestamp;
    """
    return run_query(sql, {
        "start": f"{start_date} 00:00:00",
        "end": f"{end_date} 23:59:59"
    })


def load_engagement_for_student(student_id, start_date=None, end_date=None):
    sql = """
        SELECT *
        FROM engagement_logs
        WHERE student_id = :sid
        AND timestamp BETWEEN :start AND :end
        ORDER BY timestamp;
    """
    return run_query(sql, {
        "sid": student_id,
        "start": f"{start_date} 00:00:00",
        "end": f"{end_date} 23:59:59"
    })


# ----------------- AGGREGATES -----------------

def load_daily_engagement():
    """
    For area/line chart: number of engagement logs per day.
    """
    sql = """
        SELECT 
            DATE(timestamp) AS day,
            COUNT(*) AS events
        FROM engagement_logs
        GROUP BY DATE(timestamp)
        ORDER BY day;
    """
    return run_query(sql)


def load_total_engagement_per_student():
    """
    Sum duration_seconds for each student.
    """
    sql = """
        SELECT 
            student_id,
            SUM(duration_seconds) AS total_duration
        FROM engagement_logs
        GROUP BY student_id
        ORDER BY total_duration DESC;
    """
    return run_query(sql)


def load_engagement_per_case():
    """
    Engagement time grouped by case study.
    """
    sql = """
        SELECT 
            case_id,
            SUM(duration_seconds) AS total_time
        FROM engagement_logs
        GROUP BY case_id
        ORDER BY case_id;
    """
    return run_query(sql)


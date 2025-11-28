import pandas as pd
from typing import Optional
# Assuming db.py is one level up (in core/)
from db import run_query 


# ----------------- BASIC LOADERS -----------------

def load_environment_metrics(start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
    """
    Load environment metrics by joining with the attempts table to filter by timestamp.
    (More efficient than using a subquery with IN).
    """
    sql = """
        SELECT e.*
        FROM environment_metrics e
        JOIN attempts a 
            ON e.attempt_id = a.attempt_id
        WHERE a.timestamp >= :start AND a.timestamp <= :end
        ORDER BY e.attempt_id;
    """
    
    # Prepare parameters with safe default date range
    params = {
        "start": f"{start_date} 00:00:00" if start_date else "1900-01-01 00:00:00",
        "end": f"{end_date} 23:59:59" if end_date else "2999-12-31 23:59:59"
    }
    
    return run_query(sql, params)


def load_environment_for_student(student_id: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
    """
    Load environment metrics for a specific student, filtering by student_id 
    and optional date range using the attempts table.
    """
    sql = """
        SELECT e.*
        FROM environment_metrics e
        JOIN attempts a 
            ON e.attempt_id = a.attempt_id
        WHERE a.student_id = :sid
          AND a.timestamp >= :start AND a.timestamp <= :end
        ORDER BY a.timestamp DESC;
    """
    
    # Prepare parameters with safe default date range
    params = {
        "sid": student_id,
        "start": f"{start_date} 00:00:00" if start_date else "1900-01-01 00:00:00",
        "end": f"{end_date} 23:59:59" if end_date else "2999-12-31 23:59:59"
    }
    
    return run_query(sql, params)


def load_environment_with_attempts(start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
    """
    Join environment metrics with attempts table for correlation plots (e.g., latency vs score).
    """
    sql = """
        SELECT 
            e.*,
            a.score,
            a.duration_seconds, -- Added duration for better analysis
            a.timestamp AS attempt_time
        FROM environment_metrics e
        JOIN attempts a
            ON e.attempt_id = a.attempt_id
        WHERE a.timestamp >= :start AND a.timestamp <= :end
        ORDER BY a.timestamp;
    """
    
    # Prepare parameters with safe default date range
    params = {
        "start": f"{start_date} 00:00:00" if start_date else "1900-01-01 00:00:00",
        "end": f"{end_date} 23:59:59" if end_date else "2999-12-31 23:59:59"
    }
    
    return run_query(sql, params)


# ----------------- AGGREGATES -----------------

def load_environment_summary() -> pd.DataFrame:
    """
    Basic averages for environment conditions across the platform.
    """
    sql = """
        SELECT 
            COUNT(e.attempt_id) AS total_records,
            AVG(noise_level)::numeric(10,2) AS avg_noise,
            AVG(noise_quality_index)::numeric(10,2) AS avg_noise_quality,
            AVG(internet_latency_ms)::numeric(10,2) AS avg_latency,
            AVG(internet_stability_score)::numeric(10,2) AS avg_stability,
            AVG(connection_drops)::numeric(10,2) AS avg_drops
        FROM environment_metrics e;
    """
    # Renamed avg(noise_quality_index) for clarity and added total_records
    return run_query(sql)


def load_device_type_distribution() -> pd.DataFrame:
    """
    Count of attempts by device type.
    """
    sql = """
        SELECT 
            device_type,
            COUNT(attempt_id) AS count
        FROM environment_metrics
        GROUP BY device_type
        ORDER BY count DESC;
    """
    return run_query(sql)

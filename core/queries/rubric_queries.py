import pandas as pd
from typing import Optional
# Assuming db.py is one level up (in core/)
from db import run_query 


# ----------------- BASIC LOADERS -----------------

def load_rubric_scores_for_attempt(attempt_id: str) -> pd.DataFrame:
    """Load all individual rubric scores for a single attempt."""
    sql = """
        SELECT *
        FROM rubric_scores
        WHERE attempt_id = :aid
        ORDER BY rubric_dimension;
    """
    return run_query(sql, {"aid": attempt_id})


def load_rubric_scores_for_student(student_id: str, 
                                   start_date: Optional[str] = None, 
                                   end_date: Optional[str] = None) -> pd.DataFrame:
    """
    Load all detailed rubric scores for a student, filtered by optional date range.
    """
    sql = """
        SELECT 
            r.*,
            a.case_id,
            a.attempt_number,
            a.timestamp
        FROM rubric_scores r
        JOIN attempts a
            ON r.attempt_id = a.attempt_id
        WHERE a.student_id = :sid
          AND a.timestamp >= :start AND a.timestamp <= :end
        ORDER BY a.timestamp DESC, r.rubric_dimension;
    """
    
    # Prepare parameters with safe default date range
    params = {
        "sid": student_id,
        "start": f"{start_date} 00:00:00" if start_date else "1900-01-01 00:00:00",
        "end": f"{end_date} 23:59:59" if end_date else "2999-12-31 23:59:59"
    }

    return run_query(sql, params)


# ----------------- AGGREGATES -----------------

def load_rubric_dimension_averages(start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
    """
    Average mastery level per rubric dimension across the platform, filtered by date.
    """
    sql = """
        SELECT 
            r.rubric_dimension,
            AVG(r.score)::numeric(10,2) AS avg_score,
            AVG(r.max_score)::numeric(10,2) AS avg_max,
            AVG(r.score * 1.0 / r.max_score)::numeric(10,4) AS mastery_rate,
            COUNT(r.id) AS total_scores
        FROM rubric_scores r
        JOIN attempts a
            ON r.attempt_id = a.attempt_id
        WHERE a.timestamp >= :start AND a.timestamp <= :end
        GROUP BY r.rubric_dimension
        ORDER BY mastery_rate DESC;
    """
    
    # Prepare parameters with safe default date range
    params = {
        "start": f"{start_date} 00:00:00" if start_date else "1900-01-01 00:00:00",
        "end": f"{end_date} 23:59:59" if end_date else "2999-12-31 23:59:59"
    }

    # Added date filtering and total_scores count
    return run_query(sql, params)


def load_rubric_case_dimension_matrix(start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
    """
    Calculates the average mastery rate for each dimension across each case (Heatmap data).
    """
    sql = """
        SELECT 
            a.case_id,
            r.rubric_dimension,
            AVG(r.score * 1.0 / r.max_score)::numeric(10,4) AS mastery
        FROM rubric_scores r
        JOIN attempts a
            ON r.attempt_id = a.attempt_id
        WHERE a.timestamp >= :start AND a.timestamp <= :end
        GROUP BY a.case_id, r.rubric_dimension
        ORDER BY a.case_id, r.rubric_dimension;
    """
    
    # Prepare parameters with safe default date range
    params = {
        "start": f"{start_date} 00:00:00" if start_date else "1900-01-01 00:00:00",
        "end": f"{end_date} 23:59:59" if end_date else "2999-12-31 23:59:59"
    }

    # Added date filtering to ensure the matrix reflects a relevant period
    return run_query(sql, params)

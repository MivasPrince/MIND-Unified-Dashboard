from core.db import run_query


# ----------------- BASIC LOADERS -----------------

def load_rubric_scores_for_attempt(attempt_id):
    sql = """
        SELECT *
        FROM rubric_scores
        WHERE attempt_id = :aid
        ORDER BY rubric_dimension;
    """
    return run_query(sql, {"aid": attempt_id})


def load_rubric_scores_for_student(student_id):
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
        ORDER BY a.timestamp, r.rubric_dimension;
    """
    return run_query(sql, {"sid": student_id})


# ----------------- AGGREGATES -----------------

def load_rubric_dimension_averages():
    """
    Average mastery level per rubric dimension (across platform)
    """
    sql = """
        SELECT 
            rubric_dimension,
            AVG(score)::numeric(10,2) AS avg_score,
            AVG(max_score)::numeric(10,2) AS avg_max,
            AVG(score * 1.0 / max_score)::numeric(10,4) AS mastery_rate
        FROM rubric_scores
        GROUP BY rubric_dimension
        ORDER BY rubric_dimension;
    """
    return run_query(sql)


def load_rubric_case_dimension_matrix():
    """
    Heatmap: dimension vs case_id
    """
    sql = """
        SELECT 
            a.case_id,
            r.rubric_dimension,
            AVG(r.score * 1.0 / r.max_score)::numeric(10,4) AS mastery
        FROM rubric_scores r
        JOIN attempts a
            ON r.attempt_id = a.attempt_id
        GROUP BY a.case_id, r.rubric_dimension
        ORDER BY a.case_id, r.rubric_dimension;
    """
    return run_query(sql)


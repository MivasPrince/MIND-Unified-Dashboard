import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from functools import lru_cache


@lru_cache(maxsize=1)
def get_engine():
    """
    Create and cache a single SQLAlchemy engine for the entire app.
    
    Reads:
    st.secrets["DB_URL"]
    """
    try:
        db_url = st.secrets["DB_URL"]
        engine = create_engine(db_url, pool_pre_ping=True)
        return engine
    except Exception as e:
        st.error(f"❌ Error loading DB engine: {e}")
        return None


def run_query(sql: str, params: dict = None) -> pd.DataFrame:
    """
    Executes a SQL query using the shared engine.
    Returns the result as a DataFrame.
    """
    engine = get_engine()
    if engine is None:
        return pd.DataFrame()

    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql), params or {})
            df = pd.DataFrame(result.mappings().all())
            return df
    except Exception as e:
        st.error(f"❌ Database query failed: {e}")
        return pd.DataFrame()


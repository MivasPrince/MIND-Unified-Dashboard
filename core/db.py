import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import pandas as pd
from typing import Optional, Dict

# Define required secret keys for the database connection
DB_SECRET_KEYS = [
    "DB_USER",
    "DB_PASSWORD",
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "DB_SSLMODE",
]


@st.cache_resource(show_spinner="Connecting to database...")
def get_engine() -> Optional[Engine]:
    """
    Create and cache a single SQLAlchemy engine for the entire app.
    
    Constructs the database URL from individual secrets.
    """
    
    # 1. Check for missing secrets
    missing_keys = [key for key in DB_SECRET_KEYS if key not in st.secrets]
    if missing_keys:
        st.error(f"❌ Database setup error: Missing required keys in Streamlit Secrets: {', '.join(missing_keys)}")
        # Use st.stop() to prevent subsequent query attempts
        st.stop()
        return None

    try:
        # 2. Construct the PostgreSQL connection URL
        # Format: postgresql://user:password@host:port/dbname
        db_url = (
            f"postgresql://{st.secrets['DB_USER']}:{st.secrets['DB_PASSWORD']}@"
            f"{st.secrets['DB_HOST']}:{st.secrets['DB_PORT']}/{st.secrets['DB_NAME']}"
        )

        # 3. Handle SSL mode for NeonDB (required)
        # SQLAlchemy requires connection arguments for SSL
        connect_args = {}
        if st.secrets["DB_SSLMODE"].lower() == "require":
            # For NeonDB, setting sslmode=require is often done via connect_args
            # which depends on the underlying driver (psycopg2)
            connect_args = {"sslmode": "require"}
        
        # 4. Create the engine
        engine = create_engine(
            db_url,
            pool_pre_ping=True,  # Recommended for managed services like Neon
            connect_args=connect_args,
            # Set pool size for better performance under load
            pool_size=5, 
            max_overflow=10
        )
        st.success("Database connection engine ready.")
        return engine
    except Exception as e:
        st.error(f"❌ Error initializing DB engine. Check URL components and connection: {e}")
        return None


# We often cache query results too, but since 'run_query' will be used 
# with different SQL/params, caching is better placed around the calls to this function.
def run_query(sql: str, params: Optional[Dict] = None) -> pd.DataFrame:
    """
    Executes a SQL query using the shared engine.
    
    Args:
        sql (str): The SQL query string.
        params (Dict, optional): Dictionary of parameters to safely bind to the query.

    Returns:
        pd.DataFrame: The result of the query.
    """
    engine = get_engine()
    if engine is None:
        # Engine failed to load, return empty DataFrame
        return pd.DataFrame() 

    try:
        with engine.connect() as conn:
            # Using text() and parameter binding for secure queries (prevents SQL injection)
            result = conn.execute(text(sql), params or {})
            
            # Use result.fetchall() and a list comprehension if .mappings() is slow 
            # or not needed, but .mappings() is generally clean.
            df = pd.DataFrame(result.mappings().all())
            return df
    except Exception as e:
        # Log the specific query failure for debugging
        error_message = f"❌ Database query failed:\nSQL: {sql[:100]}...\nError: {e}"
        st.error(error_message)
        return pd.DataFrame()

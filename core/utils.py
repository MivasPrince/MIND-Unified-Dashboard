import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
from typing import Tuple, Optional


# ------------- DATE RANGE PICKER -------------
def date_range_picker() -> Tuple[Optional[str], Optional[str]]:
    """
    Provides a standardized date range selector.
    
    Returns: (start_date_str, end_date_str) in 'YYYY-MM-DD' format, 
             or (None, None) if the selection is invalid.
    """

    today = datetime.now().date()
    # Default to the last 90 days for richer data context
    default_start = today - timedelta(days=90) 

    col1, col2 = st.columns(2)
    with col1:
        # Use datetime.date for the picker input
        start_date: date = st.date_input("Start Date", default_start)
    with col2:
        end_date: date = st.date_input("End Date", today)

    if start_date > end_date:
        st.error("Start date cannot be after end date.")
        return None, None

    # Convert date objects to the string format required by the query functions
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    return start_date_str, end_date_str


# ------------- SAFE DF CASTING -------------
def safe_cast_df(df: pd.DataFrame, column: str, dtype: str) -> pd.DataFrame:
    """
    Safely casts a DataFrame column to a specified type, coercing errors 
    and handling missing values.
    """
    if column not in df.columns:
        return df

    if dtype in ['int', 'float']:
        # Use pandas' dedicated numeric conversion
        df[column] = pd.to_numeric(df[column], errors='coerce').astype(dtype, errors='ignore')
    elif dtype == 'datetime':
        # Use pandas' dedicated datetime conversion
        df[column] = pd.to_datetime(df[column], errors='coerce')
    else:
        # Generic cast
        try:
            df[column] = df[column].astype(dtype, errors='ignore')
        except:
            pass # Failsafe, though errors='ignore' should cover most cases
            
    return df


def to_int(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Safely converts a column to integer type."""
    return safe_cast_df(df, column, 'Int64') # Using nullable integer type


def to_float(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Safely converts a column to float type."""
    return safe_cast_df(df, column, 'float')


# ------------- JOIN HELPERS -------------
def join_case_titles(df: pd.DataFrame, case_df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds 'title' column from a separate DataFrame (e.g., case metadata) 
    to any DataFrame containing 'case_id'.
    """
    # Check for required columns before merging
    if "case_id" in df.columns and "case_id" in case_df.columns and "title" in case_df.columns:
        return df.merge(case_df[["case_id", "title"]], on="case_id", how="left")
    
    # If columns are missing, return the original DataFrame with a warning
    st.warning("⚠️ Cannot join case titles: Missing 'case_id' or 'title' in one of the DataFrames.")
    return df


# ------------- SORTING HELPERS -------------
def sort_by_timestamp(df: pd.DataFrame, column: str = "timestamp") -> pd.DataFrame:
    """
    Converts the specified column to datetime (if necessary) and sorts the DataFrame.
    """
    if column in df.columns:
        # Safely convert to datetime
        df = safe_cast_df(df, column, 'datetime')
        
        # Sort values, dropping NaT if they resulted from coercion
        df = df.sort_values(by=column, na_position='last')
        
    return df


# ------------- EMPTY CHECK -------------
def is_empty(df: Optional[pd.DataFrame]) -> bool:
    """
    Standard empty check for all dashboards.
    """
    return df is None or df.empty

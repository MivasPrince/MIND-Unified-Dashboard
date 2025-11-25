import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


# ------------- DATE RANGE PICKER -------------
def date_range_picker():
    """
    Provides a standardized date range selector.
    Returns (start_date, end_date) as datetime objects.
    """

    today = datetime.now().date()
    default_start = today - timedelta(days=30)

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", default_start)
    with col2:
        end_date = st.date_input("End Date", today)

    if start_date > end_date:
        st.error("Start date cannot be after end date.")
        return None, None

    return start_date, end_date


# ------------- SAFE DF CASTING -------------
def to_int(df, column):
    try:
        df[column] = df[column].astype(int)
    except:
        pass
    return df


def to_float(df, column):
    try:
        df[column] = df[column].astype(float)
    except:
        pass
    return df


# ------------- JOIN HELPERS -------------
def join_case_titles(df, case_df):
    """
    Adds case title to any dataframe containing case_id.
    """
    if "case_id" in df and "case_id" in case_df:
        return df.merge(case_df[["case_id", "title"]], on="case_id", how="left")
    return df


# ------------- SORTING HELPERS -------------
def sort_by_timestamp(df, column="timestamp"):
    if column in df:
        try:
            df[column] = pd.to_datetime(df[column])
            df = df.sort_values(by=column)
        except:
            pass
    return df


# ------------- EMPTY CHECK -------------
def is_empty(df):
    """
    Standard empty check for all dashboards.
    """
    return df is None or df.empty


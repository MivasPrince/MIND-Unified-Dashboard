import streamlit as st
import pandas as pd
from core.auth import role_guard, logout_button
from core.theme import apply_theme
from core.utils import date_range_picker, is_empty, to_float
from core.components import (
    section_header, kpi_card, kpi_row,
    plot_line, plot_bar, plot_hist, plot_scatter, show_empty
)

from core.queries.admin_queries import (
    load_admin_aggregates,
    total_active_students,
    total_attempts,
    average_score,
    average_ces, # Now defined
    average_time_on_task, # Now defined
    case_study_summary, # Filtered in Load
    campus_summary, # Global, not filtered
    department_summary # Global, not filtered
)

from core.queries.reliability_queries import (
    load_system_reliability,
    load_api_latency_summary, # Filtered in Load
)

from core.queries.environment_queries import (
    load_environment_summary, # Filtered in Load
    load_device_type_distribution # Filtered in Load
)

# --------------------------- PAGE SETUP ---------------------------

apply_theme()
user_role, username = role_guard("Admin")

st.title("🧭 Admin Dashboard — MIND Unified Platform Overview")
st.caption(f"Welcome, **{username}** — You have full administrative visibility.")
logout_button()

st.markdown("---")


# --------------------------- DATE FILTER ---------------------------

start_date, end_date = date_range_picker()
if not start_date or not end_date:
    st.stop()


# --------------------------- LOAD METRICS ---------------------------

# GLOBAL KPI DATA (Filtered by date)
# DataFrames are returned, we need to extract the single value later.
active_students_df = total_active_students(start_date, end_date)
attempts_count_df = total_attempts(start_date, end_date)
avg_score_df = average_score(start_date, end_date)
avg_ces_df = average_ces(start_date, end_date)
avg_time_df = average_time_on_task(start_date, end_date)


# AGGREGATES & SUMMARIES (Filtered by date where applicable)
admin_metrics = load_admin_aggregates(start_date, end_date)
case_df = case_study_summary(start_date, end_date) # ADDED DATE FILTER
rel_df = load_system_reliability(start_date, end_date)
api_latency = load_api_latency_summary(start_date, end_date) # ADDED DATE FILTER
env_summary = load_environment_summary(start_date, end_date) # ADDED DATE FILTER
device_mix = load_device_type_distribution(start_date, end_date) # ADDED DATE FILTER


# GLOBAL STATIC SUMMARIES (No date filter)
campus_df = campus_summary()
dept_df = department_summary()


# --------------------------- KPI SECTION ---------------------------

section_header("Platform-Wide KPIs")

# Helper function to safely extract the value from the single-row, single-column DataFrame
def extract_kpi_value(df, col_name, default=0):
    if not is_empty(df) and col_name in df.columns:
        # Use .iloc[0] to get the value from the first row
        return df[col_name].iloc[0]
    return default

kpi_row([
    ("Active Students", extract_kpi_value(active_students_df, "active_students")),
    ("Total Attempts", extract_kpi_value(attempts_count_df, "attempts_count")),
    ("Average Score", extract_kpi_value(avg_score_df, "avg_score")),
    ("Average CES", extract_kpi_value(avg_ces_df, "avg_ces")),
    ("Avg Time on Task (secs)", extract_kpi_value(avg_time_df, "avg_time")),
])


# --------------------------- ADMIN AGGREGATES TIMELINE ---------------------------

section_header("📈 Key Metrics Over Time (Admin Aggregates)")

if not is_empty(admin_metrics):
    # Iterate through unique metric names and plot their trends
    # Ensure 'metric_value' is float for plotting
    admin_metrics = to_float(admin_metrics, "metric_value")
    
    # Use st.expander to keep the dashboard tidy since this section can have many plots
    with st.expander("View Detailed Metric Trends"):
        for metric_name in admin_metrics["metric_name"].unique():
            df_metric = admin_metrics[admin_metrics["metric_name"] == metric_name]
            plot_line(df_metric, x="timestamp", y="metric_value", title=f"{metric_name} Over Time")
else:
    show_empty("No admin aggregate metrics available for the selected period.")


# --------------------------- CASE STUDY SUMMARY ---------------------------

section_header("📚 Case Study Summary (Filtered)")

if not is_empty(case_df):
    st.dataframe(case_df, use_container_width=True)
else:
    show_empty("No case study summary data available for the selected period.")


# --------------------------- CAMPUS & DEPARTMENT SUMMARY ---------------------------

cols = st.columns(2)

with cols[0]:
    section_header("Global Campus Summary")
    if not is_empty(campus_df):
        st.dataframe(campus_df, use_container_width=True)
    else:
        show_empty("Global campus data is not available.")

with cols[1]:
    section_header("Global Department Summary")
    if not is_empty(dept_df):
        st.dataframe(dept_df, use_container_width=True)
    else:
        show_empty("Global department data is not available.")


# --------------------------- SYSTEM HEALTH ---------------------------

section_header("🛠️ System Health — Reliability Index & API Latency")

if not is_empty(rel_df):
    rel_df = to_float(rel_df, "reliability_index")
    plot_line(rel_df, x="timestamp", y="reliability_index", title="Reliability Index Over Time")
else:
    show_empty("No system reliability data available.")

if not is_empty(api_latency):
    api_latency = to_float(api_latency, "p95_latency")
    plot_bar(api_latency, x="api_name", y="p95_latency", title="P95 Latency (ms) per API")
else:
    show_empty("No API latency summary data available.")


# --------------------------- ENVIRONMENT HEALTH ---------------------------

section_header("🌐 Environment Health Summary")

if not is_empty(env_summary):
    st.dataframe(env_summary, use_container_width=True)
else:
    show_empty("No environment summary data available for the selected period.")

section_header("📱 Device Type Distribution")

if not is_empty(device_mix):
    device_mix = to_float(device_mix, "count")
    plot_bar(device_mix, x="device_type", y="count", title="Devices Used Across Platform")
else:
    show_empty("No device distribution data available.")

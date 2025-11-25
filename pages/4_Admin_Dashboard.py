import streamlit as st

from core.auth import role_guard, logout_button
from core.theme import apply_theme
from core.utils import date_range_picker, is_empty
from core.components import (
    section_header, kpi_card, kpi_row,
    plot_line, plot_bar, plot_hist, plot_scatter, show_empty
)

from core.queries.admin_queries import (
    load_admin_aggregates,
    total_active_students,
    total_attempts,
    average_score,
    average_ces,
    average_time_on_task,
    case_study_summary,
    campus_summary,
    department_summary
)

from core.queries.reliability_queries import (
    load_system_reliability,
    load_api_latency_summary,
)

from core.queries.environment_queries import (
    load_environment_summary,
    load_device_type_distribution
)

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

admin_metrics = load_admin_aggregates(start_date, end_date)
active_students = total_active_students(start_date, end_date)
attempts_count = total_attempts(start_date, end_date)
avg_score_df = average_score(start_date, end_date)
avg_ces_df = average_ces(start_date, end_date)
avg_time_df = average_time_on_task(start_date, end_date)

case_df = case_study_summary()
campus_df = campus_summary()
dept_df = department_summary()

rel_df = load_system_reliability(start_date, end_date)
api_latency = load_api_latency_summary()

env_summary = load_environment_summary()
device_mix = load_device_type_distribution()


# --------------------------- KPI SECTION ---------------------------

section_header("Platform-Wide KPIs")

kpi_row([
    ("Active Students", active_students.get("active_students", 0)),
    ("Total Attempts", attempts_count.get("attempts_count", 0)),
    ("Average Score", avg_score_df.get("avg_score", 0)),
    ("Average CES", avg_ces_df.get("avg_ces", 0)),
    ("Avg Time on Task (secs)", avg_time_df.get("avg_time", 0)),
])


# --------------------------- ADMIN AGGREGATES TIMELINE ---------------------------

section_header("📈 Key Metrics Over Time (Admin Aggregates)")

if not is_empty(admin_metrics):
    for metric_name in admin_metrics["metric_name"].unique():
        df_metric = admin_metrics[admin_metrics["metric_name"] == metric_name]
        plot_line(df_metric, x="timestamp", y="metric_value", title=f"{metric_name} Over Time")
else:
    show_empty("No admin aggregate metrics available.")


# --------------------------- CASE STUDY SUMMARY ---------------------------

section_header("📚 Case Study Summary")

if not is_empty(case_df):
    st.dataframe(case_df)
else:
    show_empty()


# --------------------------- CAMPUS & DEPARTMENT SUMMARY ---------------------------

cols = st.columns(2)

with cols[0]:
    section_header("Campus Summary")
    if not is_empty(campus_df):
        st.dataframe(campus_df)
    else:
        show_empty()

with cols[1]:
    section_header("Department Summary")
    if not is_empty(dept_df):
        st.dataframe(dept_df)
    else:
        show_empty()


# --------------------------- SYSTEM HEALTH ---------------------------

section_header("🛠️ System Health — Reliability Index & API Latency")

if not is_empty(rel_df):
    plot_line(rel_df, x="timestamp", y="reliability_index", title="Reliability Index Over Time")
else:
    show_empty()

if not is_empty(api_latency):
    plot_bar(api_latency, x="api_name", y="avg_latency", title="Avg Latency (ms) per API")
else:
    show_empty()


# --------------------------- ENVIRONMENT HEALTH ---------------------------

section_header("🌐 Environment Health Summary")

if not is_empty(env_summary):
    st.dataframe(env_summary)
else:
    show_empty()

section_header("📱 Device Type Distribution")

if not is_empty(device_mix):
    plot_bar(device_mix, x="device_type", y="count", title="Devices Used Across Platform")
else:
    show_empty()


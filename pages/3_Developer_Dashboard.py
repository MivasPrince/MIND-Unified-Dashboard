import streamlit as st

from core.auth import role_guard, logout_button
from core.theme import apply_theme
from core.utils import date_range_picker, is_empty
from core.components import (
    section_header, kpi_card, kpi_row,
    plot_line, plot_bar, plot_hist, plot_scatter, show_empty
)

from core.queries.reliability_queries import (
    load_system_reliability,
    load_api_latency_summary,
    load_error_rate_by_api,
    load_critical_incidents,
    load_incidents_by_location,
    load_latest_reliability
)

from core.queries.environment_queries import (
    load_environment_with_attempts,
    load_device_type_distribution
)

apply_theme()
user_role, username = role_guard("Developer")

st.title("🛠️ Developer Dashboard")
st.caption(f"Welcome, **{username}** — System Reliability & Environment Insights")
logout_button()

st.markdown("---")


# --------------------------- DATE FILTER ---------------------------

start_date, end_date = date_range_picker()
if not start_date or not end_date:
    st.stop()


# --------------------------- LOAD SYSTEM RELIABILITY ---------------------------

rel_df = load_system_reliability(start_date, end_date)
latest_rel = load_latest_reliability()
api_latency = load_api_latency_summary()
error_rates = load_error_rate_by_api()
critical_inc = load_critical_incidents()
incidents_by_loc = load_incidents_by_location()

# Environment + attempts
env_attempts = load_environment_with_attempts(start_date, end_date)
device_mix = load_device_type_distribution()


# --------------------------- KPI SECTION ---------------------------

section_header("System Reliability KPIs")

if not is_empty(latest_rel):
    avg_rel = latest_rel["reliability_index"].mean().round(2)
    avg_latency = latest_rel["latency_ms"].mean().round(2)
    avg_error = latest_rel["error_rate"].mean().round(4)

    kpi_row([
        ("Reliability Index (recent)", avg_rel),
        ("Avg API Latency (ms)", avg_latency),
        ("Avg Error Rate", avg_error),
    ])
else:
    show_empty()


# --------------------------- API LATENCY ---------------------------

section_header("⏱️ API Latency Overview")

if not is_empty(api_latency):
    plot_bar(api_latency, x="api_name", y="avg_latency", title="Avg Latency (ms) per API")
else:
    show_empty()


# --------------------------- ERROR RATES ---------------------------

section_header("🚨 Error Rate by API")

if not is_empty(error_rates):
    plot_bar(error_rates, x="api_name", y="avg_error", title="Average Error Rate per API")
else:
    show_empty()


# --------------------------- RELIABILITY TREND ---------------------------

section_header("📉 Reliability Index Trend")

if not is_empty(rel_df):
    plot_line(rel_df, x="timestamp", y="reliability_index", title="Reliability Over Time")
else:
    show_empty()


# --------------------------- CRITICAL INCIDENTS ---------------------------

section_header("⚠️ Critical Incidents")

if not is_empty(critical_inc):
    st.dataframe(critical_inc)
else:
    show_empty()


# --------------------------- INCIDENTS BY LOCATION ---------------------------

section_header("📍 Incidents by Location")

if not is_empty(incidents_by_loc):
    plot_bar(incidents_by_loc, x="location", y="incidents", title="Critical Incidents by Location")
else:
    show_empty()


# --------------------------- ENVIRONMENT QUALITY ---------------------------

section_header("🌐 Environment Quality Correlations")

if not is_empty(env_attempts):
    plot_scatter(env_attempts, x="internet_latency_ms", y="score", title="Latency vs Score")
    plot_scatter(env_attempts, x="internet_stability_score", y="score", title="Stability vs Score")
    plot_scatter(env_attempts, x="noise_level", y="score", title="Noise Level vs Score")
else:
    show_empty()


# --------------------------- DEVICE TYPE DISTRIBUTION ---------------------------

section_header("📱 Device Type Distribution")

if not is_empty(device_mix):
    plot_bar(device_mix, x="device_type", y="count", title="Device Type Breakdown")
else:
    show_empty()


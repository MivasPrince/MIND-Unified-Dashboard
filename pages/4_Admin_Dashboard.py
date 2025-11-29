"""
Admin Dashboard - Platform-Wide Analytics
Executive view of institutional KPIs and system health
"""

import streamlit as st
from auth import require_auth, get_current_user
from theme import apply_streamlit_theme
from db import init_database

# Page config
st.set_page_config(
    page_title="Admin Dashboard - MIND",
    page_icon="🔧",
    layout="wide"
)

# Apply theme
st.markdown(apply_streamlit_theme(), unsafe_allow_html=True)

# Require authentication
require_auth(allowed_roles=["Admin"])

# Get user info
user = get_current_user()

# Initialize database
db = init_database()

# Header
st.markdown("# 🔧 Admin Dashboard")
st.markdown(f"### Welcome, {user['name']}!")
st.markdown("---")

# Placeholder content
st.info("🚧 Admin Dashboard is under construction")

st.markdown("""
### Planned Features:

#### Key Performance Indicators
- Total active students
- Total attempts completed
- Platform-wide average score
- Platform-wide average CES
- Active cohorts / campuses / departments
- Platform reliability index
- Overall environment quality index

#### Charts
- Executive KPI tiles
- Daily active users trend
- Weekly metrics trend
- Usage by campus/department
- System health overview
- Environment health overview
- Case study engagement

#### Tables
- Admin metrics (from admin_aggregates)
- Top/bottom case studies
- Campus/department summary
- Key incidents summary

#### Filters
- Time range
- Campus
- Department
- Cohort
- Metric name
- Severity level
""")

st.markdown("---")
st.caption("💡 MIND Unified Dashboard | Miva Open University")

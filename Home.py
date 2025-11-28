import streamlit as st
from pathlib import Path
# Assuming auth.py, theme.py are in the project root
from auth import check_authentication, login_widget, logout_button 
from theme import apply_theme 

# =================================================================
# 1. INITIAL SETUP & THEME APPLICATION
# =================================================================

# Apply consistent branding/theme, including st.set_page_config()
apply_theme()

# Load logo path relative to the script location
logo_path = Path(__file__).parent / "assets" / "mind_logo.png"

# Sidebar Branding and Logout
with st.sidebar:
    st.image(str(logo_path), use_column_width=True) # Convert Path object to string for st.image
    st.markdown("### **MIND Unified Dashboard**")
    st.markdown("---")

    # The authentication check happens below, but the logout button 
    # must be defined here for placement. It will only show if auth_status is True.
    # The logout_button function should handle its own conditional rendering.

# =================================================================
# 2. AUTHENTICATION GATE
# =================================================================

auth_status, user_role, username = check_authentication()

if not auth_status:
    # If not logged in, display the login form and stop execution
    login_widget()
    st.stop()
else:
    # If logged in, display the logout button in the sidebar
    logout_button() 

# =================================================================
# 3. MAIN UI AFTER LOGIN
# =================================================================

st.title("💡 Welcome to the MIND Unified Dashboard")
st.write(f"Hello **{username}** 👋")
st.write(f"Your current access role: **{user_role}**")

st.markdown("""
This platform provides real-time analytics and insights across key domains:
* **Student Performance** 📊
* **Faculty Cohort Insights** 🎓
* **System Reliability & Environment Quality** 💻
* **Institution-wide Administrative KPIs** 📈

Please use the sidebar on the left to navigate the dashboards available to your role.
""")

st.divider()

# Role-based page access reminder (Improves UX)
if user_role == "Student":
    st.info("You have access to the **Student Dashboard** only.")
elif user_role == "Faculty":
    st.info("You have access to the **Faculty Dashboard** and related analytics.")
elif user_role == "Developer":
    st.info("You have access to the **Developer Dashboard** (Reliability & Environment) and related analytics.")
elif user_role == "Admin":
    st.success("You have access to **all dashboards** listed in the sidebar.")

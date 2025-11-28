import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional, Any, List, Tuple

# Assuming theme.py is in the root and defines these color constants
try:
    from theme import PRIMARY_COLOR, SECONDARY_BACKGROUND_COLOR
except ImportError:
    # Fallback to hardcoded colors if theme.py is not ready or imports fail
    PRIMARY_COLOR = "#004B7A" # Used for headers, borders
    SECONDARY_BACKGROUND_COLOR = "#ECF1F3" # Used for KPI background
    ACCENT_COLOR = "#BD300E" # Used for HR/Accent lines


# ---------- KPI CARD ----------
def kpi_card(label: str, value: Any, delta: Optional[Any] = None, help_text: Optional[str] = None):
    """
    Renders a custom-styled KPI card.
    
    NOTE: Using st.markdown with HTML/CSS for custom look, which bypasses st.metric's native delta handling.
    """
    
    # Format the delta value with a color (green for positive, red for negative)
    delta_html = ""
    if delta is not None:
        try:
            float_delta = float(delta)
            color = "green" if float_delta >= 0 else "red"
            delta_html = f'<span style="color: {color}; font-size: 0.8em;">({float_delta:+.2f})</span>'
        except ValueError:
            delta_html = f'<span style="font-size: 0.8em;">({delta})</span>'


    html_content = f"""
        <div style="
            background-color:{SECONDARY_BACKGROUND_COLOR};
            padding:15px;
            border-radius:10px;
            border-left:6px solid {PRIMARY_COLOR};
            height: 100%;
        ">
            <p style="margin:0; color:#555555; font-size: 0.9em; line-height: 1.2;">{label}</p>
            <h3 style="margin: 5px 0 0 0; color:{PRIMARY_COLOR};">
                {value} {delta_html}
            </h3>
        </div>
    """
    
    st.markdown(html_content, unsafe_allow_html=True)

    if help_text:
        # Use native st.caption for standard styling below the card
        st.caption(help_text)


# ---------- SECTION HEADER ----------
def section_header(text: str):
    """
    Renders a custom-styled header for sections.
    """
    try:
        hr_color = ACCENT_COLOR
    except NameError:
        hr_color = "#bd300e" # Fallback accent color

    st.markdown(
        f"""
        <h2 style="color:{PRIMARY_COLOR}; margin-top:25px; margin-bottom:5px;">{text}</h2>
        <hr style="border:1px solid {hr_color}; margin-bottom:20px;">
        """,
        unsafe_allow_html=True
    )


# ---------- GENERIC PLOTLY WRAPPERS ----------

# Standard Plotly template for better theme integration
DEFAULT_TEMPLATE = "plotly_white" 
# Use PRIMARY_COLOR for main plot elements if specific color column isn't used
DEFAULT_COLOR = PRIMARY_COLOR

def _base_plot_update(fig: go.Figure) -> go.Figure:
    """Applies common layout updates to all plots."""
    fig.update_layout(
        height=400,
        margin=dict(t=50, b=50, l=50, r=50),
        template=DEFAULT_TEMPLATE,
        hovermode="x unified"
    )
    return fig


def plot_line(df: pd.DataFrame, x: str, y: str, color: Optional[str] = None, title: Optional[str] = None):
    """Renders a line plot."""
    fig = px.line(df, x=x, y=y, color=color, title=title, color_discrete_sequence=[DEFAULT_COLOR])
    st.plotly_chart(_base_plot_update(fig), use_container_width=True)


def plot_bar(df: pd.DataFrame, x: str, y: str, color: Optional[str] = None, title: Optional[str] = None):
    """Renders a bar plot."""
    fig = px.bar(df, x=x, y=y, color=color, title=title, color_discrete_sequence=[DEFAULT_COLOR])
    st.plotly_chart(_base_plot_update(fig), use_container_width=True)


def plot_hist(df: pd.DataFrame, x: str, title: Optional[str] = None):
    """Renders a histogram."""
    fig = px.histogram(df, x=x, title=title, color_discrete_sequence=[DEFAULT_COLOR])
    st.plotly_chart(_base_plot_update(fig), use_container_width=True)


def plot_scatter(df: pd.DataFrame, x: str, y: str, color: Optional[str] = None, title: Optional[str] = None):
    """Renders a scatter plot."""
    fig = px.scatter(df, x=x, y=y, color=color, title=title, color_discrete_sequence=[DEFAULT_COLOR])
    st.plotly_chart(_base_plot_update(fig), use_container_width=True)


# ---------- EMPTY / LOADER ----------

def show_empty(message: str = "No data available"):
    """Displays an information box for missing data."""
    st.info(message)


def loading_spinner():
    """Returns a context manager for showing a loading spinner."""
    return st.spinner("Loading...please wait")


# ---------- CARD ROW LAYOUT ----------
def kpi_row(kpi_list: List[Tuple[str, Any, Optional[Any]]]):
    """
    Takes a list of (label, value, delta) tuples and displays them using kpi_card 
    in equal columns.
    """
    cols = st.columns(len(kpi_list))
    
    # Ensure there are columns to zip with the list
    if not cols or not kpi_list:
        return
        
    for col, (label, value, delta) in zip(cols, kpi_list):
        with col:
            # Pass delta directly to kpi_card
            kpi_card(label, value, delta=delta)

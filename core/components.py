import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# ---------- KPI CARD ----------
def kpi_card(label: str, value, delta=None, help_text=None):
    """
    Renders a KPI card with optional delta values.
    """
    st.markdown(
        f"""
        <div style="
            background-color:#ecf1f3;
            padding:15px;
            border-radius:10px;
            border-left:6px solid #203891;
            margin-bottom:10px;
        ">
            <h3 style="margin:0; color:#203891;">{value}</h3>
            <p style="margin:0; color:#232020;">{label}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if delta:
        st.caption(f"Δ {delta}")

    if help_text:
        st.caption(help_text)


# ---------- SECTION HEADER ----------
def section_header(text: str):
    st.markdown(
        f"""
        <h2 style="color:#203891; margin-top:25px;">{text}</h2>
        <hr style="border:1px solid #bd300e; margin-bottom:20px;">
        """,
        unsafe_allow_html=True
    )


# ---------- GENERIC PLOTLY WRAPPERS ----------
def plot_line(df, x, y, color=None, title=None):
    fig = px.line(df, x=x, y=y, color=color, title=title)
    fig.update_layout(height=400, plot_bgcolor="#ffffff")
    st.plotly_chart(fig, use_container_width=True)


def plot_bar(df, x, y, color=None, title=None):
    fig = px.bar(df, x=x, y=y, color=color, title=title)
    fig.update_layout(height=400, plot_bgcolor="#ffffff")
    st.plotly_chart(fig, use_container_width=True)


def plot_hist(df, x, title=None):
    fig = px.histogram(df, x=x, title=title)
    fig.update_layout(height=400, plot_bgcolor="#ffffff")
    st.plotly_chart(fig, use_container_width=True)


def plot_scatter(df, x, y, color=None, title=None):
    fig = px.scatter(df, x=x, y=y, color=color, title=title)
    fig.update_layout(height=400, plot_bgcolor="#ffffff")
    st.plotly_chart(fig, use_container_width=True)


# ---------- EMPTY / LOADER ----------

def show_empty(message="No data available"):
    st.info(message)


def loading_spinner():
    return st.spinner("Loading...please wait")


# ---------- CARD ROW LAYOUT ----------
def kpi_row(kpi_list: list):
    """
    Takes a list of (label, value) tuples and displays them in equal columns.
    """
    cols = st.columns(len(kpi_list))
    for col, (label, value) in zip(cols, kpi_list):
        with col:
            kpi_card(label, value)


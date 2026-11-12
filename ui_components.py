"""
TrendScope - Custom UI Styling and Component Library
Professional Dark Theme Layout Engine
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg-main: #090d16;
    --bg-card: #0f172a;
    --border-color: #1e293b;
    --primary: #6366f1;
    --cyan: #06b6d4;
    --emerald: #10b981;
    --amber: #f59e0b;
    --rose: #f43f5e;
    --text-primary: #f8fafc;
    --text-muted: #94a3b8;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-primary);
}

.stApp {
    background-color: var(--bg-main);
}

section[data-testid="stSidebar"] {
    background-color: #0b1120;
    border-right: 1px solid var(--border-color);
}

.kpi-container {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 12px;
}

.kpi-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94a3b8;
    margin-bottom: 4px;
}

.kpi-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.2;
}

.kpi-subtext {
    font-size: 0.75rem;
    color: #64748b;
    margin-top: 4px;
}

.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #f8fafc;
    margin-top: 24px;
    margin-bottom: 4px;
    border-left: 3px solid #6366f1;
    padding-left: 10px;
}

.section-desc {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-bottom: 16px;
    padding-left: 13px;
}

.log-box {
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 6px;
    padding: 12px;
    font-family: 'Fira Code', monospace;
    font-size: 0.8rem;
    color: #38bdf8;
    line-height: 1.4;
}

div[data-testid="stMetricValue"] {
    font-size: 1.6rem !important;
    font-weight: 700 !important;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #1e293b;
    border-radius: 8px;
    overflow: hidden;
}
</style>
"""

def inject_styles():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def render_kpi(label, value, subtext="", border_color="#6366f1"):
    st.markdown(f"""
    <div class="kpi-container" style="border-top: 2px solid {border_color};">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-subtext">{subtext}</div>
    </div>
    """, unsafe_allow_html=True)

def render_header(title, description=""):
    st.markdown(f"""
    <div class="section-title">{title}</div>
    <div class="section-desc">{description}</div>
    """, unsafe_allow_html=True)

def apply_plotly_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.6)",
        font=dict(family="Inter, sans-serif", color="#e2e8f0", size=11),
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(
            bgcolor="rgba(15, 23, 42, 0.8)",
            bordercolor="#1e293b",
            borderwidth=1
        ),
        xaxis=dict(
            gridcolor="#1e293b",
            zerolinecolor="#334155",
            showline=True,
            linecolor="#334155"
        ),
        yaxis=dict(
            gridcolor="#1e293b",
            zerolinecolor="#334155",
            showline=True,
            linecolor="#334155"
        )
    )
    return fig

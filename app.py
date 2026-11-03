# ================================================================
# VALUATION MATRIX AI
# Professional Financial Analysis & Business Valuation SaaS
# Framework: Python + Streamlit
# Deployment: Streamlit Community Cloud
# ================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io

# ================================================================
# 1. PAGE CONFIGURATION
# ================================================================

st.set_page_config(
    page_title="Valuation Matrix AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================
# 2. PROFESSIONAL UI STYLING
# ================================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #0b1120;
        color: #e2e8f0;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #263449;
    }

    [data-testid="stSidebar"] * {
        color: #e2e8f0;
    }

    .main-title {
        font-size: 35px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -1.2px;
    }

    .subtitle {
        font-size: 14px;
        color: #94a3b8;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #60a5fa;
        margin-top: 20px;
        margin-bottom: 12px;
    }

    .info-card {
        background: linear-gradient(135deg, #17243a, #111827);
        border: 1px solid #263449;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
    }

    .info-label {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
    }

    .info-value {
        color: #ffffff;
        font-size: 25px;
        font-weight: 800;
        margin-top: 7px;
    }

    .positive {
        color: #34d399;
    }

    .negative {
        color: #f87171;
    }

    .stButton > button {
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 700;
        width: 100%;
        min-height: 42px;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #1d4ed8, #6d28d9);
        border: none;
    }

    div[data-testid="stMetric"] {
        background-color: #111c2e;
        border: 1px solid #263449;
        padding: 16px;
        border-radius: 10px;
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff;
    }

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 12px;
        padding: 25px 0;
        border-top: 1px solid #263449;
        margin-top: 35px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ================================================================
# 3. FINANCIAL CALCULATION FUNCTIONS
# ================================================================

def safe_divide(numerator, denominator, default=0.0):
    """Safely divide two numbers."""
    if denominator is None or abs(denominator) < 1e-12:
        return default
    return numerator / denominator


def calculate_revenue_projection(
    revenue,
    growth_rates,
    years
):
    """Calculate projected annual revenue."""

    projections = []
    current_revenue = revenue

    for year in range(years):
        growth = growth_rates[year]
        current_revenue *= (1 + growth)
        projections.append(current_revenue)

    return projections


def calculate_ebitda(revenue, margin):
    """Calculate EBITDA."""
    return revenue * margin


def calculate_free_cash_flow(
    revenue,
    ebit_margin,
    tax_rate,
    da_percentage,
    capex_percentage,
    nwc_percentage
):
    """Calculate unlevered free cash flow."""

    ebit = revenue * ebit_margin

    taxes = max(0, ebit * tax_rate)

    depreciation = revenue * da_percentage

    capex = revenue * capex_percentage

    change_nwc = revenue * nwc_percentage

    nopat = ebit - taxes

    free_cash_flow = ()
    nopat
   # ================================================================
# VALUATION MATRIX AI
# Professional Financial Analysis & Business Valuation SaaS
# Framework: Python + Streamlit
# Deployment: Streamlit Community Cloud
# ================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io

# ================================================================
# 1. PAGE CONFIGURATION
# ================================================================

st.set_page_config(
    page_title="Valuation Matrix AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================
# 2. PROFESSIONAL UI STYLING
# ================================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #0b1120;
        color: #e2e8f0;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #263449;
    }

    [data-testid="stSidebar"] * {
        color: #e2e8f0;
    }

    .main-title {
        font-size: 35px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -1.2px;
    }

    .subtitle {
        font-size: 14px;
        color: #94a3b8;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #60a5fa;
        margin-top: 20px;
        margin-bottom: 12px;
    }

    .info-card {
        background: linear-gradient(135deg, #17243a, #111827);
        border: 1px solid #263449;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
    }

    .info-label {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
    }

    .info-value {
        color: #ffffff;
        font-size: 25px;
        font-weight: 800;
        margin-top: 7px;
    }

    .positive {
        color: #34d399;
    }

    .negative {
        color: #f87171;
    }

    .stButton > button {
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 700;
        width: 100%;
        min-height: 42px;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #1d4ed8, #6d28d9);
        border: none;
    }

    div[data-testid="stMetric"] {
        background-color: #111c2e;
        border: 1px solid #263449;
        padding: 16px;
        border-radius: 10px;
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff;
    }

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 12px;
        padding: 25px 0;
        border-top: 1px solid #263449;
        margin-top: 35px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ================================================================
# 3. FINANCIAL CALCULATION FUNCTIONS
# ================================================================

def safe_divide(numerator, denominator, default=0.0):
    """Safely divide two numbers."""
    if denominator is None or abs(denominator) < 1e-12:
        return default
    return numerator / denominator


def calculate_revenue_projection(
    revenue,
    growth_rates,
    years
):
    """Calculate projected annual revenue."""

    projections = []
    current_revenue = revenue

    for year in range(years):
        growth = growth_rates[year]
        current_revenue *= (1 + growth)
        projections.append(current_revenue)

    return projections


def calculate_ebitda(revenue, margin):
    """Calculate EBITDA."""
    return revenue * margin


def calculate_free_cash_flow(
    revenue,
    ebit_margin,
    tax_rate,
    da_percentage,
    capex_percentage,
    nwc_percentage
):
    """Calculate unlevered free cash flow."""

    ebit = revenue * ebit_margin

    taxes = max(0, ebit * tax_rate)

    depreciation = revenue * da_percentage

    capex = revenue * capex_percentage

    change_nwc = revenue * nwc_percentage

    nopat = ebit - taxes

    free_cash_flow = (
        nopat
        + depreciation + depreciation

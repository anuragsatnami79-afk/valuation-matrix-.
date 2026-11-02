import streamlit as st
import pandas as pd
import numpy as np

from datetime import datetime


# ==========================================================
# VALUATION MATRIX AI
# Created by mr Anurag
# ==========================================================

st.set_page_config(
    page_title="Valuation Matrix AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #080D19;
    color: #FFFFFF;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

.main-title {
    font-size: 35px;
    font-weight: 800;
    color: #FFFFFF;
    text-align: center;
}

.subtitle {
    color: #94A3B8;
    text-align: center;
    font-size: 14px;
}

.creator {
    color: #38BDF8;
    text-align: center;
    font-weight: 600;
}

.section-title {
    color: #38BDF8;
    font-size: 22px;
    font-weight: 700;
    margin-top: 20px;
}

.metric-card {
    background: #111B2E;
    border: 1px solid #24344F;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 10px;
}

.metric-label {
    font-size: 13px;
    color: #94A3B8;
}

.metric-value {
    font-size: 25px;
    font-weight: 800;
    color: #FFFFFF;
}

.metric-description {
    font-size: 12px;
    color: #38BDF8;
}

.buy {
    color: #22C55E;
    font-size: 30px;
    font-weight: 800;
}

.hold {
    color: #FACC15;
    font-size: 30px;
    font-weight: 800;
}

.sell {
    color: #EF4444;
    font-size: 30px;
    font-weight: 800;
}

.report-card {
    background: #111B2E;
    border-left: 4px solid #38BDF8;
    padding: 20px;
    border-radius: 10px;
    margin: 12px 0;
}

.payment-card {
    background: #13243A;
    border: 1px solid #38BDF8;
    border-radius: 15px;
    padding: 25px;
    text-align: center;
}

.disclaimer {
    color: #94A3B8;
    font-size: 11px;
    line-height: 1.7;
}

div.stButton > button {
    background: #0284C7;
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: 700;
    min-height: 45px;
    width: 100%;
}

div.stButton > button:hover {
    background: #0369A1;
    color: white;
}

[data-testid="stMetric"] {
    background: #111B2E;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #24344F;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def money(value):
    if value is None or not np.isfinite(value):
        return "N/A"

    return f"₹{value:,.2f}"


def percentage(value):
    if value is None or not np.isfinite(value):
        return "N/A"

    return f"{value:.2f}%"


def safe_divide(a, b):

    if b is None or b == 0:
        return None

    return a / b


def metric_card(title, value, description=""):

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-description">{description}</div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================================
# DCF VALUATION ENGINE
# ==========================================================

def calculate_dcf(
    fcff,
    growth,
    wacc,
    terminal_growth,
    years,
    shares,
    debt,
    cash
):

    if shares <= 0:
        raise ValueError("Shares outstanding must be positive.")

    if wacc <= terminal_growth:
        raise ValueError(
            "WACC must be greater than terminal growth."
        )

    if wacc <= -1 or terminal_growth <= -1:
        raise ValueError("Invalid discount or growth rate.")

    if years < 1:
        raise ValueError("Projection years must be positive.")

    projected_cashflows = []
    present_values = []

    for year in range(1, years + 1):

        future_fcff = fcff * (
            (1 + growth) ** year
        )

        discount_factor = (
            1 + wacc
        ) ** year

        pv = future_fcff / discount_factor

        projected_cashflows.append(future_fcff)
        present_values.append(pv)

    terminal_fcff = (
        projected_cashflows[-1] *
        (1 + terminal_growth)
    )

    terminal_value = (
        terminal_fcff /
        (wacc - terminal_growth)
    )

    terminal_pv = (
        terminal_value /
        ((1 + wacc) ** years)
    )

    enterprise_value = (
        sum(present_values) + terminal_pv
    )

    net_debt = debt - cash

    equity_value = (
        enterprise_value - net_debt
    )

    intrinsic_value = (
        equity_value / shares
    )

    return {
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "intrinsic_value": intrinsic_value,
        "terminal_value": terminal_value,
        "terminal_pv": terminal_pv,
        "projected_cashflows": projected_cashflows,
        "present_values": present_values
    }


# ==========================================================
# GRAHAM ANALYSIS
# ==========================================================

def graham_analysis(
    current_assets,
    total_liabilities,
    shares,
    stock_price,
    debt,
    equity
):

    ncav = current_assets - total_liabilities

    ncav_per_share = (
        ncav / shares if shares > 0 else 0
    )

    debt_equity = (
        debt / equity if equity > 0 else None
    )

    net_net_price = max(
        0,
        ncav_per_share
    )

    net_net_discount = (
        (net_net_price - stock_price) /
        stock_price * 100
        if stock_price > 0 else None
    )

    if ncav > 0 and stock_price < net_net_price:
        net_net_status = "PASS"
    else:
        net_net_status = "FAIL"

    if debt_equity is None:
        debt_status = "INSUFFICIENT DATA"
    elif debt_equity <= 0.5:
        debt_status = "STRONG"
    elif debt_equity <= 1:
        debt_status = "MODERATE"
    else:
        debt_status = "HIGH DEBT"

    return {
        "ncav": ncav,
        "ncav_per_share": ncav_per_share,
        "net_net_status": net_net_status,
        "net_net_discount": net_net_discount,
        "debt_equity": debt_equity,
        "debt_status": debt_status
    }


# ==========================================================
# BUFFETT OWNER EARNINGS
# ==========================================================

def calculate_owner_earnings(
    operating_cash_flow,
    capex
):

    owner_earnings = (
        operating_cash_flow - capex
    )

    return owner_earnings


# ==========================================================
# LYNCH PEG ANALYSIS
# ==========================================================

def calculate_peg(
    stock_price,
    net_income,
    shares,
    earnings_growth
):

    if shares <= 0 or earnings_growth <= 0:
        return None, None, None

    eps = net_income / shares

    if eps <= 0:
        return eps, None, None

    pe_ratio = stock_price / eps

    peg = pe_ratio / earnings_growth

    return eps, pe_ratio, peg


def classify_stock(growth):

    if growth >= 20:
        return "FAST GROWER"

    elif growth >= 10:
        return "STALWART"

    else:
        return "SLOW GROWER"


# ==========================================================
# MOAT SCORE
# ==========================================================

def calculate_moat(
    brand,
    roic,
    free_cash_flow
):

    score = 0

    if brand >= 4:
        score += 1

    if roic >= 15:
        score += 1

    if free_cash_flow > 0:
        score += 1

    if score == 3:
        rating = "STRONG ECONOMIC MOAT"

    elif score == 2:
        rating = "MODERATE ECONOMIC MOAT"

    else:
        rating = "WEAK ECONOMIC MOAT"

    return score, rating


# ==========================================================
# VERDICT ENGINE
# ==========================================================

def generate_verdict(
    intrinsic_value,
    safe_price,
    current_price,
    owner_earnings,
    debt_status,
    peg,
    fisher_score,
    moat_score
):

    if intrinsic_value <= 0:
        return "OVERVALUED", (
            "DCF equity value is non-positive. "
            "The company requires further investigation."
        )

    if current_price <= safe_price:

        if owner_earnings > 0 and debt_status in [
            "STRONG", "MODERATE"
        ]:

            return "BUY", (
                "Price is at or below the 25% margin-of-safety "
                "price, with positive owner earnings and "
                "acceptable debt levels."
            )

    if current_price <= intrinsic_value:

        return "HOLD", (
            "The stock trades below estimated intrinsic value "
            "but does not satisfy all conservative buying criteria."
        )

    return "OVERVALUED", (
        "The current stock price exceeds estimated intrinsic value."
    )


# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    '<div class="main-title">📊 VALUATION MATRIX AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Institutional-Style Stock Valuation & Fundamental Analysis'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="creator">Created by mr Anurag</div>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("📊 Valuation Matrix")

    st.write("Fundamental Analysis Engine")

    st.divider()

    st.markdown("### Knowledge Framework")

    st.write("1. Damodaran - DCF Valuation")

    st.write("2. Graham - Margin of Safety")

    st.write("3. Fisher - Business Quality")

    st.write("4. Buffett - Economic Moat")

    st.write("5. Lynch - Growth & PEG")

    st.divider()

    st.caption("Version 1.0")

    st.caption("Created by mr Anurag")


# ==========================================================
# INPUT SECTION
# ==========================================================

st.markdown(
    '<div class="section-title">🏢 Company Financial Inputs</div>',
    unsafe_allow_html=True
)

with st.form("valuation_form"):

    company_name = st.text_input(
        "Company Name",
        value="Example Company"
    )

    col1, col2 = st.columns(2)

    with col1:

        revenue = st.number_input(
            "Revenue (₹ Crore)",
            min_value=0.0,
            value=1000.0
        )

        net_income = st.number_input(
            "Net Income (₹ Crore)",
            value=100.0
        )

        operating_cash_flow = st.number_input(
            "Operating Cash Flow (₹ Crore)",
            value=150.0
        )

        total_debt = st.number_input(
            "Total Debt (₹ Crore)",
            min_value=0.0,
            value=100.0
        )

        cash = st.number_input(
            "Cash & Short Term Investments (₹ Crore)",
            min_value=0.0,
            value=50.0
        )

    with col2:

        growth_rate = st.number_input(
            "Expected Annual Growth Rate (%)",
            min_value=-99.0,
            max_value=200.0,
            value=12.0
        )

        wacc = st.number_input(
            "Discount Rate / WACC (%)",
            min_value=0.1,
            max_value=100.0,
            value=10.0
        )

        stock_price = st.number_input(
            "Current Stock Price (₹)",
            min_value=0.01,
            value=500.0
        )

        shares = st.number_input(
            "Shares Outstanding (Crore)",
            min_value=0.001,
            value=1.0
        )

        equity = st.number_input(
            "Shareholders' Equity (₹ Crore)",
            min_value=0.0,
            value=500.0
        )

    st.divider()

    st.markdown("### Advanced Financial Inputs")

    a, b = st.columns(2)

    with a:

        capex = st.number_input(
            "Capital Expenditure (₹ Crore)",
            min_value=0.0,
            value=40.0
        )

        interest_expense = st.number_input(
            "Interest Expense (₹ Crore)",
            min_value=0.0,
            value=5.0
        )

        tax_rate = st.number_input(
            "Effective Tax Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=25.0
        )

        terminal_growth = st.number_input(
            "Terminal Growth Rate (%)",
            min_value=-5.0,
            max_value=20.0,
            value=4.0
        )

    with b:

        projection_years = st.number_input(
            "DCF Projection Period (Years)",
            min_value=1,
            max_value=20,
            value=5
        )

        earnings_growth = st.number_input(
            "Expected EPS Growth (%)",
            min_value=-100.0,
            max_value=200.0,
            value=15.0
        )

        current_assets = st.number_input(
            "Current Assets (₹ Crore)",
            min_value=0.0,
            value=400.0
        )

        total_liabilities = st.number_input(
            "Total Liabilities (₹ Crore)",
            min_value=0.0,
            value=200.0
        )

    st.divider()

    st.markdown("### Philip Fisher Quality Checklist")

    c1, c2 = st.columns(2)

    with c1:

        rnd_score = st.slider(
            "R&D / Innovation Quality",
            1, 5, 3
        )

        margin_score = st.slider(
            "Profit Margin Expansion",
            1, 5, 3
        )

    with c2:

        management_score = st.slider(
            "Management Quality",
            1, 5, 3
        )

        brand_score = st.slider(
            "Brand Power",
            1, 5, 3
        )

    roic = st.number_input(
        "Return on Invested Capital (%)",
        min_value=-100.0,
        max_value=200.0,
        value=18.0
    )

    submitted = st.form_submit_button(
        "🚀 ANALYZE COMPANY",
        use_container_width=True
    )


# ==========================================================
# CALCULATION ENGINE
# ==========================================================

if submitted:

    errors = []

    if revenue <= 0:
        errors.append("Revenue must be positive.")

    if shares <= 0:
        errors.append("Shares outstanding must be positive.")

    if stock_price <= 0:
        errors.append("Stock price must be positive.")

    if net_income < 0:
        st.warning(
            "Negative net income: conventional P/E and PEG "
            "interpretation may not be meaningful."
        )

    if operating_cash_flow < 0:
        st.warning(
            "Negative operating cash flow: cash-flow valuation "
            "requires additional investigation."
        )

    if wacc <= terminal_growth:
        errors.append(
            "WACC must be greater than terminal growth."
        )

    if earnings_growth <= 0:
        st.warning(
            "PEG cannot be meaningfully calculated with "
            "non-positive EPS growth."
        )

    if errors:

        for error in errors:
            st.error(error)

        st.stop()

    # FCFF:
    # CFO - CAPEX + after-tax interest expense.
    #
    # This assumes CFO is after interest payments.

    after_tax_interest = (
        interest_expense * (1 - tax_rate / 100)
    )

    fcff = (
        operating_cash_flow
        - capex
        + after_tax_interest
    )

    # DCF

    dcf = calculate_dcf(
        fcff=fcff,
        growth=growth_rate / 100,
        wacc=wacc / 100,
        terminal_growth=terminal_growth / 100,
        years=int(projection_years),
        shares=shares,
        debt=total_debt,
        cash=cash
    )

    intrinsic_value = dcf["intrinsic_value"]

    safe_price = intrinsic_value * 0.75

    margin_of_safety = (
        (intrinsic_value - stock_price) /
        intrinsic_value * 100
    ) if intrinsic_value > 0 else None

    # OWNER EARNINGS

    owner_earnings = calculate_owner_earnings(
        operating_cash_flow,
        capex
    )

    # GRAHAM

    graham = graham_analysis(
        current_assets,
        total_liabilities,
        shares,
        stock_price,
        total_debt,
        equity
    )

    # LYNCH

    eps, pe_ratio, peg = calculate_peg(
        stock_price,
        net_income,
        shares,
        earnings_growth
    )

    stock_category = classify_stock(
        growth_rate
    )

    # FISHER

    fisher_score = (
        rnd_score +
        margin_score +
        management_score
    )

    fisher_percentage = (
        fisher_score / 15
    ) * 100

    # BUFFETT

    moat_score, moat_rating = calculate_moat(
        brand_score,
        roic,
        owner_earnings
    )

    # VERDICT

    verdict, verdict_reason = generate_verdict(
        intrinsic_value,
        safe_price,
        stock_price,
        owner_earnings,
        graham["debt_status"],
        peg,
        fisher_score,
        moat_score
    )

    st.session_state["analysis"] = {
        "company": company_name,
        "intrinsic": intrinsic_value,
        "safe_price": safe_price,
        "margin": margin_of_safety,
        "fcff": fcff,
        "owner_earnings": owner_earnings,
        "peg": peg,
        "pe": pe_ratio,
        "eps": eps,
        "category": stock_category,
        "graham": graham,
        "fisher_score": fisher_score,
        "fisher_percentage": fisher_percentage,
        "moat_score": moat_score,
        "moat_rating": moat_rating,
        "verdict": verdict,
        "reason": verdict_reason,
        "dcf": dcf,
        "price": stock_price,
        "revenue": revenue,
        "net_income": net_income,
        "growth": growth_rate
    }


# ==========================================================
# RESULTS DASHBOARD
# ==========================================================

if "analysis" in st.session_state:

    data = st.session_state["analysis"]

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '📈 VALUATION RESULTS DASHBOARD'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"### {data['company']}"
    )

    verdict = data["verdict"]

    if verdict == "BUY":

        st.markdown(
            '<div class="buy">🟢 BUY</div>',
            unsafe_allow_html=True
        )

    elif verdict == "HOLD":

        st.markdown(
            '<div class="hold">🟡 HOLD</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="sell">🔴 OVERVALUED</div>',
            unsafe_allow_html=True
        )

    st.info(data["reason"])

    # Main metrics

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Intrinsic Value",
            money(data["intrinsic"])
        )

    with c2:

        st.metric(
            "Safe Buying Price",
            money(data["safe_price"])
        )

    with c3:

        st.metric(
            "Current Price",
            money(data["price"])
        )

    c4, c5, c6 = st.columns(3)

    with c4:

        st.metric(
            "Margin of Safety",
            percentage(data["margin"])
        )

    with c5:

        st.metric(
            "PEG Ratio",
            "N/A" if data["peg"] is None
            else f"{data['peg']:.2f}"
        )

    with c6:

        st.metric(
            "Debt / Equity",
            "N/A" if data["graham"]["debt_equity"] is None
            else f"{data['graham']['debt_equity']:.2f}"
        )

    st.divider()

    # Valuation chart

    st.markdown("### Price vs Intrinsic Value")

    chart_data = pd.DataFrame({
        "Valuation": [
            "Current Price",
            "Safe Buying Price",
            "Intrinsic Value"
        ],
     

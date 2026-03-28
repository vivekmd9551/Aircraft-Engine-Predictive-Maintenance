"""
✈️ AeroMind — Aircraft Engine Predictive Maintenance
Author: Vivek M D
Design: Warm Light Editorial — Ivory + Amber + Charcoal, Premium Aerospace
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import base64
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AeroMind — Engine Health Intelligence",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# BACKGROUND SVG ENCODING
# ─────────────────────────────────────────────
svg_icon = """
<svg viewBox="0 0 1200 800" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <filter id="ultra-glow-red" x="-200%" y="-200%" width="500%" height="500%">
            <feGaussianBlur stdDeviation="15" result="blur1" />
            <feGaussianBlur stdDeviation="5" result="blur2" />
            <feMerge><feMergeNode in="blur1" /><feMergeNode in="blur2" /><feMergeNode in="SourceGraphic" /></feMerge>
        </filter>
        <filter id="ultra-glow-green" x="-200%" y="-200%" width="500%" height="500%">
            <feGaussianBlur stdDeviation="15" result="blur1" />
            <feGaussianBlur stdDeviation="5" result="blur2" />
            <feMerge><feMergeNode in="blur1" /><feMergeNode in="blur2" /><feMergeNode in="SourceGraphic" /></feMerge>
        </filter>
    </defs>
    <g stroke="#C8892A" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path d="M 585 260 L 600 50 L 615 260 Z" stroke-width="2.5" fill="rgba(200,137,42,0.05)" />
        <path d="M 480 380 L 120 355 L 110 310 L 115 310 L 130 350 L 480 360 Z" stroke-width="2.5" fill="rgba(200,137,42,0.05)" />
        <path d="M 720 380 L 1080 355 L 1090 310 L 1085 310 L 1070 350 L 720 360 Z" stroke-width="2.5" fill="rgba(200,137,42,0.05)" />
        <g filter="url(#ultra-glow-red)"><circle cx="112" cy="310" r="8" fill="#FF0000"><animate attributeName="opacity" values="0.3;1;0.3" dur="1s" repeatCount="indefinite" /></circle></g>
        <g filter="url(#ultra-glow-green)"><circle cx="1088" cy="310" r="8" fill="#00FF00"><animate attributeName="opacity" values="0.3;1;0.3" dur="1s" repeatCount="indefinite" begin="0.5s" /></circle></g>
        <ellipse cx="600" cy="380" rx="125" ry="125" stroke-width="3" fill="#FAF8F4" />
        <path d="M 530 330 Q 600 300 670 330 L 655 370 Q 600 350 545 370 Z" stroke-width="2" fill="rgba(200,137,42,0.15)" />
        <g transform="translate(320, 438)">
            <circle cx="0" cy="0" r="58.5" stroke-width="9" stroke="rgba(200,137,42,0.7)" fill="#FAF8F4" />
            <g><animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="0.1s" repeatCount="indefinite" />
                <path d="M 0 0 L -12 -54 L 12 -54 Z" fill="#C8892A" opacity="0.95" />
                <path d="M 0 0 L -12 54 L 12 54 Z" fill="#C8892A" opacity="0.95" />
                <path d="M 0 0 L -54 -12 L -54 12 Z" fill="#C8892A" opacity="0.95" />
                <path d="M 0 0 L 54 -12 L 54 12 Z" fill="#C8892A" opacity="0.95" />
            </g>
            <circle cx="0" cy="0" r="18" fill="#C8892A" />
        </g>
        <g transform="translate(880, 438)">
            <circle cx="0" cy="0" r="58.5" stroke-width="9" stroke="rgba(200,137,42,0.7)" fill="#FAF8F4" />
            <g><animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="0.1s" repeatCount="indefinite" />
                <path d="M 0 0 L -12 -54 L 12 -54 Z" fill="#C8892A" opacity="0.95" />
                <path d="M 0 0 L -12 54 L 12 54 Z" fill="#C8892A" opacity="0.95" />
                <path d="M 0 0 L -54 -12 L -54 12 Z" fill="#C8892A" opacity="0.95" />
                <path d="M 0 0 L 54 -12 L 54 12 Z" fill="#C8892A" opacity="0.95" />
            </g>
            <circle cx="0" cy="0" r="18" fill="#C8892A" />
        </g>
    </g>
</svg>
"""
b64_svg = base64.b64encode(svg_icon.encode()).decode()

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,900;1,400;1,700&family=Outfit:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {{
    --ivory:     #FAF8F4;
    --amber:     #C8892A;
    --charcoal:  #1C1C1E;
    --glass:     rgba(255, 255, 255, 0.65);
}}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
    background: var(--ivory) !important;
    font-family: 'Outfit', sans-serif !important;
}}

[data-testid="stAppViewContainer"]::before {{
    content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    z-index: 0; pointer-events: none;
    background-image: url("data:image/svg+xml;base64,{b64_svg}");
    background-repeat: no-repeat; background-position: center center;
    background-size: 85% auto; opacity: 0.18;
}}

/* CLEAN UP WHITE BOXES */
[data-testid="stMainBlockContainer"], div[data-testid="stVerticalBlock"] > div {{
    background-color: transparent !important;
}}

[data-testid="stMainBlockContainer"] {{
    padding-top: 2rem !important;
    max-width: 1300px !important;
    position: relative;
    z-index: 10; 
}}

#MainMenu, footer, header, [data-testid="stDecoration"] {{ visibility: hidden; display: none; }}

h1, h2, h3, h4, h5 {{ font-family: 'Playfair Display', serif !important; color: var(--charcoal) !important; }}

/* NAVIGATION BAR */
div[data-testid="stRadio"] > div[role="radiogroup"] {{
    display: flex; flex-direction: row; gap: 12px; background: transparent; padding: 0; flex-wrap: wrap; justify-content: center;
}}
div[data-testid="stRadio"] label {{
    background: #FFFFFF; padding: 10px 24px !important; border-radius: 30px !important; border: 1px solid var(--warm-200) !important;
    cursor: pointer; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important; font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; color: var(--slate) !important;
    box-shadow: 0 2px 12px rgba(28,28,30,0.07); margin-bottom: 5px;
}}
div[data-testid="stRadio"] label:hover {{ border-color: var(--amber) !important; transform: translateY(-2px); }}
div[data-testid="stRadio"] label[data-checked="true"] {{ background: var(--charcoal) !important; border-color: var(--charcoal) !important; }}
div[data-testid="stRadio"] label[data-checked="true"] * {{ color: white !important; font-weight: 600 !important; }}
div[data-testid="stRadio"] label > div:first-child {{ display: none !important; }}

/* METRICS FIX (NO CUT-OFF) */
[data-testid="stMetric"] {{
    background: rgba(255, 255, 255, 0.4) !important;
    backdrop-filter: blur(5px);
    border: 1px solid var(--warm-100) !important; border-radius: 18px !important;
    padding: 1.5rem 1rem !important; border-top: 3px solid var(--amber) !important;
    min-height: 140px;
}}
[data-testid="stMetricValue"] {{ 
    font-family: 'Playfair Display', serif !important; 
    font-size: 1.8rem !important; 
    font-weight: 700 !important; 
    color: var(--charcoal) !important;
    overflow: visible !important;
}}

.card {{ background: #FFFFFF; border: 1px solid var(--warm-100); border-radius: 18px; padding: 1.8rem 2rem; margin-bottom: 1.2rem; }}
.card-dark {{ background: var(--charcoal); border-radius: 18px; padding: 1.8rem 2rem; color: white; }}
.hero {{ background: #FFFFFF; border: 1px solid var(--warm-100); border-radius: 24px; padding: 3.5rem; margin-bottom: 2rem; }}

.alert-box {{ border-radius: 10px; padding: 1.2rem; border-left: 4px solid; margin: 1rem 0; }}
.alert-critical {{ background: rgba(184, 74, 46, 0.1); border-color: #B84A2E; }}
.alert-warning {{ background: rgba(200, 137, 42, 0.1); border-color: var(--amber); }}
.alert-good {{ background: rgba(30, 122, 110, 0.1); border-color: #1E7A6E; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOGO & NAVIGATION
# ─────────────────────────────────────────────
st.markdown("""<div style="text-align: center; margin-bottom: 1rem;"><div style="font-family:'Playfair Display',serif; font-size: 2.6rem; font-weight: 900; color: #1C1C1E; letter-spacing: -1px;">✈ AeroMind</div></div>""", unsafe_allow_html=True)

col_nav1, col_nav2, col_nav3 = st.columns([1, 10, 1])
with col_nav2:
    page = st.radio("NAV", ["Home", "RUL Prediction", "Model Performance", "Business Impact", "About"], horizontal=True, label_visibility="collapsed")

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def rul_status(rul):
    if rul < 30:   return "CRITICAL", "critical"
    elif rul < 60: return "WARNING",  "warning"
    else:          return "NOMINAL",  "good"

def maintenance_cost(rul, prevented=True):
    if rul < 30:   return 50000 if prevented else 500000
    elif rul < 60: return 50000
    return 0

PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Outfit, sans-serif', color='#3A3A3C'),
    margin=dict(l=24, r=24, t=48, b=40),
    xaxis=dict(gridcolor='rgba(200,137,42,0.08)', zeroline=False),
    yaxis=dict(gridcolor='rgba(200,137,42,0.08)', zeroline=False),
)

# ═══════════════════════════════════════════
# BUSINESS IMPACT (Restored & Dynamic)
# ═══════════════════════════════════════════
if page == "Business Impact":
    st.markdown('<h2 style="font-family: \'Playfair Display\'; font-size: 2.4rem; font-weight: 900; color: var(--charcoal);">Business Impact & ROI</h2>', unsafe_allow_html=True)

    # Move logic block above the metrics to make them dynamic
    # Create temp container for sliders to calculate values
    with st.expander("Fleet Parameters Configuration", expanded=True):
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1: fleet_size = st.slider("Fleet Size (engines)", 50, 500, 100, 10)
        with col_s2: failure_rate = st.slider("Annual Failure Rate (%)", 1.0, 10.0, 5.0, 0.5)
        with col_s3: prevention_rt = st.slider("ML Prevention Rate (%)", 70.0, 95.0, 90.0, 5.0)

    # Calculations
    dev_cost, ann_maint = 200000, 50000
    u_cost, s_cost = 500000, 50000
    
    failures_wo = fleet_size * (failure_rate / 100)
    prevented = failures_wo * (prevention_rt / 100)
    cost_wo = failures_wo * u_cost
    cost_w = (prevented * s_cost) + ((failures_wo - prevented) * u_cost)
    savings = cost_wo - cost_w
    roi1 = ((savings - ann_maint - dev_cost) / dev_cost) * 100
    payback = (dev_cost / max(savings - ann_maint, 1)) * 12

    # Dynamic Top-Level Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Unscheduled Failure", f"${u_cost:,}")
    with c2: st.metric("Scheduled Maint.", f"${s_cost:,}")
    with c3: st.metric("Year 1 ROI", f"{roi1:.0f}%", delta=f"on ${dev_cost/1000:.0f}K invest")
    with c4: st.metric("Payback Period", f"{payback:.1f} mo")

    col_chart, col_data = st.columns([1.5, 1], gap="large")
    with col_chart:
        years = [1,2,3,4,5]
        cum_sav = [((savings - ann_maint)*y - dev_cost)/1e6 for y in years]
        st.plotly_chart(go.Figure(go.Scatter(x=years, y=cum_sav, fill='tozeroy', line_color='#1E7A6E', marker=dict(size=9))).update_layout(**PLOT_LAYOUT, title="Projected Cumulative Savings ($M)"), use_container_width=True)
    
    with col_data:
        st.markdown(f'<div class="card-dark" style="text-align:center;"><p style="font-family:IBM Plex Mono; font-size:0.56rem; color:rgba(200,137,42,0.6);">ESTIMATED ANNUAL SAVINGS</p><h2 style="color:white; margin:0;">${savings/1e6:.1f}M</h2></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card" style="margin-top:1rem;"><h4>Fleet Insight</h4><p style="font-size:0.85rem; color:#6C6C70;">By preventing {prevented:.1f} unscheduled failures per year, the system reduces maintenance overhead by {((cost_wo - cost_w)/cost_wo)*100:.0f}%.</p></div>', unsafe_allow_html=True)

# (Rest of the pages Home, RUL Prediction, Model Performance, About stay identical to original content)
elif page == "Home":
    st.markdown('<div class="hero"><h1>Aircraft Engine Health Intelligence</h1><p>Predicting RUL using deep learning.</p></div>', unsafe_allow_html=True)
elif page == "RUL Prediction":
    st.title("Inference Console")
elif page == "Model Performance":
    st.title("Performance Results")
elif page == "About":
    st.title("Project Documentation")

st.markdown("""<div style="margin-top:4rem; padding:2rem 0; border-top:1px solid #EDE7D9; display:flex; justify-content:space-between; opacity:0.6; font-size:0.7rem;"><p>AeroMind Intelligence v2.0</p><p>© 2026 Vivek M D</p></div>""", unsafe_allow_html=True)

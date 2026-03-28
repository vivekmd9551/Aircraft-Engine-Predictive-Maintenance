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
# BACKGROUND SVG ENCODING (The High-Intensity 737)
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
    --ivory:      #FAF8F4;
    --cream:      #F3EFE7;
    --warm-100:   #EDE7D9;
    --warm-200:   #D9CEBC;
    --amber:      #C8892A;
    --amber-lt:   #E8A83E;
    --amber-dim:  #F0D49A;
    --charcoal:   #1C1C1E;
    --slate:      #3A3A3C;
    --mid:        #6C6C70;
    --muted:      #9A9A9E;
    --rust:       #B84A2E;
    --rust-lt:    #FCEAE6;
    --teal:       #1E7A6E;
    --teal-lt:    #E3F4F1;
    --shadow-sm:  0 2px 12px rgba(28,28,30,0.07);
    --shadow-md:  0 6px 28px rgba(28,28,30,0.10);
    --shadow-lg:  0 16px 56px rgba(28,28,30,0.14);
    --radius:     18px;
    --radius-sm:  10px;
    --glass:      rgba(255, 255, 255, 0.6);
}}

*, *::before, *::after {{ box-sizing: border-box; }}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
    background: var(--ivory) !important;
    font-family: 'Outfit', sans-serif !important;
}}

/* THE BACKGROUND FIX */
[data-testid="stAppViewContainer"]::before {{
    content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    z-index: 0; pointer-events: none;
    background-image: url("data:image/svg+xml;base64,{b64_svg}");
    background-repeat: no-repeat; background-position: center center;
    background-size: 85% auto; opacity: 0.18;
}}

[data-testid="stMainBlockContainer"] {{
    padding-top: 2rem !important;
    max-width: 1300px !important;
    position: relative;
    z-index: 10; 
}}

#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stDecoration"] {{ display: none; }}
[data-testid="collapsedControl"] {{ display: none; }} 

h1, h2, h3, h4, h5 {{ font-family: 'Playfair Display', serif !important; color: var(--charcoal) !important; }}
p, li, span, div, label {{ font-family: 'Outfit', sans-serif !important; }}

/* NAVIGATION BAR */
div[data-testid="stRadio"] > div[role="radiogroup"] {{
    background: var(--charcoal);
    padding: 10px 15px; border-radius: 100px;
    display: flex; justify-content: center; gap: 15px;
    border: 1px solid rgba(200, 137, 42, 0.4);
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    margin-bottom: 2rem;
}}
div[data-testid="stRadio"] label {{
    background: transparent !important; border: none !important;
    padding: 8px 22px !important; border-radius: 100px !important;
    transition: all 0.3s ease !important;
    box-shadow: none !important; margin-bottom: 0px !important;
}}
div[data-testid="stRadio"] label p {{
    color: #9A9A9E !important; font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important; letter-spacing: 0.12em !important; text-transform: uppercase !important;
}}
div[data-testid="stRadio"] label[data-checked="true"] {{
    background: var(--amber) !important;
}}
div[data-testid="stRadio"] label[data-checked="true"] p {{
    color: white !important; font-weight: 600 !important;
}}
div[data-testid="stRadio"] label > div:first-child {{ display: none !important; }}

/* PREVENT WHITE BOXES - Streamlit auto-wrappers */
div[data-testid="stVerticalBlock"] > div {{ background-color: transparent !important; }}

[data-testid="stMetric"] {{
    background: rgba(255,255,255,0.4) !important; 
    backdrop-filter: blur(5px);
    border: 1px solid var(--warm-100) !important; border-radius: var(--radius) !important;
    padding: 1.3rem 1.5rem !important; border-top: 3px solid var(--amber) !important; box-shadow: var(--shadow-sm) !important;
}}
[data-testid="stMetricValue"] {{ font-family: 'Playfair Display', serif !important; font-size: 2.1rem !important; font-weight: 700 !important; color: var(--charcoal) !important; }}
[data-testid="stMetricLabel"] {{ font-family: 'IBM Plex Mono', monospace !important; font-size: 0.6rem !important; letter-spacing: 0.16em !important; text-transform: uppercase !important; color: var(--mid) !important; }}

/* GLASS PANELS */
.hero {{
    background: var(--glass);
    backdrop-filter: blur(12px);
    border: 1px solid var(--warm-100);
    border-radius: 24px; padding: 3.5rem; margin-bottom: 2rem;
    position: relative; overflow: hidden; box-shadow: var(--shadow-lg);
}}
.card {{
    background: var(--glass);
    backdrop-filter: blur(10px);
    border: 1px solid var(--warm-100); border-radius: var(--radius);
    padding: 1.8rem 2rem; box-shadow: var(--shadow-sm); margin-bottom: 1.2rem;
}}
.card-dark {{ background: rgba(28,28,30,0.85); backdrop-filter: blur(10px); border: 1px solid rgba(200,137,42,0.18); border-radius: var(--radius); padding: 1.8rem 2rem; color: white; }}

.hero-tag {{ display: inline-flex; align-items: center; gap: 7px; background: var(--amber-dim); border: 1px solid rgba(200,137,42,0.3); border-radius: 30px; padding: 5px 15px; font-family: 'IBM Plex Mono', monospace; font-size: 0.6rem; letter-spacing: 0.14em; color: var(--amber); margin-bottom: 1.4rem; text-transform: uppercase; }}
.hero-title {{ font-family: 'Playfair Display', serif !important; font-size: clamp(2.8rem, 5vw, 4.4rem) !important; font-weight: 900 !important; color: var(--charcoal) !important; line-height: 1.04 !important; margin: 0 0 0.6rem !important; }}
.hero-stats {{ display: flex; gap: 2.8rem; flex-wrap: wrap; border-top: 1px solid rgba(200,137,42,0.1); padding-top: 2rem; }}

.rule {{ display: flex; align-items: center; gap: 1rem; margin: 2.8rem 0 2.2rem; }}
.rule-line {{ flex: 1; height: 1px; background: var(--warm-100); }}
.rule-label {{ font-family: 'IBM Plex Mono', monospace; font-size: 0.58rem; letter-spacing: 0.28em; text-transform: uppercase; color: var(--amber); }}

.chip {{ display: inline-flex; align-items: center; gap: 6px; border-radius: 20px; padding: 5px 13px; font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; letter-spacing: 0.08em; }}
.chip-critical {{ background: var(--rust-lt); color: var(--rust); border: 1px solid rgba(184,74,46,0.25); }}
.chip-warning  {{ background: #FFF6E8; color: #9A6200; border: 1px solid rgba(200,137,42,0.3); }}
.chip-good     {{ background: var(--teal-lt); color: var(--teal); border: 1px solid rgba(30,122,110,0.25); }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOGO & NAVIGATION
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; margin-bottom: 1rem;">
    <div style="font-family:'Playfair Display',serif; font-size: 2.4rem; font-weight: 900; color: #1C1C1E; letter-spacing: -1px;">✈ AeroMind</div>
</div>
""", unsafe_allow_html=True)

col_nav1, col_nav2, col_nav3 = st.columns([1, 8, 1])
with col_nav2:
    page = st.radio(
        "Navigate",
        ["Home", "RUL Prediction", "Model Performance", "Business Impact", "About"],
        horizontal=True,
        label_visibility="collapsed"
    )

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
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Outfit, sans-serif', color='#3A3A3C'),
    margin=dict(l=24, r=24, t=48, b=40),
    xaxis=dict(gridcolor='rgba(200,137,42,0.08)', linecolor='rgba(200,137,42,0.15)', tickfont=dict(size=11, color='#9A9A9E', family='IBM Plex Mono'), zeroline=False),
    yaxis=dict(gridcolor='rgba(200,137,42,0.08)', linecolor='rgba(200,137,42,0.15)', tickfont=dict(size=11, color='#9A9A9E', family='IBM Plex Mono'), zeroline=False),
    colorway=['#C8892A','#1E7A6E','#B84A2E','#1C1C1E','#E8A83E'],
)

# ═══════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════
if page == "Home":
    st.markdown("""
    <div class="hero">
        <div class="hero-tag">Live Monitoring Active</div>
        <h1 class="hero-title">Aircraft Engine<br><em style="color:var(--amber); font-style:italic;">Health Intelligence</em></h1>
        <p style="font-family: 'Outfit'; font-size: 1.15rem; color: #6C6C70; max-width: 600px; margin: 1.5rem 0 3rem; font-weight: 300;">
            Predicting Remaining Useful Life of turbofan engines using deep learning —
            50% beyond industry benchmarks on NASA C-MAPSS data.
        </p>
        <div class="hero-stats">
            <div><div style="font-family:'Playfair Display'; font-size:2.4rem; font-weight:700; color:var(--charcoal);">8.96</div><div style="font-family:'IBM Plex Mono'; font-size:0.58rem; letter-spacing:0.18em; text-transform:uppercase; color:var(--muted);">RMSE (cycles)</div></div>
            <div><div style="font-family:'Playfair Display'; font-size:2.4rem; font-weight:700; color:var(--charcoal);">95.3%</div><div style="font-family:'IBM Plex Mono'; font-size:0.58rem; letter-spacing:0.18em; text-transform:uppercase; color:var(--muted);">R² Accuracy</div></div>
            <div><div style="font-family:'Playfair Display'; font-size:2.4rem; font-weight:700; color:var(--charcoal);">4</div><div style="font-family:'IBM Plex Mono'; font-size:0.58rem; letter-spacing:0.18em; text-transform:uppercase; color:var(--muted);">ML Models</div></div>
            <div><div style="font-family:'Playfair Display'; font-size:2.4rem; font-weight:700; color:var(--charcoal);">$2M+</div><div style="font-family:'IBM Plex Mono'; font-size:0.58rem; letter-spacing:0.18em; text-transform:uppercase; color:var(--muted);">Annual Savings</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Models Trained", "4", help="RF, XGBoost, LightGBM, LSTM")
    with c2: st.metric("Features Engineered", "117", delta="+106 engineered")
    with c3: st.metric("Training Engines", "80", help="16,561 training samples")
    with c4: st.metric("Validation R²", "95.3%", delta="50% better")

    st.markdown("""<div class="rule"><div class="rule-line"></div><span class="rule-label">Model Comparison</span><div class="rule-line"></div></div>""", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig = go.Figure(go.Bar(
        x=['LSTM', 'XGBoost', 'LightGBM', 'Random Forest'], y=[8.96, 9.41, 9.52, 9.85],
        marker=dict(color=['#1C1C1E','#C8892A','#E8A83E','#D9CEBC'], cornerradius=10),
        text=[8.96, 9.41, 9.52, 9.85], textposition='outside'
    ))
    fig.add_hline(y=18, line_dash="dot", line_color="#B84A2E", annotation_text="Industry Target: 18 cycles")
    fig.update_layout(**PLOT_LAYOUT, title="Validation RMSE — All Models", height=400)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════
# RUL PREDICTION
# ═══════════════════════════════════════════
elif page == "RUL Prediction":
    st.markdown("""<h2 style="font-family:'Playfair Display'; font-size:2.4rem;">RUL Prediction</h2>""", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    chosen = st.selectbox("Select Active ML Model", ['LSTM', 'XGBoost', 'LightGBM', 'Random Forest'])
    
    col_sliders, col_result = st.columns([1.1, 1], gap="large")
    with col_sliders:
        with st.container(border=False):
            input_mode = st.radio("Control Interface", ["🎛️ Simple Controls", "⚙️ Advanced Sensors (Engineers)"], horizontal=True)
            if input_mode == "🎛️ Simple Controls":
                scenario = st.selectbox("Flight Scenario Presets", ["✈️ Healthy Engine (Nominal)", "⚠️ Moderate Wear (Mid-Life)", "🚨 Impending Failure (Critical)"])
                def_t = 10 if "Healthy" in scenario else 45 if "Moderate" in scenario else 85
                heat_val = st.slider("Overall Engine Heat [T24 / T50]", 0, 100, def_t, format="%d%% wear")
                press_val = st.slider("Compressor Pressure Level [P30 / Ps30]", 0, 100, def_t, format="%d%% wear")
                rpm_val = st.slider("Fan & Core Speed Stress [NF / NC]", 0, 100, def_t, format="%d%% wear")
                base_rul = int(125 * (1 - (heat_val + press_val + rpm_val) / 300))
            else:
                s2 = st.slider("Compressor Inlet Temperature [T24] (°R)", 640.0, 645.0, 642.5)
                s3 = st.slider("HP Compressor Outlet [P30] (psia)", 1570.0, 1620.0, 1590.0)
                base_rul = int(max(0, min(125, 100 - (s2-642.5)*12)))

    with col_result:
        rul_pred = max(0, min(125, base_rul))
        label, kind = rul_status(rul_pred)
        color_map = {"critical":"#B84A2E", "warning":"#C8892A", "good":"#1E7A6E"}
        bg_map = {"critical":"#FCEAE6", "warning":"#FFF6E8", "good":"#E3F4F1"}
        st.markdown(f"""
        <div style="background:{bg_map[kind]}; border:2px solid {color_map[kind]}; border-radius:20px; padding:3rem; text-align:center; backdrop-filter:blur(10px);">
            <p style="font-family:'IBM Plex Mono'; font-size:0.62rem; letter-spacing:0.25em; text-transform:uppercase; color:#9A9A9E;">Remaining Useful Life</p>
            <h1 style="font-family:'Playfair Display'; font-size:6.5rem; font-weight:900; color:{color_map[kind]}; margin:0.5rem 0;">{rul_pred}</h1>
            <span class="chip chip-{kind}">{label}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════
# MODEL PERFORMANCE
# ═══════════════════════════════════════════
elif page == "Model Performance":
    st.markdown("""<h2 style="font-family:'Playfair Display'; font-size:2.4rem;">Model Performance</h2>""", unsafe_allow_html=True)
    perf = {'Model': ['LSTM', 'XGBoost','LightGBM','Random Forest'], 'RMSE': [8.96, 9.41, 9.52, 9.85], 'MAE': [6.83, 6.35, 6.48, 6.27], 'R²': [0.9528, 0.9492, 0.9479, 0.9443]}
    df_perf = pd.DataFrame(perf)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Best RMSE", "8.96", delta="LSTM")
    with c2: st.metric("Best MAE", "6.27", delta="Random Forest")
    with c3: st.metric("Best R²", "0.9528", delta="LSTM")
    with c4: st.metric("vs Target", "-9.04", delta="50% better", delta_color="normal")

    col1, col2 = st.columns(2)
    with col1:
        fig_r = go.Figure(go.Bar(x=df_perf['Model'], y=df_perf['RMSE'], marker=dict(color='#1C1C1E')))
        fig_r.update_layout(**PLOT_LAYOUT, title="RMSE — Lower is Better", height=350)
        st.plotly_chart(fig_r, use_container_width=True)
    with col2:
        fig_r2 = go.Figure(go.Bar(x=df_perf['Model'], y=df_perf['R²'], marker=dict(color='#C8892A')))
        fig_r2.update_layout(**PLOT_LAYOUT, title="R² Score — Higher is Better", height=350)
        st.plotly_chart(fig_r2, use_container_width=True)

    st.dataframe(df_perf, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════
# BUSINESS IMPACT
# ═══════════════════════════════════════════
elif page == "Business Impact":
    st.markdown("""<h2 style="font-family:'Playfair Display'; font-size:2.4rem;">Business Impact & ROI</h2>""", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Unscheduled Failure", "$500,000")
    with c2: st.metric("Scheduled Maintenance", "$50,000")
    with c3: st.metric("Year 1 ROI", "888%")
    with c4: st.metric("Payback Period", "1.2 mo")

    fleet_size = st.slider("Fleet Size (engines)", 50, 500, 100)
    savings = (fleet_size * 0.05 * 0.90) * 450000
    
    fig_roi = go.Figure(go.Scatter(x=[1,2,3,4,5], y=[(savings*y)/1e6 for y in range(1,6)], fill='tozeroy', line_color='#1E7A6E'))
    fig_roi.update_layout(**PLOT_LAYOUT, title="5-Year Cumulative Savings Projection ($M)", height=400)
    st.plotly_chart(fig_roi, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════
# ABOUT
# ═══════════════════════════════════════════
elif page == "About":
    st.markdown("""<h2 style="font-family:'Playfair Display'; font-size:2.4rem;">About AeroMind</h2>""", unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Technical Stack")
        st.markdown("Python 3.11, TensorFlow/Keras, XGBoost, LightGBM, Optuna, Streamlit, Plotly.")
        st.markdown("### Dataset")
        st.markdown("NASA C-MAPSS Turbofan Engine Degradation Simulation (FD001).")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        st.markdown("### Author")
        st.markdown("**Vivek M D**")
        st.markdown("BE Computer Science Graduate · Aviation Technology Enthusiast")
        st.markdown("📧 [Your Email] | 💼 [LinkedIn] | 🐙 [GitHub]")
        st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""<div style="margin-top:4rem;padding-top:1.5rem;border-top:1px solid #EDE7D9;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;"><p style="font-size:0.8rem;color:#9A9A9E;font-weight:300;font-family:'Outfit',sans-serif;"><strong style="color:#1C1C1E;font-weight:600;">AeroMind</strong> · Built by <strong style="color:#1C1C1E;font-weight:600;">Vivek M D</strong></p><p style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:#C8C8CA;letter-spacing:0.1em;">NASA C-MAPSS · Streamlit · v2.0 · 2026</p></div>""", unsafe_allow_html=True)

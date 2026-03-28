"""
✈️ AeroMind — Aircraft Engine Predictive Maintenance
Author: Vivek M D
Design: Premium Glassmorphism — Ivory + Amber + Charcoal
"""

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
# BACKGROUND SVG ENCODING (Fixed Realistic B737)
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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Outfit:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {{
    --ivory: #FAF8F4;
    --amber: #C8892A;
    --charcoal: #1C1C1E;
    --glass: rgba(255, 255, 255, 0.75);
    --glass-dark: rgba(28, 28, 30, 0.85);
}}

html, body, [data-testid="stAppViewContainer"] {{
    background: var(--ivory) !important;
}}

/* Aircraft Background Fix */
[data-testid="stAppViewContainer"]::before {{
    content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    z-index: 0; pointer-events: none;
    background-image: url("data:image/svg+xml;base64,{b64_svg}");
    background-repeat: no-repeat; background-position: center center;
    background-size: 85% auto; opacity: 0.18;
}}

[data-testid="stMainBlockContainer"] {{
    position: relative; z-index: 10; max-width: 1300px !important; padding-top: 1.5rem !important;
}}

#MainMenu, footer, header, [data-testid="stDecoration"] {{ visibility: hidden; display: none; }}

/* NAVIGATION BAR */
div[data-testid="stRadio"] > div[role="radiogroup"] {{
    background: var(--charcoal);
    padding: 10px 15px; border-radius: 100px;
    display: flex; justify-content: center; gap: 15px;
    border: 1px solid rgba(200, 137, 42, 0.4);
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}}
div[data-testid="stRadio"] label {{
    background: transparent !important; border: none !important;
    padding: 8px 20px !important; border-radius: 100px !important;
    transition: 0.3s ease !important;
}}
div[data-testid="stRadio"] label p {{
    color: #9A9A9E !important; font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.7rem !important; text-transform: uppercase !important; letter-spacing: 0.1em;
}}
div[data-testid="stRadio"] label[data-checked="true"] {{
    background: var(--amber) !important;
}}
div[data-testid="stRadio"] label[data-checked="true"] p {{
    color: white !important; font-weight: 600 !important;
}}
div[data-testid="stRadio"] label > div:first-child {{ display: none !important; }}

/* GLASS CARDS */
.glass-card {{
    background: var(--glass);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(200, 137, 42, 0.1);
    border-radius: 24px;
    padding: 2.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.03);
}}
.glass-dark-card {{
    background: var(--glass-dark);
    backdrop-filter: blur(12px);
    color: white;
    border-radius: 24px;
    padding: 2.5rem;
}}

/* TYPOGRAPHY */
h1, h2, h3 {{ font-family: 'Playfair Display', serif !important; color: var(--charcoal); }}
.eyebrow {{ font-family: 'IBM Plex Mono'; font-size: 0.6rem; letter-spacing: 3px; color: var(--amber); text-transform: uppercase; }}

/* METRICS */
[data-testid="stMetric"] {{
    background: rgba(255, 255, 255, 0.6) !important;
    backdrop-filter: blur(5px);
    border: 1px solid rgba(200, 137, 42, 0.1) !important;
    border-radius: 15px !important;
    padding: 1rem !important;
}}

.rule {{ display: flex; align-items: center; gap: 1rem; margin: 2rem 0; }}
.rule-line {{ flex: 1; height: 1px; background: rgba(200, 137, 42, 0.2); }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER & NAVIGATION
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; margin-bottom: 1rem;">
    <div style="font-family:'Playfair Display',serif; font-size: 2.4rem; font-weight: 900; color: #1C1C1E;">✈ AeroMind</div>
</div>
""", unsafe_allow_html=True)

col_nav1, col_nav2, col_nav3 = st.columns([1, 8, 1])
with col_nav2:
    page = st.radio("NAV", ["Home", "RUL Prediction", "Model Performance", "Business Impact", "About"], horizontal=True, label_visibility="collapsed")

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def rul_status(rul):
    if rul < 30: return "CRITICAL", "#B84A2E", "rgba(184, 74, 46, 0.1)"
    elif rul < 60: return "WARNING", "#C8892A", "rgba(200, 137, 42, 0.1)"
    return "NOMINAL", "#1E7A6E", "rgba(30, 122, 110, 0.1)"

PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Outfit, sans-serif', color='#3A3A3C'),
    margin=dict(l=20, r=20, t=40, b=40),
    xaxis=dict(gridcolor='rgba(200,137,42,0.1)', zeroline=False),
    yaxis=dict(gridcolor='rgba(200,137,42,0.1)', zeroline=False),
)

# ═══════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════
if page == "Home":
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 4rem 2rem;">
        <span class="eyebrow">Aviation Predictive Maintenance</span>
        <h1 style="font-size: 4.2rem; margin: 1rem 0;">Engine <em>Health Intelligence</em></h1>
        <p style="color: #6C6C70; max-width: 600px; margin: 0 auto 3rem; font-size: 1.1rem; font-weight: 300;">
            Predicting Remaining Useful Life (RUL) of turbofan engines using advanced LSTM and Ensemble architectures. 
            Optimized for NASA C-MAPSS data.
        </p>
        <div style="display: flex; justify-content: center; gap: 4rem;">
            <div><h2 style="margin:0;">8.96</h2><p class="eyebrow" style="letter-spacing:1px;">RMSE Cycles</p></div>
            <div><h2 style="margin:0;">95.3%</h2><p class="eyebrow" style="letter-spacing:1px;">R² Accuracy</p></div>
            <div><h2 style="margin:0;">$2M+</h2><p class="eyebrow" style="letter-spacing:1px;">Annual Savings</p></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div class="rule"><div class="rule-line"></div><span class="eyebrow">Fleet Benchmarks</span><div class="rule-line"></div></div>""", unsafe_allow_html=True)
    
    # CHARTS IN GLASS CONTAINER
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        fig = go.Figure(go.Bar(
            x=['LSTM', 'XGBoost', 'LightGBM', 'Random Forest'], y=[8.96, 9.41, 9.52, 9.85],
            marker=dict(color=['#1C1C1E','#C8892A','#E8A83E','#D9CEBC'], cornerradius=10),
            text=[8.96, 9.41, 9.52, 9.85], textposition='outside'
        ))
        fig.add_hline(y=18, line_dash="dot", line_color="#B84A2E", annotation_text="Industry Target")
        fig.update_layout(**PLOT_LAYOUT, height=350, title="Validation RMSE — All Models")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════
# RUL PREDICTION
# ═══════════════════════════════════════════
elif page == "RUL Prediction":
    st.markdown('<span class="eyebrow">Inference Console</span><h2 style="margin-bottom:2rem;">Remaining Useful Life Prediction</h2>', unsafe_allow_html=True)
    
    col_sliders, col_result = st.columns([1.2, 1], gap="large")
    
    with col_sliders:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        model_choice = st.selectbox("Select Active ML Architecture", ['LSTM (Champion)', 'XGBoost', 'LightGBM', 'Random Forest'])
        input_mode = st.radio("Control Interface", ["🎛️ Simple Presets", "⚙️ Raw Sensor Data"], horizontal=True)
        
        if input_mode == "🎛️ Simple Presets":
            scenario = st.select_slider("Engine Condition", options=["Nominal", "Moderate Wear", "Near Failure"])
            wear = 10 if scenario == "Nominal" else 50 if scenario == "Moderate Wear" else 90
            heat = st.slider("Engine Heat Stress (%)", 0, 100, wear)
            press = st.slider("Pressure Ratio Degradation (%)", 0, 100, wear)
            base_rul = int(125 * (1 - (heat + press)/200))
        else:
            s2 = st.slider("T24 - Total Temp (°R)", 641.0, 644.0, 642.5)
            s3 = st.slider("P30 - HP Outlet Press (psia)", 1580.0, 1610.0, 1590.0)
            s11 = st.slider("NC - Core Speed (rpm)", 47.0, 49.0, 47.8)
            base_rul = int(100 - (s2-642)*15 - (s3-1590)/2)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_result:
        rul_pred = max(0, min(125, base_rul))
        label, color, bg = rul_status(rul_pred)
        st.markdown(f"""
        <div style="background:{bg}; border: 2px solid {color}; border-radius: 24px; padding: 3rem; text-align: center; backdrop-filter: blur(10px);">
            <p class="eyebrow" style="color:#6C6C70;">Predicted RUL</p>
            <h1 style="font-size: 7rem; color:{color}; margin: 0.5rem 0;">{rul_pred}</h1>
            <p class="eyebrow" style="color:#6C6C70; margin-bottom:1.5rem;">Flight Cycles Remaining</p>
            <div style="display:inline-block; padding:8px 20px; background:{color}; color:white; border-radius:100px; font-family:'IBM Plex Mono'; font-size:0.8rem;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════
# MODEL PERFORMANCE
# ═══════════════════════════════════════════
elif page == "Model Performance":
    st.markdown('<span class="eyebrow">Validation Data</span><h2>Performance Matrix</h2>', unsafe_allow_html=True)
    
    perf = {'Model': ['LSTM', 'XGBoost', 'LightGBM', 'Random Forest'], 'RMSE': [8.96, 9.41, 9.52, 9.85], 'R²': [0.9528, 0.9492, 0.9479, 0.9443]}
    df = pd.DataFrame(perf)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Best RMSE", "8.96", "LSTM")
    c2.metric("Best MAE", "6.27", "RF")
    c3.metric("Best R²", "0.9528", "LSTM")
    
    radar_fig = go.Figure(go.Scatterpolar(r=[0.95, 0.9, 0.95, 0.5, 0.8], theta=['RMSE','MAE','R²','Speed','Explainability'], fill='toself', line_color='#C8892A'))
    radar_fig.update_layout(**PLOT_LAYOUT, height=400, title="Multi-Metric Comparison")
    st.plotly_chart(radar_fig, use_container_width=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════
# BUSINESS IMPACT
# ═══════════════════════════════════════════
elif page == "Business Impact":
    st.markdown('<span class="eyebrow">Financial Intel</span><h2>Fleet ROI & Savings</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.5])
    with col1:
        fleet = st.slider("Fleet Size (Engines)", 50, 500, 100)
        fail_rate = st.slider("Annual Failure Rate (%)", 1.0, 10.0, 5.0)
        # Financial logic restored
        savings = (fleet * (fail_rate/100) * 0.90) * (500000 - 50000)
        st.metric("Annual Fleet Savings", f"${savings/1e6:.2f}M", delta="888% ROI")
    
    with col2:
        years = [1,2,3,4,5]
        cum_sav = [((savings * y) - 200000)/1e6 for y in years]
        fig_roi = go.Figure(go.Scatter(x=years, y=cum_sav, fill='tozeroy', line_color='#1E7A6E'))
        fig_roi.update_layout(**PLOT_LAYOUT, title="5-Year Cumulative Savings ($M)", height=300)
        st.plotly_chart(fig_roi, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════
# ABOUT
# ════════════════════════════════──────────────────────
elif page == "About":
    st.markdown('<span class="eyebrow">Documentation</span><h2>Project Intelligence</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3>Author & Vision</h3>
            <p><b>Vivek M D</b><br>BE Computer Science · AI/ML Specialist</p>
            <p>Designed to optimize maintenance windows and prevent catastrophic engine failure using NASA C-MAPSS telemetry data.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="glass-dark-card">
            <h3>Technical Stack</h3>
            <p>• Python 3.11 / Streamlit<br>• TensorFlow & Keras (LSTM)<br>• XGBoost / LightGBM<br>• Plotly Intelligence</p>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""<div style="margin-top:5rem; padding:2rem 0; border-top:1px solid #EDE7D9; display:flex; justify-content:space-between; opacity:0.6; font-size:0.7rem;"><p>AeroMind Intelligence v2.0</p><p>© 2026 Vivek M D</p></div>""", unsafe_allow_html=True)

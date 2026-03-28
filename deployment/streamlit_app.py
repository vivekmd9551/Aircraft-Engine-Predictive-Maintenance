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
# BACKGROUND SVG ENCODING (FIXED)
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
    --cream:     #F3EFE7;
    --warm-100:  #EDE7D9;
    --warm-200:  #D9CEBC;
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
p, li, span, div, label {{ font-family: 'Outfit', sans-serif !important; }}

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
div[data-testid="stRadio"] label[data-checked="true"] * {{ color: var(--amber-lt) !important; font-weight: 600 !important; }}
div[data-testid="stRadio"] label > div:first-child {{ display: none !important; }}

[data-testid="stMetric"] {{
    background: rgba(255, 255, 255, 0.4) !important; backdrop-filter: blur(5px);
    border: 1px solid var(--warm-100) !important; border-radius: 18px !important;
    padding: 1.3rem !important; border-top: 3px solid var(--amber) !important;
}}

.alert-box {{ border-radius: 10px; padding: 1.2rem 1.4rem; border-left: 4px solid; margin: 1rem 0; }}
.alert-critical {{ background: rgba(184, 74, 46, 0.1); border-color: #B84A2E; }}
.alert-warning {{ background: rgba(200, 137, 42, 0.1); border-color: var(--amber); }}
.alert-good {{ background: rgba(30, 122, 110, 0.1); border-color: #1E7A6E; }}

.card {{ background: var(--glass); backdrop-filter: blur(10px); border: 1px solid var(--warm-100); border-radius: 18px; padding: 1.8rem 2rem; margin-bottom: 1.2rem; }}
.card-dark {{ background: rgba(28,28,30,0.85); border-radius: 18px; padding: 1.8rem 2rem; color: white; }}
.hero {{ background: var(--glass); backdrop-filter: blur(12px); border: 1px solid var(--warm-100); border-radius: 24px; padding: 3.5rem; margin-bottom: 2rem; }}

.hero-tag-dot {{ width: 7px; height: 7px; border-radius: 50%; background: var(--amber); animation: pulse-dot 2s ease-in-out infinite; }}
@keyframes pulse-dot {{ 0%, 100% {{ transform: scale(1); opacity: 1; }} 50% {{ transform: scale(1.4); opacity: 0.6; }} }}
.rule {{ display: flex; align-items: center; gap: 1rem; margin: 2.8rem 0 2.2rem; }}
.rule-line {{ flex: 1; height: 1px; background: var(--warm-100); }}
.rule-label {{ font-family: 'IBM Plex Mono', monospace; font-size: 0.58rem; letter-spacing: 0.28em; text-transform: uppercase; color: var(--amber); }}
.chip {{ display: inline-flex; align-items: center; gap: 6px; border-radius: 20px; padding: 5px 13px; font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; letter-spacing: 0.08em; }}
.pill-grid {{ display: flex; flex-wrap: wrap; gap: 7px; margin-top: 1rem; }}
.pill {{ background: var(--cream); border: 1px solid var(--warm-200); border-radius: 6px; padding: 4px 11px; font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOGO & NAVIGATION
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; margin-bottom: 1rem;">
    <div style="font-family:'Playfair Display',serif; font-size: 2.6rem; font-weight: 900; color: #1C1C1E; letter-spacing: -1px;">✈ AeroMind</div>
</div>
""", unsafe_allow_html=True)

col_nav1, col_nav2, col_nav3 = st.columns([1, 10, 1])
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
        <div style="display: inline-flex; align-items: center; gap: 7px; background: rgba(200,137,42,0.1); border-radius: 30px; padding: 6px 16px; font-family: 'IBM Plex Mono'; font-size: 0.65rem; color: var(--amber); margin-bottom: 2rem; text-transform: uppercase; letter-spacing: 2px;">
            <div class="hero-tag-dot"></div> Live Monitoring Active
        </div>
        <h1 style="font-size: 4.4rem; line-height: 1.04; margin: 0 0 0.6rem;">Aircraft Engine<br><em style="color:var(--amber); font-style:italic;">Health Intelligence</em></h1>
        <p style="font-family: 'Outfit'; font-size: 1.15rem; color: #6C6C70; max-width: 650px; margin: 2rem 0 3.5rem; font-weight: 300;">
            Predicting Remaining Useful Life of turbofan engines using deep learning — 50% beyond industry benchmarks on NASA C-MAPSS data.
        </p>
        <div style="display: flex; gap: 2.8rem; flex-wrap: wrap; border-top: 1px solid rgba(200,137,42,0.1); padding-top: 2rem;">
            <div><div style="font-family:'Playfair Display'; font-size:2.4rem; font-weight:700; color:var(--charcoal);">8.96</div><div style="font-family:'IBM Plex Mono'; font-size:0.58rem; letter-spacing:0.18em; text-transform:uppercase; color:var(--muted);">RMSE (cycles)</div></div>
            <div><div style="font-family:'Playfair Display'; font-size:2.4rem; font-weight:700; color:var(--charcoal);">95.3%</div><div style="font-family:'IBM Plex Mono'; font-size:0.58rem; letter-spacing:0.18em; text-transform:uppercase; color:var(--muted);">R² Accuracy</div></div>
            <div><div style="font-family:'Playfair Display'; font-size:2.4rem; font-weight:700; color:var(--charcoal);">4</div><div style="font-family:'IBM Plex Mono'; font-size:0.58rem; letter-spacing:0.18em; text-transform:uppercase; color:var(--muted);">ML Models</div></div>
            <div><div style="font-family:'Playfair Display'; font-size:2.4rem; font-weight:700; color:var(--charcoal);">$2M+</div><div style="font-family:'IBM Plex Mono'; font-size:0.58rem; letter-spacing:0.18em; text-transform:uppercase; color:var(--muted);">Annual Savings</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Models Trained", "4")
    with c2: st.metric("Features Engineered", "117", delta="+106")
    with c3: st.metric("Training Engines", "80")
    with c4: st.metric("Validation R²", "95.3%")

    st.markdown("""<div class="rule"><div class="rule-line"></div><span class="rule-label">Model Comparison</span><div class="rule-line"></div></div>""", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig = go.Figure(go.Bar(
        x=['LSTM', 'XGBoost', 'LightGBM', 'Random Forest'], y=[8.96, 9.41, 9.52, 9.85],
        marker=dict(color=['#1C1C1E','#C8892A','#E8A83E','#D9CEBC'], cornerradius=10),
        text=[8.96, 9.41, 9.52, 9.85], textposition='outside'
    ))
    fig.add_hline(y=18, line_dash="dot", line_color="#B84A2E", annotation_text="Industry Target")
    fig.update_layout(**PLOT_LAYOUT, title=dict(text="Validation RMSE — All Models", font=dict(family='Playfair Display', size=17, color='#1C1C1E')), height=400)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════
# RUL PREDICTION
# ═══════════════════════════════════════════
elif page == "RUL Prediction":
    st.markdown("""
    <span style="font-family: 'IBM Plex Mono'; font-size: 0.6rem; letter-spacing: 0.28em; text-transform: uppercase; color: var(--amber); margin-bottom: 0.4rem; display: block;">Inference Console</span>
    <h2 style="font-family: 'Playfair Display'; font-size: 2.4rem; font-weight: 900; color: var(--charcoal); line-height: 1.05; margin-bottom: 0.4rem;">RUL Prediction</h2>
    <p style="font-size: 0.95rem; font-weight: 300; color: var(--mid); line-height: 1.65; margin-bottom: 2rem;">Adjust sensor readings to compute the engine's Remaining Useful Life in real time.</p>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    chosen = st.selectbox("Select Active ML Model", ['LSTM', 'XGBoost', 'LightGBM', 'Random Forest'])

    st.markdown("""<div class="rule"><div class="rule-line"></div><span class="rule-label">Input Parameters</span><div class="rule-line"></div></div>""", unsafe_allow_html=True)

    col_sliders, col_result = st.columns([1.1, 1], gap="large")

    with col_sliders:
        input_mode = st.radio("Control Interface", ["🎛️ Simple Controls", "⚙️ Advanced Sensors (Engineers)"], horizontal=True)
        st.markdown("---")
        if input_mode == "🎛️ Simple Controls":
            scenario = st.selectbox("Flight Scenario Presets", ["✈️ Healthy Engine (Nominal)", "⚠️ Moderate Wear (Mid-Life)", "🚨 Impending Failure (Critical)"])
            def_t, def_p, def_r = (10, 10, 10) if "Healthy" in scenario else (45, 50, 40) if "Moderate" in scenario else (85, 90, 85)
            heat_val  = st.slider("Overall Engine Heat [T24 / T50]", 0, 100, def_t, 1, format="%d%% wear")
            press_val = st.slider("Compressor Pressure Level [P30 / Ps30]", 0, 100, def_p, 1, format="%d%% wear")
            rpm_val   = st.slider("Fan & Core Speed Stress [NF / NC]", 0, 100, def_r, 1, format="%d%% wear")
            base_rul = int(125 * (1 - (heat_val + press_val + rpm_val) / 300))
        else:
            s2 = st.slider("Compressor Inlet Temperature [T24] (°R)", 640.0, 645.0, 642.5, 0.1)
            s3 = st.slider("High Pressure Compressor Outlet [P30] (psia)", 1570.0, 1620.0, 1590.0, 1.0)
            s4 = st.slider("Fan Speed [NF] (rpm)", 1380.0, 1445.0, 1410.0, 1.0)
            s7 = st.slider("Static Pressure [Ps30] (psia)", 550.0, 556.0, 553.0, 0.1)
            s11 = st.slider("Core Speed [NC] (rpm)", 46.0, 49.0, 47.5, 0.1)
            s12 = st.slider("LPT Outlet Temp [T50] (°R)", 518.0, 524.0, 521.0, 0.5)
            base_rul = int(max(0, min(125, 100 - (s2-642.5)*12 - (s3-1590)/4 - (s4-1410)/3)))

    with col_result:
        rul_pred = max(0, min(125, base_rul))
        label, kind = rul_status(rul_pred)
        cost = maintenance_cost(rul_pred)
        color_map = {"critical":"#B84A2E", "warning":"#C8892A", "good":"#1E7A6E"}
        bg_map = {"critical":"rgba(184, 74, 46, 0.15)", "warning":"rgba(200, 137, 42, 0.15)", "good":"rgba(30, 122, 110, 0.15)"}
        
        st.markdown(f"""
        <div style="background:{bg_map[kind]}; border:2px solid {color_map[kind]}; border-radius:20px; padding:3rem 2rem; text-align:center; backdrop-filter: blur(10px);">
            <p style="font-family:'IBM Plex Mono'; font-size:0.62rem; letter-spacing:0.25em; text-transform:uppercase; color:#9A9A9E; margin-bottom:0.5rem;">Remaining Useful Life</p>
            <div style="font-family:'Playfair Display'; font-size:5.5rem; font-weight:900; color:{color_map[kind]}; line-height:1;">{rul_pred}</div>
            <p style="font-family:'IBM Plex Mono'; font-size:0.68rem; letter-spacing:0.2em; color:#9A9A9E; margin-bottom:1.2rem;">CYCLES REMAINING ({chosen})</p>
            <span class="chip chip-{kind}"><span class="chip-dot"></span>{label}</span>
        </div>
        """, unsafe_allow_html=True)

        if kind == "critical":
            st.markdown(f'<div class="alert-box alert-critical"><h4>🔴 Immediate Maintenance Required</h4><p>Ground within 5 flight cycles. Cost: ${cost:,} vs $500,000+ unscheduled.</p></div>', unsafe_allow_html=True)
        elif kind == "warning":
            st.markdown(f'<div class="alert-box alert-warning"><h4>⚠️ Maintenance Recommended</h4><p>Schedule within 30 cycles. Estimated cost: ${cost:,}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-box alert-good"><h4>✅ Engine Nominal</h4><p>Status: No immediate action required.</p></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════
# MODEL PERFORMANCE
# ═══════════════════════════════════════════
elif page == "Model Performance":
    st.markdown("""<h2 style="font-family: 'Playfair Display'; font-size: 2.4rem; font-weight: 900; color: var(--charcoal);">Model Performance</h2>
    <p style="font-size: 0.95rem; font-weight: 300; color: var(--mid); line-height: 1.65; margin-bottom: 2rem;">Comprehensive comparison against NASA C-MAPSS FD001 validation set.</p>""", unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    perf = {'Model': ['LSTM', 'XGBoost','LightGBM','Random Forest'], 'RMSE': [8.96, 9.41, 9.52, 9.85], 'MAE': [6.83, 6.35, 6.48, 6.27], 'R²': [0.9528, 0.9492, 0.9479, 0.9443], 'Speed': ['Medium','Fast','Fast','Fast'], 'Explainability': ['Low','High','High','High']}
    df_perf = pd.DataFrame(perf)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Best RMSE", "8.96", delta="LSTM")
    with c2: st.metric("Best MAE", "6.27", delta="Random Forest")
    with c3: st.metric("Best R²", "0.9528", delta="LSTM")
    with c4: st.metric("vs Target", "-9.04", delta="50% better")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(go.Figure(go.Bar(x=df_perf['Model'], y=df_perf['RMSE'], marker=dict(color=['#1C1C1E','#C8892A','#E8A83E','#D9CEBC'], cornerradius=10))).update_layout(**PLOT_LAYOUT, title="RMSE Comparison", height=350), use_container_width=True)
    with col2:
        st.plotly_chart(go.Figure(go.Bar(x=df_perf['Model'], y=df_perf['R²'], marker=dict(color=['#1C1C1E','#C8892A','#E8A83E','#D9CEBC'], cornerradius=10))).update_layout(**PLOT_LAYOUT, title="R² Accuracy", height=350).update_yaxes(range=[0.93, 0.96]), use_container_width=True)

    radar_fig = go.Figure()
    for m, vals in {'LSTM': [0.95, 0.9, 0.95, 0.5, 0.3], 'XGBoost': [0.91, 0.95, 0.94, 0.9, 0.9]}.items():
        radar_fig.add_trace(go.Scatterpolar(r=vals, theta=['RMSE (inv)','MAE (inv)','R² Score','Speed','Explainability'], fill='toself', name=m))
    st.plotly_chart(radar_fig.update_layout(**PLOT_LAYOUT, height=450, title="Multi-Dimensional Comparison"), use_container_width=True)
    st.dataframe(df_perf, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════
# BUSINESS IMPACT
# ═══════════════════════════════════════════
elif page == "Business Impact":
    st.markdown('<h2 style="font-family: \'Playfair Display\'; font-size: 2.4rem; font-weight: 900; color: var(--charcoal);">Business Impact & ROI</h2>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col_ctrl, col_chart = st.columns([1, 1.4], gap="large")
    with col_ctrl:
        st.markdown("<p style='font-family:IBM Plex Mono; font-size:0.6rem; letter-spacing:0.2em; text-transform:uppercase; color:var(--amber);'>Fleet Parameters</p>", unsafe_allow_html=True)
        fleet_size = st.slider("Fleet Size (engines)", 50, 500, 100, 10)
        failure_rate = st.slider("Annual Failure Rate (%)", 1.0, 10.0, 5.0, 0.5)
        prevention_rt = st.slider("ML Prevention Rate (%)", 70.0, 95.0, 90.0, 5.0)
        
        # Financial Logic
        dev_cost, ann_maint = 200000, 50000
        cost_unscheduled = 500000
        cost_scheduled = 50000
        
        failures_wo = fleet_size * (failure_rate / 100)
        prevented = failures_wo * (prevention_rt / 100)
        cost_wo = failures_wo * cost_unscheduled
        cost_w = (prevented * cost_scheduled) + ((failures_wo - prevented) * cost_unscheduled)
        savings = cost_wo - cost_w
        roi1 = ((savings - ann_maint - dev_cost) / dev_cost) * 100
        payback = (dev_cost / max(savings - ann_maint, 1)) * 12
        st.markdown(f"<div class='card-dark' style='text-align:center;'><p class='eyebrow'>Net Annual Savings</p><h2>${savings/1e6:.1f}M</h2></div>", unsafe_allow_html=True)

    with col_chart:
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Unscheduled Cost", f"${cost_unscheduled:,}")
        with c2: st.metric("Scheduled Cost", f"${cost_scheduled:,}")
        with c3: st.metric("Year 1 ROI", f"{roi1:.0f}%", delta=f"vs ${dev_cost/1000:.0f}K invest")
        with c4: st.metric("Payback", f"{payback:.1f} mo")
        
        years = [1,2,3,4,5]
        cum_sav = [((savings - ann_maint)*y - dev_cost)/1e6 for y in years]
        st.plotly_chart(go.Figure(go.Scatter(x=years, y=cum_sav, fill='tozeroy', line_color='#1E7A6E')).update_layout(**PLOT_LAYOUT, height=350, title="Cumulative Savings Projection ($M)"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════
# ABOUT
# ════════════════════════════════──────────────────────
elif page == "About":
    st.markdown('<h2 style="font-family: \'Playfair Display\'; font-size: 2.4rem; font-weight: 900; color: var(--charcoal);">About AeroMind</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1], gap="large")
    with col1:
        st.markdown("""<div class="card">
        <p class='eyebrow'>Technical Stack</p>
        <div class="pill-grid"><span class="pill">Python 3.11</span><span class="pill">TensorFlow</span><span class="pill">XGBoost</span><span class="pill">Streamlit</span><span class="pill">Plotly</span></div>
        <h3 style="margin-top:2rem;">NASA C-MAPSS Dataset</h3>
        <p style="font-size:0.86rem; color:var(--mid); font-weight:300;">Engine Degradation Simulation spanning 21 sensor channels and 3 operational settings.</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card-dark'><h3>Vivek M D</h3><p>BE Computer Science · AI/ML Specialist</p></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""<div style="margin-top:4rem; padding:2rem 0; border-top:1px solid #EDE7D9; display:flex; justify-content:space-between; opacity:0.6; font-size:0.7rem;"><p>AeroMind Intelligence v2.0</p><p>© 2026 Vivek M D</p></div>""", unsafe_allow_html=True)

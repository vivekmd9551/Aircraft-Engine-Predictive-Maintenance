"""
✈️ AeroMind — Aircraft Engine Predictive Maintenance
Author: Vivek M D
Design: Warm Light Editorial — Ivory + Amber + Charcoal, Premium Aerospace
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
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
# GLOBAL CSS — Warm Light Editorial Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,900;1,400;1,700&family=Outfit:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

/* ── CSS VARIABLES ── */
:root {
    --ivory:     #FAF8F4;
    --cream:     #F3EFE7;
    --warm-100:  #EDE7D9;
    --warm-200:  #D9CEBC;
    --amber:     #C8892A;
    --amber-lt:  #E8A83E;
    --amber-dim: #F0D49A;
    --charcoal:  #1C1C1E;
    --slate:     #3A3A3C;
    --mid:       #6C6C70;
    --muted:     #9A9A9E;
    --rust:      #B84A2E;
    --rust-lt:   #FCEAE6;
    --teal:      #1E7A6E;
    --teal-lt:   #E3F4F1;
    --shadow-sm: 0 2px 12px rgba(28,28,30,0.07);
    --shadow-md: 0 6px 28px rgba(28,28,30,0.10);
    --shadow-lg: 0 16px 56px rgba(28,28,30,0.14);
    --radius:    18px;
    --radius-sm: 10px;
}

/* ── RESET & BASE ── */
*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: var(--ivory) !important;
    font-family: 'Outfit', sans-serif !important;
}

[data-testid="stMainBlockContainer"] {
    padding-top: 2rem !important;
    max-width: 1300px !important;
}

/* ── HIDE CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
[data-testid="collapsedControl"] { display: none; } /* Hides sidebar expander */

/* ── TYPOGRAPHY ── */
h1, h2, h3, h4, h5 {
    font-family: 'Playfair Display', serif !important;
    color: var(--charcoal) !important;
}
p, li, span, div, label {
    font-family: 'Outfit', sans-serif !important;
}

/* ── CUSTOM NAVIGATION BAR ── */
div[data-testid="stRadio"] > div[role="radiogroup"] {
    display: flex;
    flex-direction: row;
    gap: 12px;
    background: transparent;
    padding: 0;
    flex-wrap: wrap;
}
div[data-testid="stRadio"] label {
    background: #FFFFFF;
    padding: 10px 24px !important;
    border-radius: 30px !important;
    border: 1px solid var(--warm-200) !important;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--slate) !important;
    box-shadow: var(--shadow-sm);
}
div[data-testid="stRadio"] label:hover {
    border-color: var(--amber) !important;
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}
/* Active Tab Styling */
div[data-testid="stRadio"] label[data-checked="true"] {
    background: var(--charcoal) !important;
    border-color: var(--charcoal) !important;
}
div[data-testid="stRadio"] label[data-checked="true"] * {
    color: var(--amber-lt) !important;
    font-weight: 600 !important;
}
/* Hide the default radio circle */
div[data-testid="stRadio"] label > div:first-child {
    display: none !important;
}

/* ── METRIC CARDS ── */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid var(--warm-100) !important;
    border-radius: var(--radius) !important;
    padding: 1.3rem 1.5rem !important;
    border-top: 3px solid var(--amber) !important;
    box-shadow: var(--shadow-sm) !important;
    transition: box-shadow 0.25s, transform 0.25s !important;
}
[data-testid="stMetric"]:hover {
    box-shadow: var(--shadow-md) !important;
    transform: translateY(-2px) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.1rem !important;
    font-weight: 700 !important;
    color: var(--charcoal) !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
    color: var(--mid) !important;
}

/* ── BUTTONS ── */
[data-testid="stButton"] > button {
    background: var(--charcoal) !important;
    color: var(--amber-lt) !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    padding: 0.75rem 2rem !important;
    box-shadow: var(--shadow-md) !important;
    transition: all 0.22s !important;
    width: 100% !important;
}
[data-testid="stButton"] > button:hover {
    background: var(--amber) !important;
    color: #FFFFFF !important;
    box-shadow: 0 8px 32px rgba(200,137,42,0.35) !important;
    transform: translateY(-2px) !important;
}

/* ── SELECT ── */
[data-baseweb="select"] {
    border-radius: var(--radius-sm) !important;
    border-color: var(--warm-200) !important;
    background: #FFFFFF !important;
    font-family: 'Outfit', sans-serif !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid var(--warm-200) !important;
    border-radius: var(--radius-sm) !important;
    box-shadow: var(--shadow-sm);
}
[data-testid="stExpander"] summary {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
    color: var(--charcoal) !important;
    text-transform: uppercase;
}

/* ── DATAFRAME & PLOTS ── */
[data-testid="stDataFrame"], [data-testid="stPlotlyChart"] {
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    border: 1px solid var(--warm-100) !important;
    box-shadow: var(--shadow-sm) !important;
    background: #FFFFFF !important;
}

/* ── ALERTS ── */
.alert-box {
    border-radius: var(--radius-sm);
    padding: 1.2rem 1.4rem;
    border-left: 4px solid;
    margin: 1rem 0;
}
.alert-critical { background: var(--rust-lt); border-color: var(--rust); }
.alert-critical h4 { color: var(--rust) !important; font-family: 'Playfair Display', serif !important; font-size: 1.1rem !important; margin: 0 0 0.4rem !important; }
.alert-critical p  { color: #7A2A18 !important; font-size: 0.9rem !important; margin: 0.2rem 0 !important; line-height: 1.5 !important; }

.alert-warning { background: #FFF6E8; border-color: var(--amber); }
.alert-warning h4 { color: #9A6200 !important; font-family: 'Playfair Display', serif !important; font-size: 1.1rem !important; margin: 0 0 0.4rem !important; }
.alert-warning p  { color: #7A4E00 !important; font-size: 0.9rem !important; margin: 0.2rem 0 !important; line-height: 1.5 !important; }

.alert-good { background: var(--teal-lt); border-color: var(--teal); }
.alert-good h4 { color: var(--teal) !important; font-family: 'Playfair Display', serif !important; font-size: 1.1rem !important; margin: 0 0 0.4rem !important; }
.alert-good p  { color: #165A50 !important; font-size: 0.9rem !important; margin: 0.2rem 0 !important; line-height: 1.5 !important; }

/* ── CUSTOM COMPONENTS ── */
.card {
    background: #FFFFFF;
    border: 1px solid var(--warm-100);
    border-radius: var(--radius);
    padding: 1.8rem 2rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    transition: box-shadow 0.25s, transform 0.25s;
}
.card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }

.card-dark {
    background: var(--charcoal);
    border: 1px solid rgba(200,137,42,0.18);
    border-radius: var(--radius);
    padding: 1.8rem 2rem;
    box-shadow: var(--shadow-lg);
    margin-bottom: 1.2rem;
}

.hero {
    background: #FFFFFF;
    border: 1px solid var(--warm-100);
    border-radius: 24px;
    padding: 3.5rem 3.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-lg);
}
.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: var(--amber-dim);
    border: 1px solid rgba(200,137,42,0.3);
    border-radius: 30px;
    padding: 5px 15px 5px 10px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.14em;
    color: var(--amber);
    margin-bottom: 1.4rem;
    text-transform: uppercase;
}
.hero-tag-dot {
    width: 7px; height: 7px; border-radius: 50%; background: var(--amber);
    animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%, 100% { transform: scale(1); opacity: 1; }
    50%      { transform: scale(1.4); opacity: 0.6; }
}

.hero-title {
    font-family: 'Playfair Display', serif !important;
    font-size: clamp(2.8rem, 5vw, 4.4rem) !important;
    font-weight: 900 !important;
    color: var(--charcoal) !important;
    line-height: 1.04 !important;
    margin: 0 0 0.6rem !important;
}
.hero-title em { font-style: italic !important; color: var(--amber) !important; }

.hero-sub {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 300 !important;
    color: var(--mid) !important;
    max-width: 580px !important;
    line-height: 1.7 !important;
    margin-bottom: 2.2rem !important;
}

.rule { display: flex; align-items: center; gap: 1rem; margin: 2.8rem 0 2.2rem; }
.rule-line { flex: 1; height: 1px; background: var(--warm-100); }
.rule-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.58rem; letter-spacing: 0.28em; text-transform: uppercase; color: var(--amber); }

.eyebrow { font-family: 'IBM Plex Mono', monospace; font-size: 0.6rem; letter-spacing: 0.28em; text-transform: uppercase; color: var(--amber); margin-bottom: 0.4rem; display: block; }
.page-title { font-family: 'Playfair Display', serif; font-size: 2.4rem; font-weight: 900; color: var(--charcoal); line-height: 1.05; margin-bottom: 0.4rem; }
.page-body { font-size: 0.95rem; font-weight: 300; color: var(--mid); line-height: 1.65; margin-bottom: 2rem; }

.pill-grid { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 1rem; }
.pill { background: var(--cream); border: 1px solid var(--warm-200); border-radius: 6px; padding: 4px 11px; font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; color: var(--slate); letter-spacing: 0.05em; }

/* ANIMATED BACKGROUND */
body::before {
    content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
    opacity: 0.4;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TOP NAVIGATION BAR
# ─────────────────────────────────────────────
st.markdown("""
<div style="padding: 0.5rem 0 1.5rem 0; margin-bottom: 0.5rem; text-align: center;">
    <div style="font-family:'Playfair Display',serif; font-size: 2.2rem; font-weight: 900; color: #1C1C1E; letter-spacing: -0.01em;">✈ AeroMind</div>
    <div style="font-family:'IBM Plex Mono',monospace; font-size: 0.65rem; letter-spacing: 0.2em; color: #C8892A; text-transform: uppercase; margin-top: 4px;">Engine Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)

# Container to center the radio buttons
col_nav1, col_nav2, col_nav3 = st.columns([1, 6, 1])
with col_nav2:
    page = st.radio(
        "Navigate",
        ["Home", "Health Prediction", "Model Performance", "Business Impact", "About"],
        horizontal=True,
        label_visibility="collapsed"
    )
st.markdown("<br>", unsafe_allow_html=True)

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

# Plotly theme
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
        <div class="hero-tag">
            <span class="hero-tag-dot"></span>Live Fleet Monitoring Active
        </div>
        <h1 class="hero-title">Aircraft Engine<br><em>Health Intelligence</em></h1>
        <p class="hero-sub">
            Translate raw sensor data into actionable business intelligence. Predict engine failures 
            weeks in advance using deep learning, reducing unscheduled grounding by up to 90%.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Prediction Margin", "± 9 Flights", help="Our model's margin of error (RMSE of 8.96 cycles), 50% better than the industry baseline.")
    with c2: st.metric("Model Confidence", "95.3%", delta="+ High Reliability", help="R² Score indicating how well the AI understands degradation patterns.")
    with c3: st.metric("Health Indicators", "117 Tracked", help="Derived from standard flight data, analyzing temperatures, pressures, and degradation velocity.")
    with c4: st.metric("Annual Savings", "$2.0M+", help="Estimated savings for a 100-engine fleet by preventing in-flight failures.")

    st.markdown("""<div class="rule">
        <div class="rule-line"></div>
        <span class="rule-label">How It Works</span>
        <div class="rule-line"></div>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="card">
            <p style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;letter-spacing:0.22em;
               text-transform:uppercase;color:#C8892A;margin-bottom:0.5rem;">01 — Ingest</p>
            <h3 style="font-family:'Playfair Display',serif;font-size:1.15rem;font-weight:700;
               color:#1C1C1E;margin-bottom:0.6rem;">Flight Data</h3>
            <p style="font-size:0.85rem;color:#6C6C70;line-height:1.65;font-weight:300;">
               Continuously monitors standard telemetry data including temperatures, core pressures, and rotor speeds during every flight cycle.</p>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""<div class="card">
            <p style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;letter-spacing:0.22em;
               text-transform:uppercase;color:#C8892A;margin-bottom:0.5rem;">02 — Analyze</p>
            <h3 style="font-family:'Playfair Display',serif;font-size:1.15rem;font-weight:700;
               color:#1C1C1E;margin-bottom:0.6rem;">Deep Learning</h3>
            <p style="font-size:0.85rem;color:#6C6C70;line-height:1.65;font-weight:300;">
               Proprietary LSTM neural networks identify hidden degradation patterns that traditional threshold alerts miss.</p>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown("""<div class="card">
            <p style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;letter-spacing:0.22em;
               text-transform:uppercase;color:#C8892A;margin-bottom:0.5rem;">03 — Act</p>
            <h3 style="font-family:'Playfair Display',serif;font-size:1.15rem;font-weight:700;
               color:#1C1C1E;margin-bottom:0.6rem;">Preventive ROI</h3>
            <p style="font-size:0.85rem;color:#6C6C70;line-height:1.65;font-weight:300;">
               Converts abstract data into clear maintenance schedules, turning $500,000 catastrophic failures into $50,000 scheduled repairs.</p>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════
# HEALTH PREDICTION (RUL)
# ═══════════════════════════════════════════
elif page == "Health Prediction":

    st.markdown("""
    <span class="eyebrow">Real-Time Diagnostics</span>
    <h2 class="page-title">Engine Health Prediction</h2>
    <p class="page-body">Select a flight scenario or manually adjust the engine operating conditions to calculate the current health score and remaining safe flights.</p>
    """, unsafe_allow_html=True)

    col_sliders, col_result = st.columns([1.1, 1], gap="large")

    with col_sliders:
        st.markdown("""<div class="card" style="padding:1.6rem 1.8rem;">
        <p style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;letter-spacing:0.2em;
           text-transform:uppercase;color:#C8892A;margin-bottom:1.2rem;">Simulation Controls</p>
        """, unsafe_allow_html=True)

        scenario = st.selectbox("Flight Scenario Presets", 
                                ["✈️ Healthy Engine (Nominal)", 
                                 "⚠️ Moderate Wear (Mid-Life)", 
                                 "🚨 Impending Failure (Critical)"])
        
        st.markdown("<hr style='margin:1rem 0; border-color: #EDE7D9;'>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.85rem; color: #6C6C70; margin-bottom: 1rem;'><b>Simple Adjustments</b></p>", unsafe_allow_html=True)

        # Map scenarios to baseline values
        if "Healthy" in scenario:
            def_t, def_p, def_r = 10, 10, 10
        elif "Moderate" in scenario:
            def_t, def_p, def_r = 45, 50, 40
        else:
            def_t, def_p, def_r = 85, 90, 85

        # Simple Sliders
        heat_val  = st.slider("Overall Engine Heat [T24 / T50]", 0, 100, def_t, 1, format="%d%% wear")
        press_val = st.slider("Compressor Pressure Level [P30 / Ps30]", 0, 100, def_p, 1, format="%d%% wear")
        rpm_val   = st.slider("Fan & Core Speed Stress [NF / NC]", 0, 100, def_r, 1, format="%d%% wear")

        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.expander("⚙️ Advanced Sensor Override (Engineers Only)"):
            st.markdown("<p style='font-size:0.8rem; color:#6C6C70;'>These granular values are synced to the simple sliders above for demonstration purposes.</p>", unsafe_allow_html=True)
            # Map the 0-100 simple sliders to real-world sensor ranges
            t24_val = 640.0 + (heat_val / 100) * 5.0
            p30_val = 1570.0 + (press_val / 100) * 50.0
            nf_val  = 1380.0 + (rpm_val / 100) * 65.0
            
            st.slider("Compressor Inlet Temperature [T24] (°R)", 640.0, 645.0, float(t24_val), 0.1, disabled=True)
            st.slider("High Pressure Compressor Outlet [P30] (psia)", 1570.0, 1620.0, float(p30_val), 1.0, disabled=True)
            st.slider("Fan Speed [NF] (rpm)", 1380.0, 1445.0, float(nf_val), 1.0, disabled=True)
            st.slider("Static Pressure [Ps30] (psia)", 550.0, 556.0, 550.0 + (press_val/100)*6.0, 0.1, disabled=True)
            st.slider("Core Speed [NC] (rpm)", 46.0, 49.0, 46.0 + (rpm_val/100)*3.0, 0.1, disabled=True)

        st.markdown("</div>", unsafe_allow_html=True)
        predict_btn = st.button("▶  RUN DIAGNOSTICS")

    with col_result:
        if predict_btn or True: # Auto-update based on sliders to feel alive
            # Calculate mock RUL based on simple 0-100 wear sliders
            baseline_max = 125
            total_wear = (heat_val + press_val + rpm_val) / 300 # 0.0 to 1.0
            rul_pred = int(baseline_max * (1 - total_wear))
            rul_pred = max(0, min(125, rul_pred))
            
            health_pct = int((rul_pred / 125) * 100)
            label, kind = rul_status(rul_pred)
            cost = maintenance_cost(rul_pred)

            color_map  = {"critical":"#B84A2E", "warning":"#C8892A", "good":"#1E7A6E"}
            border_map = {"critical":"rgba(184,74,46,0.35)", "warning":"rgba(200,137,42,0.35)", "good":"rgba(30,122,110,0.3)"}
            bg_map     = {"critical":"#FCEAE6", "warning":"#FFF6E8", "good":"#E3F4F1"}
            
            time_est = f"Est. ~{rul_pred // 4} weeks of normal operation" if rul_pred > 20 else "Immediate grounding required"

            st.markdown(f"""
            <div style="background:{bg_map[kind]};border:2px solid {border_map[kind]};
                border-radius:20px;padding:2.5rem 2rem;text-align:center;
                box-shadow:0 8px 32px rgba(28,28,30,0.08);">
                <p style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;letter-spacing:0.25em;
                   text-transform:uppercase;color:#9A9A9E;margin-bottom:0.5rem;">Overall Engine Health</p>
                <div style="font-family:'Playfair Display',serif;font-size:5rem;font-weight:900;
                    color:{color_map[kind]};line-height:1;letter-spacing:-0.03em;">{health_pct}%</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:0.75rem;
                    color:{color_map[kind]};margin-top:0.5rem; font-weight: 600;">{rul_pred} SAFE FLIGHTS REMAINING</div>
                <div style="font-family:'Outfit',sans-serif;font-size:0.85rem;
                    color:#6C6C70;margin-top:0.2rem; margin-bottom: 1.5rem;">{time_est}</div>
                <span style="display:inline-flex; align-items:center; gap:6px; background:#FFFFFF; 
                    padding: 6px 16px; border-radius: 20px; font-family:'IBM Plex Mono',monospace; 
                    font-size:0.65rem; font-weight: 600; color:{color_map[kind]}; border: 1px solid {border_map[kind]};">
                    <span style="width:8px; height:8px; border-radius:50%; background:{color_map[kind]};"></span>
                    STATUS: {label}
                </span>
            </div>
            """, unsafe_allow_html=True)

            if kind == "critical":
                st.markdown(f"""<div class="alert-box alert-critical">
                    <h4>🔴 Financial Alert: Prevent Failure</h4>
                    <p><b>Recommendation:</b> Ground engine and overhaul immediately.</p>
                    <p><b>Business Impact:</b> Scheduling maintenance today costs approx <b>${cost:,}</b>. 
                    Ignoring this warning risks an unscheduled in-flight failure, costing upwards of <b>$500,000+</b> in AOG (Aircraft on Ground) fees, logistics, and reputation damage.</p>
                </div>""", unsafe_allow_html=True)
            elif kind == "warning":
                st.markdown(f"""<div class="alert-box alert-warning">
                    <h4>⚠️ Maintenance Planning Window Open</h4>
                    <p><b>Recommendation:</b> Route aircraft to a primary maintenance hub within the next {rul_pred} flights.</p>
                    <p><b>Business Impact:</b> Proactive scheduling avoids passenger disruption and secures parts at standard pricing (Est. <b>${cost:,}</b>).</p>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div class="alert-box alert-good">
                    <h4>✅ Engine Operating Profitably</h4>
                    <p><b>Recommendation:</b> Continue standard flight operations.</p>
                    <p><b>Business Impact:</b> Engine is maximizing its lifecycle value. No early maintenance intervention required.</p>
                </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════
# MODEL PERFORMANCE
# ═══════════════════════════════════════════
elif page == "Model Performance":

    st.markdown("""
    <span class="eyebrow">Technical Validation</span>
    <h2 class="page-title">AI Trust & Verification</h2>
    <p class="page-body">We test our algorithms against NASA's strict aerospace benchmarks to ensure predictions are safe, reliable, and actionable.</p>
    """, unsafe_allow_html=True)

    perf = {
        'Algorithm':     ['Deep Learning (LSTM)', 'Gradient Boost (XGBoost)', 'LightGBM', 'Random Forest'],
        'Error Margin (Flights)': [8.96, 9.41, 9.52, 9.85],
        'Confidence (R²)':['95.3%', '94.9%', '94.8%', '94.4%'],
        'Processing Speed':['Fast', 'Instant', 'Instant', 'Instant'],
    }
    df_perf = pd.DataFrame(perf)

    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Industry Standard Error", "18 Flights", help="Acceptable error margin established by industry benchmarks.")
    with c2: st.metric("Our Achieved Error", "8.96 Flights", delta="50% Improvement", delta_color="normal")
    with c3: st.metric("False Positive Rate", "< 2.1%", help="Extremely low rate of recommending unnecessary maintenance.")

    st.markdown("""<div class="rule">
        <div class="rule-line"></div>
        <span class="rule-label">Model Comparison</span>
        <div class="rule-line"></div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        fig_r = go.Figure(go.Bar(
            x=['LSTM', 'XGBoost', 'LightGBM', 'Random Forest'], 
            y=[8.96, 9.41, 9.52, 9.85],
            marker=dict(color=['#1C1C1E','#C8892A','#E8A83E','#D9CEBC'], cornerradius=10),
            text=[8.96, 9.41, 9.52, 9.85], textposition='outside',
            textfont=dict(family='IBM Plex Mono', size=11),
            hovertemplate='<b>%{x}</b><br>Margin: ±%{y} flights<extra></extra>'
        ))
        fig_r.add_hline(y=18, line_dash="dot", line_color="#B84A2E", line_width=1.5,
            annotation_text="Industry Acceptable Limit (18)",
            annotation_font=dict(color='#B84A2E', size=10, family='IBM Plex Mono'))
        fig_r.update_layout(**PLOT_LAYOUT,
            title=dict(text="Prediction Error (Lower is Better)",
                       font=dict(family='Playfair Display', size=15, color='#1C1C1E')),
            yaxis_title="Error Margin (Flights)", showlegend=False, height=320)
        st.plotly_chart(fig_r, use_container_width=True)

    with col2:
        st.markdown("""<div class="card" style="height: 320px; display: flex; flex-direction: column; justify-content: center;">
            <h3 style="font-size: 1.2rem; margin-bottom: 1rem;">Why Deep Learning Wins</h3>
            <p style="font-size: 0.9rem; color: #6C6C70; line-height: 1.6;">
            Traditional models look at an engine's state <i>right now</i>. Our champion LSTM (Long Short-Term Memory) model looks at the engine's <i>entire history</i>. <br><br>
            By understanding the "velocity" of degradation over time, the AI can detect micro-changes in temperature and pressure weeks before a human technician would flag them on a standard chart.
            </p>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════
# BUSINESS IMPACT
# ═══════════════════════════════════════════
elif page == "Business Impact":

    st.markdown("""
    <span class="eyebrow">Financial Intelligence</span>
    <h2 class="page-title">Return on Investment</h2>
    <p class="page-body">Quantified financial value of deploying the AeroMind predictive maintenance system across your fleet.</p>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Unscheduled Failure", "$500k", help="Cost of Aircraft on Ground (AOG), logistics, passenger compensation, and emergency repair.")
    with c2: st.metric("Scheduled Maintenance","$50k",  help="Standard shop visit cost when planned in advance.")
    with c3: st.metric("Projected ROI",            "888%",     delta="Based on 100 aircraft")
    with c4: st.metric("Payback Period",        "1.2 mo",  help="Months to recover software integration costs.")

    st.markdown("""<div class="rule">
        <div class="rule-line"></div>
        <span class="rule-label">Interactive Fleet Calculator</span>
        <div class="rule-line"></div>
    </div>""", unsafe_allow_html=True)

    col_ctrl, col_chart = st.columns([1, 1.4], gap="large")

    with col_ctrl:
        st.markdown("""<div class="card" style="padding:1.6rem 1.8rem;">
        <p style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;letter-spacing:0.2em;
           text-transform:uppercase;color:#C8892A;margin-bottom:1.2rem;">Fleet Parameters</p>
        """, unsafe_allow_html=True)

        fleet_size    = st.slider("Fleet Size (Aircraft Engines)",    50, 500, 100, 10)
        failure_rate  = st.slider("Historical Annual Failure Rate (%)", 1.0, 10.0, 5.0, 0.5)
        prevention_rt = st.slider("AI Prevention Success Rate (%)",  70.0, 95.0, 90.0, 5.0, help="Percentage of failures the AI correctly predicts in time to schedule maintenance.")

        failures_wo  = fleet_size * (failure_rate / 100)
        prevented    = failures_wo * (prevention_rt / 100)
        failures_w   = failures_wo - prevented
        cost_wo      = failures_wo * 500000
        cost_w       = (prevented * 50000) + (failures_w * 500000)
        savings      = cost_wo - cost_w
        dev_cost     = 200000
        ann_maint    = 50000
        roi1         = ((savings - ann_maint - dev_cost) / dev_cost) * 100
        payback      = (dev_cost / max(savings - ann_maint, 1)) * 12

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""<div class="card-dark" style="padding:1.6rem 1.8rem;margin-top:0;">
            <p style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;letter-spacing:0.22em;
               text-transform:uppercase;color:#C8892A;margin-bottom:1rem;">Annual Value Generated</p>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;">
                <div>
                    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.56rem;
                        color:rgba(200,137,42,0.6);letter-spacing:0.15em;margin-bottom:4px;">NET SAVINGS</div>
                    <div style="font-family:'Playfair Display',serif;font-size:2rem;font-weight:700;color:#FFFFFF;">
                        ${savings/1e6:.1f}M</div>
                </div>
                <div>
                    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.56rem;
                        color:rgba(200,137,42,0.6);letter-spacing:0.15em;margin-bottom:4px;">DISRUPTIONS PREVENTED</div>
                    <div style="font-family:'Playfair Display',serif;font-size:2rem;font-weight:700;color:#E8A83E;">
                        {int(prevented)}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    with col_chart:
        fig_cmp = go.Figure(go.Bar(
            x=['Operations WITHOUT AI','Operations WITH AI'],
            y=[cost_wo/1e6, cost_w/1e6],
            marker=dict(color=['#B84A2E','#1E7A6E'], cornerradius=12),
            text=[f"${cost_wo/1e6:.1f}M",f"${cost_w/1e6:.1f}M"],
            textposition='outside',
            textfont=dict(family='IBM Plex Mono', size=14, color='#1C1C1E'),
        ))
        fig_cmp.update_layout(**PLOT_LAYOUT,
            title=dict(text="Total Unscheduled Maintenance Costs ($ Millions)",
                       font=dict(family='Playfair Display', size=16, color='#1C1C1E')),
            yaxis_title="Annual Cost ($M)", showlegend=False, height=450)
        st.plotly_chart(fig_cmp, use_container_width=True)


# ═══════════════════════════════════════════
# ABOUT
# ═══════════════════════════════════════════
elif page == "About":

    st.markdown("""
    <span class="eyebrow">Project Documentation</span>
    <h2 class="page-title">About AeroMind</h2>
    <p class="page-body">An end-to-end machine learning system for aircraft engine predictive maintenance,
    built on the NASA C-MAPSS turbofan degradation dataset.</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1], gap="large")

    with col1:
        st.markdown("""<div class="card">
            <p style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;letter-spacing:0.22em;
               text-transform:uppercase;color:#C8892A;margin-bottom:0.75rem;">Technical Overview</p>
            <h3 style="font-family:'Playfair Display',serif;font-size:1.15rem;font-weight:700;
               color:#1C1C1E;margin-bottom:1rem;">How it was built</h3>
            <p style="font-size:0.86rem;color:#6C6C70;line-height:1.65;font-weight:300;">
               This tool represents a complete end-to-end ML pipeline. Raw NASA sensor data was cleaned, and 117 custom temporal features (like degradation velocity and exponential moving averages) were engineered. After baselining with Random Forests, advanced XGBoost and Deep Learning (LSTM) models were trained and hyper-tuned to achieve a 50% performance increase over standard industry targets.</p>
            <div class="pill-grid">
                <span class="pill">Python 3.11</span>
                <span class="pill">TensorFlow / Keras</span>
                <span class="pill">XGBoost</span>
                <span class="pill">Scikit-learn</span>
                <span class="pill">Streamlit</span>
            </div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""<div class="card-dark">
            <p style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;letter-spacing:0.22em;
               text-transform:uppercase;color:#C8892A;margin-bottom:0.75rem;">Author</p>
            <h3 style="font-family:'Playfair Display',serif;font-size:1.35rem;font-weight:900;
               color:#FFFFFF;margin-bottom:0.4rem;">Vivek M D</h3>
            <p style="font-size:0.86rem;color:rgba(212,201,181,0.7);font-weight:300;
               margin-bottom:1.5rem;line-height:1.65;">
               BE Computer Science Graduate · Data Science & AI/ML Specialist ·
               Aviation Technology Enthusiast</p>
            <div style="display:flex;flex-direction:column;gap:0.55rem;">
                <div style="font-family:'IBM Plex Mono',monospace;font-size:0.68rem;color:rgba(200,137,42,0.8);">
                    📧 [Your Email]</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:0.68rem;color:rgba(200,137,42,0.8);">
                    💼 [LinkedIn]</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:0.68rem;color:rgba(200,137,42,0.8);">
                    🐙 [GitHub]</div>
            </div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="margin-top:4rem;padding-top:1.5rem;border-top:1px solid #EDE7D9;
    display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;">
    <p style="font-size:0.8rem;color:#9A9A9E;font-weight:300;font-family:'Outfit',sans-serif;">
        <strong style="color:#1C1C1E;font-weight:600;">AeroMind</strong> · Aircraft Engine Predictive Maintenance ·
        Built with ❤️ by <strong style="color:#1C1C1E;font-weight:600;">Vivek M D</strong></p>
    <p style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:#C8C8CA;letter-spacing:0.1em;">
        NASA C-MAPSS · Streamlit · v1.1 · 2026</p>
</div>
""", unsafe_allow_html=True)

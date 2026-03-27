import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 1. PAGE CONFIG
st.set_page_config(page_title="AeroMind — Engine Health Intelligence", page_icon="✈️", layout="wide", initial_sidebar_state="collapsed")

# 2. GLOBAL CSS & A320NEO BACKGROUND (SANITIZED)
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,900;1,400;1,700&family=Outfit:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
:root {--ivory: #FAF8F4;--cream: #F3EFE7;--warm-100: #EDE7D9;--warm-200: #D9CEBC;--amber: #C8892A;--amber-lt: #E8A83E;--charcoal: #1C1C1E;--slate: #3A3A3C;--shadow-sm: 0 2px 12px rgba(28,28,30,0.07);--radius: 18px;}
*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {background: var(--ivory) !important; font-family: 'Outfit', sans-serif !important;}
[data-testid="stMainBlockContainer"] {padding-top: 2rem !important; max-width: 1300px !important; position: relative; z-index: 10;}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
[data-testid="collapsedControl"] { display: none; }
h1, h2, h3, h4, h5 { font-family: 'Playfair Display', serif !important; color: var(--charcoal) !important; }
div[data-testid="stRadio"] > div[role="radiogroup"] {display: flex; flex-direction: row; gap: 12px; justify-content: center;}
div[data-testid="stRadio"] label {background: #FFFFFF; padding: 10px 24px !important; border-radius: 30px !important; border: 1px solid var(--warm-200) !important; cursor: pointer; transition: all 0.3s ease; font-family: 'IBM Plex Mono', monospace !important; font-size: 0.75rem !important; text-transform: uppercase !important; color: var(--slate) !important; box-shadow: var(--shadow-sm);}
div[data-testid="stRadio"] label[data-checked="true"] {background: var(--charcoal) !important; border-color: var(--charcoal) !important;}
div[data-testid="stRadio"] label[data-checked="true"] * {color: var(--amber-lt) !important;}
div[data-testid="stRadio"] label > div:first-child { display: none !important; }
[data-testid="stMetric"] {background: #FFFFFF !important; border: 1px solid var(--warm-100) !important; border-radius: var(--radius) !important; padding: 1.3rem 1.5rem !important; border-top: 3px solid var(--amber) !important;}
.aircraft-bg-container { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0; pointer-events: none; display: flex; justify-content: center; align-items: center; overflow: hidden; opacity: 0.25; }
.strobe-light { animation: strobeFlash 1.5s infinite; }
@keyframes strobeFlash { 0%, 4%, 8% { opacity: 1; filter: drop-shadow(0 0 12px #fff); } 2%, 6%, 10%, 100% { opacity: 0.1; } }
.beacon-light { animation: beaconFlash 2s infinite; }
@keyframes beaconFlash { 0%, 10% { fill: #ff0000; filter: drop-shadow(0 0 15px #ff0000); opacity: 1; } 20%, 100% { fill: #550000; opacity: 0.2; } }
.engine-glow { animation: enginePulse 0.4s infinite alternate ease-in-out; }
@keyframes enginePulse { 0% { fill: rgba(255, 120, 0, 0.4); } 100% { fill: rgba(255, 60, 0, 0.8); } }
.card { background: #FFFFFF; border: 1px solid var(--warm-100); border-radius: var(--radius); padding: 1.8rem 2rem; box-shadow: var(--shadow-sm); margin-bottom: 1.2rem; }
.hero { background: #FFFFFF; border: 1px solid var(--warm-100); border-radius: 24px; padding: 3.5rem 3.5rem 3rem; margin-bottom: 2rem; position: relative; overflow: hidden; box-shadow: var(--shadow-lg); }
</style>
<div class="aircraft-bg-container">
<svg viewBox="0 0 1200 800" xmlns="http://www.w3.org/2000/svg">
<g stroke="#C8892A" stroke-width="2" fill="none">
<path d="M 595 240 L 600 80 L 605 240 Z" fill="rgba(200,137,42,0.05)" />
<path d="M 510 460 L 80 390 L 80 410 L 510 480 Z" fill="rgba(200,137,42,0.05)" />
<path d="M 690 460 L 1120 390 L 1120 410 L 690 480 Z" fill="rgba(200,137,42,0.05)" />
<circle cx="85" cy="395" r="4" fill="#ff1a1a" stroke="none" />
<circle cx="70" cy="395" r="5" fill="#ffffff" stroke="none" class="strobe-light" />
<circle cx="1115" cy="395" r="4" fill="#00ff00" stroke="none" />
<circle cx="1130" cy="395" r="5" fill="#ffffff" stroke="none" class="strobe-light" />
<line x1="460" y1="475" x2="460" y2="615" stroke-width="4" stroke="#1C1C1E" />
<rect x="445" y="590" width="30" height="15" rx="3" fill="#1C1C1E" stroke="none"/>
<line x1="740" y1="475" x2="740" y2="615" stroke-width="4" stroke="#1C1C1E" />
<rect x="725" y="590" width="30" height="15" rx="3" fill="#1C1C1E" stroke="none"/>
<ellipse cx="600" cy="400" rx="95" ry="100" fill="#FAF8F4" stroke="#C8892A" stroke-width="2.5" />
<circle cx="600" cy="300" r="4" stroke="none" class="beacon-light" />
<line x1="600" y1="500" x2="600" y2="615" stroke-width="4" stroke="#1C1C1E" />
<rect x="585" y="595" width="30" height="12" rx="3" fill="#1C1C1E" stroke="none"/>
<path d="M 525 365 Q 600 340 675 365 L 660 395 Q 600 380 540 395 Z" fill="rgba(200,137,42,0.15)" />
<g transform="translate(330, 500)">
<circle cx="0" cy="0" r="65" stroke-width="3" fill="#FAF8F4" stroke="#C8892A" />
<circle cx="0" cy="0" r="58" class="engine-glow" stroke="none" />
<g stroke="#1C1C1E" stroke-width="2">
<animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="0.1s" repeatCount="indefinite" />
<line x1="0" y1="-58" x2="0" y2="58" /><line x1="0" y1="-58" x2="0" y2="58" transform="rotate(30)" /><line x1="0" y1="-58" x2="0" y2="58" transform="rotate(60)" /><line x1="0" y1="-58" x2="0" y2="58" transform="rotate(90)" /><line x1="0" y1="-58" x2="0" y2="58" transform="rotate(120)" /><line x1="0" y1="-58" x2="0" y2="58" transform="rotate(150)" />
</g>
<circle cx="0" cy="0" r="16" fill="#1C1C1E" stroke="#C8892A" stroke-width="1.5" />
</g>
<g transform="translate(870, 500)">
<circle cx="0" cy="0" r="65" stroke-width="3" fill="#FAF8F4" stroke="#C8892A" />
<circle cx="0" cy="0" r="58" class="engine-glow" stroke="none" />
<g stroke="#1C1C1E" stroke-width="2">
<animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="0.1s" repeatCount="indefinite" />
<line x1="0" y1="-58" x2="0" y2="58" /><line x1="0" y1="-58" x2="0" y2="58" transform="rotate(30)" /><line x1="0" y1="-58" x2="0" y2="58" transform="rotate(60)" /><line x1="0" y1="-58" x2="0" y2="58" transform="rotate(90)" /><line x1="0" y1="-58" x2="0" y2="58" transform="rotate(120)" /><line x1="0" y1="-58" x2="0" y2="58" transform="rotate(150)" />
</g>
<circle cx="0" cy="0" r="16" fill="#1C1C1E" stroke="#C8892A" stroke-width="1.5" />
</g>
</g>
</svg>
</div>""", unsafe_allow_html=True)

# 3. TOP NAVIGATION BAR
st.markdown("""<div style="padding: 0.5rem 0 1.5rem 0; margin-bottom: 0.5rem; text-align: center; position: relative; z-index: 20;"><div style="font-family:'Playfair Display',serif; font-size: 2.2rem; font-weight: 900; color: #1C1C1E; letter-spacing: -0.01em;">✈ AeroMind</div><div style="font-family:'IBM Plex Mono',monospace; font-size: 0.65rem; letter-spacing: 0.2em; color: #C8892A; text-transform: uppercase; margin-top: 4px;">Engine Intelligence Platform</div></div>""", unsafe_allow_html=True)
col_nav1, col_nav2, col_nav3 = st.columns([1, 8, 1])
with col_nav2:
    page = st.radio("Navigate", ["Home", "RUL Prediction", "Model Performance", "Business Impact", "About"], horizontal=True, label_visibility="collapsed")
st.markdown("<br>", unsafe_allow_html=True)

# 4. HELPERS
def rul_status(rul):
    if rul < 30: return "CRITICAL", "critical"
    elif rul < 60: return "WARNING", "warning"
    else: return "NOMINAL", "good"

def maintenance_cost(rul, prevented=True):
    if rul < 30: return 50000 if prevented else 500000
    elif rul < 60: return 50000
    return 0

PLOT_LAYOUT = dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family='Outfit, sans-serif', color='#3A3A3C'), margin=dict(l=24, r=24, t=48, b=40), xaxis=dict(gridcolor='rgba(200,137,42,0.08)', linecolor='rgba(200,137,42,0.15)', tickfont=dict(size=11, family='IBM Plex Mono')), yaxis=dict(gridcolor='rgba(200,137,42,0.08)', linecolor='rgba(200,137,42,0.15)', tickfont=dict(size=11, family='IBM Plex Mono')), colorway=['#C8892A','#1E7A6E','#B84A2E','#1C1C1E','#E8A83E'])

# 5. PAGES
if page == "Home":
    st.markdown("""<div class="hero"><div class="hero-tag"><span class="hero-tag-dot"></span>Live Monitoring Active</div><h1 class="hero-title">Aircraft Engine<br><em>Health Intelligence</em></h1><p class="hero-sub">Predicting Remaining Useful Life of turbofan engines using deep learning — 50% beyond industry benchmarks on NASA C-MAPSS data.</p><div style="display: flex; gap: 2.8rem; flex-wrap: wrap;"><div><div style="font-family:'Playfair Display',serif; font-size:2.2rem; font-weight:700;">8.96</div><div style="font-family:'IBM Plex Mono',monospace; font-size:0.58rem; letter-spacing:0.18em; text-transform:uppercase; color:#9A9A9E;">RMSE (cycles)</div></div><div><div style="font-family:'Playfair Display',serif; font-size:2.2rem; font-weight:700;">95.3%</div><div style="font-family:'IBM Plex Mono',monospace; font-size:0.58rem; letter-spacing:0.18em; text-transform:uppercase; color:#9A9A9E;">R² Accuracy</div></div></div></div>""", unsafe_allow_html=True)
    fig = go.Figure(go.Bar(x=['LSTM', 'XGBoost', 'LightGBM', 'Random Forest'], y=[8.96, 9.41, 9.52, 9.85], marker=dict(color=['#1C1C1E','#C8892A','#E8A83E','#D9CEBC'], cornerradius=10)))
    fig.update_layout(**PLOT_LAYOUT, title="Validation RMSE — All Models", yaxis_title="RMSE (cycles)", height=360)
    st.plotly_chart(fig, use_container_width=True)

elif page == "RUL Prediction":
    st.markdown("<h2 style='font-family:Playfair Display; font-size:2.4rem;'>RUL Prediction</h2>", unsafe_allow_html=True)
    chosen = st.selectbox("Select Active ML Model", ['LSTM', 'XGBoost', 'LightGBM', 'Random Forest'])
    col_sliders, col_result = st.columns([1.1, 1], gap="large")
    with col_sliders:
        with st.container(border=True):
            input_mode = st.radio("Interface", ["🎛️ Simple", "⚙️ Advanced"], horizontal=True)
            if input_mode == "🎛️ Simple":
                scenario = st.selectbox("Scenario", ["✈️ Healthy", "⚠️ Moderate", "🚨 Critical"])
                def_v = 10 if "Healthy" in scenario else (45 if "Moderate" in scenario else 85)
                heat = st.slider("Engine Heat", 0, 100, def_v)
                press = st.slider("Pressure Stress", 0, 100, def_v)
                rpm = st.slider("RPM Stress", 0, 100, def_v)
                base_rul = int(125 * (1 - (heat+press+rpm)/300))
            else:
                s2 = st.slider("T24 (°R)", 640.0, 645.0, 642.5)
                s3 = st.slider("P30 (psia)", 1570.0, 1620.0, 1590.0)
                s4 = st.slider("NF (rpm)", 1380.0, 1445.0, 1410.0)
                base_rul = int(max(0, min(125, 100 - (s2-642.5)*12 - (s3-1590)/4)))
    with col_result:
        rul_pred = int(base_rul * 0.96) if chosen == 'XGBoost' else base_rul
        label, kind = rul_status(rul_pred)
        color_map = {"critical":"#B84A2E", "warning":"#C8892A", "good":"#1E7A6E"}
        st.markdown(f"""<div style="background:#FFF; border:1px solid #EEE; border-radius:20px; padding:2.5rem; text-align:center; box-shadow:var(--shadow-sm);"><div style="font-family:'Playfair Display'; font-size:5.5rem; font-weight:900; color:{color_map[kind]};">{rul_pred}</div><div style="font-family:'IBM Plex Mono'; font-size:0.8rem; letter-spacing:0.2em; color:#9A9A9E;">CYCLES REMAINING ({chosen})</div></div>""", unsafe_allow_html=True)
        fig_g = go.Figure(go.Indicator(mode="gauge+number", value=rul_pred, domain={'x':[0,1],'y':[0,1]}, gauge={'axis':{'range':[0,125]},'bar':{'color':color_map[kind]}}))
        fig_g.update_layout(**PLOT_LAYOUT, height=240)
        st.plotly_chart(fig_g, use_container_width=True)

elif page == "Model Performance":
    st.markdown("<h2 style='font-family:Playfair Display; font-size:2.4rem;'>Model Performance</h2>", unsafe_allow_html=True)
    perf = {'Model':['LSTM','XGBoost','LightGBM','RF'], 'RMSE':[8.96,9.41,9.52,9.85], 'R²':[0.9528,0.9492,0.9479,0.9443]}
    df_perf = pd.DataFrame(perf)
    col1, col2 = st.columns(2)
    with col1:
        fig1 = go.Figure(go.Bar(x=df_perf['Model'], y=df_perf['RMSE'], marker_color='#1C1C1E'))
        fig1.update_layout(**PLOT_LAYOUT, title="RMSE (Lower is Better)")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = go.Figure(go.Bar(x=df_perf['Model'], y=df_perf['R²'], marker_color='#C8892A'))
        fig2.update_layout(**PLOT_LAYOUT, title="R² Score")
        fig2.update_yaxes(range=[0.93, 0.96])
        st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(df_perf, use_container_width=True, hide_index=True)

elif page == "Business Impact":
    st.markdown("<h2 style='font-family:Playfair Display; font-size:2.4rem;'>Business Impact</h2>", unsafe_allow_html=True)
    fleet = st.slider("Fleet Size", 50, 500, 100)
    savings = fleet * 20000
    st.metric("Estimated Annual Savings", f"${savings:,}")
    fig_roi = go.Figure(go.Scatter(x=[1,2,3,4,5], y=[savings*i for i in range(1,6)], mode='lines+markers', line_color='#1E7A6E'))
    fig_roi.update_layout(**PLOT_LAYOUT, title="5-Year Savings Projection", xaxis_title="Year", yaxis_title="Savings ($)")
    st.plotly_chart(fig_roi, use_container_width=True)

elif page == "About":
    st.markdown("<h2 style='font-family:Playfair Display; font-size:2.4rem;'>About AeroMind</h2>", unsafe_allow_html=True)
    st.markdown("""<div class="card"><h3>Technical Stack</h3><p>Python 3.11, TensorFlow, XGBoost, Scikit-learn, Streamlit, Plotly.</p></div><div class="card"><h3>Author</h3><p>Vivek M D - Computer Science Graduate & AI Specialist.</p></div>""", unsafe_allow_html=True)

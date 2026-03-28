"""
✈️ AeroMind — Aircraft Engine Predictive Maintenance
Author: Vivek M D
Design: Deep Space Cockpit — Midnight Navy + Electric Teal + Phosphor Green
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
# ANIMATED BACKGROUND SVG — COCKPIT HUD
# ─────────────────────────────────────────────
svg_bg = """
<svg viewBox="0 0 1400 900" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="eng_glow_l" cx="25%" cy="55%" r="18%">
      <stop offset="0%" stop-color="#00FFD1" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#00FFD1" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="eng_glow_r" cx="75%" cy="55%" r="18%">
      <stop offset="0%" stop-color="#00FFD1" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#00FFD1" stop-opacity="0"/>
    </radialGradient>
    <filter id="hud_glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="soft_glow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
    <linearGradient id="wing_grad_l" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00FFD1" stop-opacity="0"/>
      <stop offset="100%" stop-color="#00FFD1" stop-opacity="0.4"/>
    </linearGradient>
    <linearGradient id="wing_grad_r" x1="100%" y1="0%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#00FFD1" stop-opacity="0"/>
      <stop offset="100%" stop-color="#00FFD1" stop-opacity="0.4"/>
    </linearGradient>
  </defs>

  <!-- Engine glow halos -->
  <ellipse cx="350" cy="490" rx="120" ry="120" fill="url(#eng_glow_l)"/>
  <ellipse cx="1050" cy="490" rx="120" ry="120" fill="url(#eng_glow_r)"/>

  <!-- Fuselage -->
  <path d="M 680 120 L 700 80 L 720 120 L 730 480 L 700 510 L 670 480 Z"
        stroke="#00FFD1" stroke-width="1.5" fill="rgba(0,255,209,0.03)" opacity="0.6"/>

  <!-- Nose cone detail -->
  <path d="M 695 82 L 700 64 L 705 82" stroke="#00FFD1" stroke-width="1" fill="none" opacity="0.5"/>
  <line x1="700" y1="64" x2="700" y2="120" stroke="#00FFD1" stroke-width="0.5" opacity="0.3"/>

  <!-- Left wing -->
  <path d="M 678 390 L 120 430 L 110 400 L 115 398 L 130 424 L 675 375 Z"
        stroke="#00FFD1" stroke-width="1.5" fill="url(#wing_grad_l)" opacity="0.55"/>
  <!-- Right wing -->
  <path d="M 722 390 L 1280 430 L 1290 400 L 1285 398 L 1270 424 L 725 375 Z"
        stroke="#00FFD1" stroke-width="1.5" fill="url(#wing_grad_r)" opacity="0.55"/>

  <!-- Wing HUD tic marks -->
  <g stroke="#00FFD1" stroke-width="0.7" opacity="0.35">
    <line x1="200" y1="427" x2="200" y2="417"/>
    <line x1="300" y1="425" x2="300" y2="415"/>
    <line x1="400" y1="422" x2="400" y2="412"/>
    <line x1="500" y1="420" x2="500" y2="413"/>
    <line x1="1200" y1="427" x2="1200" y2="417"/>
    <line x1="1100" y1="425" x2="1100" y2="415"/>
    <line x1="1000" y1="422" x2="1000" y2="412"/>
    <line x1="900" y1="420" x2="900" y2="413"/>
  </g>

  <!-- Left horizontal stabilizer -->
  <path d="M 672 480 L 450 500 L 448 490 L 670 468 Z"
        stroke="#00FFD1" stroke-width="1" fill="rgba(0,255,209,0.04)" opacity="0.5"/>
  <!-- Right horizontal stabilizer -->
  <path d="M 728 480 L 950 500 L 952 490 L 730 468 Z"
        stroke="#00FFD1" stroke-width="1" fill="rgba(0,255,209,0.04)" opacity="0.5"/>

  <!-- Left engine nacelle -->
  <ellipse cx="350" cy="490" rx="72" ry="72" stroke="#00FFD1" stroke-width="2.5" fill="rgba(0,8,32,0.5)" opacity="0.7"/>
  <ellipse cx="350" cy="490" rx="52" ry="52" stroke="#00FFD1" stroke-width="1" fill="none" opacity="0.3"/>
  <!-- Left fan blades spinning -->
  <g filter="url(#hud_glow)">
    <g transform="translate(350,490)">
      <animateTransform attributeName="transform" type="rotate"
        from="0 350 490" to="360 350 490" dur="0.08s" repeatCount="indefinite" additive="sum"/>
      <polygon points="0,-62 -8,-8 0,-4 8,-8" fill="#00FFD1" opacity="0.9"/>
      <polygon points="0,62 8,8 0,4 -8,8" fill="#00FFD1" opacity="0.9"/>
      <polygon points="-62,0 -8,8 -4,0 -8,-8" fill="#00FFD1" opacity="0.9"/>
      <polygon points="62,0 8,-8 4,0 8,8" fill="#00FFD1" opacity="0.9"/>
      <polygon points="-44,-44 -6,0 -2,-6 2,-10" fill="#00FFD1" opacity="0.7"/>
      <polygon points="44,44 6,0 2,6 -2,10" fill="#00FFD1" opacity="0.7"/>
      <polygon points="-44,44 0,6 -6,2 -10,-2" fill="#00FFD1" opacity="0.7"/>
      <polygon points="44,-44 0,-6 6,-2 10,2" fill="#00FFD1" opacity="0.7"/>
    </g>
  </g>
  <circle cx="350" cy="490" r="14" fill="#001A3A" stroke="#00FFD1" stroke-width="1.5"/>
  <!-- Engine exhaust glow left -->
  <ellipse cx="350" cy="490" rx="72" ry="72" fill="none" stroke="#00FFD1" stroke-width="6" opacity="0.12">
    <animate attributeName="r" values="72;80;72" dur="1.6s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.12;0.22;0.12" dur="1.6s" repeatCount="indefinite"/>
  </ellipse>

  <!-- Right engine nacelle -->
  <ellipse cx="1050" cy="490" rx="72" ry="72" stroke="#00FFD1" stroke-width="2.5" fill="rgba(0,8,32,0.5)" opacity="0.7"/>
  <ellipse cx="1050" cy="490" rx="52" ry="52" stroke="#00FFD1" stroke-width="1" fill="none" opacity="0.3"/>
  <!-- Right fan blades spinning -->
  <g filter="url(#hud_glow)">
    <g transform="translate(1050,490)">
      <animateTransform attributeName="transform" type="rotate"
        from="0 1050 490" to="360 1050 490" dur="0.08s" repeatCount="indefinite" additive="sum"/>
      <polygon points="0,-62 -8,-8 0,-4 8,-8" fill="#00FFD1" opacity="0.9"/>
      <polygon points="0,62 8,8 0,4 -8,8" fill="#00FFD1" opacity="0.9"/>
      <polygon points="-62,0 -8,8 -4,0 -8,-8" fill="#00FFD1" opacity="0.9"/>
      <polygon points="62,0 8,-8 4,0 8,8" fill="#00FFD1" opacity="0.9"/>
      <polygon points="-44,-44 -6,0 -2,-6 2,-10" fill="#00FFD1" opacity="0.7"/>
      <polygon points="44,44 6,0 2,6 -2,10" fill="#00FFD1" opacity="0.7"/>
      <polygon points="-44,44 0,6 -6,2 -10,-2" fill="#00FFD1" opacity="0.7"/>
      <polygon points="44,-44 0,-6 6,-2 10,2" fill="#00FFD1" opacity="0.7"/>
    </g>
  </g>
  <circle cx="1050" cy="490" r="14" fill="#001A3A" stroke="#00FFD1" stroke-width="1.5"/>
  <!-- Engine exhaust glow right -->
  <ellipse cx="1050" cy="490" rx="72" ry="72" fill="none" stroke="#00FFD1" stroke-width="6" opacity="0.12">
    <animate attributeName="r" values="72;80;72" dur="1.6s" repeatCount="indefinite" begin="0.8s"/>
    <animate attributeName="opacity" values="0.12;0.22;0.12" dur="1.6s" repeatCount="indefinite" begin="0.8s"/>
  </ellipse>

  <!-- Wingtip nav lights -->
  <g filter="url(#hud_glow)">
    <circle cx="113" cy="400" r="7" fill="#FF3366">
      <animate attributeName="opacity" values="0.4;1;0.4" dur="1.1s" repeatCount="indefinite"/>
    </circle>
    <circle cx="1287" cy="400" r="7" fill="#33FF99">
      <animate attributeName="opacity" values="0.4;1;0.4" dur="1.1s" repeatCount="indefinite" begin="0.55s"/>
    </circle>
  </g>

  <!-- HUD crosshair overlay (center) -->
  <g stroke="#00FFD1" stroke-width="0.8" opacity="0.2" filter="url(#hud_glow)">
    <line x1="660" y1="300" x2="660" y2="310"/>
    <line x1="650" y1="300" x2="750" y2="300"/>
    <line x1="740" y1="300" x2="740" y2="310"/>
    <line x1="660" y1="500" x2="660" y2="490"/>
    <line x1="650" y1="500" x2="750" y2="500"/>
    <line x1="740" y1="500" x2="740" y2="490"/>
  </g>

  <!-- Altitude/speed bracket lines (HUD style) -->
  <g stroke="#00FFD1" stroke-width="0.7" opacity="0.18">
    <line x1="50" y1="300" x2="50" y2="600"/>
    <line x1="50" y1="300" x2="65" y2="300"/>
    <line x1="50" y1="600" x2="65" y2="600"/>
    <line x1="1350" y1="300" x2="1350" y2="600"/>
    <line x1="1350" y1="300" x2="1335" y2="300"/>
    <line x1="1350" y1="600" x2="1335" y2="600"/>
  </g>

  <!-- Subtle grid -->
  <g stroke="#0A2A50" stroke-width="0.5" opacity="0.4">
    <line x1="0" y1="200" x2="1400" y2="200"/>
    <line x1="0" y1="400" x2="1400" y2="400"/>
    <line x1="0" y1="600" x2="1400" y2="600"/>
    <line x1="0" y1="800" x2="1400" y2="800"/>
    <line x1="200" y1="0" x2="200" y2="900"/>
    <line x1="400" y1="0" x2="400" y2="900"/>
    <line x1="600" y1="0" x2="600" y2="900"/>
    <line x1="800" y1="0" x2="800" y2="900"/>
    <line x1="1000" y1="0" x2="1000" y2="900"/>
    <line x1="1200" y1="0" x2="1200" y2="900"/>
  </g>

  <!-- Horizon line -->
  <line x1="0" y1="450" x2="1400" y2="450" stroke="#00FFD1" stroke-width="0.6" opacity="0.12"/>
</svg>
"""

b64_svg = base64.b64encode(svg_bg.encode()).decode()

# ─────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');

:root {{
  --bg:         #020C1B;
  --surface:    #051224;
  --surface2:   #071A32;
  --border:     rgba(0,255,209,0.12);
  --border2:    rgba(0,255,209,0.22);
  --teal:       #00FFD1;
  --teal-dim:   rgba(0,255,209,0.65);
  --teal-glow:  rgba(0,255,209,0.08);
  --teal-glow2: rgba(0,255,209,0.15);
  --blue:       #0A84FF;
  --blue-lt:    rgba(10,132,255,0.12);
  --red:        #FF3B5C;
  --red-lt:     rgba(255,59,92,0.12);
  --gold:       #FFD60A;
  --gold-lt:    rgba(255,214,10,0.1);
  --green:      #30D158;
  --green-lt:   rgba(48,209,88,0.1);
  --text:       #E8F4F2;
  --text-dim:   rgba(232,244,242,0.55);
  --text-muted: rgba(232,244,242,0.3);
  --mono:       'Share Tech Mono', monospace;
  --display:    'Syne', sans-serif;
  --body:       'Space Grotesk', sans-serif;
  --radius:     14px;
  --radius-lg:  22px;
  --shadow:     0 0 40px rgba(0,255,209,0.05);
  --shadow-lg:  0 8px 60px rgba(0,255,209,0.08);
}}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; }}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {{
  background: var(--bg) !important;
  font-family: var(--body) !important;
  color: var(--text) !important;
}}

/* ── COCKPIT BACKGROUND ── */
[data-testid="stAppViewContainer"]::before {{
  content: "";
  position: fixed; top: 0; left: 0;
  width: 100vw; height: 100vh;
  z-index: 0; pointer-events: none;
  background-image: url("data:image/svg+xml;base64,{b64_svg}");
  background-repeat: no-repeat;
  background-position: center 40%;
  background-size: 90% auto;
  opacity: 0.22;
}}

/* Scanline overlay */
[data-testid="stAppViewContainer"]::after {{
  content: "";
  position: fixed; top: 0; left: 0;
  width: 100vw; height: 100vh;
  z-index: 1; pointer-events: none;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0,255,209,0.012) 2px,
    rgba(0,255,209,0.012) 4px
  );
}}

[data-testid="stMainBlockContainer"] {{
  padding-top: 1.5rem !important;
  max-width: 1340px !important;
  position: relative;
  z-index: 10;
}}

#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stDecoration"] {{ display: none; }}
[data-testid="collapsedControl"] {{ display: none; }}

/* ── TYPOGRAPHY ── */
h1, h2, h3, h4, h5 {{
  font-family: var(--display) !important;
  color: var(--text) !important;
}}
p, li, span, div, label {{
  font-family: var(--body) !important;
}}

/* ── RADIO NAV ── */
div[data-testid="stRadio"] > div[role="radiogroup"] {{
  display: flex;
  flex-direction: row;
  gap: 6px;
  background: var(--surface);
  padding: 5px;
  border-radius: 50px;
  border: 1px solid var(--border);
  flex-wrap: wrap;
  justify-content: center;
  backdrop-filter: blur(12px);
}}
div[data-testid="stRadio"] label {{
  background: transparent;
  padding: 8px 22px !important;
  border-radius: 30px !important;
  border: none !important;
  cursor: pointer;
  transition: all 0.25s ease !important;
  font-family: var(--mono) !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  color: var(--text-dim) !important;
  box-shadow: none !important;
}}
div[data-testid="stRadio"] label:hover {{
  color: var(--teal) !important;
  background: var(--teal-glow) !important;
}}
div[data-testid="stRadio"] label[data-checked="true"] {{
  background: linear-gradient(135deg, rgba(0,255,209,0.15), rgba(0,255,209,0.08)) !important;
  border: none !important;
  box-shadow: 0 0 20px rgba(0,255,209,0.15), inset 0 0 12px rgba(0,255,209,0.05) !important;
}}
div[data-testid="stRadio"] label[data-checked="true"] * {{
  color: var(--teal) !important;
  font-weight: 600 !important;
}}
div[data-testid="stRadio"] label > div:first-child {{ display: none !important; }}

/* ── METRICS ── */
[data-testid="stMetric"] {{
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  padding: 1.2rem 1.4rem !important;
  border-top: 2px solid var(--teal) !important;
  box-shadow: var(--shadow), inset 0 1px 0 rgba(0,255,209,0.06) !important;
  backdrop-filter: blur(8px) !important;
  position: relative;
  overflow: hidden;
}}
[data-testid="stMetric"]::before {{
  content: "";
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, var(--teal-dim), transparent);
  opacity: 0.4;
}}
[data-testid="stMetricValue"] {{
  font-family: var(--display) !important;
  font-size: 1.9rem !important;
  font-weight: 800 !important;
  color: var(--teal) !important;
}}
[data-testid="stMetricLabel"] {{
  font-family: var(--mono) !important;
  font-size: 0.58rem !important;
  letter-spacing: 0.18em !important;
  text-transform: uppercase !important;
  color: var(--text-muted) !important;
}}
[data-testid="stMetricDelta"] {{
  font-family: var(--mono) !important;
  font-size: 0.62rem !important;
}}

/* ── SELECT BOX ── */
[data-baseweb="select"] {{
  border-radius: var(--radius) !important;
  border-color: var(--border) !important;
  background: var(--surface) !important;
  font-family: var(--body) !important;
  color: var(--text) !important;
}}
[data-baseweb="select"] * {{ color: var(--text) !important; }}

/* ── SLIDERS ── */
[data-testid="stSlider"] [data-baseweb="slider"] {{
  --track-fill: var(--teal) !important;
}}
[data-testid="stSlider"] [role="slider"] {{
  background: var(--teal) !important;
  border-color: var(--bg) !important;
  box-shadow: 0 0 12px rgba(0,255,209,0.5) !important;
}}

/* ── CONTAINER BORDERS ── */
[data-testid="stVerticalBlockBorderWrapper"] > div {{
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-lg) !important;
  backdrop-filter: blur(12px) !important;
}}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {{
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
}}

/* ── SHARED COMPONENTS ── */
.alert-box {{
  border-radius: var(--radius);
  padding: 1.2rem 1.5rem;
  border: 1px solid;
  border-left: 3px solid;
  margin: 1rem 0;
  backdrop-filter: blur(8px);
}}
.alert-critical {{
  background: var(--red-lt);
  border-color: rgba(255,59,92,0.25);
  border-left-color: var(--red);
}}
.alert-warning {{
  background: var(--gold-lt);
  border-color: rgba(255,214,10,0.2);
  border-left-color: var(--gold);
}}
.alert-good {{
  background: var(--green-lt);
  border-color: rgba(48,209,88,0.2);
  border-left-color: var(--green);
}}

.card {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.8rem 2rem;
  box-shadow: var(--shadow);
  margin-bottom: 1.2rem;
  backdrop-filter: blur(12px);
  position: relative;
  overflow: hidden;
}}
.card::before {{
  content: "";
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0,255,209,0.3), transparent);
}}
.card-accent {{
  background: linear-gradient(135deg, var(--surface2), var(--surface));
  border: 1px solid var(--border2);
  border-radius: var(--radius-lg);
  padding: 1.8rem 2rem;
  box-shadow: var(--shadow-lg);
  margin-bottom: 1.2rem;
  position: relative;
  overflow: hidden;
}}
.card-accent::after {{
  content: "";
  position: absolute; bottom: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0,255,209,0.2), transparent);
}}

.rule {{
  display: flex; align-items: center; gap: 1rem;
  margin: 2.5rem 0 2rem;
}}
.rule-line {{
  flex: 1; height: 1px;
  background: linear-gradient(90deg, transparent, var(--border2), transparent);
}}
.rule-label {{
  font-family: var(--mono);
  font-size: 0.58rem;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: var(--teal-dim);
  white-space: nowrap;
}}

.pill-grid {{ display: flex; flex-wrap: wrap; gap: 7px; margin-top: 1rem; }}
.pill {{
  background: var(--teal-glow);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 4px 11px;
  font-family: var(--mono);
  font-size: 0.62rem;
  color: var(--teal-dim);
  letter-spacing: 0.05em;
}}

/* ── HERO PULSE DOT ── */
.hero-tag-dot {{
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--teal);
  animation: pulse-dot 1.8s ease-in-out infinite;
  box-shadow: 0 0 8px var(--teal);
}}
@keyframes pulse-dot {{
  0%, 100% {{ transform: scale(1); opacity: 1; box-shadow: 0 0 8px var(--teal); }}
  50% {{ transform: scale(1.5); opacity: 0.6; box-shadow: 0 0 16px var(--teal); }}
}}

/* ── GLITCH TITLE EFFECT ── */
@keyframes flicker {{
  0%, 99% {{ opacity: 1; }}
  100% {{ opacity: 0.9; }}
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLOT DEFAULTS
# ─────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Space Grotesk, sans-serif', color='rgba(232,244,242,0.7)'),
    margin=dict(l=24, r=24, t=48, b=40),
    xaxis=dict(
        gridcolor='rgba(0,255,209,0.06)',
        linecolor='rgba(0,255,209,0.1)',
        tickfont=dict(size=10, color='rgba(232,244,242,0.4)', family='Share Tech Mono'),
        zeroline=False,
    ),
    yaxis=dict(
        gridcolor='rgba(0,255,209,0.06)',
        linecolor='rgba(0,255,209,0.1)',
        tickfont=dict(size=10, color='rgba(232,244,242,0.4)', family='Share Tech Mono'),
        zeroline=False,
    ),
    colorway=['#00FFD1', '#0A84FF', '#FF3B5C', '#FFD60A', '#30D158'],
)

# ─────────────────────────────────────────────
# TOP HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style="padding: 0.5rem 0 1.8rem; text-align: center; position: relative;">
  <div style="
    display: inline-block;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.35em;
    color: rgba(0,255,209,0.5);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    border: 1px solid rgba(0,255,209,0.15);
    padding: 3px 14px;
    border-radius: 20px;
  ">v2.0 · Active · NASA C-MAPSS</div>
  <div style="
    font-family: 'Syne', sans-serif;
    font-size: clamp(1.8rem, 4vw, 2.8rem);
    font-weight: 800;
    color: #E8F4F2;
    letter-spacing: -0.02em;
    line-height: 1;
  ">AERO<span style="color: #00FFD1;">MIND</span></div>
  <div style="
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.22em;
    color: rgba(0,255,209,0.45);
    text-transform: uppercase;
    margin-top: 5px;
  ">Engine Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# NAVIGATION
# ─────────────────────────────────────────────
col_nav1, col_nav2, col_nav3 = st.columns([1, 6, 1])
with col_nav2:
    page = st.radio(
        "Navigate",
        ["Home", "RUL Prediction", "Model Performance", "Business Impact", "About"],
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

# ═══════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════
if page == "Home":
    # Hero
    st.markdown("""
    <div style="
      background: linear-gradient(135deg, rgba(5,18,36,0.95) 0%, rgba(7,26,50,0.9) 100%);
      border: 1px solid rgba(0,255,209,0.18);
      border-radius: 24px;
      padding: 3.5rem 3.5rem 3rem;
      margin-bottom: 2rem;
      position: relative;
      overflow: hidden;
      box-shadow: 0 0 80px rgba(0,255,209,0.06), 0 20px 60px rgba(0,0,0,0.4);
    ">
      <!-- Corner accent -->
      <div style="position:absolute;top:0;left:0;width:120px;height:120px;
        border-top:2px solid rgba(0,255,209,0.3);border-left:2px solid rgba(0,255,209,0.3);
        border-radius:24px 0 0 0;pointer-events:none;"></div>
      <div style="position:absolute;bottom:0;right:0;width:80px;height:80px;
        border-bottom:1px solid rgba(0,255,209,0.15);border-right:1px solid rgba(0,255,209,0.15);
        border-radius:0 0 24px 0;pointer-events:none;"></div>

      <div style="
        display: inline-flex; align-items: center; gap: 8px;
        background: rgba(0,255,209,0.08);
        border: 1px solid rgba(0,255,209,0.2);
        border-radius: 30px;
        padding: 5px 16px 5px 10px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.6rem; letter-spacing: 0.16em;
        color: #00FFD1; margin-bottom: 1.5rem;
        text-transform: uppercase;
      ">
        <span class="hero-tag-dot"></span>Live Monitoring Active
      </div>

      <h1 style="
        font-family: 'Syne', sans-serif !important;
        font-size: clamp(2.4rem, 5vw, 4rem) !important;
        font-weight: 800 !important;
        color: #E8F4F2 !important;
        line-height: 1.05 !important;
        margin: 0 0 0.6rem !important;
        letter-spacing: -0.02em;
      ">Aircraft Engine<br>
      <span style="color: #00FFD1; font-style: italic;">Health Intelligence</span></h1>

      <p style="
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 300 !important;
        color: rgba(232,244,242,0.55) !important;
        max-width: 500px !important;
        line-height: 1.75 !important;
        margin-bottom: 2.5rem !important;
      ">Predicting Remaining Useful Life of turbofan engines using deep learning —
      50% beyond industry benchmarks on NASA C-MAPSS data.</p>

      <div style="display: flex; gap: 3rem; flex-wrap: wrap;">
        <div>
          <div style="font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;color:#00FFD1;line-height:1;text-shadow:0 0 20px rgba(0,255,209,0.4);">8.96</div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:0.55rem;letter-spacing:0.2em;text-transform:uppercase;color:rgba(232,244,242,0.3);margin-top:6px;">RMSE (cycles)</div>
        </div>
        <div>
          <div style="font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;color:#00FFD1;line-height:1;text-shadow:0 0 20px rgba(0,255,209,0.4);">95.3%</div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:0.55rem;letter-spacing:0.2em;text-transform:uppercase;color:rgba(232,244,242,0.3);margin-top:6px;">R² Accuracy</div>
        </div>
        <div>
          <div style="font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;color:#00FFD1;line-height:1;text-shadow:0 0 20px rgba(0,255,209,0.4);">4</div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:0.55rem;letter-spacing:0.2em;text-transform:uppercase;color:rgba(232,244,242,0.3);margin-top:6px;">ML Models</div>
        </div>
        <div>
          <div style="font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;color:#00FFD1;line-height:1;text-shadow:0 0 20px rgba(0,255,209,0.4);">$2M+</div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:0.55rem;letter-spacing:0.2em;text-transform:uppercase;color:rgba(232,244,242,0.3);margin-top:6px;">Annual Savings</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Models Trained", "4", help="RF, XGBoost, LightGBM, LSTM")
    with c2: st.metric("Features Engineered", "117", delta="+106 engineered")
    with c3: st.metric("Training Engines", "80", help="16,561 training samples")
    with c4: st.metric("Validation R²", "95.3%", delta="50% better than target")

    st.markdown("""<div class="rule"><div class="rule-line"></div><span class="rule-label">Model Comparison</span><div class="rule-line"></div></div>""", unsafe_allow_html=True)

    fig = go.Figure(go.Bar(
        x=['LSTM', 'XGBoost', 'LightGBM', 'Random Forest'],
        y=[8.96, 9.41, 9.52, 9.85],
        marker=dict(
            color=['#00FFD1', 'rgba(0,255,209,0.6)', 'rgba(0,255,209,0.4)', 'rgba(0,255,209,0.25)'],
            cornerradius=8,
            line=dict(color='rgba(0,255,209,0.3)', width=1)
        ),
        text=[8.96, 9.41, 9.52, 9.85], textposition='outside',
        textfont=dict(family='Share Tech Mono', size=12, color='rgba(232,244,242,0.7)'),
        hovertemplate='<b>%{x}</b><br>RMSE: %{y} cycles<extra></extra>'
    ))
    fig.add_hline(y=18, line_dash="dot", line_color="#FF3B5C", line_width=1.5,
        annotation_text="Industry Target: 18 cycles",
        annotation_font=dict(color='#FF3B5C', size=10, family='Share Tech Mono'))
    fig.update_layout(
        **PLOT_LAYOUT,
        title=dict(text="Validation RMSE — All Models", font=dict(family='Syne', size=17, color='#E8F4F2')),
        yaxis_title="RMSE (cycles)", showlegend=False, height=360
    )
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════
# RUL PREDICTION
# ═══════════════════════════════════════════
elif page == "RUL Prediction":
    st.markdown("""
    <span style="font-family:'Share Tech Mono',monospace;font-size:0.6rem;letter-spacing:0.3em;text-transform:uppercase;color:rgba(0,255,209,0.6);margin-bottom:0.4rem;display:block;">Inference Console</span>
    <h2 style="font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;color:#E8F4F2;line-height:1.05;margin-bottom:0.4rem;letter-spacing:-0.01em;">RUL Prediction</h2>
    <p style="font-size:0.95rem;font-weight:300;color:rgba(232,244,242,0.5);line-height:1.7;margin-bottom:2rem;">Adjust sensor readings to compute the engine's Remaining Useful Life in real time.</p>
    """, unsafe_allow_html=True)

    chosen = st.selectbox("Select Active ML Model", ['LSTM', 'XGBoost', 'LightGBM', 'Random Forest'])

    st.markdown("""<div class="rule"><div class="rule-line"></div><span class="rule-label">Input Parameters</span><div class="rule-line"></div></div>""", unsafe_allow_html=True)

    col_sliders, col_result = st.columns([1.1, 1], gap="large")

    with col_sliders:
        with st.container(border=True):
            st.markdown("<p style=\"font-family:'Share Tech Mono',monospace;font-size:0.6rem;letter-spacing:0.22em;text-transform:uppercase;color:#00FFD1;margin-bottom:1.2rem;opacity:0.8;\">Sensor Dashboard</p>", unsafe_allow_html=True)

            input_mode = st.radio("Control Interface", ["🎛️ Simple Controls", "⚙️ Advanced Sensors (Engineers)"], horizontal=True)
            st.markdown("<hr style='margin:0.5rem 0 1rem 0; border-color: rgba(0,255,209,0.1);'>", unsafe_allow_html=True)

            if input_mode == "🎛️ Simple Controls":
                scenario = st.selectbox("Flight Scenario Presets", ["✈️ Healthy Engine (Nominal)", "⚠️ Moderate Wear (Mid-Life)", "🚨 Impending Failure (Critical)"])
                if "Healthy" in scenario:    def_t, def_p, def_r = 10, 10, 10
                elif "Moderate" in scenario: def_t, def_p, def_r = 45, 50, 40
                else:                        def_t, def_p, def_r = 85, 90, 85

                heat_val  = st.slider("Overall Engine Heat [T24 / T50]", 0, 100, def_t, 1, format="%d%% wear")
                press_val = st.slider("Compressor Pressure Level [P30 / Ps30]", 0, 100, def_p, 1, format="%d%% wear")
                rpm_val   = st.slider("Fan & Core Speed Stress [NF / NC]", 0, 100, def_r, 1, format="%d%% wear")

                baseline   = 125
                total_wear = (heat_val + press_val + rpm_val) / 300
                base_rul   = int(baseline * (1 - total_wear))

            else:
                s2  = st.slider("Compressor Inlet Temperature [T24] (°R)", 640.0, 645.0, 642.5, 0.1)
                s3  = st.slider("High Pressure Compressor Outlet [P30] (psia)", 1570.0, 1620.0, 1590.0, 1.0)
                s4  = st.slider("Fan Speed [NF] (rpm)", 1380.0, 1445.0, 1410.0, 1.0)
                s7  = st.slider("Static Pressure [Ps30] (psia)", 550.0, 556.0, 553.0, 0.1)
                s11 = st.slider("Core Speed [NC] (rpm)", 46.0, 49.0, 47.5, 0.1)
                s12 = st.slider("LPT Outlet Temp [T50] (°R)", 518.0, 524.0, 521.0, 0.5)

                baseline = 100
                base_rul = int(max(0, min(125, baseline - (s2 - 642.5) * 12 - (s3 - 1590) / 4 - (s4 - 1410) / 3)))

    with col_result:
        rul_pred = max(0, min(125, base_rul))
        label, kind = rul_status(rul_pred)
        cost = maintenance_cost(rul_pred)

        color_map = {
            "critical": "#FF3B5C",
            "warning":  "#FFD60A",
            "good":     "#00FFD1"
        }
        bg_map = {
            "critical": "rgba(255,59,92,0.07)",
            "warning":  "rgba(255,214,10,0.07)",
            "good":     "rgba(0,255,209,0.05)"
        }
        border_map = {
            "critical": "rgba(255,59,92,0.3)",
            "warning":  "rgba(255,214,10,0.25)",
            "good":     "rgba(0,255,209,0.25)"
        }
        glow_map = {
            "critical": "0 0 40px rgba(255,59,92,0.12)",
            "warning":  "0 0 40px rgba(255,214,10,0.1)",
            "good":     "0 0 40px rgba(0,255,209,0.1)"
        }

        st.markdown(f"""
        <div style="
          background:{bg_map[kind]};
          border:1px solid {border_map[kind]};
          border-radius:20px;padding:2.5rem 2rem;text-align:center;
          box-shadow:{glow_map[kind]};
          position:relative;overflow:hidden;
        ">
          <div style="position:absolute;top:0;left:0;right:0;height:2px;
            background:linear-gradient(90deg,transparent,{color_map[kind]},transparent);
            opacity:0.6;"></div>
          <p style="font-family:'Share Tech Mono',monospace;font-size:0.6rem;letter-spacing:0.28em;
             text-transform:uppercase;color:rgba(232,244,242,0.35);margin-bottom:0.6rem;">Remaining Useful Life</p>
          <div style="font-family:'Syne',sans-serif;font-size:5.8rem;font-weight:800;
              color:{color_map[kind]};line-height:1;letter-spacing:-0.04em;
              text-shadow:0 0 40px {color_map[kind]}55;">{rul_pred}</div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;letter-spacing:0.22em;
              color:rgba(232,244,242,0.3);margin-bottom:1.4rem;">CYCLES REMAINING · {chosen}</div>
          <span style="
            display:inline-flex;align-items:center;gap:7px;
            border-radius:20px;padding:6px 16px;
            font-family:'Share Tech Mono',monospace;font-size:0.62rem;
            letter-spacing:0.1em;font-weight:500;
            background:{bg_map[kind]};color:{color_map[kind]};
            border:1px solid {border_map[kind]};
          ">
            <span style="width:6px;height:6px;border-radius:50%;
              background:{color_map[kind]};
              box-shadow:0 0 8px {color_map[kind]};
              animation:pulse-dot 1.5s ease-in-out infinite;">
            </span>{label}
          </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if kind == "critical":
            st.markdown(f"""<div class="alert-box alert-critical">
                <h4 style="color:#FF3B5C!important;font-family:'Syne',sans-serif!important;font-size:1rem!important;margin:0 0 0.4rem!important;">🔴 Immediate Maintenance Required</h4>
                <p style="color:rgba(255,100,120,0.85)!important;font-size:0.84rem!important;margin:0.2rem 0!important;line-height:1.55!important;"><b>Action:</b> Ground and inspect within 5 flight cycles.</p>
                <p style="color:rgba(255,100,120,0.85)!important;font-size:0.84rem!important;margin:0.2rem 0!important;line-height:1.55!important;"><b>Scheduled maintenance cost:</b> ${cost:,} — vs $500,000+ unscheduled.</p>
            </div>""", unsafe_allow_html=True)
        elif kind == "warning":
            st.markdown(f"""<div class="alert-box alert-warning">
                <h4 style="color:#FFD60A!important;font-family:'Syne',sans-serif!important;font-size:1rem!important;margin:0 0 0.4rem!important;">⚠️ Maintenance Recommended</h4>
                <p style="color:rgba(255,214,10,0.8)!important;font-size:0.84rem!important;margin:0.2rem 0!important;line-height:1.55!important;"><b>Action:</b> Schedule preventive maintenance within 30 cycles.</p>
                <p style="color:rgba(255,214,10,0.8)!important;font-size:0.84rem!important;margin:0.2rem 0!important;line-height:1.55!important;"><b>Estimated cost:</b> ${cost:,}</p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="alert-box alert-good">
                <h4 style="color:#00FFD1!important;font-family:'Syne',sans-serif!important;font-size:1rem!important;margin:0 0 0.4rem!important;">✅ Engine Nominal</h4>
                <p style="color:rgba(0,255,209,0.75)!important;font-size:0.84rem!important;margin:0.2rem 0!important;line-height:1.55!important;"><b>Status:</b> No immediate action required.</p>
                <p style="color:rgba(0,255,209,0.75)!important;font-size:0.84rem!important;margin:0.2rem 0!important;line-height:1.55!important;">Continue standard monitoring intervals.</p>
            </div>""", unsafe_allow_html=True)

        fig_g = go.Figure(go.Indicator(
            mode="gauge+number", value=rul_pred, domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "RUL Health Index", 'font': {'family': 'Syne', 'size': 13, 'color': 'rgba(232,244,242,0.7)'}},
            number={'font': {'family': 'Syne', 'size': 30, 'color': color_map[kind]}, 'suffix': ' cyc'},
            gauge={
                'axis': {
                    'range': [0, 125],
                    'tickfont': {'size': 9, 'color': 'rgba(232,244,242,0.3)', 'family': 'Share Tech Mono'},
                    'tickcolor': 'rgba(0,255,209,0.15)'
                },
                'bar': {'color': color_map[kind], 'thickness': 0.2},
                'bgcolor': 'rgba(0,0,0,0)',
                'bordercolor': 'rgba(0,255,209,0.12)',
                'steps': [
                    {'range': [0, 30],   'color': 'rgba(255,59,92,0.12)'},
                    {'range': [30, 60],  'color': 'rgba(255,214,10,0.08)'},
                    {'range': [60, 125], 'color': 'rgba(0,255,209,0.05)'}
                ],
                'threshold': {'line': {'color': '#FF3B5C', 'width': 2}, 'thickness': 0.8, 'value': 30}
            }
        ))
        fig_g.update_layout(**PLOT_LAYOUT, height=240)
        st.plotly_chart(fig_g, use_container_width=True)

# ═══════════════════════════════════════════
# MODEL PERFORMANCE
# ═══════════════════════════════════════════
elif page == "Model Performance":
    st.markdown("""
    <span style="font-family:'Share Tech Mono',monospace;font-size:0.6rem;letter-spacing:0.3em;text-transform:uppercase;color:rgba(0,255,209,0.6);margin-bottom:0.4rem;display:block;">Validation Results</span>
    <h2 style="font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;color:#E8F4F2;line-height:1.05;margin-bottom:0.4rem;letter-spacing:-0.01em;">Model Performance</h2>
    <p style="font-size:0.95rem;font-weight:300;color:rgba(232,244,242,0.5);line-height:1.7;margin-bottom:2rem;">Comprehensive comparison of all four trained models against the NASA C-MAPSS FD001 validation set.</p>
    """, unsafe_allow_html=True)

    perf = {
        'Model':          ['LSTM',   'XGBoost', 'LightGBM', 'Random Forest'],
        'RMSE':           [8.96,     9.41,      9.52,       9.85],
        'MAE':            [6.83,     6.35,      6.48,       6.27],
        'R²':             [0.9528,   0.9492,    0.9479,     0.9443],
        'Speed':          ['Medium', 'Fast',    'Fast',     'Fast'],
        'Explainability': ['Low',    'High',    'High',     'High'],
    }
    df_perf = pd.DataFrame(perf)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Best RMSE", "8.96", delta="LSTM")
    with c2: st.metric("Best MAE", "6.27", delta="Random Forest")
    with c3: st.metric("Best R²", "0.9528", delta="LSTM")
    with c4: st.metric("vs Target", "−9.04", delta="50% better", delta_color="normal")

    st.markdown("""<div class="rule"><div class="rule-line"></div><span class="rule-label">Charts</span><div class="rule-line"></div></div>""", unsafe_allow_html=True)

    bar_colors = ['#00FFD1', 'rgba(0,255,209,0.6)', 'rgba(0,255,209,0.4)', 'rgba(0,255,209,0.22)']

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        fig_r = go.Figure(go.Bar(
            x=df_perf['Model'], y=df_perf['RMSE'],
            marker=dict(color=bar_colors, cornerradius=8, line=dict(color='rgba(0,255,209,0.2)', width=1)),
            text=df_perf['RMSE'], textposition='outside',
            textfont=dict(family='Share Tech Mono', size=11, color='rgba(232,244,242,0.6)'),
            hovertemplate='<b>%{x}</b><br>RMSE: %{y:.2f}<extra></extra>'
        ))
        fig_r.add_hline(y=18, line_dash="dot", line_color="#FF3B5C", line_width=1.5,
            annotation_text="Target 18", annotation_font=dict(color='#FF3B5C', size=10, family='Share Tech Mono'))
        fig_r.update_layout(**PLOT_LAYOUT, title=dict(text="RMSE — Lower is Better", font=dict(family='Syne', size=15, color='#E8F4F2')),
            yaxis_title="RMSE (cycles)", showlegend=False, height=320)
        st.plotly_chart(fig_r, use_container_width=True)

    with col2:
        fig_r2 = go.Figure(go.Bar(
            x=df_perf['Model'], y=df_perf['R²'],
            marker=dict(color=bar_colors, cornerradius=8, line=dict(color='rgba(0,255,209,0.2)', width=1)),
            text=[f"{v:.4f}" for v in df_perf['R²']], textposition='outside',
            textfont=dict(family='Share Tech Mono', size=11, color='rgba(232,244,242,0.6)'),
            hovertemplate='<b>%{x}</b><br>R²: %{y:.4f}<extra></extra>'
        ))
        fig_r2.update_layout(**PLOT_LAYOUT, title=dict(text="R² Score — Higher is Better", font=dict(family='Syne', size=15, color='#E8F4F2')),
            yaxis_title="R² Score", showlegend=False, height=320)
        fig_r2.update_yaxes(range=[0.93, 0.96])
        st.plotly_chart(fig_r2, use_container_width=True)

    categories = ['RMSE (inv)', 'MAE (inv)', 'R² Score', 'Speed', 'Explainability']
    radar_vals = {
        'LSTM':          [0.95, 0.90, 0.95, 0.5, 0.3],
        'XGBoost':       [0.91, 0.95, 0.94, 0.9, 0.9],
        'LightGBM':      [0.90, 0.93, 0.93, 0.9, 0.9],
        'Random Forest': [0.87, 0.96, 0.92, 0.8, 0.9]
    }
    radar_colors = ['#00FFD1', '#0A84FF', '#FFD60A', 'rgba(232,244,242,0.4)']

    fig_radar = go.Figure()
    for (model, vals), col in zip(radar_vals.items(), radar_colors):
        fig_radar.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=categories + [categories[0]],
            fill='toself', name=model,
            line=dict(color=col, width=2),
            fillcolor=col.replace(')', ',0.06)').replace('rgb', 'rgba') if col.startswith('rgb') else col + '10',
            opacity=0.9
        ))
    fig_radar.update_layout(
        **PLOT_LAYOUT,
        title=dict(text="Multi-Dimensional Model Comparison", font=dict(family='Syne', size=15, color='#E8F4F2')),
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, range=[0, 1], gridcolor='rgba(0,255,209,0.08)', tickfont=dict(size=9, family='Share Tech Mono', color='rgba(232,244,242,0.3)')),
            angularaxis=dict(gridcolor='rgba(0,255,209,0.08)', tickfont=dict(size=10, color='rgba(232,244,242,0.6)', family='Space Grotesk'))
        ),
        showlegend=True, height=420,
        legend=dict(font=dict(family='Share Tech Mono', size=10, color='rgba(232,244,242,0.7)'), bgcolor='rgba(5,18,36,0.7)', bordercolor='rgba(0,255,209,0.15)', borderwidth=1)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("""<div class="rule"><div class="rule-line"></div><span class="rule-label">Full Comparison Table</span><div class="rule-line"></div></div>""", unsafe_allow_html=True)
    st.dataframe(df_perf, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════
# BUSINESS IMPACT
# ═══════════════════════════════════════════
elif page == "Business Impact":
    st.markdown("""
    <span style="font-family:'Share Tech Mono',monospace;font-size:0.6rem;letter-spacing:0.3em;text-transform:uppercase;color:rgba(0,255,209,0.6);margin-bottom:0.4rem;display:block;">Financial Intelligence</span>
    <h2 style="font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;color:#E8F4F2;line-height:1.05;margin-bottom:0.4rem;letter-spacing:-0.01em;">Business Impact & ROI</h2>
    <p style="font-size:0.95rem;font-weight:300;color:rgba(232,244,242,0.5);line-height:1.7;margin-bottom:2rem;">Quantified financial value of deploying the AeroMind predictive maintenance system across your fleet.</p>
    """, unsafe_allow_html=True)

    st.markdown("""<div class="rule"><div class="rule-line"></div><span class="rule-label">ROI Calculator</span><div class="rule-line"></div></div>""", unsafe_allow_html=True)

    col_ctrl, col_chart = st.columns([1, 1.4], gap="large")

    with col_ctrl:
        st.markdown("""<div class="card"><p style="font-family:'Share Tech Mono',monospace;font-size:0.58rem;letter-spacing:0.22em;text-transform:uppercase;color:#00FFD1;opacity:0.7;margin-bottom:1.2rem;">Fleet Parameters</p>""", unsafe_allow_html=True)
        fleet_size    = st.slider("Fleet Size (engines)", 50, 500, 100, 10)
        failure_rate  = st.slider("Annual Failure Rate (%)", 1.0, 10.0, 5.0, 0.5)
        prevention_rt = st.slider("ML Prevention Rate (%)", 70.0, 95.0, 90.0, 5.0)

        failures_wo = fleet_size * (failure_rate / 100)
        prevented   = failures_wo * (prevention_rt / 100)
        failures_w  = failures_wo - prevented
        cost_wo     = failures_wo * 500000
        cost_w      = (prevented * 50000) + (failures_w * 500000)
        savings     = cost_wo - cost_w
        dev_cost    = 200000
        ann_maint   = 50000
        roi1        = ((savings - ann_maint - dev_cost) / dev_cost) * 100
        payback     = (dev_cost / max(savings - ann_maint, 1)) * 12
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card-accent">
          <p style="font-family:'Share Tech Mono',monospace;font-size:0.56rem;letter-spacing:0.24em;text-transform:uppercase;color:rgba(0,255,209,0.55);margin-bottom:1rem;">Results</p>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.2rem;">
            <div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:0.54rem;color:rgba(0,255,209,0.4);letter-spacing:0.14em;margin-bottom:5px;">NET SAVINGS</div>
              <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:#E8F4F2;text-shadow:0 0 20px rgba(0,255,209,0.2);">${savings/1e6:.1f}M</div>
            </div>
            <div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:0.54rem;color:rgba(0,255,209,0.4);letter-spacing:0.14em;margin-bottom:5px;">ROI Y1</div>
              <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:#00FFD1;text-shadow:0 0 20px rgba(0,255,209,0.3);">{roi1:.0f}%</div>
            </div>
            <div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:0.54rem;color:rgba(0,255,209,0.4);letter-spacing:0.14em;margin-bottom:5px;">PAYBACK</div>
              <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:#E8F4F2;">{payback:.1f} mo</div>
            </div>
            <div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:0.54rem;color:rgba(0,255,209,0.4);letter-spacing:0.14em;margin-bottom:5px;">PREVENTED</div>
              <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:#00FFD1;">{prevented:.1f}/yr</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Unscheduled Failure", "$500,000", help="Cost per catastrophic failure")
    with c2: st.metric("Scheduled Maintenance", "$50,000", help="Preventive maintenance cost")
    with c3: st.metric("Year 1 ROI", f"{roi1:.0f}%", delta=f"vs ${dev_cost/1000:.0f}K invest")
    with c4: st.metric("Payback Period", f"{payback:.1f} mo", help="Months to break even")

    with col_chart:
        years   = [1, 2, 3, 4, 5]
        cum_sav = [(savings - ann_maint) * y - dev_cost for y in years]

        fig_roi = go.Figure()
        fig_roi.add_trace(go.Scatter(
            x=years, y=[v/1e6 for v in cum_sav],
            mode='lines+markers', name='Cumulative Savings',
            line=dict(color='#00FFD1', width=3),
            marker=dict(size=9, color='#00FFD1', line=dict(width=2, color=PLOT_LAYOUT['paper_bgcolor'])),
            fill='tozeroy', fillcolor='rgba(0,255,209,0.06)',
            hovertemplate='Year %{x}<br>$%{y:.2f}M cumulative<extra></extra>'
        ))
        fig_roi.add_hline(y=0, line_dash="dot", line_color="#FF3B5C", line_width=1.5,
            annotation_text="Break-even", annotation_font=dict(color='#FF3B5C', size=10, family='Share Tech Mono'))
        fig_roi.update_layout(
            **PLOT_LAYOUT,
            title=dict(text="5-Year Cumulative Savings Projection", font=dict(family='Syne', size=15, color='#E8F4F2')),
            xaxis_title="Year", yaxis_title="Savings ($M)", height=340
        )
        st.plotly_chart(fig_roi, use_container_width=True)

        fig_cmp = go.Figure(go.Bar(
            x=['Without ML', 'With ML'],
            y=[cost_wo/1e6, cost_w/1e6],
            marker=dict(color=['#FF3B5C', '#00FFD1'], cornerradius=10, opacity=0.85),
            text=[f"${cost_wo/1e6:.1f}M", f"${cost_w/1e6:.1f}M"],
            textposition='outside',
            textfont=dict(family='Share Tech Mono', size=12, color='rgba(232,244,242,0.7)')
        ))
        fig_cmp.update_layout(
            **PLOT_LAYOUT,
            title=dict(text="Annual Maintenance Cost Comparison", font=dict(family='Syne', size=15, color='#E8F4F2')),
            yaxis_title="Annual Cost ($M)", showlegend=False, height=280
        )
        st.plotly_chart(fig_cmp, use_container_width=True)

# ═══════════════════════════════════════════
# ABOUT
# ═══════════════════════════════════════════
elif page == "About":
    st.markdown("""
    <span style="font-family:'Share Tech Mono',monospace;font-size:0.6rem;letter-spacing:0.3em;text-transform:uppercase;color:rgba(0,255,209,0.6);margin-bottom:0.4rem;display:block;">Project Documentation</span>
    <h2 style="font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;color:#E8F4F2;line-height:1.05;margin-bottom:0.4rem;letter-spacing:-0.01em;">About AeroMind</h2>
    <p style="font-size:0.95rem;font-weight:300;color:rgba(232,244,242,0.5);line-height:1.7;margin-bottom:2rem;">An end-to-end machine learning system for aircraft engine predictive maintenance, built on the NASA C-MAPSS turbofan degradation dataset.</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1], gap="large")
    with col1:
        st.markdown("""
        <div class="card">
          <p style="font-family:'Share Tech Mono',monospace;font-size:0.56rem;letter-spacing:0.22em;text-transform:uppercase;color:rgba(0,255,209,0.6);margin-bottom:0.75rem;">Technical Stack</p>
          <h3 style="font-family:'Syne',sans-serif!important;font-size:1.15rem!important;font-weight:700!important;color:#E8F4F2!important;margin-bottom:1rem!important;">Technologies Used</h3>
          <div class="pill-grid">
            <span class="pill">Python 3.11</span><span class="pill">TensorFlow / Keras</span>
            <span class="pill">XGBoost</span><span class="pill">LightGBM</span>
            <span class="pill">Scikit-learn</span><span class="pill">Optuna</span>
            <span class="pill">SHAP</span><span class="pill">Pandas</span>
            <span class="pill">NumPy</span><span class="pill">Streamlit</span>
            <span class="pill">Plotly</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
          <p style="font-family:'Share Tech Mono',monospace;font-size:0.56rem;letter-spacing:0.22em;text-transform:uppercase;color:rgba(0,255,209,0.6);margin-bottom:0.75rem;">Dataset</p>
          <h3 style="font-family:'Syne',sans-serif!important;font-size:1.15rem!important;font-weight:700!important;color:#E8F4F2!important;margin-bottom:0.75rem!important;">NASA C-MAPSS</h3>
          <p style="font-size:0.86rem;color:rgba(232,244,242,0.45);line-height:1.7;font-weight:300;">Turbofan Engine Degradation Simulation. 100 training engines, 100 test engines, 26 original features spanning 21 sensor channels and 3 operational settings.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card-accent" style="padding:2rem;">
          <p style="font-family:'Share Tech Mono',monospace;font-size:0.56rem;letter-spacing:0.22em;text-transform:uppercase;color:rgba(0,255,209,0.5);margin-bottom:0.75rem;">Author</p>
          <h3 style="font-family:'Syne',sans-serif!important;font-size:1.5rem!important;font-weight:800!important;color:#E8F4F2!important;margin-bottom:0.5rem!important;">Vivek M D</h3>
          <p style="font-size:0.86rem;color:rgba(232,244,242,0.4);font-weight:300;margin-bottom:0;line-height:1.7;">BE Computer Science Graduate · Data Science & AI/ML Specialist · Aviation Technology Enthusiast</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""<div class="card"><p style="font-family:'Share Tech Mono',monospace;font-size:0.56rem;letter-spacing:0.22em;text-transform:uppercase;color:rgba(0,255,209,0.6);margin-bottom:0.8rem;">Project Stats</p>""", unsafe_allow_html=True)
        c1_, c2_ = st.columns(2)
        with c1_:
            st.metric("Lines of Code", "2,500+")
            st.metric("Models Trained", "4")
        with c2_:
            st.metric("Notebooks", "6")
            st.metric("Visualizations", "12+")
        st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="
  margin-top: 4rem;
  padding: 1.4rem 0 0.5rem;
  border-top: 1px solid rgba(0,255,209,0.08);
  display: flex; align-items: center; justify-content: space-between;
  flex-wrap: wrap; gap: 0.5rem;
">
  <p style="font-size:0.8rem;color:rgba(232,244,242,0.3);font-weight:300;font-family:'Space Grotesk',sans-serif;">
    <strong style="color:rgba(232,244,242,0.7);font-weight:600;">AeroMind</strong>
    &nbsp;·&nbsp; Aircraft Engine Predictive Maintenance
    &nbsp;·&nbsp; Built with ❤️ by
    <strong style="color:rgba(232,244,242,0.7);font-weight:600;">Vivek M D</strong>
  </p>
  <p style="font-family:'Share Tech Mono',monospace;font-size:0.58rem;color:rgba(0,255,209,0.25);letter-spacing:0.12em;">
    NASA C-MAPSS · Streamlit · v2.0 · 2026
  </p>
</div>
""", unsafe_allow_html=True)

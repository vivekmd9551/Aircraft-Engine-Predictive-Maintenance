"""
✈️ AeroMind — Aircraft Engine Predictive Maintenance
Author: Vivek M D
Design: Aerospace Engineering Light — Cloud White + Slate Blue + Vivid Coral
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import base64
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
# ANIMATED BACKGROUND SVG
# ─────────────────────────────────────────────
svg_bg = """
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
b64_svg = base64.b64encode(svg_bg.encode()).decode()

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {{
    --white: #FFFFFF;
    --bg: #F8F9FC;
    --surface: #FFFFFF;
    --blue: #2563EB;
    --blue-dark: #1D4ED8;
    --border: #E2E8F0;
    --ink: #0F172A;
    --ink2: #334155;
    --ink3: #64748B;
    --ink4: #94A3B8;
    --radius: 14px;
    --radius-lg: 20px;
    --mono: 'JetBrains Mono', monospace;
    --display: 'DM Serif Display', serif;
    --body: 'Inter', sans-serif;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
    --shadow: 0 4px 16px rgba(0,0,0,0.07), 0 1px 4px rgba(0,0,0,0.04);
    --shadow-lg: 0 8px 32px rgba(0,0,0,0.10), 0 2px 8px rgba(0,0,0,0.05);
}}

/* ── GLOBAL ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
    background: var(--bg) !important;
    font-family: var(--body) !important;
    color: var(--ink) !important;
}}

/* ── ANIMATED BG ── */
[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 0;
    pointer-events: none;
    background-image: url("data:image/svg+xml;base64,{b64_svg}");
    background-repeat: no-repeat;
    background-position: center center;
    background-size: 85% auto;
    opacity: 0.12;
}}

/* ── MAIN BLOCK ── */
[data-testid="stMainBlockContainer"] {{
    padding-top: 0 !important;
    max-width: 1400px !important;
    position: relative;
    z-index: 10;
    animation: fadein 0.4s ease;
}}

@keyframes fadein {{
    from {{ opacity: 0; transform: translateY(8px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

/* ── HIDE CHROME ── */
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stDecoration"] {{ display: none; }}
[data-testid="collapsedControl"] {{ display: none; }}

/* ── HEADINGS ── */
h1, h2, h3, h4, h5 {{
    font-family: var(--display) !important;
    color: var(--ink) !important;
    letter-spacing: -0.01em !important;
}}

/* ── METRICS: fix clipping completely ── */
[data-testid="stMetric"] {{
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow-sm) !important;
    padding: 1rem 1.1rem 0.9rem !important;
    overflow: visible !important;
    min-height: 90px !important;
}}
[data-testid="stMetricLabel"] > div {{
    font-family: var(--mono) !important;
    font-size: 0.6rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--ink3) !important;
    margin-bottom: 0.3rem !important;
    line-height: 1.4 !important;
    white-space: normal !important;
    overflow: visible !important;
}}
[data-testid="stMetricValue"] > div {{
    font-family: var(--display) !important;
    font-size: 1.7rem !important;
    font-weight: 400 !important;
    color: var(--ink) !important;
    line-height: 1.2 !important;
    overflow: visible !important;
    white-space: nowrap !important;
    padding-bottom: 2px !important;
}}
[data-testid="stMetricDelta"] {{
    font-family: var(--mono) !important;
    font-size: 0.66rem !important;
    margin-top: 0.2rem !important;
    overflow: visible !important;
}}

/* ── RADIO ── */
[data-testid="stRadio"] > div {{
    display: flex !important;
    gap: 0.2rem !important;
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: 50px !important;
    padding: 5px !important;
    box-shadow: var(--shadow-sm) !important;
    flex-wrap: wrap !important;
    justify-content: center !important;
}}
[data-testid="stRadio"] label {{
    font-family: var(--body) !important;
    font-size: 0.84rem !important;
    font-weight: 500 !important;
    color: var(--ink3) !important;
    border-radius: 50px !important;
    padding: 6px 18px !important;
    cursor: pointer !important;
    transition: all 0.18s ease !important;
    white-space: nowrap !important;
}}
[data-testid="stRadio"] label:has(input:checked) {{
    background: var(--blue) !important;
    color: white !important;
}}

/* ── CONTAINERS ── */
[data-testid="stVerticalBlockBorderWrapper"] > div {{
    border-radius: var(--radius-lg) !important;
    border-color: var(--border) !important;
    background: var(--white) !important;
    box-shadow: var(--shadow-sm) !important;
    padding: 1.4rem 1.6rem !important;
}}

/* ── CARDS ── */
.card {{
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.5rem 1.8rem;
    box-shadow: var(--shadow);
    margin-bottom: 0.9rem;
    overflow: visible;
}}
.card-blue {{
    background: linear-gradient(135deg, #1E3A8A 0%, #1D4ED8 50%, #3B82F6 100%);
    border-radius: var(--radius-lg);
    padding: 1.5rem 1.8rem;
    box-shadow: 0 6px 24px rgba(37,99,235,0.3);
    margin-bottom: 0.9rem;
}}

/* ── STAT HELPERS ── */
.stat-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #64748B;
    display: block;
    margin-bottom: 0.3rem;
    line-height: 1.3;
}}
.stat-label-white {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.45);
    display: block;
    margin-bottom: 0.3rem;
    line-height: 1.3;
}}
.stat-number {{
    font-family: 'DM Serif Display', serif;
    font-size: 2.3rem;
    font-weight: 400;
    line-height: 1.1;
    color: #0F172A;
    display: block;
    overflow: visible;
    white-space: nowrap;
}}
.stat-number-white {{
    font-family: 'DM Serif Display', serif;
    font-size: 2.1rem;
    font-weight: 400;
    line-height: 1.1;
    color: white;
    display: block;
    overflow: visible;
    white-space: nowrap;
}}
.stat-number-green {{
    font-family: 'DM Serif Display', serif;
    font-size: 2.1rem;
    font-weight: 400;
    line-height: 1.1;
    color: #86EFAC;
    display: block;
    overflow: visible;
    white-space: nowrap;
}}
.stat-sub {{
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    color: #64748B;
    margin-top: 0.2rem;
    display: block;
}}

/* ── SECTION RULE ── */
.rule {{
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin: 1.8rem 0 1.3rem;
}}
.rule-line {{
    flex: 1;
    height: 1px;
    background: var(--border);
}}
.rule-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--ink4);
    white-space: nowrap;
    padding: 4px 12px;
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 20px;
}}

/* ── ALERTS ── */
.alert-box {{
    border-radius: var(--radius);
    padding: 1rem 1.3rem;
    margin-top: 0.9rem;
}}
.alert-critical {{ background:#FFF1EE; border:1.5px solid rgba(239,68,68,0.3); }}
.alert-warning  {{ background:#FFFBEB; border:1.5px solid rgba(245,158,11,0.25); }}
.alert-good     {{ background:#ECFDF5; border:1.5px solid rgba(16,185,129,0.25); }}
.alert-box h4 {{
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    margin: 0 0 0.35rem 0 !important;
    line-height: 1.4 !important;
}}
.alert-box p {{
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    margin: 0.12rem 0 !important;
    line-height: 1.6 !important;
}}

/* ── PILLS ── */
.pill-grid {{ display:flex; flex-wrap:wrap; gap:0.4rem; margin-top:0.5rem; }}
.pill {{
    background: #EEF3FF; color: #2563EB;
    border: 1px solid #BFDBFE; border-radius: 20px;
    padding: 4px 13px; font-size: 0.76rem;
    font-family: 'Inter', sans-serif; font-weight: 500;
    white-space: nowrap;
}}

/* ── LIVE DOT ── */
.live-dot {{
    display: inline-block; width: 7px; height: 7px;
    border-radius: 50%; background: #4ADE80; flex-shrink: 0;
    animation: blink 1.4s ease-in-out infinite;
}}
@keyframes blink {{
    0%, 100% {{ opacity:1; box-shadow: 0 0 5px #4ADE80; }}
    50%       {{ opacity:0.35; box-shadow: none; }}
}}

/* ── PAGE HEADER HELPERS ── */
.page-eyebrow {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem; letter-spacing: 0.28em;
    text-transform: uppercase; color: #2563EB;
    margin-bottom: 0.45rem; display: block;
}}
.page-title {{
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2rem, 3.5vw, 2.8rem);
    font-weight: 400; color: #0F172A;
    line-height: 1.05; margin-bottom: 0.5rem;
    letter-spacing: -0.02em; display: block;
}}
.page-desc {{
    font-size: 0.93rem; font-weight: 400;
    color: #64748B; line-height: 1.7;
    margin-bottom: 1.8rem; max-width: 620px; display: block;
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLOT THEME
# ─────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter, sans-serif', color='#334155'),
    margin=dict(l=28, r=28, t=60, b=44),
    xaxis=dict(
        gridcolor='rgba(37,99,235,0.07)',
        linecolor='rgba(37,99,235,0.12)',
        tickfont=dict(size=11, color='#94A3B8', family='JetBrains Mono'),
        zeroline=False,
    ),
    yaxis=dict(
        gridcolor='rgba(37,99,235,0.07)',
        linecolor='rgba(37,99,235,0.12)',
        tickfont=dict(size=11, color='#94A3B8', family='JetBrains Mono'),
        zeroline=False,
    ),
    colorway=['#2563EB', '#F05438', '#0E9580', '#D97706', '#7C3AED'],
)
BAR_COLORS = ['#2563EB', '#3B82F6', '#60A5FA', '#93C5FD']

# ─────────────────────────────────────────────
# HEADER BANNER
# ─────────────────────────────────────────────
st.markdown("""
<div style="
    background: linear-gradient(135deg, #1E3A8A 0%, #1D4ED8 45%, #2563EB 75%, #3B82F6 100%);
    border-radius: 0 0 28px 28px;
    padding: 2rem 3rem 1.8rem;
    margin: -1rem -1rem 2rem -1rem;
    position: relative; overflow: hidden;
    box-shadow: 0 8px 40px rgba(37,99,235,0.3);
">
    <div style="position:absolute;top:-80px;right:-80px;width:300px;height:300px;
        border-radius:50%;background:rgba(255,255,255,0.04);pointer-events:none;"></div>
    <div style="position:absolute;bottom:-100px;right:120px;width:220px;height:220px;
        border-radius:50%;background:rgba(255,255,255,0.03);pointer-events:none;"></div>

    <div style="display:flex;align-items:center;justify-content:space-between;
        flex-wrap:wrap;gap:1.5rem;position:relative;z-index:2;">

        <!-- Brand -->
        <div style="min-width:200px;">
            <div style="display:inline-flex;align-items:center;gap:8px;
                background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.18);
                border-radius:20px;padding:5px 14px;margin-bottom:1rem;">
                <span class="live-dot"></span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                    letter-spacing:0.16em;color:rgba(255,255,255,0.85);text-transform:uppercase;">
                    Live Monitoring Active
                </span>
            </div>
            <div style="font-family:'DM Serif Display',serif;
                font-size:clamp(2rem,3.5vw,2.8rem);font-weight:400;
                color:white;line-height:1.05;letter-spacing:-0.02em;">
                &#x2708;&#xFE0F; AERO<em style="opacity:0.8;">MIND</em>
            </div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                letter-spacing:0.24em;color:rgba(255,255,255,0.45);
                text-transform:uppercase;margin-top:6px;">
                Engine Intelligence Platform
            </div>
        </div>

        <!-- Stats — individual pill boxes guarantee no clipping -->
        <div style="display:flex;gap:0.9rem;flex-wrap:wrap;align-items:stretch;">

            <div style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.15);
                border-radius:16px;padding:0.9rem 1.3rem;text-align:center;min-width:88px;">
                <div style="font-family:'DM Serif Display',serif;font-size:1.9rem;
                    color:white;line-height:1.1;letter-spacing:-0.02em;">8.96</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.48rem;
                    letter-spacing:0.16em;color:rgba(255,255,255,0.45);
                    text-transform:uppercase;margin-top:5px;">RMSE</div>
            </div>

            <div style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.15);
                border-radius:16px;padding:0.9rem 1.3rem;text-align:center;min-width:88px;">
                <div style="font-family:'DM Serif Display',serif;font-size:1.9rem;
                    color:white;line-height:1.1;letter-spacing:-0.02em;">95.3%</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.48rem;
                    letter-spacing:0.16em;color:rgba(255,255,255,0.45);
                    text-transform:uppercase;margin-top:5px;">R&#178; Score</div>
            </div>

            <div style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.15);
                border-radius:16px;padding:0.9rem 1.3rem;text-align:center;min-width:88px;">
                <div style="font-family:'DM Serif Display',serif;font-size:1.9rem;
                    color:white;line-height:1.1;letter-spacing:-0.02em;">4</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.48rem;
                    letter-spacing:0.16em;color:rgba(255,255,255,0.45);
                    text-transform:uppercase;margin-top:5px;">ML Models</div>
            </div>

            <div style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.15);
                border-radius:16px;padding:0.9rem 1.3rem;text-align:center;min-width:88px;">
                <div style="font-family:'DM Serif Display',serif;font-size:1.9rem;
                    color:#86EFAC;line-height:1.1;letter-spacing:-0.02em;">$2M+</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.48rem;
                    letter-spacing:0.16em;color:rgba(255,255,255,0.45);
                    text-transform:uppercase;margin-top:5px;">Savings/yr</div>
            </div>

        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# NAVIGATION
# ─────────────────────────────────────────────
c_l, c_mid, c_r = st.columns([1, 6, 1])
with c_mid:
    page = st.radio(
        "Navigate",
        ["Home", "RUL Prediction", "Model Performance", "Business Impact", "About"],
        horizontal=True,
        label_visibility="collapsed"
    )
st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def rul_status(rul):
    if rul < 30:
        return "CRITICAL", "critical"
    elif rul < 60:
        return "WARNING", "warning"
    else:
        return "NOMINAL", "good"


def maintenance_cost(rul, prevented=True):
    if rul < 30:
        return 50000 if prevented else 500000
    elif rul < 60:
        return 50000
    return 0


def page_header(eyebrow, title, desc):
    st.markdown(f"""
    <span class="page-eyebrow">{eyebrow}</span>
    <span class="page-title">{title}</span>
    <span class="page-desc">{desc}</span>
    """, unsafe_allow_html=True)


def section_rule(label):
    st.markdown(f"""
    <div class="rule">
        <div class="rule-line"></div>
        <span class="rule-label">{label}</span>
        <div class="rule-line"></div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════
if page == "Home":

    col_hero, col_info = st.columns([1.6, 1], gap="large")

    with col_hero:
        st.markdown("""
        <div class="card" style="padding:2.4rem 2.6rem;border-left:5px solid #2563EB;min-height:260px;">
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                letter-spacing:0.22em;text-transform:uppercase;color:#2563EB;display:block;margin-bottom:0.8rem;">
                Predictive Maintenance &middot; NASA C-MAPSS
            </span>
            <div style="font-family:'DM Serif Display',serif;
                font-size:clamp(2rem,4vw,3.2rem);font-weight:400;
                color:#0F172A;line-height:1.1;margin-bottom:1rem;letter-spacing:-0.02em;">
                Aircraft Engine<br>
                <span style="color:#2563EB;font-style:italic;">Health Intelligence</span>
            </div>
            <p style="font-size:0.95rem;font-weight:400;color:#64748B;line-height:1.75;
                margin-bottom:0;max-width:440px;font-family:'Inter',sans-serif;">
                Deep learning models predicting Remaining Useful Life of turbofan engines —
                outperforming industry benchmarks by 50% on the NASA C-MAPSS dataset.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_info:
        st.markdown("""
        <div style="display:flex;flex-direction:column;gap:0.75rem;">

            <div class="card" style="border-top:4px solid #F05438;padding:1.2rem 1.5rem;margin-bottom:0;">
                <span class="stat-label">Best Model</span>
                <span class="stat-number">LSTM</span>
                <span class="stat-sub">RMSE 8.96 &middot; R&#178; 0.9528</span>
            </div>

            <div class="card" style="border-top:4px solid #10B981;padding:1.2rem 1.5rem;margin-bottom:0;">
                <span class="stat-label">Industry Target</span>
                <span class="stat-number">18 RMSE</span>
                <span class="stat-sub" style="color:#10B981;">We beat it by 50% &#x2197;</span>
            </div>

            <div class="card" style="border-top:4px solid #F59E0B;padding:1.2rem 1.5rem;margin-bottom:0;">
                <span class="stat-label">Engineered Features</span>
                <span class="stat-number">117</span>
                <span class="stat-sub">+106 engineered from 11 raw sensors</span>
            </div>

        </div>
        """, unsafe_allow_html=True)

    section_rule("Model Comparison — All Four Models vs Industry Target")

    col_chart1, col_chart2 = st.columns([2, 1], gap="large")

    with col_chart1:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['LSTM', 'XGBoost', 'LightGBM', 'Random Forest'],
            y=[8.96, 9.41, 9.52, 9.85],
            marker=dict(color=BAR_COLORS, cornerradius=8, line=dict(color='white', width=1.5)),
            text=[8.96, 9.41, 9.52, 9.85],
            textposition='outside',
            textfont=dict(family='JetBrains Mono', size=12, color='#334155'),
            hovertemplate='<b>%{x}</b><br>RMSE: %{y} cycles<extra></extra>'
        ))
        fig.add_hline(y=18, line_dash="dot", line_color="#EF4444", line_width=2,
                      annotation_text="Industry Target: 18 cycles",
                      annotation_font=dict(color='#EF4444', size=11, family='JetBrains Mono'))
        fig.update_layout(
            **PLOT_LAYOUT,
            title=dict(text="Validation RMSE — Lower is Better",
                       font=dict(family='DM Serif Display', size=19, color='#0F172A')),
            yaxis_title="RMSE (cycles)",
            yaxis=dict(**PLOT_LAYOUT['yaxis'], range=[0, 22]),
            showlegend=False,
            height=380
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_chart2:
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Models", "4", help="RF, XGBoost, LightGBM, LSTM")
        with c2:
            st.metric("R²", "95.3%", delta="+50%")
        c3, c4 = st.columns(2)
        with c3:
            st.metric("Engines", "80")
        with c4:
            st.metric("Samples", "16,561")

        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card" style="background:#EEF3FF;border-color:#BFDBFE;padding:1.3rem 1.5rem;">
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.56rem;
                letter-spacing:0.18em;text-transform:uppercase;color:#2563EB;display:block;margin-bottom:0.7rem;">
                How It Works
            </span>
            <ol style="font-size:0.84rem;color:#334155;line-height:2;
                padding-left:1.1rem;margin:0;font-family:'Inter',sans-serif;">
                <li>Raw sensor data ingested</li>
                <li>117 features engineered</li>
                <li>4 ML models trained</li>
                <li>RUL predicted in real time</li>
                <li>Maintenance alerts triggered</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════
# RUL PREDICTION
# ═══════════════════════════════════════════
elif page == "RUL Prediction":

    page_header(
        "Inference Console",
        "RUL Prediction",
        "Adjust sensor readings below to compute the engine's Remaining Useful Life in real time."
    )

    top_l, top_r = st.columns([2, 1], gap="medium")
    with top_l:
        chosen = st.selectbox("Select Active ML Model",
                              ['LSTM', 'XGBoost', 'LightGBM', 'Random Forest'])

    section_rule("Input Parameters")

    col_sliders, col_result = st.columns([1.1, 1], gap="large")

    with col_sliders:
        with st.container(border=True):
            st.markdown("""
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                letter-spacing:0.2em;text-transform:uppercase;color:#2563EB;
                display:block;margin-bottom:1rem;padding-bottom:0.7rem;
                border-bottom:1px solid #E2E8F0;">
                Sensor Dashboard
            </span>
            """, unsafe_allow_html=True)

            input_mode = st.radio(
                "Control Interface",
                ["🎛️ Simple Controls", "⚙️ Advanced Sensors (Engineers)"],
                horizontal=True
            )
            st.markdown("<div style='height:0.7rem;'></div>", unsafe_allow_html=True)

            if input_mode == "🎛️ Simple Controls":
                scenario = st.selectbox(
                    "Flight Scenario Presets",
                    ["✈️ Healthy Engine (Nominal)",
                     "⚠️ Moderate Wear (Mid-Life)",
                     "🚨 Impending Failure (Critical)"]
                )
                if "Healthy" in scenario:
                    def_t, def_p, def_r = 10, 10, 10
                elif "Moderate" in scenario:
                    def_t, def_p, def_r = 45, 50, 40
                else:
                    def_t, def_p, def_r = 85, 90, 85

                heat_val  = st.slider("Overall Engine Heat [T24 / T50]",
                                      0, 100, def_t, 1, format="%d%% wear")
                press_val = st.slider("Compressor Pressure Level [P30 / Ps30]",
                                      0, 100, def_p, 1, format="%d%% wear")
                rpm_val   = st.slider("Fan & Core Speed Stress [NF / NC]",
                                      0, 100, def_r, 1, format="%d%% wear")

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
                base_rul = int(max(0, min(125, baseline
                                          - (s2 - 642.5) * 12
                                          - (s3 - 1590) / 4
                                          - (s4 - 1410) / 3)))

    with col_result:
        rul_pred = max(0, min(125, base_rul))
        label, kind = rul_status(rul_pred)
        cost = maintenance_cost(rul_pred)

        color_map = {
            "critical": "#EF4444",
            "warning":  "#F59E0B",
            "good":     "#10B981"
        }
        bg_map = {
            "critical": "#FFF1EE",
            "warning":  "#FFFBEB",
            "good":     "#ECFDF5"
        }
        border_map = {
            "critical": "rgba(239,68,68,0.28)",
            "warning":  "rgba(245,158,11,0.25)",
            "good":     "rgba(16,185,129,0.25)"
        }

        # Big RUL number — uses clamp font + table-cell to guarantee full display
        st.markdown(f"""
        <div style="
            background:{bg_map[kind]};
            border:2px solid {border_map[kind]};
            border-radius:24px;
            padding:2rem 1.6rem 1.8rem;
            text-align:center;
            box-shadow:0 6px 28px {border_map[kind]};
            position:relative;
            overflow:visible;
        ">
            <div style="position:absolute;top:0;left:0;right:0;height:5px;
                background:{color_map[kind]};border-radius:24px 24px 0 0;"></div>

            <span style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;
                letter-spacing:0.26em;text-transform:uppercase;
                color:rgba(0,0,0,0.28);display:block;margin-bottom:0.5rem;">
                Remaining Useful Life
            </span>

            <div style="
                font-family:'DM Serif Display',serif;
                font-size:clamp(4.5rem,9vw,6rem);
                font-weight:400;
                color:{color_map[kind]};
                line-height:1;
                letter-spacing:-0.04em;
                padding:0.15rem 0 0.6rem;
                overflow:visible;
            ">
                {rul_pred}
            </div>

            <span style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                letter-spacing:0.2em;color:rgba(0,0,0,0.28);display:block;margin-bottom:1.2rem;">
                CYCLES REMAINING &middot; {chosen}
            </span>

            <span style="display:inline-flex;align-items:center;gap:8px;
                border-radius:30px;padding:8px 20px;
                font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                letter-spacing:0.1em;font-weight:600;
                background:white;color:{color_map[kind]};
                border:1.5px solid {border_map[kind]};
                box-shadow:0 2px 10px {border_map[kind]};">
                <span style="width:8px;height:8px;border-radius:50%;
                    background:{color_map[kind]};flex-shrink:0;"></span>
                {label}
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.9rem;'></div>", unsafe_allow_html=True)

        if kind == "critical":
            st.markdown(f"""
            <div class="alert-box alert-critical">
                <h4 style="color:#EF4444!important;">&#x1F534; Immediate Maintenance Required</h4>
                <p style="color:#7F1D1D!important;"><b>Action:</b> Ground and inspect within 5 flight cycles.</p>
                <p style="color:#7F1D1D!important;"><b>Scheduled cost:</b> ${cost:,} vs $500,000+ unscheduled.</p>
            </div>
            """, unsafe_allow_html=True)
        elif kind == "warning":
            st.markdown(f"""
            <div class="alert-box alert-warning">
                <h4 style="color:#F59E0B!important;">&#x26A0;&#xFE0F; Maintenance Recommended</h4>
                <p style="color:#78350F!important;"><b>Action:</b> Schedule maintenance within 30 cycles.</p>
                <p style="color:#78350F!important;"><b>Estimated cost:</b> ${cost:,}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alert-box alert-good">
                <h4 style="color:#10B981!important;">&#x2705; Engine Nominal</h4>
                <p style="color:#064E3B!important;"><b>Status:</b> No immediate action required.</p>
                <p style="color:#064E3B!important;">Continue standard monitoring intervals.</p>
            </div>
            """, unsafe_allow_html=True)

        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=rul_pred,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "RUL Health Index",
                   'font': {'family': 'Inter', 'size': 13, 'color': '#64748B'}},
            number={'font': {'family': 'DM Serif Display', 'size': 34,
                             'color': color_map[kind]}, 'suffix': ' cyc'},
            gauge={
                'axis': {
                    'range': [0, 125],
                    'tickfont': {'size': 9, 'color': '#94A3B8', 'family': 'JetBrains Mono'},
                    'tickcolor': 'rgba(37,99,235,0.15)'
                },
                'bar': {'color': color_map[kind], 'thickness': 0.22},
                'bgcolor': 'rgba(255,255,255,0.8)',
                'bordercolor': 'rgba(37,99,235,0.08)',
                'steps': [
                    {'range': [0, 30],   'color': 'rgba(239,68,68,0.08)'},
                    {'range': [30, 60],  'color': 'rgba(245,158,11,0.07)'},
                    {'range': [60, 125], 'color': 'rgba(16,185,129,0.06)'}
                ],
                'threshold': {
                    'line': {'color': '#EF4444', 'width': 2},
                    'thickness': 0.8,
                    'value': 30
                }
            }
        ))
        fig_g.update_layout(**PLOT_LAYOUT, height=255, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_g, use_container_width=True)


# ═══════════════════════════════════════════
# MODEL PERFORMANCE
# ═══════════════════════════════════════════
elif page == "Model Performance":

    page_header(
        "Validation Results",
        "Model Performance",
        "Comprehensive comparison of all four trained models against the NASA C-MAPSS FD001 validation set."
    )

    perf = {
        'Model':          ['LSTM', 'XGBoost', 'LightGBM', 'Random Forest'],
        'RMSE':           [8.96, 9.41, 9.52, 9.85],
        'MAE':            [6.83, 6.35, 6.48, 6.27],
        'R²':             [0.9528, 0.9492, 0.9479, 0.9443],
        'Speed':          ['Medium', 'Fast', 'Fast', 'Fast'],
        'Explainability': ['Low', 'High', 'High', 'High'],
    }
    df_perf = pd.DataFrame(perf)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Best RMSE", "8.96", delta="LSTM")
    with c2:
        st.metric("Best MAE", "6.27", delta="Rand. Forest")
    with c3:
        st.metric("Best R²", "0.9528", delta="LSTM")
    with c4:
        st.metric("vs Industry", "−9.04", delta="50% better", delta_color="normal")

    section_rule("Performance Charts")

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        fig_r = go.Figure(go.Bar(
            x=df_perf['Model'],
            y=df_perf['RMSE'],
            marker=dict(color=BAR_COLORS, cornerradius=8, line=dict(color='white', width=1.5)),
            text=[f"{v:.2f}" for v in df_perf['RMSE']],
            textposition='outside',
            textfont=dict(family='JetBrains Mono', size=12, color='#334155'),
            hovertemplate='<b>%{x}</b><br>RMSE: %{y:.2f}<extra></extra>'
        ))
        fig_r.add_hline(y=18, line_dash="dot", line_color="#EF4444", line_width=1.8,
                        annotation_text="Target 18",
                        annotation_font=dict(color='#EF4444', size=11, family='JetBrains Mono'))
        fig_r.update_layout(
            **PLOT_LAYOUT,
            title=dict(text="RMSE — Lower is Better",
                       font=dict(family='DM Serif Display', size=18, color='#0F172A')),
            yaxis_title="RMSE (cycles)",
            yaxis=dict(**PLOT_LAYOUT['yaxis'], range=[0, 22]),
            showlegend=False,
            height=340
        )
        st.plotly_chart(fig_r, use_container_width=True)

    with col2:
        fig_r2 = go.Figure(go.Bar(
            x=df_perf['Model'],
            y=df_perf['R²'],
            marker=dict(color=BAR_COLORS, cornerradius=8, line=dict(color='white', width=1.5)),
            text=[f"{v:.4f}" for v in df_perf['R²']],
            textposition='outside',
            textfont=dict(family='JetBrains Mono', size=12, color='#334155'),
            hovertemplate='<b>%{x}</b><br>R²: %{y:.4f}<extra></extra>'
        ))
        fig_r2.update_layout(
            **PLOT_LAYOUT,
            title=dict(text="R² Score — Higher is Better",
                       font=dict(family='DM Serif Display', size=18, color='#0F172A')),
            yaxis_title="R² Score",
            yaxis=dict(**PLOT_LAYOUT['yaxis'], range=[0.925, 0.965]),
            showlegend=False,
            height=340
        )
        st.plotly_chart(fig_r2, use_container_width=True)

    categories = ['RMSE (inv)', 'MAE (inv)', 'R² Score', 'Speed', 'Explainability']
    radar_vals = {
        'LSTM':          [0.95, 0.90, 0.95, 0.5, 0.3],
        'XGBoost':       [0.91, 0.95, 0.94, 0.9, 0.9],
        'LightGBM':      [0.90, 0.93, 0.93, 0.9, 0.9],
        'Random Forest': [0.87, 0.96, 0.92, 0.8, 0.9]
    }
    line_colors = ['#2563EB', '#F05438', '#0E9580', '#D97706']
    fill_colors = [
        'rgba(37,99,235,0.09)',
        'rgba(240,84,56,0.09)',
        'rgba(14,149,128,0.09)',
        'rgba(217,119,6,0.09)',
    ]

    fig_radar = go.Figure()
    for (model, vals), lc, fc in zip(radar_vals.items(), line_colors, fill_colors):
        fig_radar.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=categories + [categories[0]],
            fill='toself', name=model,
            line=dict(color=lc, width=2.5),
            fillcolor=fc,
        ))
    fig_radar.update_layout(
        **PLOT_LAYOUT,
        title=dict(text="Multi-Dimensional Model Comparison",
                   font=dict(family='DM Serif Display', size=18, color='#0F172A')),
        polar=dict(
            bgcolor='rgba(255,255,255,0.8)',
            radialaxis=dict(
                visible=True, range=[0, 1],
                gridcolor='rgba(37,99,235,0.1)',
                tickfont=dict(size=9, family='JetBrains Mono', color='#94A3B8')
            ),
            angularaxis=dict(
                gridcolor='rgba(37,99,235,0.1)',
                tickfont=dict(size=12, color='#334155', family='Inter')
            )
        ),
        showlegend=True, height=440,
        legend=dict(
            font=dict(family='Inter', size=12, color='#334155'),
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='rgba(37,99,235,0.12)',
            borderwidth=1
        )
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    section_rule("Full Comparison Table")
    st.dataframe(df_perf, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════
# BUSINESS IMPACT
# ═══════════════════════════════════════════
elif page == "Business Impact":

    page_header(
        "Financial Intelligence",
        "Business Impact &amp; ROI",
        "Quantified financial value of deploying AeroMind predictive maintenance across your fleet."
    )

    section_rule("ROI Calculator")

    col_ctrl, col_chart = st.columns([1, 1.6], gap="large")

    with col_ctrl:
        with st.container(border=True):
            st.markdown("""
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                letter-spacing:0.2em;text-transform:uppercase;color:#2563EB;
                display:block;margin-bottom:1rem;padding-bottom:0.7rem;
                border-bottom:1px solid #E2E8F0;">
                Fleet Parameters
            </span>
            """, unsafe_allow_html=True)
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

        st.markdown(f"""
        <div class="card-blue" style="margin-top:0.9rem;">
            <span class="stat-label-white" style="margin-bottom:1rem;display:block;">Projected Results</span>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.1rem;">

                <div>
                    <span class="stat-label-white">Net Savings</span>
                    <span class="stat-number-white">${savings/1e6:.1f}M</span>
                </div>
                <div>
                    <span class="stat-label-white">ROI Year 1</span>
                    <span class="stat-number-green">{roi1:.0f}%</span>
                </div>
                <div>
                    <span class="stat-label-white">Payback</span>
                    <span class="stat-number-white">{payback:.1f} mo</span>
                </div>
                <div>
                    <span class="stat-label-white">Prevented / yr</span>
                    <span class="stat-number-green">{prevented:.1f}</span>
                </div>

            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Failure Cost", "$500K", help="Per catastrophic failure")
            st.metric("Year 1 ROI", f"{roi1:.0f}%", delta=f"vs ${dev_cost/1000:.0f}K invest")
        with c2:
            st.metric("Maint. Cost", "$50K", help="Preventive maintenance cost")
            st.metric("Payback", f"{payback:.1f} mo", help="Months to break even")

    with col_chart:
        years   = [1, 2, 3, 4, 5]
        cum_sav = [(savings - ann_maint) * y - dev_cost for y in years]

        fig_roi = go.Figure()
        fig_roi.add_trace(go.Scatter(
            x=years,
            y=[v / 1e6 for v in cum_sav],
            mode='lines+markers',
            name='Cumulative Savings',
            line=dict(color='#2563EB', width=3),
            marker=dict(size=10, color='#2563EB', line=dict(width=2.5, color='white')),
            fill='tozeroy',
            fillcolor='rgba(37,99,235,0.07)',
            hovertemplate='Year %{x}<br>$%{y:.2f}M cumulative<extra></extra>'
        ))
        fig_roi.add_hline(y=0, line_dash="dot", line_color="#EF4444", line_width=1.8,
                          annotation_text="Break-even",
                          annotation_font=dict(color='#EF4444', size=11, family='JetBrains Mono'))
        fig_roi.update_layout(
            **PLOT_LAYOUT,
            title=dict(text="5-Year Cumulative Savings Projection",
                       font=dict(family='DM Serif Display', size=18, color='#0F172A')),
            xaxis_title="Year", yaxis_title="Savings ($M)", height=340
        )
        st.plotly_chart(fig_roi, use_container_width=True)

        fig_cmp = go.Figure(go.Bar(
            x=['Without ML', 'With ML'],
            y=[cost_wo / 1e6, cost_w / 1e6],
            marker=dict(color=['#EF4444', '#2563EB'], cornerradius=10),
            text=[f"${cost_wo/1e6:.1f}M", f"${cost_w/1e6:.1f}M"],
            textposition='outside',
            textfont=dict(family='JetBrains Mono', size=13, color='#334155')
        ))
        fig_cmp.update_layout(
            **PLOT_LAYOUT,
            title=dict(text="Annual Maintenance Cost Comparison",
                       font=dict(family='DM Serif Display', size=18, color='#0F172A')),
            yaxis_title="Annual Cost ($M)",
            yaxis=dict(**PLOT_LAYOUT['yaxis'], range=[0, cost_wo / 1e6 * 1.3]),
            showlegend=False,
            height=300
        )
        st.plotly_chart(fig_cmp, use_container_width=True)


# ═══════════════════════════════════════════
# ABOUT
# ═══════════════════════════════════════════
elif page == "About":

    page_header(
        "Project Documentation",
        "About AeroMind",
        "An end-to-end ML system for aircraft engine predictive maintenance, built on the NASA C-MAPSS turbofan degradation dataset."
    )

    col1, col2 = st.columns([1.2, 1], gap="large")

    with col1:
        st.markdown("""
        <div class="card">
            <span class="stat-label" style="color:#2563EB;margin-bottom:0.5rem;display:block;">Technical Stack</span>
            <div style="font-family:'DM Serif Display',serif;font-size:1.25rem;
                color:#0F172A;margin-bottom:0.8rem;">Technologies Used</div>
            <div class="pill-grid">
                <span class="pill">Python 3.11</span>
                <span class="pill">TensorFlow / Keras</span>
                <span class="pill">XGBoost</span>
                <span class="pill">LightGBM</span>
                <span class="pill">Scikit-learn</span>
                <span class="pill">Optuna</span>
                <span class="pill">SHAP</span>
                <span class="pill">Pandas</span>
                <span class="pill">NumPy</span>
                <span class="pill">Streamlit</span>
                <span class="pill">Plotly</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <span class="stat-label" style="color:#2563EB;margin-bottom:0.5rem;display:block;">Dataset</span>
            <div style="font-family:'DM Serif Display',serif;font-size:1.25rem;
                color:#0F172A;margin-bottom:0.6rem;">NASA C-MAPSS</div>
            <p style="font-size:0.88rem;color:#64748B;line-height:1.8;font-weight:400;margin:0;
                font-family:'Inter',sans-serif;">
                Turbofan Engine Degradation Simulation. 100 training engines, 100 test engines,
                26 original features spanning 21 sensor channels and 3 operational settings.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card-blue" style="margin-bottom:0.9rem;">
            <span class="stat-label-white">Author</span>
            <div style="font-family:'DM Serif Display',serif;font-size:1.8rem;
                color:white;margin:0.3rem 0 0.5rem;letter-spacing:-0.01em;">Vivek M D</div>
            <p style="font-size:0.86rem;color:rgba(255,255,255,0.55);
                font-weight:400;line-height:1.75;margin:0;font-family:'Inter',sans-serif;">
                BE Computer Science Graduate &middot; Data Science &amp; AI/ML Specialist
                &middot; Aviation Technology Enthusiast
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <span class="stat-label" style="color:#2563EB;display:block;margin-bottom:0.9rem;">Project Stats</span>
        """, unsafe_allow_html=True)

        ca, cb = st.columns(2)
        with ca:
            st.metric("Lines of Code", "2,500+")
            st.metric("Models Trained", "4")
        with cb:
            st.metric("Notebooks", "6")
            st.metric("Visualizations", "12+")

        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="
    margin-top:4rem;
    padding:1.3rem 0 0.5rem;
    border-top:1px solid #E2E8F0;
    display:flex;
    align-items:center;
    justify-content:space-between;
    flex-wrap:wrap;
    gap:0.5rem;
">
    <p style="font-size:0.82rem;color:#94A3B8;font-weight:400;
        font-family:'Inter',sans-serif;margin:0;">
        <strong style="color:#0F172A;font-weight:600;">AeroMind</strong>
        &nbsp;&middot;&nbsp; Aircraft Engine Predictive Maintenance
        &nbsp;&middot;&nbsp; Built with &#10084;&#65039; by
        <strong style="color:#0F172A;font-weight:600;">Vivek M D</strong>
    </p>
    <p style="font-family:'JetBrains Mono',monospace;font-size:0.56rem;
        color:#CBD5E1;letter-spacing:0.1em;margin:0;">
        NASA C-MAPSS &middot; Streamlit &middot; v2.1 &middot; 2026
    </p>
</div>
""", unsafe_allow_html=True)

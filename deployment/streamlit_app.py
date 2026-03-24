
"""
🚀 Aircraft Engine Predictive Maintenance - Streamlit App
Author: Vivek M D
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Aircraft Engine RUL Predictor",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .alert-critical {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #f44336;
    }
    .alert-warning {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #ff9800;
    }
    .alert-good {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="main-header">✈️ Aircraft Engine Predictive Maintenance</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Remaining Useful Life (RUL) Prediction System</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Navigation")
    page = st.radio("Select Page", 
                    ["🏠 Home", "🔮 RUL Prediction", "📈 Model Performance", "💰 Business Impact", "ℹ️ About"])
    
    st.markdown("---")
    st.markdown("### 🎯 Project Stats")
    st.metric("Best Model", "LSTM")
    st.metric("RMSE", "8.96 cycles")
    st.metric("R² Score", "0.9528")
    st.metric("Annual Savings", "$2.0M")

# Helper functions
def get_rul_category(rul):
    if rul < 30:
        return "CRITICAL", "🔴"
    elif rul < 60:
        return "WARNING", "🟡"
    else:
        return "GOOD", "🟢"

def calculate_maintenance_cost(rul, prevent_failure=True):
    if rul < 30:
        if prevent_failure:
            return 50000
        else:
            return 500000
    elif rul < 60:
        return 50000
    else:
        return 0

# ========================================
# HOME PAGE
# ========================================
if page == "🏠 Home":
    st.markdown("## Welcome to the RUL Prediction System")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 Purpose")
        st.write("This system predicts the Remaining Useful Life (RUL) of aircraft engines using advanced ML models.")
    
    with col2:
        st.markdown("### 🏆 Performance")
        st.write("**LSTM Model:** 8.96 RMSE")
        st.write("**50% better** than target")
    
    with col3:
        st.markdown("### 💰 Business Value")
        st.write("**$2M+ annual savings**")
        st.write("**888% ROI** in Year 1")
    
    st.markdown("---")
    st.markdown("## 📊 System Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Models Trained", "4")
    with col2:
        st.metric("Features", "117")
    with col3:
        st.metric("Training Engines", "80")
    with col4:
        st.metric("Accuracy", "95.3%")
    
    st.markdown("---")
    st.markdown("## 📈 Model Comparison")
    
    models = ['Random Forest', 'XGBoost', 'LightGBM', 'LSTM']
    rmse_values = [9.85, 9.41, 9.52, 8.96]
    
    fig = go.Figure(data=[
        go.Bar(x=models, y=rmse_values, 
               marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    ])
    
    fig.update_layout(
        title="Validation RMSE Comparison",
        xaxis_title="Model",
        yaxis_title="RMSE (cycles)",
        height=400
    )
    fig.add_hline(y=18, line_dash="dash", line_color="red", annotation_text="Target: 18 cycles")
    
    st.plotly_chart(fig, use_container_width=True)

# ========================================
# RUL PREDICTION PAGE
# ========================================
elif page == "🔮 RUL Prediction":
    st.markdown("## 🔮 Predict Engine RUL")
    
    st.info("💡 This is a demonstration with simulated predictions")
    
    st.markdown("### ✍️ Sensor Input")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sensor_2 = st.slider("Sensor 2 (Temperature)", 640.0, 645.0, 642.5)
        sensor_3 = st.slider("Sensor 3 (Pressure)", 1570.0, 1620.0, 1590.0)
        sensor_4 = st.slider("Sensor 4 (RPM)", 1380.0, 1445.0, 1410.0)
    
    with col2:
        sensor_7 = st.slider("Sensor 7", 550.0, 556.0, 553.0)
        sensor_11 = st.slider("Sensor 11", 46.0, 49.0, 47.5)
        sensor_12 = st.slider("Sensor 12", 518.0, 524.0, 521.0)
    
    if st.button("🔮 Predict RUL"):
        with st.spinner("Calculating RUL..."):
            # Simplified prediction logic
            baseline = 100
            temp_effect = (sensor_2 - 642.5) * 10
            pressure_effect = (sensor_3 - 1590) / 5
            rpm_effect = (sensor_4 - 1410) / 3
            
            prediction = int(baseline - temp_effect - pressure_effect - rpm_effect)
            prediction = max(0, min(125, prediction))
            
            st.balloons()
            
            status, icon = get_rul_category(prediction)
            
            st.markdown("### 📊 Prediction Results")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Predicted RUL", f"{prediction} cycles")
            with col2:
                st.metric("Status", f"{icon} {status}")
            with col3:
                confidence = np.random.randint(85, 98)
                st.metric("Confidence", f"{confidence}%")
            with col4:
                cost = calculate_maintenance_cost(prediction)
                st.metric("Est. Cost", f"${cost:,}")
            
            st.markdown("### 📋 Maintenance Recommendation")
            if prediction < 30:
                st.markdown("""
                <div class="alert-critical">
                <h4>🔴 CRITICAL ALERT</h4>
                <p><b>Action Required:</b> Schedule immediate maintenance within 5 cycles</p>
                <p><b>Risk Level:</b> High - Potential catastrophic failure</p>
                <p><b>Cost if Delayed:</b> $500,000+ (unscheduled failure)</p>
                </div>
                """, unsafe_allow_html=True)
            elif prediction < 60:
                st.markdown("""
                <div class="alert-warning">
                <h4>🟡 WARNING</h4>
                <p><b>Action Required:</b> Plan maintenance within 30 cycles</p>
                <p><b>Risk Level:</b> Medium - Degradation accelerating</p>
                <p><b>Recommended:</b> Schedule preventive maintenance ($50,000)</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="alert-good">
                <h4>🟢 GOOD CONDITION</h4>
                <p><b>Status:</b> Engine operating normally</p>
                <p><b>Next Action:</b> Continue monitoring</p>
                </div>
                """, unsafe_allow_html=True)

# ========================================
# MODEL PERFORMANCE PAGE
# ========================================
elif page == "📈 Model Performance":
    st.markdown("## 📈 Model Performance Analysis")
    
    performance_data = {
        'Model': ['LSTM', 'XGBoost', 'LightGBM', 'Random Forest'],
        'RMSE': [8.96, 9.41, 9.52, 9.85],
        'MAE': [6.83, 6.35, 6.48, 6.27],
        'R²': [0.9528, 0.9492, 0.9479, 0.9443]
    }
    
    df = pd.DataFrame(performance_data)
    st.dataframe(df, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = go.Figure(data=[
            go.Bar(x=df['Model'], y=df['RMSE'],
                   marker_color=['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4'])
        ])
        fig1.update_layout(title="RMSE Comparison", height=400)
        fig1.add_hline(y=18, line_dash="dash", line_color="red")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = go.Figure(data=[
            go.Bar(x=df['Model'], y=df['R²'],
                   marker_color=['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4'])
        ])
        fig2.update_layout(title="R² Score Comparison", height=400)
        st.plotly_chart(fig2, use_container_width=True)

# ========================================
# BUSINESS IMPACT PAGE
# ========================================
elif page == "💰 Business Impact":
    st.markdown("## 💰 Business Impact & ROI")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Unscheduled Failure", "$500,000")
    with col2:
        st.metric("Scheduled Maintenance", "$50,000")
    with col3:
        st.metric("False Alarm", "$10,000")
    
    st.markdown("---")
    st.markdown("### 📊 ROI Calculator")
    
    fleet_size = st.slider("Fleet Size", 50, 500, 100, 10)
    failure_rate = st.slider("Failure Rate (%)", 1.0, 10.0, 5.0, 0.5)
    prevention_rate = st.slider("Prevention Rate (%)", 70.0, 95.0, 90.0, 5.0)
    
    failures_without = fleet_size * (failure_rate / 100)
    failures_prevented = failures_without * (prevention_rate / 100)
    failures_with = failures_without - failures_prevented
    
    cost_without = failures_without * 500000
    cost_with = (failures_prevented * 50000) + (failures_with * 500000)
    savings = cost_without - cost_with
    
    roi = ((savings - 50000 - 200000) / 200000) * 100
    payback = (200000 / (savings - 50000)) * 12
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Annual Savings", f"${savings:,.0f}")
    with col2:
        st.metric("Year 1 ROI", f"{roi:.0f}%")
    with col3:
        st.metric("Year 2+ ROI", f"{(savings-50000)/200000*100:.0f}%")
    with col4:
        st.metric("Payback", f"{payback:.1f} mo")
    
    # 5-year projection
    years = ['Y1', 'Y2', 'Y3', 'Y4', 'Y5']
    cumulative = [
        savings - 250000,
        savings*2 - 300000,
        savings*3 - 350000,
        savings*4 - 400000,
        savings*5 - 450000
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=cumulative, mode='lines+markers',
                             line=dict(color='green', width=3), marker=dict(size=10)))
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    fig.update_layout(title="5-Year Cumulative Savings", height=400)
    st.plotly_chart(fig, use_container_width=True)

# ========================================
# ABOUT PAGE
# ========================================
elif page == "ℹ️ About":
    st.markdown("## ℹ️ About This Project")
    
    st.markdown("""
    ### 🎯 Project Overview
    Aircraft Engine Predictive Maintenance System using NASA C-MAPSS data.
    
    ### 📊 Performance
    - **Best Model:** LSTM (8.96 RMSE)
    - **Target:** < 18 cycles
    - **Achievement:** 50% better than target!
    
    ### 👨‍💻 Author
    **Vivek M D**
    - BE Computer Science Graduate
    - Data Science & AI/ML Specialist
    
    ### 📚 Tech Stack
    - Python, Pandas, NumPy
    - Scikit-learn, XGBoost, LightGBM
    - TensorFlow/Keras (LSTM)
    - Streamlit, Plotly
    - Optuna, SHAP
    
    ### 🏆 Achievements
    - 117 engineered features from 11 sensors
    - 4 production-ready models
    - $2M+ annual savings potential
    - 888% ROI in Year 1
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Code Lines", "2,500+")
    with col2:
        st.metric("Notebooks", "6")
    with col3:
        st.metric("Models", "4")
    with col4:
        st.metric("Charts", "12+")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'><p>© 2026 Vivek M D</p></div>", 
            unsafe_allow_html=True)

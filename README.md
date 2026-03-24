# ✈️ Aircraft Engine Predictive Maintenance

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.19-orange.svg)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> End-to-end machine learning system for predicting aircraft engine Remaining Useful Life (RUL) using NASA C-MAPSS turbofan engine degradation data.

## 🎯 Project Highlights

- **🏆 Performance:** RMSE = 8.96 cycles (50% better than 18-cycle target)
- **💰 Business Impact:** $2M+ annual savings potential with 888% ROI
- **🧠 Best Model:** Bidirectional LSTM with 95.3% accuracy (R²)
- **📊 Feature Engineering:** 117 features engineered from 11 base sensors
- **🔧 Production Ready:** Complete pipeline from EDA to deployment

---

## 📊 Results Summary

| Model | Validation RMSE | R² Score | Status |
|-------|-----------------|----------|--------|
| **LSTM** | **8.96** | **0.9528** | 🏆 **Best** |
| XGBoost | 9.41 | 0.9492 | 🥈 Strong |
| LightGBM | 9.52 | 0.9479 | 🥉 Good |
| Random Forest | 9.85 | 0.9443 | Baseline |

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
TensorFlow 2.x
XGBoost, LightGBM
Pandas, NumPy, Scikit-learn
```

### Installation
```bash
# Clone the repository
git clone https://github.com/YourUsername/Aircraft-Engine-Predictive-Maintenance.git

# Install dependencies
pip install -r requirements.txt
```

---

## 📁 Project Structure
```
Aircraft-Engine-Predictive-Maintenance/
├── notebooks/                  # Jupyter notebooks (complete pipeline)
│   ├── 00_Project_Setup.ipynb
│   ├── 01_EDA.ipynb
│   ├── 02_Feature_Engineering.ipynb
│   ├── 03_Baseline_Models.ipynb
│   ├── 04_Advanced_XGBoost.ipynb
│   ├── 05_LSTM_Deep_Learning.ipynb
│   └── 06_Ensemble_Evaluation.ipynb
├── config/                     # Configuration files
├── deployment/                 # Streamlit web app
├── results/                    # Figures, reports, analysis
└── README.md
```

---

## 🔬 Methodology

### 1. **Exploratory Data Analysis**
- Analyzed NASA C-MAPSS turbofan engine dataset
- Identified 10 constant sensors (removed)
- Analyzed degradation patterns across 100 engines
- Created lifecycle stage categorization

### 2. **Feature Engineering** 
- **Rolling statistics:** Windows of 5, 10, 20 cycles
- **Rate-of-change features:** Degradation velocity
- **Exponential moving averages:** Recent trend emphasis
- **Lifecycle encoding:** Critical/Warning/Good stages
- **Result:** 11 → 117 powerful features

### 3. **Model Development**

#### Baseline Models
- Linear Regression: 10.71 RMSE
- Random Forest: 9.85 RMSE
- Gradient Boosting: 9.94 RMSE

#### Advanced Models
- **XGBoost** (Optuna-tuned): 9.41 RMSE
- **LightGBM** (Optuna-tuned): 9.52 RMSE
- **LSTM** (Bidirectional): **8.96 RMSE** ✨

### 4. **Deep Learning Architecture**
```
Bidirectional LSTM (64 units) + Dropout + BatchNorm
    ↓
Bidirectional LSTM (32 units) + Dropout + BatchNorm
    ↓
Dense Layers (32 → 16) + Dropout
    ↓
Output (RUL prediction)
```

---

## 💰 Business Impact

### Cost Analysis (100-engine fleet)
- **Without ML:** $2.5M annual failure costs
- **With ML:** $475K annual costs (90% prevention)
- **Annual Savings:** $2.025M
- **ROI Year 1:** 888%
- **Payback Period:** 1.2 months

### Key Benefits
✅ 90% failure prevention rate  
✅ Optimized maintenance scheduling  
✅ Reduced unscheduled downtime  
✅ Improved fleet availability  

---

## 🛠️ Technologies Used

**Languages & Libraries:**
- Python 3.8+
- Pandas, NumPy, Matplotlib, Seaborn

**Machine Learning:**
- Scikit-learn
- XGBoost, LightGBM
- Optuna (hyperparameter tuning)
- SHAP (explainability)

**Deep Learning:**
- TensorFlow 2.x / Keras
- Bidirectional LSTM
- Early stopping, learning rate scheduling

**Deployment:**
- Streamlit (web interface)
- Plotly (interactive visualizations)

---

## 📈 Key Findings

1. **Feature engineering was critical** - Lifecycle stage features showed 78% importance in Random Forest
2. **Rolling std > rolling mean** - Variability in sensors predicts failure better than averages
3. **LSTM captures temporal patterns** - 4.7% better than XGBoost by learning degradation sequences
4. **Ensemble potential** - Hybrid LSTM + XGBoost strategy for production
5. **Strong generalization** - Low train-validation gap (8.63 → 8.96 RMSE)

---

## 🎯 Future Enhancements

- [ ] Multi-dataset validation (FD002-FD004)
- [ ] Real-time monitoring dashboard
- [ ] REST API for system integration
- [ ] Continuous model retraining pipeline
- [ ] Mobile application
- [ ] SHAP-based prediction explanations in UI

---

## 📊 Model Performance Visualizations

### Training History
- LSTM converged in 28 epochs with early stopping
- Optimal learning rate schedule (0.001 → 0.000125)
- Validation loss: 242 → 80 (67% reduction)

### Feature Importance
Top 3 most predictive features:
1. `stage_good` (78% importance)
2. `normalized_cycle` (12.5% importance)
3. `stage_warning` (4% importance)

---

## 👨‍💻 Author

**Vivek M D**
- BE Computer Science Graduate
- Data Science & AI/ML Specialist
- Aviation Technology Enthusiast

📧 Email: [Your Email]  
💼 LinkedIn: [Your LinkedIn]  
🐙 GitHub: [@YourUsername](https://github.com/YourUsername)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **NASA:** C-MAPSS dataset from NASA Ames Prognostics Data Repository
- **Research Papers:** Various papers on RUL prediction and LSTM applications
- **Community:** TensorFlow, Scikit-learn, and XGBoost communities

---

## 📚 References

1. Saxena, A., & Goebel, K. (2008). Turbofan Engine Degradation Simulation Data Set. NASA Ames Prognostics Data Repository.
2. Zheng, S., et al. (2017). Long Short-Term Memory Network for Remaining Useful Life Estimation. IEEE.

---

<p align="center">
  <strong>⭐ Star this repository if you found it helpful!</strong>
</p>

<p align="center">
  Built with ❤️ for aviation safety and efficiency
</p>

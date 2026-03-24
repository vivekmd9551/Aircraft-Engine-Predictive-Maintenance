"""
Project Configuration File
Aircraft Engine Predictive Maintenance

This file contains all project settings, paths, and hyperparameters.
Industry best practice: Never hardcode values in notebooks!
"""

import os

# ============================================================================
# PROJECT PATHS
# ============================================================================
PROJECT_ROOT = '/content/drive/MyDrive/Aircraft_Engine_Predictive_Maintenance'

# Data paths
DATA_RAW = os.path.join(PROJECT_ROOT, 'data/raw')
DATA_PROCESSED = os.path.join(PROJECT_ROOT, 'data/processed')
DATA_PREDICTIONS = os.path.join(PROJECT_ROOT, 'data/predictions')

# Model paths
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')

# Results paths
RESULTS_FIGURES = os.path.join(PROJECT_ROOT, 'results/figures')
RESULTS_REPORTS = os.path.join(PROJECT_ROOT, 'results/reports')
RESULTS_LOGS = os.path.join(PROJECT_ROOT, 'results/logs')

# ============================================================================
# DATASET CONFIGURATION
# ============================================================================

# Column names for the dataset (26 columns total)
COLUMN_NAMES = [
    'unit_id',           # Engine unit number
    'time_cycles',       # Operational cycle number
    'setting_1',         # Operational setting 1
    'setting_2',         # Operational setting 2  
    'setting_3',         # Operational setting 3
    'sensor_1',  'sensor_2',  'sensor_3',  'sensor_4',  'sensor_5',
    'sensor_6',  'sensor_7',  'sensor_8',  'sensor_9',  'sensor_10',
    'sensor_11', 'sensor_12', 'sensor_13', 'sensor_14', 'sensor_15',
    'sensor_16', 'sensor_17', 'sensor_18', 'sensor_19', 'sensor_20',
    'sensor_21'
]

# Dataset characteristics
DATASETS = {
    'FD001': {
        'train_engines': 100,
        'test_engines': 100,
        'conditions': 1,
        'fault_modes': 1,
        'description': 'Sea Level - HPC Degradation'
    },
    'FD002': {
        'train_engines': 260,
        'test_engines': 259,
        'conditions': 6,
        'fault_modes': 1,
        'description': 'Six Conditions - HPC Degradation'
    },
    'FD003': {
        'train_engines': 100,
        'test_engines': 100,
        'conditions': 1,
        'fault_modes': 2,
        'description': 'Sea Level - HPC & Fan Degradation'
    },
    'FD004': {
        'train_engines': 248,
        'test_engines': 249,
        'conditions': 6,
        'fault_modes': 2,
        'description': 'Six Conditions - HPC & Fan Degradation'
    }
}

# ============================================================================
# DATA PREPROCESSING
# ============================================================================

# Random seed for reproducibility
RANDOM_SEED = 42

# Train/Validation split ratio
VALIDATION_SPLIT = 0.2

# RUL (Remaining Useful Life) configuration
MAX_RUL = 125  # Piecewise linear degradation - cap RUL at 125 cycles

# Feature engineering parameters
ROLLING_WINDOW_SIZES = [5, 10, 20]  # For rolling mean/std features

# ============================================================================
# MODEL HYPERPARAMETERS
# ============================================================================

# Random Forest
RF_PARAMS = {
    'n_estimators': 100,
    'max_depth': 20,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'random_state': RANDOM_SEED,
    'n_jobs': -1
}

# XGBoost
XGB_PARAMS = {
    'n_estimators': 200,
    'max_depth': 6,
    'learning_rate': 0.05,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'random_state': RANDOM_SEED,
    'n_jobs': -1,
    'objective': 'reg:squarederror'
}

# LightGBM
LGBM_PARAMS = {
    'n_estimators': 200,
    'max_depth': 6,
    'learning_rate': 0.05,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'random_state': RANDOM_SEED,
    'n_jobs': -1,
    'verbose': -1
}

# LSTM Deep Learning
LSTM_PARAMS = {
    'sequence_length': 50,      # Use last 50 cycles to predict RUL
    'lstm_units': [50, 50],     # Two LSTM layers with 50 units each
    'dropout': 0.2,
    'batch_size': 32,
    'epochs': 100,
    'learning_rate': 0.001,
    'early_stopping_patience': 10
}

# ============================================================================
# EVALUATION METRICS
# ============================================================================

# Target metrics
TARGET_RMSE = 18.0  # Target Root Mean Squared Error
TARGET_R2 = 0.85    # Target R-squared score

# Early warning classification thresholds
RUL_THRESHOLDS = {
    'critical': 30,   # RUL < 30 cycles -> Critical (immediate maintenance)
    'warning': 60     # 30 <= RUL < 60 -> Warning (schedule maintenance)
                       # RUL >= 60 -> Good (normal operation)
}

# ============================================================================
# VISUALIZATION SETTINGS
# ============================================================================

# Figure size and DPI
FIGURE_SIZE = (12, 6)
FIGURE_DPI = 100

# Color palette
COLORS = {
    'critical': '#d32f2f',   # Red
    'warning': '#f57c00',    # Orange
    'good': '#388e3c',       # Green
    'primary': '#1976d2'     # Blue
}

# ============================================================================
# BUSINESS METRICS
# ============================================================================

# Cost assumptions (for ROI calculation)
COST_UNSCHEDULED_MAINTENANCE = 500000  # $500K per unscheduled failure
COST_SCHEDULED_MAINTENANCE = 50000      # $50K per scheduled maintenance
COST_FALSE_ALARM = 10000                # $10K per false alarm

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOG_LEVEL = 'INFO'  # Options: DEBUG, INFO, WARNING, ERROR

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_dataset_path(dataset_name, file_type='train'):
    """
    Get full path to dataset file.
    
    Args:
        dataset_name: 'FD001', 'FD002', 'FD003', or 'FD004'
        file_type: 'train', 'test', or 'rul'
    
    Returns:
        str: Full path to the file
    """
    if file_type == 'train':
        filename = f'train_{dataset_name}.txt'
    elif file_type == 'test':
        filename = f'test_{dataset_name}.txt'
    elif file_type == 'rul':
        filename = f'RUL_{dataset_name}.txt'
    else:
        raise ValueError(f"Invalid file_type: {file_type}")
    
    return os.path.join(DATA_RAW, filename)

def print_config_summary():
    """Print a summary of key configuration settings."""
    print("=" * 60)
    print("PROJECT CONFIGURATION SUMMARY")
    print("=" * 60)
    print(f"\nProject Root: {PROJECT_ROOT}")
    print(f"Random Seed: {RANDOM_SEED}")
    print(f"Validation Split: {VALIDATION_SPLIT}")
    print(f"Max RUL Cap: {MAX_RUL} cycles")
    print(f"\nTarget Metrics:")
    print(f"  - RMSE: < {TARGET_RMSE}")
    print(f"  - R²: > {TARGET_R2}")
    print(f"\nRUL Classification:")
    print(f"  - Critical: < {RUL_THRESHOLDS['critical']} cycles")
    print(f"  - Warning: {RUL_THRESHOLDS['critical']}-{RUL_THRESHOLDS['warning']} cycles")
    print(f"  - Good: > {RUL_THRESHOLDS['warning']} cycles")
    print("=" * 60)

# Print configuration on import
if __name__ == "__main__":
    print_config_summary()

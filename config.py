"""
Configuration settings for the Stroke Prediction API
"""

import os

class Config:
    """Base configuration class"""
    
    # API Settings
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 6200))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Model Settings
    MODEL_PATH = "models/random_forest_model_97.74%.pkl"
    SCALER_PATH = "models/scaler_97.74%.pkl"
    ENCODER_PATH = "models/encoder_97.74%.pkl"
    FEATURE_SELECTOR_PATH = "models/feature_selector_97.74%.pkl"
    
    # Risk Level Thresholds
    HIGH_RISK_THRESHOLD = 0.7
    MEDIUM_RISK_THRESHOLD = 0.3
    
    # Required Fields for Prediction
    REQUIRED_FIELDS = [
        'gender', 'age', 'hypertension', 'heart_disease', 
        'ever_married', 'work_type', 'Residence_type', 
        'avg_glucose_level', 'bmi', 'smoking_status'
    ]
    
    # Valid Values for Categorical Fields
    VALID_VALUES = {
        'gender': ['Male', 'Female'],
        'ever_married': ['Yes', 'No'],
        'work_type': ['Private', 'Self-employed', 'Govt_job', 'children', 'Never_worked'],
        'Residence_type': ['Urban', 'Rural'],
        'smoking_status': ['formerly smoked', 'never smoked', 'smokes', 'Unknown']
    }
    
    # Numerical Field Ranges
    FIELD_RANGES = {
        'age': (0, 100),
        'hypertension': (0, 1),
        'heart_disease': (0, 1),
        'avg_glucose_level': (50, 300),
        'bmi': (10, 50)
    }
    
    # Logging Settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # CORS Settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # Security Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Model Information
    MODEL_INFO = {
        'model_type': 'Random Forest Classifier',
        'accuracy': '97.74%',
        'description': 'Stroke risk prediction model trained on healthcare dataset'
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    API_HOST = '0.0.0.0'
    API_PORT = int(os.environ.get('PORT', 6200))

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    LOG_LEVEL = 'DEBUG'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 
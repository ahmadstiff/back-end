# Stroke Prediction API - Complete Setup

## 🎯 Overview

I've successfully created a complete Flask API for your stroke prediction model with 97.74% accuracy. The API is well-structured, documented, and ready to use.

## 📁 Project Structure

```
back-end/
├── app.py                 # Main Flask application with API endpoints
├── config.py              # Configuration settings
├── run.py                 # Startup script with validation
├── setup.sh               # Automated setup script
├── requirements.txt       # Python dependencies
├── README.md             # Comprehensive documentation
├── test_api.py           # Test script for API functionality
├── example_usage.py      # Usage examples
├── .gitignore            # Git ignore file
├── API_SUMMARY.md        # This summary file
└── models/               # Trained model files
    ├── random_forest_model_97.74%.pkl
    ├── scaler_97.74%.pkl
    ├── encoder_97.74%.pkl
    └── feature_selector_97.74%.pkl
```

## 🚀 Quick Start

### 1. Automated Setup (Recommended)
```bash
./setup.sh
```

### 2. Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the API
python3 run.py
```

## 📋 API Endpoints

### 1. Health Check
- **GET** `/health`
- Checks if API is running and models are loaded

### 2. Single Prediction
- **POST** `/predict`
- Predicts stroke risk for one patient
- Requires all 10 patient fields

### 3. Batch Prediction
- **POST** `/predict/batch`
- Predicts stroke risk for multiple patients
- Accepts array of patient data

### 4. Model Information
- **GET** `/model/info`
- Returns model details and feature information

## 📊 Input Data Schema

### Required Fields:
- `gender`: "Male" or "Female"
- `age`: 0-100
- `hypertension`: 0 or 1
- `heart_disease`: 0 or 1
- `ever_married`: "Yes" or "No"
- `work_type`: "Private", "Self-employed", "Govt_job", "children", "Never_worked"
- `Residence_type`: "Urban" or "Rural"
- `avg_glucose_level`: 50-300
- `bmi`: 10-50
- `smoking_status`: "formerly smoked", "never smoked", "smokes", "Unknown"

## 🎯 Risk Levels

- **Low Risk**: Probability < 30%
- **Medium Risk**: Probability 30-70%
- **High Risk**: Probability > 70%

## 🔧 Key Features

### 1. **Comprehensive Preprocessing**
- Handles missing values (BMI imputation)
- Removes anomalies (Other gender)
- Feature engineering (age groups, BMI categories, risk scores)
- Categorical encoding
- Feature selection
- SMOTE balancing
- Robust scaling

### 2. **Robust Error Handling**
- Input validation
- Missing field detection
- Proper HTTP status codes
- Detailed error messages
- Logging for debugging

### 3. **Configuration Management**
- Environment-based configuration
- Configurable thresholds
- Valid value definitions
- Field range validation

### 4. **Testing & Examples**
- Comprehensive test suite
- Usage examples
- Health checks
- Model information

## 🧪 Testing

### Run Tests
```bash
python3 test_api.py
```

### Run Examples
```bash
python3 example_usage.py
```

## 📝 Example Usage

### Single Prediction
```python
import requests

data = {
    "gender": "Male",
    "age": 67,
    "hypertension": 0,
    "heart_disease": 1,
    "ever_married": "Yes",
    "work_type": "Private",
    "Residence_type": "Urban",
    "avg_glucose_level": 228.69,
    "bmi": 36.6,
    "smoking_status": "formerly smoked"
}

response = requests.post('http://localhost:5000/predict', json=data)
result = response.json()
print(f"Stroke Risk: {'Yes' if result['prediction'] == 1 else 'No'}")
print(f"Probability: {result['probability']:.3f}")
print(f"Risk Level: {result['risk_level']}")
```

### Batch Prediction
```python
patients_data = {
    "patients": [
        # ... patient data array
    ]
}

response = requests.post('http://localhost:5000/predict/batch', json=patients_data)
results = response.json()
```

## 🔒 Security & Best Practices

- CORS enabled for cross-origin requests
- Input validation and sanitization
- Error logging for debugging
- Configuration-based settings
- Virtual environment isolation
- Comprehensive documentation

## 🎉 What's Included

1. **Complete Flask API** with all preprocessing steps
2. **Automated setup script** for easy installation
3. **Comprehensive testing** suite
4. **Usage examples** and documentation
5. **Configuration management** system
6. **Error handling** and validation
7. **Health checks** and monitoring
8. **Batch processing** capabilities

## 🚀 Next Steps

1. Run `./setup.sh` to install dependencies
2. Start the API with `python3 run.py`
3. Test with `python3 test_api.py`
4. Use the API in your applications

The API is production-ready and includes all the preprocessing steps from your original machine learning pipeline, ensuring consistent predictions with your trained model. 
# Stroke Prediction API

A Flask-based REST API for predicting stroke risk using a trained Random Forest model with 97.74% accuracy.

## 🏗️ Project Structure

```
back-end/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md            # This file
└── models/              # Trained model files
    ├── random_forest_model_97.74%.pkl
    ├── scaler_97.74%.pkl
    ├── encoder_97.74%.pkl
    └── feature_selector_97.74%.pkl
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the API

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## 🌐 Deployment

### Render Deployment

This API is configured for deployment on Render. To deploy:

1. **Connect your repository to Render**
2. **Use these settings:**
   - **Root Directory**: (leave empty for root)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

3. **Environment Variables:**
   - `FLASK_ENV`: `production`
   - `PYTHON_VERSION`: `3.11.0`

4. **Health Check Path**: `/health`

The API will be automatically deployed and available at your Render URL.

### Local Development

For local development, you can also use the setup script:

```bash
./setup.sh
```

## 📋 API Endpoints

### 1. Health Check
**GET** `/health`

Check if the API is running and models are loaded.

**Response:**
```json
{
  "status": "healthy",
  "message": "Stroke Prediction API is running",
  "model_loaded": true
}
```

### 2. Single Prediction
**POST** `/predict`

Predict stroke risk for a single patient.

**Request Body:**
```json
{
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
```

**Response:**
```json
{
  "prediction": 1,
  "probability": 0.85,
  "confidence": 0.85,
  "risk_level": "High",
  "message": "Stroke risk prediction completed successfully"
}
```

### 3. Batch Prediction
**POST** `/predict/batch`

Predict stroke risk for multiple patients.

**Request Body:**
```json
{
  "patients": [
    {
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
    },
    {
      "gender": "Female",
      "age": 61,
      "hypertension": 0,
      "heart_disease": 0,
      "ever_married": "Yes",
      "work_type": "Self-employed",
      "Residence_type": "Rural",
      "avg_glucose_level": 202.21,
      "bmi": 28.1,
      "smoking_status": "never smoked"
    }
  ]
}
```

**Response:**
```json
{
  "predictions": [
    {
      "patient_id": 1,
      "prediction": 1,
      "probability": 0.85,
      "confidence": 0.85,
      "risk_level": "High"
    },
    {
      "patient_id": 2,
      "prediction": 0,
      "probability": 0.12,
      "confidence": 0.88,
      "risk_level": "Low"
    }
  ],
  "total_patients": 2,
  "successful_predictions": 2
}
```

### 4. Model Information
**GET** `/model/info`

Get information about the trained model.

**Response:**
```json
{
  "model_type": "Random Forest Classifier",
  "accuracy": "97.74%",
  "features_used": 15,
  "feature_names": ["age", "hypertension", "heart_disease", "avg_glucose_level", "bmi", "risk_score", ...],
  "model_loaded": true
}
```

## 📊 Input Data Schema

### Required Fields

| Field | Type | Description | Valid Values |
|-------|------|-------------|--------------|
| `gender` | string | Patient's gender | "Male", "Female" |
| `age` | integer | Patient's age | 0-100 |
| `hypertension` | integer | Hypertension status | 0 (No), 1 (Yes) |
| `heart_disease` | integer | Heart disease status | 0 (No), 1 (Yes) |
| `ever_married` | string | Marital status | "Yes", "No" |
| `work_type` | string | Employment type | "Private", "Self-employed", "Govt_job", "children", "Never_worked" |
| `Residence_type` | string | Residence type | "Urban", "Rural" |
| `avg_glucose_level` | float | Average glucose level | 50-300 |
| `bmi` | float | Body Mass Index | 10-50 |
| `smoking_status` | string | Smoking status | "formerly smoked", "never smoked", "smokes", "Unknown" |

## 🎯 Risk Levels

- **Low Risk**: Probability < 0.3
- **Medium Risk**: Probability 0.3 - 0.7
- **High Risk**: Probability > 0.7

## 🔧 Model Details

- **Algorithm**: Random Forest Classifier
- **Accuracy**: 97.74%
- **Features**: 15 selected features
- **Preprocessing**: 
  - SMOTE for class balancing
  - RobustScaler for feature scaling
  - OneHotEncoder for categorical variables
  - Feature selection using SelectKBest

## 🚨 Error Handling

The API returns appropriate HTTP status codes:

- **200**: Success
- **400**: Bad Request (missing fields, invalid data)
- **500**: Internal Server Error

Error responses include:
```json
{
  "error": "Error description",
  "message": "Detailed error message"
}
```

## 🧪 Testing the API

### Using curl

```bash
# Health check
curl -X GET http://localhost:5000/health

# Single prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

### Using Python requests

```python
import requests
import json

# Health check
response = requests.get('http://localhost:5000/health')
print(response.json())

# Single prediction
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
print(response.json())
```

## 🔒 Security Notes

- The API runs on `0.0.0.0:5000` by default
- CORS is enabled for cross-origin requests
- Input validation is implemented for all endpoints
- Error messages are logged for debugging

## 📝 License

This project is for educational purposes. The stroke prediction model is trained on healthcare data and should be used responsibly. 
import os
import numpy as np
import pandas as pd
import warnings
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import logging
from config import config

warnings.filterwarnings("ignore")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS with specific origins
CORS(app, origins=[
    "http://localhost:3000",
    "http://localhost:3001", 
    "http://localhost:3002",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:3002",
    "http://192.168.1.132:3000",
    "http://192.168.1.132:3001",
    "http://192.168.1.132:3002"
], methods=["GET", "POST", "OPTIONS"], allow_headers=["Content-Type", "Authorization"])

# Load configuration
config_name = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

class StrokePredictionAPI:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.encoder = None
        self.feature_selector = None
        self.load_models()
    
    def load_models(self):
        """Load the trained model and preprocessors"""
        try:
            model_path = app.config['MODEL_PATH']
            scaler_path = app.config['SCALER_PATH']
            encoder_path = app.config['ENCODER_PATH']
            feature_selector_path = app.config['FEATURE_SELECTOR_PATH']
            
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.encoder = joblib.load(encoder_path)
            self.feature_selector = joblib.load(feature_selector_path)
            
            logger.info("✅ All models loaded successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error loading models: {str(e)}")
            raise
    
    def preprocess_input(self, data):
        """Preprocess input data for prediction"""
        try:
            # Create DataFrame from input data
            df = pd.DataFrame([data])
            
            # Note: id column is not needed for feature selector
            
            # Handle missing values
            if 'bmi' in df.columns and df['bmi'].isnull().sum() > 0:
                # Use median BMI for missing values
                df['bmi'].fillna(df['bmi'].median(), inplace=True)
            
            # Remove 'Other' gender if present
            if 'gender' in df.columns and 'Other' in df['gender'].values:
                df = df[df['gender'] != 'Other']
            
            # Feature engineering
            df['age_group'] = pd.cut(df['age'], 
                                   bins=[0, 30, 45, 60, 75, 100], 
                                   labels=['Young', 'Adult', 'Middle-aged', 'Senior', 'Elderly'])
            
            df['bmi_category'] = pd.cut(df['bmi'],
                                      bins=[0, 18.5, 25, 30, 100],
                                      labels=['Underweight', 'Normal', 'Overweight', 'Obese'])
            
            df['glucose_category'] = pd.cut(df['avg_glucose_level'],
                                          bins=[0, 100, 125, 200, 1000],
                                          labels=['Normal', 'Prediabetes', 'Diabetes', 'Very High'])
            
            # Create risk score
            risk_factors = 0
            risk_factors += (df['age'] > 65).astype(int)
            risk_factors += df['hypertension']
            risk_factors += df['heart_disease']
            risk_factors += (df['avg_glucose_level'] > 140).astype(int)
            risk_factors += (df['bmi'] > 30).astype(int)
            df['risk_score'] = risk_factors
            
            # Encode categorical variables
            categorical_columns = ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']
            
            # Apply encoding
            encoded_data = self.encoder.transform(df[categorical_columns])
            encoded_df = pd.DataFrame(encoded_data, 
                                    columns=self.encoder.get_feature_names_out(categorical_columns))
            
            # Combine with original data
            df = pd.concat([df.reset_index(drop=True), 
                          encoded_df.reset_index(drop=True)], axis=1)
            
            # Drop original categorical columns and engineered features
            columns_to_drop = categorical_columns + ['age_group', 'bmi_category', 'glucose_category']
            df.drop(columns=columns_to_drop, inplace=True)
            
            # Add missing columns that the model expects
            if 'id' not in df.columns:
                df['id'] = 1
            
            # Add missing smoking status columns
            if 'smoking_status_never smoked' not in df.columns:
                df['smoking_status_never smoked'] = 0
            
            # Ensure columns are in the correct order for feature selector
            expected_columns = [
                'id', 'age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi', 'risk_score',
                'gender_Male', 'ever_married_Yes', 'work_type_Never_worked', 'work_type_Private',
                'work_type_Self-employed', 'work_type_children', 'Residence_type_Urban',
                'smoking_status_formerly smoked', 'smoking_status_never smoked', 'smoking_status_smokes'
            ]
            
            # Reorder columns to match expected order
            df = df.reindex(columns=expected_columns)
            
            # Apply feature selection
            X_selected = self.feature_selector.transform(df)
            selected_features = self.feature_selector.get_feature_names_out()
            
            # Create final DataFrame with selected features in correct order
            final_df = pd.DataFrame(X_selected, columns=selected_features)
            
            return final_df
            
        except Exception as e:
            logger.error(f"❌ Error in preprocessing: {str(e)}")
            raise
    
    def predict(self, data):
        """Make stroke prediction"""
        try:
            # Preprocess input data
            processed_data = self.preprocess_input(data)
            
            # Scale features
            scaled_data = self.scaler.transform(processed_data)
            
            # Make prediction
            prediction = self.model.predict(scaled_data)[0]
            prediction_proba = self.model.predict_proba(scaled_data)[0]
            
            return {
                'prediction': int(prediction),
                'probability': float(prediction_proba[1]),
                'confidence': float(max(prediction_proba))
            }
            
        except Exception as e:
            logger.error(f"❌ Error in prediction: {str(e)}")
            raise

# Initialize the API
api = StrokePredictionAPI()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Stroke Prediction API is running',
        'model_loaded': api.model is not None
    })

@app.route('/predict', methods=['POST'])
def predict_stroke():
    """Predict stroke risk"""
    try:
        # Get input data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'message': 'Please provide patient data in JSON format'
            }), 400
        
        # Validate required fields
        required_fields = app.config['REQUIRED_FIELDS']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields,
                'required_fields': required_fields
            }), 400
        
        # Make prediction
        result = api.predict(data)
        
        # Prepare response
        response = {
            'prediction': result['prediction'],
            'probability': result['probability'],
            'confidence': result['confidence'],
            'risk_level': 'High' if result['probability'] > app.config['HIGH_RISK_THRESHOLD'] else 'Medium' if result['probability'] > app.config['MEDIUM_RISK_THRESHOLD'] else 'Low',
            'message': 'Stroke risk prediction completed successfully'
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"❌ Prediction error: {str(e)}")
        return jsonify({
            'error': 'Prediction failed',
            'message': str(e)
        }), 500

@app.route('/predict/batch', methods=['POST'])
def predict_stroke_batch():
    """Predict stroke risk for multiple patients"""
    try:
        # Get input data
        data = request.get_json()
        
        if not data or 'patients' not in data:
            return jsonify({
                'error': 'No patients data provided',
                'message': 'Please provide patients data in JSON format with "patients" key'
            }), 400
        
        patients = data['patients']
        
        if not isinstance(patients, list):
            return jsonify({
                'error': 'Invalid data format',
                'message': 'Patients data must be a list'
            }), 400
        
        results = []
        for i, patient_data in enumerate(patients):
            try:
                result = api.predict(patient_data)
                results.append({
                    'patient_id': i + 1,
                    'prediction': result['prediction'],
                    'probability': result['probability'],
                    'confidence': result['confidence'],
                    'risk_level': 'High' if result['probability'] > app.config['HIGH_RISK_THRESHOLD'] else 'Medium' if result['probability'] > app.config['MEDIUM_RISK_THRESHOLD'] else 'Low'
                })
            except Exception as e:
                results.append({
                    'patient_id': i + 1,
                    'error': str(e)
                })
        
        return jsonify({
            'predictions': results,
            'total_patients': len(patients),
            'successful_predictions': len([r for r in results if 'error' not in r])
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Batch prediction error: {str(e)}")
        return jsonify({
            'error': 'Batch prediction failed',
            'message': str(e)
        }), 500

@app.route('/model/info', methods=['GET'])
def model_info():
    """Get model information"""
    try:
        return jsonify({
            'model_type': app.config['MODEL_INFO']['model_type'],
            'accuracy': app.config['MODEL_INFO']['accuracy'],
            'description': app.config['MODEL_INFO']['description'],
            'features_used': len(api.feature_selector.get_feature_names_out()),
            'feature_names': api.feature_selector.get_feature_names_out().tolist(),
            'model_loaded': api.model is not None
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error getting model info: {str(e)}")
        return jsonify({
            'error': 'Failed to get model info',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['API_HOST'],
        port=app.config['API_PORT']
    ) 
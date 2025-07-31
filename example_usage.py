#!/usr/bin/env python3
"""
Example usage of the Stroke Prediction API
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:5000"

def example_single_prediction():
    """Example of making a single prediction"""
    print("🎯 Example: Single Patient Prediction")
    print("-" * 40)
    
    # Patient data
    patient_data = {
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
    
    print("📋 Patient Data:")
    for key, value in patient_data.items():
        print(f"   {key}: {value}")
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=patient_data)
        if response.status_code == 200:
            result = response.json()
            print(f"\n🎯 Prediction Result:")
            print(f"   Stroke Risk: {'Yes' if result['prediction'] == 1 else 'No'}")
            print(f"   Probability: {result['probability']:.3f} ({result['probability']*100:.1f}%)")
            print(f"   Risk Level: {result['risk_level']}")
            print(f"   Confidence: {result['confidence']:.3f}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")

def example_batch_prediction():
    """Example of making batch predictions"""
    print("\n🎯 Example: Batch Patient Predictions")
    print("-" * 40)
    
    # Multiple patients data
    patients_data = {
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
            },
            {
                "gender": "Male",
                "age": 80,
                "hypertension": 1,
                "heart_disease": 1,
                "ever_married": "Yes",
                "work_type": "Private",
                "Residence_type": "Urban",
                "avg_glucose_level": 105.92,
                "bmi": 32.5,
                "smoking_status": "never smoked"
            }
        ]
    }
    
    print(f"📋 Processing {len(patients_data['patients'])} patients...")
    
    try:
        response = requests.post(f"{BASE_URL}/predict/batch", json=patients_data)
        if response.status_code == 200:
            result = response.json()
            print(f"\n🎯 Batch Prediction Results:")
            print(f"   Total patients: {result['total_patients']}")
            print(f"   Successful predictions: {result['successful_predictions']}")
            
            for prediction in result['predictions']:
                patient_id = prediction['patient_id']
                stroke_risk = "Yes" if prediction['prediction'] == 1 else "No"
                probability = prediction['probability']
                risk_level = prediction['risk_level']
                
                print(f"\n   Patient {patient_id}:")
                print(f"     Stroke Risk: {stroke_risk}")
                print(f"     Probability: {probability:.3f} ({probability*100:.1f}%)")
                print(f"     Risk Level: {risk_level}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")

def example_model_info():
    """Example of getting model information"""
    print("\n🎯 Example: Model Information")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/model/info")
        if response.status_code == 200:
            result = response.json()
            print("📊 Model Details:")
            print(f"   Model Type: {result['model_type']}")
            print(f"   Accuracy: {result['accuracy']}")
            print(f"   Features Used: {result['features_used']}")
            print(f"   Model Loaded: {result['model_loaded']}")
            
            print(f"\n🔍 Feature Names:")
            for i, feature in enumerate(result['feature_names'], 1):
                print(f"   {i:2d}. {feature}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")

def example_health_check():
    """Example of health check"""
    print("\n🎯 Example: Health Check")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            result = response.json()
            print("🏥 API Status:")
            print(f"   Status: {result['status']}")
            print(f"   Message: {result['message']}")
            print(f"   Model Loaded: {result['model_loaded']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")

def main():
    """Run all examples"""
    print("🏥 Stroke Prediction API - Usage Examples")
    print("=" * 50)
    
    # Check if API is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ API is not responding properly. Make sure it's running on http://localhost:5000")
            return
    except:
        print("❌ Cannot connect to API. Make sure it's running on http://localhost:5000")
        print("   Run: python app.py")
        return
    
    # Run examples
    example_health_check()
    example_model_info()
    example_single_prediction()
    example_batch_prediction()
    
    print("\n" + "=" * 50)
    print("✅ Examples completed!")

if __name__ == "__main__":
    main() 
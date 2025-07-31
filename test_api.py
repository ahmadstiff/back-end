#!/usr/bin/env python3
"""
Test script for Stroke Prediction API
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed!")
            print(f"   Status: {data['status']}")
            print(f"   Model loaded: {data['model_loaded']}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running.")
        return False

def test_model_info():
    """Test model info endpoint"""
    print("\n🔍 Testing model info...")
    try:
        response = requests.get(f"{BASE_URL}/model/info")
        if response.status_code == 200:
            data = response.json()
            print("✅ Model info retrieved successfully!")
            print(f"   Model type: {data['model_type']}")
            print(f"   Accuracy: {data['accuracy']}")
            print(f"   Features used: {data['features_used']}")
            return True
        else:
            print(f"❌ Model info failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting model info: {str(e)}")
        return False

def test_single_prediction():
    """Test single prediction endpoint"""
    print("\n🔍 Testing single prediction...")
    
    # Test data
    test_data = {
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
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=test_data)
        if response.status_code == 200:
            data = response.json()
            print("✅ Single prediction successful!")
            print(f"   Prediction: {data['prediction']}")
            print(f"   Probability: {data['probability']:.3f}")
            print(f"   Risk level: {data['risk_level']}")
            return True
        else:
            print(f"❌ Single prediction failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error in single prediction: {str(e)}")
        return False

def test_batch_prediction():
    """Test batch prediction endpoint"""
    print("\n🔍 Testing batch prediction...")
    
    # Test data for multiple patients
    test_patients = [
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
    
    try:
        response = requests.post(f"{BASE_URL}/predict/batch", json={"patients": test_patients})
        if response.status_code == 200:
            data = response.json()
            print("✅ Batch prediction successful!")
            print(f"   Total patients: {data['total_patients']}")
            print(f"   Successful predictions: {data['successful_predictions']}")
            
            for prediction in data['predictions']:
                print(f"   Patient {prediction['patient_id']}: {prediction['prediction']} ({prediction['risk_level']} risk)")
            return True
        else:
            print(f"❌ Batch prediction failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error in batch prediction: {str(e)}")
        return False

def test_error_handling():
    """Test error handling with invalid data"""
    print("\n🔍 Testing error handling...")
    
    # Test with missing fields
    invalid_data = {
        "gender": "Male",
        "age": 67
        # Missing required fields
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=invalid_data)
        if response.status_code == 400:
            data = response.json()
            print("✅ Error handling working correctly!")
            print(f"   Error: {data['error']}")
            print(f"   Missing fields: {data['missing_fields']}")
            return True
        else:
            print(f"❌ Expected 400 error, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error in error handling test: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🧪 Starting API Tests...")
    print("=" * 50)
    
    tests = [
        test_health_check,
        test_model_info,
        test_single_prediction,
        test_batch_prediction,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the API implementation.")
    
    return passed == total

if __name__ == "__main__":
    run_all_tests() 
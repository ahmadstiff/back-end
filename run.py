#!/usr/bin/env python3
"""
Startup script for the Stroke Prediction API
"""

import os
import sys
from app import app

def main():
    """Main function to run the API"""
    print("🏥 Starting Stroke Prediction API...")
    print("=" * 50)
    
    # Check if models exist
    model_files = [
        "models/random_forest_model_97.74%.pkl",
        "models/scaler_97.74%.pkl",
        "models/encoder_97.74%.pkl",
        "models/feature_selector_97.74%.pkl"
    ]
    
    missing_files = []
    for file_path in model_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing model files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\nPlease ensure all model files are present in the models/ directory.")
        sys.exit(1)
    
    print("✅ All model files found!")
    print(f"🌐 API will be available at: http://{app.config['API_HOST']}:{app.config['API_PORT']}")
    print(f"🔧 Debug mode: {app.config['DEBUG']}")
    print("=" * 50)
    
    # Run the application
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['API_HOST'],
        port=app.config['API_PORT']
    )

if __name__ == "__main__":
    main() 
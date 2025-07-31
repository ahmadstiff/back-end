#!/bin/bash

echo "🏥 Setting up Stroke Prediction API..."
echo "=" * 50

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if models exist
echo "🔍 Checking model files..."
model_files=(
    "models/random_forest_model_97.74%.pkl"
    "models/scaler_97.74%.pkl"
    "models/encoder_97.74%.pkl"
    "models/feature_selector_97.74%.pkl"
)

missing_files=()
for file in "${model_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo "⚠️  Missing model files:"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    echo "Please ensure all model files are present in the models/ directory."
else
    echo "✅ All model files found"
fi

# Test import
echo "🧪 Testing API import..."
python3 -c "import app; print('✅ API module imported successfully')"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup completed successfully!"
    echo "=" * 50
    echo "To run the API:"
    echo "  1. Activate virtual environment: source venv/bin/activate"
    echo "  2. Run the API: python3 run.py"
    echo "  3. Or run directly: python3 app.py"
    echo ""
    echo "To test the API:"
    echo "  python3 test_api.py"
    echo ""
    echo "To see examples:"
    echo "  python3 example_usage.py"
else
    echo "❌ Setup failed. Please check the error messages above."
    exit 1
fi 
# 🚀 Deployment Guide - Stroke Prediction API

## 🌐 Render Deployment

### Langkah-langkah Deployment di Render:

#### 1. **Persiapkan Repository**
Pastikan semua file sudah ada di repository:
- ✅ `app.py` - Main Flask application
- ✅ `requirements.txt` - Dependencies
- ✅ `render.yaml` - Render configuration
- ✅ `models/` - Model files
- ✅ `config.py` - Configuration

#### 2. **Connect ke Render**

1. Buka [Render Dashboard](https://dashboard.render.com)
2. Klik **"New +"** → **"Web Service"**
3. Connect dengan GitHub repository Anda
4. Pilih repository yang berisi kode API

#### 3. **Konfigurasi Service**

**Basic Settings:**
- **Name**: `stroke-prediction-api` (atau nama yang Anda inginkan)
- **Environment**: `Python 3`
- **Region**: Pilih yang terdekat (misal: Singapore)

**Build & Deploy Settings:**
- **Root Directory**: (kosongkan - gunakan root)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

**Environment Variables:**
```
FLASK_ENV=production
PYTHON_VERSION=3.11.0
```

**Health Check:**
- **Health Check Path**: `/health`

#### 4. **Deploy**

1. Klik **"Create Web Service"**
2. Render akan otomatis build dan deploy aplikasi
3. Tunggu hingga status berubah menjadi **"Live"**

#### 5. **Verifikasi Deployment**

Setelah deploy selesai, test endpoint:

```bash
# Health check
curl https://your-app-name.onrender.com/health

# Model info
curl https://your-app-name.onrender.com/model/info

# Test prediction
curl -X POST https://your-app-name.onrender.com/predict \
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

## 🔧 Konfigurasi File

### `render.yaml`
```yaml
services:
  - type: web
    name: stroke-prediction-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: FLASK_ENV
        value: production
    healthCheckPath: /health
    autoDeploy: true
```

### `requirements.txt`
```
Flask==2.3.3
Flask-CORS==4.0.0
gunicorn==21.2.0
numpy>=1.26.0
pandas>=2.0.0
scikit-learn>=1.3.0
imbalanced-learn>=0.11.0
joblib>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.15.0
Werkzeug==2.3.7
```

## 📋 API Endpoints

Setelah deploy, API akan tersedia di: `https://your-app-name.onrender.com`

### Endpoints:
- **GET** `/health` - Health check
- **POST** `/predict` - Single prediction
- **POST** `/predict/batch` - Batch predictions
- **GET** `/model/info` - Model information

## 🧪 Testing Deployment

### 1. Health Check
```bash
curl https://your-app-name.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Stroke Prediction API is running",
  "model_loaded": true
}
```

### 2. Single Prediction
```bash
curl -X POST https://your-app-name.onrender.com/predict \
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

Expected response:
```json
{
  "prediction": 1,
  "probability": 0.85,
  "confidence": 0.85,
  "risk_level": "High",
  "message": "Stroke risk prediction completed successfully"
}
```

## 🔍 Troubleshooting

### Common Issues:

1. **Build Failed**
   - Pastikan semua dependencies ada di `requirements.txt`
   - Check log build di Render dashboard

2. **Model Loading Error**
   - Pastikan file model ada di folder `models/`
   - Check path di `config.py`

3. **Port Issues**
   - Render menggunakan environment variable `$PORT`
   - Pastikan app menggunakan `os.environ.get('PORT', 5000)`

4. **Health Check Failed**
   - Pastikan endpoint `/health` berfungsi
   - Check log aplikasi di Render dashboard

### Debug Commands:

```bash
# Check build logs
# Lihat di Render dashboard → Logs

# Test locally
python3 run.py

# Test with curl
curl http://localhost:5000/health
```

## 📊 Monitoring

### Render Dashboard:
- **Logs**: Lihat real-time logs
- **Metrics**: Monitor performance
- **Deployments**: Track deployment history

### Health Monitoring:
- Render akan otomatis check `/health` endpoint
- Jika health check gagal, Render akan restart service

## 🚀 Auto-Deploy

Dengan `render.yaml`, setiap push ke repository akan otomatis trigger deployment baru.

## 📝 Notes

- Render free tier memiliki cold start (akan sleep setelah 15 menit tidak ada request)
- Untuk production, consider upgrade ke paid plan
- Monitor usage di Render dashboard 
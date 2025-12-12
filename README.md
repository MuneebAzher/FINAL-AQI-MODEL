# AQI PM2.5 Prediction Model

A machine learning model to predict Air Quality Index (PM2.5) based on weather parameters.

## Features

The model uses 8 features:
- Average Temperature (°F)
- Average Dew Point (°F)
- Average Humidity (%)
- Average Wind Speed (mph)
- Average Pressure (in)
- AQI Lag 1 (1 day ago)
- AQI Lag 2 (2 days ago)
- AQI Lag 7 (7 days ago)

## Local Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run "app (1).py"
```

The app will open in your browser at `http://localhost:8501`

## Deployment Options

### Option 1: Streamlit Cloud (Recommended - Free & Easy)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository and set the main file path to `app (1).py`
6. Click "Deploy"

**Note:** Make sure `model.pkl` is included in your repository.

### Option 2: Heroku

1. Create a `Procfile`:
```
web: sh setup.sh && streamlit run "app (1).py" --server.port=$PORT --server.address=0.0.0.0
```

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
" > ~/.streamlit/config.toml
```

3. Deploy using Heroku CLI:
```bash
heroku create your-app-name
git push heroku main
```

### Option 3: Docker

1. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app (1).py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. Build and run:
```bash
docker build -t aqi-predictor .
docker run -p 8501:8501 aqi-predictor
```

### Option 4: AWS / Azure / GCP

For cloud platforms, you can:
- Use AWS Elastic Beanstalk
- Deploy to Azure App Service
- Use Google Cloud Run with Docker

## Files

- `app (1).py` - Streamlit application
- `model.pkl` - Trained ML model
- `requirements.txt` - Python dependencies
- `template/index.html` - HTML template (for Flask alternative)

## Model Performance

- R² Score: ~0.525
- MAE Error: ~36

## Notes

- The model requires lag features (previous AQI values) for best accuracy
- For real-time predictions without historical data, you may need to use default values or retrain without lag features




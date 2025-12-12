import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.express as px

# App setup
st.set_page_config(
    page_title="AQI PM2.5 Predictor",
    page_icon="🌬️",
    layout="centered",
)

# Subtle styling
st.markdown(
    """
    <style>
        .main {background-color: #f8fafc;}
        .stButton>button {background: linear-gradient(90deg,#2563eb,#10b981); color: white;}
        .metric-card {padding: 1rem; border-radius: 12px; background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.06);}
    </style>
    """,
    unsafe_allow_html=True,
)

# Load Model
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

st.title("🌬️ AQI PM2.5 Predictor")
st.write("Enter weather parameters to predict Air Quality Index (PM2.5):")

# Main weather features
st.subheader("Current Weather Conditions")
avg_temp = st.number_input("Average Temperature (°F)", value=70.0, step=0.1)
avg_dew_point = st.number_input("Average Dew Point (°F)", value=50.0, step=0.1)
avg_humidity = st.number_input("Average Humidity (%)", value=60.0, step=0.1)
avg_wind_speed = st.number_input("Average Wind Speed (mph)", value=5.0, step=0.1)
avg_pressure = st.number_input("Average Pressure (in)", value=29.0, step=0.1)

# Lag features (previous AQI values)
st.subheader("Previous AQI Values (Optional)")
st.caption("If you don't have previous values, leave defaults or enter estimated values")
aqi_lag_1 = st.number_input("AQI (1 day ago)", value=100.0, step=0.1)
aqi_lag_2 = st.number_input("AQI (2 days ago)", value=100.0, step=0.1)
aqi_lag_7 = st.number_input("AQI (7 days ago)", value=100.0, step=0.1)

# Prepare input array in the correct order
inputs = [
    avg_temp,
    avg_dew_point,
    avg_humidity,
    avg_wind_speed,
    avg_pressure,
    aqi_lag_1,
    aqi_lag_2,
    aqi_lag_7
]

if st.button("Predict AQI", type="primary"):
    input_data = np.array([inputs])
    prediction = model.predict(input_data)
    predicted_aqi = prediction[0]
    
    # Display prediction with context (wider left column to pull card left)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3 style="margin-bottom:0;color:black">🎯 Predicted AQI</h3>
                <p style="font-size:32px; margin:0; font-weight:700;color:black">{predicted_aqi:.2f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # Add AQI category interpretation
    category_text = ""
    category_tone = None
    if predicted_aqi <= 50:
        category_text = "✅ Good - Air quality is satisfactory"
        category_tone = st.info
    elif predicted_aqi <= 100:
        category_text = "⚠️ Moderate - Acceptable for most people"
        category_tone = st.warning
    elif predicted_aqi <= 150:
        category_text = "⚠️ Unhealthy for Sensitive Groups"
        category_tone = st.warning
    elif predicted_aqi <= 200:
        category_text = "🔴 Unhealthy - Everyone may experience health effects"
        category_tone = st.error
    elif predicted_aqi <= 300:
        category_text = "🔴 Very Unhealthy - Health alert"
        category_tone = st.error
    else:
        category_text = "🔴 Hazardous - Health warning of emergency conditions"
        category_tone = st.error

    if category_tone:
        with col2:
            category_tone(category_text)

    # Dynamic heatmap for current inputs and predicted AQI
    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
    heatmap_df = pd.DataFrame(
        [[avg_temp, avg_dew_point, avg_humidity, avg_wind_speed, avg_pressure, predicted_aqi]],
        index=["Value"],
        columns=[
            "Avg Temp (°F)",
            "Avg Dew Point (°F)",
            "Avg Humidity (%)",
            "Avg Wind Speed (mph)",
            "Avg Pressure (in)",
            "Predicted AQI",
        ],
    )
    heatmap_fig = px.imshow(
        heatmap_df,
        color_continuous_scale=[
            (0.0, "#22c55e"),
            (0.2, "#84cc16"),
            (0.4, "#facc15"),
            (0.6, "#f97316"),
            (0.8, "#ef4444"),
            (1.0, "#991b1b"),
        ],
        text_auto=".1f",
        labels=dict(color="Value"),
        aspect="auto",
    )
    heatmap_fig.update_layout(
        title="Feature Snapshot Heatmap",
        margin=dict(l=10, r=10, t=40, b=10),
        coloraxis_colorbar=dict(title="Value"),
    )
    st.plotly_chart(heatmap_fig, use_container_width=True)

    # Line chart: Actual vs Predicted AQI over time
    timeline = [
        {"Day": "7 days ago", "Series": "Actual", "AQI": aqi_lag_7},
        {"Day": "2 days ago", "Series": "Actual", "AQI": aqi_lag_2},
        {"Day": "1 day ago", "Series": "Actual", "AQI": aqi_lag_1},
        {"Day": "Today", "Series": "Predicted", "AQI": predicted_aqi},
    ]
    line_df = pd.DataFrame(timeline)
    line_fig = px.line(
        line_df,
        x="Day",
        y="AQI",
        color="Series",
        markers=True,
        title="Actual vs Predicted AQI Over Time",
        category_orders={"Day": ["7 days ago", "2 days ago", "1 day ago", "Today"]},
    )
    line_fig.update_traces(marker=dict(size=10))
    line_fig.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        yaxis_title="AQI (PM2.5)",
        xaxis_title="",
    )
    st.plotly_chart(line_fig, use_container_width=True)

    # Add static PNG images at the bottom, centered
    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
    st.subheader("Additional Visualizations")
    img_cols = st.columns([1, 3, 1])
    with img_cols[1]:
        st.image("heatmap.png", caption="AQI Heatmap", use_container_width=True)
        st.image("line.png", caption="AQI Trend", use_container_width=True)

import streamlit as st
import pandas as pd
import numpy as np
import time
import cv2
from src.database.db_manager import DBManager
from src.utils.config import Config

# Load config
config = Config("config.yaml")
db = DBManager(config.get("database.url"))

def main():
    st.set_page_config(page_title="Predictive Traffic Signal Control Dashboard", layout="wide")
    
    st.title("🚦 Predictive Traffic Signal Control Dashboard")
    st.sidebar.header("Settings")
    
    # Live Traffic Video (Simulated)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📺 Live Traffic Video")
        # In a real app, this would be a cv2 frame or a video stream
        st.image("https://via.placeholder.com/640x480.png?text=Live+Traffic+Video+Stream", use_column_width=True)
        
    with col2:
        st.subheader("📊 Current Signal Status")
        # Display real-time lane densities and green times
        lane_data = {
            "lane_1": {"density": 0.45, "green_time": 30},
            "lane_2": {"density": 0.12, "green_time": 15},
            "lane_3": {"density": 0.88, "green_time": 45},
            "lane_4": {"density": 0.23, "green_time": 20}
        }
        for lane_id, data in lane_data.items():
            st.metric(label=f"Lane {lane_id} Density", value=f"{data['density']*100:.1f}%", delta=f"{data['green_time']}s green")
            
    # Predicted Traffic Flow
    st.divider()
    st.subheader("🔮 Predicted Traffic Flow (Next Cycle)")
    prediction_data = pd.DataFrame({
        'Lane': ['lane_1', 'lane_2', 'lane_3', 'lane_4'],
        'Predicted Count': [15, 5, 25, 8],
        'Confidence': [0.92, 0.85, 0.95, 0.88]
    })
    st.bar_chart(prediction_data.set_index('Lane')['Predicted Count'])
    
    # Historical Trends
    st.divider()
    st.subheader("📈 Historical Traffic Trends")
    chart_data = pd.DataFrame(
        np.random.randn(20, 4),
        columns=['lane_1', 'lane_2', 'lane_3', 'lane_4']
    )
    st.line_chart(chart_data)

    # Queue Lengths
    st.divider()
    st.subheader("📏 Queue Length Estimation")
    queue_data = pd.DataFrame({
        'Lane': ['lane_1', 'lane_2', 'lane_3', 'lane_4'],
        'Queue Length (m)': [120, 40, 250, 60]
    })
    st.table(queue_data)

    # Emergency Alerts
    if np.random.rand() > 0.9: # Randomly simulate an alert
        st.warning("🚨 EMERGENCY VEHICLE DETECTED in Lane 3! Priority mode active.")

if __name__ == "__main__":
    main()

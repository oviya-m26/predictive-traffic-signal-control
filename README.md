# Predictive Traffic Signal Control System

A research-grade, vision-based predictive traffic signal optimization system that analyzes traffic from video feeds and dynamically controls traffic lights using machine learning and real-time digital twin technology.

## Project Overview

This project implements an end-to-end intelligent traffic management pipeline. It uses YOLOv8 for vehicle detection, spatial polygon-based lane mapping, and machine learning to forecast traffic flow. The core objective is to minimize vehicle wait times, reduce congestion, and prioritize emergency vehicles. This implementation includes a Traffic Digital Twin that continuously records the intersection state for analysis, replay, and model training.

## Team Contribution

This project was collaboratively developed as an end-to-end predictive traffic signal control system. The work involved integrating computer vision, traffic analysis, machine learning-based prediction, signal optimization, SUMO simulation, and Streamlit dashboard visualization into a unified pipeline.

## System Architecture

The system follows a modular, research-focused architecture:

1. **Video Input**: Captures raw video frames from cameras or files using OpenCV.
2. **Vehicle Detection (YOLOv8)**: Real-time detection of cars, buses, trucks, motorcycles, bicycles, and ambulances.
3. **Lane Mapping**: Assigns detected vehicles to specific road lanes using pre-configured polygon regions.
4. **Density Estimation**: Calculates weighted vehicle density per lane (with higher weights for larger vehicles).
5. **Queue Estimation**: Estimates queue length and average waiting time by tracking vehicle speeds and positions relative to stop lines.
6. **Traffic Data Storage & Digital Twin**: Writes time-stamped intersection states to an SQLite database for historical analysis.
7. **Traffic Prediction**: Uses Random Forest, LightGBM, or LSTM models to forecast next-cycle traffic volume.
8. **Signal Optimization Engine**: Computes optimal green light durations using a combination of density, queue length, and predicted flow.
9. **Emergency Prioritization**: Immediately overrides signal cycles when emergency vehicles (ambulances, fire trucks, police) are detected.
10. **Simulation (SUMO)**: Validates control strategies in a simulated urban environment.
11. **Dashboard (Streamlit)**: Interactive dashboard for visualizing real-time metrics and historical data.

## Installation

### Prerequisites

- Python 3.8 or higher
- [SUMO (Simulation of Urban Mobility)](https://sumo.dlr.de/docs/Installing/index.html) (optional, for simulation)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/oviya-m26/predictive-traffic-signal-control.git
   cd predictive-traffic-signal-control
   ```

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Edit `config.yaml` to customize:

- YOLO model path and confidence thresholds
- Lane polygon coordinates for your specific intersection
- Signal timing bounds
- Database storage paths

## How to Run

### 1. Main Pipeline

Runs the detection, lane mapping, and optimization loop on a video stream or file.

```bash
python main.py
```

_(By default, `main.py` looks for video files in `data/raw_videos/`; you can modify the path in `main.py`)_

### 2. Dashboard

Launches the interactive analytics dashboard.

```bash
streamlit run dashboard/dashboard_app.py
```

### 3. Performance Evaluation

Generates comparison plots for system evaluation.

```bash
python experiments/evaluate_system.py
```

## Performance Metrics

The system is evaluated using the following research-grade metrics:

- **Average Wait Time**: Total time vehicles spend stopped at the intersection
- **Average Queue Length**: Number of vehicles waiting in each lane at each signal cycle
- **Vehicle Throughput**: Total vehicles passing through the intersection per hour
- **Signal Efficiency**: Ratio of green time actually utilized by traffic flow
- **Fuel Wastage Estimate**: Derived from wait times and queue lengths
- **Prediction Accuracy**: Mean Absolute Error (MAE) and R² for the traffic prediction models

## Technologies Used

- **Computer Vision**: OpenCV, Ultralytics YOLOv8
- **Machine Learning**: Scikit-learn, LightGBM, PyTorch
- **Database**: SQLAlchemy, SQLite
- **Simulation**: SUMO
- **Visualization**: Streamlit, Matplotlib
- **Backend**: Python

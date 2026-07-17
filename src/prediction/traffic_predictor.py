import pandas as pd
import numpy as np
import pickle
import torch
import torch.nn as nn
from sklearn.ensemble import RandomForestRegressor
try:
    import lightgbm as lgb
except ImportError:
    lgb = None
from src.utils.logger import logger

class LSTMModel(nn.Module):
    """LSTM model for traffic flow prediction."""
    def __init__(self, input_dim, hidden_dim, output_dim=1):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        _, (hn, _) = self.lstm(x)
        out = self.fc(hn[-1])
        return out

class TrafficPredictor:
    """
    Advanced Traffic Flow Predictor with multi-model support.
    Supports Random Forest, LightGBM, and LSTM architectures for research comparison.
    """
    def __init__(self, model_type="random_forest", config=None):
        self.model_type = model_type
        self.config = config or {}
        self.model = None
        logger.info(f"Traffic Predictor initialized with {model_type} model.")

    def prepare_features(self, history_data):
        """
        Standardizes input features for prediction.
        """
        # Example: [lane_density, queue_length, time_of_day, car_count, bus_count, truck_count]
        return np.array(history_data).reshape(1, -1)

    def predict(self, features):
        """
        Predicts traffic count for the next cycle.
        """
        if self.model is None:
            # Baseline: return current density if no model is loaded
            return float(features[0][0])
            
        if self.model_type == "lstm":
            # Pytorch inference
            self.model.eval()
            with torch.no_grad():
                input_tensor = torch.FloatTensor(features).unsqueeze(0) # [Batch, Seq, Feat]
                prediction = self.model(input_tensor)
                return float(prediction.item())
        else:
            # Scikit-learn or LightGBM inference
            return float(self.model.predict(features)[0])

    def train(self, X_train, y_train):
        """Trains the prediction model."""
        logger.info(f"Training {self.model_type} on historical traffic data...")
        if self.model_type == "random_forest":
            self.model = RandomForestRegressor(n_estimators=100)
            self.model.fit(X_train, y_train)
        elif self.model_type == "lightgbm" and lgb:
            self.model = lgb.LGBMRegressor()
            self.model.fit(X_train, y_train)
        elif self.model_type == "lstm":
            # Simplified LSTM training loop for prototype
            self.model = LSTMModel(input_dim=X_train.shape[-1], hidden_dim=64)
            # Training logic here...
            pass
        logger.info("Model training complete.")

    def save_model(self, path):
        """Saves the trained model to disk."""
        if self.model_type == "lstm":
            torch.save(self.model.state_dict(), path)
        else:
            with open(path, 'wb') as f:
                pickle.dump(self.model, f)
        logger.info(f"Model saved to {path}")

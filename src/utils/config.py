import yaml
import os

class Config:
    def __init__(self, config_path="config.yaml"):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value

# Sample default config.yaml content
DEFAULT_CONFIG = {
    "detection": {
        "model_path": "models/yolo/yolov8n.pt",
        "confidence": 0.5,
        "classes": [2, 3, 5, 7]  # car, motorcycle, bus, truck
    },
    "simulation": {
        "sumo_cfg": "simulation/intersection_config.sumocfg",
        "step_length": 0.1
    },
    "optimization": {
        "min_green": 10,
        "max_green": 60,
        "base_time": 20
    },
    "database": {
        "url": "sqlite:///data/traffic_data.db"
    }
}

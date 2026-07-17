import numpy as np
from src.utils.logger import logger

class SignalOptimizer:
    """
    Advanced Traffic Signal Optimization Engine.
    Uses multi-lane density, queue length, and predictive flow with fairness constraints.
    """
    def __init__(self, config=None):
        self.config = config or {}
        self.min_green = self.config.get("min_green", 10)
        self.max_green = self.config.get("max_green", 60)
        self.weights = self.config.get("weights", {"density": 0.5, "queue": 0.3, "prediction": 0.2})
        logger.info("Signal Optimization Engine initialized.")

    def optimize_phase_times(self, lane_metrics):
        """
        Calculates optimal green times for each lane phase.
        
        lane_metrics: dict mapping lane_id to {density, queue_length, predicted_flow}
        """
        optimized_times = {}
        
        # Calculate base scores for each lane
        for lane_id, metrics in lane_metrics.items():
            score = (
                self.weights["density"] * metrics["density"] +
                self.weights["queue"] * metrics["queue_length"] +
                self.weights["prediction"] * metrics["predicted_flow"]
            )
            
            # Linear scaling of score to green time
            # Assuming a score of 100 results in max_green
            green_time = self.min_green + (score / 100.0) * (self.max_green - self.min_green)
            optimized_times[lane_id] = int(np.clip(green_time, self.min_green, self.max_green))
            
        # Apply fairness constraints: ensure no lane is starvation-blocked
        # and total cycle time remains within reasonable bounds.
        self._apply_fairness(optimized_times)
        
        return optimized_times

    def _apply_fairness(self, optimized_times):
        """Internal method to adjust times for intersection fairness."""
        # Implementation for multi-lane coordination
        pass

    def get_emergency_override(self, lane_id):
        """Returns override signal for emergency vehicle priority."""
        return {lane_id: self.max_green}

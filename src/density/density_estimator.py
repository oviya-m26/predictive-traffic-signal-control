from src.utils.logger import logger

class DensityEstimator:
    """
    Module for calculating weighted vehicle density per lane.
    Weights are assigned based on vehicle size and impact on traffic flow.
    """
    def __init__(self, weights=None):
        self.weights = weights or {
            "bicycle": 0.5,
            "motorcycle": 0.8,
            "car": 1.0,
            "truck": 2.0,
            "bus": 3.0,
            "ambulance": 10.0
        }
        logger.info(f"Density estimator initialized with weights: {self.weights}")

    def calculate_weighted_density(self, detections):
        """
        Calculates weighted density for each lane.
        Formula: weighted_density = Σ(vehicle_count × weight)
        """
        lane_densities = {}
        
        for det in detections:
            lane_id = det.get("lane_id")
            if not lane_id:
                continue
                
            vehicle_type = det.get("vehicle_type")
            weight = self.weights.get(vehicle_type, 1.0)
            
            if lane_id not in lane_densities:
                lane_densities[lane_id] = 0.0
                
            lane_densities[lane_id] += weight
            
        return lane_densities

    def log_densities(self, densities):
        """Helper to log current densities"""
        for lane_id, density in densities.items():
            logger.info(f"Lane {lane_id}: Current weighted density = {density:.2f}")

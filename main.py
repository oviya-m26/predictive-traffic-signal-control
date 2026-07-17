import cv2
import time
from src.utils.config import Config
from src.utils.logger import logger
from src.detection.vehicle_detector import VehicleDetector
from src.lane_mapping.lane_mapper import LaneMapper
from src.density.density_estimator import DensityEstimator
from src.queue.queue_estimator import QueueEstimator
from src.prediction.traffic_predictor import TrafficPredictor
from src.signal_control.signal_optimizer import SignalOptimizer
from src.emergency.emergency_detector import EmergencyDetector
from src.database.db_manager import DBManager
from src.digital_twin.twin_manager import TrafficDigitalTwin

def main_pipeline(video_path=0, max_frames=50):
    """
    Research-grade Predictive Traffic Signal Control Pipeline with Digital Twin integration.
    """
    config = Config("config.yaml")
    
    # Initialize Core Modules
    detector = VehicleDetector(config.get("detection.model_path"))
    lane_mapper = LaneMapper(config.get("lane_mapping.lanes"))
    density_estimator = DensityEstimator()
    queue_estimator = QueueEstimator()
    predictor = TrafficPredictor(model_type="random_forest")
    optimizer = SignalOptimizer(config.get("optimization"))
    emergency_detector = EmergencyDetector()
    
    # Initialize Database & Digital Twin
    db = DBManager(config.get("database.url"))
    digital_twin = TrafficDigitalTwin(db)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logger.error(f"Could not open video source: {video_path}")
        return

    logger.info(f"Traffic Signal Pipeline Started on {video_path}.")
    frame_count = 0

    while cap.isOpened() and frame_count < max_frames:
        ret, frame = cap.read()
        if not ret: break
        
        frame_count += 1
        
        # 1. Detection & Tracking
        detections = detector.detect(frame)
        
        # 2. Lane Mapping
        for det in detections:
            lane_id, dist = lane_mapper.assign_vehicle_to_lane(det["bounding_box"])
            det["lane_id"] = lane_id
            det["distance_from_stop_line"] = dist # Corrected key
            
        # 3. Analytics: Density & Queue
        lane_densities = density_estimator.calculate_weighted_density(detections)
        queue_stats = queue_estimator.estimate_queue_length(detections)
        
        # 4. Emergency Prioritization
        emergency_events = emergency_detector.detect_emergency_vehicles(detections)
        override_needed, priority_lane = emergency_detector.override_signal(emergency_events)
        
        # 5. Prediction & Optimization
        lane_data = {}
        for lane in config.get("lane_mapping.lanes"):
            lane_id = lane["id"]
            features = [lane_densities.get(lane_id, 0.0), queue_stats.get(lane_id, {}).get("queue_length", 0)]
            pred_count = predictor.predict(predictor.prepare_features(features))
            
            lane_data[lane_id] = {
                "density": lane_densities.get(lane_id, 0.0),
                "queue_length": queue_stats.get(lane_id, {}).get("queue_length", 0),
                "predicted_flow": pred_count
            }
            
            # 6. Synchronize Digital Twin State
            digital_twin.update_state(
                lane_id=lane_id,
                vehicle_count=len([d for d in detections if d["lane_id"] == lane_id]),
                queue_length=lane_data[lane_id]["queue_length"],
                avg_wait_time=0.0,
                signal_state="GREEN" if override_needed and lane_id == priority_lane else "AUTO",
                predicted_flow=pred_count
            )

        if override_needed:
            optimized_times = optimizer.get_emergency_override(priority_lane)
            print(f"Frame {frame_count}: EMERGENCY OVERRIDE for lane {priority_lane}")
        else:
            optimized_times = optimizer.optimize_phase_times(lane_data)

        # Output progress every 10 frames
        if frame_count % 10 == 0:
            print(f"Frame {frame_count}: Detections={len(detections)}, Densities={lane_densities}, Optimized Times={optimized_times}")

    cap.release()
    logger.info("Traffic Signal Pipeline Terminated.")

def run_single_image_test(image_path):
    """Test the pipeline on a single image and output results."""
    config = Config("config.yaml")
    detector = VehicleDetector(config.get("detection.model_path"))
    lane_mapper = LaneMapper(config.get("lane_mapping.lanes"))
    density_estimator = DensityEstimator()
    queue_estimator = QueueEstimator()
    predictor = TrafficPredictor(model_type="random_forest")
    optimizer = SignalOptimizer(config.get("optimization"))
    emergency_detector = EmergencyDetector()
    db = DBManager(config.get("database.url"))
    digital_twin = TrafficDigitalTwin(db)

    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not read image {image_path}")
        return

    detections = detector.detect(frame)
    
    # MOCK DATA INJECTION FOR DEMO IF NO DETECTIONS FOUND
    if len(detections) == 0:
        print("Note: No vehicles detected by model. Injecting mock traffic for demo output...")
        # Simulate some traffic
        lane_densities = {"lane_1": 15.5, "lane_2": 4.2}
        queue_stats = {"lane_1": {"queue_length": 8}, "lane_2": {"queue_length": 2}}
    else:
        for det in detections:
            lane_id, dist = lane_mapper.assign_vehicle_to_lane(det["bounding_box"])
            det["lane_id"] = lane_id
            det["distance_from_stop_line"] = dist

        lane_densities = density_estimator.calculate_weighted_density(detections)
        queue_stats = queue_estimator.estimate_queue_length(detections)
    
    lane_data = {}
    for lane in config.get("lane_mapping.lanes"):
        lane_id = lane["id"]
        density = lane_densities.get(lane_id, 0.0)
        queue_len = queue_stats.get(lane_id, {}).get("queue_length", 0)
        
        features = [density, queue_len]
        pred_count = predictor.predict(predictor.prepare_features(features))
        
        lane_data[lane_id] = {
            "density": density,
            "queue_length": queue_len,
            "predicted_flow": pred_count
        }
    
    optimized_times = optimizer.optimize_phase_times(lane_data)
    print("\n--- TRAFFIC CONTROL ANALYSIS ---")
    print(f"Source: {image_path}")
    print(f"Vehicles Processed: {len(detections) if len(detections) > 0 else 'Mocked for demo'}")
    for lane_id, data in lane_data.items():
        print(f"\n{lane_id.upper()}:")
        print(f"  > Traffic Density Score: {data['density']:.2f}")
        print(f"  > Current Queue Length: {data['queue_length']} vehicles")
        print(f"  > Predicted Flow (Next Cycle): {data['predicted_flow']:.2f}")
        print(f"  > CALCULATED GREEN TIME: {optimized_times.get(lane_id)} seconds")
    print("\n--------------------------------\n")

if __name__ == "__main__":
    # Try running on the intersection image for better demo output
    import os
    img_path = "../images/intersection.jpg"
    if os.path.exists(img_path):
        print(f"Running analysis on {img_path}...")
        run_single_image_test(img_path)
    else:
        print("Running analysis on Demo.gif...")
        main_pipeline(video_path="../Demo.gif", max_frames=5)



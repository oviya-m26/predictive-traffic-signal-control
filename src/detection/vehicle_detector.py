import cv2
import time
from ultralytics import YOLO
from src.utils.logger import logger

class VehicleDetector:
    """
    Module for vehicle detection using YOLOv8.
    Detects cars, buses, trucks, motorcycles, bicycles, and ambulances.
    """
    def __init__(self, model_path="yolov8n.pt", confidence=0.5):
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.classes = {
            2: "car",
            3: "motorcycle",
            5: "bus",
            7: "truck",
            0: "person",  # Sometimes useful for safety
            1: "bicycle"
        }
        # Assuming YOLO has a special class or you can define one for ambulances
        # For standard YOLOv8 COCO, ambulances might be detected as 'truck' or 'car'.
        # For academic prototype, we'll simulate a class if needed or use a specific model.
        logger.info(f"Vehicle detector initialized with {model_path}")

    def detect(self, frame):
        """
        Processes a video frame and returns a list of detected vehicles.
        """
        results = self.model.predict(frame, conf=self.confidence, verbose=False)
        detections = []
        
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                if cls_id in self.classes:
                    detection = {
                        "vehicle_id": None, # Will be set by tracker
                        "vehicle_type": self.classes[cls_id],
                        "bounding_box": box.xyxy[0].tolist(),
                        "confidence": float(box.conf[0]),
                        "timestamp": time.time(),
                        "lane_id": None # Will be set by lane mapper
                    }
                    detections.append(detection)
        
        return detections

    def draw_detections(self, frame, detections):
        """Helper to draw bounding boxes on frame"""
        for det in detections:
            x1, y1, x2, y2 = map(int, det["bounding_box"])
            label = f"{det['vehicle_type']} {det['confidence']:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return frame

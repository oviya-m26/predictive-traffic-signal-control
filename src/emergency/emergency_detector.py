from src.utils.logger import logger

class EmergencyDetector:
    """
    Module for detecting emergency vehicles and overriding traffic signals.
    """
    def __init__(self, emergency_classes=None):
        self.emergency_classes = emergency_classes or ["ambulance", "fire truck", "police car"]
        logger.info(f"Emergency detector initialized with classes: {self.emergency_classes}")

    def detect_emergency_vehicles(self, detections):
        """
        Detects ambulances and other emergency vehicles in detections.
        """
        emergency_events = []
        for det in detections:
            vehicle_type = det.get("vehicle_type")
            if vehicle_type in self.emergency_classes:
                event = {
                    "lane_id": det.get("lane_id"),
                    "vehicle_type": vehicle_type,
                    "confidence": det.get("confidence"),
                    "timestamp": det.get("timestamp")
                }
                emergency_events.append(event)
                logger.warning(f"EMERGENCY VEHICLE DETECTED: {vehicle_type} in lane {event['lane_id']}")
                
        return emergency_events

    def override_signal(self, emergency_events):
        """
        Returns signal override flag and lane to prioritize.
        """
        if emergency_events:
            # Prioritize the lane with the first detected emergency vehicle
            override_flag = True
            priority_lane = emergency_events[0]["lane_id"]
            return override_flag, priority_lane
            
        return False, None

    def log_event(self, event):
        """Logs emergency events to the database or system log"""
        logger.warning(f"EMERGENCY EVENT LOGGED: {event['vehicle_type']} at {event['timestamp']}")

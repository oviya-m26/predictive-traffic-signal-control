import cv2
import numpy as np
from src.utils.logger import logger

class LaneMapper:
    """
    Module for mapping vehicle detections to predefined lane regions.
    """
    def __init__(self, lanes_config=None):
        self.lanes = lanes_config or []
        logger.info(f"Lane mapper initialized with {len(self.lanes)} lanes")

    def is_inside_polygon(self, point, polygon):
        """
        Uses OpenCV to check if a point is inside a polygon region.
        """
        result = cv2.pointPolygonTest(np.array(polygon), (point[0], point[1]), False)
        return result >= 0

    def assign_vehicle_to_lane(self, vehicle_bbox):
        """
        Assigns a vehicle detection (bounding box) to a lane ID.
        Uses the bottom-center point of the bounding box as the vehicle's position.
        """
        x1, y1, x2, y2 = vehicle_bbox
        bottom_center = [(x1 + x2) / 2, y2]
        
        for lane in self.lanes:
            if self.is_inside_polygon(bottom_center, lane["polygon"]):
                # Calculate distance from stop line (assuming stop line is at bottom of polygon)
                # This is a simple heuristic: the y-distance to the bottom edge of the lane
                dist_from_stop_line = abs(y2 - max([p[1] for p in lane["polygon"]]))
                return lane["id"], dist_from_stop_line
        
        return "unassigned", 0.0

    def draw_lanes(self, frame):
        """Helper to visualize lane polygons"""
        for lane in self.lanes:
            polygon = np.array(lane["polygon"], dtype=np.int32)
            cv2.polylines(frame, [polygon], True, (255, 0, 0), 2)
            cv2.putText(frame, lane["id"], (polygon[0][0], polygon[0][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        return frame

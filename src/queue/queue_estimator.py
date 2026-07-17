from src.utils.logger import logger

class QueueEstimator:
    """
    Module for estimating queue length and average waiting time per lane.
    Detects stopped vehicles near the stop line.
    """
    def __init__(self, stop_threshold=5.0, distance_threshold=20.0):
        self.stop_threshold = stop_threshold  # pixels per frame or distance-based
        self.distance_threshold = distance_threshold # distance from stop line
        logger.info(f"Queue estimator initialized with stop_threshold: {stop_threshold}, distance_threshold: {distance_threshold}")

    def estimate_queue_length(self, detections):
        """
        Estimates queue length based on stopped vehicles near the stop line.
        Conditions: speed < threshold, distance_to_stopline < region.
        """
        queue_stats = {}
        
        for det in detections:
            lane_id = det.get("lane_id")
            if not lane_id:
                continue
                
            distance = det.get("distance_from_stop_line", 0.0)
            # Assuming speed is 0.0 if not tracked. In real-world, we'd use tracker speed.
            speed = det.get("speed", 0.0)
            
            if lane_id not in queue_stats:
                queue_stats[lane_id] = {
                    "queue_length": 0,
                    "avg_wait_time": 0.0,
                    "stopped_vehicles": 0
                }
            
            if speed < self.stop_threshold and distance < self.distance_threshold:
                queue_stats[lane_id]["queue_length"] += 1
                queue_stats[lane_id]["stopped_vehicles"] += 1
                # Simplified wait time calculation (needs actual tracker data for real wait time)
                queue_stats[lane_id]["avg_wait_time"] += 1.0 # arbitrary increment
                
        return queue_stats

    def log_queue_stats(self, queue_stats):
        """Helper to log current queue stats"""
        for lane_id, stats in queue_stats.items():
            logger.info(f"Lane {lane_id}: Current queue length = {stats['queue_length']}, avg wait time = {stats['avg_wait_time']:.2f}s")

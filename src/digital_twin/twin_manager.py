from datetime import datetime
from src.utils.logger import logger

class TrafficDigitalTwin:
    """
    Manager for the Traffic Digital Twin system.
    Replicates real-time intersection states for analysis, replaying, and optimization.
    """
    def __init__(self, db_manager):
        self.db = db_manager
        self.current_state = {}
        logger.info("Traffic Digital Twin Manager initialized.")

    def update_state(self, lane_id, vehicle_count, queue_length, avg_wait_time, signal_state, predicted_flow):
        """
        Updates the virtual replica of the intersection state.
        """
        state_entry = {
            "timestamp": datetime.now(),
            "lane_id": lane_id,
            "vehicle_count": vehicle_count,
            "queue_length": queue_length,
            "avg_wait_time": avg_wait_time,
            "signal_state": signal_state,
            "predicted_flow": predicted_flow
        }
        
        self.current_state[lane_id] = state_entry
        
        # Persist to Digital Twin table
        self.db.save_digital_twin_state(state_entry)
        
    def get_lane_history(self, lane_id, limit=100):
        """
        Retrieves historical states for a specific lane from the Digital Twin.
        """
        return self.db.get_digital_twin_history(lane_id, limit)

    def sync_with_simulation(self, sumo_data):
        """
        Synchronizes the digital twin state with external simulation data (e.g., SUMO).
        """
        logger.info("Synchronizing Digital Twin with SUMO simulation...")
        # Implementation for real-time sync
        pass

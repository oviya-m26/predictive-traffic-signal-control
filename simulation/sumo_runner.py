import os
import sys
import optparse
from src.utils.logger import logger

# Try to import traci for SUMO interaction
try:
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")
    import traci
except ImportError:
    traci = None
    logger.warning("traci not found. SUMO simulation runner will not work.")

class SUMORunner:
    """
    Module for running and interacting with the SUMO traffic simulation.
    Tests three control strategies: fixed signal timing, density-based control, and predictive control.
    """
    def __init__(self, sumo_cfg="simulation/intersection_config.sumocfg", gui=False):
        self.sumo_cfg = sumo_cfg
        self.gui = gui
        self.sumo_cmd = ["sumo-gui" if gui else "sumo", "-c", sumo_cfg]
        logger.info(f"SUMO runner initialized with {sumo_cfg}")

    def start(self):
        """Starts the SUMO simulation"""
        if traci:
            traci.start(self.sumo_cmd)
            logger.info("SUMO simulation started")
        else:
            logger.error("Cannot start SUMO: traci not available")

    def run_step(self):
        """Advances the simulation by one step"""
        if traci:
            traci.simulationStep()
            # Collect data from SUMO
            # Example: vehicle_ids = traci.vehicle.getIDList()
            # return vehicle_ids
            return True
        return False

    def get_lane_vehicle_count(self, lane_id):
        """Gets the number of vehicles on a specific lane in SUMO"""
        if traci:
            return traci.lane.getLastStepVehicleNumber(lane_id)
        return 0

    def set_signal_timing(self, traffic_light_id, state):
        """Sets the traffic light state (e.g., green, red) in SUMO"""
        if traci:
            traci.trafficlight.setRedYellowGreenState(traffic_light_id, state)
            logger.info(f"Signal timing set for {traffic_light_id}: {state}")

    def stop(self):
        """Stops the SUMO simulation"""
        if traci:
            traci.close()
            logger.info("SUMO simulation stopped")

    def run_strategy(self, strategy_name, steps=1000):
        """
        Runs a simulation strategy and collects performance metrics.
        Strategies: fixed, density, predictive.
        """
        logger.info(f"Running strategy: {strategy_name} for {steps} steps")
        self.start()
        
        metrics = {
            "total_wait_time": 0.0,
            "total_fuel_wastage": 0.0,
            "avg_queue_length": 0.0
        }
        
        for step in range(steps):
            self.run_step()
            # Update metrics here
            
        self.stop()
        logger.info(f"Strategy {strategy_name} completed. Final metrics: {metrics}")
        return metrics

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from src.utils.logger import logger

Base = declarative_base()

class TrafficState(Base):
    """Digital Twin Traffic State Table"""
    __tablename__ = 'traffic_state'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    lane_id = Column(String)
    vehicle_count = Column(Integer)
    queue_length = Column(Integer)
    avg_wait_time = Column(Float)
    signal_state = Column(String)
    predicted_flow = Column(Float)

class EmergencyEvent(Base):
    """Emergency Vehicle Logs Table"""
    __tablename__ = 'emergency_events'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    lane_id = Column(String)
    vehicle_type = Column(String)
    action_taken = Column(String)

class DBManager:
    """
    Enhanced Database Manager for Research-grade Traffic System and Digital Twin.
    """
    def __init__(self, db_url="sqlite:///data/traffic_digital_twin.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        logger.info(f"Research DB Manager initialized with {db_url}")

    def save_digital_twin_state(self, state_entry):
        session = self.Session()
        state = TrafficState(**state_entry)
        session.add(state)
        session.commit()
        session.close()

    def get_digital_twin_history(self, lane_id, limit=100):
        session = self.Session()
        history = session.query(TrafficState).filter(TrafficState.lane_id == lane_id).order_by(TrafficState.timestamp.desc()).limit(limit).all()
        session.close()
        return history

    def log_emergency_event(self, lane_id, vehicle_type, action):
        session = self.Session()
        event = EmergencyEvent(lane_id=lane_id, vehicle_type=vehicle_type, action_taken=action)
        session.add(event)
        session.commit()
        session.close()

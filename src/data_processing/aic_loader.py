import os
import cv2
import pandas as pd
from src.utils.logger import logger

class AICityChallengeLoader:
    """
    Loader and Preprocessor for the AI City Challenge Dataset (CityFlow).
    Note: You must register and download the dataset from https://www.aicitychallenge.org/
    before using this loader.
    """
    def __init__(self, raw_data_dir, processed_data_dir):
        self.raw_data_dir = raw_data_dir
        self.processed_data_dir = processed_data_dir
        if not os.path.exists(self.processed_data_dir):
            os.makedirs(self.processed_data_dir)
        logger.info(f"AI City Challenge Loader initialized. Raw: {raw_data_dir}, Processed: {processed_data_dir}")

    def extract_frames(self, video_filename, frame_interval=30):
        """
        Extracts frames from an AI City Challenge video and saves them for processing.
        """
        video_path = os.path.join(self.raw_data_dir, video_filename)
        if not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            return
            
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        extracted_count = 0
        
        # Create a specific directory for the video frames
        video_name = os.path.splitext(video_filename)[0]
        output_dir = os.path.join(self.processed_data_dir, video_name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_count % frame_interval == 0:
                frame_path = os.path.join(output_dir, f"frame_{frame_count:06d}.jpg")
                cv2.imwrite(frame_path, frame)
                extracted_count += 1
                
            frame_count += 1
            
        cap.release()
        logger.info(f"Extracted {extracted_count} frames from {video_filename} to {output_dir}")

    def parse_detections(self, det_filename):
        """
        Parses AIC detection format (MOT format: frame, id, x, y, w, h, score, -1, -1, -1).
        """
        det_path = os.path.join(self.raw_data_dir, det_filename)
        if not os.path.exists(det_path):
            logger.error(f"Detection file not found: {det_path}")
            return None
            
        # AICity detections are often space-separated or comma-separated
        df = pd.read_csv(det_path, header=None, names=['frame', 'id', 'x', 'y', 'w', 'h', 'score', 'c1', 'c2', 'c3'])
        logger.info(f"Parsed {len(df)} detection records from {det_filename}")
        return df

    def organize_by_lane(self, detections_df, lane_mapper):
        """
        Uses the lane mapper to categorize historical detections by lane.
        Useful for generating traffic density training data.
        """
        # This function would take the bounding boxes from detections_df
        # and assign them to lanes, creating a time-series dataset of lane counts.
        pass

if __name__ == "__main__":
    # Example usage (after user downloads the data)
    loader = AICityChallengeLoader(
        raw_data_dir="data/datasets/aic_raw",
        processed_data_dir="data/processed/aic_processed"
    )
    # loader.extract_frames("S01_c001.mp4")

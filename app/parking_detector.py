import cv2
import numpy as np

class ParkingDetector:
    def __init__(self, min_area=1000, threshold=0.5):
        self.min_area = min_area
        self.threshold = threshold
        self.background = None
    
    def set_background(self, frame):
        """Set background for background subtraction"""
        self.background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.background = cv2.GaussianBlur(self.background, (21, 21), 0)
    
    def detect_slot_occupied(self, roi):
        """Detect if a parking slot is occupied using multiple methods"""
        # Method 1: Edge Detection
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_count = np.sum(edges > 0)
        
        # Method 2: Background Subtraction (if background is set)
        bg_diff = 0
        if self.background is not None:
            # Resize background to match ROI
            bg_roi = self.background[:roi.shape[0], :roi.shape[1]]
            diff = cv2.absdiff(gray, bg_roi)
            diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
            bg_diff = np.sum(diff > 0)
        
        # Method 3: Color Analysis (check for car colors)
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        # Count pixels that are not road color
        lower_road = np.array([0, 0, 50])
        upper_road = np.array([180, 50, 200])
        mask = cv2.inRange(hsv, lower_road, upper_road)
        road_pixels = np.sum(mask > 0)
        total_pixels = roi.shape[0] * roi.shape[1]
        non_road_ratio = 1 - (road_pixels / total_pixels)
        
        # Combined decision
        edge_ratio = edge_count / total_pixels
        bg_ratio = bg_diff / total_pixels if bg_diff > 0 else 0
        
        # Weighted score
        score = (edge_ratio * 0.4 + bg_ratio * 0.4 + non_road_ratio * 0.2)
        
        return score > self.threshold, score
    
    def process_frame(self, frame, slot_positions):
        """Process frame and detect occupancy for all slots"""
        results = {}
        annotated = frame.copy()
        
        for slot in slot_positions:
            x1, y1, x2, y2 = slot['x1'], slot['y1'], slot['x2'], slot['y2']
            roi = frame[y1:y2, x1:x2]
            
            if roi.size > 0:
                occupied, score = self.detect_slot_occupied(roi)
                results[slot['id']] = occupied
                
                # Draw annotation
                color = (0, 0, 255) if occupied else (0, 255, 0)
                cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
                cv2.putText(annotated, f"Slot {slot['id']}: {score:.2f}",
                           (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX,
                           0.5, (255, 255, 255), 1)
        
        return annotated, results

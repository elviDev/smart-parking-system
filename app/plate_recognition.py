import cv2
import numpy as np
import easyocr
import re

class PlateRecognizer:
    def __init__(self):
        # Initialize EasyOCR reader
        self.reader = easyocr.Reader(['en'], gpu=False)
    
    def detect_plate(self, image):
        """Detect license plate in image"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Use EasyOCR to read text
        results = self.reader.readtext(gray)
        
        plates = []
        for (bbox, text, confidence) in results:
            # Filter by confidence and text length
            if confidence > 0.5 and len(text) >= 4:
                # Clean the text
                clean_text = re.sub(r'[^A-Z0-9]', '', text.upper())
                if len(clean_text) >= 4:
                    plates.append({
                        'text': clean_text,
                        'confidence': confidence,
                        'bbox': bbox
                    })
        
        return plates
    
    def draw_plate_boxes(self, image, plates):
        """Draw bounding boxes around detected plates"""
        img_copy = image.copy()
        for plate in plates:
            bbox = plate['bbox']
            text = plate['text']
            confidence = plate['confidence']
            
            # Draw polygon
            pts = np.array(bbox, dtype=np.int32)
            cv2.polylines(img_copy, [pts], True, (0, 255, 0), 2)
            
            # Draw label
            x, y = bbox[0]
            cv2.putText(img_copy, f"{text} ({confidence:.2f})", 
                       (int(x), int(y)-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return img_copy

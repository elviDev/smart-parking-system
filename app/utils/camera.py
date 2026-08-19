import cv2
import time
from threading import Thread

class Camera:
    def __init__(self, source=0, width=640, height=480):
        self.source = source
        self.width = width
        self.height = height
        self.cap = None
        self.frame = None
        self.is_running = False
        self.thread = None
    
    def start(self):
        """Start the camera thread"""
        if self.is_running:
            return
        
        self.cap = cv2.VideoCapture(self.source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        if not self.cap.isOpened():
            raise Exception("Could not open camera")
        
        self.is_running = True
        self.thread = Thread(target=self._update, daemon=True)
        self.thread.start()
    
    def _update(self):
        """Update frame in background thread"""
        while self.is_running:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame
            time.sleep(0.03)  # ~30 FPS
    
    def get_frame(self):
        """Get the latest frame"""
        if self.frame is not None:
            return self.frame.copy()
        return None
    
    def stop(self):
        """Stop the camera"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1)
        if self.cap:
            self.cap.release()
    
    def __del__(self):
        self.stop()

import cv2
import numpy as np


class HandDetector:
    def __init__(self):
        # HSV range for skin color detection
        self.lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        self.upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        # Kernel for morphological operations (reduced size for performance)
        self.kernel = np.ones((3, 3), np.uint8)
        
    def detect_hand(self, frame):
        """
        Detect hand in the frame using HSV skin segmentation
        
        Args:
            frame: Input image frame from webcam
            
        Returns:
            tuple: (contour, centroid) or (None, None) if no hand detected
        """
        # Resize frame for faster processing (half size)
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        
        # Convert BGR to HSV
        hsv = cv2.cvtColor(small_frame, cv2.COLOR_BGR2HSV)
        
        # Threshold the HSV image to get only skin colors
        mask = cv2.inRange(hsv, self.lower_skin, self.upper_skin)
        
        # Apply morphological transformations to clean up the mask
        # Reduced iterations for performance
        mask = cv2.dilate(mask, self.kernel, iterations=2)
        mask = cv2.erode(mask, self.kernel, iterations=1)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # If no contours found, return None
        if not contours:
            return None, None
            
        # Find the largest contour (assumed to be the hand)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Filter out very small contours
        if cv2.contourArea(largest_contour) < 500:
            return None, None
        
        # Calculate centroid using image moments
        moments = cv2.moments(largest_contour)
        if moments["m00"] != 0:
            # Scale coordinates back to original frame size
            cx = int(moments["m10"] / moments["m00"]) * 2
            cy = int(moments["m01"] / moments["m00"]) * 2
            centroid = (cx, cy)
        else:
            # Fallback if moments are zero
            x, y, w, h = cv2.boundingRect(largest_contour)
            # Scale coordinates back to original frame size
            centroid = (x + w // 2) * 2, (y + h // 2) * 2
            
        # Scale contour back to original frame size
        scaled_contour = largest_contour * 2
        
        return scaled_contour, centroid
    
    def draw_detection(self, frame, contour, centroid):
        """
        Draw the detected hand contour and centroid on the frame
        
        Args:
            frame: Image frame to draw on
            contour: Hand contour
            centroid: Hand centroid coordinates
            
        Returns:
            frame: Frame with drawings
        """
        if contour is not None and centroid is not None:
            # Draw contour
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
            
            # Draw centroid
            cv2.circle(frame, centroid, 5, (255, 0, 0), -1)
            
            # Draw bounding rectangle around hand
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            
        return frame
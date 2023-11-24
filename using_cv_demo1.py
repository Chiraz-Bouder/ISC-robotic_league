import numpy as np
import cv2
from threading import Thread  # Import the Thread class for multithreading

class line_follow():
    def __init__(self):
        # Initialize attributes for centroid coordinates, line detection status, and frame
        self.cx = None
        self.cy = None
        self.no_line = False
        self.frame = None


    def start(self):
        # Start the thread
        Thread(target=self.run, args=()).start()
        return self

    def run(self):
        while True:
            # Crop the image to the region of interest
            crop_img = self.frame[60:120, 0:160]
            
            # Convert the cropped image to grayscale
            gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur to the grayscale image
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Threshold the blurred image to create a binary image
            ret, thresh1 = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
            
            # Erode and dilate to remove noise and enhance the detected lines
            mask = cv2.erode(thresh1, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            
            # Find contours in the binary image
            contours, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
            
            # Find the largest contour (if any)
            if len(contours) > 0:
                c = max(contours, key=cv2.contourArea)
                M = cv2.moments(c)
                
                # Calculate centroid coordinates
                self.cx = int(M['m10'] / M['m00'])
                self.cy = int(M['m01'] / M['m00'])
            else:
                # If no contour is detected, set no_line to True
                self.no_line = True

    def stop(self):
        pass  



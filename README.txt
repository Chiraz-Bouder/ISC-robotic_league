mainLineFollower:
Contains the main logic for the robot.
Starts threads for camera input, color detection, line following, and distance sensing.
Implements the core behavior of the robot, including starting, stopping, and moving based on various conditions.


colorprint:
Module for color detection.
Defines a scanColor class that uses threading to detect colors from the camera feed.
Detects colors (red, green, blue) and assigns a color label.


HSV_thresholder:
Script for finding HSV range of a target object.
Uses OpenCV to create a window with trackbars for adjusting HSV values.
Helps in tuning the color thresholding parameters for color detection.


IRsensor:
Controlling the robot with infrared sensors.
Uses GPIO and the gpiozero library to control robot movements based on IR readings.
Demonstrates basic obstacle avoidance or line following behavior.


using_cv_demo_1:
Module for line following using computer vision.
Defines a line_follow class that uses OpenCV to follow a line on the ground.
Uses grayscale conversion, Gaussian blur, thresholding, and contour detection.


using_cv_demo_2:
Script for line following using computer vision.
Uses OpenCV and GPIO to follow a line on the ground.
Involves capturing frames, converting to grayscale, applying a mask, finding contours, and adjusting robot movements based on the line position.


Crossing Code:
Implements distance sensing using ultrasonic sensors.
Utilizes GPIO pins and ultrasonic sensors to measure distances.
Calculates the time of flight for ultrasonic waves.
Converts time of flight to distance and updates the distance attribute.


Camera Input Code:
Captures frames from the webcam for processing.
Utilizes OpenCV to access and read frames from the webcam.
Runs as a separate thread to continuously update the frame attribute.

init:
Contains type hints and aliases for various data structures and types used in the OpenCV library.
Provides clear and consistent annotations for functions and methods using these types in OpenCV-related code.
Enhances code readability and provides information about expected data types.
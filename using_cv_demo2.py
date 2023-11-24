import cv2
import numpy as np
import RPi.GPIO as GPIO

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(3, 160)  # Set width
cap.set(4, 120)  # Set height

# Define GPIO pins for motor control
in1 = 4
in2 = 17
in3 = 27
in4 = 22
en1 = 23
en2 = 24

# Set up GPIO mode and pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(en1, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

# Initialize PWM for motor speed control
p1 = GPIO.PWM(en1, 100)
p2 = GPIO.PWM(en2, 100)
p1.start(50)
p2.start(50)

# Set initial motor directions
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Define color thresholding parameters
    low_b = np.uint8([0, 0, 0])
    high_b = np.uint8([5, 5, 5])

    # Create a binary mask based on color thresholding
    mask = cv2.inRange(frame, low_b, high_b)

    # Find contours in the binary mask
    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)

    # Check if contours are found
    if len(contours) > 0:
        # Find the largest contour
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        # Calculate centroid coordinates
        if M["m00"] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            print("CX: " + str(cx) + "  CY: " + str(cy))

            # Motor control based on centroid position
            if cx >= 120:
                print("Turn Left")
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)
                GPIO.output(in3, GPIO.LOW)
                GPIO.output(in4, GPIO.HIGH)
            elif 40 < cx < 120:
                print("On Track!")
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)
                GPIO.output(in3, GPIO.HIGH)
                GPIO.output(in4, GPIO.LOW)
            elif cx <= 40:
                print("Turn Right")
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.HIGH)
                GPIO.output(in3, GPIO.HIGH)
                GPIO.output(in4, GPIO.LOW)

            # Draw a circle at the centroid position
            cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)
    else:
        # If no contours are found, stop the motors
        print("I don't see the line")
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)

    # Draw contours on the original frame
    if len(contours) > 0:
        cv2.drawContours(frame, c, -1, (0, 255, 0), 1)

    # Display the binary mask and original frame
    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)

    # Check for keyboard input to exit the loop
    if cv2.waitKey(1) & 0xff == ord('q'):
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)
        break

# Release camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()

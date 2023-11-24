# Import necessary modules
from colorDetection.colorprint import scanColor
from lineDetection.using_cv_demo1 import line_follow, no_line
from crossing import distance
from cameraInput import camera
from threading import Thread
from gpiozero import GPIO
import time 


# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Initialize threads
cameraThread = camera()
colorThread = scanColor()
lineThread = line_follow()
distanceThread = distance()

# Setup Output Pins
# Left Forward
GPIO.setup("P8_10", GPIO.OUT)
# Right Forward
GPIO.setup("P9_11", GPIO.OUT)
# Start the motors
GPIO.output("P8_10", GPIO.HIGH)
GPIO.output("P9_11", GPIO.HIGH)

motorsleft = 1
motorsright = 2
GPIO.setup(motorsleft, GPIO.OUT)  # Motors left
GPIO.setup(motorsright, GPIO.OUT)  # Motors right

# Define function to move forward
def forward():
    GPIO.output(motorsleft, True)
    GPIO.output(motorsright, True)

# Define function to stop
def stop(stoptime):
    GPIO.output(motorsleft, False)
    GPIO.output(motorsright, False)
    time.sleep(stoptime)
    line_follow()

# Define main function
def main():
    color = colorThread.color
    dist = distanceThread.dist
    no_line = lineThread.no_line
    cx = lineThread.cx

    if dist < 5:
        GPIO.output(motorsleft, False)
        GPIO.output(motorsright, False)

    if color == "R" or color == "G":
        stop(5000)

    if color == "B":
        stop(2000)

    if not no_line:
        if cx >= 120:
            GPIO.output("P8_10", GPIO.HIGH)
            GPIO.output("P9_11", GPIO.LOW)
        if 50 < cx < 120:
            GPIO.output("P8_10", GPIO.LOW)
            GPIO.output("P9_11", GPIO.LOW)
        if cx <= 50:
            GPIO.output("P8_10", GPIO.LOW)
            GPIO.output("P9_11", GPIO.HIGH)
    else:
        forward()
        time.sleep(1000)  # Enough time for line cut 15cm dist
        line_follow()

if __name__ == '__main__':
    # Start the threads
    distanceThread.start()
    cameraThread.start()
    colorThread.start()
    lineThread.start()

    while True:
        main()
        colorThread.frame = cameraThread.frame
        lineThread.frame = cameraThread.frame
        dist = distanceThread.dist
        time.sleep(2)

# Stop the threads when the task is done
colorThread.stop()
lineThread.stop()
distanceThread.stop()
cameraThread.stop()
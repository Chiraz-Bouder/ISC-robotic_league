import cv2
from threading import Thread
from time import sleep

class Camera(Thread):
    def __init__(self):
        # Initialize the superclass (Thread)
        super(Camera, self).__init__()

        # Attributes for storing frames and managing the webcam
        self.frame = None
        self.webcam = cv2.VideoCapture(0)
        self.on = False

    def start(self):
        # Start the thread
        super(Camera, self).start()
        return self

    def run(self):
        # The main method that runs in the thread
        self.on = True
        while self.on:
            # Read frames from the webcam
            _, self.frame = self.webcam.read()

    def stop(self):
        # Stop the thread and release resources
        self.on = False
        cv2.destroyAllWindows()
        self.webcam.release()

if __name__ == "__main__":
    # Create an instance of the Camera class
    cameraThread = Camera()
    cameraThread.start()
    sleep(1)  # Allow time for the camera to initialize

    try:
        # Main loop to display frames
        while True:
            cv2.imshow("test", cameraThread.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        # Stop the camera thread when done
        cameraThread.stop()

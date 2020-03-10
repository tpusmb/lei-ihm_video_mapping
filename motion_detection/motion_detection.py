import threading
from time import sleep

import cv2
import imutils
from imutils.video import VideoStream

from utils.config_reader import ConfigReader

WITDH = 250
DEFAULT_COLOR = (0, 255, 0)


class MotionDetection:
    """
    Motion Detection is performed with openCV

    We compare each frame with the precedent.
    To simplify comparison we transform each frame on a black/white scale then blur it.
    Then we use cv2's findContours method to retrieve bounding box of changed pixel.
    """

    def __init__(self, config_reader: ConfigReader, callback):
        """
        Create a new Threaded MotionDetection that will call the callback function on detection, once start is called
        """
        config = config_reader.Motion_detection
        self.camera_index = config.getint("camera_index", 0)
        self.sensibility = config.getint("sensibility", 100)
        self.time_between_detection = config.getint("time_between_detection", 0)
        self.callback = callback
        self._stop = True

        self._thread = None  # init when we start it, to allow motion detection to be run multiple time
        self._thread = threading.Thread(target=self.run, args=())
        self._thread.start()  # Call run()

    def run(self):
        # Reading from webcam
        cam = cv2.VideoCapture(self.camera_index)
        prev_frame = None  # Previous frame is used to compare the pixel vs the current frame
        while True:
            ret, frame = cam.read()
            frame = imutils.resize(frame, width=WITDH)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if prev_frame is None:
                prev_frame = gray
                continue  # First frame, skip processing for now

            # compute the absolute difference between the current frame and first frame
            frame_delta = cv2.absdiff(prev_frame, gray)
            thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
            # dilate the thresholded image to fill in holes, then find contours on thresholded image
            thresh = cv2.dilate(thresh, None, iterations=1)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0]

            nbr_countour = 0
            # loop over the contours
            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) >= self.sensibility:
                    nbr_countour += 1
            if nbr_countour and not self._stop:
                self.callback()
                #sleep(self.time_between_detection)
                event = threading.Event()
                event.wait(timeout=self.time_between_detection)  # Not blocking sleep
            else:
                event = threading.Event()
                event.wait(timeout=1)  # Not blocking sleep
            prev_frame = gray  # For next frame
        # cleanup the camera and close any open windows
        cam.release()

    def stop(self):
        """Stopping gracefully, might take a few seconds"""
        self._stop = True

    def start(self):
        self._stop = False

import threading
from time import sleep

import cv2
import imutils
from imutils.video import VideoStream

from utils.config_reader import ConfigReader

WITDH = 500
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
        self.debug = config.getboolean("debug", False)
        self.time_between_detection = config.getint("time_between_detection", 0)
        self.callback = callback
        self._stop = False

        self._thread = threading.Thread(target=self.run, args=())

    def run(self):
        # Reading from webcam
        vs = VideoStream(src=self.camera_index, framerate=10).start()
        prev_frame = None  # Previous frame is used to compare the pixel vs the current frame
        while not self._stop:
            frame = vs.read()
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
                if cv2.contourArea(c) < self.sensibility:
                    continue
                nbr_countour += 1
                if self.debug:
                    # compute the bounding box for the contour, draw it on the frame
                    (x, y, w, h) = cv2.boundingRect(c)

                    color = DEFAULT_COLOR
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

            if self.debug:
                cv2.putText(frame, f"Motion: {bool(nbr_countour)}", (10, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.imshow("Frame", frame)
                cv2.imshow("Gray", gray)

                key = cv2.waitKey(1)
                # if the `q` key is pressed, break from the loop
                if key == ord("q"):
                    print('stop')
                    break
            if nbr_countour:
                if self.debug:
                    print(f'nbr_countour: {nbr_countour}')
                self.callback()
                sleep(self.time_between_detection)
            prev_frame = gray  # For next frame
        # cleanup the camera and close any open windows
        vs.stop()
        cv2.destroyAllWindows()

    def stop(self):
        """Stopping gracefully, might take a few seconds"""
        self._stop = True
        if self._thread.is_alive():
            self._thread.join()

    def start(self):
        self._stop = False
        self._thread.start()  # Call run()

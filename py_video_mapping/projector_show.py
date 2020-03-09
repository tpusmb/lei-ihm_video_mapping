#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os
from threading import Thread, Lock

import cv2
import numpy as np

from py_video_mapping.face_object import FaceObject
from py_video_mapping.frame_getter import FrameGetter
from utils import json_io

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/projector_show.log",
                                                 when="midnight", backupCount=60)
STREAM_HDLR = logging.StreamHandler()
FORMATTER = logging.Formatter("%(asctime)s %(filename)s [%(levelname)s] %(message)s")
HDLR.setFormatter(FORMATTER)
STREAM_HDLR.setFormatter(FORMATTER)
PYTHON_LOGGER.addHandler(HDLR)
PYTHON_LOGGER.addHandler(STREAM_HDLR)
PYTHON_LOGGER.setLevel(logging.DEBUG)

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
PROJECTOR_DATA = "projector_data.map"


class ProjectorShow(Thread):
    def __init__(self, screen, nb_face, delay=20):
        """
        Display image , video on video projector
        :param screen: (Monitor) Information to display the mapping
        :param nb_face: (int) Number of the face to display
        :param delay: (int) Delay between frame (useful for video)
        """
        Thread.__init__(self)
        self.screen = screen
        self.current_image = None
        self.window_name = 'projector'
        self.end = False
        # Read the mapping file creat by the ui interface
        self.projector_positions = json_io.load(PROJECTOR_DATA)
        self.nb_face = nb_face
        if self.projector_positions is not None:
            self.faces_object = [FaceObject(self.screen.width, self.screen.height, *self.projector_positions[i])
                                 for i in range(nb_face)]
        else:
            # If no file detected creat face with no projector information
            self.faces_object = [FaceObject(output_width=self.screen.width, output_height=self.screen.height)
                                 for _ in range(nb_face)]
            self.projector_positions = [None] * nb_face
        self.frame_getter_list = [None, None, None]
        self.wall_paper = self.creat_blank_image()
        self.mutex = Lock()
        self.delay = delay

    def creat_blank_image(self):
        """
        generate a black image with the dimention of the projector
        :return: (ndarray) Black image
        """
        return np.zeros((self.screen.height, self.screen.width, 3), np.uint8)

    def run(self):
        """
        Main method that creat a fullscreen window at the video projector position
        Get all frame of each faces
        Creat a single image to display on to the projector window
        """
        # Creat a full screen window and move to the video projector position
        cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow(self.window_name, self.screen.x - 1, self.screen.y - 1)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while not self.end:
            # Get the wall paper
            output_frame = self.wall_paper.copy()
            self.mutex.acquire()
            # For each faces get the frame getter and the face object
            for frame_getter, face_object in zip(self.frame_getter_list, self.faces_object):
                if frame_getter is None or not face_object.is_ready():
                    continue
                # Get the current frame of a face. And transform the image
                output_frame = face_object.process_image(output_frame, frame_getter.get_image())
            self.mutex.release()
            cv2.imshow(self.window_name, output_frame)
            # Wait before the next frame
            cv2.waitKey(self.delay)

    def display_face(self, face_id, object_to_show: FrameGetter):
        """
        Display something on to face
        :param face_id: (int) 0 to n - 1. Where n his the number of faces
        :param object_to_show: (FrameGetter) video or image to display
        """
        # control the id
        assert 0 <= face_id < len(self.faces_object)
        with self.mutex:
            if self.frame_getter_list[face_id] is not None:
                # Stop the frame getter
                self.frame_getter_list[face_id].stop()
            # Remove the blackout
            self.faces_object[face_id].set_blackout(False)
            # Update the FrameGetter
            self.frame_getter_list[face_id] = object_to_show

    def set_blackout(self, face_id, b: bool):
        """
        Set the face to black out (display black image)
        :param face_id: (int) 0 to n - 1. Where n his the number of faces
        :param b: (bool)
        """
        assert 0 <= face_id < len(self.faces_object)
        with self.mutex:
            self.faces_object[face_id].set_blackout(b)

    def update_face(self, face_id, projector_top_left, projector_top_right,
                    projector_bottom_right, projector_bottom_left):
        """
        Update face projector position
        :param face_id: (int) 0 to n - 1. Where n his the number of faces
        :param projector_top_left: (tuple) Position to display the image in the project (x, y)
        :param projector_top_right: (tuple) Position to display the image in the project (x, y)
        :param projector_bottom_right: (tuple) Position to display the image in the project (x, y)
        :param projector_bottom_left: (tuple) Position to display the image in the project (x, y)
        """
        assert 0 <= face_id < len(self.faces_object)
        with self.mutex:
            self.faces_object[face_id].__init__(self.screen.width, self.screen.height,
                                                projector_top_left, projector_top_right,
                                                projector_bottom_right, projector_bottom_left)
            self.projector_positions[face_id] = [projector_top_left, projector_top_right,
                                                 projector_bottom_right, projector_bottom_left]
        json_io.save(self.projector_positions, PROJECTOR_DATA)

    def stop(self):
        """
        Stop the video mapping
        """
        self.end = True

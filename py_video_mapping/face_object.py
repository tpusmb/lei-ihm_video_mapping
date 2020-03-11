#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

import cv2
import numpy as np

from utils.img_utils import add_sub_image

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/face_object.log",
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


class FaceObject:

    def __init__(self, output_width, output_height,
                 projector_top_left=None, projector_top_right=None,
                 projector_bottom_right=None, projector_bottom_left=None):
        """
        Represent a face to project image or video
        :param output_width: (int) width of the face to project
        :param output_height: (int) Height of the ace to project
        :param projector_top_left: (tuple) Position to display the image in the project (x, y)
        :param projector_top_right: (tuple) Position to display the image in the project (x, y)
        :param projector_bottom_right: (tuple) Position to display the image in the project (x, y)
        :param projector_bottom_left: (tuple) Position to display the image in the project (x, y)
        """
        self.projector_top_left = projector_top_left
        self.projector_top_right = projector_top_right
        self.projector_bottom_right = projector_bottom_right
        self.projector_bottom_left = projector_bottom_left
        self.output_width = output_width
        self.output_height = output_height
        self.blackout = False
        self.perspective_mat = None

    def transform_image(self, frame):
        """
        Function to transform the input frame to the projector positions
        :param frame: (ndarray) Frame to transform
        :return: (ndarray) Deform frame
        """
        h, w, _ = frame.shape
        # Source a mat of the image
        rect = np.array([
            [0, 0],
            [w - 1, 0],
            [w - 1, h - 1],
            [0, h - 1]], dtype="float32")
        # Destination mat into the projector
        dst = np.array([
            self.projector_top_left,
            self.projector_top_right,
            self.projector_bottom_right,
            self.projector_bottom_left
        ], dtype="float32")
        # Get perspective mat
        self.perspective_mat = cv2.getPerspectiveTransform(rect, dst)
        # Transform image
        warped = cv2.warpPerspective(frame, self.perspective_mat, (self.output_width, self.output_height))
        # Now we just get the part of the image with color pixel
        min_x = min(self.projector_top_left[0], self.projector_bottom_left[0])
        max_x = max(self.projector_top_right[0], self.projector_bottom_right[0])
        min_y = min(self.projector_top_left[1], self.projector_top_right[1])
        max_y = max(self.projector_bottom_left[1], self.projector_bottom_right[1])
        return warped[min_y:max_y, min_x:max_x]

    def is_ready(self):
        """
        Control if projector parameters are ready
        :return: (bool)
        """
        return self.projector_top_left is not None and self.projector_top_right is not None \
               and self.projector_bottom_right is not None and self.projector_bottom_left

    def set_blackout(self, b: bool):
        """
        Set the face to black out (return image)
        :param b: (bool)
        """
        self.blackout = b

    def process_image(self, wall_paper, frame):
        """
        Transform the input frame to the projector positions. And add the transform image into the wall paper image
        :param wall_paper: (ndarray) Wall paper to add the image
        :param frame: (ndarray) Frame to transform
        :return: (ndarray) the wall paper with the transform image.
            If you are in blackout mode we just return the wall paper
        """
        assert self.is_ready()
        if self.blackout:
            return wall_paper
        wrap = self.transform_image(frame)
        return add_sub_image(wall_paper, wrap, *self.projector_top_left)

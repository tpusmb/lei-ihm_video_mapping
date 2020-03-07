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

        :param output_width:
        :param projector_top_left: (tuple) x, y
        :param output_height:
        :param projector_top_right:
        :param projector_bottom_right:
        :param projector_bottom_left:
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

        :param frame:
        :return:
        """
        # TODO if self.perspective_mat is None:
        h, w, _ = frame.shape
        rect = np.array([
            [0, 0],
            [w - 1, 0],
            [w - 1, h - 1],
            [0, h - 1]], dtype="float32")
        dst = np.array([
            self.projector_top_left,
            self.projector_top_right,
            self.projector_bottom_right,
            self.projector_bottom_left
        ], dtype="float32")
        self.perspective_mat = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(frame, self.perspective_mat, (self.output_width, self.output_height))
        min_x = min(self.projector_top_left[0], self.projector_bottom_left[0])
        max_x = max(self.projector_top_right[0], self.projector_bottom_right[0])
        min_y = min(self.projector_top_left[1], self.projector_top_right[1])
        max_y = max(self.projector_bottom_left[1], self.projector_bottom_right[1])
        return warped[min_y:max_y, min_x:max_x]

    def is_ready(self):
        return self.projector_top_left is not None and self.projector_top_right is not None \
               and self.projector_bottom_right is not None and self.projector_bottom_left

    def set_blackout(self, b: bool):
        self.blackout = b

    def process_image(self, wall_paper, frame):
        assert self.is_ready()
        if self.blackout:
            return wall_paper
        wrap = self.transform_image(frame)
        return add_sub_image(wall_paper, wrap, *self.projector_top_left)

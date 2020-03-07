#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os
import cv2
import numpy as np

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/img_utils.log",
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


def add_sub_image(wall_paper, frame, x_offset, y_offset):
    """

    :param wall_paper:
    :param frame:
    :param x_offset:
    :param y_offset:
    :return:
    """
    wall_paper_copy = wall_paper.copy()
    try:
        wall_paper_copy[y_offset:y_offset + frame.shape[0], x_offset:x_offset + frame.shape[1]] = frame
    except ValueError:
        pass
    return wall_paper_copy


def draw_text_onto_image(image, text, x_offset, y_offset, scale, color=(0, 0, 0), letters_thickness=5):
    org = (x_offset, y_offset)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = scale
    thickness = letters_thickness
    return cv2.putText(image, text, org, font, font_scale, color, thickness, cv2.LINE_AA)


def xp_bar_draw(xp_in_percent):
    max_width = 1080
    height = 700
    width = int((xp_in_percent * max_width) // 100)
    img = np.zeros((height, max_width, 3), np.uint8)

    x = np.ones((height, width, 3))
    x[:, :, 0:3] = np.random.randint(0, 200, (3,))
    img[:, 0:width] = x
    return draw_text_onto_image(img, "{}%".format(int(xp_in_percent)), width // 2, height // 2, 3, (255, 255, 255))

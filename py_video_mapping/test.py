#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

import cv2

from py_video_mapping import PyVideoMapping

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/test.log",
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

py_video_mapping = PyVideoMapping(PyVideoMapping.get_all_screens()[0])
square = cv2.imread("square.png")

h, w, _ = py_video_mapping.get_image_size(square)

wall_paper = py_video_mapping.creat_blank_image()
top_left = [(w // 2) - 10, 0]
top_right = [(w // 2) + 10, 0]
bottom_right = [w, h]
bottom_left = [0, h]

wrap = py_video_mapping.transform_image(square, top_left, top_right, bottom_right, bottom_left, w, h)

frame = py_video_mapping.add_sub_image(wall_paper, wrap, 100, 100)

py_video_mapping.show_to_projector(frame)

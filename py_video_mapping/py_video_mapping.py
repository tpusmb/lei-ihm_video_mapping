#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os
import time
from threading import Thread

import cv2
import imutils
import numpy as np
import screeninfo
from screeninfo import Monitor

from utils import save_mapping
from .screen_relation import ScreenRelation

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/py_video_mapping.log",
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

TEST_IMAGE = os.path.join(FOLDER_ABSOLUTE_PATH, "test_image.jpg")
PROJECTOR_DATA = "projector_data.json"


class ImgShow(Thread):
    def __init__(self, mutex, screen):
        ''' Constructor. '''
        Thread.__init__(self)
        self.mutex = mutex
        self.screen = screen
        self.current_image = None
        self.window_name = 'projector'
        self.end = False

    def run(self):

        cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow(self.window_name, self.screen.x - 1, self.screen.y - 1)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while not self.end:
            if self.current_image is not None:
                cv2.imshow(self.window_name, self.current_image)
                cv2.waitKey(1)
            time.sleep(0.1)

    def show_image(self, img):
        self.current_image = img.copy()

    def stop(self):
        self.end = True


class PyVideoMapping:
    def __init__(self, screen, ui_screen: Monitor = None):
        self.screen = screen
        self.ui_screen = ui_screen
        self.screen_relation = None
        self.wall_paper = self.creat_blank_image()
        self.test_image = cv2.imread(TEST_IMAGE)
        self.img_show = ImgShow(None, self.screen)
        if self.ui_screen is not None:
            self.screen_relation = ScreenRelation(ui_screen, self.screen)
        self.img_show.start()

    @staticmethod
    def get_image_size(frame):
        """

        :param frame:
        :return: (tuple) height, width
        """
        return frame.shape

    @staticmethod
    def get_all_screens():
        return screeninfo.get_monitors()

    @staticmethod
    def resize(frame, width, height):
        return imutils.resize(frame, width=width, height=height)

    @staticmethod
    def add_sub_image(wall_paper, frame, x_offset, y_offset):
        wall_paper_copy = wall_paper.copy()
        wall_paper_copy[y_offset:y_offset + frame.shape[0], x_offset:x_offset + frame.shape[1]] = frame
        return wall_paper_copy

    @staticmethod
    def transform_image(frame, top_left, top_right, bottom_right, bottom_left, output_width, output_height):
        """

        :param frame:
        :param top_left: (tuple) x, y
        :param top_right: (tuple) x, y
        :param bottom_right: (tuple) x, y
        :param bottom_left: (tuple) x, y
        :param output_width:
        :param output_height:
        :return:
        """
        h, w, _ = frame.shape
        rect = np.array([
            [0, 0],
            [w - 1, 0],
            [w - 1, h - 1],
            [0, h - 1]], dtype="float32")

        dst = np.array([
            top_left,
            top_right,
            bottom_right,
            bottom_left
        ], dtype="float32")

        m = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(frame, m, (output_width, output_height))
        min_x = min(top_left[0], bottom_left[0])
        max_x = max(top_right[0], bottom_right[0])
        min_y = min(top_left[1], top_right[1])
        max_y = max(bottom_left[1], bottom_right[1])
        return warped[min_y:max_y, min_x:max_x]

    def change_ui_screen(self, ui_screen: Monitor):
        self.ui_screen = ui_screen
        self.screen_relation = ScreenRelation(self.ui_screen, self.screen)

    def creat_blank_image(self):
        return np.zeros((self.screen.height, self.screen.width, 3), np.uint8)

    def show_to_projector(self, frame, blocking=True):
        self.img_show.show_image(frame)

    def transform_and_add(self, frame, projector_top_left, projector_top_right,
                          projector_bottom_right, projector_bottom_left):
        """

        :param frame:
        :param projector_top_left:
        :param projector_top_right:
        :param projector_bottom_right:
        :param projector_bottom_left:
        :return:
        """
        wrap = self.transform_image(self.test_image, projector_top_left, projector_top_right,
                                    projector_bottom_right, projector_bottom_left,
                                    self.screen.width, self.screen.height)
        return self.add_sub_image(frame, wrap, *projector_top_left)

    def mapping_calibration(self, ui_images):
        """

        :param ui_images: (list) All test image to display into the projector
                                    Image 1
            [ [ui_top_left, ui_top_right, ui_bottom_right, ui_bottom_left], ... ]
            ui_top_left = x, y
        :return:
        """
        new_positions = []
        if self.screen_relation is None:
            raise ValueError("Need to provide ui screen in the constructor")
        output_frame = self.wall_paper.copy()
        # Get all image tuple (tuple) x, y
        for ui_top_left, ui_top_right, ui_bottom_right, ui_bottom_left in ui_images:
            projector_top_left = self.screen_relation.to_projector_screen(*ui_top_left)
            projector_top_right = self.screen_relation.to_projector_screen(*ui_top_right)
            projector_bottom_right = self.screen_relation.to_projector_screen(*ui_bottom_right)
            projector_bottom_left = self.screen_relation.to_projector_screen(*ui_bottom_left)
            new_positions.append([projector_top_left, projector_top_right,
                                  projector_bottom_right, projector_bottom_left])
            output_frame = self.transform_and_add(output_frame, projector_top_left, projector_top_right,
                                                  projector_bottom_right, projector_bottom_left)
        self.show_to_projector(output_frame, blocking=False)
        save_mapping.save(new_positions, PROJECTOR_DATA)
        return new_positions

    def show_save_projector_positions(self):
        projector_positions = save_mapping.load(PROJECTOR_DATA)
        if projector_positions is None:
            PYTHON_LOGGER.info("No projector save positions")
            return
        output_frame = self.wall_paper.copy()
        for projector_top_left, projector_top_right, projector_bottom_right, projector_bottom_left \
                in projector_positions:
            output_frame = self.transform_and_add(output_frame, projector_top_left, projector_top_right,
                                                  projector_bottom_right, projector_bottom_left)
        self.show_to_projector(output_frame, blocking=False)

    def stop(self):
        self.img_show.stop()

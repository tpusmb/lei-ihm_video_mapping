#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

import cv2
import screeninfo
from screeninfo import Monitor

from .frame_getter import ImageGetter, VideoGetter, VideoOnWallpaper
from .projector_show import ProjectorShow
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
NB_FACES = 3


class PyVideoMapping:
    def __init__(self, screen, ui_screen: Monitor = None, delay=22):
        self.screen = screen
        self.ui_screen = ui_screen
        self.screen_relation = None
        self.test_image = cv2.imread(TEST_IMAGE)
        self.projector_show = ProjectorShow(self.screen, NB_FACES, delay)

        if self.ui_screen is not None:
            self.screen_relation = ScreenRelation(ui_screen, self.screen)
        self.projector_show.start()

        for i in range(NB_FACES):
            self.projector_show.display_face(i, ImageGetter(self.test_image))

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

    def change_ui_screen(self, ui_screen: Monitor):
        self.ui_screen = ui_screen
        self.screen_relation = ScreenRelation(self.ui_screen, self.screen)

    def mapping_calibration(self, ui_images):
        """

        :param ui_images: (list) All test image to display into the projector
                                    Image 1
            [ [ui_top_left, ui_top_right, ui_bottom_right, ui_bottom_left], ... ]
            ui_top_left = x, y
        :return:
        """
        if self.screen_relation is None:
            raise ValueError("Need to provide ui screen in the constructor")
        # Get all image tuple (tuple) x, y
        for face_id in range(len(ui_images)):
            ui_top_left, ui_top_right, ui_bottom_right, ui_bottom_left = ui_images[face_id]
            projector_top_left = self.screen_relation.to_projector_screen(*ui_top_left)
            projector_top_right = self.screen_relation.to_projector_screen(*ui_top_right)
            projector_bottom_right = self.screen_relation.to_projector_screen(*ui_bottom_right)
            projector_bottom_left = self.screen_relation.to_projector_screen(*ui_bottom_left)
            self.projector_show.update_face(face_id, projector_top_left, projector_top_right,
                                            projector_bottom_right, projector_bottom_left)

    def show_video(self, face_id: int, video_path: str, enable_audio: bool = False):
        self.projector_show.display_face(face_id, VideoGetter(video_path, enable_audio))

    def show_image(self, face_id: int, image_path):
        """

        :param face_id:
        :param image_path: image path or ndarray
        :return:
        """
        if isinstance(image_path, str):
            image = cv2.imread(image_path)
        else:
            image = image_path
        self.projector_show.display_face(face_id, ImageGetter(image))

    def show_video_on_wallpaper(self, face_id: int, video_path: str, image_path,
                                x_offset: int, y_offset: int, width: int, height: int,
                                play_video_audio: bool = False):
        """

        :param face_id:
        :param video_path:
        :param image_path: image path or ndarray
        :param x_offset:
        :param y_offset:
        :param width:
        :param height:
        :param play_video_audio:
        :return:
        """
        if isinstance(image_path, str):
            image = cv2.imread(image_path)
        else:
            image = image_path
        self.projector_show.display_face(face_id,
                                         VideoOnWallpaper(image, video_path, x_offset, y_offset, width, height,
                                                          play_video_audio))

    def set_blackout(self, face_id, b: bool):
        """

        :param face_id:
        :param b:
        :return:
        """
        self.projector_show.set_blackout(face_id, b)

    def stop(self):
        self.projector_show.stop()

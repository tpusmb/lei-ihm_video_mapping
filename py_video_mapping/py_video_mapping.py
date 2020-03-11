#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

import cv2
import screeninfo
from screeninfo import Monitor

from utils.config_reader import ConfigReader
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
# We have 3 face
NB_FACES = 3


class PyVideoMapping:
    def __init__(self, screen: Monitor, ui_screen: Monitor = None, config_reader: ConfigReader = ConfigReader()):
        """
        Class to display image or video onto faces.
        :param screen: (Monitor) Screen to display the mapping
        :param ui_screen: (Monitor) Screen information of the ui (use by the web interface)
        :param config_reader: (ConfigReader) Config file class
        """
        self.config_reader = config_reader
        self.screen = screen
        self.ui_screen = ui_screen
        self.screen_relation = None
        self.test_image = cv2.imread(TEST_IMAGE)
        # Start the projector show
        self.projector_show = ProjectorShow(self.screen, NB_FACES, config_reader.Py_video_mapping.getint("delay"))

        if self.ui_screen is not None:
            self.screen_relation = ScreenRelation(ui_screen, self.screen)
        self.projector_show.start()

        # creat faces
        for i in range(NB_FACES):
            self.projector_show.display_face(i, ImageGetter(self.test_image))

    @staticmethod
    def get_image_size(frame):
        """
        Get the size of a image
        :param frame: (ndarray)
        :return: (tuple) height, width
        """
        return frame.shape

    @staticmethod
    def get_all_screens():
        """
        :return: (list of Monitor) Return all connected monitors
        """
        return screeninfo.get_monitors()

    def change_ui_screen(self, ui_screen: Monitor):
        """
        Change the ui screen
        :param ui_screen: (Monitor) Screen information of the ui (use by the web interface)
        """
        self.ui_screen = ui_screen
        self.screen_relation = ScreenRelation(self.ui_screen, self.screen)

    def mapping_calibration(self, ui_images):
        """
        Update test images on the video projector screen
        :param ui_images: (list) All test image to display into the projector
                                    Image 1
            [ [ui_top_left, ui_top_right, ui_bottom_right, ui_bottom_left],
                                    ...,
                                    Image n
              [ui_top_left, ui_top_right, ui_bottom_right, ui_bottom_left]
            ui_top_left, ui_top_right, ui_bottom_right, ui_bottom_left: (tuple) x, y
        """
        if self.screen_relation is None:
            raise ValueError("Need to provide ui screen in the constructor")
        # Get all image tuple (tuple) x, y
        for face_id in range(len(ui_images)):
            ui_top_left, ui_top_right, ui_bottom_right, ui_bottom_left = ui_images[face_id]
            # Get the position into the video projector
            projector_top_left = self.screen_relation.to_projector_screen(*ui_top_left)
            projector_top_right = self.screen_relation.to_projector_screen(*ui_top_right)
            projector_bottom_right = self.screen_relation.to_projector_screen(*ui_bottom_right)
            projector_bottom_left = self.screen_relation.to_projector_screen(*ui_bottom_left)
            self.projector_show.update_face(face_id, projector_top_left, projector_top_right,
                                            projector_bottom_right, projector_bottom_left)

    def show_video(self, face_id: int, video_path: str, enable_audio: bool = False):
        """
        display a video on face
        :param face_id: (int) 0 to n - 1. Where n his the number of faces
        :param video_path: (string) Path to read the video
        :param enable_audio: (bool) If true play the audio of the file
        """
        self.projector_show.display_face(face_id, VideoGetter(video_path, enable_audio))

    def show_image(self, face_id: int, image_path):
        """
        Display a image on face
        :param face_id: (int) 0 to n - 1. Where n his the number of faces
        :param image_path: (string or ndarray) image path to show or frame to show
        :return:
        """
        if isinstance(image_path, str):
            image = cv2.imread(image_path)
        else:
            image = image_path
        if image is not None:
            self.projector_show.display_face(face_id, ImageGetter(image))
        else:
            PYTHON_LOGGER.error("Image path {} not found".format(image_path))

    def show_video_on_wallpaper(self, face_id: int, video_path: str, image_path,
                                x_offset: int, y_offset: int, width: int, height: int,
                                play_video_audio: bool = False):
        """
        Display a video on wallpaper
        :param face_id: (int) 0 to n - 1. Where n his the number of faces
        :param video_path: (string) Path to read the video
        :param image_path: (string or ndarray) image path to show or frame to show
        :param x_offset: (int) X position of the video
        :param y_offset: (int) y position of the video
        :param width: (int) width of the video
        :param height: (int) height of the video
        :param play_video_audio: (bool) If true play audio of the video
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
        Set the face to black out (display black image)
        :param face_id: (int) 0 to n - 1. Where n his the number of faces
        :param b: (bool)
        """
        self.projector_show.set_blackout(face_id, b)

    def stop(self):
        """
        Stop the mapping
        """
        self.projector_show.stop()

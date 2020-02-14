#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os
from abc import ABC, abstractmethod
from threading import Thread, Lock

import cv2
import imutils
import numpy as np
import screeninfo
from screeninfo import Monitor
from ffpyplayer.player import MediaPlayer

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
PROJECTOR_DATA = "projector_data.map"
NB_FACES = 3


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


class FrameGetter(ABC):

    @abstractmethod
    def get_image(self):
        pass


class VideoGetter(FrameGetter):

    def __init__(self, path_video):
        self.path_video = path_video
        self.video_capture = cv2.VideoCapture(self.path_video)

    def get_image(self):
        _, frame = self.video_capture.read()
        if frame is None:
            self.video_capture.release()
            self.video_capture = cv2.VideoCapture(self.path_video)
            _, frame = self.video_capture.read()
        return frame


class ImageGetter(FrameGetter):

    def __init__(self, image):
        self.image = image

    def get_image(self):
        return self.image


class VideoOnWallpaper(FrameGetter):

    def __init__(self, image, video_path, x_offset, y_offset, width, height):
        """

        :param image:
        :param video_path:
        :param x_offset:
        :param y_offset:
        :param width:
        :param height:
        """
        offset_ok = 0 <= x_offset < image.shape[1] and 0 <= y_offset < image.shape[1]
        dim_ok = 0 < width < image.shape[1] and 0 < height < image.shape[0]
        assert offset_ok and dim_ok
        self.video_getter = VideoGetter(video_path)
        self.image_getter = ImageGetter(image)
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.width = width
        self.height = height


def get_image(self):
    video_img = self.video_getter.get_image()
    wall_paper = self.image_getter.get_image()
    video_img = imutils.resize(video_img, width=self.width, height=self.height)
    wall_image = add_sub_image(wall_paper, video_img, self.x_offset, self.y_offset)
    return wall_image


class ProjectorShow(Thread):
    def __init__(self, screen, nb_face):
        """

        :param screen:
        """
        Thread.__init__(self)
        self.screen = screen
        self.current_image = None
        self.window_name = 'projector'
        self.end = False
        self.projector_positions = save_mapping.load(PROJECTOR_DATA)
        self.nb_face = nb_face
        if self.projector_positions is not None:
            self.faces_object = [FaceObject(self.screen.width, self.screen.height, *self.projector_positions[i])
                                 for i in range(nb_face)]
        else:
            self.faces_object = [FaceObject(output_width=self.screen.width, output_height=self.screen.height)
                                 for _ in range(nb_face)]
            self.projector_positions = [None] * nb_face
        self.frame_getter_list = [None, None, None]
        self.wall_paper = self.creat_blank_image()
        self.mutex = Lock()

    def creat_blank_image(self):
        return np.zeros((self.screen.height, self.screen.width, 3), np.uint8)

    def run(self):

        cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow(self.window_name, self.screen.x - 1, self.screen.y - 1)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while not self.end:
            output_frame = self.wall_paper.copy()
            self.mutex.acquire()
            for frame_getter, face_object in zip(self.frame_getter_list, self.faces_object):
                if frame_getter is None or not face_object.is_ready():
                    continue
                output_frame = face_object.process_image(output_frame, frame_getter.get_image())
            self.mutex.release()
            cv2.imshow(self.window_name, output_frame)
            cv2.waitKey(1)

    def display_face(self, face_id, object_to_show: FrameGetter):
        """

        :param face_id: 0 to 2
        :param object_to_show: video or image
        :return:
        """
        assert 0 <= face_id < len(self.faces_object)
        with self.mutex:
            self.faces_object[face_id].set_blackout(False)
            self.frame_getter_list[face_id] = object_to_show

    def set_blackout(self, face_id, b: bool):
        assert 0 <= face_id < len(self.faces_object)
        with self.mutex:
            self.faces_object[face_id].set_blackout(b)

    def update_face(self, face_id, projector_top_left, projector_top_right,
                    projector_bottom_right, projector_bottom_left):
        """

        :param face_id:
        :param projector_top_left: (tuple) x, y
        :param projector_top_right:
        :param projector_bottom_right:
        :param projector_bottom_left:
        :return:
        """
        assert 0 <= face_id < len(self.faces_object)
        with self.mutex:
            self.faces_object[face_id].__init__(self.screen.width, self.screen.height,
                                                projector_top_left, projector_top_right,
                                                projector_bottom_right, projector_bottom_left)
            self.projector_positions[face_id] = [projector_top_left, projector_top_right,
                                                 projector_bottom_right, projector_bottom_left]
        save_mapping.save(self.projector_positions, PROJECTOR_DATA)

    def stop(self):
        self.end = True


class PyVideoMapping:
    def __init__(self, screen, ui_screen: Monitor = None):
        self.screen = screen
        self.ui_screen = ui_screen
        self.screen_relation = None
        self.test_image = cv2.imread(TEST_IMAGE)
        self.projector_show = ProjectorShow(self.screen, NB_FACES)
        self.player = MediaPlayer("")

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

    def show_video(self, face_id: int, video_path: str, enable_audio: bool):
        self.projector_show.display_face(face_id, VideoGetter(video_path))
        if enable_audio:
            self.play_audio(video_path)

    def show_image(self, face_id: int, image_path: str):
        image = cv2.imread(image_path)
        self.projector_show.display_face(face_id, ImageGetter(image))

    def show_video_on_wallpaper(self, face_id: int, video_path: str, image_path: str,
                                x_offset: int, y_offset: int, width: int, height: int):
        image = cv2.imread(image_path)
        self.projector_show.display_face(face_id,
                                         VideoOnWallpaper(image, video_path, x_offset, y_offset, width, height))

    def set_blackout(self, face_id, b: bool):
        """

        :param face_id:
        :param b:
        :return:
        """
        self.projector_show.set_blackout(face_id, b)

    def play_audio(self, video_path):
        self.player = MediaPlayer(video_path)
        frame, val = self.player.get_frame()
        while val != 'eof':
            frame, val = self.player.get_frame()
        self.player.close_player()

    def stop(self):
        self.projector_show.stop()
